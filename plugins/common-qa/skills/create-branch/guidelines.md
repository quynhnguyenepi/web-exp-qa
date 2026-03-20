# Create Branch Guidelines

Standards for creating git branches from JIRA tickets following team naming conventions.

## Branch Naming Rules

### Format

```
{username}/{TICKET-ID}-{short-description-in-kebab-case}
```

### Username Resolution

1. Check `git config user.name` first
2. If multi-word, check `git branch -r` for existing patterns from this user
3. If ambiguous, ask the user via AskUserQuestion
4. Never guess or fabricate a username

### Ticket ID

- Always uppercase: `CJS-10886`, not `cjs-10886`
- Extract from URLs or plain text input
- Validate format: `[A-Z]+-[0-9]+`

### Short Description

- Convert ticket title to kebab-case
- Lowercase, replace spaces with hyphens
- Remove special characters (parentheses, brackets, colons)
- Remove consecutive hyphens
- Truncate to keep branch name under ~80 characters total

---

## Safety Rules

### Before Switching Branches

- Always check for uncommitted changes with `git status --porcelain`
- If changes exist, offer: stash, discard, or cancel
- Never silently discard uncommitted work

### Before Creating Branch

- Always check if the branch already exists locally
- Always pull latest from the default branch before branching
- Detect the correct default branch (main or master), do not assume

### Do Not

- Force-delete existing branches without user confirmation
- Create branches from non-default branches unless explicitly requested
- Modify any files -- this skill only creates branches
- Push the branch to remote (user will do that when ready)

---

## Input Parsing

### Accepted Formats

| Input | How to Parse |
|-------|-------------|
| `https://optimizely-ext.atlassian.net/browse/CJS-10886` | Extract last path segment |
| `CJS-10886` | Use directly (uppercase) |
| `cjs-10886` | Convert to uppercase |
| `"work on CJS-10886"` | Extract ticket ID pattern |

### When Input Is Ambiguous

- If no ticket ID found, ask the user
- If multiple ticket IDs found, ask which one to use
- Never proceed without a confirmed ticket ID

---

## Anti-Patterns

### Hardcoding Default Branch

**Problem:** Assuming `main` is always the default branch.
**Solution:** Detect with `git symbolic-ref refs/remotes/origin/HEAD` or check remote branches.

### Skipping Confirmation

**Problem:** Creating the branch without showing the user the proposed name.
**Solution:** Always present the branch name and ask for confirmation before creating.

### Long Branch Names

**Problem:** Using the full untruncated ticket title, creating 100+ character branch names.
**Solution:** Truncate the description portion to keep total length reasonable.

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Parse JIRA ticket ID and build branch name", status: "in_progress", activeForm: "Parsing ticket ID" },
  { content: "Checkout default branch and pull latest", status: "pending", activeForm: "Pulling latest from default branch" },
  { content: "Create and checkout new branch", status: "pending", activeForm: "Creating new branch" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| No ticket ID provided | Ask user via AskUserQuestion |
| Git username not configured | Ask user for username |
| Atlassian MCP not available | Ask user for short description instead |
| Uncommitted changes | Offer to stash, discard, or cancel |
| Branch already exists | Offer to switch, recreate, or cancel |
| Not a git repository | Exit with error message |
| Pull fails (network) | Warn user, offer to continue with local state |

---


## Self-Correction

1. **"Use a different branch name"** -> Ask for custom name, use that instead
2. **"Branch from develop instead"** -> Use `develop` as base branch
3. **"Change the username"** -> Use specified username instead of git config
4. **"Shorter description"** -> Truncate or use user-provided short description

---


## Notes

### Input Flexibility

| Input Type | Example |
|------------|---------|
| JIRA ticket ID | `CJS-10873` |
| JIRA URL | `https://optimizely-ext.atlassian.net/browse/CJS-10873` |
| Custom branch name | `my-branch-name` (skips naming convention) |

### Integration with Other Skills

- **`/exp-qa-agents:create-test-scripts-cypress-js`**: Uses this skill to create a branch before generating test scripts
- **`/exp-qa-agents:create-pr`**: Creates a PR from the branch created by this skill
