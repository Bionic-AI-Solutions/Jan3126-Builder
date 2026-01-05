# virgin-devcontainer

A clean devcontainer setup template for development environments with BMAD methodology integrations.

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
* **BMAD Integrations** - OpenProject work management + Archon knowledge repository
* Clean, minimal devcontainer setup following best practices
* Version-pinned dependencies for reproducibility
* Security-focused configuration

## Getting Started

1. Clone this repository
2. Copy the `.devcontainer` folder to your project root
3. Copy the `_bmad` folder for BMAD methodology support
4. Copy `scripts/bmad-setup.py` for project initialization
5. Customize the devcontainer configuration for your needs
6. Open in VS Code, Cursor, or GitHub Codespaces

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

---

## BMAD Integrations Package

This template includes the **BMAD Integrations Package** for standardized work management and knowledge repository integration.

### What's Included

```
_bmad/
├── _config/
│   └── project-config.yaml      # ← EDIT THIS for each project
├── integrations/
│   ├── openproject/             # OpenProject MCP integration
│   │   ├── README.md
│   │   ├── tools.md             # Complete tool reference
│   │   └── workflow.md          # Work-driven development workflow
│   ├── archon/                  # Archon MCP integration
│   │   ├── README.md
│   │   ├── tools.md             # Complete tool reference
│   │   └── workflow.md          # Research-driven workflow
│   ├── workflows/
│   │   └── project-init/        # Project initialization workflow
│   ├── agent-integration-mixin.md
│   ├── cursor-rules.mdc
│   └── README.md
└── templates/
    └── CLAUDE.md.template       # Template for CLAUDE.md generation

scripts/
└── bmad-setup.py                # Setup and management script
```

### Quick Start - BMAD Setup

```bash
# Interactive project initialization
python scripts/bmad-setup.py init

# Regenerate CLAUDE.md after config changes
python scripts/bmad-setup.py generate-claude-md

# Validate configuration
python scripts/bmad-setup.py validate

# Show current configuration
python scripts/bmad-setup.py show-config
```

### Configuration

Edit `_bmad/_config/project-config.yaml` with your project settings:

```yaml
project:
  name: "my-project"
  display_name: "My Project"

openproject:
  enabled: true
  project_id: 8  # Your OpenProject project ID

archon:
  enabled: true
  project_id: "your-uuid-here"  # Your Archon project UUID
```

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     BMAD AGENTS                             │
│  (PM, Dev, Architect, SM, TEA, Tech Writer, UX Designer)   │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
     ┌─────────────────────┐     ┌─────────────────────┐
     │     OPENPROJECT     │     │       ARCHON        │
     │  (Work Management)  │     │ (Knowledge Repo)    │
     │                     │     │                     │
     │  • Epics            │     │  • Documents        │
     │  • Stories          │     │  • Research         │
     │  • Tasks            │     │  • Code Examples    │
     │  • Status           │     │  • Specifications   │
     └─────────────────────┘     └─────────────────────┘
```

### Core Workflow

1. **OpenProject-First**: All work items are managed in OpenProject
2. **Research-First**: Search Archon knowledge base before implementing
3. **Configuration-Driven**: Single `project-config.yaml` for all settings

### Detailed Documentation

- [BMAD Integrations README](_bmad/integrations/README.md)
- [OpenProject Integration](_bmad/integrations/openproject/README.md)
- [Archon Integration](_bmad/integrations/archon/README.md)

---

## Documentation

See [.devcontainer/README.md](.devcontainer/README.md) for detailed devcontainer setup and usage instructions.

## License

MIT License - see LICENSE file for details
