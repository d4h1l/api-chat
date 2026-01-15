from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import Chat, Message


def save_chat(db: Session, chat: Chat) -> Chat:
    """
    Сохраняет чат в БД и возвращает объект с обновлённым ID
    """
    db.add(chat)
    db.commit()
    db.refresh(chat)
    
    chat.messages = []
    
    return chat


def save_message(db: Session, message: Message) -> Message:
    """
    Сохраняет сообщение в БД и возвращает объект с обновлённым ID
    """
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message


def get_chat(db: Session, chat_id: int) -> Chat:
    """
    Возвращает чат по ID из БД.
    """
    chat = db.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return chat


def get_messages(db: Session, chat_id: int, limit: int) -> list[Message]:
    """
    Возвращает последние сообщения чата с ограничением
    """
    messages = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    
    return list(reversed(messages))


def delete_chat(db: Session, chat_id: int) -> None:
    """
    Удаляет чат из БД по ID
    """
    chat = db.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    db.delete(chat)
    db.commit()
