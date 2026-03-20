# Opal Chat - Detailed Reference

**This file contains exhaustive tool definitions, API details, island response formats, and configuration options. For core product knowledge, see SKILL.md.**

## Available Opal Tools (Complete Reference)

### Test Planning & Analysis

**exp_calculate_sample_size**
- Calculate sample size and duration for A/B tests
- Inputs: baseline_rate (0-1, default 0.1), mde (default 0.05), significance (default 95%), variants (default 2), visitors (default 2500), frequency (daily/weekly/monthly, default "weekly")
- Outputs: sample_size_per_variant, total_sample_size, days/weeks/months_to_run
- Pure computation, no API calls

**exp_summarize_test_result**
- Fetch and enrich experiment results with metadata
- Inputs: experiment_id OR experiment_name (as STRING), project_id OR project_name
- **CRITICAL:** ID format must be STRING ("6680344594743296", not number)
- Post-processing: extracts audience_ids from audience_conditions, calls exp_execute_query for audience details

### OpenSearch Query Engine

**exp_get_schemas** (MANDATORY prerequisite for exp_execute_query)
- Get entity schemas before querying
- Inputs: entities (list of entity types)
- Supported entities: experiment, page, audience, event, flag, campaign, environment, experience, rule, extension, attribute, experimentsection, project

**exp_execute_query**
- Execute template-based queries against OpenSearch
- Inputs: template (JSON with "steps" array), project_id (optional, as STRING)
- Query structure:
```json
{
  "steps": [{
    "entity": "experiment",
    "filters": [{"field": "id", "operator": "equals", "value": 123}],
    "return_fields": ["id", "name", "status"],
    "enrich": {"page_ids": {"entity": "page", "fields": [...]}},
    "limit": 100
  }]
}
```
- Filter operators: equals, contains, in, greater_than, less_than
- Date filters must use absolute ISO-8601 format
- Output: Display names/keys first, hide raw IDs, use markdown tables for lists >= 2 items

### Entity Management

**exp_get_entity_templates** (MANDATORY prerequisite for exp_manage_entity_lifecycle)
- Fetch CREATE/UPDATE schemas before entity operations
- Inputs: project_id, operation ("create" or "update"), entity_type (optional), template_id (optional)
- Supported types: attribute, audience, campaign, event, experiment, flag, ruleset, page, variable_definition, flag_variation

**exp_manage_entity_lifecycle**
- Create or update entities
- Inputs: operation (create/update), entity_type, project_id, entity_id (for updates), template_data
- Returns IslandResponse with confirmation form
- DELETE operations currently disabled
- Requires user confirmation via island form

### Flag Management

**exp_suggest_flag_variables**
- Generate flag variables from hypothesis
- Inputs: project_id (int), flag_key (str), variables (list with key, type, default_value, description)
- Variable types: boolean, string, integer, double
- Returns IslandResponse with islands per variable
- Action endpoint: `/interactions/flag-variable`

**exp_suggest_flag_variations**
- Generate flag variations with variable assignments
- Inputs: project_id (int), flag_key (str), variations (list with name, key, description, variables dict)
- Returns IslandResponse with islands per variation
- Action endpoint: `/interactions/flag-variation`

### Visual Editor Tools

**exp_ve_element_read** - Read element info (tag, attributes, styles, children)
**exp_ve_element_glob** - Find elements matching glob patterns
**exp_ve_element_grep** - Search elements by text patterns
**exp_ve_element_tree** - Get DOM tree structure
**exp_ve_get_selector** - Generate unique CSS selector
**exp_ve_get_change_schema** - Get validation schema for changes
**exp_ve_validate_change** - Validate proposed change before apply
**exp_ve_apply_change** - Apply style/text changes
**exp_ve_revert_change** - Revert previously applied changes
**exp_ve_list_pending_changes** - List all pending changes

### Design & Suggestions

**exp_suggest_design_improvements**
- Generate design improvement suggestions using LLM
- Categories: Call to Action, Visual Hierarchy, UX, Color/Contrast, Typography, Layout, Accessibility, Loading State, Mobile Responsiveness
- Returns IslandResponse with islands per design variation

### SDK Documentation

**exp_search_fx_sdk_docs**
- Search Feature Experimentation SDK documentation via Vertex AI Search RAG
- Inputs: query (1-500 chars)
- Returns: success, answer, sources (URLs)

