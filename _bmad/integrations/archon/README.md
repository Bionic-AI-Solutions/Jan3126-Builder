# Archon Integration for BMAD

This module provides the standard integration between BMAD methodology and Archon knowledge repository.

## Overview

Archon serves as the **knowledge repository** for all BMAD projects:

- **Documents**: Technical specifications, architecture docs, PRDs
- **Research**: Technical research and findings
- **Code Examples**: Patterns and implementation examples
- **Decisions**: Architecture Decision Records (ADRs)

**Important:** Archon is NOT for task management - use OpenProject for that.

## Quick Setup

### 1. Create or Find Your Archon Project

```python
# Check if project exists
projects = mcp_archon_find_projects(query="My Project")

# Or create new
project = mcp_archon_manage_project(
    action="create",
    title="My Project - Knowledge Base",
    description="Technical documentation and research"
)
print(project["project"]["id"])  # Save this UUID
```

### 2. Get Available Knowledge Sources

```python
# List sources for RAG search
sources = mcp_archon_rag_get_available_sources()
# Note the source IDs you want to use frequently
```

### 3. Update Configuration

Edit `_bmad/_config/project-config.yaml`:

```yaml
archon:
  enabled: true
  project_id: "your-project-uuid"  # ← From step 1
  
  rag:
    default_match_count: 5
    preferred_sources:               # ← From step 2
      - "src_abc123"
      - "src_def456"
```

## Files in This Module

| File | Purpose |
|------|---------|
| `tools.md` | Complete MCP tool reference |
| `workflow.md` | Research-driven development workflow |
| `README.md` | This setup guide |

## Core Workflow

```
1. IDENTIFY    → What knowledge do I need?
2. SEARCH      → mcp_archon_rag_search_knowledge_base(query, ...)
3. EXAMPLES    → mcp_archon_rag_search_code_examples(query, ...)
4. READ        → mcp_archon_rag_read_full_page(page_id)
5. IMPLEMENT   → Use research in implementation
6. DOCUMENT    → mcp_archon_manage_document(...) for new docs
```

## Integration with OpenProject

Archon and OpenProject work together:

| System | Responsibility |
|--------|----------------|
| **OpenProject** | Work items (epics, stories, tasks), status, sprints |
| **Archon** | Knowledge (docs, research, examples, decisions) |

**Link them:** Include OpenProject IDs in Archon documents:

```python
mcp_archon_manage_document(
    action="create",
    project_id=archon_id,
    title="Epic 1: Technical Spec",
    content={
        "markdown": f"{spec_content}\n\n---\n**OpenProject Epic:** {epic_id}"
    },
    tags=["epic-1", "spec"]
)
```

## Common Tasks

### Search Documentation
```python
results = mcp_archon_rag_search_knowledge_base(
    query="authentication JWT",  # Keep queries SHORT (2-5 words)
    match_count=5
)
```

### Find Code Examples
```python
examples = mcp_archon_rag_search_code_examples(
    query="FastAPI middleware",
    match_count=3
)
```

### Store New Document
```python
mcp_archon_manage_document(
    action="create",
    project_id=archon_project_id,
    title="Architecture Overview",
    document_type="spec",
    content={"markdown": "# Architecture\n\n..."},
    tags=["architecture"]
)
```

## Troubleshooting

### Poor Search Results

- **Shorten your query** to 2-5 keywords
- Try different keyword combinations
- Use source filtering if you know where info should be

### Source ID Not Working

- Source IDs are internal identifiers (e.g., "src_abc123")
- NOT URLs or domain names
- Run `mcp_archon_rag_get_available_sources()` to get current IDs

### Document Not Found

- Use `mcp_archon_find_documents(project_id=...)` to list documents
- Verify you're using the correct `project_id` (UUID format)

## Related Documentation

- See `workflow.md` for detailed workflow patterns
- See `tools.md` for complete tool reference
- See `_bmad/integrations/openproject/` for work management

