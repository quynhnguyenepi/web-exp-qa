# Test Cases for evaluate-skills

## Overview

Test cases to validate the evaluate-skills skill itself (meta-evaluation).

## Test Categories

### 1. Pre-Flight
| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-001 | Single skill target | `evaluate-skills analyze-ticket` | Discovers and evaluates only analyze-ticket |
| TC-002 | Plugin-wide target | `evaluate-skills --plugin common-qa` | Discovers and evaluates all common-qa skills |
| TC-003 | Missing test_cases.md | Skill with no testing/test_cases.md | Reports error, skips skill, continues |
| TC-004 | Empty test_cases.md | Skill with empty test_cases.md | Reports error, skips skill, continues |
| TC-005 | No input provided | `evaluate-skills` (no args) | Asks user which skill(s) to evaluate |

### 2. Test Case Parsing
| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-006 | Standard table format | Well-formatted test_cases.md | Parses all test cases correctly |
| TC-007 | Multiple categories | test_cases.md with 3+ categories | Groups test cases by category |
| TC-008 | Malformed table | Missing columns in table | Reports parsing error, skips malformed rows |

### 3. Execution
| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-009 | Simulation mode (default) | No --live flag | Runs in simulation mode, no MCP calls |
| TC-010 | Live mode opt-in | `--live` flag | Runs in live mode with actual MCP calls |
| TC-011 | Parallel category execution | Skill with 3+ categories | Dispatches one agent per category in parallel |
| TC-012 | Agent failure | Agent crashes during execution | Retries once, then records as error |

### 4. Result Recording
| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-013 | Valid evaluations.json | Completed evaluation | Writes valid JSON matching schema |
| TC-014 | Summary counts | 10 tests: 8 pass, 1 fail, 1 error | Summary shows total:10, passed:8, failed:1, errors:1, pass_rate:80% |
| TC-015 | Overwrites previous results | evaluations.json already has data | Replaces with new results |

### 5. Reporting
| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-016 | Single skill report | One skill evaluated | Shows per-category breakdown table |
| TC-017 | Multi-skill report | Three skills evaluated | Shows cross-skill summary + per-skill details |
| TC-018 | All pass report | All test cases pass | Reports 100% pass rate |
| TC-019 | Failed-only re-run | `--failed-only` flag | Re-executes only previously failed/errored tests |

## Success Criteria

- [ ] All test categories covered
- [ ] Simulation mode works without MCP servers
- [ ] evaluations.json schema matches guidelines.md specification
- [ ] Parallel execution dispatches correctly
- [ ] Report format is clear and actionable

## Known Limitations (v1)

- Simulation mode cannot validate actual MCP responses
- Live mode requires manual setup of test data
- No automated scheduling (must be invoked manually)
