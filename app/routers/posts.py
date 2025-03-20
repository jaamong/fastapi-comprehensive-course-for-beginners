from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Post'],
    prefix="/posts"
)


@router.get("", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
async def get_post(id: int,
                   current_user: models.User = Depends(
                       oauth2.get_current_user),
                   db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(create_post_request: schemas.PostCreate,
                      current_user: models.User = Depends(
                          oauth2.get_current_user),
                      db: Session = Depends(get_db)):

    # ** : unpack the dictionary
    new_post = models.Post(**create_post_request.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # return the newly created post

    return new_post


@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, update_post_request: schemas.PostCreate,
                      current_user: models.User = Depends(
                          oauth2.get_current_user),
                      db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(update_post_request.model_dump(),
                      synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,
                      current_user: models.User = Depends(
                          oauth2.get_current_user),
                      db: Session = Depends(get_db)):

    # returns Query object
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # post.fisrt() returns Post class instance
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
