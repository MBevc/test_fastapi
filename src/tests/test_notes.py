import pytest
from app.api import crud


def test_create_note(test_app, monkeypatch):
    test_request_payload = {"title": "something", "description": "something"}
    test_response_payload = {"id": 1, "title": "something", "description": "something"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/notes/", json=test_request_payload)
    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_app):
    response = test_app.post("/notes/", json={"title": "something"})
    assert response.status_code == 422


def test_crate_note_too_long_title(test_app):
    response = test_app.post(
        "/notes/",
        json={
            "title": "somesomethingsomethingsomethingsomethingsomethingsomethingsomethingsomethingthing",
            "description": "something",
        },
    )
    assert response.status_code == 422


def test_read_note(test_app, monkeypatch):
    test_data = {"id": 1, "title": "something", "description": "something"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)
    response = test_app.get("/notes/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)
    response = test_app.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_read_all_notes(test_app, monkeypatch):
    test_data = [
        {"id": 1, "title": "something", "description": "something"},
        {"id": 2, "title": "something", "description": "something"},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)
    response = test_app.get("/notes/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_note(test_app, monkeypatch):
    test_update_data = {"title": "something", "description": "something"}
    test_update_data_response = {
        "id": 1,
        "title": "something",
        "description": "something",
    }

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/notes/1/", json=test_update_data)
    assert response.status_code == 200
    assert response.json() == test_update_data_response


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "something"}, 422],
        [1, {"title": "something"}, 422],
        [999, {"title": "something", "description": "something"}, 404],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/notes/{id}/", json=payload)
    assert response.status_code == status_code
