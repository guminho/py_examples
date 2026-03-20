# database.py
from config import cfg


def connect():
    # settings.DATABASE_URL is a validated Dsn object
    print(f"{cfg.DATABASE_URL=}")

    # Accessing the secret safely
    print(f"{cfg.API_KEY=}")
    print(f"{cfg.JWT_SECRET=}")


if __name__ == "__main__":
    connect()
