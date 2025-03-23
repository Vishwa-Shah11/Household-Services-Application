import sys
import os
# Add backend/ to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
import redis
from app import create_app
from flask_jwt_extended import create_access_token
import json
app1 = create_app()

@pytest.fixture
def client():
    app1.config["TESTING"] = True
    with app1.test_client() as client:
        yield client

def get_auth_headers(client):
    """Generate JWT token for admin login."""
    login_data = {
        "email": "admin@gmail.com",  # Use an actual admin email
        "password": "123456"  # Use actual admin password
    }

    headers = {"Content-Type": "application/json"}
    response = client.post("/auth/login", json=login_data, headers=headers)

    # print("Login Response JSON:", response.json)
    
    assert response.status_code == 200  # Ensure login is successful
    token = response.json.get("token")  # Extract token
    assert token is not None  # Ensure token is returned
    return {"Authorization": f"Bearer {token}"}


def test_cache(client):
    redis_client = redis.Redis(host="localhost", port=6379, db=0)

    # Ensure cache is empty before test
    redis_client.flushdb()

    # Get authentication headers
    headers = get_auth_headers(client)

    # First request (cache miss)
    response = client.get("/admin/services", headers=headers)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "services" in data  # Ensure the 'services' key exists
    assert isinstance(data["services"], list)  # Ensure it's a list
    # assert b"Service List" in response.data  # Modify as per API response

    # Check cache is populated
    keys = redis_client.keys("*")
    assert len(keys) > 0  # At least one cache entry exists

    # Second request (cache hit)
    response2 = client.get("/admin/services", headers=headers)
    assert response2.status_code == 200
    # No DB query should occur if cache is working

# Verify Data is Served from Cache (Cache Hit Test)
def test_cache_hit(client):
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    redis_client.flushdb()  # Clear cache before test

    headers = get_auth_headers(client)

    # First request (Cache Miss)
    response1 = client.get("/admin/services", headers=headers)
    assert response1.status_code == 200

    # Ensure cache is populated
    keys = redis_client.keys("*")
    assert len(keys) > 0  # Cache entry exists

    # Second request (Cache Hit)
    response2 = client.get("/admin/services", headers=headers)
    assert response2.status_code == 200

    # Verify data is the same (served from cache)
    assert response1.data == response2.data

import time

# Verify Cache Expiry
def test_cache_expiry(client):
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    # Ensure cache is empty before test
    redis_client.flushdb()

    headers = get_auth_headers(client)

    # First request (Cache Miss)
    response1 = client.get("/admin/services", headers=headers)
    assert response1.status_code == 200

    # Wait for cache to expire (set time slightly longer than expiry)
    time.sleep(310)  # 5 minutes + buffer

    # # Ensure cache is populated
    # keys = redis_client.keys("*")
    # assert len(keys) > 0

    # # Wait for cache expiry (adjust based on your config, e.g., 5 min = 300s)
    # time.sleep(5)  # Use 300 for actual expiry test

    # Check if cache has expired
    keys_after_expiry = redis_client.keys("*")
    assert len(keys_after_expiry) == 0  # Cache should be empty

# Test API with Invalid Headers (Unauthorized Access)
def test_cache_unauthorized(client):
    response = client.get("/admin/services")  # No auth headers
    assert response.status_code == 401  # Unauthorized

# Test Cache After Data Update
def test_cache_invalidation(client):
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    redis_client.flushdb()

    headers = get_auth_headers(client)

    # First request (Cache Miss)
    response1 = client.get("/admin/services", headers=headers)
    assert response1.status_code == 200

    # Ensure cache is populated
    keys_before_update = redis_client.keys("*")
    assert len(keys_before_update) > 0  # Cache exists

    # Add new service (This should invalidate cache)
    new_service = {
        "name": "New Cleaning Service",
        "base_price": 500,
        "description": "Deep cleaning",
        "time_required": 60,
        "category": "Cleaning"
    }
    create_service_response = client.post("/admin/create_service", json=new_service, headers=headers)
    assert create_service_response.status_code == 201  # Successfully added

    # Fetch services again (should be a fresh DB hit)
    response2 = client.get("/admin/services", headers=headers)
    assert response2.status_code == 200

    # Cache should be updated after service addition
    keys_after_update = redis_client.keys("*")
    assert len(keys_after_update) > 0
