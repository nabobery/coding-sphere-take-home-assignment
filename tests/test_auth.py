from fastapi.testclient import TestClient
import pytest

def test_register_user(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "newuser",
            "password": "password123",
            "email": "newuser@example.com",
            "full_name": "New User",
            "role": "user"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "user"
    assert "id" in data

def test_register_duplicate_username(client: TestClient):
    # Register user first time
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "duplicate",
            "password": "password123",
            "role": "user"
        },
    )
    
    # Try to register with same username
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "duplicate",
            "password": "different",
            "role": "user"
        },
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_user(client: TestClient):
    # Register a user first
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "loginuser",
            "password": "password123",
            "role": "user"
        },
    )
    
    # Login with the user
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "loginuser",
            "password": "password123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "loginuser"

def test_login_invalid_credentials(client: TestClient):
    # Register a user first
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "validuser",
            "password": "correctpass",
            "role": "user"
        },
    )
    
    # Try to login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "validuser",
            "password": "wrongpass"
        },
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]