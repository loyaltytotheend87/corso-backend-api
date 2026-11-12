from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
import models, schemas
from database import engine, get_db

# Crea automaticamente le tabelle nel database se non esistono
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + SQLAlchemy Enterprise API")

# ROTTE CRUD USERS
@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=List[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# ROTTE CRUD POSTS
@app.post("/posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post non trovato")
    db.delete(post)
    db.commit()

# QUERY COMPLESSA: OUTER JOIN + GROUP BY + ORDER BY
@app.get("/analytics/users-summary", response_model=List[schemas.UserAnalytics])
def get_user_analytics(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.User.id.label("user_id"),
            models.User.name.label("user_name"),
            func.count(models.Post.id).label("total_posts"),
            func.coalesce(func.sum(models.Post.views), 0).label("total_views"),
        )
        .outerjoin(models.Post, models.User.id == models.Post.author_id)
        .group_by(models.User.id, models.User.name)
        .order_by(desc("total_views"))
        .all()
    )
    return results