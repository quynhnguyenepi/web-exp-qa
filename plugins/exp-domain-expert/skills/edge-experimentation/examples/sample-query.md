# Sample Query: edge-experimentation

## Question
"What is the microsnippet and how does it differ from the standard Optimizely snippet?"

## Answer
The **microsnippet** is a lightweight JavaScript snippet used with Optimizely Performance Edge. It replaces the standard full-size Optimizely snippet for edge-enabled experiments.

### Key Differences

| Aspect | Standard Snippet | Microsnippet |
|--------|-----------------|--------------|
| Size | Full snippet (~80-200KB) | Minimal loader (~5KB) |
| Execution | Client-side decisions | Decisions made at edge, applied client-side |
| Flicker | Possible (mitigated with anti-flicker) | Eliminated (decisions happen before page load) |
| Latency | Depends on snippet load time | Near-zero decision latency |
| Feature parity | Full feature set | Subset of features supported at edge |

### How It Works
1. The microsnippet is placed on the page like the standard snippet.
2. When a visitor requests the page, the CDN edge worker intercepts the request.
3. The edge decider evaluates experiment conditions and assigns a variation.
4. The decision is passed to the microsnippet via response headers or cookies.
5. The microsnippet applies the assigned variation changes immediately, before the page renders.

### When to Use
- High-traffic pages where performance is critical.
- Experiments where flicker is unacceptable.
- Sites already using a supported CDN provider.
