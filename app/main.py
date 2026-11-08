from fastapi import FastAPI

from app.routers import audits

app = FastAPI(
    title="Audit Service API",
    description="REST API для управления внутренними аудитами качества (АС ВАК)",
    version="1.0.0",
)

app.include_router(audits.router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
