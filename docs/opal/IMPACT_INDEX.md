# Impact Index — Opal Tools

> **Purpose**: Lookup table for blast radius analysis during ticket review.
> When a ticket mentions a file/module, find its entry here to instantly see what else is impacted.
>
> **Source of truth**: `CLAUDE.md` (Architecture & Core Logic sections)
> **Scope**: `optimizely/opal-tools` repo (Python FastAPI backend service)
> **Last Updated**: 2026-03-17

---

## How to Use

1. Find the file/module mentioned in the ticket
2. Read "If changed, impacts" -> these are downstream consumers that need regression testing
3. Read "Critical path" -> these are the test flows that must pass
4. Check "Test file" to find existing tests to run
5. Check "Cross-repo" for impacts on the Visual Editor browser-side code

---

## Cross-Repo Impact (opal-tools <-> visual-editor)

The two repos communicate via **WebSocket bridge** and **Opal Chat events**. Changes in one repo can break the other.

### Integration Architecture

```
opal-tools (Python backend)                     visual-editor (Browser frontend)
--------------------------                      --------------------------------
src/tools/visual_editor_bridge/                 src/llm-tools/
  apply_change.py         <-- WebSocket -->       tools/applyChange.ts
  element_glob.py         <-- WebSocket -->       tools/elementGlob.ts
  element_grep.py         <-- WebSocket -->       tools/elementGrep.ts
  element_read.py         <-- WebSocket -->       tools/elementRead.ts
  element_tree.py         <-- WebSocket -->       tools/elementTree.ts
  get_selector.py         <-- WebSocket -->       tools/getSelector.ts
  get_change_schema.py    <-- WebSocket -->       tools/getChangeSchema.ts
  list_pending_changes.py <-- WebSocket -->       tools/listPendingChanges.ts
  revert_change.py        <-- WebSocket -->       tools/revertChange.ts
  validate_change.py      <-- WebSocket -->       tools/jsValidator.ts (ValidateChange)

src/services/websocket_bridge/                  src/llm-tools/
  manager.py (server)     <-- WebSocket -->       websocket-bridge.ts (client)
  routes.py (/ws/{thread_id})                     server.ts (executeTool dispatcher)

src/tools/visual_editor/                        src/components/common/opal-chat/
  design_improvement_suggestions.py               OpalChat.tsx (renders LazyAIChatComponent)
    -> returns IslandResponse                      OpalCTA.tsx (dispatches VariationCodeGenerationRequested)
    -> POST /interactions/design-improvement       useOpalEvents.ts (loads remote event names)
                                                   useOpalPromptQueue.ts (loads remote prompt queue)
                                                   constants.ts (DEFAULT_EVENT_NAMES)
                                                   lazy_opal_chat.tsx (Module Federation loader)

src/services/interaction_island/                src/stores/opalChatStore.ts
  routes.py (/interactions/*)                     (thread management, selector-thread mapping)
    -> /save-changes                             src/stores/changeStore.ts
    -> /check-code-changes                        (Opal-generated changes applied here)
    -> /design-improvement
    -> /flag-variable
    -> /flag-variation
    -> /entity-lifecycle-create
    -> /entity-lifecycle-update
```

### Shared Contract (MCPToolName enum — must match both sides)

Commands sent over WebSocket must match the `MCPToolName` type in VE `src/llm-tools/types.ts`:
`ElementGlob | ElementGrep | ElementRead | ElementTree | ApplyChange | GetSelector | ListPendingChanges | RevertChange | GetChangeSchema | ValidateChange`

### Integration Points Summary

| opal-tools File | VE File | Protocol | What Changes |
|----------------|---------|----------|-------------|
| `src/services/websocket_bridge/routes.py` | `src/llm-tools/websocket-bridge.ts` | WebSocket `/ws/{thread_id}` | Connection lifecycle, auth token, ping/pong |
| `src/services/websocket_bridge/manager.py` | `src/llm-tools/websocket-bridge.ts` | WebSocket JSON messages | Command routing, response futures, timeouts |
| `src/services/websocket_bridge/models.py` | `src/llm-tools/types.ts` | Shared data contract | MCPCommand/MCPResponse schema, MCPToolName enum |
| `src/tools/visual_editor_bridge/*.py` | `src/llm-tools/tools/*.ts` | WebSocket command args | Parameter names/types, return value schema |
| `src/tools/visual_editor_bridge/utils.py` | `src/llm-tools/server.ts` | WebSocket via `send_bridge_command()` | Command name routing to tool handlers |
| `src/services/interaction_island/routes.py` | `src/components/common/opal-chat/OpalChat.tsx` | HTTP POST `/interactions/*` | Island field names, action endpoints |
| `src/services/interaction_island/dtos.py` | `src/components/common/opal-chat/OpalChat.tsx` | JSON (IslandResponse) | Island field labels, action types |
| `src/tools/visual_editor/design_improvement_suggestions.py` | `src/components/common/opal-chat/OpalChat.tsx` | IslandResponse → event | `OPAL_INTERACTION_ISLAND_CLICKED` event |
| `src/services/context/routes.py` | `src/components/common/opal-chat/OpalChat.tsx` | HTTP GET `/context` | Context messages injected into chat |

