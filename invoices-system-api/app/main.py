from fastapi import FastAPI
from app.api.routers import api_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Invoices system ⒶⓅⒾ",
    description="Managment API for invoices 📑 📝 📜",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api")