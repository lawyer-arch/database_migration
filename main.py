import asyncio
from migrator.db_connectors import AsyncDBConnector
from migrator.schema_reader import SchemaReader
from migrator.schema_transformer import SchemaTransformer
from migrator.schema_writer import SchemaWriter
from migrator.data_migrator import DataMigrator
from db_waiter import wait_databases

async def full_migration():
    mysql_connector = AsyncDBConnector()
    pg_connector = AsyncDBConnector()

    await mysql_connector.connect_to_mysql()
    await pg_connector.connect_to_postgres()

    reader = SchemaReader()
    schema = await reader.fetch_schema()
    print("Схема MySQL:", schema)

    transformer = SchemaTransformer()
    transformed_schema = transformer.transform_schema(schema)

    writer = SchemaWriter(transformed_schema, pg_connector)
    await writer.write_schema()

    migrator = DataMigrator(mysql_connector, pg_connector)
    await migrator.migrate_data(transformed_schema)

    await mysql_connector.close_connections()
    await pg_connector.close_connections()

async def main():
    print("Ожидание готовности БД...")
    await wait_databases()
    print("Базы данных готовы! Запускаем мигратор...")
    await full_migration()

if __name__ == "__main__":
    asyncio.run(main())


