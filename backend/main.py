from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import hashlib
import uuid
import os
from typing import List

from database import SessionLocal, engine, Base
from models import User, Prediction
from ml_model import model_instance

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OcuVision AI API")

# Setup CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change to specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/register")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(password)
    new_user = User(name=name, email=email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_pw = hash_password(password)
    user = db.query(User).filter(User.email == email, User.password == hashed_pw).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    return {"message": "Login successful", "user": {"id": user.id, "name": user.name, "email": user.email}}

@app.post("/predict")
async def predict(user_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    # Read image bytes
    image_bytes = await file.read()
    
    # Run prediction
    label, confidence = model_instance.predict(image_bytes)
    
    # Save image to uploads folder just to keep history (optional but good for hackathons)
    os.makedirs("../uploads", exist_ok=True)
    file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    safe_filename = f"{uuid.uuid4().hex}.{file_ext}"
    file_path = os.path.join("../uploads", safe_filename)
    
    with open(file_path, "wb") as f:
        f.write(image_bytes)
        
    # Save to database
    new_prediction = Prediction(
        user_id=user_id,
        image_path=safe_filename, # Store filename
        prediction=label,
        confidence=confidence
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    
    return {
        "prediction": label,
        "confidence": confidence,
        "image_path": safe_filename,
        "created_at": new_prediction.created_at
    }

@app.get("/history/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(Prediction).filter(Prediction.user_id == user_id).order_by(Prediction.created_at.desc()).all()
    return history

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model_instance.is_loaded}
