import os
from dotenv import load_dotenv
import pyodbc

# Load .env
load_dotenv()

# Ambil dari environment
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    if DB_USER and DB_PASSWORD:
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_NAME};'
            f'UID={DB_USER};PWD={DB_PASSWORD};'
        )
    else:
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={DB_SERVER};'
            f'DATABASE={DB_NAME};'
            f'Trusted_Connection=yes;'
        )
    
    return pyodbc.connect(conn_str)
