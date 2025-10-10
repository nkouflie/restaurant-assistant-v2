#!/bin/bash
# Simple script to start just the database

set -e

echo "🐘 Starting PostgreSQL database..."

# Start database
docker-compose up -d db

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 5

# Test connection
echo "🔍 Testing database connection..."
if python -c "from app.db import create_tables; create_tables(); print('✅ Database is ready!')" 2>/dev/null; then
    echo "✅ Database is ready and accessible!"
else
    echo "❌ Database connection failed!"
    echo "Make sure your .env file has the correct DATABASE_URL"
    exit 1
fi

echo "🚀 Database is running on localhost:5432"
echo "📊 You can now start your FastAPI server"
