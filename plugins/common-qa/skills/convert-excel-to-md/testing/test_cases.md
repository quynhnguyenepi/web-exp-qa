# Test Cases - convert-excel-to-md

## TC-01: Convert multi-row Excel with standard columns

**Input:** Excel file with multi-row layout (Title, Test Step, Expected Result, Priority columns)
**Expected:** Markdown file with grouped test cases, numbered steps, preconditions extracted

## TC-02: Convert single-row Excel with embedded steps

**Input:** Excel file where each row is a complete test case with steps separated by newlines
**Expected:** Markdown file with steps split into numbered lists

## TC-03: Handle missing expected results

**Input:** Excel file where some steps have no expected result
**Expected:** Markdown output contains "(no expected result specified)" for missing results

## TC-04: Handle multiple sheets

**Input:** Excel file with 2+ valid sheets and 1 metadata sheet
**Expected:** Metadata sheet is skipped, user is asked which valid sheet(s) to convert

## TC-05: Handle CSV input

**Input:** CSV file with standard columns
**Expected:** Markdown file with test cases parsed from CSV (no openpyxl needed)

## TC-06: Handle ambiguous column headers

**Input:** Excel file with non-standard column names
**Expected:** User is prompted to confirm column mapping via AskUserQuestion

## TC-07: Handle empty Excel file

**Input:** Excel file with only header row, no data
**Expected:** Error reported: "No test cases found", user asked to check the file
