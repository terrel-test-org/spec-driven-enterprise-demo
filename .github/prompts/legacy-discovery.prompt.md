---
description: "Analyzes legacy code to discover and document implicit business rules, data flows, and system behaviors."
---

# Legacy Code Discovery

You are analyzing a legacy codebase to extract specifications. Your goal is to understand WHAT the code does (behavior) without being distracted by HOW it does it (implementation).

## Analysis Approach

1. **Start with entry points** - Find main functions, API endpoints, CLI handlers
2. **Trace data flows** - Follow data from input through processing to output
3. **Identify decision points** - Look for if/else, switch, validation logic
4. **Note magic values** - Constants, thresholds, limits that encode business rules
5. **Map state transitions** - Status fields, workflow stages, lifecycle events

## What to Extract

### Business Rules
Look for:
- Validation logic ("if X then reject")
- Calculation formulas ("total = subtotal * rate")
- Conditional processing ("orders over $10K need approval")
- Status transitions ("can only cancel if pending")

### Data Relationships
Look for:
- Foreign keys and joins
- Parent-child relationships
- Many-to-many associations
- Denormalized duplications

### External Dependencies
Look for:
- API calls
- File I/O
- Database connections
- Message queues

## Output Format

For each discovered component, document:

```markdown
## [Component Name]

### Purpose
[One sentence describing what this does]

### Business Rules
1. [Rule]: [Condition] → [Action]
2. [Rule]: [Condition] → [Action]

### Data
- Input: [what it receives]
- Output: [what it produces]
- Storage: [where data persists]

### Dependencies
- [External system/service]

### Observations
- [Technical debt, issues, concerns]
```

## Focus Areas

- **Don't fix the code** - Just document what it does
- **Flag inconsistencies** - Note conflicting logic
- **Preserve intent** - Even if implementation is wrong
- **Reference sources** - Include file:line for traceability
