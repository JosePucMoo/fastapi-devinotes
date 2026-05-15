
from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserCreate
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository
        
    def register(self, payload: UserCreate) -> User:
        if self.userRepository.get_by_email(payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email it's alredy in use"
            )
        user = User(
            email= payload.email,
            full_name= payload.full_name,
            hashed_password= hash_password(payload.password[:72])
        )
        
        return self.userRepository.create(user=user)
    
    def login(self, email:str, password:str) -> str:
        user = self.userRepository.get_by_email(email=email)
        
        if not user or not verify_password(password[:72], user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The email address or password is incorrect."
            )
            
        token = create_access_token(
            {"sub": str(user.id)}
        )
        return token
