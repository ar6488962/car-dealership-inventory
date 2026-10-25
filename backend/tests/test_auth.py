def register(client, email="user@example.com", password="StrongPass123"):
    return client.post("/api/auth/register", json={"name":"Test User", "email":email, "password":password})

def test_register_creates_user_without_returning_password(client):
    response = register(client)
    assert response.status_code == 201
    assert response.json()["email"] == "user@example.com"
    assert "password" not in response.json() and "password_hash" not in response.json()

def test_duplicate_email_is_rejected(client):
    assert register(client).status_code == 201
    assert register(client).status_code == 409

def test_login_returns_bearer_token(client):
    register(client)
    response = client.post("/api/auth/login", json={"email":"user@example.com", "password":"StrongPass123"})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]

def test_wrong_password_is_rejected(client):
    register(client)
    response = client.post("/api/auth/login", json={"email":"user@example.com", "password":"WrongPass123"})
    assert response.status_code == 401

def test_short_password_is_rejected(client):
    response = client.post("/api/auth/register", json={"name":"Test User", "email":"user@example.com", "password":"short"})
    assert response.status_code == 422

def test_invalid_token_is_rejected_for_protected_route(client):
    response = client.post("/api/vehicles/1/purchase", headers={"Authorization": "Bearer not-a-jwt"})
    assert response.status_code == 401

def test_registration_does_not_allow_client_role_escalation(client):
    response = client.post("/api/auth/register", json={
        "name": "Attempted Admin",
        "email": "attempt@example.com",
        "password": "StrongPass123",
        "role": "admin",
    })
    assert response.status_code == 201
    assert response.json()["role"] == "user"
