from .PendoDatabase import *
from sqlalchemy.orm import joinedload, with_loader_criteria
from .PendoDatabaseProvider import get_db
from sqlalchemy import desc
import uuid
import datetime
from .PendoDatabase import User  # Ensure this imports the User model

class MessageRepository():
    """
    This class is responsible for handling all the database operations related to messages
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
            conversation_id: ID of the conversation (string or UUID object)
            user_id: ID of the user (string or UUID object)
        
        Returns:
            The newly created conversation participant object
        """

        print(conversation_id, user_id)
        print(type(conversation_id), type(user_id))

        # Convert to UUID objects if they're not already
        if not isinstance(conversation_id, uuid.UUID):
            try:
                conversation_id = uuid.UUID(str(conversation_id))
            except ValueError:
                raise ValueError("Invalid UUID format for conversation_id")
                
        if not isinstance(user_id, uuid.UUID):
            try:
                user_id = uuid.UUID(str(user_id))
            except ValueError:
                raise ValueError("Invalid UUID format for user_id")
        
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
        Get all conversations a user is part of
        
        Parameters:
            user_id: ID of the user
        
        Returns:
            List of conversations sorted by most recent update
        """
        return self.db_session.query(Conversations)\
            .join(ConversationParticipants)\
            .filter(ConversationParticipants.UserId == user_id)\
            .filter(ConversationParticipants.LeftAt == None)\
            .order_by(Conversations.UpdateDate.desc())\
            .all()
    
    def get_user_by_id(self, user_id):
        """
        Fetch a user from the database by user_id.

        Parameters:
            user_id (str): ID of the user

        Returns:
            The user object
        """
        return self.db_session.query(User).get(user_id)
    
    def create_conversation_with_participants(self, conversation_type, participants, name=None):
        """
        Create a new conversation and add participants.
        
        Parameters:
            conversation_type (str): Type of the conversation
            participants (list): List of user_id strings (UUIDs)
            name (str, optional): Conversation name
        
        Returns:
            The created conversation object.
        """
        conversation = self.create_conversation(conversation_type, name)
        
        # Track already added users to prevent duplicates
        added_users = set()
        
        for participant in participants:
            # Skip if we've already processed this participant
            participant_str = str(participant)
            if participant_str in added_users:
                continue
                
            # Convert string to UUID if it's not already a UUID
            if not isinstance(participant, uuid.UUID):
                participant_id = uuid.UUID(str(participant))
            else:
                participant_id = participant
                
            # Check if the user exists before adding
            user = self.get_user_by_id(participant_id)
            if user:
                # Successfully add the user to the conversation
                self.add_user_to_conversation(conversation.ConversationId, participant_id)
                added_users.add(participant_str)
        
        return conversation