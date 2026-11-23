def test_create_note(client):
    response = client.post(
        "/notes",
        json={"title": "Test", "content": "Treść testowa"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["content"] == "Treść testowa"

def test_get_note(client):
    response = client.post(
        "/notes",
        json={"title": "Test", "content": "Treść testowa"},
    )
    assert response.status_code == 200
    note_id = response.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Test"
    assert data["content"] == "Treść testowa"

def test_get_nonexistent_note(client):
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Note 999 not found"}

def test_get_all_notes(client):
    response = client.post(
        "/notes",
        json={"title": "Test1", "content": "Treść testowa 1"},
    )
    assert response.status_code == 200

    response = client.post(
        "/notes",
        json={"title": "Test2", "content": "Treść testowa 2"},
    )
    assert response.status_code == 200

    response = client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    assert any(note["title"] == "Test1" for note in data)
    assert any(note["title"] == "Test2" for note in data)