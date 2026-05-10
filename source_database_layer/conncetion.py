from sqlalchemy import create_engine
def create_db_connection():
    engine = create_engine(
        "postgresql+psycopg2://GraphSync:123123123@localhost:5432/GraphSync"
    )
    return engine