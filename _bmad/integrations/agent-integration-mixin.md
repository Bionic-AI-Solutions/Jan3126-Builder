# Agent Integration Mixin

This file defines the standard integration capabilities that ALL BMAD agents should have. When activated, agents should load this mixin in addition to their persona.

## Integration Activation Block

Add this to the agent activation sequence after loading the base persona:

```xml
<integration-activation critical="MANDATORY">
  <step n="I1">Load project configuration from {project-root}/_bmad/_config/project-config.yaml</step>
  <step n="I2">Store integration settings:
    - openproject_project_id = {config.openproject.project_id}
    - archon_project_id = {config.archon.project_id}
    - types = {config.openproject.types}
    - statuses = {config.openproject.statuses}
    - priorities = {config.openproject.priorities}
  </step>
  <step n="I3">If openproject.enabled=true, verify OpenProject MCP is available</step>
  <step n="I4">If archon.enabled=true, verify Archon MCP is available</step>
</integration-activation>
```

## Standard Integration Capabilities

### OpenProject Capabilities

All agents have access to these OpenProject operations:

```yaml
openproject_capabilities:
  query:
    - list_work_packages: "Get open/closed work packages"
    - get_work_package: "Get specific work package details"
    - search_work_packages: "Search by subject"
    - get_work_package_children: "Get child items"
    - get_work_package_hierarchy: "Get full hierarchy"

  create:
    - create_work_package: "Create epic/feature/story/task"
    - set_work_package_parent: "Set parent relationship"
    - add_work_package_comment: "Add comments"

  update:
    - update_work_package: "Update any field"
    - update_work_package_status: "Change status with comment"
    - assign_work_package: "Assign to user"
    - log_time: "Log time entry"
```

### Archon Capabilities

All agents have access to these Archon operations:

```yaml
archon_capabilities:
  search:
    - rag_search_knowledge_base: "Search all knowledge"
    - rag_search_code_examples: "Find code examples"
    - rag_read_full_page: "Read complete page"
    - rag_get_available_sources: "List knowledge sources"
    - rag_list_pages_for_source: "Browse source structure"

  documents:
    - find_documents: "List/search documents"
    - manage_document_create: "Create new document"
    - manage_document_update: "Update existing document"

  versions:
    - find_versions: "List version history"
    - manage_version_create: "Create version snapshot"
```

## Agent-Specific Integration Behaviors

### PM Agent Integration

```yaml
pm_integration:
  primary_actions:
    - Create Epics from product brief
    - Create User Stories from PRD with full acceptance criteria
    - Store product briefs in Archon
    - Store PRDs in Archon
    - Link Archon documents to OpenProject work packages

  workflow_triggers:
    - "[PR] Create PRD" → Store in Archon + Create OpenProject structure
    - "[ES] Create Epics/Stories" → Create in OpenProject from Archon PRD
    - "[IR] Implementation Readiness" → Query OpenProject + Archon
```

### Dev Agent Integration

```yaml
dev_integration:
  primary_actions:
    - Query assigned tasks from OpenProject
    - Update task status in OpenProject
    - Search Archon knowledge before implementing
    - Log time against work packages
    - Document implementation decisions in Archon

  workflow_triggers:
    - Start task → Update OpenProject status to In Progress
    - Implementation → Search Archon for patterns/examples
    - Complete task → Update OpenProject status to In Testing/Closed
```

### Architect Agent Integration

```yaml
architect_integration:
  primary_actions:
    - Create technical specifications in Archon
    - Create architecture work packages in OpenProject
    - Create ADRs in Archon with OpenProject links
    - Research existing patterns in Archon

  workflow_triggers:
    - "[CA] Create Architecture" → Store in Archon + Create tech tasks in OpenProject
    - Technical decision → Create ADR in Archon
```

### SM Agent Integration

```yaml
sm_integration:
  primary_actions:
    - Sprint planning using OpenProject
    - Status reporting from OpenProject
    - Blocker tracking in OpenProject

  workflow_triggers:
    - "[SP] Sprint Planning" → Query/update OpenProject
    - "[SS] Sprint Status" → Generate report from OpenProject
```

### TEA Agent Integration

```yaml
tea_integration:
  primary_actions:
    - Create test work packages in OpenProject
    - Document test strategies in Archon
    - Update test status in OpenProject
    - Research test patterns in Archon

  workflow_triggers:
    - Test planning → Search Archon for patterns
    - Test creation → Create work packages in OpenProject
    - Test execution → Update status in OpenProject
```

## Integration Menu Items

Add these menu items to all agents:

```xml
<integration-menu>
  <item cmd="OPW or fuzzy match on openproject-work">[OPW] Show OpenProject Work Packages</item>
  <item cmd="OPC or fuzzy match on openproject-create">[OPC] Create OpenProject Work Package</item>
  <item cmd="AKS or fuzzy match on archon-search">[AKS] Search Archon Knowledge Base</item>
  <item cmd="AKD or fuzzy match on archon-document">[AKD] Create/Update Archon Document</item>
</integration-menu>
```

## Integration Handlers

```xml
<integration-handlers>
  <handler cmd="OPW">
    Execute: mcp_openproject_list_work_packages(project_id={openproject_project_id}, status="open")
    Display: Formatted list of work packages with status
  </handler>

  <handler cmd="OPC">
    Ask: Work package type (Epic/Feature/Story/Task)
    Ask: Subject and description
    Execute: mcp_openproject_create_work_package(project_id={openproject_project_id}, type_id=..., subject=..., description=...)
  </handler>

  <handler cmd="AKS">
    Ask: Search query (remind: 2-5 keywords)
    Execute: mcp_archon_rag_search_knowledge_base(query=..., match_count=5)
    Display: Search results with snippets
    Offer: Read full page for any result
  </handler>

  <handler cmd="AKD">
    Ask: Document title and type (spec/design/note/api/guide)
    Ask: Content (markdown)
    Execute: mcp_archon_manage_document(action="create", project_id={archon_project_id}, title=..., document_type=..., content={markdown: ...})
  </handler>
</integration-handlers>
```

## Configuration Reference

All settings come from `_bmad/_config/project-config.yaml`:

| Setting Path                       | Description                 |
| ---------------------------------- | --------------------------- |
| `openproject.project_id`           | OpenProject project ID      |
| `openproject.types.epic`           | Epic type ID                |
| `openproject.types.feature`        | Feature type ID             |
| `openproject.types.user_story`     | User Story type ID          |
| `openproject.types.task`           | Task type ID                |
| `openproject.statuses.new`         | New status ID               |
| `openproject.statuses.in_progress` | In Progress status ID       |
| `openproject.statuses.in_testing`  | In Testing status ID        |
| `openproject.statuses.closed`      | Closed status ID            |
| `archon.project_id`                | Archon project UUID         |
| `archon.rag.default_match_count`   | Default search result count |

## Usage Example

When an agent activates:

```
1. Load base persona (pm.md, dev.md, etc.)
2. Load integration mixin (this file)
3. Read project-config.yaml
4. Store config values for use in workflows
5. Display standard menu + integration menu items
6. Execute commands using configured IDs
```

When executing a workflow:

```
1. Check if integration is enabled in config
2. Use configured IDs for all MCP calls
3. Follow OpenProject-First rule for work management
4. Follow Research-First rule for implementation
5. Link Archon documents to OpenProject work packages
```
