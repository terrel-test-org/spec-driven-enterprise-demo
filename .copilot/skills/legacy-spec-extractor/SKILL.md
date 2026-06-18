---
name: legacy-spec-extractor
description: "Analyzes legacy codebases to extract formal specifications. Scans code to identify business rules, data flows, validation logic, and implicit requirements. WHEN: analyze legacy code, extract specs from code, document existing system, reverse engineer requirements, understand legacy application, prepare for modernization."
license: MIT
metadata:
  author: Enterprise Platform Team
  version: "1.0.0"
---

# Legacy Spec Extractor Skill

> Extract formal specifications from legacy codebases to enable Spec-Driven Development.

## Triggers

Activate this skill when:
- Analyzing existing/legacy code for modernization
- Extracting business rules from undocumented systems
- Creating specifications from existing implementations
- Documenting implicit requirements
- Preparing legacy code for refactoring

## Rules

1. **Document Behavior, Not Intent** - Extract what the code DOES, not what it SHOULD do
2. **Preserve Business Logic** - Business rules are valuable even if implementation is poor
3. **Flag Uncertainty** - Mark rules that seem inconsistent or incomplete
4. **Reference Sources** - Always include file and line number citations
5. **Separate Concerns** - Keep business rules distinct from technical implementation

## Workflow

### Step 1: Codebase Survey
- Identify languages, frameworks, and structure
- Locate entry points (main, APIs, CLI handlers)
- Map module dependencies
- Find configuration files

### Step 2: Business Logic Extraction
For each module, identify:
- Validation functions and rules
- Calculation/computation logic
- Decision trees and conditionals
- Status/state machines
- Error handling patterns

### Step 3: Data Model Discovery
- Database schemas and tables
- Entity relationships
- Constraints and validations
- Data transformations

### Step 4: Process Flow Mapping
- User-initiated workflows
- Background processes
- Integration points
- Event handlers

### Step 5: Specification Generation
Output formal specs following the template in [spec-template.md](references/spec-template.md)

## Output Format

Generate specifications to: `specs/requirements/{component-name}.md`

```markdown
# {Component} Specification

## Overview
[Extracted from code comments and behavior]

## Business Rules
| ID | Rule | Source | Confidence |
|----|------|--------|------------|
| BR-001 | [Rule description] | file.py:42 | High/Medium/Low |

## Data Model
[Entities, fields, relationships]

## Process Flows
[Step-by-step workflows]

## Technical Debt
[Issues discovered during analysis]
```

## References

- [spec-template.md](references/spec-template.md) - Output template
- [extraction-patterns.md](references/extraction-patterns.md) - Common patterns to look for
- [language-guides.md](references/language-guides.md) - Language-specific extraction tips
