from sqlalchemy import create_engine, Column, Integer, String, Boolean, \
    DateTime, ForeignKey, exists, update
from sqlalchemy.sql import select, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker

from settings import DB_URL

# Configure a Session class.
Session = sessionmaker()

# Create an engine which the Session will use for connections.
engine = create_engine(DB_URL)

# Create a configured Session class.
Session.configure(bind=engine)

# Create a Session
session = Session()

# Create a base for the models to build upon.
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String)
    is_admin = Column(Boolean, default=False)
    is_muted = Column(Boolean, default=False)

    def __init__(self, user, is_admin=False, is_muted=False):
        self.user_id = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.username = user.username
        self.is_admin = is_admin
        self.is_muted = is_muted

    def exists(self):
        return session.query(exists().where(
            User.user_id == self.user_id)).scalar()

    def commit(self):
        session.add(self)
        session.commit()

    def __repr__(self):
        return "<User (user_id='%i', first_name='%s', username='%s')>" % (
            self.user_id, self.first_name, self.username
        )


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True)
    title = Column(String)
    is_active = Column(Boolean, default=True)

    def __init__(self, chat, is_active=True):
        self.chat_id = chat.id
        self.title = chat.title
        self.is_active = is_active

    def exits(self):
        return session.query(exists().where(
            Chat.chat_id == self.chat_id)).scalar()

    def commit(self):
        session.add(self)
        session.commit()

    def __repr__(self):
        return "<Chat (chat_id='%i', title='%s')>" % (
            self.chat_id, self.title
        )


def set_chat_active(chat, is_active=True):
    conn = engine.connect()
    stmt = update(Chat).\
        values(is_active=is_active).\
        where(Chat.chat_id == chat.id)
    conn.execute(stmt)


class ChatMember(Base):
    __tablename__ = "chat_members"

    user_id = Column(Integer, ForeignKey("users.user_id"))
    chat_id = Column(Integer, ForeignKey("chats.chat_id"))
    is_muted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    __table_args__ = PrimaryKeyConstraint(user_id, chat_id), {}

    def __init__(self, user, chat, is_muted=False, is_active=True):
        self.user_id = user.id
        self.chat_id = chat.id
        self.is_muted = is_muted
        self.is_active = is_active

    def exists(self):
        return session.query(exists().where(
            ChatMember.user_id == self.user_id and
            ChatMember.chat_id == self.chat_id)).scalar()

    def commit(self):
        session.add(self)
        session.commit()

    def __repr__(self):
        return "<ChatMember (user_id='%i', chat_id='%i')>" % (
            self.user_id, self.chat_id
        )


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.chat_id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    content = Column(String)
    forward_user_id = Column(Integer)
    reply_message_id = Column(Integer)

    def __init__(self, msg):
        self.message_id = msg.message_id
        self.user_id = msg.from_user.id
        self.chat_id = msg.chat.id
        self.datetime = msg.date
        self.content = msg.text
        self.forward_user_id = \
            msg.forward_from.id if msg.forward_from else None
        self.reply_message_id = \
            msg.reply_to_message.message_id if msg.reply_to_message else None

    def exits(self):
        return session.query(exists().where(
            Message.message_id == self.message_id)).scalar()

    def commit(self):
        session.add(self)
        session.commit()

    def __repr__(self):
        return "<Message (user_id='%i', chat_id='%i', content='%s')>" % (
            self.user_id, self.chat_id, self.content
        )
