# Run Test Suite - Guidelines

**Shared reference:** For login configuration, Playwright action mapping, verification strategies, common test patterns, and error handling patterns, read `../execute-test-case/guidelines.md`. This file covers suite-specific rules only.

## Quality Guidelines

### Test Case Preparation

- Every step must have a concrete, verifiable expected outcome before execution begins
- Collect all unclear expected outcomes at once and present them to the user in a single prompt
- Do not accept vague outcomes like "it works", "page loads", or "verify" without specifics
- Validate that test cases have numbered steps, not paragraph descriptions

### Execution Rules

- Run in headless mode -- no visible browser window
- **Screenshot policy (cost-optimized):** Only capture `browser_take_screenshot` for the **last 2 steps** of each test case and at **any step that fails**. For all other steps, execute the action without taking screenshots. Use `browser_snapshot` only when needed for element refs.
- Do NOT capture screenshots during login or setup/navigation steps — these are not test evidence
- On step failure: IMMEDIATELY capture failure screenshot (`step-{K}-FAIL.png`), then STOP current TC and mark remaining steps as SKIPPED
- If a step failure makes subsequent steps impossible, mark remaining steps as SKIPPED
- Between test cases: navigate back to target URL and wait for page load before starting next TC
- Never ask the user mid-suite -- all clarifications happen before execution starts

### Parallel Execution with Isolated Browser Instances

**Architecture:** Two separate Playwright MCP server instances (`playwrightA` on port 3100, `playwrightB` on port 3101) each run their own browser process. This enables true parallel execution without interference.

