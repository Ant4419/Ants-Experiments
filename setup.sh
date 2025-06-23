#!/bin/bash
# setup.sh - One-command setup for Ants-Experiments
set -e

# Load environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "No .env file found. Copy .env.example to .env and fill in your values."
  exit 1
fi

# Build and start all services
cd docker

docker-compose up --build -d

# Wait for services to be healthy
sleep 10

echo "\nAll services started!"
echo "CEX API:        http://localhost:${CEX_PORT:-8000}/ticker"
echo "DEX API:        http://localhost:${DEX_PORT:-9000}"
echo "Dashboard:      http://localhost:${DASHBOARD_PORT:-8050}"
echo "Prometheus:     http://localhost:${PROMETHEUS_PORT:-9090}"
echo "Grafana:        http://localhost:${GRAFANA_PORT:-3000}"
echo "Anvil RPC:      http://localhost:8545"
