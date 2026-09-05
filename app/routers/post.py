from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    results = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
            isouter=True
        )
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    results = list(map(lambda x: x._mapping, results))
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_dict = post.model_dump()
    new_post = models.Post(owner_id=current_user.id, **post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
            isouter=True
        )
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )
    result = result._mapping if result else None

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return result

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    for key, value in updated_post.model_dump().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
