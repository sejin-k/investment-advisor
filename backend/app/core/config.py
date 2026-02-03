"""pydantic-settings를 사용한 애플리케이션 설정."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """환경 변수에서 로드되는 애플리케이션 설정."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # 애플리케이션
    APP_NAME: str = "Investment Advisor API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = Field(default=False)

    # API
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"]
    )
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = Field(default=["*"])
    CORS_ALLOW_HEADERS: list[str] = Field(default=["*"])

    # 데이터베이스
    # TODO: 데이터베이스 준비 시 주석 해제
    # 형식: postgresql://user:password@host:port/database
    # 예시: postgresql://postgres:postgres@localhost:5432/stock_advisor
    DATABASE_URL: str = Field(
        default="",
        description="PostgreSQL 연결 URL (psycopg3 형식). 데이터베이스 설정 전까지 비워둡니다."
    )

    # PostgreSQL (docker-compose용)
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "investment_advisor"

    # 로깅
    LOG_LEVEL: str = "INFO"

    # 보안
    SECRET_KEY: str = Field(
        default="change-in-production-use-strong-secret-key",
        description="JWT 토큰 생성을 위한 비밀 키"
    )

    # 외부 API
    OPENAI_API_KEY: str = Field(default="", description="AI 기능을 위한 OpenAI API 키")

    @property
    def is_development(self) -> bool:
        """개발 모드 실행 여부 확인."""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """프로덕션 모드 실행 여부 확인."""
        return self.ENVIRONMENT == "production"


settings = Settings()
