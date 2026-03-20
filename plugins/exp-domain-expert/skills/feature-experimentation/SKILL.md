---
description: Product domain knowledge for Optimizely Feature Experimentation (Feature Flags). Use when answering questions about feature flags, flag variations, flag variables, rules, environments, rollouts, A/B tests, MAB, CMAB, audiences, events, bucketing, SDKs, FX APIs, scheduling, approvals, holdouts, groups, custom fields, change history, permissions, datafile build service, datafile access tokens, or search indexing. Helps QA engineers write tests with accurate product understanding.
---

## Dependencies

- **MCP Servers (optional):** `optimizely-prod` - Query real flag/experiment data from Optimizely platform
  - `exp_get_schemas` - Get entity schemas (flag, rule, environment, event, audience, attribute)
  - `exp_execute_query` - Query real flags, rules, environments, events by project
  - `exp_search_fx_sdk_docs` - Search FX SDK documentation (installation, initialization, decide methods, event tracking)

### When to Use MCP vs Static Knowledge

| Question Type | Source | Example |
|---|---|---|
| "How does X work?" | Static knowledge (this file) | "How does flag bucketing work?" |
| "What flags exist in project X?" | MCP `exp_execute_query` | "List all flags with A/B test rules in project 12345" |
| "How do I use the SDK?" | MCP `exp_search_fx_sdk_docs` | "How to initialize the JavaScript SDK?" |

**Rules:**
- Always call `exp_get_schemas` before `exp_execute_query` to get correct field names and query syntax.
- FX experiments are rules on flags -- query the `flag` entity with `environments.rules.rule_type` filter, NOT the `experiment` entity.
- Always add `project_id` filter to scope queries.

### Source Repositories
- **Documentation repo:** `fx-docs` repository at `docs/` directory (user-facing product documentation)
- **Dev repos:**
  - `flags` — FX backend service (Python/Flask + PostgreSQL, flag/rule/variation CRUD, rulesets, environments)
  - `flags-scheduling` — Scheduling & approvals service (Python/FastAPI, scheduled flag/rule changes, approval workflows)
  - `change-history` — Change tracking microservice (audit trail for flags, rules, environments)
  - `permission-service` — Authorization service (entity-level permissions, team-based access, restricted environments)
  - `datafile-build-service` — Datafile building & CDN publishing (Python + S3/Cloudflare, V2/V3/V4 datafile generation)
  - `datafile-access-tokens` — SDK token auth for private datafiles (Node.js + Cloudflare KV)
  - `appx-changelog-elasticsearch` — Search indexing pipeline (GCP Pub/Sub → Cloud Function → AWS SNS → SQS → Lambda → Elasticsearch 6.8)

## Role

You are an Optimizely Feature Experimentation domain expert. You have deep knowledge of FX including its architecture, concepts, APIs, SDKs, scheduling, approvals, holdouts, mutual exclusion groups, change history, permissions, the Datafile Build Service pipeline, datafile access tokens, and the changelog search indexing system.

**Full reference:** See reference.md for detailed API endpoints, datafile V4 schema, DBS internals, DAT token format, Elasticsearch indexing pipeline, permission matrices, and scheduling/approval API details.

## Product Overview

Optimizely Feature Experimentation (FX) is a server-side experimentation and feature management platform enabling:
- **Feature Flags**: Toggle functionality without deploying code
- **Gradual Rollouts**: Gradually expose features to increasing percentages
- **Server-side A/B Testing**: Experiments using SDKs in application code
- **Multi-Armed Bandit (MAB)**: Automatically optimize traffic toward winners
- **Contextual Multi-Armed Bandit (CMAB)**: AI-powered personalization per user context
- **Remote Configuration**: Change behavior via flag variables without redeploying
- **Scheduling**: Schedule flag/rule changes at specific dates/times
- **Change Approvals**: Require approval before changes go live
- **Holdouts**: Control groups for cumulative impact measurement
- **Mutual Exclusion Groups**: Ensure users see only one experiment at a time

## Core Concepts

### Flags
Central entity in FX with: key (unique, max 64 chars, immutable), name (max 255), variable_definitions, per-environment configuration, archived state, custom_fields (feature-flagged via `FX_FLAGS_STATUSES`), owner_user_id, team_ids. Flag creator auto-assigned **Admin** role.

### Flag Variables
Remote configuration without hard-coding. Types: `boolean`, `string`, `integer`, `double`, `json`. Each has key (immutable), type (immutable), default_value. Optional acceptable value constraints: `custom_list` or `min_max_values`.

### Flag Variations
Reusable groups of variable values. Every flag has "on" (enabled) and "off" (disabled, key reserved). Variations in use by any rule cannot be deleted.

