# Ticket Analysis Guidelines

Detailed reference material and examples beyond the workflow in SKILL.md.

---

## 1. Ticket Pattern Recognition

**Common ticket patterns and their testing implications:**

| Pattern | What to Expect | Testing Focus |
|---------|---------------|---------------|
| **Story** | New feature — new code, new UI, new tests needed | Full coverage: happy path, validation, edge cases |
| **Bug** | Fix for existing issue | Regression, verify the fix, check edge cases |
| **Task** | Refactoring or config change | No-regression, verify behavior preserved |
| **Sub-task** | Part of a larger story — check parent for full context | Integration with sibling tasks |

---

## 2. Epic Signals

**What to look for in epic children:**

| Signal | Meaning |
|--------|---------|
| Multiple tickets with same label | Feature area is being actively developed |
| Bug tickets in the epic | Known issues — avoid duplicating test cases |
| Closed tickets | Previously tested areas — focus on integration |
| `Requires_QA` label | Other tickets also need testing — look for interactions |

---

## 3. Identifying Hidden Changes in PRs

PRs often contain changes beyond the ticket scope. Look for these patterns:

- **Import reordering**: Cosmetic, no testing needed
- **Event name changes**: Behavior change, needs verification
- **Removing parameters from function calls**: May indicate a refactoring — check if data is moved elsewhere (e.g., to global properties)
- **Adding new function calls**: New behavior being introduced
- **Store modifications**: Can have cascading effects on many components

**Example of a hidden change:**
```
Ticket says: "Add thread_id to save_all_opal event"
PR actually does:
  1. Adds thread_id to save_all_opal (as requested)
  2. Adds thread_id to undo_all_opal (related)
  3. Refactors ALL tracking to use global properties (broad change!)
  4. Removes experiment_id from 10 individual calls
  5. Adds new opal_apply_change event (not mentioned in ticket)
```

In this example, testing ONLY the ticket AC would miss items 3-5.

### File Type Classification

| File type | What to look for | Test implication |
|-----------|-----------------|-----------------|
| `*.tsx` / `*.jsx` (Components) | New UI elements, changed props, event handlers | Verify rendering, user interactions |
| `*Store.ts` (Stores) | New state fields, changed actions, new side effects | Verify state transitions, data flow |
| `*api/*.ts` (Services) | New endpoints, changed request/response format | Verify API integration |
| `*.test.*` (Tests) | Changed assertions, new test scenarios | Understand what devs already verified |
| `constants.ts` / `enums.ts` | New values, renamed constants | Verify downstream usage |
| `*.module.scss` (Styles) | Visual changes | Visual verification needed |

---

## 4. Verification Methods by Category

Always include HOW to verify each test case. Use these methods per category:

### Tracking / Analytics
- **How to verify**: Browser DevTools > Network tab, filter for Segment API calls
- **What to check**: Event name format, property values, property presence

### UI / Visual
- **How to verify**: Visual inspection in the application
- **What to check**: Element visibility, correct text, proper styling

### State Management
- **How to verify**: React DevTools, functional testing (trigger state change, verify effect)
- **What to check**: State transitions, data persistence, cross-component effects

### API / Services
- **How to verify**: Network tab, API response inspection
- **What to check**: Request format, response handling, error states

### Configuration
- **How to verify**: Test with flag on/off, different environments
- **What to check**: Feature availability, correct environment URLs

### Business Logic
- **How to verify**: Functional testing, edge cases
- **What to check**: Input/output correctness, error handling

### Verification Tools Summary

| Category | Primary Method | Tools |
|----------|---------------|-------|
| Tracking events | Network tab, filter `segment.io` or `api.segment.io` | DevTools > Network |
| Event properties | Inspect request payload in Network tab | DevTools > Network > Preview |
| UI rendering | Visual inspection | Browser |
| State changes | Trigger action, verify effect in UI | Browser + React DevTools |
| API calls | Network tab, inspect request/response | DevTools > Network |
| Feature flags | Test with flag on and off | Optimizely dashboard |

