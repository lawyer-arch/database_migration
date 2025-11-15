from typing import List, Dict, Any
from .utils import get_mysql_schema  
from .db_connectors import AsyncDBConnector


class SchemaReader:
    async def fetch_schema(self) -> List[Dict]:
        """
        Возвращает полный список таблиц и их колонок в базе данных MySQL.
        """
        connector = AsyncDBConnector()
        await connector.connect_to_mysql()
        session = connector.get_mysql_session()

        # Получаем синхронный движок через биндинг асинхронной сессии
        engine = session.bind.sync_engine

        # Передаем синхронный движок в синхронную функцию
        schema = await session.run_sync(lambda sync_sess: get_mysql_schema(engine))
        return schema
