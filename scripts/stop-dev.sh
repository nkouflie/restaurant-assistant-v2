#!/bin/bash
# Script to stop the development environment

set -e

echo "🛑 Stopping Restaurant Assistant Development Environment..."

# Stop all Docker containers
echo "🐳 Stopping Docker containers..."
docker-compose down

echo "✅ Development environment stopped!"
echo ""
echo "To start again, run: ./scripts/dev.sh"
