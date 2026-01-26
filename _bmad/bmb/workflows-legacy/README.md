# Legacy Workflows

> **DEPRECATION NOTICE**: The workflows in this folder are deprecated and may be removed in a future version.

## Status

These workflows were part of earlier BMAD versions but have been superseded by newer implementations:

| Legacy Workflow | Replacement | Notes |
|-----------------|-------------|-------|
| `edit-module` | `@bmad/bmb/workflows/create-module` | Use create-module for module management |
| `module-brief` | `@bmad/bmb/workflows/create-module` | Module planning integrated into create-module |

## Migration

If you have been using these workflows, please migrate to the current versions:

1. **For module editing**: Use the `create-module` workflow which now includes edit capabilities
2. **For module planning**: The planning phase is integrated into `create-module` workflow

## Preservation

These workflows are preserved for:
- Reference of historical implementation patterns
- Backwards compatibility during transition period
- Documentation of original design approaches

## Do Not Use

These workflows do **NOT** have corresponding `.mdc` cursor rules and are not accessible through the standard BMAD invocation system.

---

*Last updated: 2026-01-25*
