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