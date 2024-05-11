import duckdb


def setup():
    cursor = duckdb.connect("users.db")

    cursor.execute("""
        CREATE SEQUENCE IF NOT EXISTS user_id_sequence START 1
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id      integer     primary key     default nextval('user_id_sequence'),
            user    text        not null        unique,
            salt    text        not null,
            hash    text        not null
        )
    """)


def get_user_auth(user: str) -> tuple[str, str]:
    cursor = duckdb.connect("users.db")
    result = cursor.execute(
        "SELECT salt, hash FROM users WHERE user = $user",
        {"user": user},
    ).fetchone()

    if result:
        return (result[0], result[1])
    return ("", "")


def create_user(user: str, salt: str, hash: str) -> bool:
    cursor = duckdb.connect("users.db")
    cursor.execute(
        """
        INSERT INTO users (user, salt, hash) VALUES
        ($user, $salt, $hash)
        """,
        {"user": user, "salt": salt, "hash": hash},
    )