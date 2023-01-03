import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DRIVER = "psycopg2"

PGUSER = os.getenv("PGUSER", "docker")
PGPASSWORD = os.getenv("PGPASSWORD", "docker")
PGHOST = os.getenv("PGHOST", "192.168.86.205")
PGPORT = os.getenv("PGPORT", "5432")
PGDATABASE = os.getenv("PGDATABASE", "app")

CONN_STRING = (
    f"postgresql+{DRIVER}://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
)


def get_engine():
    return create_engine(CONN_STRING)


def get_session():
    return Session(get_engine())
