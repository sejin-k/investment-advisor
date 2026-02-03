"""PostgreSQL과 psycopg3를 직접 사용한 데이터베이스 연결 설정.

이 모듈은 현재 주석 처리되어 있으며, 데이터베이스 통합이 준비되면 활성화될 예정입니다.
"""

# TODO: 데이터베이스 준비 시 주석 해제
#
# from collections.abc import AsyncGenerator
# from typing import Any
#
# import psycopg
# from psycopg import AsyncConnection
# from psycopg.rows import dict_row
# from psycopg_pool import AsyncConnectionPool
#
# from app.core.config import settings
# from app.core.logging import get_logger
#
# logger = get_logger(__name__)
#
# # 전역 연결 풀
# pool: AsyncConnectionPool | None = None
#
#
# async def init_db() -> None:
#     """데이터베이스 연결 풀 초기화.
#
#     애플리케이션 시작 시 호출되어 연결 풀을 생성합니다.
#     """
#     global pool
#
#     if pool is not None:
#         logger.warning("데이터베이스 연결 풀이 이미 초기화되어 있습니다")
#         return
#
#     try:
#         pool = AsyncConnectionPool(
#             conninfo=settings.DATABASE_URL,
#             min_size=5,  # 최소 연결 수
#             max_size=20,  # 최대 연결 수
#             timeout=30.0,  # 연결 대기 시간 (초)
#             max_idle=300.0,  # 유휴 연결 최대 시간 (초)
#             max_lifetime=3600.0,  # 연결 최대 수명 (초, 1시간)
#         )
#         await pool.open()
#         logger.info("데이터베이스 연결 풀 초기화 완료")
#
#         # 연결 테스트
#         async with pool.connection() as conn:
#             async with conn.cursor() as cur:
#                 await cur.execute("SELECT version()")
#                 version = await cur.fetchone()
#                 logger.info(f"PostgreSQL 버전: {version[0] if version else 'Unknown'}")
#
#     except Exception as e:
#         logger.error(f"데이터베이스 연결 풀 초기화 실패: {e}")
#         raise
#
#
# async def close_db() -> None:
#     """데이터베이스 연결 풀 종료.
#
#     애플리케이션 종료 시 호출되어 모든 연결을 정리합니다.
#     """
#     global pool
#
#     if pool is None:
#         logger.warning("종료할 데이터베이스 연결 풀이 없습니다")
#         return
#
#     try:
#         await pool.close()
#         pool = None
#         logger.info("데이터베이스 연결 풀 종료 완료")
#     except Exception as e:
#         logger.error(f"데이터베이스 연결 풀 종료 실패: {e}")
#         raise
#
#
# async def get_db() -> AsyncGenerator[AsyncConnection[dict[str, Any]], None]:
#     """데이터베이스 연결을 가져오는 의존성 함수.
#
#     FastAPI 엔드포인트에서 Depends()와 함께 사용됩니다.
#
#     Example:
#         @router.get("/users")
#         async def get_users(conn: AsyncConnection = Depends(get_db)):
#             async with conn.cursor() as cur:
#                 await cur.execute("SELECT * FROM users")
#                 return await cur.fetchall()
#
#     Yields:
#         AsyncConnection: 딕셔너리 row 형식의 데이터베이스 연결
#
#     Raises:
#         RuntimeError: 연결 풀이 초기화되지 않은 경우
#     """
#     if pool is None:
#         raise RuntimeError("데이터베이스 연결 풀이 초기화되지 않았습니다")
#
#     async with pool.connection() as conn:
#         # 딕셔너리 형식으로 결과 반환하도록 설정
#         conn.row_factory = dict_row
#         try:
#             yield conn
#             # 명시적 커밋은 필요 시 서비스 레이어에서 수행
#         except Exception:
#             # 에러 발생 시 롤백
#             await conn.rollback()
#             raise
#
#
# async def check_db_connection() -> bool:
#     """데이터베이스 연결 상태를 확인.
#
#     헬스 체크 엔드포인트에서 사용됩니다.
#
#     Returns:
#         bool: 데이터베이스 연결 가능 시 True, 그렇지 않으면 False
#     """
#     if pool is None:
#         logger.error("데이터베이스 연결 풀이 초기화되지 않았습니다")
#         return False
#
#     try:
#         async with pool.connection() as conn:
#             async with conn.cursor() as cur:
#                 await cur.execute("SELECT 1")
#                 result = await cur.fetchone()
#                 return result is not None
#     except Exception as e:
#         logger.error(f"데이터베이스 연결 확인 실패: {e}")
#         return False
#
#
# async def execute_query(
#     query: str,
#     params: tuple[Any, ...] | dict[str, Any] | None = None,
#     fetch_one: bool = False,
#     fetch_all: bool = True,
# ) -> Any:
#     """Raw SQL 쿼리를 실행하는 헬퍼 함수.
#
#     Args:
#         query: 실행할 SQL 쿼리
#         params: 쿼리 파라미터 (tuple 또는 dict)
#         fetch_one: 단일 행만 가져올지 여부
#         fetch_all: 모든 행을 가져올지 여부
#
#     Returns:
#         Any: 쿼리 결과 (fetch_one이면 단일 행, fetch_all이면 행 목록)
#
#     Raises:
#         RuntimeError: 연결 풀이 초기화되지 않은 경우
#
#     Example:
#         # 단일 행 조회
#         user = await execute_query(
#             "SELECT * FROM users WHERE id = %s",
#             (user_id,),
#             fetch_one=True
#         )
#
#         # 여러 행 조회
#         users = await execute_query(
#             "SELECT * FROM users WHERE age > %(min_age)s",
#             {"min_age": 18},
#             fetch_all=True
#         )
#
#         # INSERT/UPDATE/DELETE
#         await execute_query(
#             "INSERT INTO users (name, email) VALUES (%s, %s)",
#             ("John", "john@example.com"),
#             fetch_all=False
#         )
#     """
#     if pool is None:
#         raise RuntimeError("데이터베이스 연결 풀이 초기화되지 않았습니다")
#
#     async with pool.connection() as conn:
#         conn.row_factory = dict_row
#         async with conn.cursor() as cur:
#             await cur.execute(query, params)
#
#             if fetch_one:
#                 return await cur.fetchone()
#             elif fetch_all:
#                 return await cur.fetchall()
#             else:
#                 # INSERT/UPDATE/DELETE의 경우 영향받은 행 수 반환
#                 return cur.rowcount
