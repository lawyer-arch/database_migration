from sqlalchemy import MetaData, Table, Column, PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint, Index
from sqlalchemy.types import Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB

class SchemaWriter:
    def __init__(self, schema: list, connector):
        self.schema = schema
        self.connector = connector

    def get_column_type(self, type_str: str):
        types_map = {
            "INTEGER": Integer(),
            "SMALLINT": Integer(),
            "BIGSERIAL": Integer(),
            "VARCHAR": String(),
            "TEXT": String(),
            "UUID": UUID(as_uuid=True),
            "ARRAY": ARRAY(String()),
            "JSONB": JSONB(),
            "BOOLEAN": Boolean(),
            "TIMESTAMP": DateTime(timezone=True),
            "NUMERIC": Numeric(scale=2)
        }
        return types_map.get(type_str.upper(), String())

    async def write_schema(self):
        engine = self.connector.postgres_engine
        meta = MetaData()

        for table_data in self.schema:
            cols = [
                Column(c["name"], self.get_column_type(c["type"]), nullable=c["nullable"])
                for c in table_data["columns"]
            ]
            pk = PrimaryKeyConstraint(*table_data["primary_key"]) if table_data["primary_key"] else None
            fks = [ForeignKeyConstraint(fk["local_columns"],
                                        [f"{fk['referenced_table']}.{c}" for c in fk["remote_columns"]])
                   for fk in table_data["foreign_keys"]]
            uniques = [UniqueConstraint(*uc["column_names"]) for uc in table_data["unique_constraints"]]
            indexes = [Index(idx["name"], *idx["column_names"], unique=idx["unique"]) for idx in table_data["indexes"]]

            Table(table_data["table"], meta, *(cols + ([pk] if pk else []) + fks + uniques + indexes))

        async with engine.begin() as conn:
            await conn.run_sync(meta.create_all)
