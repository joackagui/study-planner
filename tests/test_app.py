from backend.app import app

def test_index_route():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200

def test_chat_requires_message():
    client = app.test_client()
    resp = client.post("/api/chat", json={})
    assert resp.status_code == 400