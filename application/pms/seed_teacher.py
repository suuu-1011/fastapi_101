from getpass import getpass

from .database import SessionLocal
from . import models
from .security import hash_password


def create_teacher():
    db = SessionLocal()

    try:
        name = input("Teacher name: ").strip()
        email = input("Teacher email: ").strip().lower()
        phone = input("Teacher phone: ").strip()

        password = getpass("Teacher password: ")
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            print("Passwords do not match.")
            return

        if len(password) < 8:
            print("Password must be at least 8 characters.")
            return

        existing_user = db.query(models.User).filter(
            models.User.email == email
        ).first()

        if existing_user:
            print("This email is already registered.")
            return

        teacher = models.User(
            name=name,
            email=email,
            phone=phone,
            password_hash=hash_password(password),
            role="teacher",
            status="active"
        )

        db.add(teacher)
        db.commit()

        print("Teacher account created successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    create_teacher()






