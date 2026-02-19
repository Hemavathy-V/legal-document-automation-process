import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # loads from project root

def get_connection():
    print("PORT:", os.getenv("DATABASE_PORT"))  # debug

    return mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"),
        port=int(os.getenv("DATABASE_PORT")),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        database=os.getenv("DATABASE_NAME")
    )
