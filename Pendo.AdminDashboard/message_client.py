import requests
import json
from websocket import create_connection

class MessageClient:
    def __init__(self, base_url, logger, jwt=None):
        self.base_url = base_url
        self.logger = logger
        self.jwt = jwt
        self.ws = None  # persistent WebSocket connection

    def _get_headers(self):
        headers = {}
        if self.jwt:
            token = f"Bearer {self.jwt}"
            headers["Authorization"] = token
            # Removed logging of the JWT to avoid exposing sensitive information:
            # self.logger.debug(f"JWT header: {token}")
        return headers

    def open_conversation(self, participant):
        """
        Calls the messaging service API to create a new conversation.
        The payload follows the CreateConversationRequest schema.
        :param participant: The user id (uuid) of the person to chat with.
        :return: The JSON data from the service if successful.
        """
        self.logger.info("Starting new conversation via message service")
        url = f"{self.base_url}/CreateConversation"
        # Note: Adjust "UserId" with the administrator's identifier if available.
        payload = {
            "UserId": "00000000-0000-0000-0000-000000000000",  # Replace with the actual admin UUID if available
            "ConversationType": "adminChat",
            "participants": [participant]
        }
        response = requests.post(
            url,
            json=payload,
            headers=self._get_headers(),
            verify=True
        )

        if response.status_code == 200:
            self.logger.info("Conversation started successfully")
            return response.json()
        else:
            self.logger.error(f"Failed to start conversation: {response.status_code} - {response.text}")
            return None

    def get_user_conversations(self, user_id):
        self.logger.info("Fetching user conversations")
        url = f"{self.base_url}/SupportConversation"
        payload = {"UserId": user_id}
        self.logger.debug(f"get_user_conversations payload: {payload}")  # Log the payload being sentHow 
        response = requests.get(
            url,
            json=payload,  # using JSON body as per spec
            headers=self._get_headers(),
            verify=True
        )
        if response.status_code == 200:
            self.logger.info("User conversations retrieved successfully")
            return response.json()
        else:
            self.logger.error(f"Failed to get user conversations: {response.status_code} - {response.text}")
            return None

    def join_conversation(self, user_id, conversation_id):
        self.logger.info("Joining conversation and requesting history via WebSocket")
        ws_url = "wss://pendo-message.clsolutions.dev/ws/"
        try:
            self.ws = create_connection(ws_url, header=self._get_headers())
            # Send join payload
            join_payload = {
                "join_conversation": True,
                "user_id": user_id,
                "conversation_id": conversation_id
            }
            self.ws.send(json.dumps(join_payload))
            join_response = json.loads(self.ws.recv())
            self.logger.info(f"Joined conversation, response: {join_response}")
            
            # Send history request payload
            history_payload = {
                "type": "history_request",
                "user_id": user_id,
                "conversation_id": conversation_id,
            }
            self.ws.send(json.dumps(history_payload))
            history_response = json.loads(self.ws.recv())
            self.logger.info(f"History response received: {history_response}")
            
            # Collect and transform messages from history_response
            messages = []
            if isinstance(history_response, dict) and "messages" in history_response:
                messages = history_response["messages"]
            elif isinstance(history_response, list):
                messages = history_response
            
            # Transform each message to include 'from', 'content', and 'timestamp'
            for msg in messages:
                if "SenderId" in msg:
                    msg["from"] = msg["SenderId"]
                if "Content" in msg:
                    msg["content"] = msg["Content"]
                if "CreateDate" in msg:
                    msg["timestamp"] = msg["CreateDate"]
                self.logger.debug(f"Transformed history message: {msg}")
            
            # Return a cleaned-up response containing only transformed messages
            return {"messages": messages}
        except Exception as e:
            self.logger.error(f"Failed to join conversation via WebSocket: {e}")
            return None

    def send_chat_message(self, sender, conversation_id, content, timestamp):
        """
        Sends a chat message via WebSocket.
        
        Expected payload format:
          {
            "type": "chat",
            "from": sender,
            "conversation_id": conversation_id,
            "content": content,
            "timestamp": timestamp
          }
        """
        self.logger.info("Sending chat message using persistent WebSocket connection")
        if self.ws and not self.ws.closed:
            payload = {
                "type": "chat",
                "from": sender,
                "conversation_id": conversation_id,
                "content": content,
                "timestamp": timestamp
            }
            self.ws.send(json.dumps(payload))
            response = json.loads(self.ws.recv())
            self.logger.info(f"Chat message sent, response: {response}")
            return response
        else:
            self.logger.error("No persistent WebSocket connection available")
            return None

    def close_connection(self):
        if self.ws:
            self.ws.close()
            self.logger.info("Persistent WebSocket connection closed")


