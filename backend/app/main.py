from fastapi import FastAPI
from app.api.clause_routes import router as clause_router
from dotenv import load_dotenv
import os

load_dotenv()

hf_token = os.getenv("HF_TOKEN")

app = FastAPI(title="Legal Automation Backend")

app.include_router(clause_router, prefix="/clauses")
