# Sample: Multi-Agent Execution

## User Request

> Analyze CJS-100, CJS-101, and review PR #45

## Execution

### Step 1: Parse Tasks

Identified 3 tasks from user input:
- T1: Analyze ticket CJS-100
- T2: Analyze ticket CJS-101
- T3: Review PR #45

### Step 2: Task Plan

```
Task Plan:
- T1: /exp-qa-agents:analyze-ticket CJS-100 [parallel]
- T2: /exp-qa-agents:analyze-ticket CJS-101 [parallel]
- T3: /exp-qa-agents:review-github-pr-cypress-js PR #45 [parallel]

Parallel groups: [T1, T2, T3]
Sequential dependencies: none

Proceed? (y/n)
```

User confirmed: "Yes"

### Step 3: Dispatch Agents

All 3 agents launched in parallel with `run_in_background: true`.

### Step 4: Agent Results

**T1: analyze-ticket CJS-100 -- Completed**
- Ticket: CJS-100 "Add audience targeting to experiments"
- Type: Feature
- 5 acceptance criteria identified
- Linked Confluence page found with design specs
- Figma design attached with 3 screens
- User reviewed and approved

**T2: analyze-ticket CJS-101 -- Completed**
- Ticket: CJS-101 "Fix experiment status not updating"
- Type: Bug
- 2 acceptance criteria identified
- Steps to reproduce found in comments
- No linked Confluence or Figma
- User reviewed and approved

**T3: review-github-pr-cypress-js PR #45 -- Completed**
- PR: #45 "Add audience page object and test"
- Files changed: 4 (2 page objects, 1 spec, 1 builder)
- Code quality: 8/10
- Findings: 2 minor convention issues (missing region comments, unused import)
- User reviewed and approved

### Step 5: Consolidated Report

```
Multi-Agent Execution Report

| Task | Skill | Target | Status | Key Findings |
|------|-------|--------|--------|--------------|
| T1 | analyze-ticket | CJS-100 | Approved | Feature, 5 ACs, Confluence + Figma linked |
| T2 | analyze-ticket | CJS-101 | Approved | Bug, 2 ACs, repro steps in comments |
| T3 | review-github-pr | PR #45 | Approved | 8/10 quality, 2 minor issues |

Cross-Ticket Insights:
- CJS-100 (audience targeting) and PR #45 (audience page object) are related
- PR #45 may partially address CJS-100 requirements
```
