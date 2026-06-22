import psycopg


def connect_to_database(db_connection):
    connection = psycopg.connect(
        host=db_connection.host,
        port=db_connection.port,
        dbname=db_connection.database_name,
        user=db_connection.username,
        password=db_connection.encrypted_password,
    )
    print("Connected successfully!")

    return connection


def get_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)

    tables = cursor.fetchall()

    cursor.close()

    return tables

def get_columns(connection,table_name):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema='public'
    AND table_name=%s
    ORDER BY ordinal_position;
    """, (table_name,))

    columns = cursor.fetchall()
    cursor.close()

    return columns
