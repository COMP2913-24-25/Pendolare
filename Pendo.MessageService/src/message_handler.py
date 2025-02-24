from enum import Enum
import json
from typing import Dict, Set

class MessageType(Enum):
    USER_TO_USER = "user_message"
    SUPPORT_TO_USER = "support_message"
    USER_TO_SUPPORT = "support_request"

class MessageHandler:
    def __init__(self):
        self.connections: Dict[str, Set] = {
            'users': set(),
            'support': set()
        }
    
    async def _handle_user_message(self, websocket, data):
        """Handle user-to-user messages"""
        if not all(k in data for k in ('sender', 'recipient', 'content')):
            return
        
        response = {
            'type': 'user_message',
            'sender': data['sender'],
            'content': data['content']
        }
        await websocket.send(json.dumps(response))

    async def _handle_support_message(self, websocket, data):
        """Handle support-related messages"""
        if not all(k in data for k in ('sender', 'content')):
            return
        
        response = {
            'type': data['type'],
            'sender': data['sender'],
            'content': data['content']
        }
        await websocket.send(json.dumps(response))

    async def handle_message(self, websocket, message):
        data = json.loads(message)
        msg_type = MessageType(data['type'])
        
        if msg_type == MessageType.USER_TO_USER:
            await self._handle_user_message(websocket, data)
        elif msg_type in [MessageType.SUPPORT_TO_USER, MessageType.USER_TO_SUPPORT]:
            await self._handle_support_message(websocket, data)
