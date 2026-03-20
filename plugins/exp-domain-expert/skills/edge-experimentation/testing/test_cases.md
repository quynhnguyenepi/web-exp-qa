# Test Cases for edge-experimentation

## Overview
Test cases for edge-experimentation domain expert skill.

## Test Categories

### 1. Knowledge Accuracy

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-001 | Performance Edge overview | "What is Performance Edge?" | Explains edge-side decision making, CDN integration, performance benefits |
| TC-002 | Edge decider | "How does the edge decider work?" | Describes decision logic at CDN edge, variation assignment, response headers |
| TC-003 | Microsnippet details | "What is the microsnippet and how big is it?" | Describes lightweight loader, approximate size, role in edge architecture |
| TC-004 | Flicker prevention | "How does Edge prevent flicker?" | Explains decisions before page render, no client-side evaluation delay |
| TC-005 | CDN compatibility | "Which CDNs support Performance Edge?" | Lists supported CDN providers and integration requirements |

### 2. Comparison Questions

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-006 | Edge vs client-side | "What are the tradeoffs between edge and client-side?" | Compares latency, feature parity, setup complexity, and use cases |
| TC-007 | Feature parity | "What features are not supported at the edge?" | Lists client-side-only features with explanations |

### 3. Edge Cases

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-008 | SDK question mismatch | "Can I use the JavaScript SDK with Performance Edge?" | Clarifies Edge uses snippet-based approach, not SDK; routes SDK questions appropriately |
