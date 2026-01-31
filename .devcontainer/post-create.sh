#!/bin/bash

# Post-create script for devcontainer setup

echo "🚀 Setting up development environment..."

# Install Claude Code CLI (runs as vscode user, installs to ~/.local/bin)
if ! command -v claude > /dev/null 2>&1; then
    echo "📦 Installing Claude Code CLI..."
    curl -fsSL https://claude.ai/install.sh | bash
    echo "✅ Claude Code CLI installed"
else
    echo "✅ Claude Code CLI already installed"
fi

# Ensure ~/.local/bin is on PATH for Claude CLI
export PATH="${HOME}/.local/bin:${PATH}"
echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ~/.bashrc 2>/dev/null || true

# Install agent-browser and download Chromium
echo "📦 Installing agent-browser..."
npm install -g agent-browser
agent-browser install  # Download Chromium
echo "✅ agent-browser installed"

# Verify Docker access (uses host engine via mounted socket)
if docker ps > /dev/null 2>&1; then
    echo "✅ Docker daemon accessible (host engine)"
else
    echo "⚠️  Docker daemon not accessible (ensure Docker Desktop / host Docker is running)"
fi

# Verify kubectl access
if kubectl version --client > /dev/null 2>&1; then
    echo "✅ kubectl is working"
    kubectl cluster-info 2>/dev/null || echo "⚠️  Kubernetes cluster not accessible"
else
    echo "⚠️  kubectl not working"
fi

# Verify gh
if command -v gh > /dev/null 2>&1; then
    echo "✅ GitHub CLI (gh) installed: $(gh --version | head -1)"
else
    echo "⚠️  GitHub CLI (gh) not found"
fi

# Set up Python virtual environment (optional)
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Set up Node.js (if package.json exists)
if [ -f "package.json" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Set up Poetry (if pyproject.toml exists)
if [ -f "pyproject.toml" ]; then
    echo "📦 Installing Python dependencies with Poetry..."
    poetry install
fi

echo "✨ Development environment setup complete!"









