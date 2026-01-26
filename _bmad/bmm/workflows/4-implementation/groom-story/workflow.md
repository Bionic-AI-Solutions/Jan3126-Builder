# BMAD BMM Workflow: groom-story

**Workflow Type:** Story Grooming  
**Agent:** PM (Product Manager), with Dev Team and Test Team  
**Phase:** Pre-Implementation  
**Status:** MANDATORY WORKFLOW

## Purpose

Groom a story by breaking it down into implementable tasks and creating them in OpenProject BEFORE implementation begins. This is a mandatory agile practice that must be completed before the story moves to "In progress".

**CRITICAL:** If the Story is in "In specification" status, ensure all required specification artifacts are attached before requesting transition to "Specified" status. Scrum Master (SM) will verify artifacts before allowing the transition.

---

## RACI Matrix

| Activity | PM | SM | Dev | TEA | Architect |
|----------|----|----|-----|-----|-----------|
| Story Review | R | I | C | C | C |
| Development Task Creation | C | A | R | I | C |
| Test Task Creation | I | A | I | R | I |
| Task Verification | I | R/A | C | C | I |
| Artifact Attachment | R | A | I | I | I |
| Status Transition Approval | I | R/A | I | I | I |

**Legend:** R = Responsible, A = Accountable, C = Consulted, I = Informed

### Key RACI Notes

- **Dev Team** is Responsible for creating development/implementation tasks
- **Test Team (TEA)** is Responsible for creating the MANDATORY test task (Task X.Y.T)
- **SM** is Accountable for ensuring ALL tasks are created before story moves to "In progress"
- **PM** is Responsible for story review and artifact attachment
- **SM** must verify test task exists before approving story for development

### Task Creation Responsibilities

| Task Type | Created By | Verified By | Notes |
|-----------|------------|-------------|-------|
| Development Tasks | Dev Team | SM | Implementation work for acceptance criteria |
| Test Task (X.Y.T) | Test Team | SM | MANDATORY - Story cannot close without this |
| Bug Fix Tasks | Dev Team | SM | Created during bug-management workflow |
| Review Follow-up Tasks | Dev Team | SM | Created during code-review workflow |

**CRITICAL:** 
- Test task MUST be created by Test Team during grooming
- SM MUST verify test task exists before allowing story to move to "In progress"
- Story CANNOT be closed until test task is completed and closed

---

## Workflow Steps

### Step 1: Review Story

1. Get story from OpenProject
2. Review acceptance criteria
3. Identify all tasks needed to complete the story
4. Ensure tasks are granular (30 min - 4 hours of work)
5. Map each task to specific acceptance criteria

### Step 2: Create Story File

1. Create story file in `_bmad-output/implementation-artifacts/`
2. Include all acceptance criteria
3. Break down into tasks with subtasks
4. Map each task to specific acceptance criteria

### Step 3: Attach Specification Artifacts (if Story is "In specification")

**CRITICAL:** If Story is in "In specification" status, ensure all required artifacts are attached:

1. ✅ **Acceptance Criteria** - Complete in Story description or as attached document
2. ✅ **UI Mocks/Designs** (if Story includes UI) - Attach UI mockups (images: PNG, JPG, SVG, or design files)
3. ✅ **Technical Specifications** (if Story requires technical details) - Attach technical spec document

**Protocol:** After attaching artifacts, request Scrum Master (SM) to verify and approve transition to "Specified" status. SM will use `mcp_openproject_list_work_package_attachments()` to verify artifacts.

### Step 4: Create Development Tasks in OpenProject (Dev Team)

**Owner:** Dev Team  
**Verified By:** SM

**CRITICAL:** Development tasks MUST be created in OpenProject during grooming, before story moves to "In progress".

**⚠️ DUPLICATE PREVENTION:** Always check for existing tasks (including closed ones) before creating new tasks.

