# FastAPI Authentication and Celery Project

### Project Overview
This project is a minimal FastAPI application that implements user authentication (login, register features) and uses Celery with Redis for asynchronous task processing. It provides an API for managing user accounts and authenticating users, as well as an example feature to calculate the first N prime numbers using a Celery task. The project uses PostgreSQL for the database backend.

### Getting Started
- Python 3.x
- PostgreSQL
- Redis

### Setup Instructions
- Clone the Repository:

```
git clone <repository-url>
cd fastapi_celery_project
```

NOTE: Replace <repository-url> with the URL of the repository.

- Create a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```

- Install Requirements
```
pip install -r requirements.txt
```

- Setup PostgreSQL

- Update Credentials

### Running the Application

- Use run.py : `python3 run.py`
- OR, run FastAPI Server: `uvicorn app.main:app --reload`