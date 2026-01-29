# Investment-advisor

## 프로젝트 목표
투자(주식 or 코인)를 도와주는 AI Agent 개발


## 프로젝트 스펙

- **Frontend**: Next.js 14 (React, TypeScript)
- **Backend**: FastAPI (Python 3.12)
- **Database**: PostgreSQL (psycopg3 직접 사용)
- **AI/ML**: LangChain, OpenAI
- **Containerization**: Docker, Docker Compose

## 📚 문서

- [개발 일지](./DEVLOG.md) - 일자별 개발 진행 사항
- [Backend README](./backend/README.md) - 백엔드 상세 문서

## 🚀 빠른 시작

### **사전 요구사항**
- Python 3.12+
- uv (권장) 또는 pip

### Backend 실행

Docker 실행 (권장)
```bash
# Docker로 실행 (권장)
docker-compose --profile prod up
```

로컬 실행

```bash
# 로컬 실행
cd backend

# 환경변수 편집
cp .env.example .env
# .env 파일을 편집하여 설정 변경

# uv 사용 (권장)
uv sync
# 또는 pip 사용
pip install -e .

# uv 사용 (권장)
uv run uvicorn app.main:app
# 또는 pip 사용
uvicorn app.main:app
```

접속:
- API: http://localhost:8000
- API 문서: http://localhost:8000/api/v1/docs

## 📁 프로젝트 구조

```
stock/
├── backend/         # FastAPI 백엔드
├── frontend/        # Next.js 프론트엔드 (예정)
├── DEVLOG.md        # 개발 일지
└── README.md        # 이 파일
```

## 🔄 개발 현황

- ✅ **2026-01-22**: FastAPI 백엔드 초기 설정 완료
  - Production-ready 프로젝트 구조
  - psycopg3 직접 사용 (Raw SQL)
  - Docker 개발/프로덕션 환경
  - Health Check & Stocks API (모의 데이터)
  - 전체 한글 문서화

- 🔜 **다음 단계**:
  - PostgreSQL 연동
  - 실제 주식 API 통합
  - Frontend 개발
  - AI Agent 구현
