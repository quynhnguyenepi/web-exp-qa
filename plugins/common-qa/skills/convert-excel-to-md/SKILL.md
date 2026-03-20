---
description: Convert Excel (.xlsx/.xls/.csv) test case files to standardized Markdown format. Handles both single-row and multi-row test case layouts. Use when you need to convert spreadsheet test cases into Markdown for review, JIRA upload, or further processing by other skills.
---

## Dependencies

- **MCP Servers:** None
- **Related Skills:** `/exp-qa-agents:review-test-cases`, `/exp-qa-agents:create-test-cases`

# Convert Excel Test Cases to Markdown

Parse Excel test case files and produce a clean, standardized Markdown file that can be consumed by `/exp-qa-agents:review-test-cases` and other skills.

## When to Use

Invoke this skill when you need to:

- Convert an Excel (.xlsx/.xls) or CSV file containing test cases into Markdown
- Standardize test case format before running a review
- Import test cases from spreadsheets into a format compatible with JIRA upload skills

## Workflow Overview

```
Pre-Flight -> Parse Excel -> Detect Layout -> Group Test Cases -> Generate Markdown -> User Confirmation
```

## Execution Workflow

### Step 0: Pre-Flight Checks

1. **Validate file:** Check the file exists and has a supported extension (`.xlsx`, `.xls`, `.csv`).
2. **Check Python dependency:** Run `python3 -c "import openpyxl"`. If it fails, install: `pip3 install openpyxl`.
3. **For .csv files:** No extra dependency needed, use Python's built-in `csv` module.

### Step 1: Parse Excel File

Use Bash to extract all rows from the Excel file:

**For .xlsx/.xls:**
```bash
python3 -c "
import openpyxl, json, sys
wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
for sheet in wb.sheetnames:
    ws = wb[sheet]
    rows = [[str(c.value) if c.value is not None else '' for c in r] for r in ws.iter_rows()]
    print(f'=== Sheet: {sheet} ===')
    for i, r in enumerate(rows):
        print(f'Row {i}: ' + '\t|\t'.join(r))
" "/path/to/file.xlsx"
```

**For .csv:**
```bash
python3 -c "
import csv, sys
with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        print(f'Row {i}: ' + '\t|\t'.join(row))
" "/path/to/file.csv"
```

**Multi-sheet handling:**
- Skip metadata/internal sheets (sheets with random hex names, single-row sheets, or sheets with only encoded data)
- If multiple valid sheets exist, process each sheet separately and ask user which to convert
- If only one valid sheet, proceed automatically

### Step 2: Detect Column Mapping

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

If column mapping is ambiguous or headers are not recognized, present the detected headers and ask the user to confirm mapping via AskUserQuestion:
```
Detected columns: A={col1}, B={col2}, C={col3}, ...

Please confirm the column mapping:
- Which column is Title?
- Which column is Test Step?
- Which column is Expected Result?
```

### Step 3: Detect Layout and Group Test Cases

**CRITICAL:** Test cases in Excel can follow different layouts. Detect which one and group accordingly.

#### Layout A: Multi-Row Test Cases (grouped rows)

**Pattern:** A row with a non-empty **Title** column starts a new test case. Subsequent rows with an **empty Title** belong to the same test case as individual steps.

```
Row 1: [Title: "Verify login"]  [Step: "Pre-con: user exists"]  [Result: ""]        [Priority: High]
Row 2: [Title: ""]              [Step: "Enter email"]            [Result: "Field accepts input"]
Row 3: [Title: ""]              [Step: "Click Login"]            [Result: "Dashboard loads"]
Row 4: [Title: "Verify logout"] [Step: "Pre-con: user logged in"] [Result: ""]       [Priority: Normal]
Row 5: [Title: ""]              [Step: "Click Logout"]           [Result: "Login page shown"]
```

**Grouping rules:**
- New test case starts when Title column is non-empty
- The first row of a test case may contain preconditions in the Step column (look for "Pre-con:", "Precondition:", or the step is not an actionable step)
- All subsequent rows with empty Title are steps belonging to the current test case
- Priority, Parameters, Labels from the title row apply to the entire test case
- Steps are numbered sequentially starting from 1 (skip the precondition row)

#### Layout B: Single-Row Test Cases

**Pattern:** Each row is a complete test case. Steps and expected results are packed into single cells, separated by line breaks (`\n`), `<br>`, numbered lists, or semicolons.

```
Row 1: [Title: "Verify login"] [Step: "1. Enter email\n2. Click Login"] [Result: "1. Field accepts\n2. Dashboard loads"] [Priority: High]
```

**Parsing rules:**
- Split step/result cells by: `\n`, `<br>`, numbered prefix (`1.`, `2.`), or semicolons
- Match step numbers to result numbers
- If steps have numbers but results don't (or vice versa), split by line breaks and pair sequentially

#### Layout Detection Logic

1. Count rows where Title is non-empty vs total data rows
2. If Title-filled rows << total rows (ratio < 0.5) -> **Layout A** (multi-row)
3. If Title-filled rows ~= total rows (ratio >= 0.5) -> **Layout B** (single-row)
4. If mixed, ask user to confirm

### Step 4: Generate Markdown Output

Write output to `{input_filename}_Test_Cases.md` in the same directory as the input file.

**Output format (matches create-test-cases standard):**

```markdown
# Test Cases - {filename}

**Source:** {file_path}
**Sheet:** {sheet_name}
**Total Test Cases:** {count}
**Converted:** {timestamp}

## Summary

| # | Title | Priority | Labels |
|---|-------|----------|--------|
| TC-01 | {title} | {priority} | {labels} |
| TC-02 | {title} | {priority} | {labels} |

---

### TC-01: {title}

**Priority:** {priority} | **Labels:** {labels}

**Pre-condition:**
- {precondition text}

**Parameters:**
- {parameter text}

**Test Steps:**
1. {step 1}
2. {step 2}
3. {step 3}

**Expected Results:**
1. {result 1}
2. {result 2}
3. {result 3}

---

### TC-02: {title}
...
```

**Formatting rules:**
- Trim whitespace from all cell values
- Replace `\n` in cells with proper markdown line breaks
- If a step has no corresponding expected result, write: `{N}. (no expected result specified)`
- If an expected result has no corresponding step, skip it
- Clean up typos in precondition labels: "Pre-con:" -> "Pre-condition:"
- Preserve original priority values (High/Normal/Low or P0-P3)
- If priority is empty, set to "Normal" (default)

### Step 5: Present Summary and Confirm

After generating the file, present:

```
Converted {N} test cases from "{filename}" to Markdown.

Output: {output_file_path}

Test Cases:
TC-01: {title} ({step_count} steps)
TC-02: {title} ({step_count} steps)
...

Would you like to:
1. Review these test cases now (invoke /exp-qa-agents:review-test-cases)
2. Open the generated file
3. Adjust conversion (re-map columns, fix grouping)
```

---


**Cost optimization:** Progress Tracking, Error Handling, Self-Correction, and Notes sections are in guidelines.md to reduce auto-loaded context size.
