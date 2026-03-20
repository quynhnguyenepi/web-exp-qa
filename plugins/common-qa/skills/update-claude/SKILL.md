---
description: Pull the latest code for a specific repo and update its CLAUDE.md file to reflect current codebase structure, patterns, conventions, and documentation. Use when onboarding a repo for Claude Code or when the codebase has changed significantly.
---

## Dependencies

- **MCP Servers:** None
- **Related Skills:** `/common-qa:review-skills`

# Update CLAUDE.md for a Repository

Pull the latest code for a target repository, analyze its structure, patterns, and conventions, then generate or update the CLAUDE.md file so Claude Code has accurate context for that codebase.

## When to Use

Invoke this skill when you need to:

- Set up CLAUDE.md for a new repository that doesn't have one yet
- Update an existing CLAUDE.md after major codebase changes (new features, refactors, migrations)
- Refresh CLAUDE.md to reflect current file structure, dependencies, and patterns
- Onboard a repository for Claude Code usage by the team
- Periodically sync CLAUDE.md with the actual state of the codebase

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│  0. Pre-Flight Checks                                                            │
│     ├─ Validate repo path or URL                                                │
│     └─ Pull latest code                                                          │
│                                                                                  │
│  1. Analyze Codebase                                                             │
│     ├─ Scan directory structure                                                  │
│     ├─ Identify tech stack, frameworks, dependencies                            │
│     ├─ Detect patterns (test framework, build tools, CI/CD)                     │
│     └─ Find existing documentation                                              │
│                                                                                  │
│  2. Generate CLAUDE.md Content                                                   │
│     ├─ Overview section (what the project does)                                 │
│     ├─ Quick reference (common commands, key paths)                             │
│     ├─ Architecture section (structure, patterns, conventions)                  │
│     ├─ Coding conventions (naming, style, rules)                                │
│     └─ Working with Claude Code section                                         │
│                                                                                  │
│  3. Review & Apply                                                               │
│     ├─ Present generated content to user                                         │
│     ├─ User reviews and requests changes                                        │
│     └─ Write or update CLAUDE.md file                                           │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

**Simple Flow:**
```
Pre-Flight → Analyze Codebase → Generate Content → Review & Apply
```

## Execution Workflow

Follow these 4 sequential steps:

### Step 0: Pre-Flight Checks

**Todo:** Mark "Run pre-flight checks" as `in_progress`.

1. **Validate user input:**
   - Check if user provided a repo path (local) or repo URL (remote)
   - If not provided, ask the user via AskUserQuestion:
     - "What is the repository path or URL?"
   - If URL provided, check if the repo is already cloned locally

2. **Pull latest code:**
   - If local repo: run `git pull` to get latest changes
   - If remote URL: check if already cloned, if not suggest cloning first
   - Verify the pull was successful

3. **Check for existing CLAUDE.md:**
   - Look for `CLAUDE.md` in project root
   - Look for `.claude/` directory
   - If exists: note that we'll be updating (not creating from scratch)
   - If not exists: note that we'll be creating a new one

4. **Report pre-flight status:**
   ```
   Pre-flight checks passed
      - Repository: {REPO_NAME}
      - Path: {REPO_PATH}
      - Branch: {CURRENT_BRANCH}
      - Latest commit: {COMMIT_HASH} - {COMMIT_MESSAGE}
      - Existing CLAUDE.md: {Yes/No}

   Proceeding to analyze codebase...
   ```

---

### Step 1: Analyze Codebase

**Todo:** Mark "Run pre-flight checks" as `completed`, mark "Analyze codebase" as `in_progress`.

1. **Scan directory structure:**
   - List top-level directories and key files
   - Identify source code directories (src/, lib/, app/, etc.)
   - Identify test directories (test/, tests/, __tests__/, cypress/, etc.)
   - Identify config files (package.json, tsconfig.json, Makefile, etc.)
   - Identify CI/CD files (.github/workflows/, Jenkinsfile, etc.)

2. **Identify tech stack:**
   - Programming language(s) from file extensions and config
   - Framework(s) from dependencies (React, Express, Django, etc.)
   - Build tools (webpack, vite, gradle, etc.)
   - Test framework(s) (Jest, Cypress, pytest, JUnit, etc.)
   - Package manager (npm, yarn, pip, etc.)

3. **Detect patterns and conventions:**
   - Code organization pattern (monorepo, feature-based, layer-based)
   - Naming conventions from existing code (camelCase, snake_case, etc.)
   - Common patterns (Page Objects, Builders, Factory, etc.)
   - Import/export patterns
   - Error handling patterns

4. **Find existing documentation:**
   - README.md content
   - Existing CLAUDE.md (if updating)
   - docs/ directory
   - API documentation
   - Contributing guidelines

5. **Extract common commands:**
   - From package.json scripts
   - From Makefile targets
   - From CI/CD configuration
   - From README.md

6. **Report analysis results:**
   ```
   Codebase Analysis Complete

   Tech Stack:
   - Language: {LANGUAGES}
   - Framework: {FRAMEWORKS}
   - Test Framework: {TEST_FRAMEWORKS}
   - Build Tool: {BUILD_TOOLS}

   Structure:
   - {N} top-level directories
   - {N} source files
   - {N} test files
   - Key patterns detected: {PATTERNS}

   Proceeding to generate CLAUDE.md...
   ```

---

### Step 2: Generate CLAUDE.md Content

**Todo:** Mark "Analyze codebase" as `completed`, mark "Generate CLAUDE.md content" as `in_progress`.

Generate the CLAUDE.md content following this structure:

1. **Overview Section:**
   - What the project does (from README.md or code analysis)
   - Technology stack summary
   - Key concepts and terminology

2. **Quick Reference:**
   - Most common commands (build, test, lint, run)
   - Key file locations (source, tests, config)
   - Environment setup requirements

3. **Architecture Section:**
   - Directory structure with descriptions
   - Code organization patterns
   - Key modules and their responsibilities
   - Data flow or request flow (if detectable)

4. **Coding Conventions:**
   - Naming conventions (files, variables, functions, classes)
   - Code style rules (from linter config if available)
   - Import ordering
   - Test naming and organization

5. **Working with Claude Code:**
   - Common Claude requests for this codebase
   - Tips specific to this project
   - Before pushing checklist

6. **If updating existing CLAUDE.md:**
   - Preserve user-added sections that are still relevant
   - Update outdated information (paths, commands, dependencies)
   - Add new sections for newly detected patterns
   - Highlight what changed

---

### Step 3: Review & Apply

**Todo:** Mark "Generate CLAUDE.md content" as `completed`, mark "Review with user and apply changes" as `in_progress`.

1. **Present the generated content to the user:**
   - Show the full CLAUDE.md content
   - If updating, highlight what changed vs the existing file

2. **Ask user for feedback via AskUserQuestion:**
   - **"Apply as-is" (Recommended)** — Write the CLAUDE.md file
   - **"Review and edit"** — Let user suggest changes before applying
   - **"Show me the diff"** — If updating, show before/after comparison

3. **Handle user response:**

   **If "Apply as-is":**
   - Write CLAUDE.md to the project root
   - If modular docs needed, create `.claude/docs/` structure
   - Report: "CLAUDE.md has been written to {REPO_PATH}/CLAUDE.md"

   **If "Review and edit":**
   - Accept user's changes
   - Apply modifications
   - Show updated version for final confirmation

   **If "Show me the diff":**
   - Show side-by-side or inline diff
   - Ask again for confirmation

4. **Mark "Review with user and apply changes" as `completed`.** All todos should now be `completed`.

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
