# Product Glossary - Detailed Reference

**This file contains the full glossary of terms, entity relationship diagrams, and service architecture tables. For core terminology and platform comparison, see SKILL.md.**

## Full Glossary

### A

**A/B Test** - An experiment that splits traffic between two or more variations to determine which performs better against defined metrics. In Web Exp, created via UI/API. In FX, created as a rule type on a flag.

**Acceptable Values** - (FX) Optional constraints on flag variable values. Types: `custom_list` (specific allowed values) or `min_max_values` (numeric range). Controls what values variations can assign.

**Activation** - The process by which Optimizely's snippet begins running an experiment on a page. Can be immediate, manual, or conditional based on URL/page targeting.

**Approval Workflow** - (FX) A process requiring changes to be reviewed and accepted before going live, configured per environment. Statuses: pending, accepted, rejected, withdrawn.

**Attribute** - A key-value property of a visitor used for audience targeting (e.g., `browser_type`, `country`, `is_logged_in`). In FX, attributes are passed via `createUserContext()`.

**Audience** - A group of visitors defined by conditions (attributes, behaviors, location, device, etc.) used to target experiments or flag rules to specific user segments.

### B

**Bucketing** - The process of assigning a visitor to a specific variation within an experiment. Uses deterministic hashing (MurmurHash3) so the same visitor always sees the same variation.

**Brainstorm** - An Opal Chat feature that uses AI to suggest flag variables or flag variations based on the current flag context.

### C

**Campaign** - (Web Exp) A personalization campaign that delivers targeted experiences to specific audiences. Contains multiple experiences, each with its own audience and changes.

**Change History** - A backend microservice that tracks and exposes changes made to Optimizely entities (experiments, flags, audiences, etc.). Enables auditing what changed, who changed it, and when. Service URLs: inte/prep/prod at `change-history.optimizely.com`.

**Change Status** - (Visual Editor) Lifecycle states of a visual change: INITIAL -> NEW -> DIRTY -> LIVE / MODIFIED / DRAFT / DELETED.

**Change Type** - (Visual Editor) Types of modifications: ATTRIBUTE, CUSTOM_CSS, CUSTOM_CODE, INSERT_HTML, INSERT_IMAGE, WIDGET, REDIRECT.

**CMAB (Contextual Multi-Armed Bandit)** - An advanced optimization that considers user context/attributes to personalize variation assignment, not just overall performance.

**Context Service** - (Opal) A backend service that maps the current page URL to relevant API data, providing Opal Chat with context about what the user is looking at.

**Changelog Elasticsearch** - A real-time indexing pipeline that feeds entity changes (experiments, flags, audiences, campaigns) from the monolith into Elasticsearch for fast search in the UI. Architecture: GCP Pub/Sub -> Cloud Function -> AWS SNS -> SQS -> Lambda -> Elasticsearch 6.8. Flags/rules include inline snapshots; other entities fetched from FrontDoor API.

**Conversion** - When a visitor triggers a tracked event that represents a business goal (purchase, signup, click, etc.).

**Custom Fields** - (FX) User-defined metadata fields (text, number, boolean, link, label) that can be attached to flags for organization and filtering. Feature-flagged via `fx_custom_fields`.

### D

**Datafile** - (FX) A JSON configuration file (versions V2/V3/V4) containing all flag, variation, rule, event, audience, holdout, and group definitions for a project environment. SDKs download and cache the datafile for local decisions. V4 adds featureFlags, rollouts, holdouts, typedAudiences, region, botFiltering.

**Datafile Access Token** - A secure authentication token for accessing private/authenticated datafiles via SDKs. Format: `base64(1:{projectId}:{accessTokenId}:{randomUuid})`. Plaintext shown only once at creation. Validated by Cloudflare Authorization Worker via SHA256 hash comparison against whitelist in KV.

**Datafile Build Service (DBS)** - Service that builds FX datafiles by merging data from Flags service (experiments, featureFlags, rollouts, groups, holdouts) and Monolith (audiences, attributes, events, integrations). Triggered by Pub/Sub messages. Uploads to S3 (public/PCI/private), Cloudflare KV, and purges CDN cache. Supports force_build, dry_run, skip_build, and deferred publishing.

**Dead Letter Queue (DLQ)** - A message queue that receives messages that failed processing after maximum retry attempts. DBS uses `dead-letter-datafile-ingress-point` (max 10 attempts). Changelog Elasticsearch uses SQS DLQ.

**Decide** - (FX SDK) The primary method (`optimizelyClient.decide()`) that evaluates a flag for a user and returns the flag decision (enabled/disabled + variation).

**Dummy Audience** - A backwards-compatibility audience (ID: `$opt_dummy_audience`) injected by DBS when a datafile has no audiences, ensuring SDK compatibility.

### E

**Edge Decider** - The server-side component of Performance Edge that receives requests, evaluates experiment configurations, makes bucketing decisions, and returns a microsnippet.

