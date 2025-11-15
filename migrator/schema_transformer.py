from typing import List, Dict, Any
from pprint import pformat

class SchemaTransformer:
    def transform_type(self, type_str: str) -> str:
        """
        Трансформирует типы данных MySQL в эквиваленты PostgreSQL.
        """
        mapping = {
            "TINYINT": "SMALLINT",
            "SMALLINT": "SMALLINT",
            "MEDIUMINT": "INTEGER",
            "INT": "INTEGER",
            "BIGINT": "BIGSERIAL",
            "FLOAT": "REAL",
            "DOUBLE": "DOUBLE PRECISION",
            "DECIMAL": "NUMERIC",
            "CHAR": "CHARACTER",
            "VARCHAR": "VARCHAR",
            "TEXT": "TEXT",
            "LONGTEXT": "TEXT",
            "DATE": "DATE",
            "DATETIME": "TIMESTAMP",
            "TIME": "TIME",
            "BOOLEAN": "BOOLEAN",
            "ENUM": "VARCHAR",
            "JSON": "JSONB"
        }
        transformed_type = mapping.get(type_str.upper(), type_str)
        return transformed_type

    def transform_schema(self, raw_schema: List[Dict]) -> List[Dict]:
        """
        Трансформируем всю схему MySQL в формат PostgreSQL.
        """
        transformed_schema = []
        for table in raw_schema:
            new_table = {}
            new_table["table"] = table["table"]

            # Переформатируем колонки
            new_columns = []
            for col in table["columns"]:
                new_col = {
                    "name": col["name"],
                    "type": self.transform_type(col["type"]),
                    "nullable": col["nullable"]
                }
                new_columns.append(new_col)
            new_table["columns"] = new_columns

            # Сохраняем первичный ключ
            new_table["primary_key"] = table["primary_key"]

            # Внешние ключи переходим в чистый вид PostgreSQL
            new_fkeys = []
            for fk in table["foreign_keys"]:
                new_fk = {
                    "constraint_name": fk.get("name"),
                    "referenced_table": fk["referred_table"],
                    "local_columns": fk["constrained_columns"],
                    "remote_columns": fk["referred_columns"]
                }
                new_fkeys.append(new_fk)
            new_table["foreign_keys"] = new_fkeys

            # Индексы сохраняем в чистом виде
            new_table["indexes"] = table["indexes"]

            # Ограничения уникальности также оставляем без изменений
            new_table["unique_constraints"] = table["unique_constraints"]

            transformed_schema.append(new_table)

        return transformed_schema

    def display_transformed_schema(self, schema: List[Dict]):
        """
        Удобный вывод итогового трансформированного формата.
        """
        print(pformat(schema))
