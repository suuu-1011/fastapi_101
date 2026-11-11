def test_teacher_can_create_and_assign_task(client, teacher_token, student):
    response = client.post(
        "/pms/tasks/",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "title": "Complete Python Assignment",
            "description": "Finish the given exercises",
            "status": "pending",
            "user_id": student.id
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Complete Python Assignment"
    assert response.json()["user_id"] == student.id


def test_teacher_can_update_task(client, teacher_token, student):
    create_response = client.post(
        "/pms/tasks/",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "title": "Original Task",
            "description": "Original description",
            "status": "pending",
            "user_id": student.id
        }
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/pms/tasks/{task_id}",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={"title": "Updated Task", "status": "in progress"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["status"] == "in progress"


def test_teacher_can_delete_task(client, teacher_token, student):
    create_response = client.post(
        "/pms/tasks/",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "title": "Task to Delete",
            "description": "Delete this task",
            "status": "pending",
            "user_id": student.id
        }
    )

    task_id = create_response.json()["id"]

    response = client.delete(
        f"/pms/tasks/{task_id}",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )

    assert response.status_code == 200

    check_response = client.get(
        f"/pms/tasks/{task_id}",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )

    assert check_response.status_code == 404


def test_student_cannot_create_task(client, student_token, student):
    response = client.post(
        "/pms/tasks/",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "title": "Unauthorized Task",
            "description": "Student should not create this",
            "status": "pending",
            "user_id": student.id
        }
    )

    assert response.status_code == 403