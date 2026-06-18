# Enterprise Development Constitution

> Governing principles for AI-assisted development at the enterprise level.
> This constitution guides all specification creation, implementation, and code review.

## Core Principles

### 1. Specification First

**All significant development work begins with a specification.**

- No feature work without a reviewed spec
- Specs define WHAT, not HOW
- Specs are living documents, updated as understanding grows
- AI agents operate within spec boundaries

### 2. Consistency Over Creativity

**Standardization enables scale.**

- Use approved patterns and templates
- Follow naming conventions exactly
- Prefer boring, proven solutions
- Document deviations with rationale

### 3. Legacy Respect

**Existing systems encode valuable business knowledge.**

- Extract specs from legacy code before replacing
- Preserve business rules during modernization
- Test against legacy behavior, not just new specs
- Gradual migration over big-bang rewrites

### 4. Quality Gates

**Every artifact passes through validation.**

- Specs validated before implementation
- Code reviewed before merge
- Tests required for business logic
- Security review for sensitive changes

---

## Development Standards

### Code Quality

| Aspect | Standard |
|--------|----------|
| Test Coverage | Minimum 80% for business logic |
| Documentation | All public APIs documented |
| Error Handling | No silent failures; log and surface |
| Performance | Response times specified in specs |

### Security Requirements

- No credentials in code or config files
- Input validation on all external data
- Parameterized queries only (no string concatenation)
- Least privilege for all service accounts
- Security review required for auth changes

### Architecture Principles

- Services should be independently deployable
- Prefer stateless over stateful
- Use approved integration patterns
- Design for observability (logs, metrics, traces)

---

## Agent & Skill Standards

### Agent Creation

All Copilot agents must:
1. Have a clear, single purpose
2. Include trigger phrases in description
3. Follow the standard agent template
4. Be reviewed before org-wide deployment

### Skill Creation

All Copilot skills must:
1. Follow the SKILL.md format
2. Include reference documentation
3. Be versioned with semantic versioning
4. Have usage examples

### Prompt Standards

- Use descriptive file names
- Include input/output documentation
- Provide at least one example
- Test with edge cases

---

## Specification Requirements

### Required Sections

Every specification must include:

| Section | Purpose |
|---------|---------|
| Overview | What and why |
| User Stories | Who benefits and how |
| Business Rules | Decision logic |
| Data Model | Entities and relationships |
| Success Criteria | How we know it's done |

### Quality Criteria

Specifications must be:
- **Clear**: No ambiguous language
- **Complete**: All scenarios covered
- **Consistent**: No contradictions
- **Testable**: Verifiable outcomes

---

## Change Management

### Specification Changes

1. Document the change request
2. Assess impact on existing implementations
3. Update all affected artifacts
4. Re-validate changed specs

### Breaking Changes

- Require explicit approval
- Minimum 2-week notice for API changes
- Maintain backwards compatibility where possible
- Document migration path

---

## Governance

### Review Requirements

| Change Type | Reviewers Required |
|-------------|-------------------|
| New Feature Spec | 2 (including domain expert) |
| Architecture Change | 3 (including architect) |
| Security Change | 2 (including security) |
| Agent/Skill Creation | 1 (platform team) |

### Approval Authority

- Spec approval: Product Owner + Tech Lead
- Architecture decisions: Architecture Review Board
- Security exceptions: Security Team Lead
- Agent deployment: Platform Team

---

## Continuous Improvement

### Retrospectives

- Review spec accuracy after implementation
- Document lessons learned
- Update templates based on feedback
- Share patterns that work

### Metrics

Track and improve:
- Spec-to-implementation accuracy
- Defect rates by spec quality
- Time from spec to deployment
- Agent/skill reuse rates

---

*This constitution is maintained by the Platform Team. Updates require Architecture Review Board approval.*
