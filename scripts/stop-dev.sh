#!/usr/bin/env bash
# Stop running development services.

set -euo pipefail

echo "🛑 Stopping Restaurant Assistant services..."
docker compose down
echo "✅ Containers stopped."
echo "   Restart anytime with: ./scripts/dev.sh"
