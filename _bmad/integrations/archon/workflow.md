# Archon Knowledge Repository Workflow

This workflow defines how BMAD agents use Archon as a knowledge repository.

## Core Principle: Research Before Implementation

**RULE:** Always search the knowledge base before implementing new features.

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESEARCH-DRIVEN DEVELOPMENT                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. IDENTIFY NEED                                                │
│     └── What knowledge do I need for this task?                 │
│                                                                  │
│  2. SEARCH KNOWLEDGE BASE                                        │
│     └── mcp_archon_rag_search_knowledge_base(query, ...)        │
│                                                                  │
│  3. FIND CODE EXAMPLES                                           │
│     └── mcp_archon_rag_search_code_examples(query, ...)         │
│                                                                  │
│  4. READ DETAILED CONTENT                                        │
│     └── mcp_archon_rag_read_full_page(page_id)                  │
│                                                                  │
│  5. IMPLEMENT WITH CONTEXT                                       │
│     └── Use research findings in implementation                  │
│                                                                  │
│  6. DOCUMENT DECISIONS                                           │
│     └── mcp_archon_manage_document(...) for ADRs, specs         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Knowledge Categories

### What Goes in Archon

✅ **Store in Archon:**
- Technical specifications
- Architecture documents
- API documentation
- Research findings
- Design documents
- Architecture Decision Records (ADRs)
- Code patterns and examples
- Reference documentation

❌ **Do NOT Store in Archon:**
- Tasks and work items (use OpenProject)
- Sprint status (use OpenProject)
- Bug reports (use OpenProject)
- Time tracking (use OpenProject)

## Document Types and Usage

| Type | Usage | Example |
|------|-------|---------|
| `spec` | Technical specifications | Architecture docs, API specs |
| `design` | Design documents | System design, database design |
| `note` | General notes | Meeting notes, research notes |
| `prp` | Product proposals | Feature proposals, enhancements |
| `api` | API documentation | Endpoint docs, SDK guides |
| `guide` | Usage guides | Tutorials, how-to guides |

## Research Workflow Patterns

### Pattern 1: Targeted Documentation Search

When you need information from specific documentation:

```python
# Step 1: Get available knowledge sources
sources = mcp_archon_rag_get_available_sources()
# Returns: {"sources": [{"id": "src_abc123", "title": "React Docs", "url": "..."}, ...]}

# Step 2: Find the source ID for your needs
# Look through sources to find the one you need

# Step 3: Search within that source
results = mcp_archon_rag_search_knowledge_base(
    query="hooks state management",
    source_id="src_abc123",  # Filter to React docs
    match_count=5
)

# Step 4: Read full content
for result in results["results"]:
    full = mcp_archon_rag_read_full_page(page_id=result["page_id"])
    # Use content
```

### Pattern 2: General Knowledge Search

When you need to explore across all knowledge:

```python
# Search broadly (no source filter)
results = mcp_archon_rag_search_knowledge_base(
    query="authentication JWT",
    match_count=10
)

# Results include source information
for result in results["results"]:
    print(f"Source: {result['source']}, Title: {result['title']}")
```

### Pattern 3: Code Example Discovery

When you need implementation patterns:

```python
# Find code examples
examples = mcp_archon_rag_search_code_examples(
    query="FastAPI dependency injection",
    match_count=5
)

# Examples include code snippets and context
for example in examples["results"]:
    print(f"Example: {example['title']}")
    print(f"Code: {example['content']}")
```

### Pattern 4: Browse Documentation Structure

When you need to explore a documentation source:

```python
# List all pages in a source
pages = mcp_archon_rag_list_pages_for_source(
    source_id="src_abc123"
)

# Optionally filter by section
pages = mcp_archon_rag_list_pages_for_source(
    source_id="src_abc123",
    section="# Getting Started"
)

# Read specific pages
for page in pages["pages"][:5]:
    content = mcp_archon_rag_read_full_page(page_id=page["id"])
```

## Document Management Workflows

### Creating Project Knowledge Base

At project start, set up the knowledge repository:

```python
# 1. Create Archon project for knowledge
project = mcp_archon_manage_project(
    action="create",
    title="{project_name} - Knowledge Base",
    description="Technical documentation and research for {project_name}",
    github_repo="{github_url}"  # Optional
)
archon_project_id = project["project"]["id"]

# 2. Store this ID in project-config.yaml
# archon:
#   project_id: "{archon_project_id}"

# 3. Create initial documentation
mcp_archon_manage_document(
    action="create",
    project_id=archon_project_id,
    title="Project Overview",
    document_type="guide",
    content={"markdown": "# Project Overview\n\n..."},
    tags=["overview", "getting-started"]
)
```

### Storing Architecture Documents

```python
mcp_archon_manage_document(
    action="create",
    project_id=archon_project_id,
    title="System Architecture",
    document_type="spec",
    content={
        "markdown": """
        # System Architecture
        
        ## Overview
        ...
        
        ## Components
        ...
        
        ## Data Flow
        ...
        
        ---
        **OpenProject Reference:** Epic {epic_id}
        """
    },
    tags=["architecture", "system-design"],
    author="Architect Agent"
)
```

