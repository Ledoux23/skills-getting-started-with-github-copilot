import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities(client):
    # Arrange: Client is set up via fixture

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status and response content
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success(client):
    # Arrange: Prepare signup data for an activity with available spots
    activity_name = "Basketball Team"
    email = "newstudent@example.com"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" == data["message"]


def test_signup_activity_not_found(client):
    # Arrange: Use a non-existent activity name
    activity_name = "NonExistent Activity"
    email = "student@example.com"

    # Act: Attempt to signup for invalid activity
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 404 error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" == data["detail"]


def test_signup_already_signed_up(client):
    # Arrange: First, signup a student
    activity_name = "Soccer Club"
    email = "duplicate@example.com"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act: Attempt to signup the same student again
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 400 error for duplicate signup
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" == data["detail"]