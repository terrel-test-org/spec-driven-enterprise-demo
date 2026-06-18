# Demo Walkthrough: Spec-Driven Development for Enterprise

This guide walks through a complete demo showing how Spec-Driven Development (SDD) helps enterprises standardize AI coding agents while modernizing legacy code.

---

## Prerequisites

1. **GitHub Copilot** with agent support
2. **Spec-Kit CLI** installed:
   ```bash
   uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@latest
   ```
3. This repository cloned locally

---

## Demo Scenario: Legacy Order System Modernization

Your customer (Micron) has a legacy order processing system with:
- Python backend services (undocumented)
- Java API layer (minimal docs)
- Business rules embedded in code
- No formal specifications

**Goal**: Use SDD to extract specs, modernize the system, and create reusable agents.

---

## Part 1: Establish Enterprise Standards (5 min)

### 1.1 Review the Constitution

Open `specs/constitution.md` to show enterprise governance:

```
"Every significant development work begins with a specification."
```

**Key points to highlight:**
- Spec-first development
- Quality gates
- Agent/skill standards
- Governance requirements

### 1.2 Initialize Spec-Kit

```bash
cd spec-driven-enterprise-demo
specify init . --integration copilot
```

This sets up spec-kit with our enterprise preset.

---

## Part 2: Extract Specs from Legacy Code (10 min)

### 2.1 Show the Legacy Code Problem

Open `legacy-app/python-services/order_processor.py`:

```python
# Point out:
# - Magic numbers (MAX_ORDER_AMOUNT = 50000)
# - Undocumented business rules (if total > 10000: 'pending_approval')
# - Mixed concerns (business logic + data access)
```

### 2.2 Use the Spec Analyzer Agent

In Copilot chat:

```
@spec-analyzer Analyze the legacy-app/python-services folder and extract 
specifications for the order processing system. Focus on:
1. Order validation rules
2. Pricing and discount logic
3. Status transitions
4. Inventory checks
```

**Expected output:** Agent scans code and generates formal specification.

### 2.3 Review Extracted Specification

Show the generated spec:
- Business rules now documented with source references
- Data model extracted from database schema
- Process flows mapped from code
- Technical debt identified

---

## Part 3: Validate Against Enterprise Standards (5 min)

### 3.1 Run Spec Validator

```
@spec-validator Validate the extracted order processing specification 
against our enterprise constitution. Check for:
- Completeness
- Clarity
- Compliance
```

### 3.2 Review Validation Report

Show the validation output:
- ✅ Required sections present
- ⚠️ Missing security considerations
- ❌ Performance requirements not specified

### 3.3 Remediate Issues

Update spec to address findings, then re-validate.

---

## Part 4: Generate Agents from Specs (10 min)

### 4.1 Create Modernization Agent

```
@spec-to-agent Generate a Copilot agent from the order processing 
specification. The agent should help developers:
- Validate order requests
- Check business rules
- Ensure compliance
```

### 4.2 Review Generated Agent

Show `.github/agents/order-processor.md`:
- Proper frontmatter with triggers
- Workflow derived from spec
- Rules from business logic
- Integration points documented

### 4.3 Create Associated Skill

Show generated `.copilot/skills/order-validation/SKILL.md`:
- Follows enterprise skill pattern
- Includes references
- Ready for deployment

---

## Part 5: Enterprise Reusability (5 min)

### 5.1 Show Preset Mechanism

Open `.specify/presets/micron-standards/`:
- Custom templates
- Required sections
- Governance gates

### 5.2 Demonstrate Sharing

```bash
# Other teams can install the preset:
specify preset add micron-standards --from github.com/terrel-test-org/spec-driven-enterprise-demo
```

### 5.3 Show Agent Catalog

All generated agents follow the same patterns:
- Consistent naming
- Standard structure
- Easy to discover and reuse

---

## Key Takeaways

### For Enterprise Leaders

1. **Standardization at scale** — Presets enforce consistency
2. **Legacy modernization** — Extract value from existing code
3. **Governance** — Constitution + validation = compliance
4. **Reusability** — Agents and skills shared across teams

### For Developers

1. **Spec-first workflow** — Better outcomes, less rework
2. **AI-assisted extraction** — Turn legacy into formal specs
3. **Automated validation** — Catch issues before implementation
4. **Agent generation** — Create tools from requirements

---

## Next Steps for Micron

1. **Pilot** — Apply SDD to one team/project
2. **Customize** — Create Micron-specific preset
3. **Train** — Onboard teams to SDD workflow
4. **Scale** — Roll out org-wide with governance

---

## Appendix: Demo Commands Reference

```bash
# Initialize spec-kit
specify init . --integration copilot

# Create constitution
/speckit.constitution Create principles for enterprise code quality

# Analyze legacy code
@spec-analyzer Analyze legacy-app/ and extract specifications

# Validate specifications
@spec-validator Validate specs/requirements/*.md

# Generate agent from spec
@spec-to-agent Create agent from specs/requirements/order-processing.md

# Full SDD workflow
/speckit.specify [describe feature]
/speckit.plan [describe tech stack]
/speckit.tasks
/speckit.implement
```
