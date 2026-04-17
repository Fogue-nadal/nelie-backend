from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models.database import Base, engine
from app.routers import auth
from app.routers import auth, budget

# Crée toutes les tables dans la base de données au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend du chatbot NELIE — Transparence budgétaire Cameroun",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistre les routes d'authentification
app.include_router(auth.router)
app.include_router(budget.router)

@app.get("/")
def root():
    return {"message": "NELIE API is running 🚀", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}