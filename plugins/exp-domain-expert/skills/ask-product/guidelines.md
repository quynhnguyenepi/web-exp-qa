# Guidelines for ask-product

## Purpose
This skill is an orchestrator that routes product questions to the appropriate domain expert skill. It does not hold domain knowledge itself.

## Routing Rules
- Questions about A/B tests, Visual Editor, audiences, pages, events -> web-experimentation
- Questions about feature flags, rules, SDKs, bucketing, CMAB -> feature-experimentation
- Questions about Performance Edge, edge decider, microsnippet -> edge-experimentation
- Questions about Opal AI assistant capabilities -> opal-chat
- Questions about terminology or cross-product comparisons -> product-glossary

## Usage Guidelines
- Always identify the correct domain before routing.
- If a question spans multiple domains, dispatch to each relevant expert in parallel.
- Combine responses into a single cohesive answer for the user.
- If the domain cannot be determined, ask the user for clarification.
- Never fabricate product knowledge; rely on the domain expert sub-skills.

## Error Handling
- If a domain expert skill is unavailable, inform the user and suggest alternatives.
- Log routing decisions for traceability.
