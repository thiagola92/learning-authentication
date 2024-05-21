from datetime import datetime, timedelta

import duckdb


conn = duckdb.connect("users.db")


def setup():
    conn.execute("""
        CREATE SEQUENCE IF NOT EXISTS user_id_sequence START 1
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id      integer     primary key     default nextval('user_id_sequence'),
            email   text        not null        unique,
            salt    text        not null,
            hash    text        not null
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS recovery_codes (
            email   text        primary key     not null,
            code    text        not null,
            time    timestamp
        )
    """)


def get_user_auth(email: str) -> tuple[str, str]:
    result = conn.execute(
        "SELECT salt, hash FROM users WHERE email = $email",
        {"email": email},
    ).fetchone()

    if result:
        return (result[0], result[1])
    return ("", "")


def create_user(email: str, salt: str, hash: str) -> bool:
    conn.execute(
        """
        INSERT INTO users (email, salt, hash) VALUES
            ($email, $salt, $hash)
        """,
        {"email": email, "salt": salt, "hash": hash},
    )


def create_recovery_code(email: str, code: str):
    conn.execute(
        """
        INSERT INTO recovery_codes (email, code, time) VALUES
            ($email, $code, current_timestamp)
        ON CONFLICT (email) DO UPDATE
            SET code = EXCLUDED.code
        """,
        {"email": email, "code": code},
    )


def is_recovery_code_valid(email: str, code: str) -> bool:
    result = conn.execute(
        """
        SELECT email, code, time, current_timestamp
        FROM recovery_codes
        WHERE email = $email AND code = $code
        """,
        {"email": email, "code": code},
    ).fetchone()

    if not result:
        return False

    created: datetime = result[2]
    now: datetime = result[3]
    now = now.replace(tzinfo=None)
    diff: timedelta = created - now

    # Válido por uma hora
    if diff.total_seconds() > 3600:
        return False

    return True


def delete_recovery_code(email: str):
    conn.execute(
        """
        DELETE FROM recovery_codes WHERE email = $email
        """,
        {"email": email},
    )


def change_account(email: str, salt: str, hash: str):
    conn.execute(
        """
        UPDATE users
        SET salt = $salt,
            hash = $hash
        WHERE email = $email
        """,
        {"email": email, "salt": salt, "hash": hash},
    )