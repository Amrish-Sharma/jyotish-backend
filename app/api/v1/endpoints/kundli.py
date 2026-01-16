from fastapi import APIRouter, HTTPException, Depends
from app.models.kundli import KundliRequest, KundliResponse
from app.service.kundli_service import KundliService

router = APIRouter()

def get_kundli_service():
    return KundliService()

@router.post("/generate", response_model=KundliResponse)
async def generate_kundli(
    request: KundliRequest,
    service: KundliService = Depends(get_kundli_service)
):
    try:
        return await service.generate_kundli(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
