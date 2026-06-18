---
description: "Transforms extracted business rules and system behaviors into formal, executable specifications."
---

# Specification Generation

You are creating a formal specification from analyzed code or requirements. The spec should be complete enough that an AI coding agent can implement it without referring to the original code.

## Specification Structure

```markdown
# [Feature/Component Name]

## Overview
[2-3 sentences describing the purpose and value]

## User Stories

### [Story ID]: [Title]
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Testable criterion]
- [ ] [Testable criterion]

## Business Rules

### BR-001: [Rule Name]
- **Trigger**: [When this rule applies]
- **Condition**: [What must be true]
- **Action**: [What happens]
- **Exception**: [Edge cases]

## Data Model

### [Entity Name]
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| field_name | string | Yes | Description |

### Relationships
- [Entity A] has many [Entity B]
- [Entity C] belongs to [Entity D]

## Process Flows

### [Process Name]
1. [Step with actor and action]
2. [Step with decision point]
   - If [condition]: [action]
   - Else: [action]
3. [Completion step]

## Constraints

### Performance
- Response time: [target]
- Throughput: [target]

### Security
- Authentication: [requirement]
- Authorization: [requirement]

### Compliance
- [Regulatory requirement]

## Success Criteria

- [ ] [Measurable outcome]
- [ ] [Measurable outcome]
```

## Writing Guidelines

1. **Be Specific** - Avoid "should", "might", "could"
2. **Be Measurable** - Include numbers where possible
3. **Be Complete** - Cover happy path AND edge cases
4. **Be Testable** - Every requirement should be verifiable
5. **Be Consistent** - Use same terms throughout

## Quality Checklist

Before finalizing, verify:
- [ ] No ambiguous language
- [ ] All acronyms defined
- [ ] Cross-references are valid
- [ ] Edge cases documented
- [ ] Error handling specified
- [ ] Success criteria are measurable
