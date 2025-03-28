import json
import pytest
from unittest.mock import MagicMock

from message_client import MessageClient
from identity_client import IdentityClient

# Dummy logger
class DummyLogger:
    def __init__(self):
        self.info = lambda msg: None
        self.debug = lambda msg: None
        self.error = lambda msg: None

class FakeResponse:
    def __init__(self, status_code, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data or {}
        self.text = text
    def json(self):
        return self._json

# IdentityClient tests
def test_identity_request_otp(monkeypatch):
    logger = DummyLogger()
    client = IdentityClient("http://fake-url", logger)
    def fake_post(url, json, headers, verify):
        assert url.endswith("/api/Identity/RequestOtp")
        return FakeResponse(200, {"success": True}, "OK")
    monkeypatch.setattr("identity_client.requests.post", fake_post)
    response = client.RequestOtp("test@example.com")
    assert response.status_code == 200
    assert response.json()["success"]

def test_identity_verify_otp(monkeypatch):
    logger = DummyLogger()
    client = IdentityClient("http://fake-url", logger)
    def fake_post(url, json, headers, verify):
        assert url.endswith("/api/Identity/VerifyOtp")
        return FakeResponse(200, {"verified": True}, "OK")
    monkeypatch.setattr("identity_client.requests.post", fake_post)
    response = client.VerifyOtp("test@example.com", "123456")
    assert response.status_code == 200
    assert response.json()["verified"]

def test_identity_ping(monkeypatch):
    logger = DummyLogger()
    client = IdentityClient("http://fake-url", logger)
    def fake_get(url, headers, verify):
        assert url.endswith("/api/Ping")
        return FakeResponse(200, {"alive": True}, "OK")
    monkeypatch.setattr("identity_client.requests.get", fake_get)
    response = client.Ping()
    assert response.status_code == 200
    assert response.json()["alive"]

class FakeWebSocket:
    def __init__(self, responses):
        self.responses = responses
        self.recv_count = 0
        self.closed = False
    def send(self, message):
        pass
    def recv(self):
        resp = self.responses[self.recv_count]
        self.recv_count += 1
        return json.dumps(resp)
    def close(self):
        self.closed = True

# MessageClient tests
def test_message_get_user_conversations(monkeypatch):
    logger = DummyLogger()
    client = MessageClient("http://fake-url", logger)
    def fake_get(url, json, headers, verify):
        assert url.endswith("/SupportConversation")
        return FakeResponse(200, {"conversations": []}, "OK")
    monkeypatch.setattr("message_client.requests.get", fake_get)
    result = client.get_user_conversations("user123")
    assert result is not None
    assert "conversations" in result

def test_message_join_and_send(monkeypatch):
    logger = DummyLogger()
    client = MessageClient("http://fake-url", logger)

    join_resp = {"joined": True}
    history_resp = {"messages": [{"SenderId": "user1", "Content": "hello", "CreateDate": "2021-01-01T00:00:00Z"}]}
    chat_resp = {"sent": True}
    fake_ws = FakeWebSocket([join_resp, history_resp, chat_resp])
    def fake_create_connection(ws_url, header):
        assert ws_url.startswith("wss://")
        return fake_ws
    monkeypatch.setattr("message_client.create_connection", fake_create_connection)
    
    join_result = client.join_conversation("user123", "conv456")
    assert join_result is not None
    assert "messages" in join_result
    msg = join_result["messages"][0]
    assert msg["from"] == "user1"
    assert msg["content"] == "hello"
    assert msg["timestamp"] == "2021-01-01T00:00:00Z"
    

    response = client.send_chat_message("user123", "conv456", "Hi", "2021-01-02T00:00:00Z")
    assert response["sent"] == True

def test_message_close_connection():
    logger = DummyLogger()
    client = MessageClient("http://fake-url", logger)
    fake_ws = FakeWebSocket([])
    client.ws = fake_ws
    client.close_connection()
    assert fake_ws.closed
