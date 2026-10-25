def create_user(client, email="user@example.com", password="StrongPass123"):
    client.post("/api/auth/register", json={"name":"Test User", "email":email, "password":password})
    token = client.post("/api/auth/login", json={"email":email, "password":password}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def create_admin(client):
    # Tests elevate a test user directly in the database; public registration never accepts a role.
    from app.database import get_db
    from app.main import app
    from app.models import User
    db = next(app.dependency_overrides[get_db]())
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        client.post("/api/auth/register", json={"name":"Admin User", "email":"admin@example.com", "password":"StrongPass123"})
        user = db.query(User).filter(User.email == "admin@example.com").first()
    user.role = "admin"; db.commit(); db.close()
    token = client.post("/api/auth/login", json={"email":"admin@example.com", "password":"StrongPass123"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def vehicle_payload(**overrides):
    data = {"make":"Toyota", "model":"Corolla", "category":"Sedan", "price":18000, "quantity":2, "image_url":None}
    data.update(overrides); return data

def test_vehicle_list_is_public_and_initially_empty(client):
    response = client.get("/api/vehicles")
    assert response.status_code == 200 and response.json() == []

def test_only_admin_can_create_vehicle(client):
    user_headers = create_user(client)
    assert client.post("/api/vehicles", json=vehicle_payload(), headers=user_headers).status_code == 403
    admin_headers = create_admin(client)
    response = client.post("/api/vehicles", json=vehicle_payload(), headers=admin_headers)
    assert response.status_code == 201 and response.json()["make"] == "Toyota"

def test_unauthenticated_user_cannot_create_vehicle(client):
    assert client.post("/api/vehicles", json=vehicle_payload()).status_code == 401

def test_search_filters_by_make_and_price(client):
    admin = create_admin(client)
    client.post("/api/vehicles", json=vehicle_payload(), headers=admin)
    client.post("/api/vehicles", json=vehicle_payload(make="Honda", model="Civic", price=26000), headers=admin)
    response = client.get("/api/vehicles/search?make=toyota&min_price=10000&max_price=20000")
    assert response.status_code == 200
    assert len(response.json()) == 1 and response.json()[0]["make"] == "Toyota"

def test_purchase_decreases_stock_and_records_purchase(client):
    admin = create_admin(client)
    user = create_user(client)
    vehicle = client.post("/api/vehicles", json=vehicle_payload(quantity=1), headers=admin).json()
    response = client.post(f"/api/vehicles/{vehicle['id']}/purchase", headers=user)
    assert response.status_code == 201
    assert response.json()["vehicle"]["quantity"] == 0
    assert client.get("/api/vehicles").json()[0]["quantity"] == 0

def test_cannot_purchase_when_out_of_stock(client):
    admin = create_admin(client); user = create_user(client)
    vehicle = client.post("/api/vehicles", json=vehicle_payload(quantity=0), headers=admin).json()
    response = client.post(f"/api/vehicles/{vehicle['id']}/purchase", headers=user)
    assert response.status_code == 409

def test_regular_user_cannot_restock_or_delete(client):
    admin = create_admin(client); user = create_user(client)
    vehicle = client.post("/api/vehicles", json=vehicle_payload(), headers=admin).json()
    assert client.post(f"/api/vehicles/{vehicle['id']}/restock", json={"quantity":2}, headers=user).status_code == 403
    assert client.delete(f"/api/vehicles/{vehicle['id']}", headers=user).status_code == 403

def test_admin_can_restock_and_delete_vehicle_without_purchase_history(client):
    admin = create_admin(client)
    vehicle = client.post("/api/vehicles", json=vehicle_payload(quantity=1), headers=admin).json()
    response = client.post(f"/api/vehicles/{vehicle['id']}/restock", json={"quantity":3}, headers=admin)
    assert response.status_code == 200 and response.json()["quantity"] == 4
    assert client.delete(f"/api/vehicles/{vehicle['id']}", headers=admin).status_code == 204

def test_update_vehicle_requires_authentication(client):
    admin = create_admin(client)
    vehicle = client.post("/api/vehicles", json=vehicle_payload(), headers=admin).json()
    assert client.put(f"/api/vehicles/{vehicle['id']}", json={"price":19000}).status_code == 401
    user = create_user(client)
    response = client.put(f"/api/vehicles/{vehicle['id']}", json={"price":19000}, headers=user)
    assert response.status_code == 200 and response.json()["price"] == 19000

def test_vehicle_update_rejects_blank_text(client):
    admin = create_admin(client)
    vehicle = client.post("/api/vehicles", json=vehicle_payload(), headers=admin).json()
    response = client.put(f"/api/vehicles/{vehicle['id']}", json={"make": "   "}, headers=admin)
    assert response.status_code == 422

def test_vehicle_not_found_operations_return_404(client):
    admin = create_admin(client)
    user = create_user(client)
    assert client.put("/api/vehicles/9999", json={"price": 1}, headers=user).status_code == 404
    assert client.post("/api/vehicles/9999/restock", json={"quantity": 1}, headers=admin).status_code == 404
    assert client.post("/api/vehicles/9999/purchase", headers=user).status_code == 404

def test_admin_cannot_delete_vehicle_with_purchase_history(client):
    admin = create_admin(client)
    user = create_user(client)
    vehicle = client.post("/api/vehicles", json=vehicle_payload(quantity=1), headers=admin).json()
    assert client.post(f"/api/vehicles/{vehicle['id']}/purchase", headers=user).status_code == 201
    response = client.delete(f"/api/vehicles/{vehicle['id']}", headers=admin)
    assert response.status_code == 409

def test_restock_requires_a_positive_integer(client):
    admin = create_admin(client)
    vehicle = client.post("/api/vehicles", json=vehicle_payload(), headers=admin).json()
    assert client.post(f"/api/vehicles/{vehicle['id']}/restock", json={"quantity": 0}, headers=admin).status_code == 422
    assert client.post(f"/api/vehicles/{vehicle['id']}/restock", json={"quantity": -1}, headers=admin).status_code == 422
