import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.api.routes import get_db
from app.service import app
from fastapi.testclient import TestClient


TEST_DATABASE_URL = "postgresql://test:test@test-db:5432/test_db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


# Тест на создания чата
def test_create_chat(client):
    # Запрос на создание чата
    response = client.post("/chats/", json={"title": "Chat 1"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Chat 1"


# Тест на создания сообщения
def test_create_message(client):
    # Запрос на создание чата
    chat_resp = client.post("/chats/", json={"title": "Chat 2"})
    chat_id = chat_resp.json()["id"]

    # Запрос на создание сообщения
    msg_resp = client.post(f"/chats/{chat_id}/messages/", json={"text": "Hello"})
    assert msg_resp.status_code == 200
    data = msg_resp.json()
    assert data["text"] == "Hello"
    assert data["chat_id"] == chat_id


# Тест на получения чата
def test_get_chat(client):
    # Запрос на создание чата
    chat_resp = client.post("/chats/", json={"title": "Chat 3"})
    chat_id = chat_resp.json()["id"]
    
    # Добавление 10 сообщений
    for _ in range(9):
        client.post(f"/chats/{chat_id}/messages/", json={"text": "Hello"})
    client.post(f"/chats/{chat_id}/messages/", json={"text": "Hello!!!"})
    
    response = client.get(f"/chats/{chat_id}?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == chat_id
    assert "messages" in data
    assert len(data["messages"]) == 10
    assert data["title"] == "Chat 3"
    assert data["messages"][9]["text"] == "Hello!!!"


# Тест на удаление чата
def test_delete_chat(client):
    # Запрос на создание чата
    chat_resp = client.post("/chats/", json={"title": "Chat 4"})
    chat_id = chat_resp.json()["id"]
    
    # Запрос на удаления чата
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 204

    # Проверка, что чата не больше существует
    get_resp = client.get(f"/chats/{chat_id}")
    assert get_resp.status_code == 404


# Тест на создания пустого сообщения
def test_create_null_message(client):
    # Запрос на создание чата
    chat_resp = client.post("/chats/", json={"title": "Chat 5"})
    chat_id = chat_resp.json()["id"]

    # Запрос на создание сообщения
    msg_resp = client.post(f"/chats/{chat_id}/messages/", json={"text": ""})
    assert msg_resp.status_code == 422


# Тест на создания пустого заголовка чата
def test_create_null_title_chat(client):
    # Запрос на создание чата
    chat_resp = client.post("/chats/", json={"title": ""})
    assert chat_resp.status_code == 422


# Тест на создания сообщения в несуществующем чате
def test_create_message_null_chat(client):
    # Запрос на создание сообщения
    response = client.post(f"/chats/01/messages/", json={"text": "Hello"})
    
    assert response.status_code == 404