### Creating Architecture Decision Records (ADRs)

```python
mcp_archon_manage_document(
    action="create",
    project_id=archon_project_id,
    title="ADR-001: Database Selection",
    document_type="note",
    content={
        "markdown": """
        # ADR-001: Database Selection
        
        **Status:** Accepted
        **Date:** 2025-01-05
        **Deciders:** Architecture Team
        
        ## Context
        We need to select a database for the RAG system that supports
        vector operations and multi-tenancy.
        
        ## Decision
        We will use PostgreSQL with pgvector extension.
        
        ## Rationale
        - Native vector operations with pgvector
        - Row-level security for multi-tenancy
        - Mature ecosystem and tooling
        - Cost-effective compared to specialized vector DBs
        
        ## Consequences
        
        ### Positive
        - Single database for all data types
        - Familiar SQL interface
        - Strong ACID guarantees
        
        ### Negative
        - May need optimization for very large vector sets
        - Requires pgvector extension maintenance
        
        ## Related
        - OpenProject Story: {story_id}
        """
    },
    tags=["adr", "database", "architecture-decision"]
)
```

### Documenting API Specifications

```python
mcp_archon_manage_document(
    action="create",
    project_id=archon_project_id,
    title="API Specification v1.0",
    document_type="api",
    content={
        "markdown": """
        # API Specification v1.0
        
        ## Base URL
        `https://api.example.com/v1`
        
        ## Authentication
        Bearer token in Authorization header
        
        ## Endpoints
        
        ### POST /documents
        Upload a document for processing.
        
        **Request:**
        ```json
        {
            "tenant_id": "string",
            "content": "string",
            "metadata": {}
        }
        ```
        
        **Response:**
        ```json
        {
            "document_id": "uuid",
            "status": "processing"
        }
        ```
        """
    },
    tags=["api", "specification", "v1"]
)
```

## Agent-Specific Workflows

### PM Agent

```python
# Store product brief
mcp_archon_manage_document(
    action="create",
    project_id=archon_project_id,
    title="Product Brief: {feature_name}",
    document_type="prp",
    content={"markdown": brief_content},
    tags=["product-brief", "planning"]
)

# Store PRD
mcp_archon_manage_document(
    action="create",
    project_id=archon_project_id,
    title="PRD: {project_name}",
    document_type="spec",
    content={"markdown": prd_content},
    tags=["prd", "requirements"]
)
```

### Architect Agent

```python
# Research existing patterns
patterns = mcp_archon_rag_search_knowledge_base(
    query="microservices event driven",
    match_count=5
)

# Store architecture
mcp_archon_manage_document(
    action="create",
    project_id=archon_project_id,
    title="Architecture: {component_name}",
    document_type="spec",
    content={"markdown": architecture_content},
    tags=["architecture", component_name]
)
```

### Dev Agent

```python
# Research implementation approach
knowledge = mcp_archon_rag_search_knowledge_base(
    query="vector embeddings API",
    match_count=5
)

examples = mcp_archon_rag_search_code_examples(
    query="OpenAI embeddings Python",
    match_count=3
)

# Document implementation notes
mcp_archon_manage_document(
    action="create",
    project_id=archon_project_id,
    title="Implementation Notes: {feature}",
    document_type="note",
    content={"markdown": notes_content},
    tags=["implementation", "notes", feature_name]
)
```

### Tech Writer Agent

```python
# Create usage guide
mcp_archon_manage_document(
    action="create",
    project_id=archon_project_id,
    title="User Guide: {feature_name}",
    document_type="guide",
    content={"markdown": guide_content},
    tags=["documentation", "user-guide", feature_name]
)

# Update existing documentation
mcp_archon_manage_document(
    action="update",
    project_id=archon_project_id,
    document_id=existing_doc_id,
    content={"markdown": updated_content}
)
```

## Version Control

### Creating Document Versions

```python
# Create a version snapshot before major changes
mcp_archon_manage_version(
    action="create",
    project_id=archon_project_id,
    field_name="docs",
    content=current_docs,
    change_summary="Pre-v2.0 snapshot",
    created_by="Architect Agent"
)
```

### Restoring Previous Versions

```python
# List versions
versions = mcp_archon_find_versions(
    project_id=archon_project_id,
    field_name="docs"
)

# Restore specific version
mcp_archon_manage_version(
    action="restore",
    project_id=archon_project_id,
    field_name="docs",
    version_number=3
)
```

## Best Practices

### 1. Always Research First
- Search knowledge base before implementing
- Find code examples for patterns
- Read full pages for detailed context

### 2. Keep Queries Focused
- Use 2-5 keywords only
- Avoid long sentences
- Multiple short queries > one long query

### 3. Link to OpenProject
- Include OpenProject IDs in documents
- Tag documents with epic/story references
- Maintain traceability

### 4. Use Consistent Tags
- Use lowercase, hyphenated tags
- Include document type in tags
- Tag with related OpenProject items

### 5. Version Important Documents
- Create versions before major changes
- Document what changed in each version
- Use meaningful change summaries

