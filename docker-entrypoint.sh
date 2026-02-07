#!/bin/sh
set -e

echo "Waiting for database to be ready..."
python - <<'PY'
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    raise SystemExit("DATABASE_URL is not set")

engine = create_engine(db_url, pool_pre_ping=True)
for _ in range(30):
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        print("Database is ready.")
        break
    except OperationalError:
        time.sleep(2)
else:
    raise SystemExit("Database is not ready after waiting.")
PY

echo "Running migrations..."
python migrate_db.py

echo "Seeding base data (if missing)..."
python setup_db.py

echo "Seeding extended packages..."
python seed_packages.py

echo "Starting app..."
python app.py
