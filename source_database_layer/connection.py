from sqlalchemy import create_engine

def create_db_connection():
    engine = create_engine(
        "postgresql+psycopg2://GraphSync:GraphSync@localhost:5432/GraphSync"
    )
    return engine