from fastapi import FastAPI
from app.api.routers import api_router

app = FastAPI(
    title="Invoices system ⒶⓅⒾ",
    description="Managment API for invoices 📑 📝 📜",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api")