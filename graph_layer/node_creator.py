from sqlalchemy import text
from source_database_layer.connection import create_db_connection
from graph_layer.neo4j_connection import get_driver

sql_engine = create_db_connection()
neo4j_driver = get_driver()


def fetch_table_data(table_name):

    query = text(f'SELECT * FROM "{table_name}"')

    with sql_engine.connect() as conn:
        result = conn.execute(query)

        rows = result.fetchall()
        columns = result.keys()

    return [dict(zip(columns, row)) for row in rows]


# Create Node from using the table name and keys
def create_nodes(table_name, primary_key):

    data = fetch_table_data(table_name)
    label = table_name.capitalize()

    with neo4j_driver.session() as session:

        for row in data:

            query = f"""
            MERGE (n:{label} {{{primary_key}: $pk_value}})
            SET n += $properties
            """

            session.run(query, pk_value=row[primary_key], properties=row)

    print(f"Created nodes for {table_name}")
