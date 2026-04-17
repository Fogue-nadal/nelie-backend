from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import (
    get_user_by_email, create_user, verify_password, create_access_token
)

router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Créer un nouveau compte utilisateur"""
    # Vérifie si l'email existe déjà
    existing = get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Cet email est déjà utilisé"
        )
    return create_user(db, user_data.username, user_data.email, user_data.password)

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Se connecter et recevoir un token JWT"""
    user = get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect"
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}