from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

from backend.services import report_service
from backend.config import CSV_PATH

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/reports")
async def get_reports():
    reports = report_service.get_all_reports()
    return {"reports": reports}


@router.get("/stats")
async def get_stats():
    stats = report_service.get_stats()
    return stats


@router.get("/reports/download")
async def download_reports():
    if os.path.exists(CSV_PATH):
        return FileResponse(
            CSV_PATH,
            media_type="text/csv",
            filename="waste_reports.csv",
        )
    return {"error": "No reports file found"}
