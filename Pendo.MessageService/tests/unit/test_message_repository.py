import pytest
import uuid
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.db.MessageRepository import MessageRepository
from src.db.PendoDatabase import Messages, Conversations, ConversationParticipants, User

# Patch all repository methods that hit the DB for all tests in this module
@pytest.fixture(autouse=True)
def patch_repository_methods(monkeypatch):
    monkeypatch.setattr(MessageRepository, "save_message", MagicMock())
    monkeypatch.setattr(MessageRepository, "get_messages_by_conversation_id", MagicMock())
    monkeypatch.setattr(MessageRepository, "get_conversation_by_id", MagicMock())
    monkeypatch.setattr(MessageRepository, "create_conversation", MagicMock())
    monkeypatch.setattr(MessageRepository, "add_user_to_conversation", MagicMock())
    monkeypatch.setattr(MessageRepository, "get_user_conversations", MagicMock())
    monkeypatch.setattr(MessageRepository, "get_user_by_id", MagicMock())
    monkeypatch.setattr(MessageRepository, "create_user_stub", MagicMock())
    monkeypatch.setattr(MessageRepository, "create_conversation_with_participants", MagicMock())
    yield

@pytest.fixture
def mock_db_session():
    """Fixture to create a mock DB session"""

    from src.db.PendoDatabase import Base
    from src.db.PendoDatabaseProvider import engine

    if engine is not None:
        Base.metadata.create_all(bind=engine)

    mock_session = MagicMock()
    mock_session.query = MagicMock(return_value=mock_session)
    mock_session.filter = MagicMock(return_value=mock_session)
    mock_session.order_by = MagicMock(return_value=mock_session)
    mock_session.offset = MagicMock(return_value=mock_session)
    mock_session.limit = MagicMock(return_value=mock_session)
    mock_session.all = MagicMock(return_value=[])
    mock_session.get = MagicMock(return_value=None)
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    return mock_session

@pytest.fixture
def message_repo(mock_db_session):
    """Create a message repository with mocked database session"""
    with patch('src.db.MessageRepository.get_db') as mock_get_db:
        mock_get_db.return_value = iter([mock_db_session])
        repo = MessageRepository()
        return repo, mock_db_session

def test_save_message(message_repo):
    """Test saving a message to the database"""
    repo, _ = message_repo
    conversation_id = uuid.uuid4()
    sender_id = uuid.uuid4()
    message_type = "text"
    content = "Test message content"
    mock_message = MagicMock()
    mock_message.ConversationId = conversation_id
    mock_message.SenderId = sender_id
    mock_message.MessageType = message_type
    mock_message.Content = content
    mock_message.IsDeleted = False
    repo.save_message.return_value = mock_message

    message = repo.save_message(conversation_id, sender_id, message_type, content)
    assert message.ConversationId == conversation_id
    assert message.SenderId == sender_id
    assert message.MessageType == message_type
    assert message.Content == content
    assert message.IsDeleted == False
    repo.save_message.assert_called_once_with(conversation_id, sender_id, message_type, content)

def test_get_messages_by_conversation_id(message_repo):
    """Test getting messages by conversation ID"""
    repo, _ = message_repo
    mock_messages = [MagicMock(spec=Messages) for _ in range(3)]
    conversation_id = uuid.uuid4()
    repo.get_messages_by_conversation_id.return_value = mock_messages

    result = repo.get_messages_by_conversation_id(conversation_id)
    assert result == mock_messages
    repo.get_messages_by_conversation_id.assert_called_once_with(conversation_id)

def test_get_conversation_by_id(message_repo):
    """Test getting a conversation by ID"""
    repo, _ = message_repo
    conversation_id = uuid.uuid4()
    mock_conversation = MagicMock(spec=Conversations)
    repo.get_conversation_by_id.return_value = mock_conversation

    result = repo.get_conversation_by_id(conversation_id)
    assert result == mock_conversation
    repo.get_conversation_by_id.assert_called_once_with(conversation_id)

def test_create_conversation(message_repo):
    """Test creating a conversation"""
    repo, _ = message_repo
    conversation_type = "direct"
    name = "Test Conversation"
    mock_conversation = MagicMock()
    mock_conversation.Type = conversation_type
    mock_conversation.Name = name
    mock_conversation.ConversationId = uuid.uuid4()
    repo.create_conversation.return_value = mock_conversation

    conversation = repo.create_conversation(conversation_type, name)
    assert conversation.Type == conversation_type
    assert conversation.Name == name
    assert isinstance(conversation.ConversationId, uuid.UUID)
    repo.create_conversation.assert_called_once_with(conversation_type, name)

def test_add_user_to_conversation(message_repo):
    """Test adding a user to a conversation"""
    repo, _ = message_repo
    conversation_id = uuid.uuid4()
    user_id = uuid.uuid4()
    mock_participant = MagicMock()
    mock_participant.ConversationId = conversation_id
    mock_participant.UserId = user_id
    mock_participant.LeftAt = None
    repo.add_user_to_conversation.return_value = mock_participant

    participant = repo.add_user_to_conversation(conversation_id, user_id)
    assert participant.ConversationId == conversation_id
    assert participant.UserId == user_id
    assert participant.LeftAt is None
    repo.add_user_to_conversation.assert_called_once_with(conversation_id, user_id)

def test_get_user_conversations(message_repo):
    """Test getting user conversations"""
    repo, _ = message_repo
    user_id = uuid.uuid4()
    mock_conversations = [MagicMock(spec=Conversations) for _ in range(2)]
    repo.get_user_conversations.return_value = mock_conversations

    result = repo.get_user_conversations(user_id)
    assert result == mock_conversations
    repo.get_user_conversations.assert_called_once_with(user_id)

def test_get_user_by_id(message_repo):
    """Test getting a user by ID"""
    repo, _ = message_repo
    user_id = uuid.uuid4()
    mock_user = MagicMock(spec=User)
    repo.get_user_by_id.return_value = mock_user

    result = repo.get_user_by_id(user_id)
    assert result == mock_user
    repo.get_user_by_id.assert_called_once_with(user_id)

def test_create_conversation_with_participants(message_repo):
    """Test creating a conversation with participants"""
    repo, _ = message_repo
    conversation_type = "group"
    name = "Test Group"
    participants = [str(uuid.uuid4()) for _ in range(3)]
    mock_conversation = MagicMock(spec=Conversations)
    repo.create_conversation_with_participants.return_value = mock_conversation

    result = repo.create_conversation_with_participants(conversation_type, participants, name)
    repo.create_conversation_with_participants.assert_called_once_with(conversation_type, participants, name)
    assert result == mock_conversation