### Opal Event Names (VE `src/components/common/opal-chat/constants.ts`)

These events flow between VE and the federated Opal Chat module. opal-tools does NOT listen to these directly — but its tool responses and IslandResponses trigger them indirectly:

| Event | VE Consumer | opal-tools Trigger |
|-------|------------|-------------------|
| `opal::canvas::elementsUpdated` | OpalChat.tsx | VE bridge `ApplyChange` / `RevertChange` results |
| `opal::interactionIsland::clicked` | OpalChat.tsx | Any tool returning `IslandResponse` |
| `opal::thread::created` | OpalChat.tsx → `connectBridge()` | New Opal thread → WebSocket connection established |
| `opal::thread::changed` | OpalChat.tsx → `connectBridge()` | Thread switch → WebSocket reconnection |
| `opal::response::completed` | OpalChat.tsx | Tool call response finished |
| `opal::chatbox::closed` | OpalChat.tsx | Chat panel closed |
| `opal::chatbox::dockStateChanged` | OpalChat.tsx | Dock/popout toggle |
| `VariationCodeGenerationRequested` | OpalCTA.tsx → OpalChat.tsx | User clicks "Build Variation" button |

---

## Layer 1: State & Configuration (Highest Blast Radius)

---

### `src/context_vars.py`
- **Type**: Request-scoped state
- **Purpose**: Thread-safe context variables set per request via `ContextMiddleware` — stores auth tokens, thread IDs, cookies for downstream use
- **Key functions**: `get_context_var()`, `set_context_var()`, context var constants (`opal_thread_id`, `experimentation_cookie`, `opti_id_access_token`, etc.)
- **If changed, impacts**:
  - **Tools**: ALL VE bridge tools (via `send_bridge_command()` → reads `opal_thread_id`)
  - **Clients**: `ExperimentationClient`, `ExperimentationClientV1`, `IceClient` (read auth tokens)
  - **Services**: `websocket_bridge/manager.py`, `interaction_island/services.py`
  - **Auth**: `authentication/egress/exp_cookie/handler.py`, `authentication/egress/exp_internal_token/handler.py`
  - **Cross-repo**: VE `websocket-bridge.ts` depends on `thread_id` matching `x-opal-thread-id` header
- **Critical path**: Authentication, WebSocket Bridge, ALL tool calls
- **Business rules**: Context vars are request-scoped via `contextvars.ContextVar` — changes here affect every request
- **Test file**: Implicitly tested via all service/tool tests using `use_experimentation` fixture

---

### `src/env_config.py`
- **Type**: Configuration (startup validation)
- **Purpose**: Loads and validates ALL environment variables on import — fails fast if required vars missing
- **Key functions**: `parse_bool()`, `_get_typescript_backend_default()`
- **If changed, impacts**:
  - **Every file that imports env vars** — `main.py`, ALL clients, ALL services, context constants
  - **Required vars**: `GCP_PROJECT_ID`, `AUTH_ISSUER` — missing = service won't start
  - **API URLs**: `EXP_BASE_API_URL`, `FLAG_BASE_API_URL`, `EXP_BASE_API_URL_V1`, `ICE_BASE_API_URL`, `TYPESCRIPT_BACKEND_BASE_URL`, `PROGRAM_REPORTING_BASE_URL`
  - **Auth**: `AUTH_ISSUER`, `AUTH_AUDIENCE`, `EXP_API_HASH_KEY`, `HMAC_CLIENT_KEY`, `HMAC_SECRET_KEY`
  - **WebSocket**: `WEBSOCKET_SERVICE_URL`, `WEBSOCKET_SERVICE_AUTH_SECRET`
