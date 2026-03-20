# Sample Query: product-glossary

## Question
"What is the difference between a 'flag' and an 'experiment' in Optimizely?"

## Answer

### Flag
A **flag** is a Feature Experimentation concept. It represents a feature toggle that controls whether a feature is enabled or disabled for users. Flags have:
- **Variations**: Different configurations of the feature (e.g., on/off, or multiple variable combinations).
- **Variables**: Configurable values within a flag (e.g., button color, copy text).
- **Rules**: Logic that determines which users see which variation (targeted delivery, A/B test, CMAB).
- **Environments**: Flags can be configured independently per environment (development, staging, production).

### Experiment
An **experiment** has different meanings depending on the product:

| Aspect | Web Experimentation | Feature Experimentation |
|--------|--------------------|-----------------------|
| Definition | A standalone A/B or MVT test | A rule type within a flag |
| Created in | Experiment list page | Inside a flag's rules |
| Targeting | Page-based URL targeting | Attribute-based audience targeting |
| Changes | Visual Editor or code changes | Flag variable values per variation |
| Execution | Client-side (snippet) | Server-side or client-side (SDK) |

### Key Distinction
In **Web Experimentation**, an experiment is a top-level entity. In **Feature Experimentation**, an experiment is a type of rule attached to a flag. A flag can have multiple rules, including experiments, rollouts, and targeted deliveries.

### Related Terms
- **Rollout**: A flag rule that delivers a variation to a percentage of users without measurement.
- **Targeted Delivery**: A flag rule that delivers a specific variation to a defined audience.
- **Campaign**: A Web Experimentation term for personalization (distinct from experiments).
