"""구조화된 로깅을 위한 로깅 설정."""

import logging
import sys
from typing import Any

from app.core.config import settings


class StructuredFormatter(logging.Formatter):
    """구조화된 로깅 출력을 위한 커스텀 포매터."""

    def format(self, record: logging.LogRecord) -> str:
        """구조화된 정보로 로그 레코드 포맷.

        Args:
            record: 로그 레코드

        Returns:
            str: 포맷된 로그 메시지
        """
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # 예외 정보가 있으면 추가
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # 추가 필드 추가
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        # 쉬운 파싱을 위해 key=value 형식으로 포맷
        formatted_parts = [f'{key}="{value}"' for key, value in log_data.items()]
        return " ".join(formatted_parts)


def setup_logging() -> None:
    """stdout으로 구조화된 출력을 하도록 애플리케이션 로깅 설정."""
    # 설정에서 로그 레벨 가져오기
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # stdout용 핸들러 생성
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # 구조화된 포매터 설정
    formatter = StructuredFormatter(
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # 서드파티 라이브러리의 노이즈 줄이기
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)

    # 시작 메시지 로그
    logger = logging.getLogger(__name__)
    logger.info(
        f"로깅 설정 완료: level={settings.LOG_LEVEL} environment={settings.ENVIRONMENT}"
    )


def get_logger(name: str) -> logging.Logger:
    """주어진 이름으로 로거 인스턴스 가져오기.

    Args:
        name: 로거 이름 (일반적으로 __name__)

    Returns:
        Logger: 로거 인스턴스
    """
    return logging.getLogger(name)
