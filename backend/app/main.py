from fastapi import FastAPI
from app.api.clause_routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Legal Document Automation API is running"}
"""
Legal Contract Management API.
Routes are grouped by feature: login, contracts, templates.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import contracts_router, login_router, templates_router
from backend.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Legal Contract Management API")
logger.info("Initializing Legal Contract Management API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
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

app.include_router(login_router.router, prefix="/api")
logger.info("Login router included")
app.include_router(contracts_router.router, prefix="/api")
logger.info("Contracts router included")
app.include_router(templates_router.router, prefix="/api")
logger.info("Templates router included")


@app.get("/health")
def health():
    logger.debug("Health check endpoint called")
    return {"status": "ok"}