- **Critical path**: Service startup, ALL API calls
- **Business rules**: Service crashes on import if `GCP_PROJECT_ID` or `AUTH_ISSUER` not set
- **Test file**: Tested indirectly; `.env.pytest` provides test values

---

### `src/tools/__init__.py`
- **Type**: Tool registry
- **Purpose**: `init_tools()` function that imports ALL tool modules via side-effect imports — called during FastAPI lifespan
- **Key functions**: `init_tools()` — 23 imports with `# noqa: F401`
- **If changed, impacts**:
  - **ALL tools**: Missing an import = tool silently not registered in Opal
  - **main.py**: Calls `init_tools()` during app lifespan
  - **Opal Chat**: Missing tool = feature unavailable in chat
- **Critical path**: Tool registration — every tool must be listed here
- **Business rules**: MUST add `# noqa: F401` import for every new tool file
- **Test file**: No direct test — verified by integration tests that call tools

---

### `src/common/decorators.py`
- **Type**: Cross-cutting decorators
- **Purpose**: `patch_tool_decorator()` wraps all `@tool()` functions with auth/context injection; `with_token_tracking_interaction_island` tracks token usage for island execution
- **If changed, impacts**:
  - **ALL tools**: `patch_tool_decorator()` modifies how every `@tool()` function receives auth_data and environment
  - **ALL interaction island endpoints**: `with_token_tracking_interaction_island` wraps every `/interactions/*` handler
  - **main.py**: Calls `patch_tool_decorator()` during app creation
- **Critical path**: Authentication (auth_data injection), ALL tool calls
- **Test file**: Implicitly tested via tool tests

---

### `src/services/interaction_island/dtos.py`
- **Type**: Shared data models
- **Purpose**: Defines `Island`, `IslandResponse`, `IslandExecuteResponse` — the interactive UI component contract between opal-tools and Opal Chat frontend
- **Key classes**: `Island` (fields + actions), `IslandResponse` (config with islands), `Island.Field`, `Island.Action`, `FlagVariableIslandData`, `FlagVariationIslandData`, `EntityLifecycleCreateIslandData`, `EntityLifecycleUpdateIslandData`
- **If changed, impacts**:
  - **Tools**: `exp_manage_entity_lifecycle`, `exp_suggest_flag_variables`, `exp_suggest_flag_variations`, `exp_suggest_visual_editor_component_improvements`
  - **Services**: `interaction_island/services.py`, `interaction_island/routes.py`
  - **Cross-repo**: VE `OpalChat.tsx` handles `OPAL_INTERACTION_ISLAND_CLICKED` events with island field data; field label changes break the handler
- **Critical path**: Entity creation (interactive mode), flag brainstorming, design improvements
- **Business rules**: Island field names/labels are part of the API contract — changes break frontend rendering
- **Test file**: `tests/services/interaction_island/test_routes.py`, `test_services.py`

---

## Layer 2: Core Modules (Business Logic)

---

### `src/tools/visual_editor_bridge/utils.py`
- **Type**: Module (shared utility)
- **Purpose**: `send_bridge_command()` — routes tool calls to browser via WebSocket (local manager or remote HTTP service)
- **Key functions**: `send_bridge_command(command_name, args)` — gets `thread_id` from context vars, dispatches to WebSocket manager or HTTP client
- **If changed, impacts**:
  - **ALL VE bridge tools**: `apply_change`, `element_glob`, `element_grep`, `element_read`, `element_tree`, `get_selector`, `get_change_schema`, `list_pending_changes`, `revert_change`, `validate_change`
  - **Cross-repo**: VE `websocket-bridge.ts` receives commands from this module
- **Critical path**: ALL VE bridge tool calls
- **Business rules**: Falls back to local WebSocket manager if remote service returns NO_CONNECTION
- **Test file**: `tests/tools/visual_editor_bridge/test_utils.py`

---

### `src/tools/utils.py`
- **Type**: Module (shared utility)
- **Purpose**: `convert_integers_to_strings()` — prevents JavaScript precision loss for large IDs
- **Key functions**: `convert_integers_to_strings(data)` — recursively converts all integers in dicts/lists to strings
- **If changed, impacts**:
  - **Tools**: `exp_execute_query`, `exp_summarize_test_result`
  - **Downstream**: Any consumer of OpenSearch results or result summaries
- **Critical path**: OpenSearch query results, result summary
- **Business rules**: Large integer IDs (>2^53) lose precision in JavaScript — ALL must be strings
- **Test file**: Implicitly tested via `test_opensearch_query.py`, `test_result_summary.py`

