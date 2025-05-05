from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import List

DATABASE_URL = "sqlite:///./reviews.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    comment = Column(Text)

Base.metadata.create_all(bind=engine)

class ReviewCreate(BaseModel):
    username: str
    comment: str

class ReviewRead(BaseModel):
    id: int
    username: str
    comment: str

    class Config:
        orm_mode = True

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/reviews/", response_model=ReviewRead)
def add_review(review: ReviewCreate):
    db = SessionLocal()
    db_review = Review(username=review.username, comment=review.comment)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    db.close()
    return db_review

@app.get("/reviews/", response_model=List[ReviewRead])
def get_reviews():
    db = SessionLocal()
    reviews = db.query(Review).all()
    db.close()
    return reviews
