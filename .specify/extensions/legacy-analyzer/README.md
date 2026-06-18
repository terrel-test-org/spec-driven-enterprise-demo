# Legacy Analyzer Extension

Spec-kit extension that adds legacy code analysis capabilities.

## Installation

```bash
specify extension add legacy-analyzer --from ./
```

## Commands Added

### `/speckit.legacy-analyze`

Analyzes legacy codebases to extract specifications.

**Usage:**
```
/speckit.legacy-analyze Analyze the src/ folder focusing on order processing logic
```

**Options:**
- `--focus <area>` - Focus on specific area (business-rules, data-model, flows)
- `--language <lang>` - Filter by language (python, java, all)
- `--output <path>` - Output directory for specs (default: specs/requirements/)

## How It Works

1. Scans codebase structure and identifies components
2. Extracts business rules from validation and decision logic
3. Maps data models from database schemas and entities
4. Documents process flows from entry points
5. Generates specification documents

## Output

Generates to `specs/requirements/{component}.md`:

```markdown
# {Component} Specification

## Overview
{Extracted description}

## Business Rules
{Rules with source references}

## Data Model
{Entities and relationships}

## Technical Debt
{Issues discovered}
```

## Integration

Works with:
- `@spec-analyzer` agent for interactive analysis
- `spec-governance` skill for validation
- `/speckit.plan` for modernization planning
