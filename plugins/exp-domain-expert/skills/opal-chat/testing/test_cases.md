# Test Cases for opal-chat

## Overview
Test cases for opal-chat domain expert skill.

## Test Categories

### 1. Knowledge Accuracy

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-001 | Brainstorm capability | "Can Opal help me brainstorm experiment ideas?" | Describes brainstorm feature, input expectations, output format |
| TC-002 | Result summarization | "How does Opal summarize results?" | Explains plain-language summaries, what metrics are covered, confidence levels |
| TC-003 | Experiment review | "What does Opal check when reviewing an experiment?" | Lists setup quality checks, sample size, metric config, audience overlap |
| TC-004 | Access and location | "Where do I find Opal in the UI?" | Describes Opal icon location, supported pages, how to invoke |
| TC-005 | Limitations | "What can Opal not do?" | Lists limitations: no direct changes, AI-generated caveats, scope boundaries |

### 2. Usage Scenarios

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-006 | Actionable advice | "Opal says my experiment needs more traffic. What does that mean?" | Explains sample size requirements, MDE, and recommended actions |
| TC-007 | Feature availability | "Is Opal available on all plans?" | Clarifies plan tier requirements and feature availability |

### 3. Edge Cases

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-008 | Conflation with external AI | "Can Opal integrate with ChatGPT?" | Clarifies Opal is Optimizely's built-in AI, not an external integration point |
