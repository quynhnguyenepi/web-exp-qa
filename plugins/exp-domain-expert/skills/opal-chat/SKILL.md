---
description: Product domain knowledge for Optimizely Opal Chat (AI Assistant) and Idea Builder. Use when answering questions about Opal Chat features, chat history, brainstorming, summarize results, review experiment, test ideas, visual editor AI, Opal backend tools, OpenSearch query engine, entity lifecycle management, program reporting, or Idea Builder. Helps QA engineers write tests with accurate product understanding.
---

## Dependencies

- **MCP Servers:** None required (Opal knowledge is static; MCP tools like `exp_get_schemas` / `exp_execute_query` are used by Opal itself, not by this skill)

### Source Repositories
- **Documentation repo:** `opal-docs` repository at `docs/` directory
- **Dev repos:**
  - `opal-tools` — Opal backend (Python/FastAPI, LLM agent, chat API, tool definitions, WebSocket for VE)
  - `idea-builder` — AI idea generation service (Python/FastAPI + Spanner, CRUD for ideas, file upload)
  - `opal-chat-e2e-test` — E2E test suite (Playwright + TypeScript)

## Role

You are an Optimizely Opal Chat domain expert. You have deep knowledge of the Opal AI Assistant product, its features, backend architecture, tool system, the Idea Builder service, and how they integrate across the Optimizely platform.

**Full reference:** See reference.md for complete tool definitions, API endpoints, island response formats, Idea Builder data model, and detailed test scenarios.

## Product Overview

Opal is Optimizely's AI-powered assistant embedded in the Experimentation platform. It provides conversational AI for experimentation workflows: brainstorming variations, summarizing results, reviewing experiments, generating test ideas, and producing copy for visual editor changes. Accessible from any page via a floating chat button. Supports context-aware interactions based on current page.

## Core Features

### Chat Interface
- Open via "Ask Opal" button (test ID: `optibot-toggle`)
- Chat input: contenteditable div; responses in `.opal-chat-wrapper`
- Progress dots loader (`.oui-progress-dots`) during processing
- Each response has **Copy** and **Regenerate** buttons
- Dock to side available; close via copilot sidebar (`common-copilot-sidebar`)
- Context-aware: understands current page

### Chat History
- Access via "Toggle Sidebar" button; searchable list grouped by date
- Per-thread "Thread options" menu with "Delete thread" (confirmation: "Yes, Delete")
- "New Chat" button; history persists across login/logout sessions
- Navigating to different page auto-creates new contextual thread
- API: `GET /api/v1/threads`

### Brainstorm Variations/Variables (FX Flags)
- Available on Variations/Variables tab of Feature Flag pages
- Click "Brainstorm" button (test ID: `brainstorm-button`, disabled after click)
- Opal generates suggestions in "island" UI with plus icon for selection
- Selecting populates variation/variable creation form
- Close Opal -> edit pre-filled form -> save

### Summarize Results
- Available on Results page across Web, Edge, and FX projects
- For campaigns: button disabled until specific experiment selected
- Generates structured summary: Summary, Variations, Primary Metric Analysis, Suggestions, Next Steps
- Supported: Web (A/B, MAB, MVT, Campaign), Edge (A/B), FX (A/B, MAB rules)

### Review Experiment
- Available on Summary tab (Web/Edge) via "Review Experiment" button
- Also triggered via Pre-launch Review flow (Start/Publish Experiment -> Review Before)
- Supported statuses: Not Started, Running, Paused

### Get Test Ideas
- Available from experiment list page (Web/Edge/FX)
- Web/Edge: test ID `get-test-ideas-using-opal-button`; FX: from Flags list page
- Users can provide URL for targeted analysis

### Generate Copy (Visual Editor)
- Flow: open variation -> classic editor -> create element change -> edit selector -> "Generate Copy"
- API: `POST /opti-ai/content-suggestions`
- Actions: "Use This Copy" or "Create New" variation

### Summarize Variations
- Available on Variations tab (Web/Edge) via test ID `summarize-variations-button`
- API: `POST /opti-ai/variation-summary`
- Per-variation actions: Edit/Regenerate/Disable/Generate Description

