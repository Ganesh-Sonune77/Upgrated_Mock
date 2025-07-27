import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # your MySQL username
        password="Pass@123",  # your MySQL password
        database="mocktestdb"
    )