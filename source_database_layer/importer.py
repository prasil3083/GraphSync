import pandas as pd
import os


def import_to_postgres(files, path, engine):
    
    for fileName in files:
        full_path = os.path.join(path, fileName)
        table_name = os.path.splitext(fileName)[0].upper()

        if fileName.endswith(".csv"):
            df = pd.read_csv(full_path)

        # EXCEL
        elif fileName.endswith((".xlsx", ".xls")):
            df = pd.read_excel(full_path)

        # CREATE TABLE + INSERT
        df.to_sql(
            table_name,
            engine,
            if_exists="replace",
            index=False
        )
        print(f"Created table: {table_name}")