"""외부 API 없이 테스트용 모의 데이터를 사용하는 주식 서비스."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from app.core.logging import get_logger
from app.schemas.stock import StockInfo, StockSymbol

logger = get_logger(__name__)

# 개발용 모의 주식 데이터
MOCK_STOCKS = {
    "AAPL": {
        "name": "Apple Inc.",
        "exchange": "NASDAQ",
        "current_price": Decimal("150.25"),
        "previous_close": Decimal("148.50"),
        "volume": 50000000,
        "market_cap": 2500000000000,
    },
    "GOOGL": {
        "name": "Alphabet Inc.",
        "exchange": "NASDAQ",
        "current_price": Decimal("140.75"),
        "previous_close": Decimal("139.20"),
        "volume": 25000000,
        "market_cap": 1800000000000,
    },
    "MSFT": {
        "name": "Microsoft Corporation",
        "exchange": "NASDAQ",
        "current_price": Decimal("380.50"),
        "previous_close": Decimal("375.80"),
        "volume": 30000000,
        "market_cap": 2800000000000,
    },
    "TSLA": {
        "name": "Tesla, Inc.",
        "exchange": "NASDAQ",
        "current_price": Decimal("245.30"),
        "previous_close": Decimal("248.10"),
        "volume": 120000000,
        "market_cap": 780000000000,
    },
    "AMZN": {
        "name": "Amazon.com Inc.",
        "exchange": "NASDAQ",
        "current_price": Decimal("175.80"),
        "previous_close": Decimal("173.50"),
        "volume": 45000000,
        "market_cap": 1800000000000,
    },
}


class StockService:
    """모의 데이터를 사용하는 주식 데이터 작업 서비스."""

    async def get_stock_info(self, symbol: str) -> Optional[StockInfo]:
        """특정 주식의 상세 정보 조회.

        Args:
            symbol: 주식 티커 심볼 (예: AAPL)

        Returns:
            StockInfo: 주식 정보 (찾을 수 없으면 None)
        """
        symbol = symbol.upper()
        logger.info(f"주식 정보 조회: {symbol}")

        stock_data = MOCK_STOCKS.get(symbol)
        if not stock_data:
            logger.warning(f"주식 심볼을 찾을 수 없음: {symbol}")
            return None

        # 변동액 및 변동률 계산
        change = stock_data["current_price"] - stock_data["previous_close"]
        change_percent = (change / stock_data["previous_close"]) * 100

        return StockInfo(
            symbol=symbol,
            name=stock_data["name"],
            exchange=stock_data["exchange"],
            current_price=stock_data["current_price"],
            previous_close=stock_data["previous_close"],
            change=change,
            change_percent=change_percent,
            volume=stock_data["volume"],
            market_cap=stock_data.get("market_cap"),
            last_updated=datetime.now(timezone.utc),
        )

    async def get_popular_stocks(self) -> list[StockSymbol]:
        """인기 주식 목록 조회.

        Returns:
            list[StockSymbol]: 인기 주식 심볼 목록
        """
        logger.info("인기 주식 목록 조회")

        popular_stocks = [
            StockSymbol(
                symbol=symbol,
                name=data["name"],
                exchange=data["exchange"],
            )
            for symbol, data in MOCK_STOCKS.items()
        ]

        return popular_stocks


# 싱글톤 인스턴스
stock_service = StockService()
