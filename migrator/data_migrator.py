from sqlalchemy import text
from tqdm import tqdm

BATCH_SIZE = 500

class DataMigrator:
    def __init__(self, mysql_connector, pg_connector):
        self.mysql_connector = mysql_connector
        self.pg_connector = pg_connector

    async def migrate_data(self, schema: list):
        mysql_session = self.mysql_connector.get_mysql_session()
        pg_session = self.pg_connector.get_postgres_session()

        for table_data in schema:
            table_name = table_data["table"]
            columns = [c["name"] for c in table_data["columns"]]
            col_str = ", ".join(columns)

            result = await mysql_session.execute(text(f"SELECT {col_str} FROM {table_name}"))
            rows = result.fetchall()
            if not rows:
                continue

            insert_sql = f"INSERT INTO {table_name} ({col_str}) VALUES ({', '.join(':'+c for c in columns)})"

            # Батчи
            for i in range(0, len(rows), BATCH_SIZE):
                chunk = rows[i:i+BATCH_SIZE]
                await pg_session.execute(
                    text(insert_sql),
                    [dict(r._mapping) for r in chunk]
                )
                print(f"{table_name}: migrated {i + len(chunk)} rows")

        await mysql_session.commit()
        await pg_session.commit()
