from fastapi import FastAPI
from app.api.v1.endpoints import kundli, geo

app = FastAPI(
    title="Jyotish Backend",
    description="High-precision astrology backend system",
    version="0.1.0"
)

app.include_router(kundli.router, prefix="/api/v1/kundli", tags=["kundli"])
app.include_router(geo.router, prefix="/api/v1/geo", tags=["geo"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
