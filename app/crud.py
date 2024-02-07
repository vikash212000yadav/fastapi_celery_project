from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Context for password hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Retrieve a user by their username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# Create a new user in the database
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Verify if provided password matches the hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
