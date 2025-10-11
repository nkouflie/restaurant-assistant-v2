#!/usr/bin/env bash
# Start only the PostgreSQL service for local development.

set -euo pipefail

echo "🐘 Starting PostgreSQL container..."
docker compose up -d db

echo "⏳ Waiting for database to be ready..."
sleep 5

echo "🔍 Testing database connection..."
if venv/bin/python - <<'PY' >/dev/null
from app.db import create_tables
create_tables()
print("ok")
PY
then
    echo "✅ Database is ready and accessible at localhost:5432."
else
    echo "❌ Database connection failed."
    echo "   Check DATABASE_URL in .env and confirm docker compose is running."
    exit 1
fi

echo "🚀 You can now run the API server (venv/bin/uvicorn app.main:app --reload)"
