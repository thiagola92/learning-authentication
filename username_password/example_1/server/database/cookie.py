from database import CONN


def get_user_cred(user: str) -> tuple[str, str]:
    result = CONN.execute(
        "SELECT cred FROM cookies WHERE user = $user",
        {"user": user},
    ).fetchone()

    if result:
        return result[0]
    return ""


def save_credential(user: str, cred: str) -> bool:
    CONN.execute(
        """
        INSERT INTO cookies (user, cred) VALUES
        ($user, $cred)
        """,
        {"user": user, "cred": cred},
    )
