"""주식 관련 API 엔드포인트."""

from fastapi import APIRouter, HTTPException, Path

from app.schemas.stock import StockInfo, StockSymbol
from app.services.stock_service import stock_service

router = APIRouter(tags=["stocks"])


@router.get("/stocks/info/{symbol}", response_model=StockInfo)
async def get_stock_info(
    symbol: str = Path(
        ...,
        description="주식 티커 심볼 (예: AAPL, GOOGL)",
        examples=["AAPL"],
        min_length=1,
        max_length=10,
    )
) -> StockInfo:
    """특정 주식의 상세 정보 조회.

    Args:
        symbol: 주식 티커 심볼

    Returns:
        StockInfo: 상세 주식 정보

    Raises:
        HTTPException: 주식 심볼을 찾을 수 없으면 404
    """
    stock_info = await stock_service.get_stock_info(symbol)

    if not stock_info:
        raise HTTPException(
            status_code=404,
            detail=f"주식 심볼 '{symbol.upper()}'을(를) 찾을 수 없습니다",
        )

    return stock_info


@router.get("/stocks/popular", response_model=list[StockSymbol])
async def get_popular_stocks() -> list[StockSymbol]:
    """인기 주식 목록 조회.

    Returns:
        list[StockSymbol]: 기본 정보가 포함된 인기 주식 심볼 목록
    """
    return await stock_service.get_popular_stocks()
