from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
from jose import JWTError, jwt
import bcrypt
import os

#fastAPI app
app = FastAPI()

#database setup
DATABASE_URL = "postgresql+psycopg2://tradingapptest:Alkason%40123@34.131.67.65:5432/tradingappdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#secret key for JWT
SECRET_KEY = "d35f8816cfe0c43ff3b8172444fecb5a8182240b7c728f09b1191fa313f9dc25"
ALGORITHM = "HS256"

def hello():
    return {"message": "message"}

#jwt token creation
def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

#jwt token verification
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

#user model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

#pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(UserCreate):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#password hashing
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

#password verification
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

#register a new user
@app.post("/register", response_model=UserInDB)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#login and get JWT token
@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

#logout (clear JWT token on client side)
@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"msg": "Successfully logged out"}
