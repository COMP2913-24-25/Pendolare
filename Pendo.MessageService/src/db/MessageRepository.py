from .PendoDatabase import *
from sqlalchemy.orm import joinedload, with_loader_criteria
from .PendoDatabaseProvider import get_db
from sqlalchemy import desc
import uuid
import datetime

class MessageRepository():
    """
    This class is responsible for handling all the database operations related to bookings
    """

    def __init__(self):
        """
        Constructor for MessageRepository class.
        """
        self.db_session = next(get_db())

    # Message methods
    def save_message(self, conversation_id, sender_id, message_type, content, is_deleted=False):
        """
        Save a new message to the database.
        
        Parameters:
            conversation_id: ID of the conversation
            sender_id: ID of the sender
            message_type: Type of the message
            content: Content of the message
            is_deleted: Flag indicating if the message is deleted

        Returns:
            The newly created message object
        """
        message = Messages(
            MessageId=uuid.uuid4(),
            ConversationId=conversation_id,
            SenderId=sender_id,
            MessageType=message_type,
            Content=content,
            CreateDate=datetime.datetime.utcnow(),
            IsDeleted=is_deleted
        )
        
        self.db_session.add(message)
        self.db_session.commit()
        return message
    
    def get_messages_by_conversation_id(self, conversation_id, limit=100, skip=0):
        """
        Get messages by conversation ID.
        
        Parameters:
            conversation_id: ID of the conversation
            limit: Number of messages to return
            skip: Number of messages to skip
        
        Returns:
            List of messages
        """
        return self.db_session.query(Messages)\
            .filter(Messages.ConversationId == conversation_id)\
            .order_by(desc(Messages.CreateDate))\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_conversation_by_id(self, conversation_id):
        """
        Get a conversation by ID.
        
        Parameters:
            conversation_id: ID of the conversation
        
        Returns:
            The conversation object
        """
        return self.db_session.query(Conversations).get(conversation_id)
    
    def create_conversation(self, conversation_type, name=None):
        """
        Create a new conversation.
        
        Parameters:
            conversation_type: Type of the conversation
            name: Name of the conversation
        
        Returns:
            The newly created conversation object
        """
        conversation = Conversations(
            ConversationId=uuid.uuid4(),
            Type=conversation_type,
            CreateDate=datetime.datetime.utcnow(),
            UpdateDate=datetime.datetime.utcnow(),
            Name=name
        )
        
        self.db_session.add(conversation)
        self.db_session.commit()
        return conversation
    
    def add_user_to_conversation(self, conversation_id, user_id):
        """
        Add a user to a conversation.
        
        Parameters:
            conversation_id: ID of the conversation
            user_id: ID of the user
        
        Returns:
            The newly created conversation participant object
        """
        participant = ConversationParticipants(
            ConversationId=conversation_id,
            UserId=user_id,
            JoinedAt=datetime.datetime.utcnow()
        )
        
        self.db_session.add(participant)
        self.db_session.commit()
        return participant
    
    def get_user_conversations(self, user_id):
        """
        Get all conversations a user is part of.
        
        Parameters:
            user_id: ID of the user
        
        Returns:
            List of conversations
        """
        return self.db_session.query(Conversations)\
            .join(ConversationParticipants)\
            .filter(ConversationParticipants.UserId == user_id)\
            .filter(ConversationParticipants.LeftAt == None)\
            .all()