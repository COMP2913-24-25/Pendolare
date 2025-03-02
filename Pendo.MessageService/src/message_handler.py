from enum import Enum
import json
import time
from typing import Dict, Set, List
from datetime import datetime
import logging
import asyncio
import websockets

logger = logging.getLogger(__name__)

class MessageType(Enum):
    USER_TO_USER = "user_message"
    SUPPORT_TO_USER = "support_message"
    USER_TO_SUPPORT = "support_request"
    HISTORY_REQUEST = "history_request"
    HISTORY_RESPONSE = "history_response"
    CHAT = "chat"
    JOIN_CONVERSATION = "join_conversation" 
    LEAVE_CONVERSATION = "leave_conversation"

class MessageHandler:
    def __init__(self):
        self.connections: Dict[str, object] = {}
        self.user_sessions: Dict[str, object] = {}

        # In-memory message cache: {recipient_id: [message_objects]}
        self.message_cache: Dict[str, List[Dict]] = {}
        # Track last activity time for users
        self.last_seen: Dict[str, float] = {}
        # Maps user_id to websocket connection
        self.user_connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        # Maps conversation_id to set of user_ids
        self.conversations: Dict[str, Set[str]] = {}
        # In-memory message store (would be replaced by database in production)
        self.message_store: Dict[str, list] = {}
        logger.info("MessageHandler initialised")
    
    def register_user(self, user_id: str, websocket: websockets.WebSocketServerProtocol):
        """Register a user connection"""
        self.connections[user_id] = websocket
        self.last_seen[user_id] = time.time()
        if user_id not in self.message_cache:
            self.message_cache[user_id] = []
        self.user_connections[user_id] = websocket
        logger.info(f"User {user_id} registered")
    
    def remove_user(self, user_id: str):
        """Remove a user connection"""
        if user_id in self.connections:
            del self.connections[user_id]
        if user_id in self.user_connections:
            del self.user_connections[user_id]
            # Remove user from any conversations they were part of
            for conv_id, users in list(self.conversations.items()):
                if user_id in users:
                    users.remove(user_id)
                    if not users:  # If conversation is now empty, remove it
                        del self.conversations[conv_id]
            logger.info(f"User {user_id} removed")
    
    def get_user_socket(self, user_id: str):
        """Get the websocket for a specific user"""
        return self.connections.get(user_id)
    
    def update_last_seen(self, user_id: str):
        """Update the last seen timestamp for a user"""
        self.last_seen[user_id] = time.time()
    
    def store_message(self, message: Dict):
        """Store a message in the cache"""
        # Add timestamp if not already present
        if 'timestamp' not in message:
            message['timestamp'] = datetime.now().isoformat()
        
        # Store message for recipient
        recipient = message.get('recipient')
        if recipient:
            if recipient not in self.message_cache:
                self.message_cache[recipient] = []
            self.message_cache[recipient].append(message)
            
            # Limit cache size (keep last 100 messages per user)
            if len(self.message_cache[recipient]) > 100:
                self.message_cache[recipient] = self.message_cache[recipient][-100:]
    
    def get_messages_for_user(self, user_id: str, since_timestamp=None):
        """Get cached messages for a user, optionally after a specific timestamp"""
        if user_id not in self.message_cache:
            return []
            
        messages = self.message_cache[user_id]
        
        if since_timestamp:
            return [msg for msg in messages if msg.get('timestamp', '') > since_timestamp]
        return messages

    async def _handle_user_message(self, websocket, data):
        """Handle user-to-user messages"""
        if not all(k in data for k in ('sender', 'recipient', 'content')):
            return
        
        # Add timestamp
        timestamp = datetime.now().isoformat()
        
        # Prepare message for storage and delivery
        message = {
            'type': 'user_message',
            'sender': data['sender'],
            'recipient': data['recipient'],
            'content': data['content'],
            'timestamp': timestamp
        }
        
        # Store message
        self.store_message(message)
        
        # Update last seen for sender
        self.update_last_seen(data['sender'])
        
        # Send to recipient if online
        recipient_ws = self.get_user_socket(data['recipient'])
        if recipient_ws:
            await recipient_ws.send(json.dumps(message))
        
        # Send confirmation to sender
        response = {
            'type': 'user_message_sent',
            'recipient': data['recipient'],
            'timestamp': timestamp,
            'status': 'delivered' if recipient_ws else 'stored'
        }
        await websocket.send(json.dumps(response))

    async def _handle_support_message(self, websocket, data):
        """Handle support-related messages"""
        if not all(k in data for k in ('sender', 'content')):
            return
        
        # Add timestamp
        timestamp = datetime.now().isoformat()
        
        response = {
            'type': data['type'],
            'sender': data['sender'],
            'content': data['content'],
            'timestamp': timestamp
        }
        
        # Add recipient if present
        if 'recipient' in data:
            response['recipient'] = data['recipient']
            self.store_message(response)
            
            # Send to recipient if online
            recipient_ws = self.get_user_socket(data['recipient'])
            if recipient_ws:
                await recipient_ws.send(json.dumps(response))
        
        # Confirm to sender
        await websocket.send(json.dumps({
            'type': 'message_sent',
            'timestamp': timestamp,
            'status': 'delivered'
        }))

    async def _handle_history_request(self, websocket, data):
        """Handle request for message history"""
        if not all(k in data for k in ('user_id',)):
            return
        
        user_id = data['user_id']
        since_timestamp = data.get('since_timestamp')
        
        # Get messages for the user
        messages = self.get_messages_for_user(user_id, since_timestamp)
        
        # Send history response
        response = {
            'type': 'history_response',
            'messages': messages
        }
        await websocket.send(json.dumps(response))

    async def handle_message(self, websocket, message):
        data = json.loads(message)
        
        # Register user if this is an authentication message
        if 'register' in data and data['register'] and 'user_id' in data:
            self.register_user(data['user_id'], websocket)
            # Send any missed messages
            since_timestamp = data.get('since_timestamp')
            messages = self.get_messages_for_user(data['user_id'], since_timestamp)
            if messages:
                await websocket.send(json.dumps({
                    'type': 'history_response',
                    'messages': messages
                }))
            return
            
        # Check if this is a history request
        if data.get('type') == 'history_request':
            await self._handle_history_request(websocket, data)
            return
            
        # Handle join/leave conversation
        if data.get('type') == 'join_conversation':
            await self._handle_join_conversation(data)
            return
            
        if data.get('type') == 'leave_conversation':
            await self._handle_leave_conversation(data)
            return
            
        try:
            msg_type = MessageType(data['type'])
            
            if msg_type == MessageType.USER_TO_USER:
                await self._handle_user_message(websocket, data)
            elif msg_type in [MessageType.SUPPORT_TO_USER, MessageType.USER_TO_SUPPORT]:
                await self._handle_support_message(websocket, data)
            elif msg_type == MessageType.CHAT:  # Add handler for chat message type
                await self._handle_chat_message(data)
        except (KeyError, ValueError) as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f'Invalid message format: {str(e)}'
            }))

    async def _handle_chat_message(self, message):
        """Handle a chat message"""
        if not all(k in message for k in ['from', 'conversation_id', 'content']):
            logger.error("Incomplete chat message")
            return

        # Add timestamp if not provided
        if 'timestamp' not in message:
            message['timestamp'] = datetime.utcnow().isoformat()
        
        # Store message
        conversation_id = message['conversation_id']
        if conversation_id not in self.message_store:
            self.message_store[conversation_id] = []
        self.message_store[conversation_id].append(message)
        
        # Send to all users in this conversation
        if conversation_id in self.conversations:
            for user_id in self.conversations[conversation_id]:
                if user_id in self.user_connections:
                    try:
                        await self.user_connections[user_id].send(json.dumps(message))
                    except websockets.exceptions.ConnectionClosed:
                        logger.info(f"Connection closed for user {user_id}")
                        self.remove_user(user_id)

    async def _handle_typing_notification(self, message):
        """Handle typing notification"""
        if not all(k in message for k in ['from', 'conversation_id', 'is_typing']):
            return
        
        conversation_id = message['conversation_id']
        if conversation_id in self.conversations:
            for user_id in self.conversations[conversation_id]:
                if user_id != message['from'] and user_id in self.user_connections:
                    try:
                        await self.user_connections[user_id].send(json.dumps(message))
                    except websockets.exceptions.ConnectionClosed:
                        self.remove_user(user_id)
    
    async def _handle_read_receipt(self, message):
        """Handle read receipt"""
        if not all(k in message for k in ['from', 'conversation_id', 'message_id']):
            return
            
        conversation_id = message['conversation_id']
        if conversation_id in self.conversations:
            for user_id in self.conversations[conversation_id]:
                if user_id != message['from'] and user_id in self.user_connections:
                    try:
                        await self.user_connections[user_id].send(json.dumps(message))
                    except websockets.exceptions.ConnectionClosed:
                        self.remove_user(user_id)
    
    async def _handle_join_conversation(self, message):
        """Handle user joining a conversation"""
        if not all(k in message for k in ['user_id', 'conversation_id']):
            return
        
        user_id = message['user_id']
        conversation_id = message['conversation_id']
        
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = set()
        
        self.conversations[conversation_id].add(user_id)
        logger.info(f"User {user_id} joined conversation {conversation_id}")
        
    async def _handle_leave_conversation(self, message):
        """Handle user leaving a conversation"""
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
