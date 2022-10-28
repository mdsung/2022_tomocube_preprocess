import os
from pathlib import Path

import pandas as pd
import sqlalchemy as db
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
    return db.create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
    )


def main():
    target_projects = ("2022_tomocube_sepsis", "2022_tomocube_igra")
    engine = get_engine(HOST, PORT, USER, PASSWORD, DBNAME)
    sql_template = get_sql(Path("src/create_tomocube_metadata.sql"))

    results = []
    for project in target_projects:
        sql = sql_template.replace("2022_tomocube_sepsis", project)
        results.append(pd.read_sql(sql, engine))

    df = pd.concat(results)
    df.to_csv("data/processed/tomocube_metadata.csv", index=False)


if __name__ == "__main__":
    main()
