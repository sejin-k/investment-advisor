"""모든 엔드포인트 라우터를 통합하는 API v1 라우터."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, stocks

api_router = APIRouter()

# 모든 엔드포인트 라우터 포함
api_router.include_router(health.router)
api_router.include_router(stocks.router)
