import duckdb
from config import PARQUET_DIR

con = duckdb.connect()


def get_db():
    """One DuckDB cursor per request."""
    cursor = con.cursor()

    try:
        yield cursor
    finally:
        cursor.close()