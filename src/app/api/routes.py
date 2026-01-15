from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Chat, Message
from app.schemas import ChatCreate, ChatSchema, MessageCreate, MessageSchema
from app.logic import create_chat, create_message
from app.db.crud import save_chat, save_message, get_chat, get_messages, delete_chat


router = APIRouter(prefix="/chats", tags=["Chats"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ChatSchema)
def CreateChat(data: ChatCreate, db: Session = Depends(get_db)) -> Chat:
    chat_obj = create_chat(data)
    saved_chat = save_chat(db, chat_obj)

    return saved_chat


@router.post("/{chat_id}/messages/", response_model=MessageSchema)
def CreateMessage(chat_id: int,
                  data: MessageCreate,
                  db: Session = Depends(get_db)
                  ) -> Message:
    
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    message_obj = create_message(chat_id, data)
    saved_message = save_message(db, message_obj)
    
    return saved_message


@router.get("/{chat_id}", response_model=ChatSchema)
def GetChat(chat_id: int,
             limit: int = Query(20, ge=1, le=100),
             db: Session = Depends(get_db)
             ) -> Chat:
    
    chat = get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")    
    
    messages = get_messages(db, chat_id, limit)
    chat.messages = messages
    
    return chat


@router.delete("/{chat_id}", status_code=204)
def DeleteChat(chat_id: int, db: Session = Depends(get_db)) -> None:
    delete_chat(db, chat_id)
