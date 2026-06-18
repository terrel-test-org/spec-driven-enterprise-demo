# SDD Instructions Extension

> Global instructions for Spec-Driven Development workflows.
> These instructions are injected into all agent contexts.

## When to Use Spec-Driven Development

Use SDD for:
- New feature development
- Legacy system modernization  
- Cross-team standardization
- Any work requiring formal documentation

## SDD Workflow Overview

```
1. /speckit.constitution  → Establish principles (once per project)
2. /speckit.specify       → Define WHAT you're building
3. /speckit.clarify       → Fill gaps in requirements
4. /speckit.plan          → Define HOW to build it
5. /speckit.tasks         → Create actionable work items
6. /speckit.implement     → Execute the plan
7. /speckit.converge      → Verify completion
```

## Agent Integration

### For Legacy Modernization
1. Use `@spec-analyzer` to extract specs from existing code
2. Use `@spec-validator` to validate extracted specs
3. Use `/speckit.plan` to create modernization plan
4. Use `/speckit.implement` to execute

### For New Development
1. Use `/speckit.constitution` to set standards
2. Use `/speckit.specify` to define requirements
3. Use `@spec-validator` to check compliance
4. Use `/speckit.plan` and `/speckit.tasks`
5. Use `/speckit.implement` to build

### For Agent/Skill Creation
1. Create specification for the agent's purpose
2. Use `@spec-to-agent` to generate agent definition
3. Use `@spec-validator` to check against standards
4. Deploy to `.github/agents/` or `.copilot/skills/`

## Key Principles

1. **Spec Before Code** - Always have a spec before implementation
2. **Validate Early** - Check specs before starting work
3. **Iterate on Specs** - Update specs as understanding grows
4. **Trace Everything** - Link code back to spec requirements
