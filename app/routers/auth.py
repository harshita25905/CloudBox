from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.crud.user import create_user, get_user_by_email
from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.core.logger import logger
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = create_user(db, user)

    return new_user


@router.get("/token")
def test_token():

    token = create_access_token(
        {
            "sub": "harshita@gmail.com"
        }
    )

    return {
        "access_token": token
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = get_user_by_email(db, form_data.username)

    if not db_user:

        logger.warning(
        f"Failed login attempt for {form_data.username} (user not found)"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):

        logger.warning(
        f"Failed login attempt for {form_data.username} (wrong password)"
        )
        
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    logger.info("User %s logged in successfully", db_user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }