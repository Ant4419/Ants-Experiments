# Placeholder for DEX service (e.g., Foundry/Anvil or custom DEX)
FROM ghcr.io/foundry-rs/foundry:latest
WORKDIR /app
COPY . .
USER root
RUN apt-get update && apt-get install -y curl
USER foundry
CMD ["anvil", "--host", "0.0.0.0", "--port", "9000", "--chain-id", "12345"]
