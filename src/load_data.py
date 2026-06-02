import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from generate_data import generate_all

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


def run_schema(conn):
    print("Creating schema...")
    with open("sql/schema.sql", "r") as file:
        schema = file.read()

    with conn.cursor() as cur:
        cur.execute(schema)
        conn.commit()

    print("Schema created successfully.")


def load_table(conn, df, table_name):
    print(f"Loading {table_name}: {len(df):,} rows...")

    columns = list(df.columns)
    column_names = ", ".join(columns)
    rows = [tuple(row) for row in df.itertuples(index=False)]

    query = f"""
        INSERT INTO {table_name} ({column_names})
        VALUES %s
    """

    with conn.cursor() as cur:
        execute_values(cur, query, rows, page_size=5000)
        conn.commit()

    print(f"{table_name} loaded.")


def main():
    patients, admissions, diagnoses, treatments = generate_all()

    print("Connecting to AWS RDS...")
    conn = get_connection()
    print("Connected.")

    run_schema(conn)

    print("Starting patients insert...")
    load_table(conn, patients, "patients")

    print("Starting admissions insert...")
    load_table(conn, admissions, "admissions")

    print("Starting diagnoses insert...")
    load_table(conn, diagnoses, "diagnoses")

    print("Starting treatments insert...")
    load_table(conn, treatments, "treatments")

    conn.close()
    print("All data loaded successfully.")


if __name__ == "__main__":
    main()