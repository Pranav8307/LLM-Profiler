# app/api/v1/endpoints/generate.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import time

from app.schemas.generate import GenerateRequest, GenerateResponse
from app.services.llm_service import LLMService
from app.services.cache_service import CacheService
from app.services.rate_limiter import RateLimiter
from app.services.logging_service import LoggingService
from app.db.session import get_db

router = APIRouter()

llm_service = LLMService()
cache_service = CacheService()
rate_limiter = RateLimiter()
logging_service = LoggingService()


@router.post("/", response_model=GenerateResponse)
def generate(request: GenerateRequest, db: Session = Depends(get_db)):
    user_id = request.user_id or "anonymous"

    # Rate limiting
    if not rate_limiter.is_allowed(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    start = time.time()

    # Cache key
    cache_key = cache_service.make_key(request.prompt, "default")

    # CHECK CACHE
    cached = cache_service.get(cache_key)
    if cached:
        latency = round((time.time() - start) * 1000, 2)

        response = {
            "answer": cached["answer"],
            "latency_ms": latency,
            "tokens": cached["tokens"],
            "cost": cached["cost"],
            "cached": True
        }

        # LOG CACHE HIT
        logging_service.log(db, {
            "prompt": request.prompt,
            "response": response["answer"],
            "latency_ms": latency,
            "tokens": response["tokens"],
            "cost": response["cost"],
            "estimated_cost": response["cost"],
            "cached": True,
        })

        return response

    # 🔹 LLM CALL
    result = llm_service.generate(request.prompt)

    latency = round((time.time() - start) * 1000, 2)

    response = {
        "answer": result["answer"],
        "latency_ms": latency,
        "tokens": result["tokens"],
        "cost": result["cost"],
        "cached": False,
    }

    # Cache result (store only reusable fields)
    cache_service.set(cache_key, {
        "answer": response["answer"],
        "tokens": response["tokens"],
        "cost": response["cost"]
    })

    # LOG NORMAL REQUEST
    logging_service.log(db, {
        "prompt": request.prompt,
        "response": response["answer"],
        "latency_ms": latency,
        "tokens": response["tokens"],
        "cost": response["cost"],
        "estimated_cost": 0.0,      
        "cached": False,
    })

    return response