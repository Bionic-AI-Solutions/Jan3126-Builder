# OpenProject Integration for BMAD

This module provides the standard integration between BMAD methodology and OpenProject work management.

## Overview

OpenProject serves as the **PRIMARY work management system** for all BMAD projects:

- **Projects**: Top-level organization
- **Epics**: Business goals and major initiatives
- **Features**: Functional capabilities
- **User Stories**: User-centric requirements with acceptance criteria
- **Tasks**: Implementation work items

## Quick Setup

### 1. Get Your Project ID

```python
# Run this to find your OpenProject project
mcp_openproject_list_projects(active_only=True)
```

### 2. Get Type IDs

```python
# Run this to get work package types for your project
mcp_openproject_list_types(project_id=YOUR_PROJECT_ID)
```

### 3. Update Configuration

Edit `_bmad/_config/project-config.yaml`:

```yaml
openproject:
  enabled: true
  project_id: YOUR_PROJECT_ID  # ← Update this
  
  types:
    epic: 40           # ← Verify/update from list_types
    feature: 39
    user_story: 41
    task: 36
```

## Files in This Module

| File | Purpose |
|------|---------|
| `tools.md` | Complete MCP tool reference with all parameters |
| `workflow.md` | Work-driven development workflow and patterns |
| `README.md` | This setup guide |

## Integration with BMAD Agents

Each BMAD agent has specific OpenProject responsibilities:

| Agent | Primary Actions |
|-------|-----------------|
| **PM** | Create Epics, Features, User Stories from PRD |
| **Dev** | Query/update Tasks, log time |
| **SM** | Sprint planning, status reporting |
| **Architect** | Create technical tasks |
| **TEA** | Create test tasks, update bug status |

## Core Workflow

```
1. GET WORK    → mcp_openproject_list_work_packages(project_id, "open")
2. START       → mcp_openproject_update_work_package(id, status_id=77)
3. RESEARCH    → (Use Archon integration)
4. IMPLEMENT   → Write code
5. REVIEW      → mcp_openproject_update_work_package(id, status_id=79)
6. COMPLETE    → mcp_openproject_update_work_package(id, status_id=82)
7. NEXT        → Return to step 1
```

## Troubleshooting

### "Parameter must be integer, got string"

The OpenProject MCP server requires integer parameters. If using JSON-RPC, ensure proper type conversion.

### Can't Find Work Package Types

Run `mcp_openproject_list_types(project_id=YOUR_ID)` to get the correct type IDs for your OpenProject instance.

### Status Updates Failing

Check available statuses with `mcp_openproject_list_statuses()` and verify the status IDs in your config match.

## Related Documentation

- See `workflow.md` for detailed workflow patterns
- See `tools.md` for complete tool reference
- See `_bmad/integrations/archon/` for knowledge repository integration

