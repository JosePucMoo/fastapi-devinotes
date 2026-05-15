from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.api.dependencies import DBSession
from app.models.user import UserCreate, UserRead
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: DBSession):
    userRepository = UserRepository(db)
    service = AuthService(userRepository)
    return service.register(payload)


@router.post("/login")
def login(email: str, password: str, db: DBSession):
    userRepository = UserRepository(db)
    service = AuthService(userRepository)
    token = service.login(email, password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token")
def login(db: DBSession, form: OAuth2PasswordRequestForm = Depends()):
    email = form.username
    password = form.password
    userRepository = UserRepository(db)
    service = AuthService(userRepository)
    token = service.login(email, password)
    return {"access_token": token, "token_type": "bearer"}