```python
# Step 4.1: Check for existing tasks (CRITICAL - prevents duplicates)
def check_existing_tasks(story_id: int) -> list[dict]:
    """
    Check for existing tasks for a story, including closed tasks.
    CRITICAL: Use status="all" to include closed tasks.
    """
    children = mcp_openproject_get_work_package_children(
        parent_id=story_id,
        status="all"  # Include closed tasks - CRITICAL!
    )
    return children.get("children", [])

# Get existing tasks
existing = check_existing_tasks(story_id)
existing_subjects = {t["subject"] for t in existing}

# Step 4.2: Define development tasks needed for the story
# These are created by Dev Team during grooming
dev_tasks = [
    {
        "subject": "Task 1: [Task Title]",
        "type_id": 36,  # Task
        "description": """
        **Implementation Task**
        
        **Acceptance Criteria Mapping:**
        - AC 1: [How this task satisfies AC 1]
        - AC 2: [How this task satisfies AC 2]
        
        **Estimated Effort:** [30 min - 4 hours]
        
        **Implementation Notes:**
        - [Technical approach]
        - [Dependencies]
        """,
    },
    # ... all other implementation tasks
]

# Step 4.3: Filter out duplicates
new_dev_tasks = [
    t for t in dev_tasks
    if t["subject"] not in existing_subjects
]

if new_dev_tasks:
    # Step 4.4: Bulk create development tasks
    result = mcp_openproject_bulk_create_work_packages(
        project_id={config.openproject.project_id},
        work_packages=json.dumps(new_dev_tasks),
        continue_on_error=True
    )
    
    # Step 4.5: Set parent relationships
    for task in result.get("created", []):
        mcp_openproject_set_work_package_parent(
            work_package_id=task["id"],
            parent_id=story_id
        )
```

### Step 5: Create Test Task in OpenProject (Test Team)

**Owner:** Test Team (TEA)  
**Verified By:** SM

**CRITICAL:** Test task is MANDATORY. Story CANNOT be closed without test task completed.

```python
# Check if test task already exists
test_task_exists = any("Task" in t["subject"] and "T:" in t["subject"] and "Testing" in t["subject"] for t in existing)

if not test_task_exists:
    # Test Team creates the MANDATORY test task
    test_task = {
        "subject": "Task X.Y.T: Story X.Y Testing and Validation",  # MANDATORY Test task
        "type_id": {config.openproject.types.task},
        "description": """
        **MANDATORY Test Task for Story X.Y**
        
        **Owner:** Test Team (TEA)
        
        **CRITICAL:** This test task MUST be completed and closed before the Story can be closed.
        
        **Activities:**
        1. Create Story test document: `story-X-Y-test-plan.md`
        2. Attach test document to Story X.Y
        3. Validate all acceptance criteria
        4. Run unit tests (verify Dev created them)
        5. Run integration tests
        6. Verify implementation works as expected
        7. Verify code follows architecture patterns
        8. Verify error handling works correctly
        9. Verify documentation is updated
        
        **Test Document Template:**
        - Test scenarios for each acceptance criterion
        - Expected vs actual results
        - Pass/fail status
        - Bug references (if any)
        
        **Subtasks (if needed):**
        - [ ] Create test plan document
        - [ ] Execute unit test verification
        - [ ] Execute integration tests
        - [ ] Document test results
        - [ ] Attach test document to story
        """,
        "status_id": {config.openproject.statuses.new},
        "priority_id": {config.openproject.priorities.high}  # High priority - required for story closure
    }
    
    # Create test task
    result = mcp_openproject_create_work_package(
        project_id={config.openproject.project_id},
        subject=test_task["subject"],
        type_id=test_task["type_id"],
        description=test_task["description"],
        status_id=test_task["status_id"],
        priority_id=test_task["priority_id"]
    )
    
    # Set parent relationship
    mcp_openproject_set_work_package_parent(
        work_package_id=result["work_package"]["id"],
        parent_id=story_id
    )
    
    print(f"✅ Test task created: {test_task['subject']}")
else:
    print(f"✅ Test task already exists for story {story_id}")
```

### Step 6: SM Verifies All Tasks Created

**Owner:** SM (Scrum Master)

**CRITICAL:** SM must verify ALL tasks exist before story can move to "In progress".

```python
def sm_verify_story_tasks(story_id: int) -> tuple[bool, str]:
    """
    SM verification of story tasks before allowing "In progress" status.
    Returns (is_valid, message)
    """
    # Get all tasks for story
    children = mcp_openproject_get_work_package_children(
        parent_id=story_id,
        status="all"
    )
    tasks = [c for c in children.get("children", []) if c["type"] == "Task"]
    
    # Check 1: Any tasks exist?
    if not tasks:
        return False, "❌ BLOCKED: No tasks found. Dev Team must create development tasks."
    
    # Check 2: Test task exists? (MANDATORY)
    test_task = next((t for t in tasks if "T:" in t["subject"] and "Testing" in t["subject"]), None)
    if not test_task:
        return False, "❌ BLOCKED: Test task (Task X.Y.T) missing. Test Team must create test task."
    
    # Check 3: Development tasks exist?
    dev_tasks = [t for t in tasks if t["id"] != test_task.get("id")]
    if not dev_tasks:
        return False, "⚠️ WARNING: No development tasks found. Dev Team should create implementation tasks."
    
    # Check 4: All tasks have descriptions?
    tasks_without_desc = [t for t in tasks if not t.get("description")]
    if tasks_without_desc:
        return False, f"⚠️ WARNING: {len(tasks_without_desc)} tasks missing descriptions."
    
    return True, f"✅ VERIFIED: {len(dev_tasks)} development tasks + 1 test task found."

# SM runs verification
is_valid, message = sm_verify_story_tasks(story_id)
print(message)

if not is_valid and "BLOCKED" in message:
    raise ValueError(f"Cannot proceed: {message}")
```

