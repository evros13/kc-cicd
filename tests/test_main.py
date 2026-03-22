from fastapi.testclient import TestClient
from app.main import app, tasks

client = TestClient(app)


def setup_function():
    tasks.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    task = {"id": 1, "title": "Testing Task Creation", "done": False}
    response = client.post("/tasks", json=task)
    assert response.status_code == 201
    assert response.json()["title"] == "Testing Task Creation"


def test_create_duplicate_task():
    task = {"id": 1, "title": "Testing Duplicate Task", "done": False}
    client.post("/tasks", json=task)
    response = client.post("/tasks", json=task)
    assert response.status_code == 400


def test_get_tasks_after_create():
    task = {"id": 1, "title": "Testing Get Tasks After Adding Task", "done": False}
    client.post("/tasks", json=task)
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_task():
    task = {"id": 1, "title": "Testing Task Deletion", "done": False}
    client.post("/tasks", json=task)
    response = client.delete("/tasks/1")
    assert response.status_code == 204


def test_delete_task_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 404
