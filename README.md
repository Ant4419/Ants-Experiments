# Local CEX/DEX Testnet Simulation

## Overview
This project simulates both CEX and DEX environments locally, supporting MetaMask, high-frequency bots, and monitoring.

## Quick Start
1. Clone this repository
2. Run `docker-compose up --build` from the `docker/` directory
3. Start Anvil (if not running in Docker):
   ```bash
   anvil --fork-url https://mainnet.infura.io/v3/YOUR_KEY --port 8545 --chain-id 31337 --auto-impersonate
   ```
4. Import generated private keys into MetaMask (localhost:8545)
5. Set environment variables as needed

## Structure
- `cex/` - FastAPI mock CEX
- `dex/` - DEX/Anvil/Foundry
- `bots/` - Trading bots
- `dashboard/` - Dash/Plotly or Grafana
- `docker/` - Docker Compose and configs
- `scripts/` - Utilities
- `tests/` - Test scripts
