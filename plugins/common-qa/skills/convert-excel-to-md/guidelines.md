# Convert Excel to Markdown - Guidelines

Detailed reference material for parsing Excel test case files into standardized Markdown format.

---

## 1. Column Detection Rules

Auto-detect columns by matching header row (Row 0) against known names (case-insensitive, partial match):

| Target Field | Match Keywords |
|-------------|---------------|
| **Title** | `title`, `test case`, `name`, `summary`, `test name` |
| **Test Step** | `test step`, `step`, `action`, `procedure` |
| **Expected Result** | `expected result`, `expected`, `result`, `outcome` |
| **Priority** | `priority`, `severity`, `importance` |
| **Preconditions** | `precondition`, `pre-condition`, `prerequisite`, `pre-con` |
| **Parameters** | `parameter`, `test data`, `data`, `input` |
| **Labels** | `label`, `tag`, `category`, `type` |

---

## 2. Layout Detection

### Layout A: Multi-Row Test Cases

**Pattern:** A row with a non-empty Title column starts a new test case. Subsequent rows with empty Title belong to the same test case.

**Indicators:**
- Title-filled rows << total rows (ratio < 0.5)
- First row of each TC may contain preconditions in the Step column

**Grouping rules:**
- New test case starts when Title column is non-empty
- First step row may be a precondition (look for "Pre-con:", "Precondition:")
- Steps are numbered sequentially starting from 1 (skip precondition row)
- Priority, Parameters, Labels from the title row apply to entire TC

### Layout B: Single-Row Test Cases

**Pattern:** Each row is a complete test case. Steps and expected results are in single cells, separated by line breaks or numbered lists.

**Indicators:**
- Title-filled rows ~= total rows (ratio >= 0.5)

**Parsing rules:**
- Split step/result cells by: `\n`, `<br>`, numbered prefix (`1.`, `2.`), or semicolons
- Match step numbers to result numbers sequentially

---

## 3. Common Issues to Handle

| Issue | How to Handle |
|-------|--------------|
| Empty expected results | Write "(no expected result specified)" -- downstream skills flag this |
| Merged cells in Excel | openpyxl reads merged cells as the value in the top-left cell; others are None |
| Extra whitespace | Trim all cell values |
| `\n` in cells | Replace with proper markdown line breaks |
| Typos in precondition labels | Normalize: "Pre-con:" -> "Pre-condition:" |
| Missing priority | Default to "Normal" |
| Internal/metadata sheets | Skip sheets with random hex names, single-row sheets, or encoded data |

---

## 4. Output Format Standards

The output Markdown must match the format used by `/exp-qa-agents:create-test-cases`:

- Summary table at top with all TCs
- Detailed cards below with `### TC-XX:` headings
- Bold field labels: `**Priority:**`, `**Pre-condition:**`, `**Parameters:**`, `**Test Steps:**`, `**Expected Results:**`
- Numbered lists for steps and expected results
- Horizontal rules (`---`) between test cases

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list.

```
TodoWrite([
  { content: "Run pre-flight checks (validate file exists, install dependencies)", status: "in_progress", activeForm: "Running pre-flight checks" },
  { content: "Parse Excel file and detect column mapping", status: "pending", activeForm: "Parsing Excel file" },
  { content: "Detect layout and group test cases", status: "pending", activeForm: "Detecting layout and grouping test cases" },
  { content: "Generate Markdown output file", status: "pending", activeForm: "Generating Markdown file" },
  { content: "Present summary and confirm with user", status: "pending", activeForm: "Presenting summary to user" }
])
```

---


## Error Handling

| Error | Action |
|-------|--------|
| File not found | Ask user to provide correct file path |
| openpyxl not installed | Install via `pip3 install openpyxl`, retry |
| No recognizable headers | Show all column values from Row 0, ask user to map |
| No test cases found (all rows empty) | Report empty file, ask user to check the file |
| Mixed layouts in same sheet | Ask user which layout to apply |
| Encoding errors | Try `utf-8`, fall back to `latin-1`, then ask user |

---


## Self-Correction

1. **"Column X is actually the title"** -> Re-map columns and regenerate
2. **"These rows are not test cases"** -> Skip specified rows, regenerate
3. **"Merge sheet A and sheet B"** -> Combine test cases from both sheets into one file
4. **"Use a different output format"** -> Adjust markdown structure per user preference
5. **"Steps are grouped wrong"** -> Switch between Layout A/B detection, regenerate

---


## Notes

- This skill produces a Markdown file as output. It does NOT review or judge test case quality. Use `/exp-qa-agents:review-test-cases` for that.
- The output format matches the standard used by `/exp-qa-agents:create-test-cases`, so all downstream skills can consume it directly.
- For JIRA-attached Excel files, first download using `/common-qa:read-attachments`, then run this skill on the downloaded file.
