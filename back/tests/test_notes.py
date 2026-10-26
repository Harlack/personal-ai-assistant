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
    assert response.json() == {"detail": "Note not found"}