from sqlalchemy import create_engine, text
from db import connection_url

def main():
    master = create_engine(connection_url("master"), future=True)
    with master.begin() as conn:
        conn.execute(text("""
        IF DB_ID(N'TaqhiShoppingMall') IS NULL
            CREATE DATABASE TaqhiShoppingMall
        """))
    print("Database ensured: TaqhiShoppingMall")
    print("Next run sql/schema.sql and sql/seed.sql in SQL Server Management Studio.")

if __name__ == "__main__":
    main()
