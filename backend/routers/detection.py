from fastapi import APIRouter
from pydantic import BaseModel

from backend.services import yolo_service, groq_service

router = APIRouter(prefix="/api/detect", tags=["Detection"])


class DetectRequest(BaseModel):
    image: str          # base64-encoded image frame
    confidence: float = 0.5


class TipRequest(BaseModel):
    items: list[str]


@router.post("")
async def detect(req: DetectRequest):
    result = yolo_service.detect_from_base64(req.image, req.confidence)
    return result


@router.post("/tip")
async def get_tip(req: TipRequest):
    tip = groq_service.get_short_tip(req.items)
    return {"tip": tip}


@router.post("/explain")
async def get_explanation(req: TipRequest):
    explanation = groq_service.get_deep_explanation(req.items)
    return {"explanation": explanation}