**SM Verification Checklist:**

- [ ] Development tasks created by Dev Team
- [ ] **Test task (Task X.Y.T) created by Test Team - MANDATORY**
- [ ] All tasks linked to story (parent relationship)
- [ ] Task descriptions include acceptance criteria mapping
- [ ] Tasks are granular (30 min - 4 hours)

### Step 7: Update Story Status

**Owner:** SM (after verification)

**ONLY after SM verifies all tasks are created:**

```python
# SM approves story for development
mcp_openproject_update_work_package(
    work_package_id=story_id,
    status_id={config.openproject.statuses.in_progress}  # Use config, not hardcoded ID
)

# Add comment documenting approval
mcp_openproject_add_work_package_comment(
    work_package_id=story_id,
    comment=f"""
    ✅ **Story Grooming Complete - SM Approved**
    
    **Tasks Created:**
    - Development Tasks: {len(dev_tasks)}
    - Test Task: ✅ Present
    
    **Ready for Development**
    
    Story is now "In progress". Dev can begin implementation.
    """
)
```

## Checklist

### PM Checklist (Story Review & Artifacts)

- [ ] Story acceptance criteria reviewed
- [ ] Story file created with all tasks
- [ ] **If Story is "In specification": All required artifacts attached (Acceptance Criteria, UI Mocks if UI, Technical Specs if required)**

### Dev Team Checklist (Development Tasks)

- [ ] **Checked for existing tasks (including closed) - prevents duplicates**
- [ ] Development tasks created in OpenProject
- [ ] Tasks map to acceptance criteria
- [ ] Tasks are granular (30 min - 4 hours)
- [ ] Task descriptions include implementation notes

### Test Team Checklist (Test Task)

- [ ] **MANDATORY: Test task (Task X.Y.T) created**
- [ ] Test task includes test plan activities
- [ ] Test task has subtasks for test document creation

### SM Checklist (Verification & Approval)

- [ ] **Verified development tasks exist** (created by Dev Team)
- [ ] **Verified test task (Task X.Y.T) exists** (created by Test Team) - MANDATORY
- [ ] All tasks linked to story (parent relationship)
- [ ] Task descriptions are complete
- [ ] **If Story is "In specification": Verified artifacts and approved transition to "Specified"**
- [ ] **Approved story to move to "In progress"**

---

**CRITICAL:** 
- Test task (Task X.Y.T) is MANDATORY and must be created by Test Team
- SM must verify test task exists before approving story for development
- Story CANNOT be closed until test task is completed and closed
- This is enforced by the `update_story_status_based_on_tasks()` helper function in `epic-story-lifecycle`

## Outputs

1. Story file in `_bmad-output/implementation-artifacts/`
2. All tasks created in OpenProject
3. Story marked as "In progress" (ready for Dev)

## Integration with Other Workflows

### Upstream Workflows (call groom-story)

- **create-story:** Creates story, then calls groom-story
- **sprint-planning:** Grooms stories for sprint, creates tasks

### Downstream Workflows (depend on groom-story)

- **dev-story:** Verifies tasks exist before starting implementation
  - Will HALT if no tasks found
  - Will WARN if test task missing
  - References groom-story for task creation
- **test-validation:** Validates test task completion before story closure
  - Enforces test task requirement
  - Creates bugs for validation failures

### Workflow Chain

```
create-story → groom-story → dev-story → test-validation → story closure
                    ↓
              [SM Verification Gate]
              - Dev tasks exist?
              - Test task exists?
              - Artifacts attached?
```

## References

- **Epic-Story Lifecycle:** `@bmad/bmm/workflows/epic-story-lifecycle` - Complete lifecycle, status transitions, and helper functions
- **Dev Story:** `@bmad/bmm/workflows/dev-story` - Story implementation (expects groom-story completed)
- **Test Validation:** `@bmad/bmm/workflows/test-validation` - Story validation and closure
- **PM Agent:** `@bmad/bmm/agents/pm` - Product Manager agent for story grooming
- **SM Agent:** `@bmad/bmm/agents/sm` - Scrum Master agent for verification
