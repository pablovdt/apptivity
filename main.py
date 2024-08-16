from fastapi import FastAPI
from core.config import settings
from api.routes import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION
)

# Incluir el router principal
app.include_router(api_router)

@app.get("/ping")
def read_root():
    return {"message": "pong"}
