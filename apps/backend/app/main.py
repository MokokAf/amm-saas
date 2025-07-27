from fastapi import FastAPI

app = FastAPI(title="AMM SaaS API", version="0.1.0")

from app.routers.auth import router as auth_router
from app.routers.dossiers import router as dossiers_router

app.include_router(auth_router)
app.include_router(dossiers_router)


@app.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
