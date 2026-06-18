# Legacy Enterprise Application

> ⚠️ **WARNING**: This is intentionally "legacy" code for demonstration purposes.
> It contains anti-patterns, security issues, and technical debt to showcase
> how Spec-Driven Development can help modernize existing systems.

## Overview

This sample application simulates a typical enterprise system that has evolved over many years:

- **Python Services**: Backend order processing and inventory management
- **Java API**: REST API layer for external integrations
- **SQLite Database**: Shared data store (simulated legacy pattern)

## Known Issues (Intentional for Demo)

### Security
- SQL injection vulnerabilities in Java API
- Hardcoded credentials in inventory manager
- No input validation on several endpoints

### Architecture
- Tight coupling between components
- Global state and singletons
- Mixed business logic and data access
- Inconsistent error handling

### Code Quality
- Minimal documentation
- No tests
- Magic numbers throughout
- Duplicated business logic between Python and Java

### Business Rules
- Undocumented rules embedded in code
- Inconsistent validation across layers
- Status transitions not formally defined

## File Structure

```
legacy-app/
├── python-services/
│   ├── database.py          # Data access layer
│   ├── order_processor.py   # Order management
│   └── inventory_manager.py # Inventory operations
├── java-api/
│   └── src/main/java/com/legacy/api/
│       ├── OrderController.java   # REST endpoints
│       └── CustomerService.java   # Customer operations
└── docs/
    └── README.md            # This file (outdated)
```

## Demo Purpose

Use this codebase to demonstrate:

1. **@spec-analyzer**: Extract specifications from this messy codebase
2. **Spec validation**: Show how extracted specs reveal inconsistencies
3. **Modernization planning**: Create a plan to refactor properly
4. **Agent generation**: Build agents to help maintain the modernized system

## Running the Demo

See the main [README](../../README.md) for the complete demo walkthrough.
