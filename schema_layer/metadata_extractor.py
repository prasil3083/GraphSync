from source_database_layer import connection
from sqlalchemy import inspect, text
import pandas as pd
import json

# ENGINE + INSPECTOR
engine = connection.create_db_connection()
inspector = inspect(engine)


# get Tables
def get_tables():
    return inspector.get_table_names()


# Get Tables
def get_columns(table_name):
    return inspector.get_columns(table_name)


# Get Primary Key
def get_primary_key(table_name):
    return inspector.get_pk_constraint(table_name).get("constrained_columns")


# Get Foreing Key
def get_foreign_keys(table_name):
    return inspector.get_foreign_keys(table_name)


# Get Sample Data
def get_sample_data(table_name, limit=5):
    query = text(f"SELECT * FROM {table_name} LIMIT {limit}")
    with engine.connect() as conn:
        result = conn.execute(query)
        rows = result.fetchall()
        columns = result.keys()

    return [dict(zip(columns, row)) for row in rows]


# Get Table Meta Data
def get_table_metadata(table_name):

    return {
        "table_name": table_name,
        "columns": [
            {"name": col["name"], "type": str(col["type"]), "nullable": col["nullable"]}
            for col in get_columns(table_name)
        ],
        "primary_key": get_primary_key(table_name),
        "foreign_keys": get_foreign_keys(table_name),
        #"sample_data": get_sample_data(table_name),   # no need for the dampole data for this test
    }


def extract_full_metadata():
    tables = get_tables()
    return {"database_schema": [get_table_metadata(table) for table in tables]}


# -----------------------------
# RUN TEST
# -----------------------------
if __name__ == "__main__":
    metadata = extract_full_metadata()
    print(json.dumps(metadata, indent=2, default=str))
