
from fastapi import FastAPI, Request
import time
from app.api.clause_routes import router
from app.core.logger import get_logger
from app.core.log_config import setup_logging

setup_logging()

app = FastAPI()

logger = get_logger("api")

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

app.include_router(router)

@app.get("/")
def home():

    return {"message": "API is running"}

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


from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.collect_inputs.dynamic_questions import ContractProcessor


class ContractRequest(BaseModel):
    template_name: str = Field(..., min_length=1)
    data: Dict[str, Any]


class TemplatesResponse(BaseModel):
    templates: List[str]


class PlaceholdersResponse(BaseModel):
    template_name: str
    simple_fields: List[str]
    loop_fields: Dict[str, List[str]]


class GenerateContractResponse(BaseModel):
    message: str
    template_name: str
    file: str
    generated_at: str
    total_fields: int


app = FastAPI(title="Legal Document Automation API", version="1.0.0")

# CORS configuration for frontend development
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

# Initialize processor
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
TEMPLATES_DIR = PROJECT_ROOT / "sample_templates"
OUTPUT_DIR = BASE_DIR / "output"

processor = ContractProcessor(templates_dir=TEMPLATES_DIR, output_dir=OUTPUT_DIR)


@app.get("/")
def root():
    return {"message": "Legal Document Automation API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/templates", response_model=TemplatesResponse)
def list_templates() -> TemplatesResponse:
    templates = processor.list_template_names()
    return TemplatesResponse(templates=templates)


@app.get("/templates/{template_name}/placeholders", response_model=PlaceholdersResponse)
def get_placeholders(template_name: str) -> PlaceholdersResponse:
    try:
        simple_fields, loop_fields = processor.get_template_placeholders(template_name)
        return PlaceholdersResponse(
            template_name=template_name,
            simple_fields=simple_fields,
            loop_fields=loop_fields,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unable to parse template: {exc}") from exc


@app.post("/contracts/data", response_model=GenerateContractResponse)
def generate_contract(request: ContractRequest) -> GenerateContractResponse:
    try:
        output_path = processor.save_contract_data(request.template_name, request.data)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unable to save contract data: {exc}") from exc

    return GenerateContractResponse(
        message="Contract data saved successfully",
        template_name=request.template_name,
        file=str(output_path),
        generated_at=datetime.now().isoformat(),
        total_fields=processor._count_fields(request.data),
    )


