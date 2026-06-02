import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("AWS_RDS_HOST"),
        database=os.getenv("AWS_RDS_DB"),
        user=os.getenv("AWS_RDS_USER"),
        password=os.getenv("AWS_RDS_PASSWORD"),
        port=os.getenv("AWS_RDS_PORT", 5432),
        sslmode="require"
    )


def run_query(conn, sql_file):
    with open(sql_file, "r") as file:
        query = file.read()

    return pd.read_sql_query(query, conn)


def run_all_queries():
    conn = get_connection()
    print("Connected to AWS RDS.")

    query_files = [
        ("01_top_diagnoses", "sql/01_top_diagnoses.sql"),
        ("02_length_of_stay", "sql/02_length_of_stay.sql"),
        ("03_deprivation_analysis", "sql/03_deprivation_analysis.sql"),
        ("04_admission_trends", "sql/04_admission_trends.sql"),
        ("05_same_day_discharge", "sql/05_same_day_discharge.sql"),
        ("06_diagnosis_los_ranking", "sql/06_diagnosis_los_ranking.sql"),
    ]

    results = {}

    for name, filepath in query_files:
        print(f"Running {name}...")
        df = run_query(conn, filepath)
        results[name] = df
        print(f"Returned {len(df)} rows.")

    conn.close()
    return results


if __name__ == "__main__":
    results = run_all_queries()

    for name, df in results.items():
        print(f"\n===== {name} =====")
        print(df.head(10))