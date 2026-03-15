from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
import numpy as np
from PIL import Image
import io

from backend.services import cnn_service, blockchain_service, report_service

from backend.config import WALLET_ADDRESS
router = APIRouter(prefix="/api/citizen", tags=["Citizen"])


@router.get("/config")
async def get_config():
    """Retrieve public configuration like the default wallet address."""
    return {"default_wallet": WALLET_ADDRESS}


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """Analyze an uploaded waste image using the CNN model."""
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image_array = np.array(image)
    result = cnn_service.analyze_waste_image(image_array)
    return result


class ReportRequest(BaseModel):
    name: str
    waste_type: str
    waste_percent: float
    lat: float
    lon: float
    wallet: str = ""


@router.post("/report")
async def submit_report(req: ReportRequest):
    """Submit a waste report and optionally earn blockchain tokens."""
    tokens = 0
    tx_hash = ""

    # Calculate tokens based on waste confidence
    if req.waste_percent >= 90:
        tokens = 5
    elif req.waste_percent >= 80:
        tokens = 3
    elif req.waste_percent >= 70:
        tokens = 1

    # Process blockchain reward if wallet provided and tokens > 0
    if req.wallet and tokens > 0 and blockchain_service.is_valid_address(req.wallet):
        tx_hash = blockchain_service.reward_user(req.wallet, tokens)

    # Save report
    report = report_service.save_report(
        name=req.name,
        waste_type=req.waste_type,
        waste_percent=req.waste_percent,
        lat=req.lat,
        lon=req.lon,
        wallet=req.wallet,
        tx_hash=tx_hash,
        tokens=tokens,
    )

    return {
        "success": True,
        "tokens_earned": tokens,
        "tx_hash": tx_hash,
        "report": report,
    }
