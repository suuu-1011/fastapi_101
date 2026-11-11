from datetime import timedelta
from application.pms.security import create_token

def test_teacher_login(client, teacher):
    response = client.post(
        "/auth/login",
        json={"email": "teacher@test.com", "password": "Teacher123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_student_login(client, student):
    response = client.post(
        "/auth/login",
        json={"email": "student@test.com", "password": "Student123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_invalid_password(client, teacher):
    response = client.post(
        "/auth/login",
        json={"email": "teacher@test.com", "password": "WrongPassword"}
    )
    assert response.status_code == 401


def test_missing_token(client):
    response = client.get("/pms/tasks/")
    assert response.status_code == 401


def test_student_cannot_access_teacher_endpoint(client, student_token):
    response = client.get(
        "/pms/tasks/",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 403

def test_expired_token(client, teacher):
    expired_token = create_token(
        {
            "sub": str(teacher.id),
            "role": "teacher",
            "sid": "expired-session",
            "type": "access"
        },
        timedelta(seconds=-1)
    )

    response = client.get(
        "/pms/tasks/",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 401
