import os
import pytest
import random
from fastapi.testclient import TestClient
from app.main import app

# Initialize TestClient
client = TestClient(app)

def test_health():
    """Verify health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_waitlist():
    """Verify waitlist registration with random email."""
    email = f"test_waitlist_{random.randint(1, 99999)}@example.com"
    response = client.post("/api/v1/waitlist", json={"email": email})
    assert response.status_code in (200, 201)

def test_auth_and_protected_routes():
    """Full flow: Register, Login, and Test Protected Endpoints."""
    email = f"user_{random.randint(1, 99999)}@example.com"
    password = "testpassword123"
    
    # 1. Register
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Deep Test User"
    })
    assert reg_resp.status_code in (201, 409)
    
    # 2. Login
    login_resp = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Test Users/Me
    me_resp = client.get("/api/v1/users/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == email
    
    # 4. Test Transactions & Auto-Categorization
    tx_payload = {
        "amount": 5000.0,
        "description": "Uber trip to office",
        "transaction_type": "debit"
    }
    tx_resp = client.post("/api/v1/transactions", json=tx_payload, headers=headers)
    assert tx_resp.status_code == 201
    tx_data = tx_resp.json()
    assert tx_data["category"] == "Transport"
    assert tx_data["amount"] == 5000.0
    
    # 5. List Transactions
    list_tx_resp = client.get("/api/v1/transactions", headers=headers)
    assert list_tx_resp.status_code == 200
    assert len(list_tx_resp.json()) >= 1
    
    # 6. Forecast
    forecast_resp = client.get("/api/v1/forecast", headers=headers)
    assert forecast_resp.status_code == 200
    assert "safe_to_spend" in forecast_resp.json()
    assert len(forecast_resp.json()["forecast"]) == 14
    
    # 7. Nudges
    nudges_resp = client.get("/api/v1/nudges", headers=headers)
    assert nudges_resp.status_code == 200
    # Since we can't easily create a nudge via API, we just verify the endpoint returns a list
    assert isinstance(nudges_resp.json(), list)

def test_chat_logic():
    """Verify AI chat logic with specific patterns."""
    # Login a temporary user
    email = f"chat_user_{random.randint(1, 99999)}@example.com"
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "password",
        "full_name": "Chat User"
    })
    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": "password"})
    headers = {"Authorization": f"Bearer {login_resp.json()['access_token']}"}

    # Test 'Can I afford' pattern
    resp1 = client.post("/api/v1/chat", json={"message": "Can I afford to buy shoes for ₦20,000?"}, headers=headers)
    assert resp1.status_code == 200
    assert "waiting 3 days" in resp1.json()["reply"].lower()
    assert resp1.json()["amount_referenced"] == 20000.0

    # Test 'How much spend' pattern
    resp2 = client.post("/api/v1/chat", json={"message": "how much can i spend today?"}, headers=headers)
    assert resp2.status_code == 200
    assert "safe to spend" in resp2.json()["reply"].lower()

    # Test Default response
    resp3 = client.post("/api/v1/chat", json={"message": "What is the capital of France?"}, headers=headers)
    assert resp3.status_code == 200
    assert "still learning" in resp3.json()["reply"].lower()

if __name__ == "__main__":
    pytest.main(["-v", __file__])
