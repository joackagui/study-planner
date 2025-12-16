import backend.app as app_module

def test_index_route():
    app = app_module.app
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200

def test_chat_requires_message():
    app = app_module.app
    client = app.test_client()
    resp = client.post("/api/chat", json={})
    assert resp.status_code == 400