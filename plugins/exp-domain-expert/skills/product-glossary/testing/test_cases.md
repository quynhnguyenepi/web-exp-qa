# Test Cases for product-glossary

## Overview
Test cases for product-glossary domain expert skill.

## Test Categories

### 1. Knowledge Accuracy

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-001 | Core term definition | "What is a variation?" | Defines variation in context of both Web and Feature Experimentation |
| TC-002 | Cross-product comparison | "What is the difference between a page and a flag?" | Explains page (Web) vs flag (Feature) with clear distinctions |
| TC-003 | Acronym expansion | "What does CMAB stand for?" | Contextual Multi-Armed Bandit, with brief explanation |
| TC-004 | Deprecated term mapping | "What is Optimizely Classic?" | Maps Classic to current platform, explains migration context |
| TC-005 | Ambiguous term | "What is an 'event' in Optimizely?" | Distinguishes click events, custom events, pageview events across products |

### 2. Comparison Queries

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-006 | Web vs FX terms | "Compare Web and Feature Experimentation terminology" | Side-by-side mapping of equivalent concepts |
| TC-007 | Related terms | "What is the difference between a rollout and a targeted delivery?" | Clear distinction with use cases for each |

### 3. Edge Cases

| ID | Name | Input | Expected Outcome |
|----|------|-------|------------------|
| TC-008 | Non-Optimizely term | "What is a control group?" | Provides general definition contextualized to Optimizely (Original variation) |
