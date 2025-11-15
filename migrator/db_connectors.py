from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import MYSQL_URL, POSTGRES_URL

class AsyncDBConnector:
    def __init__(self):
        self.mysql_engine = None
        self.postgres_engine = None
        self.mysql_session = None
        self.postgres_session = None

    async def connect_to_mysql(self):
        self.mysql_engine = create_async_engine(MYSQL_URL, future=True, echo=True)
        self.mysql_session = sessionmaker(
            bind=self.mysql_engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def connect_to_postgres(self):
        self.postgres_engine = create_async_engine(POSTGRES_URL, future=True, echo=True)
        self.postgres_session = sessionmaker(
            bind=self.postgres_engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    def get_mysql_session(self):
        if not self.mysql_session:
            raise ValueError("MySQL соединение не установлено!")
        return self.mysql_session()

    def get_postgres_session(self):
        if not self.postgres_session:
            raise ValueError("Postgres соединение не установлено!")
        return self.postgres_session()

    async def close_connections(self):
        if self.mysql_engine:
            await self.mysql_engine.dispose()
        if self.postgres_engine:
            await self.postgres_engine.dispose()

