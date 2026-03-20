# MCP Integration -- Test Cases

## TC-001: stdio Server Setup

**Description:** Configure and connect a local stdio MCP server.

**Input:**
- User says: "Add a filesystem MCP server using npx"
- No existing `.mcp.json` file

**Expected:**
- `.mcp.json` created at plugin root with valid JSON
- Server entry uses `"command": "npx"` with appropriate `"args"`
- `${CLAUDE_PLUGIN_ROOT}` used for any path references
- Server appears in `/mcp` output
- File tools are callable

**Pass Criteria:**
- `.mcp.json` is valid JSON
- Server key uses kebab-case
- Command and args fields are present
- No `"type"` field (stdio is the default)

---

## TC-002: SSE Server with OAuth

**Description:** Configure an SSE MCP server that uses OAuth authentication.

**Input:**
- User says: "Connect to Asana MCP server"
- Server URL: `https://mcp.asana.com/sse`

**Expected:**
- `.mcp.json` entry with `"type": "sse"` and correct URL
- No hardcoded tokens in configuration
- OAuth flow initiates on first tool use
- User is prompted to authenticate in browser
- Tools from the SSE server are available after auth

**Pass Criteria:**
- `"type"` is `"sse"`
- URL uses `https://`
- No `"headers"` with hardcoded tokens
- Configuration is valid JSON

---

## TC-003: HTTP Server with Token Authentication

**Description:** Configure an HTTP MCP server with token-based auth using environment variables.

**Input:**
- User says: "Add an HTTP MCP server at https://api.example.com/mcp with a bearer token"
- Token should come from `$API_TOKEN` environment variable

**Expected:**
- `.mcp.json` entry with `"type": "http"`, correct URL, and headers
- Authorization header uses `${API_TOKEN}` syntax
- No hardcoded token values
- README or documentation mentions the required env var

**Pass Criteria:**
- `"type"` is `"http"`
- `"url"` uses `https://`
- `"headers"` contains `"Authorization": "Bearer ${API_TOKEN}"`
- Token is NOT hardcoded

---

## TC-004: Missing Environment Variables

**Description:** Handle the case where required environment variables are not set.

**Input:**
- `.mcp.json` references `${DB_URL}` and `${API_KEY}`
- Neither environment variable is set in the user's shell

**Expected:**
- Clear error message identifying which variables are missing
- Guidance on how to set the variables (export command)
- Server does not silently fail with empty values
- Suggestion to add variables to shell profile or `.env` file

**Pass Criteria:**
- Agent identifies the missing variables by name
- Provides `export VAR_NAME=value` example
- Does not proceed with empty/undefined values
- Documents the variables in README if not already present

---

## TC-005: Invalid JSON Configuration

**Description:** Detect and fix invalid JSON in `.mcp.json`.

**Input:**
- User has an existing `.mcp.json` with syntax errors (trailing comma, missing quotes, unescaped characters)

**Expected:**
- Agent detects the JSON syntax error
- Provides specific error location (line/character if possible)
- Fixes the JSON and validates the corrected version
- Does not overwrite unrelated configuration

**Pass Criteria:**
- Invalid JSON is identified before attempting to use it
- Fix produces valid JSON (parseable by `JSON.parse`)
- Original server entries are preserved
- Agent explains what was wrong

---

## TC-006: Server Not Connecting

**Description:** Debug and resolve MCP server connection failures.

**Input:**
- User says: "My MCP server is not connecting"
- `.mcp.json` exists with a valid entry
- Server URL is unreachable or process fails to start

**Expected:**
- Agent runs diagnostic steps (`claude --debug`, check URL, verify process)
- Identifies root cause (wrong URL, server not running, auth failure, network issue)
- Provides specific fix for the identified issue
- Verifies fix by re-testing connection

**Pass Criteria:**
- Agent suggests `claude --debug` for logs
- Checks server URL accessibility
- Verifies authentication configuration
- Provides actionable fix (not just "check your config")

---

## TC-007: Multi-Server Setup

**Description:** Configure multiple MCP servers in a single `.mcp.json`.

**Input:**
- User says: "Set up both GitHub and Jira MCP servers"
- GitHub: SSE at `https://mcp.github.com/sse`
- Jira: SSE at `https://mcp.jira.com/sse`

**Expected:**
- Single `.mcp.json` with both server entries
- Each server has a distinct key name
- Both servers appear in `/mcp` output
- Tools from both servers are available
- `allowed-tools` in commands reference correct prefixed names

**Pass Criteria:**
- `.mcp.json` contains exactly two server entries
- Both entries have `"type": "sse"` and valid URLs
- Server keys are distinct and descriptive (e.g., `"github"`, `"jira"`)
- JSON is valid with both entries

---

## TC-008: WebSocket Server Setup

**Description:** Configure a WebSocket MCP server for real-time communication.

**Input:**
- User says: "Add a WebSocket MCP server at wss://mcp.example.com/ws with token auth"
- Token from `$WS_TOKEN` environment variable

**Expected:**
- `.mcp.json` entry with `"type": "ws"` and `wss://` URL
- Headers include Authorization with `${WS_TOKEN}`
- Connection uses secure WebSocket (wss, not ws)
- Real-time tools are available after connection

**Pass Criteria:**
- `"type"` is `"ws"`
- URL uses `wss://` protocol (not `ws://`)
- Token uses environment variable syntax `${WS_TOKEN}`
- Configuration is valid JSON
- No hardcoded credentials
