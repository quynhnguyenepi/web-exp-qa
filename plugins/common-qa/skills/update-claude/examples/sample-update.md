# Sample: Update CLAUDE.md for a Cypress Test Repository

---

## Input

User request: "Update CLAUDE.md for my test repo at ~/Documents/GIT/my-e2e-tests"

---

## Step 0: Pre-Flight Checks

```
Pre-flight checks passed
   - Repository: my-e2e-tests
   - Path: ~/Documents/GIT/my-e2e-tests
   - Branch: main
   - Latest commit: a1b2c3d - Add new API tests for user management
   - Existing CLAUDE.md: No

Proceeding to analyze codebase...
```

---

## Step 1: Analyze Codebase

```
Codebase Analysis Complete

Tech Stack:
- Language: JavaScript
- Framework: Cypress v15.9.0
- Test Framework: Cypress (E2E)
- Build Tool: npm

Structure:
- 8 top-level directories
- 45 source files
- 32 test files
- Key patterns detected: Page Objects, Builder Pattern, Custom Commands

Proceeding to generate CLAUDE.md...
```

---

## Step 2: Generated CLAUDE.md

```markdown
# CLAUDE.md

## Overview

End-to-end test suite for a web application built with Cypress. Covers user management, authentication, and dashboard features.

**Technology Stack:**
- Cypress v15.9.0
- JavaScript
- Node.js

## Quick Reference

### Common Commands

npm run cy:open          # Open Cypress GUI
npm run cy:run           # Run all tests headless
npm run lint             # Run ESLint
npm run lint:fix         # Fix lint issues

### Key File Locations

cypress/
├── e2e/           # Test spec files
├── pages/         # Page objects
├── support/
│   ├── commands/  # Custom Cypress commands
│   └── apis/      # API helpers
└── fixtures/      # Test data

## Architecture

### Page Object Pattern
All UI interactions use page objects in cypress/pages/.

### Builder Pattern
Test data is created using builders in cypress/support/builders/.

### Custom Commands
Reusable operations are registered as Cypress commands in cypress/support/commands/.

## Coding Conventions

- File names: kebab-case (user-management.spec.js)
- Test names: [TICKET-ID][Module]_Description
- Page objects: PascalCase classes with chainable methods
- Always clean up test data in afterEach()
```

---

## Step 3: Review & Apply

User selected: "Apply as-is"

```
CLAUDE.md has been written to ~/Documents/GIT/my-e2e-tests/CLAUDE.md

The file contains:
- Overview with tech stack
- 4 common commands
- Directory structure with descriptions
- Architecture patterns (Page Objects, Builders, Commands)
- Coding conventions

Re-run /common-qa:update-claude after major codebase changes to keep it fresh.
```
