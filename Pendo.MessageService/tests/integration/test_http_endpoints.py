import uuid
from unittest.mock import patch, MagicMock
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web

from src.app import root_handler, health_check, user_conversations_handler, create_conversation_handler


class TestHttpEndpoints(AioHTTPTestCase):
    
    async def get_application(self):
        """Create and return a test application"""
        app = web.Application()
        
        # Create mock repository
        self.mock_repo = MagicMock()
        self.mock_repo.create_conversation_with_participants = MagicMock()
        self.mock_repo.get_user_conversations = MagicMock()
        
        # Store the mock for use in tests
        app['repository'] = self.mock_repo
        
        # Register routes
        app.router.add_get('/', root_handler)
        app.router.add_get('/health', health_check)
        app.router.add_post('/user-conversations', user_conversations_handler)
        app.router.add_post('/create-conversation', create_conversation_handler)
        
        # Patch the repository in the app module
        # Derived from: https://stackoverflow.com/questions/69192748/pytest-mocking-class-instance-passed-as-an-argument
        patcher = patch('src.app.repository', self.mock_repo)
        patcher.start()
        
        self.addCleanup(patcher.stop)
        
        return app
    
    async def test_root_handler(self):
        """Test the root endpoint"""
        resp = await self.client.get('/')
        self.assertEqual(resp.status, 200)
        
        data = await resp.json()
        self.assertEqual(data['service'], 'Pendo Message Service')
        self.assertIn('endpoints', data)
    
    async def test_health_check(self):
        """Test the health check endpoint"""
        resp = await self.client.get('/health')
        self.assertEqual(resp.status, 200)
        
        data = await resp.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertEqual(data['service'], 'message-service')
    
    async def test_user_conversations_handler(self):
        """Test the user conversations endpoint"""
        user_id = str(uuid.uuid4())
        
        # Setup mock conversations
        mock_conv1 = MagicMock()
        mock_conv1.ConversationId = uuid.uuid4()
        mock_conv1.Type = "direct"
        mock_conv1.CreateDate.isoformat.return_value = "2023-01-01T12:00:00Z"
        mock_conv1.UpdateDate.isoformat.return_value = "2023-01-01T12:05:00Z"
        mock_conv1.Name = "Test Conversation 1"
        
        mock_conv2 = MagicMock()
        mock_conv2.ConversationId = uuid.uuid4()
        mock_conv2.Type = "support"
        mock_conv2.CreateDate.isoformat.return_value = "2023-01-02T12:00:00Z"
        mock_conv2.UpdateDate.isoformat.return_value = "2023-01-02T12:05:00Z"
        mock_conv2.Name = "Test Conversation 2"
        
        # Configure mock repository to return conversations
        self.mock_repo.get_user_conversations.return_value = [mock_conv1, mock_conv2]
        
        # Send request
        resp = await self.client.post(
            '/user-conversations',
            json={"UserId": user_id}
        )
        
        # Check response
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertIn('conversations', data)
        self.assertEqual(len(data['conversations']), 2)
    
    async def test_create_conversation_handler(self):
        """Test the create conversation endpoint"""
        # Setup test data
        conversation_id = uuid.uuid4()
        conversation_type = "direct"
        name = "Test Conversation"
        participants = [str(uuid.uuid4()) for _ in range(2)]
        
        # Create mock conversation
        mock_conversation = MagicMock()
        mock_conversation.ConversationId = conversation_id
        mock_conversation.Type = conversation_type
        mock_conversation.Name = name
        mock_conversation.CreateDate.isoformat.return_value = "2023-01-01T12:00:00Z"
        mock_conversation.UpdateDate.isoformat.return_value = "2023-01-01T12:05:00Z"
        
        # Configure mock repository
        self.mock_repo.create_conversation_with_participants.return_value = mock_conversation
        
        # Send request
        resp = await self.client.post(
            '/create-conversation',
            json={
                "ConversationType": conversation_type,
                "name": name,
                "participants": participants
            }
        )
        
        # Check response
        self.assertEqual(resp.status, 200)
        data = await resp.json()
        self.assertEqual(data['ConversationId'], str(conversation_id))
        self.assertEqual(data['Type'], conversation_type)
        self.assertEqual(data['Name'], name)
    
    async def test_missing_fields_in_create_conversation(self):
        """Test validation for missing fields in create conversation"""
        # Send request with missing fields
        resp = await self.client.post(
            '/create-conversation',
            json={"name": "Test"}  # Missing ConversationType and participants
        )
        
        # Check response
        self.assertEqual(resp.status, 400)
        data = await resp.json()
        self.assertIn('error', data)
    
    async def test_invalid_participants_in_create_conversation(self):
        """Test validation for invalid participants in create conversation"""
        # Send request with invalid participants (not a list)
        resp = await self.client.post(
            '/create-conversation',
            json={
                "ConversationType": "direct",
                "name": "Test",
                "participants": "not-a-list"
            }
        )
        
        # Check response
        self.assertEqual(resp.status, 400)
        data = await resp.json()
        self.assertIn('error', data)
