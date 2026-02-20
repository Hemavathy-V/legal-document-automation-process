from fastapi import FastAPI
from app.api.clause_routes import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def home():
    return {"message": "API is running"}