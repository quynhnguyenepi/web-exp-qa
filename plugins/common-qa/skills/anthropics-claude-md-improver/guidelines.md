# CLAUDE.md Improver Guidelines

Standards for auditing, scoring, and improving CLAUDE.md files across repositories.

## Quality Criteria Weights

Each CLAUDE.md file is scored out of 100 points across six criteria:

| Criterion | Max Points | Weight | Description |
|-----------|:----------:|:------:|-------------|
| Commands/workflows documented | 20 | High | Build, test, lint, deploy commands present and runnable |
| Architecture clarity | 20 | High | Directory structure, key files, module relationships |
| Non-obvious patterns | 15 | Medium | Gotchas, quirks, workarounds that save time |
| Conciseness | 15 | Medium | Dense and scannable, no filler or obvious info |
| Currency | 15 | High | Reflects current codebase state, not stale |
| Actionability | 15 | High | Instructions are executable, not vague or aspirational |

## Scoring Rubric

### Commands/Workflows (0-20)

| Score | Criteria |
|:-----:|----------|
| 18-20 | All major commands documented, copy-paste ready, covers build/test/lint/deploy |
| 12-17 | Most commands present, minor gaps (e.g., missing deploy or lint) |
| 6-11 | Only basic commands (e.g., just `npm install`), missing test/lint |
| 0-5 | No commands or only vague references ("run the tests") |

### Architecture Clarity (0-20)

| Score | Criteria |
|:-----:|----------|
| 18-20 | Clear directory tree, key files identified, module relationships explained |
| 12-17 | Directory structure present but incomplete, some key files missing |
| 6-11 | Minimal structure info, no key files identified |
| 0-5 | No architecture information |

### Non-Obvious Patterns (0-15)

| Score | Criteria |
|:-----:|----------|
| 13-15 | Documents gotchas, env quirks, common mistakes, workarounds |
| 8-12 | Some gotchas mentioned but incomplete |
| 4-7 | One or two notes, mostly obvious information |
| 0-3 | No gotchas or non-obvious patterns documented |

### Conciseness (0-15)

| Score | Criteria |
|:-----:|----------|
| 13-15 | Dense, scannable, no filler, uses tables and lists effectively |
| 8-12 | Mostly concise with some verbose sections |
| 4-7 | Overly verbose, paragraphs where bullets would suffice |
| 0-3 | Wall of text, obvious information restated, hard to scan |

### Currency (0-15)

| Score | Criteria |
|:-----:|----------|
| 13-15 | All commands verified working, file paths match current structure |
| 8-12 | Mostly current with minor stale references |
| 4-7 | Several outdated commands or paths |
| 0-3 | Severely outdated, references deleted files or old tooling |

### Actionability (0-15)

| Score | Criteria |
|:-----:|----------|
| 13-15 | All instructions executable, specific, with expected outcomes |
| 8-12 | Most instructions actionable, some vague ("configure as needed") |
| 4-7 | Mix of actionable and vague instructions |
| 0-3 | Mostly vague or aspirational ("follow best practices") |

---

## Update Rules

### Preserve Existing Content

- Never delete or rewrite existing sections without explicit user approval
- Propose additions and improvements as diffs, not replacements
- Maintain the author's voice and formatting style where possible

### Propose Additions Only

- Focus on genuinely useful information discovered during analysis
- Each proposed addition must include a "Why" justification
- Show diffs in context so the user can see where content goes

### Show Diffs Before Applying

- Every change must be shown as a diff block before applying
- Group related changes together for easier review
- Allow user to approve/reject individual changes

---

## Anti-Patterns

### Over-Documenting

**Problem:** Adding information that is obvious from the code itself.
**Example:** Documenting every file in `src/` when the structure is standard.
**Rule:** If a developer can figure it out in 30 seconds from the code, skip it.

### Stale Commands

**Problem:** Documenting commands that no longer work or have been renamed.
**Rule:** Verify commands against `package.json`, `Makefile`, or equivalent before including.

### Generic Advice

**Problem:** Adding boilerplate like "follow best practices" or "write clean code."
**Rule:** Every line should be specific to this project. If it applies to any project, remove it.

### Duplicating README Content

**Problem:** Copying the README.md into CLAUDE.md verbatim.
**Rule:** CLAUDE.md is for Claude-specific context. Link to README for general docs.

### Ignoring Monorepo Structure

**Problem:** Putting all context in root CLAUDE.md when packages have distinct needs.
**Rule:** Use package-level CLAUDE.md files for package-specific commands and patterns.

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list so the user can see what the agent is doing at all times.

**Initial todo list (create immediately when skill is invoked):**

```
TodoWrite([
  { content: "Discover all CLAUDE.md files in repository", status: "in_progress", activeForm: "Discovering CLAUDE.md files" },
  { content: "Assess quality of each file", status: "pending", activeForm: "Assessing quality" },
  { content: "Generate and present quality report", status: "pending", activeForm: "Generating quality report" },
  { content: "Apply targeted updates (with user approval)", status: "pending", activeForm: "Applying updates" }
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
| No CLAUDE.md files found | Report "No CLAUDE.md files found", suggest creating one |
| File is read-only | Warn user, suggest fixing permissions |
| Very large file (>500 lines) | Focus on key sections, warn about verbosity |
| Invalid markdown syntax | Report parse issues, proceed with best effort |
| Monorepo with 10+ CLAUDE.md files | Process in batches, summarize findings |
| User denies update | Respect decision, report was still generated |
| Git conflicts after update | Warn user, suggest resolving manually |

---


## Self-Correction

When user requests adjustments:

1. **"Focus on commands only"** --> Re-audit with focus on commands/workflows section
2. **"Use a different template"** --> Apply user's preferred template structure
3. **"Skip low-scoring files"** --> Only update files below threshold
4. **"Be more/less strict"** --> Adjust quality criteria weights
5. **"Don't modify, just report"** --> Skip update phase, only generate report
6. **"Update the global CLAUDE.md too"** --> Include ~/.claude/CLAUDE.md in scope

---


## Notes

### Templates

See [references/templates.md](references/templates.md) for CLAUDE.md templates by project type.

### Common Issues to Flag

1. **Stale commands**: Build commands that no longer work
2. **Missing dependencies**: Required tools not mentioned
3. **Outdated architecture**: File structure that's changed
4. **Missing environment setup**: Required env vars or config
5. **Broken test commands**: Test scripts that have changed
6. **Undocumented gotchas**: Non-obvious patterns not captured

### User Tips to Share

When presenting recommendations, remind users:

- **`#` key shortcut**: During a Claude session, press `#` to have Claude auto-incorporate learnings into CLAUDE.md
- **Keep it concise**: CLAUDE.md should be human-readable; dense is better than verbose
- **Actionable commands**: All documented commands should be copy-paste ready
- **Use `.claude.local.md`**: For personal preferences not shared with team (add to `.gitignore`)
- **Global defaults**: Put user-wide preferences in `~/.claude/CLAUDE.md`

### What Makes a Great CLAUDE.md

**Key principles:**
- Concise and human-readable
- Actionable commands that can be copy-pasted
- Project-specific patterns, not generic advice
- Non-obvious gotchas and warnings

**Recommended sections** (use only what's relevant):
- Commands (build, test, dev, lint)
- Architecture (directory structure)
- Key Files (entry points, config)
- Code Style (project conventions)
- Environment (required vars, setup)
- Testing (commands, patterns)
- Gotchas (quirks, common mistakes)
- Workflow (when to do what)
