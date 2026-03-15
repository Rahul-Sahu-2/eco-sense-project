from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import numpy as np
from PIL import Image
import io

from backend.services import cnn_service, blockchain_service

router = APIRouter(prefix="/api/blockchain", tags=["Blockchain"])


@router.post("/verify")
async def verify(file: UploadFile = File(...)):
    """Verify if an uploaded image is waste using CNN."""
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image_array = np.array(image)
    is_waste, waste_conf, non_waste_conf = cnn_service.check_waste_cnn(image_array)
    tokens = blockchain_service.calculate_tokens(waste_conf) if is_waste else 0

    return {
        "is_waste": is_waste,
        "waste_confidence": round(waste_conf, 1),
        "non_waste_confidence": round(non_waste_conf, 1),
        "tokens_eligible": tokens,
    }


class RewardRequest(BaseModel):
    wallet: str
    tokens: int


@router.post("/reward")
async def reward(req: RewardRequest):
    """Send blockchain reward tokens."""
    if not blockchain_service.is_valid_address(req.wallet):
        return {"success": False, "error": "Invalid wallet address"}

    if req.tokens <= 0:
        return {"success": False, "error": "No tokens to send"}

    tx_hash = blockchain_service.reward_user(req.wallet, req.tokens)

    if tx_hash.startswith("0x"):
        return {"success": True, "tx_hash": tx_hash}
    else:
        return {"success": False, "error": tx_hash}
