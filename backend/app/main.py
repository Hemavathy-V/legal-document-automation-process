"""
Legal Contract Management API.
Routes are grouped by feature: login, contracts, templates, users.
"""
import sys
import os

# Add backend directory to sys.path so `app` package imports resolve
# This allows running from project root with: uvicorn backend.app.main:app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi import Request

from app.routers import contracts_router, login_router, templates_router, generator_router, users_router
from app.api.clause_routes import router as clause_router
from app.core.logger import get_logger
from app.core.log_config import setup_logging

# Setup logging
setup_logging()

logger = get_logger(__name__)

app = FastAPI(title="Legal Contract Management API")
logger.info("Initializing Legal Contract Management API")

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)
logger.info(f"CORS middleware configured with origins: {origins}")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests"""
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)
    
    logger.info(
        f"HTTP {request.method} {request.url.path} - {response.status_code} ({duration}s)"
    )
    return response


# Include routers
app.include_router(login_router.router, prefix="/api")
logger.info("Login router included")

app.include_router(contracts_router.router, prefix="/api")
logger.info("Contracts router included")

app.include_router(templates_router.router, prefix="/api")
logger.info("Templates router included")
app.include_router(users_router.router, prefix="/api")
logger.info("Users router included")

app.include_router(generator_router.router, prefix="/api")
logger.info("Generator (dynamic contract) router included")

app.include_router(clause_router, prefix="/api")
logger.info("Clause router included")


@app.get("/")
def home():
    """Root endpoint"""
    return {"message": "Legal Contract Management API is running"}


@app.get("/health")
def health():
    """Health check endpoint"""
    logger.debug("Health check endpoint called")
    return {"status": "ok"}