### Program Reporting

**exp_get_top_experiments** - Top-performing experiments in date range
**exp_get_underperforming_experiments** - Underperforming experiments
**exp_get_win_rate** - Experiment win rate metrics

Inputs for all: date_range (start/end ISO8601), project_ids (optional), page_size (1-100)

## Interaction Island Response Format

Tools return IslandResponse for user confirmation:
```json
{
  "type": "island",
  "config": {
    "islands": [{
      "fields": [
        {"name": "field_id", "label": "Label", "type": "string", "value": "...", "editable": false}
      ],
      "actions": [
        {"name": "action_id", "label": "Button", "type": "button", "endpoint": "/interactions/...", "operation": "create"}
      ]
    }]
  }
}
```

## Context Service Details

- Maps the current page URL to relevant API calls using regex patterns
- Supports dependency chains (API 1 response used in API 2)
- API client types: EXP (with OptiID), EXP_INTERNAL (special token), ICE, FLAG
- URL patterns include: `/v2/projects/{project_id}/experiments/{experiment_id}`, `/v2/projects/{project_id}/flags/{flag_id}`, etc.

## Idea Builder API (Full Reference)

### Ideas CRUD
```
POST   /api/ideas              -- Create idea (201)
GET    /api/ideas              -- List ideas (paginated, searchable)
GET    /api/ideas/{idea_id}    -- Get idea (200)
PATCH  /api/ideas/{idea_id}    -- Update idea (200)
DELETE /api/ideas/{idea_id}    -- Delete idea (204)
```

### Test Idea Generation
```
POST   /api/generate-test-ideas   -- Generate ideas via OPAL agent (multipart form)
```

### Experimentation Context
```
GET    /api/saved-pages         -- List saved pages (query: project_id, search, limit, offset)
GET    /api/experiments          -- List experiments (query: project_id, search, status, type, page_id)
```

### Idea Data Model

```
id: UUID (36 chars)
project_id: int64 (required)
title: string (255 chars, required)
target_url: string (2048 chars, optional)
page_id: int64 (optional)
description: string (optional)
problem: string (optional)
reasonability: string (optional)
hypothesis_title: string (255 chars, optional)
hypothesis_description: string (optional)
sources: list[string] (JSON serialized)
created_at, updated_at: timestamps
```

### Generate Test Ideas Request (Multipart Form)

```json
{
  "data": {
    "target_by": "URL | Saved Page | Screenshot",
    "url": "string (if target_by=URL)",
    "saved_page_id": "string (if target_by=Saved Page)",
    "goal": "string (required)",
    "additional_context_text": "string",
    "previous_test_ids": ["string"]
  },
  "screenshot": "File (optional, max 5MB: PNG, JPG, GIF)",
  "additional_context_file": "File (optional)"
}
```

### Idea Builder Environment URLs

| Environment | Backend | Frontend |
|---|---|---|
| Local | `http://localhost:8030` | `http://localhost:5001` |
| Integration | `https://inte.idea-builder.optimizely.com` | Cloudflare Pages |
| Production | `https://idea-builder.optimizely.com` | Cloudflare Pages |

## Detailed Test Scenarios

### OpenSearch Query Test Scenarios
- Query experiments by status, name, project
- Query flags with enrichment (related entities)
- Verify date filters use ISO-8601 format
- Verify ID precision (strings, not numbers)

### Program Reporting Test Scenarios
- Get top/underperforming experiments by date range
- Get win rate metrics
- Filter by project_ids
- Verify pagination (page_size 1-100)

### Idea Builder Test Scenarios
- Create, list, get, update, delete ideas (CRUD)
- Generate test ideas with URL, Saved Page, Screenshot targets
- Verify file upload size limits (max 5MB)
- Verify search on ideas (case-insensitive, title + target_url)
- Verify pagination (limit 1-1000, offset >= 0)
- Test authentication (missing/expired OptiID token -> 401)
- Test authorization (wrong project access -> 403)

## Reference Links

- **Documentation source**: `opal-docs` repository at `docs/` directory
- **Backend source:** `optimizely/opal-tools` (GitHub)
- **Idea Builder source:** `optimizely/idea-builder` (GitHub)
- **E2E tests:** `optimizely/opal-chat-e2e-test` (GitHub)
- **Test framework:** Playwright with TypeScript
