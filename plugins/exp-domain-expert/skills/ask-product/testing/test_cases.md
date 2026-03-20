# Test Cases for ask-product

## Overview
Test cases for ask-product domain expert skill (orchestrator).

## Test Categories

### 1. Routing Accuracy

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-001 | Route to web-experimentation | "How do I create an A/B test in the Visual Editor?" | Routes to web-experimentation expert |
| TC-002 | Route to feature-experimentation | "How does sticky bucketing work in the SDK?" | Routes to feature-experimentation expert |
| TC-003 | Route to edge-experimentation | "What is the microsnippet?" | Routes to edge-experimentation expert |
| TC-004 | Route to opal-chat | "Can Opal summarize my experiment results?" | Routes to opal-chat expert |
| TC-005 | Route to product-glossary | "What is the difference between a flag and an experiment?" | Routes to product-glossary expert |

### 2. Multi-Domain Routing

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-006 | Cross-domain question | "How does audience targeting differ between Web and Feature Experimentation?" | Routes to web-experimentation, feature-experimentation, and product-glossary in parallel |
| TC-007 | Ambiguous question | "Tell me about experiments" | Routes to product-glossary for disambiguation or asks user for clarification |

### 3. Error Handling

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-008 | Out-of-scope question | "How do I configure a CMS page?" | Informs user the question is outside the domain scope |
