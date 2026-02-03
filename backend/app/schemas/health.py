"""헬스 체크 응답 스키마."""

from enum import Enum

from pydantic import BaseModel, Field


class HealthStatus(str, Enum):
    """헬스 체크 상태 값."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class HealthResponse(BaseModel):
    """헬스 체크 엔드포인트 응답 모델."""

    status: HealthStatus = Field(
        description="애플리케이션의 전반적인 상태"
    )
    version: str = Field(
        description="애플리케이션 버전"
    )
    database: bool = Field(
        default=True,
        description="데이터베이스 연결 상태"
    )
    environment: str = Field(
        description="현재 환경 (development, staging, production)"
    )


class ReadinessResponse(BaseModel):
    """준비 상태 프로브 응답 모델."""

    ready: bool = Field(
        description="애플리케이션이 요청을 받을 준비가 되었는지 여부"
    )
    details: dict[str, bool] = Field(
        default_factory=dict,
        description="개별 구성 요소의 상세 준비 상태"
    )


class LivenessResponse(BaseModel):
    """활성 상태 프로브 응답 모델."""

    alive: bool = Field(
        description="애플리케이션이 살아있는지 여부"
    )
