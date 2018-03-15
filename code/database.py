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

    def __repr__(self):
        return "<User (user_id='%i', first_name='%s', username='%s')>" % (
            self.user_id, self.first_name, self.username
        )


def add_user(user, is_admin=False, is_muted=False, commit=True):
    new_user = User(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        is_admin=is_admin,
        is_muted=is_muted
    )
    session.add(new_user)
    if commit:
        session.commit()


def user_is_known(user):
    return session.query(exists().where(User.user_id == user.id)).scalar()


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(Integer, primary_key=True)
    title = Column(String)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return "<Chat (chat_id='%i', title='%s')>" % (
            self.chat_id, self.title
        )


def add_chat(chat, is_active=True, commit=True):
    new_chat = Chat(
        chat_id=chat.id,
        title=chat.title,
        is_active=is_active
    )
    session.add(new_chat)
    if commit:
        session.commit()


def set_chat_active(chat, is_active=True):
    conn = engine.connect()
    stmt = update(Chat).\
        values(is_active=is_active).\
        where(Chat.chat_id == chat.id)
    conn.execute(stmt)


def chat_is_known(chat):
    return session.query(exists().where(Chat.chat_id == chat.id)).scalar()


class ChatMember(Base):
    __tablename__ = "chat_members"

    user_id = Column(Integer, ForeignKey("users.user_id"))
    chat_id = Column(Integer, ForeignKey("chats.chat_id"))
    is_muted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    __table_args__ = PrimaryKeyConstraint(user_id, chat_id), {}

    def __repr__(self):
        return "<ChatMember (user_id='%i', chat_id='%i')>" % (
            self.user_id, self.chat_id
        )


def add_chat_member(user, chat, is_muted=False, commit=True):
    if not user_is_known(user):
        add_user(user, commit=False)

    if not chat_is_known(chat):
        add_chat(chat, commit=False)

    new_chat_members = ChatMember(
        user_id=user.id,
        chat_id=chat.id,
        is_muted=is_muted
    )
    session.add(new_chat_members)
    if commit:
        session.commit()


def chat_has_member(user, chat):
    return session.query(exists().where(ChatMember.user_id == user.id and
                                        ChatMember.chat_id == chat.id)).scalar()


def set_chat_member_active(user, chat, is_active=True):
    conn = engine.connect()
    stmt = update(ChatMember).\
        values(is_active=is_active).\
        where(ChatMember.user_id == user.id and ChatMember.chat_id == chat.id)
    conn.execute(stmt)


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.chat_id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    content = Column(String)
    forward_user_id = Column(Integer)
    reply_message_id = Column(Integer)

    def __repr__(self):
        return "<Message (user_id='%i', chat_id='%i', content='%s')>" % (
            self.user_id, self.chat_id, self.content
        )


def add_message(message, content, commit=True):
    new_message = Message(
        message_id=message.message_id,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        datetime=message.date,
        content=content,
        forward_user_id=message.forward_from.id if message.forward_from else None,
        reply_message_id=message.reply_to_message.message_id if message.reply_to_message else None
    )
    session.add(new_message)
    if commit:
        session.commit()


def add_text_message(message, commit=True):
    add_message(message, message.text, commit)


class Quote(Base):
    __tablename__ = "quotes"

    quote_id = Column(Integer, primary_key=True)
    content = Column(String)


class ChatQuote(Base):
    __tablename__ = "chat_quotes"

    quote_id = Column(Integer, ForeignKey("quotes.quote_id"))
    chat_id = Column(Integer, ForeignKey("chats.chat_id"))

    __table_args__ = PrimaryKeyConstraint(quote_id, chat_id), {}


def add_quote(content, chats, commit=True):
    new_quote = Quote(
        content=content
    )
    session.add(new_quote)
    session.commit()

    for chat in chats:
        new_chat_quote = ChatQuote(
            quote_id=new_quote.quote_id,
            chat_id=chat
        )
        session.add(new_chat_quote)

    if commit:
        session.commit()


def get_random_quote(chat):
    q = session.query(Quote, ChatQuote).\
        filter(ChatQuote.quote_id == Quote.quote_id).\
        filter(ChatQuote.chat_id == chat.id).\
        order_by(func.random()).limit(1)

    for row in q:
        return row[0].content
