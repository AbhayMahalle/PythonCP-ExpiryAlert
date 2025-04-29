from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database import User, get_db, hash_password, verify_password 


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/SignUp")
def signup(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    shop_name: str = Form(...),
    db: Session = Depends(get_db)
    ):

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(password)
    new_user = User(full_name=full_name, email=email, hashed_password=hashed, shop_name = shop_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
    ):

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        # Let user know
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {"message": f"Welcome back, {user.full_name}"}
