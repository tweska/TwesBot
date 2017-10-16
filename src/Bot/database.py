from psycopg2 import connect


def setup_connection(db_login_details):
    db_hostname, db_username, db_password, db_database = db_login_details

    return connect(
        host=db_hostname,
        user=db_username,
        password=db_password,
        dbname=db_database
    )
