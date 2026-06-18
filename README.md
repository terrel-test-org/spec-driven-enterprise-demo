# Spec-Driven Development Enterprise Demo

[![Spec-Kit](https://img.shields.io/badge/Spec--Kit-Enabled-blue)](https://github.com/github/spec-kit)
[![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Agents%20%26%20Skills-green)](https://github.com/features/copilot)

> **Demo**: How enterprises can standardize AI coding agents and skills using Spec-Driven Development.

## 🎯 What This Demo Shows

This repository demonstrates how **Spec-Driven Development (SDD)** can help enterprises:

1. **Extract specifications from legacy code** — Turn undocumented systems into formal specs
2. **Standardize agent/skill creation** — Generate consistent Copilot agents from specs
3. **Enforce enterprise governance** — Validate all work against organizational standards
4. **Enable reusability at scale** — Share patterns across teams via presets and extensions

## 🏗️ Repository Structure

```
├── .github/
│   ├── agents/                    # Custom Copilot agents
│   │   ├── spec-analyzer.md       # Extracts specs from legacy code
│   │   ├── spec-validator.md      # Validates specs against standards
│   │   └── spec-to-agent.md       # Generates agents from specs
│   ├── extensions/
│   │   └── sdd-instructions.md    # SDD workflow guidance
│   └── prompts/                   # Reusable prompt templates
│       ├── legacy-discovery.prompt.md
│       ├── spec-generation.prompt.md
│       └── agent-blueprint.prompt.md
│
├── .specify/                      # Spec-kit configuration
│   ├── presets/
│   │   └── micron-standards/      # Enterprise preset
│   └── extensions/                # Custom spec-kit commands
│
├── .copilot/
│   └── skills/                    # Custom Copilot skills
│       ├── legacy-spec-extractor/ # Extract specs from code
│       └── spec-governance/       # Validate spec compliance
│
├── legacy-app/                    # Sample legacy application
│   ├── python-services/           # Python backend (orders, inventory)
│   └── java-api/                  # Java REST API
│
└── specs/                         # Generated specifications
    ├── constitution.md            # Enterprise principles
    ├── requirements/              # Feature specs
    └── plans/                     # Implementation plans
```

## 🚀 Getting Started

### Prerequisites

1. **GitHub Copilot** — With agent support enabled
2. **Spec-Kit CLI** — Install via [spec-kit instructions](https://github.com/github/spec-kit#-get-started)

```bash
# Install spec-kit
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@latest

# Initialize in this repo
specify init . --integration copilot
```

### Quick Demo

#### Demo 1: Extract Specs from Legacy Code

```
@spec-analyzer Analyze the legacy-app/python-services folder and extract 
specifications for the order processing system. Focus on business rules 
around order validation, pricing, and status management.
```

#### Demo 2: Validate Against Enterprise Standards

```
@spec-validator Validate the extracted specifications against our 
enterprise constitution in specs/constitution.md
```

#### Demo 3: Generate Agent from Spec

```
@spec-to-agent Create a new Copilot agent from the order processing 
specification, following our enterprise agent patterns.
```

## 📋 Demo Scenarios

### Scenario 1: Legacy Code → Specification

**Problem**: Legacy Python/Java order system with no documentation.

**Solution**: 
1. Use `@spec-analyzer` to scan the codebase
2. Extract business rules (order limits, pricing, status flows)
3. Generate formal specification documents
4. Identify technical debt and security issues

### Scenario 2: Specification → Agent/Skill

**Problem**: Need consistent agents across global engineering teams.

**Solution**:
1. Start with validated specification
2. Use `@spec-to-agent` to generate standardized agent
3. Automatically create associated skills
4. Ensure compliance with enterprise patterns

### Scenario 3: Enterprise Governance

**Problem**: Need audit trails and compliance verification.

**Solution**:
1. Define standards in `specs/constitution.md`
2. Use `@spec-validator` for pre-implementation checks
3. Validate specs meet security, performance, and quality requirements
4. Generate compliance reports

## 📚 Key Components

### Custom Agents

| Agent | Purpose |
|-------|---------|
| `@spec-analyzer` | Extracts specifications from existing code |
| `@spec-validator` | Validates specs against enterprise standards |
| `@spec-to-agent` | Generates agents/skills from specifications |

### Custom Skills

| Skill | Purpose |
|-------|---------|
| `legacy-spec-extractor` | Detailed legacy code analysis |
| `spec-governance` | Compliance validation and reporting |

### Enterprise Preset

The `micron-standards` preset enforces:
- Required specification sections
- Security and performance documentation
- Governance gates in implementation plans
- Standardized output formats

## 🎓 Enterprise Adoption Guide

### Phase 1: Pilot
1. Select 1-2 teams for pilot
2. Install spec-kit and custom agents
3. Apply to one legacy modernization project
4. Gather feedback and refine

### Phase 2: Standardization  
1. Create organization-specific preset
2. Define constitution with architecture team
3. Train teams on SDD workflow
4. Establish governance process

### Phase 3: Scale
1. Deploy preset org-wide
2. Create team-specific extensions
3. Build agent/skill catalog
4. Measure adoption and quality metrics

## 📖 Resources

- [Spec-Kit Documentation](https://github.com/github/spec-kit)
- [Spec-Kit Video Overview](https://www.youtube.com/watch?v=a9eR1xsfvHg)
- [GitHub Copilot Agents](https://docs.github.com/en/copilot)
- [Enterprise Constitution](specs/constitution.md)

## 🤝 Contributing

This is a demo repository. For questions or feedback, please open an issue.

---

*Built for demonstrating Spec-Driven Development at enterprise scale.*
