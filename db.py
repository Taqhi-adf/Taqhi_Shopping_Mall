from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from config import (
    SQL_SERVER, SQL_DATABASE, SQL_DRIVER, SQL_TRUSTED_CONNECTION,
    SQL_ENCRYPT, SQL_TRUST_SERVER_CERTIFICATE, SQL_USERNAME, SQL_PASSWORD
)

def connection_url(database: str | None = None) -> str:
    db = database or SQL_DATABASE
    params = [
        f"DRIVER={{{SQL_DRIVER}}}",
        f"SERVER={SQL_SERVER}",
        f"DATABASE={db}",
        f"Encrypt={SQL_ENCRYPT}",
        f"TrustServerCertificate={SQL_TRUST_SERVER_CERTIFICATE}",
    ]
    if SQL_TRUSTED_CONNECTION.lower() == "yes":
        params.append("Trusted_Connection=yes")
    else:
        params.extend([f"UID={SQL_USERNAME}", f"PWD={SQL_PASSWORD}"])
    return "mssql+pyodbc:///?odbc_connect=" + quote_plus(";".join(params))

engine = create_engine(connection_url(), pool_pre_ping=True, future=True)

def fetch_all(sql: str, params: dict | None = None):
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row._mapping) for row in result]

def fetch_one(sql: str, params: dict | None = None):
    with engine.connect() as conn:
        row = conn.execute(text(sql), params or {}).mappings().first()
        return dict(row) if row else None

def execute(sql: str, params: dict | None = None):
    with engine.begin() as conn:
        conn.execute(text(sql), params or {})
