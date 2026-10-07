from fastapi import APIRouter
from backend.models.schemas import HealthResponse
import ollama

router = APIRouter(prefix="/api/health", tags=["health"])

@router.get("", response_model=HealthResponse)
async def check_health():
    ollama_ok = False
    models_avail = []
    try:
        res = ollama.list()
        ollama_ok = True
        models_avail = [m.model for m in res.models]
    except Exception:
        pass
        
    return HealthResponse(
        status="ok",
        ollama_connected=ollama_ok,
        models_available=models_avail,
        total_documents=0, # skipped
        total_chunks=0 # skipped
    )
