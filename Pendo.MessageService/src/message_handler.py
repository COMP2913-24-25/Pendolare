from enum import Enum
import json
from typing import Dict, Set, List
from datetime import datetime, timezone
import logging
import websockets

logger = logging.getLogger(__name__)

"""
Code derived from websockets documentation & example code
Reference: https://websockets.readthedocs.io/en/stable/topics/index.html
"""

class MessageType(Enum):
    CHAT = "chat",
    HISTORY_REQUEST = "history_request",
    HISTORY_RESPONSE = "history_response",
    JOIN_CONVERSATION = "join_conversation", 
    LEAVE_CONVERSATION = "leave_conversation",

class MessageHandler:
    def __init__(self, repository=None):
        # User connections and sessions
        self.connections: Dict[str, object] = {}
        self.user_sessions: Dict[str, object] = {}
        self.repository = repository  # Database repository

        # In memory data and user connections
        # Provides quick access to messages and user connections
        self.message_cache: Dict[str, List[Dict]] = {}
        self.user_connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.conversations: Dict[str, Set[str]] = {}
        self.message_store: Dict[str, list] = {}

        logger.info("MessageHandler initialised")
    
    def register_user(self, user_id: str, websocket: websockets.WebSocketServerProtocol):
        """
        Register a user connection

        Parameters:
            user_id (str): Unique user identifier
            websocket (websockets.WebSocketServerProtocol): Websocket connection object
        
        Returns:
            None
        """
        self.connections[user_id] = websocket
        # Create message cache for user
        if user_id not in self.message_cache:
            self.message_cache[user_id] = []

        self.user_connections[user_id] = websocket
        logger.info(f"User {user_id} registered")
    
    def remove_user(self, user_id: str):
        """
        Remove a user connection

        Parameters:
            user_id (str): Unique user
        
        Returns:
            None
        """
        if user_id in self.connections:
            del self.connections[user_id]
        if user_id in self.user_connections:
            del self.user_connections[user_id]
            for conv_id, users in list(self.conversations.items()):
                if user_id in users:
                    users.remove(user_id)

                    # Remove conversation from memory if empty
                    if not users:
                        del self.conversations[conv_id]

            logger.info(f"User {user_id} removed")

    async def _handle_history_request(self, websocket, data):
        """
        Handle request for message history for a conversation and send back to the requester
        
        Parameters:
            websocket (websockets.WebSocketServerProtocol): Websocket connection object
            data (dict): Message data
        Returns:
            None
        """

        if not all(k in data for k in ('conversation_id', 'user_id')):
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Missing conversation_id or user_id"
            }))
            return
        
        conversation_id = data['conversation_id']
        since_timestamp = data.get('since_timestamp')
        
        messages = []
        if self.repository:
            messages = self.repository.get_messages_by_conversation_id(conversation_id)
            if since_timestamp:
                messages = [msg for msg in messages if msg.CreateDate.isoformat() > since_timestamp]
        else:
            messages = self.message_store.get(conversation_id, [])
            if since_timestamp:
                messages = [msg for msg in messages if msg.get('timestamp', '') > since_timestamp]
        
        response = {
            'type': 'history_response',
            'messages': messages
        }

        # Send the response only to the requesting user's websocket
        await websocket.send(json.dumps(response))

    async def handle_message(self, websocket, message):
        """
        Handle incoming messages
        
        Parameters:
            websocket (websockets.WebSocketServerProtocol): Websocket connection object
            message (str): JSON message string
        Returns:
            None
        """
        data = json.loads(message)
        
        # Register user if this is an authentication message
        if 'register' in data and data['register'] and 'user_id' in data:
            self.register_user(data['user_id'], websocket)
            return
            
        # Direct handling for specific message types without enum validation
        message_type = data.get('type')
        
        match message_type:
            case 'history_request':
                await self._handle_history_request(websocket, data)
                return
            case 'join_conversation':
                await self._handle_join_conversation(data)
                return
            case 'leave_conversation':
                await self._handle_leave_conversation(data)
                return
            case 'chat':
                await self._handle_chat_message(data)
                return

    async def _handle_chat_message(self, message):
        """
        Handle a chat message
        
        Parameters:
            message (dict): Chat message data

        Returns:
            None
        """
        if not all(k in message for k in ['from', 'conversation_id', 'content']):
            logger.error("Incomplete chat message")
            return

        # Add timestamp if not provided
        if 'timestamp' not in message:
            message['timestamp'] = datetime.now(timezone.utc).isoformat()  # ...changed...
        
        # Store message in memory
        conversation_id = message['conversation_id']
        if conversation_id not in self.message_store:
            self.message_store[conversation_id] = []
        self.message_store[conversation_id].append(message)
        
        # Store message in database if repository is available
        try:
            if self.repository:
                self.repository.save_message(
                    conversation_id=conversation_id,
                    sender_id=message['from'],
                    message_type='chat',
                    content=message['content']
                )
        except Exception as e:
            logger.error(f"Error saving chat message to database: {str(e)}")
        
        # Log message for debugging
        logger.debug(f"Broadcasting message to conversation {conversation_id}: {message}")
        
        # Broadcast to all users in this conversation except the sender
        await self._broadcast_to_conversation(conversation_id, message, exclude_user=message['from'])
        
    
    async def _handle_join_conversation(self, message):
        """
        Handle user joining a conversation
        
        Parameters:
            message (dict): Join conversation

        Returns:
            None
        """
        if not all(k in message for k in ['user_id', 'conversation_id']):
            return
        
        user_id = message['user_id']
        conversation_id = message['conversation_id']
        
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = set()
        
        # Add user to conversation in memory
        self.conversations[conversation_id].add(user_id)
        logger.info(f"User {user_id} joined conversation {conversation_id}")
        
        # Add user to conversation in database if repository is available
        try:
            if self.repository:
                self.repository.add_user_to_conversation(
                    conversation_id=conversation_id,
                    user_id=user_id
                )
        except Exception as e:
            logger.error(f"Error adding user to conversation in database: {str(e)}")
        
        # Send confirmation to the user
        user_socket = self.user_connections.get(user_id)
        if user_socket:
            await user_socket.send(json.dumps({
                'type': 'conversation_joined',
                'conversation_id': conversation_id,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'message': f'Successfully joined conversation {conversation_id}'
            }))
            
            # Retrieve conversation history
            await self._handle_history_request(user_socket, message)
        
        # Notify other users in the conversation
        join_notification = {
            'type': 'user_joined',
            'user_id': user_id,
            'conversation_id': conversation_id,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        await self._broadcast_to_conversation(conversation_id, join_notification, exclude_user=user_id)

    async def _broadcast_to_conversation(self, conversation_id, message, exclude_user=None):
        """
        Broadcast a message to all users in a conversation, optionally excluding one user
        
        Parameters:
            conversation_id (str): Conversation identifier
            message (dict): Message to broadcast
            exclude_user (str): Optional user to exclude from broadcast
        
        Returns:
            None
        """
        if conversation_id not in self.conversations:
            return
            
        for user_id in self.conversations[conversation_id]:
            # Skip the excluded user if specified
            if exclude_user and user_id == exclude_user:
                # Echo back to sender for confirmation
                response = {
                    'type': 'user_message_sent',
                    'timestamp': datetime.now(timezone.utc).isoformat(),  # ...changed...
                    'status': 'delivered' if len(self.conversations[conversation_id]) > 2 else 'stored'
                }

                try:
                    await self.user_connections[user_id].send(json.dumps(response))
                except websockets.exceptions.ConnectionClosed:
                    logger.info(f"Connection closed for user {user_id}")
                    self.remove_user(user_id)
    
                continue
                
            if user_id in self.user_connections:
                try:
                    await self.user_connections[user_id].send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    logger.info(f"Connection closed for user {user_id}")
                    self.remove_user(user_id)

    async def _handle_leave_conversation(self, message):
        """
        Handle user leaving a conversation
        
        Parameters:
            message (dict): Leave conversation
        
        Returns:
            None
        """
        if not all(k in message for k in ['user_id', 'conversation_id']):
            return
            
        user_id = message['user_id'] 
        conversation_id = message['conversation_id']
        
        if conversation_id in self.conversations and user_id in self.conversations[conversation_id]:
            self.conversations[conversation_id].remove(user_id)
            logger.info(f"User {user_id} left conversation {conversation_id}")
            
            # Remove conversation if empty
            if not self.conversations[conversation_id]:
                del self.conversations[conversation_id]