---

### `src/common/agent/builder.py`
- **Type**: Module (LLM agent wrapper)
- **Purpose**: `Agent` class wrapping `llm-framework` package — supports function calling, conversation management, thinking modes
- **Key functions**: `run(input)`, `_execute_llm_with_tools()`, `_create_conversation_from_prompt()`
- **If changed, impacts**:
  - **Tools**: `exp_suggest_visual_editor_component_improvements` (uses LLM for design analysis)
  - **Services**: `llm_usage/llm_usage_service.py` (receives usage metrics)
- **Critical path**: Design improvement suggestions (VE context)
- **Test file**: `tests/common/agent/test_builder.py`

---

### `src/services/context/constants.py`
- **Type**: Module (configuration)
- **Purpose**: `CONTEXT_URL_MAPPINGS` — declarative URL pattern-to-API-call mapping (27+ patterns)
- **Key data**: Array of `ContextUrlConfig` objects with regex patterns, API URLs, formatters, processors, dependency chains
- **If changed, impacts**:
  - **Context service**: `context/service.py` iterates these mappings for every context request
  - **Formatters**: `ExperimentDetailsFormatter`, `RuleDetailsFormatter`, `flags_list_formatter`
  - **Processors**: `ExperimentDetailsProcessor`, `RuleDetailsProcessor`
  - **Instructions**: `FlagsInstructions` (injected into LLM context)
  - **Downstream**: Opal Chat receives enriched context — wrong/missing pattern = LLM has no context for that page
- **Critical path**: Context enrichment — every Opal Chat session on Optimizely App
- **Business rules**: Patterns use regex with named capture groups; order matters (first match wins); `depends_on` creates dependency chains
- **Test file**: `tests/services/context/test_service.py`, `test_routes.py`

---

### `src/services/context/models.py`
- **Type**: Module (data models)
- **Purpose**: `ContextUrlConfig`, `MappedApiUrlConfig`, `ParamExtractorConfig` — declarative models for URL-to-API mapping
- **If changed, impacts**:
  - **Context constants**: `constants.py` instantiates these models
  - **Context service**: `service.py` reads these models to execute API calls
  - **Processors**: Use `extract_params`, `depends_on` configuration
- **Critical path**: Context enrichment
- **Test file**: `tests/services/context/test_service.py`

---

### `src/authorization/ingress/decorators.py`
- **Type**: Module (decorator)
- **Purpose**: `@inject_admin_account_ids` — injects authorized admin account IDs into auth_data for OpenSearch and program reporting tools
- **If changed, impacts**:
  - **Tools**: `exp_execute_query`, `exp_program_reporting_top_experiments`, `exp_program_reporting_underperforming_experiments`, `exp_program_reporting_win_rate`
  - **Downstream**: Query results scoped to wrong accounts if broken
- **Critical path**: OpenSearch queries, program reporting
- **Test file**: `tests/authorization/ingress/test_decorators.py`, `test_organization_authorization.py`

---

## Layer 3: Services & API Clients

---

### `src/services/websocket_bridge/manager.py`
- **Type**: Service (singleton)
- **Purpose**: `WebSocketManager` — manages active WebSocket connections, routes commands to correct browser session by `thread_id`, handles async response futures
- **Key functions**: `connect()`, `disconnect()`, `send_command()`, `handle_response()`
- **If changed, impacts**:
  - **VE bridge utils**: `send_bridge_command()` calls `websocket_manager.send_command()`
  - **WebSocket routes**: `routes.py` calls `websocket_manager.connect/disconnect`
  - **ALL VE bridge tools**: Indirectly — commands fail if manager broken
  - **Cross-repo**: VE `websocket-bridge.ts` is the client side of this connection
- **Critical path**: ALL VE bridge tool calls
- **Business rules**: 30-second default timeout; async response tracking with UUIDs; ping/pong heartbeat
- **Test file**: `tests/services/websocket_bridge/test_manager.py`

---

### `src/services/websocket_bridge/routes.py`
- **Type**: Service (WebSocket endpoint)
- **Purpose**: WebSocket endpoint at `/{thread_id}` — accepts browser connections, routes messages to manager
- **If changed, impacts**:
  - **Cross-repo**: VE `websocket-bridge.ts` connects to this endpoint (`wss://opal-tools/ws/{thread_id}`)
  - **VE `OpalChat.tsx`**: `connectBridge()` calls establish connections here
  - **Auth**: Uses `WebSocketAuthentication(AuthenticationMechanism.OPTIID)`
