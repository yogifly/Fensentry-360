from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import Base, engine
from app.database import models
from app.api.routes import router
from app.config.settings import CORS_ORIGINS
Base.metadata.create_all(bind=engine)
app=FastAPI(title="FinSentry 360",description="AI-powered financial fraud defense MVP — DEMO / SIMULATION ONLY",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=CORS_ORIGINS,allow_methods=["*"],allow_headers=["*"])
app.include_router(router)
