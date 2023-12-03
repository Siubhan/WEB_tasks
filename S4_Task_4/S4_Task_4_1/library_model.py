import pandas as pd


def get_table(conn, table_name) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, conn)
