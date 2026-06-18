# Agent Generator Extension

Spec-kit extension for generating Copilot agents and skills from specifications.

## Installation

```bash
specify extension add agent-generator --from ./
```

## Commands Added

### `/speckit.generate-agent`

Generates a Copilot agent definition from a specification.

**Usage:**
```
/speckit.generate-agent Create an agent from specs/requirements/order-processing.md
```

**Options:**
- `--type <type>` - Output type: agent, skill, both (default: both)
- `--output <path>` - Output directory (default: .github/agents/)
- `--name <name>` - Override generated name

## How It Works

1. Parses input specification
2. Extracts purpose, triggers, rules, and workflow
3. Generates agent definition following enterprise patterns
4. Creates associated skill if applicable
5. Adds reference documentation

## Output Structure

### Agent (`.github/agents/{name}.md`)
```markdown
---
name: {name}
description: "{description}. WHEN: {triggers}"
---
# {Name}
## Triggers
## Workflow
## Rules
```

### Skill (`.copilot/skills/{name}/SKILL.md`)
```markdown
---
name: {name}
description: "{description}"
---
# {Name}
## Triggers
## Rules
## Workflow
```

## Naming Conventions

- Agents: `{domain}-{function}` (e.g., `order-validator`)
- Skills: `{action}-{target}` (e.g., `validate-order`)

## Integration

Works with:
- `@spec-to-agent` agent for interactive generation
- `@spec-validator` for pre-generation validation
- Enterprise preset for standards compliance
