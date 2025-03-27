from .PendoDatabase import *
from sqlalchemy.orm import joinedload, with_loader_criteria
from .PendoDatabaseProvider import get_db
from sqlalchemy import desc
import uuid
import datetime
from .PendoDatabase import User
from .PendoDatabase import ConversationParticipants

class MessageRepository():
    """
    Responsible for handling all database operations related to messages.
    A new database session is generated for each method call to avoid holding
    a long-lived session.
    """

    def save_message(self, conversation_id, sender_id, message_type, content, is_deleted=False):
        db_session = next(get_db())
        try:
            message = Messages(
                MessageId=uuid.uuid4(),
                ConversationId=conversation_id,
                SenderId=sender_id,
                MessageType=message_type,
                Content=content,
                CreateDate=datetime.datetime.utcnow(),
                IsDeleted=is_deleted
            )
            db_session.add(message)
            db_session.commit()
            return message
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    def get_messages_by_conversation_id(self, conversation_id, limit=100, skip=0):
        db_session = next(get_db())
        try:
            messages = db_session.query(Messages)\
                .filter(Messages.ConversationId == conversation_id)\
                .order_by(desc(Messages.CreateDate))\
                .offset(skip)\
                .limit(limit)\
                .all()
            return messages
        finally:
            db_session.close()

    def get_conversation_by_id(self, conversation_id):
        db_session = next(get_db())
        try:
            conversation = db_session.query(Conversations).get(conversation_id)
            return conversation
        finally:
            db_session.close()

    def create_conversation(self, conversation_type, name=None):
        db_session = next(get_db())
        try:
            conversation = Conversations(
                ConversationId=uuid.uuid4(),
                Type=conversation_type,
                CreateDate=datetime.datetime.utcnow(),
                UpdateDate=datetime.datetime.utcnow(),
                Name=name
            )
            db_session.add(conversation)
            db_session.commit()

            db_session.refresh(conversation)
            return conversation
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    def add_user_to_conversation(self, conversation_id, user_id):
        # Convert conversation_id and user_id to UUID if needed.
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
                    
        db_session = next(get_db())
        try:
            existing = db_session.query(ConversationParticipants).filter(
                ConversationParticipants.ConversationId == conversation_id,
                ConversationParticipants.UserId == user_id,
                ConversationParticipants.LeftAt == None
            ).first()
            if existing:
                return existing

            participant = ConversationParticipants(
                ConversationId=conversation_id,
                UserId=user_id,
                JoinedAt=datetime.datetime.utcnow()
            )
            db_session.add(participant)
            db_session.commit()
            db_session.refresh(participant)
            return participant
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    def get_user_conversations(self, user_id):
        db_session = next(get_db())
        try:
            conversations = db_session.query(Conversations)\
                .options(joinedload(Conversations.ConversationParticipants))\
                .join(ConversationParticipants)\
                .filter(ConversationParticipants.UserId == user_id)\
                .filter(ConversationParticipants.LeftAt == None)\
                .order_by(Conversations.UpdateDate.desc())\
                .all()
            return conversations
        finally:
            db_session.close()

    def get_user_by_id(self, user_id):
        db_session = next(get_db())
        try:
            user = db_session.query(User).get(user_id)
            return user
        finally:
            db_session.close()

    def create_user_stub(self, user_id):
        db_session = next(get_db())
        try:
            user = User(
                UserId=user_id,
                Email=f"user_{user_id}@example.com",
                UserTypeId=1,  # Default user type
                CreateDate=datetime.datetime.utcnow(),
                UpdateDate=datetime.datetime.utcnow(),
                FirstName="",
                LastName=""
            )
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            return user
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    def create_conversation_with_participants(self, conversation_type, participants, name=None):
        conversation = self.create_conversation(conversation_type, name)
        added_users = set()
        for participant in participants:
            participant_str = str(participant)
            if participant_str in added_users:
                continue
            if not isinstance(participant, uuid.UUID):
                participant_id = uuid.UUID(str(participant))
            else:
                participant_id = participant
            user = self.get_user_by_id(participant_id)
            if not user:
                user = self.create_user_stub(participant_id)
            self.add_user_to_conversation(conversation.ConversationId, participant_id)
            added_users.add(participant_str)
        return conversation