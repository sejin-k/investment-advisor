# Investment Advisor Backend

FastAPI, PostgreSQL, LangChain을 사용한 AI 기반 주식 투자 어드바이저 API

## 주요 기능

- **FastAPI**: 현대적이고 고성능 Python 웹 프레임워크
- **비동기/Await**: 완전한 비동기 데이터베이스 및 API 작업
- **PostgreSQL**: psycopg3를 직접 사용한 Raw SQL 방식
- **타입 안정성**: Pydantic을 사용한 포괄적인 타입 힌트 및 검증
- **Docker**: 컨테이너화된 개발 및 프로덕션 환경
- **테스트**: pytest를 사용한 포괄적인 테스트 스위트
- **코드 품질**: 일관된 코드 스타일을 위한 Black, isort, mypy

## 프로젝트 구조

```
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py          # 의존성 주입
│   │   └── v1/
│   │       ├── endpoints/           # API 엔드포인트
│   │       │   ├── health.py        # 헬스 체크 엔드포인트
│   │       │   └── stocks.py        # 주식 엔드포인트
│   │       └── router.py            # API 라우터
│   ├── core/
│   │   ├── config.py                # 애플리케이션 설정
│   │   ├── database.py              # psycopg3 연결 풀 (주석처리)
│   │   └── logging.py               # 로깅 설정
│   ├── models/                      # 데이터베이스 테이블 정의 (향후)
│   ├── repositories/                # Raw SQL 리포지토리 (향후)
│   ├── schemas/                     # Pydantic 모델
│   │   ├── health.py                # 헬스 체크 스키마
│   │   └── stock.py                 # 주식 스키마
│   ├── services/                    # 비즈니스 로직
│   │   └── stock_service.py         # 모의 데이터를 사용하는 주식 서비스
│   ├── utils/                       # 유틸리티 함수
│   └── main.py                      # 애플리케이션 진입점
├── tests/
│   ├── conftest.py                  # 테스트 설정
│   ├── test_health.py               # 헬스 엔드포인트 테스트
│   └── test_stocks.py               # 주식 엔드포인트 테스트
├── Dockerfile                       # 프로덕션 Docker 이미지
├── pyproject.toml                   # 프로젝트 설정 및 의존성
└── .env.example                     # 환경 변수 템플릿
```

## 빠른 시작

### 개발 환경 (Local)

1. **사전 요구사항**
   - Python 3.12+
   - uv (권장) 또는 pip

2. **uv 설치** (권장)
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **의존성 설치**
   ```bash
   cd backend

   # uv 사용 (권장)
   uv sync --extra dev

   # 또는 pip 사용
   pip install -e ".[dev]"
   ```

4. **환경 설정**
   ```bash
   cp .env.example .env
   # .env 파일을 편집하여 설정 변경
   ```

5. **애플리케이션 실행**
   ```bash
   # uv 사용 (권장)
   uv run uvicorn app.main:app --reload

   # 또는 pip 사용시
   uvicorn app.main:app --reload
   ```

6. **API 접속**
   - API: http://localhost:8000
   - 인터랙티브 문서: http://localhost:8000/api/v1/docs
   - ReDoc: http://localhost:8000/api/v1/redoc

### Docker Production 실행

1. **서비스 시작**
   ```bash
   # 프로젝트 루트에서
   docker-compose --profile prod up
   ```

2. **로그 확인**
   ```bash
   docker-compose logs -f investment-advisor-backend
   ```

4. **서비스 중지**
   ```bash
   docker-compose down
   ```

## API 엔드포인트

### 헬스 체크

- `GET /api/v1/health` - 전체 상태 확인
- `GET /api/v1/health/ready` - 준비 상태 프로브 (Kubernetes)
- `GET /api/v1/health/live` - 활성 상태 프로브 (Kubernetes)

### 주식 (모의 데이터)

- `GET /api/v1/stocks/info/{symbol}` - 상세 주식 정보 조회
- `GET /api/v1/stocks/popular` - 인기 주식 목록 조회

## 개발

### 코드 포매팅 및 린팅

```bash
# ruff로 코드 포맷 (black + isort 대체)
ruff format app tests

# ruff로 린팅
ruff check app tests

# ruff로 린팅 문제 자동 수정
ruff check --fix app tests
```

