from fastapi import FastAPI
from fastapi import Request
import uvicorn



app = FastAPI(
    title="Swiggy Order Service",
    description=(
        "Internal API for managing orders"
        "Habdle creation, tracking of delivery system"
    ),
    version="1.1.2.3",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

@app.get("/")
def read_root():
    """Root endpoint - Health Check"""
    # FatsAPI convert this dict to json
    return {
        "message": "Welcome to swiggy Order service",
        "status":"healthy"
    }

@app.get("/about")
def about():
    """Return API metaData"""
    return {
        "serive":"Order_service",
        "team":"Backend plateform",
        "region":"ap-south-1",
        "version":"1.2.2"
    }