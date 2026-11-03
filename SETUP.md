# FastAPI 101 - Setup Guide

## 1. Requirements
- Python
- VS Code
- Git
- Postman

## 2. Clone the Repository
git clone https://github.com/suuu-1011/fastapi_101.git

cd fastapi_101

## 3. Create Virtual Environment
python -m venv venv

## 4. Activate Virtual Environment
source venv/Scripts/activate

## 5. Install Dependencies
pip install -r requirements.txt

## 6. Run the API
uvicorn application.quotes:app --reload

## 7. Access the API
API URL: http://127.0.0.1:8000

API Documentation: http://127.0.0.1:8000/docs

## 8. Test Using Postman
Method: GET

URL: http://127.0.0.1:8000/quotes

Expected result: 200 OK

## 9. Git Workflow
git switch -c feature/setup-project

git add .
git commit -m "Add gitignore for project setup"

git push -u origin feature/setup-project