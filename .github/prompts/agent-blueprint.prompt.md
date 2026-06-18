---
description: "Creates standardized Copilot agent and skill definitions from specifications."
---

# Agent Blueprint Generator

You are creating a Copilot agent or skill from a specification. The output should follow enterprise patterns and be immediately usable.

## Agent Template

```markdown
---
name: {kebab-case-name}
description: "{One sentence with trigger phrases}. WHEN: {trigger1}, {trigger2}, {trigger3}."
---

# {Display Name}

> **PURPOSE**: {Single sentence from spec overview}

## Triggers

Activate this agent when user wants to:
- {Action derived from user stories}
- {Action derived from user stories}

## Workflow

### Phase 1: {Phase Name}
{Steps derived from spec process flows}

### Phase 2: {Phase Name}
{Steps derived from spec process flows}

## Rules

1. **{Rule Name}** - {From spec business rules}
2. **{Rule Name}** - {From spec constraints}

## Output

{Format and location of outputs}

## Integration

- Depends on: {From spec dependencies}
- Used by: {Related agents/skills}
```

## Skill Template

```markdown
---
name: {skill-name}
description: "{Description with triggers}"
license: MIT
metadata:
  author: {Organization}
  version: "1.0.0"
---

# {Skill Name}

## Triggers
{From spec user stories}

## Rules
{From spec business rules and constraints}

## Workflow
{From spec process flows}

## References
- [context.md](references/context.md) - Domain background
- [patterns.md](references/patterns.md) - Usage patterns
```

## Naming Conventions

### Agents
- Format: `{domain}-{function}`
- Examples: `order-validator`, `inventory-checker`, `customer-onboarding`

### Skills
- Format: `{action}-{target}` or `{domain}-{capability}`
- Examples: `validate-order`, `check-inventory`, `customer-lookup`

### Prompts
- Format: `{action}-{target}.prompt.md`
- Examples: `analyze-code.prompt.md`, `generate-report.prompt.md`

## Mapping Guide

| Spec Section | → | Agent/Skill Section |
|--------------|---|---------------------|
| Overview | → | PURPOSE / description |
| User Stories | → | Triggers |
| Business Rules | → | Rules |
| Process Flows | → | Workflow |
| Constraints | → | Rules |
| Data Model | → | References |
| Success Criteria | → | Output expectations |

## Quality Checklist

- [ ] Name follows conventions
- [ ] Description includes WHEN triggers
- [ ] All spec requirements mapped
- [ ] Workflow is complete and actionable
- [ ] Rules are specific and enforceable
- [ ] Output format is defined
