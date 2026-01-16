from fastapi import FastAPI
from app.api.v1.endpoints import kundli

app = FastAPI(
    title="Jyotish Backend",
    description="High-precision astrology backend system",
    version="0.1.0"
)

app.include_router(kundli.router, prefix="/api/v1/kundli", tags=["kundli"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
