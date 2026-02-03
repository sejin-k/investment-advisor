"""FastAPI 애플리케이션 진입점."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging

# 로깅 초기화
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """애플리케이션 시작 및 종료 이벤트를 관리하는 lifespan 컨텍스트 매니저.

    Args:
        app: FastAPI 애플리케이션 인스턴스

    Yields:
        None
    """
    # 시작
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    # TODO: 데이터베이스 준비 시 주석 해제
    # from app.core.database import init_db
    # logger.info("데이터베이스 초기화 중...")
    # await init_db()
    # logger.info("데이터베이스 초기화 완료")

    yield

    # 종료
    logger.info("애플리케이션 종료 중...")

    # TODO: 데이터베이스 준비 시 주석 해제
    # from app.core.database import close_db
    # logger.info("데이터베이스 연결 종료 중...")
    # await close_db()
    # logger.info("데이터베이스 연결 종료 완료")

    logger.info("애플리케이션 종료 완료")


# FastAPI 애플리케이션 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI 기반 주식 투자 어드바이저 API",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# 전역 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """처리되지 않은 모든 예외를 전역으로 처리.

    Args:
        request: 예외를 발생시킨 요청
        exc: 발생한 예외

    Returns:
        JSONResponse: 에러 상세 정보
    """
    logger.error(f"처리되지 않은 예외: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "내부 서버 오류",
            "type": "internal_error",
        },
    )


# API 라우터 포함
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root() -> dict[str, str]:
    """API 버전 정보를 반환하는 루트 엔드포인트.

    Returns:
        dict: API 이름 및 버전
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
    )
