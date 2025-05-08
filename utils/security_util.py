import os

from dotenv import load_dotenv

load_dotenv()
ADMIN_USERNAMES = list(map(lambda x: x.lower().strip(), str(os.getenv("ADMIN_USERNAMES", "")).split(",")))
if ADMIN_USERNAMES == [""]: ADMIN_USERNAMES = []
print(f"ADMIN_USERNAMES: {ADMIN_USERNAMES}")


def is_admin(username: str) -> bool:
    return username.lower() in ADMIN_USERNAMES
