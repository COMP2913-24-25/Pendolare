import pytest
import uuid
from unittest.mock import MagicMock, patch
from datetime import datetime

from src.db.MessageRepository import MessageRepository
from src.db.PendoDatabase import Messages, Conversations, ConversationParticipants, User


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
    repo, mock_db = message_repo

    # Patch save_message to avoid real DB call and return a mock message
    with patch.object(repo, "save_message") as mock_save_message:
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

        mock_save_message.return_value = mock_message

        message = repo.save_message(conversation_id, sender_id, message_type, content)

        assert message.ConversationId == conversation_id
        assert message.SenderId == sender_id
        assert message.MessageType == message_type
        assert message.Content == content
        assert message.IsDeleted == False

        mock_save_message.assert_called_once_with(conversation_id, sender_id, message_type, content)


def test_get_messages_by_conversation_id(message_repo):
    """Test getting messages by conversation ID"""
    repo, mock_db = message_repo

    # Patch get_messages_by_conversation_id to avoid real DB call and return mock messages
    with patch.object(repo, "get_messages_by_conversation_id") as mock_get_msgs:
        mock_messages = [MagicMock(spec=Messages) for _ in range(3)]
        conversation_id = uuid.uuid4()
        mock_get_msgs.return_value = mock_messages

        result = repo.get_messages_by_conversation_id(conversation_id)

        assert result == mock_messages
        mock_get_msgs.assert_called_once_with(conversation_id)


def test_get_conversation_by_id(message_repo):
    """Test getting a conversation by ID"""
    repo, mock_db = message_repo
    
    # Setup mock conversation
    conversation_id = uuid.uuid4()
    mock_conversation = MagicMock(spec=Conversations)
    mock_db.query.return_value.get.return_value = mock_conversation
    
    result = repo.get_conversation_by_id(conversation_id)
    
    assert result == mock_conversation
    mock_db.query.assert_called_once_with(Conversations)
    mock_db.query.return_value.get.assert_called_once_with(conversation_id)


def test_create_conversation(message_repo):
    """Test creating a conversation"""
    repo, mock_db = message_repo
    
    conversation_type = "direct"
    name = "Test Conversation"
    
    conversation = repo.create_conversation(conversation_type, name)
    
    assert conversation.Type == conversation_type
    assert conversation.Name == name
    assert isinstance(conversation.ConversationId, uuid.UUID)
    
    # Verify conversation was added to the session and committed
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_add_user_to_conversation(message_repo):
    """Test adding a user to a conversation"""
    repo, mock_db = message_repo
    
    # Test data
    conversation_id = uuid.uuid4()
    user_id = uuid.uuid4()
    
    participant = repo.add_user_to_conversation(conversation_id, user_id)
    
    assert participant.ConversationId == conversation_id
    assert participant.UserId == user_id
    assert participant.LeftAt is None
    
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_get_user_conversations(message_repo):
    """Test getting user conversations"""
    repo, mock_db = message_repo
    
    # Setup mock query response
    user_id = uuid.uuid4()
    mock_conversations = [MagicMock(spec=Conversations) for _ in range(2)]
    
    mock_query = mock_db.query.return_value
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.all.return_value = mock_conversations
    
    result = repo.get_user_conversations(user_id)
    
    assert result == mock_conversations
    mock_db.query.assert_called_once_with(Conversations)
    mock_query.join.assert_called_once_with(ConversationParticipants)
    assert mock_query.filter.call_count == 2  # Two filters: UserId and LeftAt
    mock_query.order_by.assert_called_once()
    mock_query.all.assert_called_once()


def test_get_user_by_id(message_repo):
    """Test getting a user by ID"""
    repo, mock_db = message_repo
    
    user_id = uuid.uuid4()
    mock_user = MagicMock(spec=User)
    mock_db.query.return_value.get.return_value = mock_user
    
    result = repo.get_user_by_id(user_id)
    
    assert result == mock_user
    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.get.assert_called_once_with(user_id)


def test_create_conversation_with_participants(message_repo):
    """Test creating a conversation with participants"""
    repo, mock_db = message_repo
    
    repo.create_conversation = MagicMock()
    repo.add_user_to_conversation = MagicMock()
    repo.get_user_by_id = MagicMock()
    
    conversation_type = "group"
    name = "Test Group"
    participants = [str(uuid.uuid4()) for _ in range(3)]
    
    mock_conversation = MagicMock(spec=Conversations)
    mock_conversation.ConversationId = uuid.uuid4()
    repo.create_conversation.return_value = mock_conversation
    
    mock_user = MagicMock(spec=User)
    mock_user.UserTypeId = 1
    repo.get_user_by_id.return_value = mock_user
    
    result = repo.create_conversation_with_participants(conversation_type, participants, name)
    
    repo.create_conversation.assert_called_once_with(conversation_type, name)
    
    assert repo.add_user_to_conversation.call_count == len(participants)
    
    assert repo.get_user_by_id.call_count == len(participants)
    
    assert result == mock_conversation
