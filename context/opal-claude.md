# Opal Tools - Claude Code Context

> **Optimizely Opal Tools** - A Python FastAPI backend service that provides AI-powered **Remote Tools** and **Experimentation Context Service** for the Optimizely Experimentation platform. This service powers the Opal Chat AI assistant with tools for querying experiments, managing entities, browsing SDK docs, generating design suggestions, and controlling the Visual Editor via WebSocket bridge.

**Last Updated**: 2026-03-17
**Repository**: https://github.com/optimizely/opal-tools

---

## Table of Contents

1. [Architecture & Directory Structure](#1-architecture--directory-structure)
2. [Core Logic & Business Rules](#2-core-logic--business-rules)
3. [QA & Testing Standards](#3-qa--testing-standards)
4. [JIRA Analysis Context](#4-jira-analysis-context)
5. [Functional Tree (UI to Code Map)](#5-functional-tree-ui-to-code-map)

---

## 1. Architecture & Directory Structure

### Architecture & Data Flow

```
Opal Chat (Frontend)
  │
  ├── HTTP Tool Calls ──→ Opal Tools (FastAPI, port 8111)
  │                         ├─ /tools/* (auto-registered via @tool decorator + opal-tools-sdk)
  │                         ├─ /context (URL → API data enrichment)
  │                         ├─ /interactions/* (Island execution endpoints)
  │                         ├─ /opensearch-query/* (entity schema/query)
  │                         ├─ /fx-sdk-docs/* (SDK documentation search)
  │                         ├─ /agents/* (agent directory)
  │                         └─ /ws/{thread_id} (WebSocket bridge for VE)
  │                                │
  ├─────────────────────────────────┼───────────────────────────────────┐
  │                                 │                                   │
  ▼                                 ▼                                   ▼
Experimentation API             OpenSearch Query Engine          Visual Editor (Browser)
(REST: /v2/experiments,         (TypeScript Backend,             (WebSocket connection
 /flags, /campaigns,             entity schemas & queries)        for DOM manipulation)
 /audiences, /events)
  │                                 │
  ▼                                 ▼
Flags API                       ICE API (Internal Content Engine)
(/projects/{id}/flags/*)        (/experimentation-project/*)
```

**Flow**:
- **Tool Calls**: Opal Chat → `@tool()` decorated functions → service layer → external APIs → response (JSON or IslandResponse)
- **Context**: Opal URL → regex match in `constants.py` → parallel API calls → formatters → enriched context for LLM
- **VE Bridge**: Opal Chat → tool call → WebSocket manager → browser VE → DOM result back
- **Interaction Islands**: Tool returns `IslandResponse` → user confirms in UI → `/interactions/*` endpoint executes action

### Directory Structure

```
opal-tools/
├── main.py                    # FastAPI app creation, router registration, lifespan, WebSocket mount
├── Makefile                   # All dev commands (run, test, format, lint, docker)
├── pyproject.toml             # Poetry deps, pytest/mypy config
├── src/
│   ├── env_config.py          # Environment validation (fails fast on missing vars)
│   ├── constants.py           # VERSION constant
│   ├── context_vars.py        # Request-scoped context variables (thread_id, auth tokens)
│   ├── authentication/
│   │   ├── enums.py           # AuthenticationMechanism enum
│   │   ├── ingress/           # Inbound auth: OptiID (Okta JWT), OpalApiGW, WebSocket auth
│   │   └── egress/            # Outbound auth: EgressAuthManager, EXP/EXP_COOKIE/EXP_INTERNAL_TOKEN
│   ├── authorization/
│   │   └── ingress/           # Organization-level authorization, @inject_admin_account_ids decorator
│   ├── common/
│   │   ├── agent/builder.py   # LLM agent wrapper (llm-framework package)
│   │   ├── client/            # HTTP clients: BaseClient, ExperimentationClient, IceClient, GcsClient, HmacHttpClient
│   │   ├── constants.py       # Shared constants
│   │   ├── decorators.py      # patch_tool_decorator, with_token_tracking_interaction_island
│   │   ├── enums.py           # Common enums
│   │   ├── json_parser.py     # JSON utilities
│   │   └── middlewares/       # ContextMiddleware (sets context vars per request)
│   ├── logger/                # structlog LOGGER, ASGI access log middleware
│   ├── services/
│   │   ├── context/           # URL-to-context enrichment service (constants, formatters, processors)
│   │   ├── interaction_island/# Island execution endpoints (flag vars, flag variations, entity lifecycle)
│   │   ├── experimentation/   # ExperimentationService (result API calls)
│   │   ├── flags/             # FlagsService (flag CRUD via Flags API)
│   │   ├── exp_manage_entity_lifecycle/ # Entity create/update via TypeScript backend
│   │   ├── opensearch_query/  # OpenSearch query engine client & routes
│   │   ├── fx_sdk_docs_search/# Vertex AI Search for FX SDK documentation
│   │   ├── program_reporting/ # Program Reporting API (win rate, top/underperforming experiments)
│   │   ├── agent_directory/   # Agent registration and discovery
│   │   ├── refresh_token/     # Token refresh service
│   │   ├── llm_usage/         # LLM usage tracking
│   │   └── websocket_bridge/  # WebSocket manager, HTTP client, models for VE bridge
│   ├── tools/                 # @tool() decorated functions (auto-registered in __init__.py)
│   │   ├── __init__.py        # init_tools() — MUST import all tool modules here
│   │   ├── opensearch_query.py         # exp_get_schemas, exp_execute_query
│   │   ├── result_summary.py           # exp_summarize_test_result
│   │   ├── exp_manage_entity_lifecycle.py # exp_manage_entity_lifecycle (create/update entities)
│   │   ├── exp_get_entity_templates.py  # exp_get_entity_templates (schema fetching)
│   │   ├── flag_variable_brainstorm.py  # exp_suggest_flag_variables
│   │   ├── flag_variation_brainstorm.py # exp_suggest_flag_variations
│   │   ├── sample_size_calculator.py    # exp_calculate_sample_size
│   │   ├── fx_sdk_docs_search.py        # exp_search_fx_sdk_docs
│   │   ├── pgm_reporting/              # Program reporting tools
│   │   │   ├── top_experiments.py       # exp_program_reporting_top_experiments
│   │   │   ├── underperforming_experiments.py # exp_program_reporting_underperforming_experiments
│   │   │   ├── win_rate.py              # exp_program_reporting_win_rate
│   │   │   └── utils.py                 # Date parsing, list normalization helpers
│   │   ├── visual_editor/              # VE-specific tools
│   │   │   ├── design_improvement_suggestions.py # exp_suggest_visual_editor_component_improvements
│   │   │   ├── generated_elements_validator.py   # Element validation
│   │   │   ├── prompts.py              # LLM prompt templates
│   │   │   └── utils.py                # VE tool utilities
│   │   └── visual_editor_bridge/       # WebSocket-based VE DOM tools
│   │       ├── apply_change.py          # exp_ve_apply_change
│   │       ├── element_glob.py          # exp_ve_element_glob
│   │       ├── element_grep.py          # exp_ve_element_grep
│   │       ├── element_read.py          # exp_ve_element_read
│   │       ├── element_tree.py          # exp_ve_element_tree
│   │       ├── get_change_schema.py     # exp_ve_get_change_schema
│   │       ├── get_selector.py          # exp_ve_get_selector
│   │       ├── list_pending_changes.py  # exp_ve_list_pending_changes
│   │       ├── revert_change.py         # exp_ve_revert_change
│   │       ├── validate_change.py       # exp_ve_validate_change
│   │       └── utils.py                 # send_bridge_command() helper
│   └── http_client/           # Turnstile HTTP client
└── tests/                     # Mirrors src/ structure
    ├── conftest.py            # Shared fixtures: use_opti_id_auth, use_experimentation, httpx_mock helpers
    ├── authentication/        # Auth tests
    ├── authorization/         # Authorization tests
    ├── common/                # Client, agent, status route tests
    ├── services/              # Service-level tests (context, flags, opensearch, websocket_bridge, etc.)
    └── tools/                 # Tool-level tests (opensearch_query, result_summary, VE bridge, etc.)
```

---

## 2. Core Logic & Business Rules

### Tools (LLM-Callable Functions)

| Tool Name | Purpose | Key Input | Returns | Service/API Used |
|-----------|---------|-----------|---------|-----------------|
| `exp_get_schemas` | Retrieve entity schemas (fields, types, enums, relationships) for OpenSearch queries | `entities[]` (experiment, flag, audience, etc.) | Schema dict with query guidance | `OpenSearchQueryService` → TypeScript backend |
| `exp_execute_query` | Execute template-based queries against OpenSearch | `template` (JSON query), `project_id` | Query results dict | `OpenSearchQueryService` → TypeScript backend |
| `exp_summarize_test_result` | Summarize experiment/rule results with enriched metadata | `experiment_id`/`rule_id`, `project_id` | Results + variations + metrics + audiences | `OpenSearchQueryService` + `ExperimentationService` (result API) |
| `exp_manage_entity_lifecycle` | Create/update entities (flags, experiments, audiences, etc.) | `operation`, `entity_type`, `project_id`, `template_data` | `IslandResponse` (interactive) or string (headless) | `ExpManageEntityLifecycleService` → TypeScript backend |
| `exp_get_entity_templates` | Fetch create/update schemas for entity operations | `project_id`, `operation`, `entity_type` | JSON template with required fields | `ExpManageEntityLifecycleClient` → TypeScript backend |
| `exp_suggest_flag_variables` | Generate flag variable suggestions for feature experimentation | `variables[]`, `project_id`, `flag_key` | `IslandResponse` with variable islands | Direct (builds Island objects) |
| `exp_suggest_flag_variations` | Generate flag variation suggestions for feature experimentation | `variations[]`, `project_id`, `flag_key` | `IslandResponse` with variation islands | Direct (builds Island objects) |
| `exp_calculate_sample_size` | Calculate A/B test sample size and duration estimates | `baseline_rate`, `mde`, `significance`, `variants`, `visitors` | Dict with sample sizes + time estimates | Direct calculation (statistical formula) |
| `exp_search_fx_sdk_docs` | Search Optimizely FX SDK documentation | `query` (search string) | Answer + source citations | `FxSdkDocsSearchService` → Vertex AI Search |
| `exp_program_reporting_top_experiments` | Get top performing experiments by lift | `date_range`, `project_ids`, `direction` | Experiment list with lift values | `ProgramReportingService` → Program Reporting API |
| `exp_program_reporting_underperforming_experiments` | Get underperforming experiments | `date_range`, `project_ids` | Experiment list with significance/lift data | `ProgramReportingService` → Program Reporting API |
| `exp_program_reporting_win_rate` | Compute experimentation win rate | `date_range`, `project_ids` | Win/total counts + percentage | `ProgramReportingService` → Program Reporting API |
| `exp_suggest_visual_editor_component_improvements` | Generate design improvement suggestions for VE | `design_suggestions_json` | `IslandResponse` with improvement islands | Direct (parses JSON, builds Island objects) |

### Visual Editor Bridge Tools (WebSocket-Based)

| Tool Name | Purpose | Key Input | Returns |
|-----------|---------|-----------|---------|
| `exp_ve_apply_change` | Apply attribute/CSS/HTML/code/redirect changes | `changeType`, `selector`, `attributes`/`css`/`code`/`value` | Change result dict |
| `exp_ve_element_glob` | Find elements by CSS selector pattern | `selector`, `limit` | List of matching elements |
| `exp_ve_element_grep` | Search elements by text/attribute regex pattern | `pattern`, `selector`, `matchAttribute` | Matching elements with context |
| `exp_ve_element_read` | Read detailed element info (attributes, styles, children) | `selector`, `includeStyles`, `depth` | Element details dict |
| `exp_ve_element_tree` | Get DOM tree structure from root element | `selector`, `depth` | Tree representation |
| `exp_ve_get_change_schema` | Get schema documentation for change types | `changeType` (optional) | Schema with required fields + examples |
| `exp_ve_get_selector` | Generate CSS selector for element | `xpath`/`elementDescription`/`clickCoordinates` | Unique CSS selector |
| `exp_ve_list_pending_changes` | List unsaved changes in VE | `includeAll` | List of pending changes |
| `exp_ve_revert_change` | Undo a previously applied change | `changeId` | Revert result |
| `exp_ve_validate_change` | Execute validation JavaScript in page context | `script` (JS expression) | Script result + execution time |

### Services

| Service | Purpose | Key Files | External API |
|---------|---------|-----------|-------------|
| **Context Service** | Maps Opal URLs to API calls, enriches context for LLM | `services/context/constants.py`, `service.py`, `formatters/`, `processors/` | Experimentation API, Flags API, ICE API |
| **Interaction Island** | Executes user-confirmed actions from tool Islands | `services/interaction_island/routes.py`, `services.py`, `dtos.py` | Flags API (variables, variations), Entity lifecycle |
| **OpenSearch Query** | Proxies schema/query requests to TypeScript query engine | `services/opensearch_query/service.py`, `client.py` | TypeScript Backend (port 3000) |
| **Entity Lifecycle** | Creates/updates Optimizely entities via templates | `services/exp_manage_entity_lifecycle/service.py`, `client.py` | TypeScript Backend (port 3000) |
| **Experimentation** | Fetches experiment results from result API | `services/experimentation/services.py` | Experimentation API (`/v2/experiments/{id}/results`) |
| **Flags** | Flag CRUD operations | `services/flags/services.py`, `dtos.py` | Flags API (`/projects/{id}/flags/*`) |
| **FX SDK Docs Search** | Searches SDK documentation via Vertex AI | `services/fx_sdk_docs_search/service.py`, `client.py` | Google Vertex AI Search |
| **Program Reporting** | Analytics queries (win rate, top/underperforming) | `services/program_reporting/services.py`, `dtos.py` | Program Reporting API |
| **WebSocket Bridge** | Manages WebSocket connections to Visual Editor browser | `services/websocket_bridge/manager.py`, `routes.py`, `models.py` | Direct WebSocket to browser |
| **Agent Directory** | Registers and discovers AI agents | `services/agent_directory/routes.py`, `service.py` | HMAC-authenticated endpoints |
| **Refresh Token** | Handles Opal token refresh | `services/refresh_token/routes.py`, `service.py` | Opal App |
| **LLM Usage** | Tracks LLM token usage | `services/llm_usage/llm_usage_service.py` | Internal tracking |

### Key Business Rules

| Rule | Description | Code Location |
|------|-------------|---------------|
| Tool registration | All tools MUST be imported in `init_tools()` with `# noqa: F401` | `src/tools/__init__.py` |
| Schema-first workflow | `exp_get_schemas` MUST be called before `exp_execute_query` | Tool descriptions enforce this |
| Template-first workflow | `exp_get_entity_templates` MUST be called before `exp_manage_entity_lifecycle` | Tool descriptions enforce this |
| Interactive vs Headless | Entity lifecycle supports both modes via `execution_mode` env key | `src/tools/exp_manage_entity_lifecycle.py:374` |
| Integer-to-string conversion | All integer IDs converted to strings to prevent JS precision loss | `src/tools/utils.py:convert_integers_to_strings()` |
| URL context matching | URL patterns in `constants.py` use regex with named capture groups | `src/services/context/constants.py` |
| Dependency chains | API calls can depend on prior responses via `depends_on` + `extract_params` | `src/services/context/models.py:MappedApiUrlConfig` |
| Platform detection | Tools auto-detect Web vs Custom/FX projects for correct entity types | `result_summary.py`, `opensearch_query.py` |
| Auth dual-layer | Ingress: OptiID JWT or API Gateway; Egress: token/cookie/internal per client | `src/authentication/` |
| WebSocket bridge routing | Thread ID from `x-opal-thread-id` header routes commands to correct browser | `src/tools/visual_editor_bridge/utils.py` |

### Context Service URL Patterns (from `src/services/context/constants.py`)

| URL Pattern | Response Tags | Formatter/Processor |
|-------------|--------------|-------------------|
| `/v2/projects/{project_id}/audiences` | audiences | — |
| `/v2/projects/{project_id}/audiences/{audience_id}/#modal` | audience | — |
| `/v2/projects/{project_id}/experiments/{experiment_id}` | experiment, project, running_experiments, hypothesis, pages, audiences, layer | `ExperimentDetailsFormatter` / `ExperimentDetailsProcessor` |
| `/v2/projects/{project_id}/results/{layer_id}/experiments/{experiment_id}` | experiment, hypothesis, audiences, results | — |
| `/v2/projects/{project_id}/flags/list` | flags | `flags_list_formatter` + `FlagsInstructions.flags_list` |
| `/v2/projects/{project_id}/flags/manage/{flag_key}` | flag | — |
| `/v2/projects/{project_id}/flags/manage/{flag_key}/rules/{env_key}` | ruleset | — |
| `/v2/projects/{project_id}/flags/manage/{flag_key}/rules/{env_key}/edit/{rule_key}` | ruleset | `RuleDetailsFormatter` / `RuleDetailsProcessor` |
| `/v2/projects/{project_id}/flags/manage/{flag_key}/variables` | variables | `FlagsInstructions.flags_variable` |
| `/v2/projects/{project_id}/flags/manage/{flag_key}/variations` | variations, variables | `FlagsInstructions.flags_variation` |
| `/v2/projects/{project_id}/experiment_list` | experiments | — |
| `/v2/projects/{project_id}/personalizations` | campaigns | — |
| `/v2/projects/{project_id}/campaigns/{campaign_id}` | campaign | — |
| `/v2/projects/{project_id}/implementation/pages` | pages | — |

---

## 3. QA & Testing Standards

### Test Commands

```bash
make test                          # Run pytest + mypy (standard CI check)
make test-pytest-with-coverage     # Run tests with coverage report
pytest tests/path/to/test.py       # Run specific test file
pytest tests/path/to/test.py::test_function  # Run specific test

# Code quality checks
make check-format                  # black --check
make check-lint                    # flake8 + pylint
make format                        # Auto-fix formatting
```

### Quality Standards

| Check | Tool | Threshold |
|-------|------|-----------|
| Formatting | Black | Line length 120 chars |
| Linting | flake8 | Max line length 120 |
| Linting | pylint | Score >= 7.0 |
| Type checking | mypy | All functions require type hints |
| Import order | isort | Black profile |
| Tests | pytest | All must pass |
| Unused code | flake8/autoflake | No unused variables or imports |

### Test Architecture

- **Test structure mirrors `src/`** — e.g., `tests/tools/test_opensearch_query.py` tests `src/tools/opensearch_query.py`
- **Async mode**: `asyncio_mode = "auto"` configured in `pyproject.toml`
- **HTTP mocking**: `httpx_mock` fixture (from `pytest-httpx`) — mock ALL external HTTP calls

### Key Test Fixtures (from `tests/conftest.py`)

| Fixture | Purpose | Usage |
|---------|---------|-------|
| `use_opti_id_auth` | Patches Okta JWT verification to accept any token | All tests requiring auth |
| `use_experimentation` | Patches all external API base URLs to test URLs | Tests calling Experimentation/Flags/ICE APIs |
| `httpx_mock` | Mocks httpx HTTP calls | All tests with external API calls |
| `mock_http_responses` | Loads mock responses from YAML files | Complex multi-API test scenarios |
| `non_mocked_hosts` | Prevents mocking TestClient (httpx-based) | Integration tests via FastAPI TestClient |

### Test Pattern Example

```python
def test_context_experiment_details(httpx_mock, use_opti_id_auth, use_experimentation):
    httpx_mock.add_response(
        url="http://test_experimentation_base_url/v2/experiments/123",
        json={"id": 123, "name": "Test Experiment", "status": "running"}
    )
    # ... test implementation
```

### Critical Test Paths

| Area | Test Files | What They Cover |
|------|-----------|----------------|
| OpenSearch Query | `tests/tools/test_opensearch_query.py`, `test_opensearch_query_date_filters.py` | Schema retrieval, query execution, date filter validation, project_id normalization |
| Entity Lifecycle | `tests/tools/exp_manage_entity_lifecycle/` | Create/update operations, variable definitions, variations, template mode enforcement |
| Context Service | `tests/services/context/` | URL matching, API call orchestration, formatters, processors, security |
| VE Bridge | `tests/tools/visual_editor_bridge/`, `tests/services/websocket_bridge/` | WebSocket commands, bridge utilities, HTTP client |
| Result Summary | `tests/tools/test_result_summary.py` | Web experiment + FX rule result enrichment |
| Flags | `tests/services/flags/test_service.py` | Flag CRUD operations |
| Authentication | `tests/authentication/`, `tests/authorization/` | OptiID auth, auth utils, org authorization |

---

## 4. JIRA Analysis Context

### Ticket Type to Code Area Mapping

| Ticket Keywords | Primary Code Area | Secondary Code Area |
|----------------|-------------------|-------------------|
| tool, new tool, tool registration | `src/tools/`, `src/tools/__init__.py` | `src/services/interaction_island/` |
| context, URL matching, context enrichment | `src/services/context/constants.py`, `formatters/`, `processors/` | `src/common/client/` |
| entity lifecycle, create entity, update entity | `src/tools/exp_manage_entity_lifecycle.py`, `src/services/exp_manage_entity_lifecycle/` | `src/services/interaction_island/` |
| flag, flag variable, flag variation | `src/tools/flag_variable_brainstorm.py`, `flag_variation_brainstorm.py` | `src/services/flags/`, `src/services/interaction_island/` |
| opensearch, query, schema | `src/tools/opensearch_query.py`, `src/services/opensearch_query/` | TypeScript backend (external) |
| visual editor, VE, design improvement | `src/tools/visual_editor/`, `src/tools/visual_editor_bridge/` | `src/services/websocket_bridge/` |
| websocket, bridge, DOM | `src/tools/visual_editor_bridge/`, `src/services/websocket_bridge/` | `src/context_vars.py` |
| result, summarize, experiment result | `src/tools/result_summary.py` | `src/services/experimentation/`, `src/services/opensearch_query/` |
| sample size, calculator | `src/tools/sample_size_calculator.py` | — |
| SDK docs, FX SDK, documentation search | `src/tools/fx_sdk_docs_search.py`, `src/services/fx_sdk_docs_search/` | Vertex AI Search (external) |
| program reporting, win rate, top experiments | `src/tools/pgm_reporting/` | `src/services/program_reporting/` |
| auth, authentication, JWT, Okta | `src/authentication/ingress/`, `src/authentication/egress/` | `src/common/client/` |
| island, interaction, confirmation | `src/services/interaction_island/` | `src/tools/` (any tool returning IslandResponse) |
| agent, agent directory | `src/services/agent_directory/` | `src/common/agent/builder.py` |
| template, entity template | `src/tools/exp_get_entity_templates.py` | `src/services/exp_manage_entity_lifecycle/client.py` |

### Complexity Assessment Scale

| Complexity | Description | Example |
|-----------|-------------|---------|
| **S** (Small) | Single file change, config update, description tweak | Update tool description text, add env variable |
| **M** (Medium) | New tool or service endpoint, moderate logic | Add new program reporting tool, new context URL pattern |
| **L** (Large) | New service module, cross-cutting changes | New WebSocket command type, new entity type in lifecycle |
| **XL** (Extra Large) | Architecture changes, new auth mechanism, new external integration | New API client type, new egress auth mechanism |

---

## 5. Functional Tree (UI to Code Map)

> **Opal Tools is a backend service** — it does not have its own UI. Its "functional tree" maps Opal Chat features (in the Opal frontend) to the backend tools and services that power them. The primary consumer is the **Opal Chat Panel** in the Visual Editor and the **Opal Chat** in the Optimizely App.

---

### 1. Opal Chat Panel in Visual Editor (Primary Focus)

> **Context**: When a user opens the Visual Editor and clicks the "Build Variation" (Opal CTA) button, the Opal Chat panel opens. The chat connects to opal-tools via HTTP tool calls and WebSocket bridge. The VE browser establishes a WebSocket connection at `/ws/{thread_id}`.

#### 1.1. DOM Exploration & Element Discovery

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **Find elements by CSS selector** | Search page for elements matching a CSS pattern (buttons, links, classes) | `src/tools/visual_editor_bridge/element_glob.py` → `exp_ve_element_glob` | `send_bridge_command("ElementGlob")` → WebSocket → browser |
| **Search elements by text/regex** | Find elements containing text matching a regex pattern, optionally in attributes | `src/tools/visual_editor_bridge/element_grep.py` → `exp_ve_element_grep` | `send_bridge_command("ElementGrep")` → WebSocket → browser |
| **Read element details** | Get comprehensive element info: tag, attributes, text, computed styles, children | `src/tools/visual_editor_bridge/element_read.py` → `exp_ve_element_read` | `send_bridge_command("ElementRead")` → WebSocket → browser |
| **Get DOM tree structure** | Hierarchical tree view from a root element showing nesting | `src/tools/visual_editor_bridge/element_tree.py` → `exp_ve_element_tree` | `send_bridge_command("ElementTree")` → WebSocket → browser |
| **Generate CSS selector** | Create unique selector via XPath, description, or click coordinates | `src/tools/visual_editor_bridge/get_selector.py` → `exp_ve_get_selector` | `send_bridge_command("GetSelector")` → WebSocket → browser |

#### 1.2. Change Application & Management

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **Apply change to page** | Modify attributes/CSS, insert HTML, inject JS/CSS, redirect | `src/tools/visual_editor_bridge/apply_change.py` → `exp_ve_apply_change` | `send_bridge_command("ApplyChange")` → WebSocket → browser |
| **Get change schema** | Retrieve format documentation for each change type (attribute, insert_html, custom_code, etc.) | `src/tools/visual_editor_bridge/get_change_schema.py` → `exp_ve_get_change_schema` | `send_bridge_command("GetChangeSchema")` → WebSocket → browser |
| **List pending changes** | Show unsaved changes in current VE session | `src/tools/visual_editor_bridge/list_pending_changes.py` → `exp_ve_list_pending_changes` | `send_bridge_command("ListPendingChanges")` → WebSocket → browser |
| **Revert a change** | Undo a specific change by ID | `src/tools/visual_editor_bridge/revert_change.py` → `exp_ve_revert_change` | `send_bridge_command("RevertChange")` → WebSocket → browser |
| **Validate change** | Execute JavaScript validation to verify changes took effect | `src/tools/visual_editor_bridge/validate_change.py` → `exp_ve_validate_change` | `send_bridge_command("ValidateChange")` → WebSocket → browser |

#### 1.3. Design Improvement Suggestions

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **Generate design suggestions** | AI-powered CRO/UX analysis producing multiple design variation ideas | `src/tools/visual_editor/design_improvement_suggestions.py` → `exp_suggest_visual_editor_component_improvements` | Direct — parses JSON, returns `IslandResponse` with improvement islands |
| **Element validation** | Validate generated elements against page structure | `src/tools/visual_editor/generated_elements_validator.py` | — |
| **LLM prompts** | Prompt templates for design analysis | `src/tools/visual_editor/prompts.py` | — |

#### 1.4. WebSocket Bridge Infrastructure

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **WebSocket connection** | Browser VE connects at `/ws/{thread_id}` with OptiID auth | — | `src/services/websocket_bridge/routes.py` |
| **Connection manager** | Manages active WebSocket connections, routes commands by thread_id | — | `src/services/websocket_bridge/manager.py` |
| **Bridge command dispatcher** | Routes tool calls to correct browser via thread_id from `x-opal-thread-id` header | `src/tools/visual_editor_bridge/utils.py` → `send_bridge_command()` | `src/services/websocket_bridge/http_client.py` (remote WS service) |
| **Error handling** | `WebSocketError` / `WebSocketErrorCode` for NO_CONNECTION, NO_THREAD_ID, TIMEOUT | — | `src/services/websocket_bridge/models.py` |

#### 1.5. Interaction Island Execution (VE Context)

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **Save changes** | Execute save from interaction island | — | `POST /interactions/save-changes` → `InteractionIslandService.execute_visual_editor_save_changes()` |
| **Check code changes** | Verify code changes from island | — | `POST /interactions/check-code-changes` → `InteractionIslandService.execute_check_code_changes()` |
| **Design improvement** | Execute design improvement from island | — | `POST /interactions/design-improvement` → `InteractionIslandService.execute_visual_editor_design_improvement()` |

---

### 2. Opal Chat in Optimizely App (Experimentation Context)

> **Context**: When a user is on any Optimizely App page and opens the Opal Chat panel, the chat uses the current URL for context enrichment and provides tools for querying, managing, and analyzing experiments.

#### 2.1. Context Enrichment (URL-Based)

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **URL context resolution** | Match current Opal URL to fetch relevant API data for LLM context | — | `src/services/context/service.py`, `constants.py` (URL pattern → API mapping) |
| **Experiment details** | Enrich experiment page with experiment, project, pages, audiences, hypothesis | — | `ExperimentDetailsFormatter`, `ExperimentDetailsProcessor` |
| **Rule details** | Enrich flag rule page with ruleset data | — | `RuleDetailsFormatter`, `RuleDetailsProcessor` |
| **Flags context** | Enrich flags list/detail pages with flag data | — | `flags_list_formatter`, `FlagsInstructions` |
| **Context route** | `GET /context` endpoint serving enriched context | — | `src/services/context/routes.py` |

#### 2.2. OpenSearch Query Engine (Data Querying)

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **Get entity schemas** | Retrieve schemas for 13+ entity types with fields, types, relationships | `src/tools/opensearch_query.py` → `exp_get_schemas` | `OpenSearchQueryService.get_schemas()` → TypeScript backend |
| **Execute queries** | Run template-based queries with filters, enrichment, pagination | `src/tools/opensearch_query.py` → `exp_execute_query` | `OpenSearchQueryService.execute_query()` → TypeScript backend |
| **Entity types supported** | experiment, flag, campaign, experience, rule, audience, event, page, project, environment, extension, attribute, experimentsection | — | Schema definitions in TypeScript backend |

#### 2.3. Entity Lifecycle Management

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **Get entity templates** | Fetch create/update schemas for any entity type | `src/tools/exp_get_entity_templates.py` → `exp_get_entity_templates` | `ExpManageEntityLifecycleClient.get_entity_templates()` → TypeScript backend |
| **Create entities** | Create flags, experiments, audiences, events, pages, campaigns, etc. | `src/tools/exp_manage_entity_lifecycle.py` → `exp_manage_entity_lifecycle` (operation="create") | `ExpManageEntityLifecycleService` → TypeScript backend |
| **Update entities** | Update existing entities with new field values | `src/tools/exp_manage_entity_lifecycle.py` → `exp_manage_entity_lifecycle` (operation="update") | `ExpManageEntityLifecycleService` → TypeScript backend |
| **Interactive mode** | Returns `IslandResponse` for user confirmation before execution | `_build_entity_lifecycle_island()` | `POST /interactions/entity-lifecycle-create`, `POST /interactions/entity-lifecycle-update` |
| **Headless mode** | Executes directly without user confirmation (for automated flows) | `exp_manage_entity_lifecycle.py:428` | `ExpManageEntityLifecycleService.manage_entity_lifecycle()` |
| **Island: Create flag variable** | Confirm and create flag variable | `src/tools/flag_variable_brainstorm.py` | `POST /interactions/flag-variable` → `InteractionIslandService` |
| **Island: Create flag variation** | Confirm and create flag variation | `src/tools/flag_variation_brainstorm.py` | `POST /interactions/flag-variation` → `InteractionIslandService` |

#### 2.4. Flag Brainstorming

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **Suggest flag variables** | AI generates variable definitions (key, type, default_value, description) based on hypothesis | `src/tools/flag_variable_brainstorm.py` → `exp_suggest_flag_variables` | Returns `IslandResponse` → user confirms → `POST /interactions/flag-variable` |
| **Suggest flag variations** | AI generates variation configs with variable values based on hypothesis | `src/tools/flag_variation_brainstorm.py` → `exp_suggest_flag_variations` | Returns `IslandResponse` → user confirms → `POST /interactions/flag-variation` |

#### 2.5. Experiment Results & Analysis

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **Summarize test results** | Fetch and enrich experiment/rule results with metadata | `src/tools/result_summary.py` → `exp_summarize_test_result` | `OpenSearchQueryService` (metadata) + `ExperimentationService.get_experiment_results()` (result API) |
| **Platform auto-detection** | Detect Web vs Custom/FX project to query correct entity type | `result_summary.py:227` | `OpenSearchQueryService` (project platform query) |
| **Sample size calculator** | Calculate required sample size and test duration | `src/tools/sample_size_calculator.py` → `exp_calculate_sample_size` | Direct statistical calculation |

#### 2.6. Program Reporting (Analytics)

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **Top experiments** | Get experiments with highest/lowest lift values | `src/tools/pgm_reporting/top_experiments.py` → `exp_program_reporting_top_experiments` | `ProgramReportingService.fetch_analytics()` (template: TOP_EXPERIMENTS) |
| **Underperforming experiments** | Identify experiments with low significance, negligible lift, stale status | `src/tools/pgm_reporting/underperforming_experiments.py` → `exp_program_reporting_underperforming_experiments` | `ProgramReportingService.fetch_analytics()` (template: UNDERPERFORMING_EXPERIMENTS) |
| **Win rate** | Compute experiment win rate (wins / total paused+concluded) | `src/tools/pgm_reporting/win_rate.py` → `exp_program_reporting_win_rate` | `ProgramReportingService.fetch_analytics()` (template: WIN_RATE) |

#### 2.7. SDK Documentation Search

| Feature | Description | Code (Tools) | Code (Services/API) |
|---------|-------------|--------------|---------------------|
| **Search FX SDK docs** | Search Optimizely Feature Experimentation SDK documentation | `src/tools/fx_sdk_docs_search.py` → `exp_search_fx_sdk_docs` | `FxSdkDocsSearchService.search()` → Google Vertex AI Search |
| **SDK coverage** | JavaScript, Python, Java, PHP, Ruby, Swift, Android, and more | — | Vertex AI Search engine with indexed SDK docs |

---

### 3. Shared Infrastructure (Cross-Cutting)

#### 3.1. Authentication

| Feature | Description | Code |
|---------|-------------|------|
| **OptiID ingress auth** | Validates Okta JWT tokens from Opal users | `src/authentication/ingress/opti_id/auth.py` |
| **API Gateway ingress auth** | For gateway-routed requests | `src/authentication/ingress/opal_api_gw/auth.py` |
| **WebSocket auth** | Authenticates WebSocket connections | `src/authentication/ingress/websocket_authentication.py` |
| **Egress auth manager** | Selects auth mechanism per outbound API client | `src/authentication/egress/auth_manager.py` |
| **EXP_INTERNAL_TOKEN** | Internal service token for Experimentation API | `src/authentication/egress/exp_internal_token/` |
| **EXP_COOKIE** | Cookie-based auth forwarded from user requests | `src/authentication/egress/exp_cookie/` |
| **Organization authorization** | `@inject_admin_account_ids` decorator for admin-scoped operations | `src/authorization/ingress/decorators.py` |

#### 3.2. HTTP Clients

| Client | Purpose | Code |
|--------|---------|------|
| `BaseClient` | Base HTTP client with retry logic and auth injection | `src/common/client/base_client.py` |
| `ExperimentationClient` | Experimentation API v2 calls | `src/common/client/experimentation_client.py` |
| `IceClient` | Internal Content Engine API | `src/common/client/ice_client.py` |
| `GcsClient` | Google Cloud Storage operations | `src/common/client/gcs_client.py` |
| `HmacHttpClient` | HMAC-authenticated HTTP calls (for agent directory, program reporting) | `src/common/client/hmac_http_client.py` |
| `UserManagementClient` | User management API calls | `src/common/client/user_management_client.py` |

#### 3.3. Environment Configuration

| Variable | Required | Purpose |
|----------|----------|---------|
| `GCP_PROJECT_ID` | Yes | Google Cloud project ID |
| `AUTH_ISSUER` | Yes | Okta JWT issuer URL |
| `EXP_BASE_API_URL` | No (default: develrc) | Experimentation API v2 base URL |
| `FLAG_BASE_API_URL` | No (default: develrc) | Flags API base URL |
| `EXP_BASE_API_URL_V1` | No (default: develrc) | Experimentation API v1 base URL |
| `ICE_BASE_API_URL` | No (default: inte) | Internal Content Engine API URL |
| `TYPESCRIPT_BACKEND_BASE_URL` | No (default: auto-detected) | TypeScript backend for OpenSearch/entity lifecycle |
| `PROGRAM_REPORTING_BASE_URL` | No (default: inte) | Program Reporting API URL |
| `WEBSOCKET_SERVICE_URL` | No | External WebSocket service URL (for production) |
| `LOG_LEVEL` | No (default: INFO) | Logging level |
| `RUNTIME_ENVIRONMENT` | No | Environment identifier (affects root_path) |

#### 3.4. Routers (from `main.py`)

| Router | Prefix | Purpose |
|--------|--------|---------|
| `misc_router` | — | Health check, status endpoints |
| `context_router` | `/context` | URL-to-context enrichment |
| `refresh_token_router` | — | Token refresh |
| `interaction_island_router` | `/interactions` | Island action execution |
| `fx_sdk_docs_router` | — | FX SDK documentation search |
| `opensearch_query_router` | — | OpenSearch query proxy |
| `agent_directory_router` | — | Agent registration/discovery |
| `websocket_bridge_router` | `/ws` (mounted as sub-app) | WebSocket connections |
| **Tools** (auto-registered) | `/tools/*` (via `ToolsService`) | All `@tool()` decorated functions |

---

### 4. Cross-System Connection Map

```
Optimizely App (Monolith)                        opal-tools (Backend)
───────────────────────────                       ────────────────────
Opal Chat Panel (all pages)
  └─ User sends message ──── HTTP ────→  @tool() functions
     with context URL                    ├─ exp_get_schemas + exp_execute_query
                                         ├─ exp_manage_entity_lifecycle
                                         ├─ exp_summarize_test_result
                                         ├─ exp_suggest_flag_variables/variations
                                         ├─ exp_calculate_sample_size
                                         ├─ exp_search_fx_sdk_docs
                                         └─ exp_program_reporting_*

Visual Editor (Browser, customer website)          opal-tools (Backend)
─────────────────────────────────────────          ────────────────────
Opal Chat in VE ("Build Variation")
  ├─ WebSocket ───── /ws/{thread_id} ───→  websocket_bridge/manager.py
  │   (VE browser connects)                (manages connections)
  │
  └─ User sends message ──── HTTP ────→  VE Bridge @tool() functions
     with x-opal-thread-id               ├─ exp_ve_element_glob/grep/read/tree
                                          ├─ exp_ve_apply_change
                                          ├─ exp_ve_get_selector
                                          ├─ exp_ve_get_change_schema
                                          ├─ exp_ve_list_pending_changes
                                          ├─ exp_ve_revert_change
                                          └─ exp_ve_validate_change
                                               │
                                               └── send_bridge_command()
                                                    → WebSocket → browser → DOM result

Interaction Islands (User Confirmation UI)         opal-tools (Backend)
──────────────────────────────────────────         ────────────────────
Tool returns IslandResponse
  └─ User clicks "Confirm" ──── HTTP ───→  /interactions/* endpoints
     with island field data               ├─ /flag-variable (create flag var)
                                          ├─ /flag-variation (create flag variation)
                                          ├─ /entity-lifecycle-create
                                          ├─ /entity-lifecycle-update
                                          ├─ /save-changes (VE save)
                                          ├─ /check-code-changes (VE code check)
                                          └─ /design-improvement (VE design)
```

**Communication**: Opal Chat Frontend ↔ opal-tools via HTTP (tool calls) + WebSocket (VE bridge)
**Auth**: OptiID JWT token passed in Authorization header → validated by ingress auth → egress auth injects credentials for external API calls
**Data**: Tools query external APIs (Experimentation, Flags, OpenSearch, Vertex AI) and return structured responses or IslandResponse for user interaction
