# virgin-devcontainer

A clean devcontainer setup template for development environments.

## Overview

This repository provides a production-ready devcontainer configuration with Node.js, Python, Docker, and Kubernetes support. It follows industry best practices and can be used as a starting point for new projects.

## Features

* **Python 3.11** with Poetry for dependency management
* **Node.js 20.x** with npm and common development tools
* **Docker CLI** - Uses host Docker daemon via socket mount
* **kubectl** - Mounted from host, configured with your Kubernetes cluster access
* **Development Tools**:
  - Python: black, flake8, pylint, pytest, pytest-asyncio, mypy
  - Node.js: TypeScript, ts-node, ESLint, Prettier, nodemon
* Clean, minimal devcontainer setup following best practices
* Version-pinned dependencies for reproducibility
* Security-focused configuration

## Getting Started

1. Clone this repository
2. Copy the `.devcontainer` folder to your project root
3. Customize the devcontainer configuration for your needs
4. Open in VS Code, Cursor, or GitHub Codespaces

## Prerequisites

- Docker Desktop or Docker Engine running on your host
- VS Code/Cursor with the "Dev Containers" extension installed
- Docker socket accessible (default: `/var/run/docker.sock`)
- kubectl installed on host (default: `/usr/local/bin/kubectl`)
- Kubernetes config file at `~/.kube/config`

## What Gets Mounted

The devcontainer automatically mounts:

1. **Docker Socket** (`/var/run/docker.sock`) - Allows container to use host Docker daemon
2. **Docker CLI** (`/usr/bin/docker`) - Docker client from host
3. **kubectl** (`/usr/local/bin/kubectl`) - Kubernetes CLI from host
4. **Kubernetes Config** (`~/.kube`) - Your Kubernetes cluster configuration
5. **MCP Config** (`~/.cursor/mcp.json`) - MCP server configuration for Cursor

## Best Practices Applied

This devcontainer follows industry best practices:
- ✅ Docker build context properly configured for devcontainer features
- ✅ Version-pinned dependencies for reproducibility
- ✅ `.dockerignore` file to optimize build performance
- ✅ Security-focused configuration with read-only mounts
- ✅ No `--privileged` flag (using host Docker daemon instead)

## Documentation

See [.devcontainer/README.md](.devcontainer/README.md) for detailed setup and usage instructions.

## License

MIT License - see LICENSE file for details
