"""
Legal Contract Management API.
Routes are grouped by feature: login, contracts, templates, users.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from backend.app.routers import contracts_router, login_router, templates_router, users_router
from backend.app.core.logger import get_logger

from backend.app.api.clause_routes import router as clause_router
from backend.app.core.log_config import setup_logging

# Setup logging
setup_logging()
logger = get_logger("api")

# Create app
app = FastAPI(
    title="Legal Document Automation API",
    version="1.0.0"
)
logger = get_logger("api")
logger.info("Initializing API")

# Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)

    logger.info(
        "api_request",
        extra={
            "method": request.method,
            "url": str(request.url),
            "status": response.status_code,
            "duration": duration
        }
    )
    return response


# CORS
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:8000/docs"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS enabled for: {origins}")

# Routers
app.include_router(clause_router)
app.include_router(login_router.router, prefix="/api")
app.include_router(contracts_router.router, prefix="/api")
app.include_router(templates_router.router, prefix="/api")
logger.info("Templates router included")
app.include_router(users_router.router, prefix="/api")
logger.info("Users router included")

logger.info("Routers registered")

# Health Routes
@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
