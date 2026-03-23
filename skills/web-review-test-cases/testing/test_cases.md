# Review Test Cases - Test Cases

## TC-001: Review test cases from JIRA with full coverage

**Preconditions:** Atlassian MCP is connected. JIRA ticket has linked test cases with clear ACs.

**Steps:**
1. Invoke skill with a JIRA ticket ID that has 5 linked test cases
2. Skill fetches test cases from JIRA
3. Skill fetches requirements (ACs, Confluence, attachments) in parallel
4. Quality review and coverage review run in parallel
5. Review report is generated and presented

**Expected Results:**
- All 5 test cases are fetched and listed
- Each test case receives a quality grade (A/B/C/D)
- Coverage analysis maps each AC to test cases
- Gaps are identified with priority classification
- Report includes quality summary, per-TC details, coverage analysis, and recommendations
- User is offered actions (fix in JIRA, generate missing, export, done)

## TC-002: Review test cases from pasted text

**Preconditions:** No Atlassian MCP required. User provides test cases as pasted text.

**Steps:**
1. Invoke skill without a JIRA ticket
2. User pastes test cases as text
3. Skill asks user for requirements/AC context
4. User provides AC text
5. Skill reviews quality and coverage

**Expected Results:**
- Test cases are parsed from pasted text regardless of format
- User is prompted for requirements since no JIRA source
- Quality and coverage reviews proceed normally
- Report is generated without JIRA-specific references

## TC-003: Coverage gap detection with missing negative cases

**Preconditions:** Atlassian MCP is connected. Ticket has ACs covering error scenarios.

**Steps:**
1. Invoke skill with a ticket that has error-handling ACs
2. Test cases only cover happy paths
3. Coverage analysis runs

**Expected Results:**
- Negative case ACs are marked as GAP
- Missing test cases table includes error scenarios with appropriate priority
- Recommendations highlight the need for negative test cases
- Coverage percentage accurately reflects the gaps

## TC-004: Quality-only review (skip coverage)

**Preconditions:** Atlassian MCP is connected.

**Steps:**
1. Invoke skill with a JIRA ticket
2. User requests "only review quality, skip coverage"
3. Skill runs quality review only

**Expected Results:**
- Coverage analysis (Step 4) is skipped per self-correction rule
- Quality report is complete with per-TC grades and suggestions
- No coverage section in the report
- No "missing test cases" table

## TC-005: Large test suite review (>50 test cases)

**Preconditions:** Atlassian MCP is connected. More than 50 test cases are linked.

**Steps:**
1. Invoke skill with a ticket or set of tickets with 60 test cases
2. Skill detects the count exceeds 50

**Expected Results:**
- Skill processes test cases in batches of 20
- Incremental results are presented after each batch
- Final consolidated report covers all 60 test cases
- Quality summary and coverage analysis span the full set
