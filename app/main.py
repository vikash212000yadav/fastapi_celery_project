from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth, celery_worker
from .database import engine
from credentials import SLEEP_TIME


# Create the database tables based on SQLAlchemy models
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()


# Root path endpoint for testing purpose
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Endpoint for user registration
@app.post("/register/")
def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


# Endpoint for user login
@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint to get first n prime numbers using async celery call
@app.get("/calculate-primes/{n}")
def calculate_primes(n: int, current_user: schemas.UserInDB = Security(auth.get_current_user)):
    task = celery_worker.get_primes.delay(n, SLEEP_TIME)
    return {"message": "Processing", "task_id": task.id}


# Endpoint to check the task-status using task_id
@app.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    task_result = celery_worker.celery.AsyncResult(task_id)
    if task_result.ready():
        return {"status": "Completed", "result": task_result.get()}
    else:
        return {"status": "Processing"}
