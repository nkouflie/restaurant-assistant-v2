#!/usr/bin/env bash
# Development bootstrap script for Restaurant Assistant

set -euo pipefail

echo "🚀 Starting Restaurant Assistant development setup..."

# Colour helpers
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn()   { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error()  { echo -e "${RED}[ERROR]${NC} $1"; }

# Ensure .env is present
if [[ ! -f .env ]]; then
    error ".env file not found."
    log "Copy .env.example to .env and update DATABASE_URL / API keys."
    exit 1
fi

# Ensure virtualenv exists
if [[ ! -d venv ]]; then
    warn "Virtual environment missing. Creating..."
    python3 -m venv venv
    success "Virtual environment created."
fi

# Install dependencies
log "Installing dependencies..."
venv/bin/pip install -r requirements.txt >/dev/null
success "Dependencies installed."

# Start database container
log "Starting PostgreSQL container..."
docker compose up -d db

log "Waiting for database to become ready..."
sleep 5

# Verify DB connectivity
log "Applying database migrations (create tables)..."
if venv/bin/python - <<'PY' >/dev/null;
from app.db import create_tables
create_tables()
print("ok")
PY
then
    success "Database connection verified."
else
    error "Database connection failed."
    log "Check DATABASE_URL in .env and ensure docker compose is running."
    exit 1
fi

# Run lint / formatting
log "Running Ruff (lint + format)..."
if venv/bin/pre-commit run --all-files; then
    success "Code quality checks passed."
else
    warn "Hooks fixed issues. Review changes and rerun if needed."
fi

# Run tests
log "Running test suite..."
if venv/bin/python -m pytest -v; then
    success "All tests passed."
else
    error "Tests failed. Inspect the output above."
    exit 1
fi

success "🎉 Development environment ready."
log "Next steps:"
log "  • Start API: venv/bin/uvicorn app.main:app --reload"
log "  • Docs: http://localhost:8000/docs"
log "Helpers:"
log "  • Lint/format: venv/bin/ruff check --fix . && venv/bin/ruff format ."
log "  • Run tests: venv/bin/python -m pytest"
log "  • Stop services: docker compose down"
