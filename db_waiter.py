from urllib.parse import urlparse
import asyncio
import aiomysql
import asyncpg

from migrator.config import MYSQL_URL, POSTGRES_URL


def parse_async_url(url: str):
    """
    Убираем +aiomysql / +asyncpg из схемы, чтобы urlparse корректно разбирал URL.
    """
    url = url.replace("+aiomysql", "").replace("+asyncpg", "")
    return urlparse(url)


async def wait_mysql(url: str, timeout: int = 30):
    parsed = parse_async_url(url)
    host, port = parsed.hostname, parsed.port or 3306
    user, password = parsed.username, parsed.password
    db = parsed.path.lstrip("/")

    start = asyncio.get_event_loop().time()
    while True:
        try:
            conn = await aiomysql.connect(
                host=host, port=port, user=user, password=password, db=db
            )
            conn.close()
            return
        except Exception:
            if asyncio.get_event_loop().time() - start > timeout:
                raise TimeoutError(f"MySQL {host}:{port} not ready after {timeout}s")
            await asyncio.sleep(1)


async def wait_postgres(url: str, timeout: int = 30):
    parsed = parse_async_url(url)
    host, port = parsed.hostname, parsed.port or 5432
    user, password = parsed.username, parsed.password
    db = parsed.path.lstrip("/")

    start = asyncio.get_event_loop().time()
    while True:
        try:
            conn = await asyncpg.connect(
                host=host, port=port, user=user, password=password, database=db
            )
            await conn.close()
            return
        except Exception:
            if asyncio.get_event_loop().time() - start > timeout:
                raise TimeoutError(f"Postgres {host}:{port} not ready after {timeout}s")
            await asyncio.sleep(1)


async def wait_databases():
    await asyncio.gather(
        wait_mysql(MYSQL_URL),
        wait_postgres(POSTGRES_URL),
    )
