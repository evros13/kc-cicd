from fastapi.testclient import TestClient
from main import app, tasks

client = TestClient(app)


def setup_function():
    """Limpia la lista de tareas antes de cada test"""
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
    task = {"id": 1, "title": "Aprender CI/CD", "done": False}
    response = client.post("/tasks", json=task)
    assert response.status_code == 201
    assert response.json()["title"] == "Aprender CI/CD"


def test_create_duplicate_task():
    task = {"id": 1, "title": "Tarea duplicada", "done": False}
    client.post("/tasks", json=task)
    response = client.post("/tasks", json=task)
    assert response.status_code == 400


def test_get_tasks_after_create():
    task = {"id": 1, "title": "Mi tarea", "done": False}
    client.post("/tasks", json=task)
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1