- **Critical path**: WebSocket connection lifecycle
- **Test file**: `tests/services/websocket_bridge/test_routes.py`

---

### `src/services/websocket_bridge/models.py`
- **Type**: Service (data models)
- **Purpose**: `MCPCommand`, `MCPResponse`, `WebSocketError`, `WebSocketErrorCode` — shared message format
- **If changed, impacts**:
  - **WebSocket manager**: Uses these models for command/response serialization
  - **VE bridge utils**: Checks for `WebSocketError` responses
  - **Cross-repo**: VE `types.ts` defines mirror `MCPCommand`/`MCPResponse` interfaces — MUST stay in sync
- **Critical path**: WebSocket message format
- **Business rules**: `MCPCommand.command` must match VE `MCPToolName` enum values exactly

---

### `src/common/client/base_client.py`
- **Type**: Client (abstract base)
- **Purpose**: Abstract HTTP client with `make_request()`, retry logic, auth header injection
- **If changed, impacts**:
  - **ALL clients**: `ExperimentationInternalClient`, `ExperimentationClient`, `ExperimentationClientV1`, `IceClient`
  - **ALL services** that use these clients
- **Critical path**: ALL external API calls
- **Risk**: Very high — change here breaks all API communication
- **Test file**: Implicitly tested via client tests

---

### `src/common/client/experimentation_client.py`
- **Type**: Client
- **Purpose**: Three client classes for Experimentation API: `ExperimentationInternalClient` (internal token), `ExperimentationClientV1` (cookie auth), `ExperimentationClient` (OptiID token)
- **If changed, impacts**:
  - **Context service**: Uses clients for API calls during context enrichment
  - **Experimentation service**: Uses `ExperimentationClient` for result API
  - **Flags service**: Indirectly via shared auth patterns
- **Critical path**: Context enrichment, result summary
- **Test file**: `tests/common/client/test_http_client.py`

---

### `src/common/client/http_client.py`
- **Type**: Client (httpx wrapper)
- **Purpose**: `AsyncHttpClient` — custom httpx client with request logging, exception handling (converts httpx errors to FastAPI exceptions)
- **If changed, impacts**:
  - **ALL HTTP clients**: Every client uses `AsyncHttpClient` under the hood
  - **Error handling**: Maps HTTP status codes to specific FastAPI exceptions (401 -> Unauthorized, 403 -> Forbidden, 504 -> GatewayTimeout, 5xx -> BadGateway)
- **Critical path**: ALL external API calls, error handling
- **Risk**: Very high — change here affects all HTTP communication
- **Test file**: `tests/common/client/test_http_client.py`

---

### `src/services/opensearch_query/service.py`
- **Type**: Service
- **Purpose**: `OpenSearchQueryService` — proxies schema/query requests to TypeScript backend
- **Key functions**: `get_schemas()`, `execute_query()`
- **If changed, impacts**:
  - **Tools**: `exp_get_schemas`, `exp_execute_query`, `exp_summarize_test_result`
  - **Downstream**: OpenSearch query results affect all data querying in Opal Chat
- **Critical path**: Entity querying, result summary
- **Test file**: `tests/services/opensearch_query/test_routes.py`

---

### `src/services/exp_manage_entity_lifecycle/service.py`
- **Type**: Service
- **Purpose**: `ExpManageEntityLifecycleService` — routes create/update operations to TypeScript backend
- **Key functions**: `manage_entity_lifecycle(operation, entity_type, project_id, ...)`
- **If changed, impacts**:
  - **Tools**: `exp_manage_entity_lifecycle` (both interactive and headless modes)
  - **Interaction island**: `entity-lifecycle-create`, `entity-lifecycle-update` endpoints
- **Critical path**: Entity creation/update
- **Test file**: `tests/services/exp_manage_entity_lifecycle/test_service.py`

---

### `src/services/exp_manage_entity_lifecycle/client.py`
- **Type**: Client
- **Purpose**: `ExpManageEntityLifecycleClient` — HTTP client for TypeScript backend (`TYPESCRIPT_BACKEND_BASE_URL`)
- **Key functions**: `get_entity_templates()`, `manage_entity_lifecycle()`
- **If changed, impacts**:
  - **Tools**: `exp_get_entity_templates`, `exp_manage_entity_lifecycle`
  - **Service**: `ExpManageEntityLifecycleService`
