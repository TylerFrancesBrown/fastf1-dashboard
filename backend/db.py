import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="f1db",
        user="postgres",
        password="Harpswell2017!",
        host="localhost",
        port="5432"
    )