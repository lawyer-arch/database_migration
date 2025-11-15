from sqlalchemy.engine.reflection import Inspector

def get_mysql_schema(sync_engine):
    inspector = Inspector.from_engine(sync_engine)

    tables = []
    for table_name in inspector.get_table_names():
        columns = [
            {"name": col["name"], "type": str(col["type"]), "nullable": col["nullable"]}
            for col in inspector.get_columns(table_name)
        ]
        pk = inspector.get_pk_constraint(table_name)["constrained_columns"]
        fk = inspector.get_foreign_keys(table_name)
        indexes = inspector.get_indexes(table_name)
        unique = inspector.get_unique_constraints(table_name)

        tables.append({
            "table": table_name,
            "columns": columns,
            "primary_key": pk,
            "foreign_keys": fk,
            "indexes": indexes,
            "unique_constraints": unique
        })

    return tables

