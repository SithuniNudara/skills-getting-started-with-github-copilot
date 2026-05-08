import pytest
from httpx import AsyncClient
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.get("/activities")
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()

@pytest.mark.asyncio
async def test_signup_for_activity_success():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

@pytest.mark.asyncio
async def test_signup_duplicate():
    # Arrange
    test_email = "michael@mergington.edu"  # Already signed up
    activity = "Chess Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

@pytest.mark.asyncio
async def test_signup_nonexistent_activity():
    # Arrange
    test_email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
