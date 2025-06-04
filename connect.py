import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from mysql.connector import Error

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),       # or your database host
            user=os.environ.get("DB_USER"),       # or your database user
            password=os.environ.get("DB_PASSWORD"), # or your database password
            database=os.environ.get("DB_NAME")     # or your database name
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            return connection

    except Error as e:
        print(f"Error: {e}")
        return None

    return None

# Example usage
conn = connect_to_database()

# Don't forget to close the connection when done
if conn:
    conn.close()