### 타입 체크

```bash
# mypy로 타입 체크
mypy app
```

### 테스트

```bash
# 모든 테스트 실행
pytest

# 커버리지와 함께 실행
pytest --cov=app tests/

# 특정 테스트 파일 실행
pytest tests/test_health.py

# 자세한 출력으로 실행
pytest -v
```

### 코드 품질 (한번에)

```bash
# 포맷, 린팅, 타입 체크, 테스트
ruff format app tests && ruff check --fix app tests && mypy app && pytest
```

## 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `ENVIRONMENT` | 애플리케이션 환경 | `development` |
| `DATABASE_URL` | PostgreSQL 연결 URL | (비어있음) |
| `POSTGRES_USER` | PostgreSQL 사용자명 | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL 비밀번호 | `postgres` |
| `POSTGRES_DB` | PostgreSQL 데이터베이스명 | `Investment_advisor` |
| `OPENAI_API_KEY` | OpenAI API 키 | (비어있음) |
| `SECRET_KEY` | JWT용 비밀 키 | `change-in-production` |
| `LOG_LEVEL` | 로깅 레벨 | `INFO` |

## 데이터베이스 통합 (향후)

데이터베이스 연결 코드는 현재 다음 파일에서 주석 처리되어 있습니다:
- `app/core/database.py` - psycopg3 연결 풀 설정
- `app/main.py` (lifespan 함수)
- `app/api/v1/endpoints/health.py`

데이터베이스 통합을 활성화하려면:

1. `.env` 파일에 `DATABASE_URL` 설정 (형식: `postgresql://user:password@host:port/database`)
2. 위 파일들에서 데이터베이스 코드 주석 해제
3. SQL 마이그레이션 스크립트 작성 (CREATE TABLE 등)
4. `app/repositories/`에 테이블별 리포지토리 구현 (Raw SQL 사용)

## 기술 스택

### 프로덕션
- **FastAPI**: 웹 프레임워크
- **Uvicorn**: ASGI 서버
- **psycopg3**: PostgreSQL 비동기 드라이버 (Raw SQL 직접 사용)
- **psycopg-pool**: 비동기 연결 풀 관리
- **Pydantic**: 데이터 검증
- **LangChain**: AI 에이전트 프레임워크
- **OpenAI**: LLM 통합

### 개발 도구
- **uv**: 빠른 Python 패키지 관리자 (10-100배 빠른 pip 대체)
- **ruff**: 빠른 린터 및 포매터 (black + isort + flake8 대체)
- **mypy**: 정적 타입 체커
- **pytest**: 테스트 프레임워크

## 다음 단계

### 즉시 가능한 개선사항

1. **데이터베이스 통합**
   - 데이터베이스 코드 주석 해제
   - SQL 마이그레이션 스크립트 작성
   - 테이블 생성 및 리포지토리 구현

2. **인증**
   - JWT 토큰 인증
   - 사용자 관리
   - 보호된 엔드포인트

3. **AI 에이전트 통합**
   - LangChain 에이전트 설정
   - OpenAI GPT 통합
   - 투자 조언 엔드포인트

### 향후 기능

- 실시간 주식 업데이트를 위한 WebSocket 지원
- 속도 제한 (Rate limiting)
- 캐싱 (Redis)
- 백그라운드 작업 (Celery)
- API 버저닝 전략
- 포괄적인 로깅 및 모니터링

## 기여

1. 코드 포맷 및 린팅: `ruff format app tests && ruff check --fix app tests`
2. 타입 체크: `mypy app`
3. 테스트 실행: `pytest --cov=app`
4. 커밋 전에 모든 체크가 통과하는지 확인

## uv 주요 명령어

```bash
# 가상환경 생성
uv venv

# 패키지 설치(의존성 반영) - 권장
uv add <package> --optional dev  # develop 환경에만 적용
uv add <package>                 # production에 적용

# 패키지 추가(의존성 반영 X) - 권장되지 않음
uv pip install <package-name>

# 의존성 설치
uv pip install -e ".[dev]"

# 의존성 동기화 (pyproject.toml 기반)
uv pip sync --extra dev # develop 환경 동기화
uv pip sync             # production 환경 동기화
```

## 라이선스

[라이선스를 여기에 추가]
