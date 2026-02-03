"""의존성 주입을 위한 API 의존성.

이 모듈은 엔드포인트 함수에 주입할 수 있는 의존성을 포함합니다.
현재는 비어있지만 다음과 같은 용도로 사용될 예정입니다:
- 데이터베이스 세션 주입
- 인증/인가
- 속도 제한
- 등
"""

# TODO: 필요에 따라 의존성 추가
# 예시:
# from fastapi import Depends
# from app.core.database import get_db
# from sqlalchemy.ext.asyncio import AsyncSession
#
# async def get_current_user(db: AsyncSession = Depends(get_db)) -> User:
#     # 인증 로직
#     pass