- Split test cases across **exactly 2 agents** (max 2, never more)
- **Agents run in parallel** — both launch simultaneously, each with its own Playwright instance
- Agent 1 uses `mcp__playwrightA__*` tools ONLY; Agent 2 uses `mcp__playwrightB__*` tools ONLY
- Each agent starts by navigating to the target URL in its own browser
- Each agent handles its own login flow — both login with the same credentials
- Each agent creates result folders only for its own assigned TCs
- Agents do NOT share state — no Smart Skip across agents (only within each agent's batch)
- The coordinator merges all agent reports into one consolidated report after both agents finish
- If an agent fails entirely (crash, MCP error), re-launch it for its batch only

### Smart TC Grouping Rules

**DO NOT distribute TCs by sequential order.** Group by shared context to maximize state reuse:

1. **Identify context clusters:**
   - TCs needing generated/created data → group together (generate once, reuse)
   - TCs sharing the same UI state (same tab, same page) → group together
   - TCs testing form inputs → group together
2. **Order within each batch:** Data-producing TCs run FIRST so subsequent TCs reuse state
3. **Balance by step count:** Aim for roughly equal total steps per agent
4. **Present grouping rationale to user** before execution

### Fallback: Sequential Execution

If only ONE Playwright instance is configured, fall back to sequential mode:
- Split TCs across up to 2 agents, run one at a time
- **NEVER use `run_in_background: true`** — agents share a single browser
- Each agent starts by navigating to target URL for clean state

### Best Practices

- Present the full suite summary to the user before execution starts
- Allow the user to select specific test cases or run all
- Display brief progress updates after each test case completes: `TC-{N}: {PASS|FAIL} ({passed}/{total} steps)`
- Reset browser state between test cases by navigating to the target URL
- Take a fresh snapshot before starting each test case to verify clean state

### Anti-Patterns

- Do NOT pause on failure and ask the user -- this is headless mode, continue automatically
- Do NOT capture screenshots for early/middle steps (steps 1 to N-2) -- only last 2 steps + failure steps get screenshots
- Do NOT capture screenshots during login or setup/navigation steps -- these waste cost and are not test evidence
- Do NOT capture more than 2 screenshots per PASSING test case -- exactly 2 (last 2 steps), no more
- Do NOT capture multiple screenshots for the same step (e.g., step-15.png AND step-15-expanded.png) -- exactly 1 per step
- Do NOT launch more than 2 agents -- 2 is the hard maximum (one per Playwright instance)
- Do NOT merge results from different test cases -- each TC has its own verdict
- Do NOT report a TC as PASS if any step was SKIPPED (report as SKIPPED instead)
- Do NOT start execution without validating all expected outcomes first
- Do NOT use arbitrary screenshot filenames -- ALWAYS use `{TC_ID} Result/step-{N}.png` convention
- Do NOT capture fewer than 2 screenshots per passing test case -- the last 2 steps MUST have evidence
- Do NOT skip screenshot capture on a FAILED step -- failure evidence is the MOST important screenshot for bug reporting
- Do NOT let quality degrade on later test cases -- treat TC-005 with the same rigor as TC-001
- Do NOT reuse screenshots from a previous TC as evidence for a different TC -- each TC needs its own screenshots
- Do NOT use `run_in_background: true` when only a single Playwright instance is configured -- agents would share the browser
- Do NOT distribute TCs by sequential order -- always group by shared context/state for maximum reuse
- Do NOT let an agent use the wrong Playwright instance -- Agent 1 MUST use `playwrightA`, Agent 2 MUST use `playwrightB`
- Do NOT use `browser_evaluate()` for clicking buttons or filling inputs -- always use native Playwright MCP tools (`browser_click`, `browser_type`) with refs from `browser_snapshot`

### Suite Evidence Checkpoint (Run after EACH test case)

After completing each test case, STOP and verify before moving to the next:

```
EVIDENCE CHECKPOINT for {TC_ID}:
- [ ] Folder exists: "{TC_ID} Result/"
- [ ] If TC PASSED: Screenshot 1 "{TC_ID} Result/step-{N-1}.png" + Screenshot 2 "{TC_ID} Result/step-{N}.png" saved (last 2 steps)
- [ ] If TC FAILED at step K: Failure screenshot "{TC_ID} Result/step-{K}-FAIL.png" saved (MANDATORY — this is the most important screenshot)
- [ ] Screenshot files are NOT reused from another TC
→ If any check fails: capture missing evidence NOW before proceeding
→ CRITICAL: A failed TC without a failure screenshot is UNACCEPTABLE — the user cannot file a bug without visual evidence
```

### Report Standards

- Suite report must include: overall result, per-TC breakdown, pass rate, and failed steps summary
- Failed steps summary collects all failures across all TCs in one table
- Include screenshot references only for steps that have screenshots (last 2 steps + failure steps). For other steps, use "-" in the screenshot column
- Offer follow-up actions: create bug tickets, re-run failed TCs, re-run specific TC in interactive mode

### Error Recovery

- If browser crashes mid-suite: restart browser and resume from the next test case
- If login is required: ask user for credentials, complete login, then resume
- If a test case has no parseable steps: log warning and skip to next TC
- If target URL is unreachable: report error and abort suite

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Error Handling

| Error | Action |
|-------|--------|
| Playwright MCP not available | Exit with error: "Playwright MCP is not configured. See .mcp.json.template for detailed configuration." |
| No test cases provided | Ask user to provide (JIRA, text, image, or file) |
| Unclear expected outcome | Ask user to clarify before executing |
| Step failure | Record evidence, continue to next step |
| Test case failure makes next steps impossible | Mark remaining steps as SKIPPED |
| Browser crashes mid-suite | Restart browser, re-login with saved credentials, resume from next test case |
| Login fails (wrong credentials, MFA) | Ask user to provide correct credentials or resolve MFA, retry login |
| Session expired between test cases | Re-login with saved credentials, continue suite |
| JIRA ticket has no test steps | Log warning, ask user for that ticket's steps |


## Self-Correction

1. **"Page needs more time"** -> Add `browser_wait_for` before re-checking
2. **"Use different credentials"** -> Ask for new username/password, re-login
3. **"Re-run TC-003"** -> Re-execute just that test case
4. **"The expected outcome for step X should be Y"** -> Update expected, re-evaluate verdict
5. **"Run in headed mode instead"** -> Switch to `/exp-qa-agents:execute-test-case` for interactive execution
6. **"Add more test cases"** -> Append to suite, execute only the new ones
