# Sample Query: ask-product

## Question
"How does audience targeting differ between Web Experimentation and Feature Experimentation?"

## Routing Decision
This question spans two domains (web-experimentation and feature-experimentation) and involves terminology comparison (product-glossary). The orchestrator dispatches to all three experts in parallel.

## Combined Answer
**Web Experimentation** uses audience conditions defined in the Optimizely UI, evaluated client-side via the snippet. Audiences are based on attributes like URL, cookies, custom JavaScript conditions, and third-party integrations. Audiences are shared across experiments within a project.

**Feature Experimentation** uses audience conditions evaluated server-side (or in the SDK). Audiences are defined using user attributes passed to the SDK's `decide` method. Attributes are developer-defined and passed programmatically at runtime.

**Key Differences:**
| Aspect | Web Experimentation | Feature Experimentation |
|--------|--------------------|-----------------------|
| Evaluation | Client-side (browser) | Server-side (SDK) |
| Attribute source | Browser context, cookies, JS | Developer-passed attributes |
| Configuration | UI-based conditions | UI + code-based attributes |
| Sharing | Project-level | Project-level per environment |
