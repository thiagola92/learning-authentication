from database import CONN


def db_setup():
    CONN.execute("""
        CREATE SEQUENCE IF NOT EXISTS user_id_sequence START 1
    """)

    CONN.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id      integer     primary key     default nextval('user_id_sequence'),
            user    text        not null        unique,
            salt    text        not null,
            hash    text        not null
        )
    """)

    CONN.execute("""
        CREATE TABLE IF NOT EXISTS cookies (
            user    text        not null        unique,
            cred    text        not null,
        )
    """)
