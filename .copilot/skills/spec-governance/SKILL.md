---
name: spec-governance
description: "Validates specifications against enterprise standards and constitution. Ensures specs are complete, consistent, and compliant before implementation begins. WHEN: validate spec, check compliance, review specification, governance check, spec quality review, pre-implementation validation."
license: MIT
metadata:
  author: Enterprise Platform Team
  version: "1.0.0"
---

# Spec Governance Skill

> Ensure specifications meet enterprise standards before implementation.

## Triggers

Activate this skill when:
- Validating a specification before implementation
- Checking spec compliance with enterprise standards
- Performing pre-implementation governance review
- Auditing existing specifications
- Preparing specs for architecture review

## Rules

1. **Check Against Constitution** - All validations reference specs/constitution.md
2. **Be Specific** - Cite exact issues with references
3. **Distinguish Severity** - Separate blocking vs. advisory issues
4. **Provide Guidance** - Include remediation recommendations
5. **Document Exceptions** - Note any approved deviations

## Workflow

### Step 1: Completeness Check
Verify required sections are present:
- [ ] Overview
- [ ] User Stories (at least one)
- [ ] Business Rules
- [ ] Data Model (if applicable)
- [ ] Success Criteria

### Step 2: Quality Check
Evaluate each section for:
- Clarity (no ambiguous terms)
- Specificity (measurable where applicable)
- Testability (can be verified)
- Consistency (no contradictions)

### Step 3: Standards Compliance
Check against constitution requirements:
- Security considerations documented
- Performance requirements specified
- Error handling defined
- Logging/monitoring addressed

### Step 4: Cross-Reference Check
Validate against related artifacts:
- No conflicts with existing specs
- Dependencies are documented
- Integration points are valid

### Step 5: Generate Report
Output validation report to: `specs/validation/{spec-name}-validation.md`

## Validation Checklist

### Required Elements
| Element | Check |
|---------|-------|
| Overview | Present and clear |
| User Stories | At least one with acceptance criteria |
| Business Rules | Documented with IDs |
| Success Criteria | Measurable outcomes |

### Quality Standards
| Criterion | Standard |
|-----------|----------|
| Clarity | No "should", "might", "could" |
| Completeness | Happy path + edge cases |
| Testability | Each requirement verifiable |
| Consistency | Same terms used throughout |

### Compliance Items
| Requirement | Source |
|-------------|--------|
| Security section | Constitution §Security |
| Performance targets | Constitution §Code Quality |
| Error handling | Constitution §Code Quality |

## Output Format

```markdown
# Specification Validation Report

**Spec**: {name}  
**Validated**: {timestamp}  
**Status**: ✅ PASSED | ⚠️ NEEDS REVIEW | ❌ FAILED

## Summary
- Completeness: {X}/{Y} required sections
- Quality Score: {percentage}%
- Compliance: {status}

## Findings

### ❌ Blocking Issues
{Must be fixed before implementation}

### ⚠️ Warnings  
{Should be addressed but not blocking}

### ✅ Passed
{Successfully validated items}

## Recommendations
{Suggested improvements}
```

## References

- [constitution.md](../../../specs/constitution.md) - Enterprise standards
- [validation-rules.md](references/validation-rules.md) - Detailed validation criteria