**Edge Delivery SDK** - npm package (`@optimizely/edge-delivery`) that enables execution of Optimizely Web experiments on Cloudflare Workers at the edge. Main method: `applyExperiments()`.

**Entity Permission** - Granular permission on a specific entity (flag, environment, audience). Levels: admin, publish, toggle, edit, view, none.

**Environment** - (FX) Isolated configuration contexts (e.g., Production, Staging, Development) where flags can have different rules and settings.

**Event** - A user action tracked for measurement (e.g., click, pageview, purchase). Events are used as metrics in experiments.

**Exclusion Group** - (Mutually Exclusive Experiments) A group of experiments where a visitor can only be in one experiment at a time, preventing interaction effects.

**Experience** - (Web Exp) A specific combination of changes and audience targeting within a personalization campaign.

**Experiment** - A test that compares variations to measure impact on metrics. Types include A/B test, multivariate test, and multi-armed bandit.

### F

**Flag** - (FX) A feature flag that can be toggled on/off and configured with variables and variations. The primary unit of feature management in FX.

**Flag Delivery** - (FX) A rule type that delivers a specific flag variation to a targeted audience without A/B testing (also called targeted rollout).

**Flag Variable** - (FX) A configurable parameter within a flag (string, boolean, integer, double, JSON) whose value can differ per variation.

**Flag Variation** - (FX) A named set of variable values for a flag (e.g., "control" has `color=blue`, "treatment" has `color=red`).

### G

**Goal** - See "Metric". A conversion event used to measure experiment success.

### H

**Holdback** - A percentage of traffic excluded from all experiments in a group, serving as a global control to measure the cumulative impact.

**Holdout** - (FX) A control group for measuring cumulative impact of multiple experiments. Properties: scope, traffic_allocation (0-10000), status (draft/active/inactive/concluded), metrics.

### I

**Idea Builder** - An AI-powered experimentation idea generator service that helps users brainstorm and validate test ideas. Uses OPAL agent for AI generation. Backend: FastAPI + Spanner. Frontend: React + Module Federation.

**Impression** - (FX) A decision event recorded when a flag is evaluated for a user. Used for experiment analysis.

**Interaction Island** - (Opal) An interactive UI component returned by Opal tools that allows users to take actions (create entity, apply suggestion) directly in the chat. Contains fields and action buttons.

### J

**JavaScript API** - (Web Exp) Client-side API (`window["optimizely"]`) for controlling experiment behavior, accessing state, and tracking events.

### K

**Key** - A unique string identifier for flags, variations, events, and audiences used in SDK code (e.g., `flag_key`, `event_key`). Max 64 chars for flags/variations/rules.

### L

**Layer** - Internal name for a campaign/experiment container. Types: single_experiment, multivariate, ordered, equal_priority, rollout.

**Lifecycle** - The stages an experiment goes through: Draft -> Running -> Paused -> Archived. Or for flags: Created -> Rules configured -> Enabled. For rules: draft -> running -> paused -> concluded.

### M

**MAB (Multi-Armed Bandit)** - An optimization algorithm that automatically shifts traffic to better-performing variations. Configuration: exploration_rate (500-5000), exploitation_rate (500-5000), distribution_goal.

**Metric** - A measurement tied to an event that defines success criteria for an experiment (e.g., conversion rate, revenue per visitor).

**Microsnippet** - (Performance Edge) Lightweight JavaScript returned by the Edge Decider, tailor-made for each visitor/page. Applies changes and injects tracking snippet.

**Multivariate Test (MVT)** - (Web Exp) An experiment testing multiple combinations of changes simultaneously to find the best combination. Not supported in Performance Edge.

### O

**Opal** - Optimizely's AI assistant (copilot) embedded in the platform UI. Provides chat, brainstorming, result summarization, experiment review, and visual editor AI capabilities.

**Opal Tools** - Backend service (FastAPI, port 8111) that provides AI-powered tools to Opal Chat, including OpenSearch queries, entity management, visual editor bridge, sample size calculator, and program reporting.

**OpenSearch** - The query engine used by Opal to search and filter experimentation entities. Requires calling `exp_get_schemas` before `exp_execute_query`.

### P

**Page** - (Web Exp) A URL or set of URL patterns where an experiment can run. Pages define where the Optimizely snippet activates experiments.

**Permission Service** - Unified authorization microservice providing granular entity-level permissions, team management, and role-based access. Uses Spanner database, Redis cache, and Pub/Sub events.

**Personalization** - (Web Exp) Delivering different experiences to different audience segments. Implemented via campaigns with multiple experiences.

**Project** - The top-level container in Optimizely. Types: Web (client-side), Custom/Full Stack (server-side FX).

### R

**Report** - (FX) Entity tracking experiment results over time. Can be archived, unarchived, and reset. Contains metrics, confidence levels, outcomes.

**Rollout** - See "Flag Delivery". Gradually releasing a feature to increasing percentages of users.

**Rule** - (FX) A configuration on a flag that defines targeting, traffic allocation, and variation assignment. Types: targeted_delivery, a/b, multi_armed_bandit, contextual_multi_armed_bandit.

