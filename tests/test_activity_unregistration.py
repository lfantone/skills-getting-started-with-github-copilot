from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_existing_participant():
    original = list(activities["Chess Club"]["participants"])

    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

    activities["Chess Club"]["participants"] = original


def test_unregister_unknown_participant_returns_404():
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_post_route_works_too():
    original = list(activities["Programming Class"]["participants"])

    response = client.post(
        "/activities/Programming Class/unregister",
        params={"email": "emma@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered emma@mergington.edu from Programming Class"
    assert "emma@mergington.edu" not in activities["Programming Class"]["participants"]

    activities["Programming Class"]["participants"] = original
