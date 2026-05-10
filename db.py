import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASS", "yourpassword"),
        database=os.environ.get("DB_NAME", "library_db"),
        port=int(os.environ.get("DB_PORT", 3306)),
        connection_timeout=10
    )