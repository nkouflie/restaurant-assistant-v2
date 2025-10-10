#!/bin/bash
# Development startup script for Restaurant Assistant

set -e  # Exit on any error

echo "🚀 Starting Restaurant Assistant Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    print_status "Please create a .env file with your database configuration"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Start database
print_status "Starting PostgreSQL database..."
docker-compose up -d db

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 5

# Check if database is accessible
print_status "Testing database connection..."
if python -c "from app.db import create_tables; create_tables(); print('Database connection successful!')" 2>/dev/null; then
    print_success "Database is ready!"
else
    print_error "Database connection failed!"
    print_status "Make sure your .env file has the correct DATABASE_URL"
    print_status "For local development, use: DATABASE_URL=postgresql://postgres:NKGiants32914!@localhost:5432/restaurant-db"
    exit 1
fi

# Run code quality checks
print_status "Running code quality checks..."
if pre-commit run --all-files; then
    print_success "Code quality checks passed!"
else
    print_warning "Code quality issues found. They will be fixed automatically."
fi

# Run tests
print_status "Running tests..."
if python -m pytest tests/ -v; then
    print_success "All tests passed!"
else
    print_error "Some tests failed!"
    exit 1
fi

print_success "🎉 Development environment is ready!"
print_status ""
print_status "Next steps:"
print_status "1. Start the FastAPI server using Cursor's debug configuration"
print_status "2. Or run manually: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
print_status "3. Visit http://localhost:8000/docs for API documentation"
print_status ""
print_status "Available commands:"
print_status "  - Run tests: python -m pytest tests/ -v"
print_status "  - Check code quality: pre-commit run --all-files"
print_status "  - Format code: black app/ tests/"
print_status "  - Stop database: docker-compose down"
