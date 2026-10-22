"""
Automated tests for the Task Manager application.

These tests mock the database layer so you can run them without
a running MySQL instance:  pytest tests/
"""

import types
import pytest
from app import app


# ---------------------------------------------------------------------------
# Fake database layer
# ---------------------------------------------------------------------------

class FakeCursor:
    """Minimal cursor that stores executed queries and returns canned data."""

    def __init__(self, rows=None):
        self.rows = rows or []
        self.last_query = None
        self.last_params = None

    def execute(self, query, params=None):
        self.last_query = query
        self.last_params = params

    def fetchall(self):
        return self.rows

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class FakeConnection:
    """Minimal connection wrapper around FakeCursor."""

    def __init__(self, rows=None):
        self._cursor = FakeCursor(rows)

    def cursor(self):
        return self._cursor

    def commit(self):
        pass

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client(monkeypatch):
    """Create a Flask test client with the DB mocked out."""
    import app as app_module

    # Default: return an empty task list
    monkeypatch.setattr(app_module, "get_db", lambda: FakeConnection())

    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _patch_db(monkeypatch, rows=None):
    """Helper to swap get_db for a FakeConnection with given rows."""
    import app as app_module
    conn = FakeConnection(rows)
    monkeypatch.setattr(app_module, "get_db", lambda: conn)
    return conn


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestIndex:
    """GET / — view all tasks."""

    def test_index_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_shows_heading(self, client):
        response = client.get("/")
        assert b"Task Manager" in response.data

    def test_index_shows_empty_state(self, client):
        response = client.get("/")
        assert b"No tasks yet" in response.data

    def test_index_shows_tasks(self, client, monkeypatch):
        from datetime import datetime

        rows = [
            {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk and eggs",
                "completed": False,
                "created_at": datetime(2026, 1, 1, 12, 0),
            }
        ]
        _patch_db(monkeypatch, rows)
        response = client.get("/")
        assert b"Buy groceries" in response.data
        assert b"Milk and eggs" in response.data


class TestAddTask:
    """POST /add — create a new task."""

    def test_add_task_redirects(self, client):
        response = client.post(
            "/add",
            data={"title": "Test task", "description": "A description"},
            follow_redirects=False,
        )
        assert response.status_code == 302

    def test_add_task_empty_title_flashes_error(self, client):
        response = client.post(
            "/add",
            data={"title": "", "description": ""},
            follow_redirects=True,
        )
        assert b"Task title is required" in response.data

    def test_add_task_success_flashes_message(self, client):
        response = client.post(
            "/add",
            data={"title": "Do homework", "description": "Math chapter 5"},
            follow_redirects=True,
        )
        assert b"Task added successfully" in response.data


class TestCompleteTask:
    """GET /complete/<id> — toggle completion."""

    def test_complete_redirects(self, client):
        response = client.get("/complete/1", follow_redirects=False)
        assert response.status_code == 302

    def test_complete_flashes_message(self, client):
        response = client.get("/complete/1", follow_redirects=True)
        assert b"Task status updated" in response.data


class TestDeleteTask:
    """GET /delete/<id> — remove a task."""

    def test_delete_redirects(self, client):
        response = client.get("/delete/1", follow_redirects=False)
        assert response.status_code == 302

    def test_delete_flashes_message(self, client):
        response = client.get("/delete/1", follow_redirects=True)
        assert b"Task deleted" in response.data
