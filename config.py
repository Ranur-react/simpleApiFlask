import os
from dotenv import load_dotenv
import pyodbc
import mysql.connector

# Load .env
load_dotenv()

# Ambil dari environment untuk SQL Server
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Ambil dari environment untuk MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
ENVIRONMENT = os.getenv("ENVIRONMENT")

def get_db_connection():
    if ENVIRONMENT == 'development':
        return get_sqlserver_connection()
    elif ENVIRONMENT == 'Production':
        return get_mysql_connection()
    else:
        raise ValueError("Environment tidak dikenali. Gunakan 'SQLSERVER' atau 'MYSQL'.")
def get_sqlserver_connection():
    """Koneksi ke SQL Server"""
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

def get_mysql_connection():
    """Koneksi ke MySQL"""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )
