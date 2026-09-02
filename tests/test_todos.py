def test_create_todo_authenticated(client):
    # First, register a new user
    reg_response = client.post("/api/v1/auth/register", json={"email": "dev@email.com", "password": "secretpassword"})
    print("Registration Response:", reg_response.json())  # Debugging line

    login_response = client.post("/api/v1/auth/login", data={"username": "dev@email.com", "password": "secretpassword"})#login for track error


    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"#validate login response

    token = login_response.json()["access_token"]

    # Execute authenticated request to create a todo
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/v1/todos/", json={"task": "Writing automated tests"}, headers=headers)

    # Assert the response
    assert response.status_code == 201
    data = response.json()
    assert data["task"] == "Writing automated tests"
    assert data["completed"] is False
    assert "id" in data