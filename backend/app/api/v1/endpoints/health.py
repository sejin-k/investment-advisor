"""애플리케이션 모니터링을 위한 헬스 체크 엔드포인트."""

from fastapi import APIRouter

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.health import (
    HealthResponse,
    HealthStatus,
    LivenessResponse,
    ReadinessResponse,
)

router = APIRouter(tags=["health"])
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """메인 헬스 체크 엔드포인트.

    데이터베이스 연결을 포함한 애플리케이션의 전반적인 상태를 반환합니다.

    Returns:
        HealthResponse: 상태 정보
    """
    # TODO: 데이터베이스 준비 시 주석 해제
    # from app.core.database import check_db_connection
    # db_healthy = await check_db_connection()

    # 플레이스홀더: 데이터베이스 설정 전까지 정상으로 가정
    db_healthy = True

    # 전반적인 상태 판단
    if db_healthy:
        status = HealthStatus.HEALTHY
    else:
        status = HealthStatus.DEGRADED

    return HealthResponse(
        status=status,
        version=settings.APP_VERSION,
        database=db_healthy,
        environment=settings.ENVIRONMENT,
    )


@router.get("/health/ready", response_model=ReadinessResponse)
async def readiness_check() -> ReadinessResponse:
    """Kubernetes 준비 상태 프로브 엔드포인트.

    애플리케이션이 트래픽을 받을 준비가 되었는지 확인합니다.
    준비되면 200, 그렇지 않으면 503을 반환합니다.

    Returns:
        ReadinessResponse: 준비 상태
    """
    # TODO: 데이터베이스 준비 시 주석 해제
    # from app.core.database import check_db_connection
    # db_ready = await check_db_connection()

    # 플레이스홀더: 데이터베이스 설정 전까지 준비 완료로 가정
    db_ready = True

    details = {
        "database": db_ready,
    }

    ready = all(details.values())

    return ReadinessResponse(
        ready=ready,
        details=details,
    )


@router.get("/health/live", response_model=LivenessResponse)
async def liveness_check() -> LivenessResponse:
    """Kubernetes 활성 상태 프로브 엔드포인트.

    애플리케이션이 살아있으며 재시작할 필요가 없는지 확인합니다.
    애플리케이션이 교착 상태가 아니면 항상 200을 반환해야 합니다.

    Returns:
        LivenessResponse: 활성 상태
    """
    return LivenessResponse(alive=True)
