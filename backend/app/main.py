from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app import models  # noqa: F401 - registers ORM models with Base
from app.routers import auth, vehicles

# For a kata this creates tables on startup. For a production deployment, use migrations.
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Car Dealership Inventory API", version="1.0.0", description="REST API for vehicle inventory, authentication and purchases.")
origins = [item.strip() for item in settings.cors_origins.split(",") if item.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router)
app.include_router(vehicles.router)

@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok"}