### Rules
Per-environment ordered list (first match wins). Types:
- `targeted_delivery` -- Rollout, no experiment results
- `a/b` -- A/B test with statistical significance
- `multi_armed_bandit` -- MAB, automatic traffic reallocation
- `contextual_multi_armed_bandit` -- CMAB, personalized per user context

Key properties: percentage_included (0-10000, where 10000=100%), audience_conditions, metrics, enabled, status (draft/running/paused/concluded).

**Rule ordering constraint**: Experiment rules must come before targeted delivery rules.

### Rule Status Transitions
```
Draft -> Running -> (Paused | Concluded)
Draft -> Paused -> Running
```

### Environments
Isolated contexts for flags/rules. Each has own datafile (SDK key) and ruleset per flag. Flags enabled/disabled independently per environment. Restricted environments require `FLAGS_TOGGLE` permission.

### Events and Audiences
Events: key-based tracking (`custom`, `click`, `pageview`). Cross-project sharing supported.
Audiences: Attribute-based targeting with `and`/`or`/`not` operators. Attributes must be defined before use.

## Flag Lifecycle

1. Create Flag -> 2. Create Variables -> 3. Create Variations -> 4. Create Rules -> 5. Configure Audiences -> 6. Add Metrics -> 7. Enable Flag (Ruleset) -> 8. Enable Rules -> 9. Analyze Results -> 10. Conclude

**Two-level enablement**: Both the flag (ruleset) AND individual rules must be enabled to serve traffic.

## Scheduling

Schedule flag/rule changes at specific dates/times. Constraints: min 2min5s delay, max 90 days. Actions: flag status on/off, rule status on/off, rule percentage change, rule audience change. Status lifecycle: PENDING -> IN_QUEUE -> COMPLETED | FAILED | PARTIALLY_FAILED.

## Change Approvals

Approval workflow for restricted environments. Status: PENDING -> ACCEPTED | REJECTED (reason required, max 350 chars) | WITHDRAWN. Configured per environment with approver lists.

## Holdouts and Exclusion Groups

**Holdouts**: Control groups measuring cumulative impact. Properties: traffic_allocation (0-10000), status (draft/active/inactive/concluded).
**Exclusion Groups**: Ensure users see only one experiment across multiple flags. No SDK changes required. All experiments should start simultaneously.

## Bucketing and Traffic Allocation

1. SDK uses **MurmurHash** on user ID + experiment ID (0-10000 range)
2. **Deterministic** and **sticky unless reconfigured**
3. Evaluation order: Forced Variation -> User Allowlisting -> User Profile Service -> Audience Targeting -> Exclusion Groups -> Traffic Allocation
4. Increasing live traffic does NOT rebucket; decreasing then increasing WILL rebucket

## SDK Overview

**Available SDKs**: Android, Swift, Flutter, React Native, JavaScript (Browser/Node), React, Java, Python, Go, Ruby, PHP, C#, Agent

**Key SDK Methods:**
```javascript
const user = optimizely.createUserContext('user123', { logged_in: true });
const decision = user.decide('product_sort');
const enabled = decision.enabled;
const sortMethod = decision.variables['sort_method'];
user.trackEvent('purchased');
```

**Datafile**: JSON config containing all flag/variation/rule/audience definitions. Environment-specific. Every flags service write triggers datafile rebuild via DBS.

## Key Business Rules

1. Flag must have ruleset **enabled** AND individual rules **enabled** to serve traffic
2. Rules evaluated **in order** -- first match wins
3. Experiment rules must come **before** targeted delivery rules
4. A/B tests produce **statistical significance**; MAB and CMAB do **not**
5. CMAB optimizes only for the **primary metric**
6. Results page only shows events tracked **after** a `Decide` call
7. Decreasing then increasing traffic rebuckets users
8. Flag creator auto-assigned **Admin** role
9. Creating a flag requires environment access
10. Production environments typically have **restricted permissions**
11. Same `Decide` works for all rule types; bucketing is deterministic

## Common Test Scenarios

### Flag Management
- Create flag with key/name/description/custom_fields
- Add variables of each type with acceptable value constraints
- Create custom variations, archive/unarchive/delete/duplicate flags

### Rule Configuration
- Create each rule type, verify ordering in ruleset
- Add audience conditions and metrics, test variation allocation
- Test user allowlisting (forced variations)

### Scheduling
- Schedule flag on/off and rule percentage/audience changes
- Test time constraints (min 2min5s, max 90 days) and timezone handling

### Change Approvals
- Create/accept/reject/withdraw approvals
- Test environment-level and entity-level approval settings

### Holdouts & Groups
- Create holdouts and mutual exclusion groups
- Verify users see only one experiment in a group

### Traffic and Bucketing
- Verify allocation percentages and deterministic bucketing
- Test exclusion groups

### Events and Results
- Create custom events, add as metrics, verify Results page data

### API Testing
- CRUD for all entities, JSON Patch for rulesets, error handling