### Visual Editor AI
- Tools: apply_change, element_glob, element_grep, element_read, element_tree, get_change_schema, get_selector, list_pending_changes, revert_change, validate_change

## Architecture

### Backend (opal-tools)
- Python FastAPI at `opal-backend.optimizely.com/opal-backend`
- Source: `optimizely/opal-tools`
- LLM agent via `llm-framework` package; Auth: OptiID (Okta JWT)
- WebSocket: `/ws/{thread_id}` for Visual Editor communication

### Key APIs
- Chat: `POST /api/v2/customer`
- Threads: `GET /api/v1/threads`
- Variation summary: `POST {BASE_URL}/opti-ai/variation-summary`
- Content suggestions: `POST {BASE_URL}/opti-ai/content-suggestions`

## Idea Builder

AI-powered experimentation idea generator. Backend: Python 3.12 FastAPI + Spanner. Frontend: React 17 + TypeScript + Zustand. Module Federation remote consumed by monolith.

### Key UI Test Selectors
```
data-testid="brainstorm-idea"       // Main layout container
data-testid="idea-form"             // Form wrapper
data-testid="saved-ideas"           // Saved ideas panel
data-testid="generated-ideas"       // Generated ideas panel
```

### Business Rules
- Ideas listed newest first; search case-insensitive on title + target_url
- Default limit: 100, max: 1000; file uploads max 5 MB
- Auth: OptiID JWT with headers: `x-instance-id`, `x-org-id`, `x-opal-instance-id`, `x-product-sku: EXP`

## UI Components (Key Locators)

| Component | Locator |
|---|---|
| Ask Opal Button | `[data-test-section="optibot-toggle"]` |
| Chat Input | `div[contenteditable="true"]` |
| Chat Wrapper | `.opal-chat-wrapper` |
| Loader | `.oui-progress-dots` |
| Brainstorm Button | `[data-test-section="brainstorm-button"]` |
| Summarize Results | Button "Summarize Results" |
| Review Experiment | Button "Review Experiment" |
| Summarize Variations | `[data-test-section="summarize-variations-button"]` |
| Get Test Ideas (Web) | `[data-test-section="get-test-ideas-using-opal-button"]` |
| Generate Copy | Button "Generate Copy" |

## Key User Flows

### Ask Opal
Click "Ask Opal" -> type question -> Enter -> wait for dots to disappear -> verify answer with Copy/Regenerate

### Brainstorm (FX)
Flag > Variables/Variations tab -> "Brainstorm" -> wait -> type hypothesis -> click plus on suggestion -> close Opal -> edit form -> save

### Summarize Results
Results page -> (campaigns: select experiment first) -> "Summarize Results" -> verify structured summary

### Generate Test Ideas (Idea Builder)
Idea Builder -> select Target By (URL/Saved Page/Screenshot) -> enter Goal -> "Get Test Ideas" -> view ideas

## Key Business Rules

- **Authentication required:** OptiID (Okta) credentials
- **Context awareness:** Responses vary based on current page URL
- **Chat persistence:** Threads persist across sessions
- **Thread auto-creation:** New page = new thread
- **Campaign summarization:** Button disabled until experiment selected
- **Brainstorm mode lock:** Button disabled after activation
- **ID precision:** All entity IDs must be STRING format (prevent JS precision loss)
- **OpenSearch prerequisite:** Must call exp_get_schemas before exp_execute_query
- **Entity lifecycle prerequisite:** Must call exp_get_entity_templates before exp_manage_entity_lifecycle

## Common Test Scenarios

- Verify Opal Chat opens and responds to questions
- Verify chat history persists after logout/login
- Verify multiple chat threads can be created and managed
- Verify brainstorm mode generates and populates forms
- Verify results summarization for all experiment types
- Verify experiment review for Draft, Running, Paused
- Verify test ideas generation for Web, Edge, FX
- Verify copy generation/regeneration in visual editor
- Verify variation summarization with all description actions
- Verify no error messages in Opal responses
