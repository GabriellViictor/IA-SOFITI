from fastapi import FastAPI
from app.api.routes import router as recommendation_router
from app.utils.error_handlers import setup_exception_handlers

app = FastAPI()
setup_exception_handlers(app)

app.include_router(recommendation_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
