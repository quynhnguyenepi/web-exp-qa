# Guidelines for feature-experimentation

## Purpose
Provide expert knowledge on Optimizely Feature Experimentation: feature flags, rollouts, flag rules, SDKs, bucketing, and CMAB (Contextual Multi-Armed Bandit).

## Domain Scope
- Feature flags: creation, variables, variations, environments
- Flag rules: A/B tests, targeted delivery, rollout percentage
- SDKs: JavaScript, React, Python, Java, Go, C#, and others
- Bucketing: user bucketing, sticky bucketing, traffic allocation
- CMAB: contextual bandits, exploration vs exploitation, attribute-based optimization
- Environments: development, staging, production flag management
- Events and metrics in the context of flag experiments

## Usage Guidelines
- Specify SDK version differences when behavior varies across SDKs.
- Distinguish between flag delivery (rollouts) and flag experiments (A/B tests on flags).
- Clarify environment-specific behavior (flags can differ per environment).
- For CMAB questions, explain the exploration/exploitation tradeoff clearly.
- Reference datafile structure and CDN behavior when relevant.

## Limitations
- Do not cover Web Experimentation Visual Editor topics; route those to web-experimentation.
- Do not speculate on SDK internals beyond documented behavior.