- **Critical path**: Entity templates, entity creation/update
- **Test file**: `tests/services/exp_manage_entity_lifecycle/test_client_error_message_extraction.py`

---

### `src/services/flags/services.py`
- **Type**: Service
- **Purpose**: `FlagsService` — creates flag variables and variations via Flags API (JSON Patch for variables, POST for variations)
- **Key functions**: `create_flag_variable()`, `create_flag_variation()`
- **If changed, impacts**:
  - **Interaction island**: `POST /interactions/flag-variable`, `POST /interactions/flag-variation`
  - **Tools**: `exp_suggest_flag_variables`, `exp_suggest_flag_variations` (island execution)
- **Critical path**: Flag variable/variation creation
- **Business rules**: Variables use JSON Patch format (`op: add`); variations use POST
- **Test file**: `tests/services/flags/test_service.py`

---

### `src/services/interaction_island/services.py`
- **Type**: Service
- **Purpose**: `InteractionIslandService` — executes user-confirmed island actions (flag vars, flag variations, entity lifecycle, VE save/check/design)
- **Key functions**: `execute_flag_variable_island()`, `execute_flag_variation_island()`, `execute_entity_lifecycle_create()`, `execute_entity_lifecycle_update()`, `execute_visual_editor_save_changes()`, `execute_check_code_changes()`, `execute_visual_editor_design_improvement()`
- **If changed, impacts**:
  - **Routes**: All `/interactions/*` endpoints delegate to this service
  - **Tools**: All tools returning `IslandResponse`
  - **Cross-repo**: VE `OpalChat.tsx` handles `OPAL_INTERACTION_ISLAND_CLICKED` events
- **Critical path**: Entity creation (interactive mode), VE save, flag brainstorming
- **Test file**: `tests/services/interaction_island/test_services.py`

---

### `src/services/interaction_island/routes.py`
- **Type**: Routes
- **Purpose**: 7 POST endpoints under `/interactions/` prefix for island action execution
- **Endpoints**: `/flag-variable`, `/flag-variation`, `/save-changes`, `/check-code-changes`, `/design-improvement`, `/entity-lifecycle-create`, `/entity-lifecycle-update`
- **If changed, impacts**:
  - **Cross-repo**: VE `OpalChat.tsx` sends POST requests to these endpoints when user confirms islands
  - **Island actions**: Route changes break frontend → backend communication
- **Critical path**: ALL interaction island flows
- **Test file**: `tests/services/interaction_island/test_routes.py`

---

### `src/services/context/service.py`
- **Type**: Service
- **Purpose**: `ContextService` — matches Opal URL against patterns, executes parallel API calls with dependency resolution, applies formatters
- **If changed, impacts**:
  - **Context route**: `routes.py` delegates all context resolution here
  - **Formatters**: `ExperimentDetailsFormatter`, `RuleDetailsFormatter`
  - **Processors**: `ExperimentDetailsProcessor`, `RuleDetailsProcessor`
  - **Downstream**: Opal Chat LLM receives context — broken = no context for AI responses
- **Critical path**: Context enrichment — every Opal Chat session
- **Test file**: `tests/services/context/test_service.py`

---

### `src/services/program_reporting/services.py`
- **Type**: Service
- **Purpose**: `ProgramReportingService` — fetches analytics data via Program Reporting API
- **Key functions**: `fetch_analytics()`
- **If changed, impacts**:
  - **Tools**: `exp_program_reporting_top_experiments`, `exp_program_reporting_underperforming_experiments`, `exp_program_reporting_win_rate`
- **Critical path**: Program reporting analytics
- **Test file**: `tests/services/program_reporting/test_services.py`

---

## Layer 4: Authentication (Cross-Cutting)

---

### `src/authentication/ingress/opti_id/auth.py`
- **Type**: Auth handler
- **Purpose**: `OptiIdAuthentication` — validates Okta JWT tokens, extracts claims (sub, uid, cid, iss, scp), stores in `ContextVars`
- **If changed, impacts**:
  - **ALL routes**: Global auth dependency in `main.py`
  - **ALL tools**: Auth data extracted here flows to every tool via `patch_tool_decorator`
  - **WebSocket**: `websocket_authentication.py` also uses OptiID validation
- **Critical path**: Authentication — service rejects all requests if broken
- **Test file**: `tests/authentication/ingress/test_opti_id_auth.py`

---

