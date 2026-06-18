# Micron Standards Preset

Enterprise preset for Spec-Driven Development that enforces organizational standards.

## Installation

```bash
specify preset add micron-standards --from ./
```

## What This Preset Does

This preset customizes spec-kit's core workflows to enforce Micron enterprise standards:

1. **Specification Templates** - Adds required sections for compliance
2. **Validation Rules** - Enforces constitution requirements  
3. **Output Formats** - Standardizes artifact structure
4. **Integration Checks** - Validates against existing systems

## Customizations

### Modified Commands

| Command | Customization |
|---------|--------------|
| `/speckit.specify` | Adds compliance sections to spec template |
| `/speckit.plan` | Includes security and performance requirements |
| `/speckit.tasks` | Adds validation tasks before implementation |

### Added Validations

- Security considerations required
- Performance targets required
- Error handling documentation required
- Cross-reference checking enabled

## Template Overrides

Templates in `templates/` override spec-kit defaults:

- `specify.md` - Specification template with enterprise sections
- `plan.md` - Implementation plan with governance gates

## Usage

After installation, all spec-kit commands automatically apply these standards:

```bash
# Creates spec with enterprise-required sections
/speckit.specify Build an order management system

# Plan includes security review gate
/speckit.plan Use Python with FastAPI, PostgreSQL database

# Tasks include validation checkpoints
/speckit.tasks
```

## Compatibility

- Spec-Kit: v0.5.0+
- Integrations: All supported agents
