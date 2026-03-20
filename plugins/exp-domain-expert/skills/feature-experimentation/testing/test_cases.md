# Test Cases for feature-experimentation

## Overview
Test cases for feature-experimentation domain expert skill.

## Test Categories

### 1. Knowledge Accuracy

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-001 | Flag creation | "How do I create a feature flag?" | Accurate steps: project, flag name, variables, variations, environments |
| TC-002 | Flag rules | "What types of rules can I add to a flag?" | Lists A/B test, targeted delivery, rollout, and CMAB with descriptions |
| TC-003 | SDK bucketing | "How does user bucketing work?" | Explains MurmurHash, traffic allocation, consistent bucketing by user ID |
| TC-004 | Sticky bucketing | "What is sticky bucketing?" | Explains persisted decisions, use cases, and SDK configuration |
| TC-005 | CMAB explanation | "How does CMAB optimize traffic?" | Explains contextual attributes, exploration/exploitation, dynamic allocation |

### 2. SDK-Specific Knowledge

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-006 | SDK comparison | "What is the difference between decide and activate?" | Explains decide (current) vs activate (legacy), return types, usage |
| TC-007 | Datafile | "How does the datafile work?" | Describes JSON config, CDN hosting, polling, and SDK initialization |

### 3. Edge Cases

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-008 | Cross-product boundary | "How do I use the Visual Editor with feature flags?" | Clarifies VE is Web Experimentation only, suggests appropriate approach |