---

## 5. Writing Good Test Cases

**Each test case should answer:**
1. **WHAT** am I testing? (Clear title)
2. **HOW** do I test it? (Steps or verification method)
3. **WHAT** do I expect? (Specific expected result)
4. **WHY** is this important? (Priority justification)

**Good test case example:**
```
| # | Test Case | What to verify |
|---|-----------|----------------|
| 1 | save_all_opal has thread_id | Click "Save All" on OpalPreviewBanner.
|   |                             | Verify Segment event EXP - VE - save_all_opal
|   |                             | includes thread_id with a valid non-empty value |
```

**Bad test case example:**
```
| # | Test Case | What to verify |
|---|-----------|----------------|
| 1 | Test saving | Check that saving works |
```

Why bad: vague title, no specific verification, no mention of what "works" means.

---

## 7. Full Flow TC — Mandatory Output (Added CJS-10818 retrospective 2026-03-24)

> **Problem:** Analysis reads FULL_FLOW_SPEC.md to identify regression scope nhưng KHÔNG translate thành instruction "Full Flow TC cần bao gồm Results page" cho web-create-test-cases.

### MANDATORY: Analysis output phải include Full Flow TC instruction

Sau khi hoàn thành analysis, LUÔN thêm block này vào output:

```
**Full Flow TC Required:**
- Type: [Standard VE | Event Full Flow | Tracking]
- Reason: [keyword triggered this]
- Must include Results page: [YES/NO]
- Checkpoints: [list từ FULL_FLOW_SPEC.md]
```

### Trigger — Event Full Flow (Results page REQUIRED)

| Keyword trong ticket | PHẢI bao gồm Results page |
|---|---|
| create event, click event, event creation | YES — CP-9 + CP-10 |
| add metric, metric, conversion | YES — CP-10 |
| event tracking, track click | YES — CP-9 + CP-10 |
| result page, visitor count, event count | YES — CP-10 |

### Anti-Pattern (KHÔNG được lặp lại)

**SAI:**
> "Full Flow Focus: Phase 1 (Events) → generated 47 TCs"
> *(Missing: không có instruction nào để web-create-test-cases biết cần Results page)*

**ĐÚNG:**
> "Full Flow TC Required: Type = Event Full Flow. Must include Results page = YES.
> Checkpoints: CP-9 (live site network request 204) + CP-10 (Results page event count)"

---

## 6. Anti-Patterns

### Testing Only the AC
**Problem**: Missing broader changes that the PR introduced
**Solution**: Always read the PR diffs, not just the ticket

### Making Everything P0
**Problem**: No prioritization means everything is "critical"
**Solution**: P0 should be 2-3 items maximum. If the ticket fails P0, it's not done.

### Vague Verification
**Problem**: "Check that it works" — what does "works" mean?
**Solution**: Be specific: "Verify the Segment event payload contains `thread_id` with a non-empty string value"

### Ignoring Follow-up PRs
**Problem**: The original PR may have been followed by fixes
**Solution**: Search git log for related commits after the main PR merge date

### Not Reading the Epic
**Problem**: Missing context about the broader feature
**Solution**: Always fetch the epic and scan sibling tickets for context

---

## 7. Quality Checklist

Before presenting the analysis:

- [ ] All PRs (including follow-ups) have been read and analyzed
- [ ] Changes are categorized (tracking, UI, state, API, etc.)
- [ ] Scope of impact is identified (isolated, moderate, broad)
- [ ] Discrepancies between AC and actual implementation are noted
- [ ] Test cases are prioritized (P0 < P1 < P2 < P3)
- [ ] Each test case has a specific verification method
- [ ] Regression areas are identified
- [ ] P0 test cases are minimal and focused (2-5 items)
- [ ] Total test count is reasonable (10-20 for a typical ticket)
- [ ] No vague language ("check it works", "test saving")
