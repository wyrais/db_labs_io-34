import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="gsllfiiz",
        database="Lab6"
    )