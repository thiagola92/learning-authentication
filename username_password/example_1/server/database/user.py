from database import CONN


def get_user_auth(user: str) -> tuple[str, str]:
    result = CONN.execute(
        "SELECT salt, hash FROM users WHERE user = $user",
        {"user": user},
    ).fetchone()

    if result:
        return (result[0], result[1])
    return ("", "")


def create_user(user: str, salt: str, hash: str) -> bool:
    CONN.execute(
        """
        INSERT INTO users (user, salt, hash) VALUES
        ($user, $salt, $hash)
        """,
        {"user": user, "salt": salt, "hash": hash},
    )
