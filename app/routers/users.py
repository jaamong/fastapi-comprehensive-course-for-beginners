from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    tags=['User'],
    prefix="/users"
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(create_user_request: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    target = create_user_request.password
    create_user_request.password = utils.hash_password(target)

    new_user = models.User(**create_user_request.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user
