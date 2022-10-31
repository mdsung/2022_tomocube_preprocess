import os
from pathlib import Path

import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
DBNAME = os.environ["DBNAME"]


def get_sql(filepath: Path):
    with open(filepath, "r") as f:
        return f.read()


def get_engine(host, port, user, password, dbname):
    return sqlalchemy.create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
    )
