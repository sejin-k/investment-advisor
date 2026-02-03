"""주식 관련 응답 스키마."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class StockSymbol(BaseModel):
    """기본 주식 심볼 정보."""

    symbol: str = Field(
        description="주식 티커 심볼 (예: AAPL, GOOGL)",
        examples=["AAPL"]
    )
    name: str = Field(
        description="회사명",
        examples=["Apple Inc."]
    )
    exchange: str = Field(
        description="거래소 (예: NASDAQ, NYSE)",
        examples=["NASDAQ"]
    )


class StockInfo(BaseModel):
    """상세 주식 정보."""

    symbol: str = Field(
        description="주식 티커 심볼",
        examples=["AAPL"]
    )
    name: str = Field(
        description="회사명",
        examples=["Apple Inc."]
    )
    exchange: str = Field(
        description="거래소",
        examples=["NASDAQ"]
    )
    current_price: Decimal = Field(
        description="현재 주가 (USD)",
        examples=[150.25]
    )
    previous_close: Decimal = Field(
        description="전일 종가",
        examples=[148.50]
    )
    change: Decimal = Field(
        description="가격 변동액",
        examples=[1.75]
    )
    change_percent: Decimal = Field(
        description="가격 변동률 (%)",
        examples=[1.18]
    )
    volume: int = Field(
        description="거래량",
        examples=[50000000]
    )
    market_cap: Optional[int] = Field(
        default=None,
        description="시가총액 (USD)",
        examples=[2500000000000]
    )
    last_updated: datetime = Field(
        description="마지막 업데이트 시간"
    )

    class Config:
        """Pydantic 모델 설정."""
        json_encoders = {
            Decimal: lambda v: float(v),
        }
