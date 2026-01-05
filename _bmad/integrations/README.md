# BMAD Integrations Package

This package provides standard integrations for OpenProject work management and Archon knowledge repository.

## Quick Start

### New Project Setup

```bash
# Run interactive setup
python scripts/bmad-setup.py init
```

This will:
1. Create `_bmad/_config/project-config.yaml` with your settings
2. Generate `CLAUDE.md` with configured IDs
3. Create output directories

### Existing Project

If you already have a config file:

```bash
# Validate configuration
python scripts/bmad-setup.py validate

# Regenerate CLAUDE.md after config changes
python scripts/bmad-setup.py generate-claude-md

# View current configuration
python scripts/bmad-setup.py show-config
```

## Package Structure

```
_bmad/
├── _config/
│   └── project-config.yaml      # ← EDIT THIS for each project
├── integrations/
│   ├── openproject/
│   │   ├── README.md            # OpenProject setup guide
│   │   ├── tools.md             # Complete tool reference
│   │   └── workflow.md          # Work-driven development workflow
│   ├── archon/
│   │   ├── README.md            # Archon setup guide
│   │   ├── tools.md             # Complete tool reference
│   │   └── workflow.md          # Research-driven workflow
│   ├── workflows/
│   │   └── project-init/
│   │       └── workflow.md      # Project initialization workflow
│   ├── agent-integration-mixin.md  # Agent enhancement definitions
│   ├── cursor-rules.mdc         # Cursor rules for integrations
│   └── README.md                # This file
├── templates/
│   └── CLAUDE.md.template       # Template for CLAUDE.md generation
└── ...existing BMAD modules...

scripts/
└── bmad-setup.py                # Setup and management script
```

## Configuration

All project-specific settings are in `_bmad/_config/project-config.yaml`:

| Section | Purpose |
|---------|---------|
| `project` | Project identity (name, description, repo) |
| `team` | Team settings (user name, language) |
| `paths` | Output directories |
| `openproject` | OpenProject IDs and workflow settings |
| `archon` | Archon project ID and RAG settings |
| `testing` | TEA agent configuration |
| `workflows` | Story sizing, sprint settings |

### Minimum Required Configuration

```yaml
openproject:
  project_id: YOUR_PROJECT_ID  # From OpenProject

archon:
  project_id: "YOUR-UUID"      # From Archon
```

## How It Works

### 1. Configuration-Driven

All integration settings are centralized in `project-config.yaml`. When you:
- Change OpenProject project → Update config → Regenerate CLAUDE.md
- Add new type IDs → Update config → Agents use new IDs automatically

### 2. CLAUDE.md Generation

The `CLAUDE.md` file is generated from a template using your config values:

```bash
python scripts/bmad-setup.py generate-claude-md
```

This ensures:
- AI assistants have the correct project IDs
- Tool examples use your actual configuration
- No manual CLAUDE.md editing needed

### 3. Agent Integration

BMAD agents reference the integration modules:
- `_bmad/integrations/cursor-rules.mdc` - Always-on integration rules
- `_bmad/integrations/agent-integration-mixin.md` - Agent capabilities

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     BMAD AGENTS                             │
│  (PM, Dev, Architect, SM, TEA, Tech Writer, UX Designer)   │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │ Integration │  │   CLAUDE.md │  │   Config    │
     │   Modules   │  │  (Generated)│  │   (YAML)    │
     └─────────────┘  └─────────────┘  └─────────────┘
              │               │               │
              └───────────────┼───────────────┘
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

## Reusing for New Projects

### Step 1: Copy Integration Package

Copy these folders to your new project:
- `_bmad/integrations/`
- `_bmad/templates/`
- `_bmad/_config/project-config.yaml` (as template)
- `scripts/bmad-setup.py`

### Step 2: Initialize

```bash
cd new-project
python scripts/bmad-setup.py init
```

### Step 3: Configure

1. Get OpenProject project ID
2. Get/create Archon project
3. Update `project-config.yaml`
4. Regenerate CLAUDE.md

### Step 4: Verify

```bash
python scripts/bmad-setup.py validate
```

## Integration Rules

### OpenProject-First Rule

**ALWAYS** use OpenProject for work management:
- Create work packages before coding
- Update status when starting/completing work
- Never skip work package updates

### Research-First Rule

**ALWAYS** search Archon before implementing:
- Search knowledge base for existing patterns
- Find code examples
- Read full documentation pages

### Configuration Reference Rule

**ALWAYS** use configured IDs:
- Don't hardcode type/status/priority IDs
- Read from `project-config.yaml`
- Use generated CLAUDE.md as reference

## Troubleshooting

### "project_id not configured"

Run setup or manually edit `project-config.yaml`:
```bash
python scripts/bmad-setup.py init
```

### "CLAUDE.md out of date"

Regenerate after config changes:
```bash
python scripts/bmad-setup.py generate-claude-md
```

### "Type/status ID not found"

Get correct IDs from OpenProject:
```python
mcp_openproject_list_types(project_id=YOUR_ID)
mcp_openproject_list_statuses()
```

Update `project-config.yaml` with correct values.

## Related Documentation

- [OpenProject Integration](openproject/README.md)
- [Archon Integration](archon/README.md)
- [Project Initialization Workflow](workflows/project-init/workflow.md)
- [Agent Integration Mixin](agent-integration-mixin.md)