### `src/authentication/ingress/authentication.py`
- **Type**: Auth dispatcher
- **Purpose**: `Authentication` class — FastAPI dependency that routes to OptiID or OpalApiGW handler based on `AuthenticationMechanism` enum
- **If changed, impacts**:
  - **main.py**: Global dependency (`Depends(Authentication(AuthenticationMechanism.OPTIID))`)
  - **ALL routes**: Every request passes through this
- **Critical path**: Authentication
- **Test file**: `tests/authentication/ingress/test_auth_utils.py`

---

### `src/authentication/egress/auth_manager.py`
- **Type**: Auth manager
- **Purpose**: `EgressAuthManager` — selects authentication mechanism for outbound API calls (internal token, cookie, or OptiID token)
- **If changed, impacts**:
  - **ALL HTTP clients**: Auth injection for every outbound request
  - **Context service**: API calls use egress auth
  - **Experimentation service**: Result API calls
- **Critical path**: ALL external API calls
- **Test file**: Implicitly tested via client tests

---

## Layer 5: Key Tools (High-Traffic Entry Points)

---

### `src/tools/opensearch_query.py`
- **Type**: Tool (2 tools in 1 file)
- **Purpose**: `exp_get_schemas` (retrieve entity schemas) + `exp_execute_query` (run queries) — the primary data querying interface for Opal Chat
- **If changed, impacts**:
  - **Schema-first workflow**: `exp_get_schemas` MUST be called before `exp_execute_query`
  - **Result summary**: `exp_summarize_test_result` uses `OpenSearchQueryService` internally
  - **Program reporting**: Tools may call `exp_execute_query` to resolve project IDs
  - **Cross-repo**: Query results rendered in Opal Chat frontend
- **Critical path**: Entity querying — most common Opal Chat operation
- **Business rules**: `project_id` must be STRING (validator rejects UUIDs); template must be valid JSON; all integers converted to strings in response
- **Test file**: `tests/tools/test_opensearch_query.py`, `tests/tools/test_opensearch_query_date_filters.py`

---

### `src/tools/exp_manage_entity_lifecycle.py`
- **Type**: Tool
- **Purpose**: Create/update entities (flags, experiments, audiences, events, pages, campaigns, attributes, environments, variables, variable_definitions, variations)
- **If changed, impacts**:
  - **Interaction island**: Creates `IslandResponse` for interactive mode; `/interactions/entity-lifecycle-*` executes
  - **Template workflow**: MUST call `exp_get_entity_templates` first
  - **Cross-repo**: VE `OpalChat.tsx` handles island confirmation events
- **Critical path**: Entity creation/update
- **Business rules**: `variable_definition` and `variation` MUST use template mode; delete operation disabled; interactive vs headless via `execution_mode`
- **Test file**: `tests/tools/exp_manage_entity_lifecycle/`

---

### `src/tools/result_summary.py`
- **Type**: Tool
- **Purpose**: `exp_summarize_test_result` — fetches experiment/rule results enriched with metadata (variations, metrics, audiences, pages)
- **If changed, impacts**:
  - **OpenSearch service**: Queries entity metadata
  - **Experimentation service**: Fetches result API data
  - **Downstream**: Result analysis in Opal Chat
- **Critical path**: Result summarization
- **Business rules**: Auto-detects Web vs Custom/FX platform; experiment_id on FX tries `layer_experiment_id` first, falls back to `id`; integers converted to strings
- **Test file**: `tests/tools/test_result_summary.py`

---

### `src/tools/visual_editor/design_improvement_suggestions.py`
- **Type**: Tool
- **Purpose**: `exp_suggest_visual_editor_component_improvements` — expert CRO/UX analysis generating multiple design variation ideas
- **If changed, impacts**:
  - **Interaction island**: Returns `IslandResponse` → `/interactions/design-improvement` endpoint
  - **Cross-repo**: VE `OpalChat.tsx` handles `OPAL_INTERACTION_ISLAND_CLICKED` with `IMPROVEMENT_IDEA_DESCRIPTION` label
- **Critical path**: Design suggestions (VE context)
- **Test file**: `tests/tools/visual_editor/test_design_improvement_suggestions.py`

---

### `src/tools/sample_size_calculator.py`
- **Type**: Tool (self-contained)
- **Purpose**: `exp_calculate_sample_size` — statistical calculation for A/B test planning
- **If changed, impacts**: Self-contained — no downstream dependencies
- **Critical path**: Sample size calculation (isolated)
- **Test file**: `tests/tools/test_sample_size_calculator.py`

