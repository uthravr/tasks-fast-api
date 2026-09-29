"""
Comprehensive Test Script for User Management System API
Tests all 10 modules and requirements:
- Registration, validation, duplicate check, password hashing
- Login, credential verification, JWT generation
- Protected endpoints, missing token, invalid token
- CRUD operations for User Profile
- User listing
- Direct database verification in MySQL
"""

import time
import pymysql
from fastapi.testclient import TestClient
from app.main import app
from app.config import DATABASE_URL

client = TestClient(app)

def test_full_flow():
    print("=" * 60)
    print("STARTING FULL API VERIFICATION TEST")
    print("=" * 60)

    unique_suffix = int(time.time())
    test_email = f"john_{unique_suffix}@example.com"
    test_password = "SecurePassword123!"
    test_name = "John Doe"

    # 1. Test Registration
    print("\n[Step 1] Testing User Registration (POST /auth/register)...")
    reg_payload = {
        "name": test_name,
        "email": test_email,
        "password": test_password
    }
    res = client.post("/auth/register", json=reg_payload)
    print(f"Status: {res.status_code}, Response: {res.json()}")
    assert res.status_code == 201
    reg_data = res.json()
    assert reg_data["email"] == test_email
    assert reg_data["name"] == test_name
    assert "id" in reg_data
    user_id = reg_data["id"]

    # 2. Test Duplicate Email Registration
    print("\n[Step 2] Testing Duplicate Email Registration (POST /auth/register)...")
    res_dup = client.post("/auth/register", json=reg_payload)
    print(f"Status: {res_dup.status_code}, Response: {res_dup.json()}")
    assert res_dup.status_code == 400
    assert "already registered" in res_dup.json()["detail"].lower()

    # 3. Test Invalid Registration Inputs
    print("\n[Step 3] Testing Invalid Inputs (Invalid Email)...")
    res_inv = client.post("/auth/register", json={
        "name": "A",
        "email": "not-an-email",
        "password": "123"
    })
    print(f"Status: {res_inv.status_code}")
    assert res_inv.status_code == 422

    # 4. Test Login with Invalid Credentials
    print("\n[Step 4] Testing Login with Wrong Password (POST /auth/login)...")
    res_wrong_pw = client.post("/auth/login", json={
        "email": test_email,
        "password": "WrongPassword!"
    })
    print(f"Status: {res_wrong_pw.status_code}, Response: {res_wrong_pw.json()}")
    assert res_wrong_pw.status_code == 401

    print("\n[Step 5] Testing Login with Non-Existent User...")
    res_no_user = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": test_password
    })
    print(f"Status: {res_no_user.status_code}, Response: {res_no_user.json()}")
    assert res_no_user.status_code == 401

    # 5. Test Successful Login
    print("\n[Step 6] Testing Successful Login (POST /auth/login)...")
    res_login = client.post("/auth/login", json={
        "email": test_email,
        "password": test_password
    })
    print(f"Status: {res_login.status_code}")
    assert res_login.status_code == 200
    login_data = res_login.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"
    token = login_data["access_token"]
    print(f"Acquired JWT Token: {token[:20]}...")

    auth_headers = {"Authorization": f"Bearer {token}"}

    # 6. Test Protected Endpoint without Token
    print("\n[Step 7] Testing Profile Access Without Token (GET /users/me)...")
    res_no_token = client.get("/users/me")
    print(f"Status: {res_no_token.status_code}, Response: {res_no_token.json()}")
    assert res_no_token.status_code == 401

    # 7. Test Protected Endpoint with Invalid Token
    print("\n[Step 8] Testing Profile Access With Invalid Token...")
    res_bad_token = client.get("/users/me", headers={"Authorization": "Bearer invalid.jwt.token"})
    print(f"Status: {res_bad_token.status_code}, Response: {res_bad_token.json()}")
    assert res_bad_token.status_code == 401

    # 8. Test Initial Profile Read (Before profile creation)
    print("\n[Step 9] Reading Own User Info before profile creation (GET /users/me)...")
    res_me_init = client.get("/users/me", headers=auth_headers)
    print(f"Status: {res_me_init.status_code}, Profile: {res_me_init.json().get('profile')}")
    assert res_me_init.status_code == 200
    assert res_me_init.json()["profile"] is None

    # 9. Test Create User Profile (POST /users/profile)
    print("\n[Step 10] Creating User Profile (POST /users/profile)...")
    profile_payload = {
        "phone_number": "+1-555-0199",
        "address": "742 Evergreen Terrace, Springfield",
        "date_of_birth": "1994-08-20",
        "bio": "Enthusiastic Python and FastAPI developer."
    }
    res_create_prof = client.post("/users/profile", json=profile_payload, headers=auth_headers)
    print(f"Status: {res_create_prof.status_code}, Response: {res_create_prof.json()}")
    assert res_create_prof.status_code == 201
    created_prof = res_create_prof.json()
    assert created_prof["phone_number"] == profile_payload["phone_number"]
    assert created_prof["address"] == profile_payload["address"]
    assert created_prof["date_of_birth"] == profile_payload["date_of_birth"]
    assert created_prof["bio"] == profile_payload["bio"]

    # 10. Test Duplicate Profile Creation
    print("\n[Step 11] Testing Duplicate Profile Creation (POST /users/profile)...")
    res_dup_prof = client.post("/users/profile", json=profile_payload, headers=auth_headers)
    print(f"Status: {res_dup_prof.status_code}, Response: {res_dup_prof.json()}")
    assert res_dup_prof.status_code == 400

    # 11. Test Read Own Profile (GET /users/me)
    print("\n[Step 12] Reading Own Profile (GET /users/me)...")
    res_me = client.get("/users/me", headers=auth_headers)
    print(f"Status: {res_me.status_code}, Profile: {res_me.json().get('profile')}")
    assert res_me.status_code == 200
    assert res_me.json()["profile"] is not None
    assert res_me.json()["profile"]["phone_number"] == "+1-555-0199"

    # 12. Test List Registered Users (GET /users)
    print("\n[Step 13] Listing Registered Users (GET /users)...")
    res_users = client.get("/users", headers=auth_headers)
    print(f"Status: {res_users.status_code}, Count: {len(res_users.json())}")
    assert res_users.status_code == 200
    assert len(res_users.json()) >= 1

    # 13. Test Update User Profile (PUT /users/profile)
    print("\n[Step 14] Updating User Profile (PUT /users/profile)...")
    update_payload = {
        "address": "100 New Tech Blvd, Silicon Valley",
        "bio": "Senior Backend Architect & Python Expert."
    }
    res_update = client.put("/users/profile", json=update_payload, headers=auth_headers)
    print(f"Status: {res_update.status_code}, Updated: {res_update.json()}")
    assert res_update.status_code == 200
    updated_data = res_update.json()
    assert updated_data["address"] == "100 New Tech Blvd, Silicon Valley"
    assert updated_data["bio"] == "Senior Backend Architect & Python Expert."
    assert updated_data["phone_number"] == "+1-555-0199"  # Preserved

    # 14. Test Delete User Profile (DELETE /users/profile)
    print("\n[Step 15] Deleting User Profile (DELETE /users/profile)...")
    res_del = client.delete("/users/profile", headers=auth_headers)
    print(f"Status: {res_del.status_code}, Response: {res_del.json()}")
    assert res_del.status_code == 200
    assert "deleted successfully" in res_del.json()["message"].lower()

    # 15. Test Delete Profile When Missing
    print("\n[Step 16] Deleting Already-Deleted Profile...")
    res_del_again = client.delete("/users/profile", headers=auth_headers)
    print(f"Status: {res_del_again.status_code}, Response: {res_del_again.json()}")
    assert res_del_again.status_code == 404

    # 16. Verify Direct MySQL Database State
    print("\n[Step 17] Verifying MySQL Database Records Directly...")
    conn = pymysql.connect(host='localhost', user='root', password='1234', database='user_management_db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, hashed_password FROM users WHERE id = %s;", (user_id,))
    user_row = cursor.fetchone()
    print(f"MySQL User Record: id={user_row[0]}, name={user_row[1]}, email={user_row[2]}")
    assert user_row is not None
    assert user_row[3].startswith("$2b$")  # Verified bcrypt hash

    cursor.execute("SELECT * FROM profiles WHERE user_id = %s;", (user_id,))
    prof_row = cursor.fetchone()
    print(f"MySQL Profile Record (should be None after deletion): {prof_row}")
    assert prof_row is None
    conn.close()

    print("\n" + "=" * 60)
    print("ALL API ENDPOINT TESTS & DATABASE CHECKS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_full_flow()
