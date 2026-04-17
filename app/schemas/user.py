from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Données reçues pour créer un compte
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Données reçues pour se connecter
class UserLogin(BaseModel):
    email: str
    password: str

# Données renvoyées au client (jamais le mot de passe !)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Token JWT renvoyé après connexion
class Token(BaseModel):
    access_token: str
    token_type: str