---

### `src/tools/pgm_reporting/` (3 tools)
- **Type**: Tools
- **Purpose**: `exp_program_reporting_top_experiments`, `exp_program_reporting_underperforming_experiments`, `exp_program_reporting_win_rate`
- **If changed, impacts**:
  - **Program reporting service**: All call `ProgramReportingService.fetch_analytics()`
  - **Auth**: All use `@inject_admin_account_ids` decorator
  - **Utils**: All use `pgm_reporting/utils.py` for date parsing, list normalization
- **Critical path**: Program reporting analytics
- **Test file**: `tests/services/program_reporting/test_services.py`

---

## Critical Path Summary

| Path | Key Files (in order of flow) |
|------|------------------------------|
| **WebSocket Bridge** | `OpalChat.tsx` → `websocket-bridge.ts` → `ws/{thread_id}` → `routes.py` → `manager.py` → `send_bridge_command()` → VE bridge tool → WebSocket → `server.ts` → `tools/*.ts` → DOM |
| **Tool Call** | Opal Chat → `@tool()` function → `patch_tool_decorator` (auth injection) → service layer → external API → response |
| **Context Enrichment** | Opal URL → `context/routes.py` → `service.py` → `constants.py` pattern match → parallel API calls → formatters → processors → LLM context |
| **Entity Creation (Interactive)** | Tool → `IslandResponse` → Opal Chat renders island → user clicks "Confirm" → `POST /interactions/entity-lifecycle-create` → `InteractionIslandService` → `ExpManageEntityLifecycleService` → TypeScript backend |
| **Entity Creation (Headless)** | Tool (headless mode) → `ExpManageEntityLifecycleService.manage_entity_lifecycle()` → TypeScript backend → success string |
| **Flag Brainstorming** | Tool → `IslandResponse` with variable/variation islands → user clicks "Create" → `POST /interactions/flag-variable` or `flag-variation` → `FlagsService` → Flags API |
| **Design Improvement** | Tool → `IslandResponse` → user clicks "Create Improvement Idea" → `POST /interactions/design-improvement` → `InteractionIslandService` |
| **Authentication** | Request → `ContextMiddleware` → `Authentication(OPTIID)` → `OptiIdAuthentication` → Okta JWT verify → `ContextVars` → egress auth for API calls |
| **OpenSearch Query** | `exp_get_schemas` → `OpenSearchQueryService` → TypeScript backend → schemas; then `exp_execute_query` → TypeScript backend → results (integers → strings) |

---

## Quick Blast Radius by Ticket Type

| Ticket mentions... | Check these files |
|--------------------|------------------|
| WebSocket / bridge / VE connection | `websocket_bridge/manager.py`, `routes.py`, `models.py`, `visual_editor_bridge/utils.py`, VE `websocket-bridge.ts` |
| Tool call / tool not working | `tools/__init__.py` (registration), `common/decorators.py` (patch_tool_decorator), specific tool file |
| Context / URL matching / no context | `context/constants.py` (URL patterns), `context/service.py`, `formatters/`, `processors/` |
| Entity create / update / lifecycle | `tools/exp_manage_entity_lifecycle.py`, `services/exp_manage_entity_lifecycle/`, `interaction_island/` |
| Flag / variable / variation brainstorm | `tools/flag_variable_brainstorm.py`, `flag_variation_brainstorm.py`, `services/flags/`, `interaction_island/` |
| Island / interaction / confirm | `interaction_island/dtos.py` (Island/IslandResponse), `routes.py`, `services.py` |
| OpenSearch / query / schema | `tools/opensearch_query.py`, `services/opensearch_query/`, TypeScript backend |
| Result / summarize | `tools/result_summary.py`, `services/experimentation/`, `services/opensearch_query/` |
| Auth / token / JWT / 401 | `authentication/ingress/opti_id/`, `authentication/egress/`, `context_vars.py` |
| Environment / config / startup crash | `env_config.py` |
| Design improvement / VE suggestions | `tools/visual_editor/design_improvement_suggestions.py`, `interaction_island/` |
| Program reporting / win rate / top | `tools/pgm_reporting/`, `services/program_reporting/` |
| SDK docs / FX search | `tools/fx_sdk_docs_search.py`, `services/fx_sdk_docs_search/` |
| Sample size / calculator | `tools/sample_size_calculator.py` (isolated) |
| Agent / agent directory | `services/agent_directory/`, `common/agent/builder.py` |
