import mysql.connector
from mysql.connector import Error

# Persistent connection
db_connection = None

def connect_to_database():
    global db_connection
    if not db_connection or not db_connection.is_connected():
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="your_user",
                password="your_password",
                database="python"
            )
        except Error as e:
            print(f"Database connection error: {e}")
            raise
    return db_connection

def get_latest_update_id():
    cursor = connect_to_database().cursor()
    cursor.execute("SELECT MAX(update_id) FROM updates")
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result[0] else 0

def save_update_id(update_id):
    cursor = connect_to_database().cursor()
    cursor.execute("INSERT INTO updates (update_id) VALUES (%s)", (update_id,))
    connect_to_database().commit()
    cursor.close()
