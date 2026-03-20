# Sample Audit: Multi-File CLAUDE.md Improvement

This is an example of a complete audit produced by the anthropics-claude-md-improver skill, showing discovery, scoring, reporting, and targeted updates.

---

## Input

User request: "Audit my CLAUDE.md files"

---

## Step 0: Discovery

**TodoWrite progression:**
```
TodoWrite([
  { content: "Discover all CLAUDE.md files in repository", status: "in_progress", activeForm: "Discovering CLAUDE.md files" },
  { content: "Assess quality of each file", status: "pending", activeForm: "Assessing quality" },
  { content: "Generate and present quality report", status: "pending", activeForm: "Generating quality report" },
  { content: "Apply targeted updates (with user approval)", status: "pending", activeForm: "Applying updates" }
])
```

```
Scanning for CLAUDE.md files...

Found 2 CLAUDE.md file(s):
  1. ./CLAUDE.md (Project Root)
  2. ./packages/api/CLAUDE.md (Package-specific)

Proceeding to assess quality...
```

---

## Step 1: Quality Assessment

**TodoWrite update:**
```
{ content: "Discover all CLAUDE.md files in repository", status: "completed" }
{ content: "Assess quality of each file", status: "in_progress" }
```

For each file, read contents and evaluate against the six quality criteria.

**File 1: ./CLAUDE.md**
- Commands: Has `npm install` and `npm start`, missing test/lint commands
- Architecture: Basic directory listing, no key files identified
- Non-obvious: No gotchas documented
- Conciseness: Good, uses bullet points
- Currency: File paths match current structure
- Actionability: Commands are copy-paste ready

**File 2: ./packages/api/CLAUDE.md**
- Commands: Only mentions "run tests" without the actual command
- Architecture: No structure documented
- Non-obvious: Documents one database quirk
- Conciseness: Very brief (8 lines)
- Currency: References a config file that still exists
- Actionability: Database quirk is actionable, rest is vague

---

## Step 2: Quality Report Output

**TodoWrite update:**
```
{ content: "Assess quality of each file", status: "completed" }
{ content: "Generate and present quality report", status: "in_progress" }
```

```
## CLAUDE.md Quality Report

### Summary
- Files found: 2
- Average score: 52/100
- Files needing update: 2

### File-by-File Assessment

#### 1. ./CLAUDE.md (Project Root)
**Score: 58/100 (Grade: C)**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Commands/workflows | 10/20 | Has install/start, missing test/lint/deploy |
| Architecture clarity | 8/20 | Basic directory listing, no key files |
| Non-obvious patterns | 2/15 | No gotchas documented |
| Conciseness | 13/15 | Good use of bullets, no filler |
| Currency | 13/15 | File paths match current structure |
| Actionability | 12/15 | Commands are runnable |

**Issues:**
- Missing test command (`npm test` exists in package.json but not documented)
- Missing lint command (`npm run lint` exists but not documented)
- No architecture key files (entry point is src/index.ts)
- No gotchas section

**Recommended additions:**
- Add test and lint commands
- Add key files section (src/index.ts, src/config.ts)
- Add gotchas section for env var requirements

#### 2. ./packages/api/CLAUDE.md (Package-specific)
**Score: 46/100 (Grade: D)**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Commands/workflows | 4/20 | Says "run tests" but no actual command |
| Architecture clarity | 3/20 | No structure documented |
| Non-obvious patterns | 10/15 | Good database quirk documentation |
| Conciseness | 12/15 | Brief but too sparse |
| Currency | 10/15 | Config reference valid |
| Actionability | 7/15 | Database note is actionable, rest is vague |

**Issues:**
- No actual test command (should be `npm run test:api`)
- No directory structure for the API package
- Missing environment variable documentation (DB_HOST, DB_PORT)

**Recommended additions:**
- Add actual test command
- Add API route structure overview
- Document required env vars
```

---

## Step 3: Targeted Updates

**TodoWrite update:**
```
{ content: "Generate and present quality report", status: "completed" }
{ content: "Apply targeted updates (with user approval)", status: "in_progress" }
```

Proposed changes presented to user:

```markdown
### Update 1: ./CLAUDE.md

**Why:** Test and lint commands exist in package.json but are not documented, causing developers to guess.

```diff
 ## Commands

 npm install        # Install dependencies
 npm start          # Start development server
+npm test           # Run all tests
+npm run lint       # Lint with ESLint
+npm run lint:fix   # Auto-fix lint issues
```

### Update 2: ./CLAUDE.md

**Why:** Key entry points help Claude navigate the codebase faster.

```diff
+## Key Files
+
+- `src/index.ts` - Application entry point
+- `src/config.ts` - Environment configuration
+- `src/routes/` - API route definitions
```

### Update 3: ./packages/api/CLAUDE.md

**Why:** Vague "run tests" instruction is not actionable. Actual command saves developer time.

```diff
-Run tests before submitting PRs.
+## Commands
+
+npm run test:api          # Run API tests
+npm run test:api:watch    # Run in watch mode
```
```

User selected: "Apply all updates"

---

## Step 4: Apply Updates

Applied 3 updates using the Edit tool:

1. ./CLAUDE.md -- Added test/lint commands (Score impact: +8 on Commands)
2. ./CLAUDE.md -- Added key files section (Score impact: +6 on Architecture)
3. ./packages/api/CLAUDE.md -- Replaced vague test reference with commands (Score impact: +10 on Commands)

**TodoWrite update:**
```
{ content: "Apply targeted updates (with user approval)", status: "completed" }
```

```
Audit complete!

Updates applied: 3
- ./CLAUDE.md: 2 updates (estimated new score: 72/100, Grade: B)
- ./packages/api/CLAUDE.md: 1 update (estimated new score: 56/100, Grade: C)

Tip: Press # during a Claude session to auto-incorporate learnings into CLAUDE.md.
```
