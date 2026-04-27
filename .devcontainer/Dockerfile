FROM mcr.microsoft.com/devcontainers/python:3.12

# Install Quarto at image build time so it is available immediately in Codespaces.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && curl -fsSL -o /tmp/quarto.deb https://github.com/quarto-dev/quarto-cli/releases/latest/download/quarto-linux-amd64.deb \
    && apt-get install -y /tmp/quarto.deb \
    && rm -f /tmp/quarto.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
