---
description: Optimizely Experimentation domain glossary and terminology reference. Use when encountering unfamiliar product terms, explaining concepts to team members, or ensuring correct terminology in test cases and documentation. Covers Web Experimentation, Feature Experimentation, Edge Delivery, Opal Chat, and supporting services.
---

## Dependencies

- **MCP Servers (optional):** `optimizely-prod` - Query real entity schemas for accurate field definitions
  - `exp_get_schemas` - Get entity schemas to verify field names, types, and valid enum values when defining terminology

### When to Use MCP vs Static Knowledge

| Question Type | Source | Example |
|---|---|---|
| "What is X?" | Static knowledge (this file) | "What is bucketing?" |
| "What fields does entity X have?" | MCP `exp_get_schemas` | "What fields does an audience entity have?" |

### Source Repositories
- **Documentation repos:** `web-docs`, `fx-docs`, `edge-docs` repositories at `docs/` directories
- **Dev repos:** All Optimizely Experimentation repositories — terminology consolidated from `optimizely`, `flags`, `flags-scheduling`, `edge-delivery`, `opal-tools`, `idea-builder`, `visual-editor`, `change-history`, `permission-service`, `datafile-build-service`, `datafile-access-tokens`, `appx-changelog-elasticsearch`

## Role

You are an Optimizely terminology expert. When asked about product terms, you provide clear, accurate definitions with context about how each concept relates to testing and QA.

**Full reference:** See reference.md for the complete A-Z glossary, full entity relationship diagram, and service architecture table.

## Key Terms Quick Reference

| Term | Definition |
|---|---|
| **A/B Test** | Experiment splitting traffic between variations to measure impact |
| **Audience** | Group of visitors defined by targeting conditions |
| **Bucketing** | Deterministic assignment of visitors to variations (MurmurHash3) |
| **Campaign** | (Web) Personalization delivering targeted experiences |
| **CMAB** | Contextual Multi-Armed Bandit; AI-powered per-user optimization |
| **Datafile** | (FX) JSON config with all flag/variation/rule definitions |
| **DBS** | Datafile Build Service; builds and publishes FX datafiles |
| **Edge Decider** | Server-side component making bucketing decisions at edge |
| **Environment** | (FX) Isolated context for flags (dev/staging/prod) |
| **Event** | User action tracked for measurement (click, pageview, custom) |
| **Exclusion Group** | Ensures visitor sees only one experiment across group |
| **Flag** | (FX) Feature flag toggled on/off with variables and variations |
| **Holdout** | (FX) Control group for cumulative experiment impact |
| **Idea Builder** | AI-powered test idea generation service |
| **Layer** | Internal name for campaign/experiment container |
| **MAB** | Multi-Armed Bandit; auto-optimizes traffic to winners |
| **Metric** | Measurement tied to an event for experiment success criteria |
| **Microsnippet** | (Edge) Lightweight JS per visitor/page from Edge Decider |
| **Opal** | AI assistant with chat, brainstorm, summarize, review capabilities |
| **Page** | (Web) URL patterns where experiments activate |
| **Permission Service** | Granular entity-level authorization (admin>publish>toggle>edit>view>none) |
| **Rule** | (FX) Config on flag for targeting/traffic/variations (delivery, a/b, mab, cmab) |
| **Ruleset** | (FX) Container for rules per flag+environment |
| **Schedule** | (FX) Planned future flag/rule change (2min-90day window) |
| **Shadow DOM** | (VE) Isolation method for new Visual Editor overlay |
| **Traffic Allocation** | Percentage of eligible visitors (0-10000 basis points) |
| **Variation** | Alternative version of page/feature shown to visitor subset |
| **Visual Editor** | WYSIWYG tool for creating experiment variations without code |

## Platform Comparison Quick Reference

| Concept | Web Experimentation | Feature Experimentation | Performance Edge |
|---|---|---|---|
| Test unit | Experiment | Flag + Rule | Experiment |
| Variations | Page variations | Flag variations (variable values) | Page variations |
| Targeting | Pages + Audiences | Environments + Rules + Audiences | Pages + Audiences (limited) |
| Implementation | JavaScript snippet | SDK (client/server) | CDN edge + microsnippet |
| Editor | Visual Editor (WYSIWYG) | Code-based | Visual Editor (limited) |
| Personalization | Campaigns + Experiences | Targeted Delivery rules | Not supported |
| Rule types | N/A | Delivery, A/B, MAB, CMAB | N/A |
| Environments | Single | Multiple (dev, staging, prod) | Single |
| MAB/MVT | Both supported | MAB + CMAB supported | Neither supported |
| Scheduling | Not available | Available (2min-90day window) | Not available |
| Change Approvals | Not available | Available per environment | Not available |
