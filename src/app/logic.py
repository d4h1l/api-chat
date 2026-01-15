from app.db.models import Chat, Message
from app.schemas import ChatCreate, MessageCreate


def create_chat(data: ChatCreate) -> Chat:
    """
    Возвращает объект Chat из данных запроса
    """
    title = data.title.strip()

    return Chat(title=title)



def create_message(chat_id: int, data: MessageCreate) -> Message:
    """
    Возвращает объект Message из данных запроса
    """
    text = data.text.strip()

    return Message(chat_id=chat_id, text=text)
