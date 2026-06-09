from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_signup_adds_participant():
    # Arrange
    activity = "Chess Club"
    email = "azalea@mergington.edu"
    activity_data = client.get("/activities").json()[activity]
    assert email not in activity_data["participants"]

    # Act
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    participants = client.get("/activities").json()[activity]["participants"]
    assert email in participants


def test_remove_participant_removes_existing_participant():
    # Arrange
    activity = "Programming Class"
    email = "remove-me@mergington.edu"
    signup_response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert signup_response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Act
    response = client.delete(
        f"/activities/{activity}/participants?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}
    participants = client.get("/activities").json()[activity]["participants"]
    assert email not in participants
