# Update CLAUDE.md Guidelines

Standards for analyzing codebases and generating accurate, useful CLAUDE.md files.

## CLAUDE.md Structure Template

A good CLAUDE.md follows this structure:

```markdown
# CLAUDE.md

## Overview
- What the project does
- Technology stack
- Key concepts

## Quick Reference
### Common Commands
### Key File Locations

## Architecture
### Directory Structure
### Patterns and Conventions

## Coding Conventions
### Naming
### Style Rules

## Working with Claude Code
### Common Requests
### Tips
### Before Pushing Checklist
```

---

## Analysis Best Practices

### 1. Start Broad, Then Deep

1. First scan top-level directory structure
2. Then identify the tech stack from config files
3. Then dive into key source directories for patterns
4. Finally extract commands and conventions

### 2. Prioritize Accuracy

- Only document commands that actually work
- Only list paths that actually exist
- Only describe patterns you can verify in the code
- If unsure about something, mark it or ask the user

### 3. Preserve User Content

When updating an existing CLAUDE.md:
- Keep user-added custom sections
- Update auto-detected sections (paths, commands, dependencies)
- Don't remove content unless it's clearly outdated/wrong
- Add a comment noting what was auto-updated vs user-written

---

## Tech Stack Detection

### From Config Files

| Config File | What It Tells Us |
|------------|-----------------|
| `package.json` | Node.js project, dependencies, scripts |
| `tsconfig.json` | TypeScript configuration |
| `requirements.txt` / `setup.py` | Python project, dependencies |
| `build.gradle` / `pom.xml` | Java/Kotlin project |
| `go.mod` | Go project |
| `Cargo.toml` | Rust project |
| `Makefile` | Build commands |
| `docker-compose.yml` | Container setup |
| `cypress.config.js` | Cypress test framework |
| `jest.config.js` | Jest test framework |
| `pytest.ini` | Pytest framework |

### From Directory Names

| Directory | Likely Purpose |
|-----------|---------------|
| `src/` | Source code |
| `lib/` | Library code |
| `app/` | Application code |
| `test/` / `tests/` / `__tests__/` | Unit tests |
| `cypress/` / `e2e/` | E2E tests |
| `pages/` | Page objects or Next.js pages |
| `components/` | UI components |
| `api/` / `routes/` | API endpoints |
| `utils/` / `helpers/` | Utility functions |
| `config/` | Configuration files |
| `docs/` | Documentation |
| `.github/` | GitHub Actions, templates |

---

## Command Extraction

### From package.json

```json
{
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint .",
    "start": "node dist/index.js"
  }
}
```

Extract as:
```markdown
### Common Commands
- `npm run build` — Compile TypeScript
- `npm test` — Run tests with Jest
- `npm run lint` — Lint code with ESLint
- `npm start` — Start the application
```

### From Makefile

Extract target names and their descriptions (from comments).

### From CI/CD

Extract build, test, and deploy commands from workflow files.

---

## Pattern Detection

### Code Organization

| Pattern | Indicators |
|---------|-----------|
| Feature-based | Directories named after features (`auth/`, `checkout/`) |
| Layer-based | Directories named after layers (`controllers/`, `services/`, `models/`) |
| Monorepo | `packages/` directory, workspaces in package.json |
| Page Object | `pages/` with classes that wrap UI elements |
| Builder | `builders/` with classes using fluent API |

### Naming Conventions

Detect from existing files:
- File names: `camelCase.ts`, `kebab-case.ts`, `snake_case.py`
- Variable names: analyze source code imports and declarations
- Test names: `describe('...', ...)` patterns, test file naming

---

## Quality Checklist

Before presenting CLAUDE.md to user:

- [ ] All listed commands are correct (verified from config)
- [ ] All file paths exist in the repo
- [ ] Tech stack information is accurate
- [ ] Patterns described match actual code
- [ ] No placeholder text left in the output
- [ ] Structure is clear and scannable
- [ ] Appropriate level of detail (not too verbose, not too sparse)

---

## Anti-Patterns

### Guessing Commands
**Problem**: Listing commands that don't exist in the repo
**Solution**: Only extract commands from actual config files

### Over-documenting
**Problem**: CLAUDE.md longer than necessary with redundant info
**Solution**: Focus on what Claude Code needs to know, not everything

### Ignoring Existing Content
**Problem**: Overwriting user-customized CLAUDE.md
**Solution**: Merge updates with existing content, preserve custom sections

### Static Snapshots
**Problem**: CLAUDE.md becomes outdated as codebase evolves
**Solution**: Re-run this skill periodically, especially after major changes

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list so the user can see what the agent is doing at all times. Update the todo status as each step progresses.

**Initial todo list (create immediately when skill is invoked):**

```
TodoWrite([
  { content: "Run pre-flight checks (validate repo, pull latest code)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Analyze codebase (structure, tech stack, patterns)", status: "pending", activeForm: "Analyzing codebase" },
  { content: "Generate CLAUDE.md content", status: "pending", activeForm: "Generating CLAUDE.md content" },
  { content: "Review with user and apply changes", status: "pending", activeForm: "Reviewing and applying changes" }
])
```

**Update rules:**
- Mark current step as `in_progress` when starting it
- Mark step as `completed` immediately when finished (do not batch)
- Only ONE step should be `in_progress` at any time

---


## Error Handling

| Error | Action |
|-------|--------|
| Repo path doesn't exist | Ask user for correct path |
| Git pull fails (conflicts) | Warn user, suggest resolving conflicts first |
| Git pull fails (auth) | Display auth error, suggest checking SSH/credentials |
| Empty repository | Create minimal CLAUDE.md template |
| Very large repo (>10k files) | Focus on key directories, skip deep scanning |
| No package.json/config found | Infer from file extensions and directory names |
| Existing CLAUDE.md is read-only | Warn user, suggest permissions fix |

---


## Self-Correction

When user requests adjustments:

1. **"Add more detail about X"** → Expand the specific section
2. **"Remove section Y"** → Remove the section and regenerate
3. **"Focus on test patterns"** → Deep-dive into test directory and patterns
4. **"Also create modular docs"** → Generate `.claude/docs/` structure with separate files
5. **"Use our team's template"** → Accept custom template and fill in with analyzed data
6. **"Only update the commands section"** → Partial update of specific sections

---


## Notes

### What Makes a Good CLAUDE.md

1. **Accurate** — Reflects the actual state of the codebase
2. **Concise** — Key information without unnecessary verbosity
3. **Actionable** — Commands that work, paths that exist
4. **Structured** — Easy to scan with clear sections
5. **Maintained** — Re-run this skill periodically to keep it fresh

### Content Sources

| Source | What We Extract |
|--------|----------------|
| `package.json` / `build.gradle` / `requirements.txt` | Dependencies, scripts, version |
| `README.md` | Project description, setup instructions |
| Linter configs (`.eslintrc`, `.prettier`) | Code style rules |
| CI/CD configs | Build/test/deploy commands |
| Directory structure | Architecture, organization patterns |
| Existing code | Naming conventions, patterns |
| Test files | Test framework, test patterns |

### Integration with Other Skills

- **`/common-qa:update-skills`**: After updating CLAUDE.md, update skills that reference codebase patterns
- **`/common-qa:review-skills`**: Review skills to ensure they align with the updated CLAUDE.md
