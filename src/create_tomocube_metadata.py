from pathlib import Path

import pandas as pd

from src.database import DBNAME, HOST, PASSWORD, PORT, USER, get_engine, get_sql


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