**Ruleset** - (FX) Container for rules per flag+environment. Has enabled state, default_variation, and rule_priorities array for ordering.

### S

**Sample Size** - The number of visitors needed for an experiment to reach statistical significance. Opal has a `exp_calculate_sample_size` tool for this.

**Schedule** - (FX) A planned future change to a flag or rule. Constraints: min 2min5s delay, max 90 days. Status: pending -> in_queue -> completed/failed/partially_failed.

**Selectorator** - (Visual Editor) The algorithm that generates CSS selectors using a powerset approach. Tries combinations of tag, ID, classes, attributes to find the shortest unique selector.

**Shadow DOM** - (Visual Editor) The new Visual Editor runs as an isolated Shadow DOM overlay on customer websites, preventing CSS/JS interference between editor and host page.

**Snippet** - (Web Exp) The JavaScript file (`optimizely.js`) added to web pages that runs experiments client-side.

**Statistical Significance** - The confidence level (typically 90-95%) that an observed difference between variations is not due to chance. Only A/B tests produce this (not MAB/CMAB).

### T

**Targeted Delivery** - (FX) A rule that serves a specific variation to users matching an audience, without A/B testing. Used for feature rollouts. Does not generate decision events.

**Team** - A group of users that can be assigned entity-level permissions collectively. Managed at the account level. Names must be unique per account.

**Traffic Allocation** - The percentage of eligible visitors included in an experiment or rule. Uses basis points (0-10000 scale where 10000 = 100%).

### U

**User Context** - (FX SDK) An object created with `createUserContext(userId, attributes)` that represents a visitor for flag decisions.

### V

**Variation** - An alternative version of a page/feature shown to a subset of visitors. Every experiment has at least an "Original/Control" and one variation.

**Vertex AI Search** - Google Cloud service used by Opal to power RAG-based documentation search for FX SDK docs.

**Visual Editor** - (Web Exp) A WYSIWYG tool for creating experiment variations without code. New version uses Shadow DOM overlay with React 18, Zustand state management, and Module Federation for Opal integration.

### W

**Web Experimentation** - Optimizely's client-side A/B testing platform that runs experiments via a JavaScript snippet on websites.

**Webhook** - A notification mechanism that sends HTTP requests when specific events occur (e.g., datafile updated).

## Entity Relationships (Full Diagram)

```
Account
  +-- Projects
  |     +-- Web Project
  |     |     +-- Experiments (A/B, MVT, MAB)
  |     |     |     +-- Variations
  |     |     |     +-- Metrics (Events)
  |     |     |     +-- Audiences
  |     |     |     +-- Pages
  |     |     +-- Campaigns (Personalization)
  |     |     |     +-- Experiences
  |     |     +-- Change History
  |     |
  |     +-- FX Project
  |     |     +-- Flags
  |     |     |     +-- Variables
  |     |     |     +-- Variations
  |     |     |     +-- Rulesets (per Environment)
  |     |     |           +-- Rules (Delivery, A/B, MAB, CMAB)
  |     |     +-- Environments
  |     |     +-- Holdouts
  |     |     +-- Groups (Mutual Exclusion)
  |     |     +-- Custom Fields
  |     |     +-- Schedules & Approvals
  |     |     +-- Reports
  |     |     +-- Change History
  |     |
  |     +-- Edge Project
  |           +-- Experiments (A/B only)
  |           +-- Change History
  |
  +-- Teams
  +-- Permissions (entity-level)
  +-- Opal (AI Assistant)
        +-- Chat Threads
        +-- Idea Builder Ideas
```

## Service Architecture (Full Table)

| Service | Purpose | Tech Stack | Port |
|---|---|---|---|
| Monolith (optimizely) | Main frontend app | Python/Flask + React/Vue | -- |
| Flags | FX backend | Python/Flask + PostgreSQL | 8000 |
| Flags-Scheduling | FX scheduling & approvals | Python/FastAPI | -- |
| Permission Service | Authorization & teams | Python/FastAPI + Spanner | 8005 |
| Change History | Audit trail | Python/Flask + PostgreSQL | -- |
| Datafile Build Service | Datafile building & CDN publishing | Python + S3/Cloudflare | -- |
| Datafile Access Tokens | SDK token auth for private datafiles | Node.js + Cloudflare KV | 3000 |
| Changelog Elasticsearch | Search indexing pipeline | Python/Lambda + Elasticsearch 6.8 | -- |
| Opal Tools | AI tools backend | Python/FastAPI | 8111 |
| Idea Builder | AI idea generation | Python/FastAPI + Spanner | 8030 |
| Visual Editor | WYSIWYG editor | React/TypeScript | 9888 |
| Edge Delivery SDK | Edge experiments | TypeScript/Cloudflare Workers | -- |

## Reference Links

- **Documentation sources**: `web-docs`, `fx-docs`, `edge-docs` repositories at `docs/` directories, plus cross-product terminology from 12+ development repositories
