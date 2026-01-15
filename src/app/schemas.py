from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


# Pydantic-модель для запроса на создания сообщения
class MessageCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


# Pydantic-модель сообщения
class MessageSchema(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Pydantic-модель для запроса на создания чата
class ChatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


# Pydantic-модель чата
class ChatSchema(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: List[MessageSchema] = []
    
    model_config = ConfigDict(from_attributes=True)
