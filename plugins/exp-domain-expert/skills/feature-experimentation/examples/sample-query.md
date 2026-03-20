# Sample Query: feature-experimentation

## Question
"What is CMAB and when should I use it instead of a standard A/B test?"

## Answer
**CMAB (Contextual Multi-Armed Bandit)** is an optimization method in Optimizely Feature Experimentation that uses machine learning to dynamically allocate traffic to variations based on user context (attributes).

### How CMAB Works
- Instead of fixed traffic allocation, CMAB continuously learns which variation performs best for different user segments.
- It uses contextual attributes (e.g., device type, location, user tier) to personalize variation assignment.
- The algorithm balances **exploration** (testing underexplored variations) with **exploitation** (sending more traffic to winning variations).

### When to Use CMAB vs A/B Test

| Criteria | Standard A/B Test | CMAB |
|----------|------------------|------|
| Goal | Find one overall winner | Find best variation per context |
| Traffic | Fixed allocation | Dynamic allocation |
| Duration | Run to statistical significance | Continuously optimizes |
| Best for | Clear hypothesis testing | Personalization at scale |
| Attributes | Not used for bucketing | Used to optimize assignment |

### When to Choose CMAB
- You have meaningful user attributes that may influence conversion.
- You want ongoing optimization rather than a one-time winner.
- You have sufficient traffic volume for the algorithm to learn.

### When to Stick with A/B
- You need a definitive statistical result for a specific hypothesis.
- You have limited traffic or few distinguishing user attributes.
- Regulatory or compliance requirements demand fixed allocation.
