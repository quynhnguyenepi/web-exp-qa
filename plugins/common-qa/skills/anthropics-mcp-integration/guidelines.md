# MCP Integration Guidelines

## Server Type Selection Criteria

Choose the appropriate MCP server type based on your use case:

### When to Use stdio

- You are running a **local** MCP server as a child process
- The server is installed via npm, pip, or compiled binary
- No external network connection is required
- You need direct process control (start/stop/restart)
- Examples: filesystem access, local databases, custom CLI tools

### When to Use SSE (Server-Sent Events)

- The MCP server is **hosted remotely** by a third-party service
- The service uses **OAuth** for authentication
- You want zero local installation (cloud-hosted)
- The server provides a dedicated SSE endpoint (e.g., `https://mcp.asana.com/sse`)
- Examples: Asana, GitHub, Sentry official MCP servers

### When to Use HTTP

- The MCP server exposes a **REST API** endpoint
- Authentication is handled via **static tokens** or API keys
- Interactions are stateless request/response pairs
- You need custom headers for each request
- Examples: internal API backends, token-gated services

### When to Use WebSocket (ws/wss)

- You need **real-time bidirectional** communication
- The server pushes data to the client without polling
- Low-latency or streaming data is required
- The connection must remain persistent across multiple tool calls
- Examples: live monitoring dashboards, real-time collaboration tools

## Configuration Format Rules

1. **Valid JSON only** -- `.mcp.json` must be parseable JSON. Trailing commas and comments are not allowed.
2. **Server names** -- Use lowercase kebab-case for server keys (e.g., `"my-database"`, not `"MyDatabase"`).
3. **stdio servers** -- Must include `"command"` (string) and optionally `"args"` (array of strings) and `"env"` (object).
4. **Remote servers** -- Must include `"type"` (`"sse"`, `"http"`, or `"ws"`) and `"url"` (string). Headers are optional.
5. **Environment variables** -- Use `${VAR_NAME}` syntax. Never hardcode secrets directly in configuration files.
6. **Paths** -- Always use `${CLAUDE_PLUGIN_ROOT}` for file paths within the plugin directory. Never use absolute paths.
7. **Single root object** -- `.mcp.json` must be a single JSON object where each key is a server name.

## Security Best Practices

### Never Hardcode Tokens

```json
// BAD -- token exposed in config
{
  "headers": { "Authorization": "Bearer sk-abc123..." }
}

// GOOD -- token from environment variable
{
  "headers": { "Authorization": "Bearer ${API_TOKEN}" }
}
```

### Always Use HTTPS/WSS

- Remote server URLs must use `https://` or `wss://` protocols.
- Never use `http://` or `ws://` in production configurations.
- Exception: `localhost` URLs during local development only.

### Principle of Least Privilege

- Pre-allow only the specific MCP tools needed by each command.
- Avoid wildcard tool permissions (`mcp__*`) unless absolutely necessary.
- Review tool permissions during code review.

### Credential Storage

- Document all required environment variables in the plugin README.
- Use `.env` files for local development (ensure `.env` is in `.gitignore`).
- Never commit `.mcp.json` files that contain real credentials.

## Testing Checklist

Before publishing or sharing an MCP integration, verify:

- [ ] `.mcp.json` is valid JSON (no syntax errors, no trailing commas)
- [ ] All server URLs are correct and reachable
- [ ] Required environment variables are documented in README
- [ ] Servers appear in `/mcp` command output
- [ ] Each tool can be called successfully at least once
- [ ] Authentication flow completes without errors (OAuth or token)
- [ ] Error cases are handled gracefully (server down, bad auth, rate limits)
- [ ] HTTPS/WSS is used for all remote connections
- [ ] No hardcoded tokens or secrets in configuration
- [ ] `${CLAUDE_PLUGIN_ROOT}` is used for all internal paths
- [ ] Tool names match exactly in `allowed-tools` frontmatter

## Port Management

When running local MCP servers that bind to ports:

1. **Avoid port conflicts** -- Do not hardcode common ports (3000, 8080, 5432). Use configurable ports via environment variables.
2. **Document default ports** -- If your server uses a default port, document it clearly.
3. **Check availability** -- Before starting a server, verify the port is not already in use.
4. **Cleanup on exit** -- Ensure the server process releases the port when Claude Code exits. stdio servers handle this automatically.
5. **Multiple servers** -- When running multiple MCP servers, assign distinct ports to each. Use a port range convention (e.g., 9100-9199 for MCP servers).

---

# Boilerplate (moved from SKILL.md for cost optimization)

## Progress Tracking

**CRITICAL**: At the start of execution, create a TodoWrite list so the user can see what the agent is doing at all times.

**Initial todo list (create immediately when skill is invoked):**

```
TodoWrite([
  { content: "Verify prerequisites and determine MCP server type", status: "in_progress", activeForm: "Verifying prerequisites" },
  { content: "Configure MCP server in .mcp.json", status: "pending", activeForm: "Configuring MCP server" },
  { content: "Set up authentication", status: "pending", activeForm: "Setting up authentication" },
  { content: "Test server connectivity", status: "pending", activeForm: "Testing connectivity" },
  { content: "Document MCP integration", status: "pending", activeForm: "Documenting integration" }
])
```

**Update rules:**
- Mark current step as `in_progress` when starting it
- Mark step as `completed` immediately when finished (do not batch)
- Only ONE step should be `in_progress` at any time


## Error Handling

### Connection Failures

Handle MCP server unavailability:
- Provide fallback behavior in commands
- Inform user of connection issues
- Check server URL and configuration

### Tool Call Errors

Handle failed MCP operations:
- Validate inputs before calling MCP tools
- Provide clear error messages
- Check rate limiting and quotas

### Configuration Errors

Validate MCP configuration:
- Test server connectivity during development
- Validate JSON syntax
- Check required environment variables


## Self-Correction

When user requests adjustments:

1. **"Use a different server type"** --> Reconfigure with the correct type (stdio/SSE/HTTP/WS)
2. **"Switch from OAuth to token auth"** --> Update configuration with token headers
3. **"Add another MCP server"** --> Append new server entry to existing .mcp.json
4. **"Remove a server"** --> Remove the server entry from .mcp.json
5. **"The server URL is wrong"** --> Update URL and re-test connection
6. **"Use environment variables instead"** --> Replace hardcoded values with ${ENV_VAR} syntax
7. **"The server is not connecting"** --> Debug with `claude --debug`, check URL, auth, network


## Notes

### Reference Files

For detailed information, consult:

- **`references/server-types.md`** - Deep dive on each server type
- **`references/authentication.md`** - Authentication patterns and OAuth
- **`references/tool-usage.md`** - Using MCP tools in commands and agents

### Example Configurations

Working examples in `examples/`:

- **`stdio-server.json`** - Local stdio MCP server
- **`sse-server.json`** - Hosted SSE server with OAuth
- **`http-server.json`** - REST API with token auth

### External Resources

- **Official MCP Docs**: https://modelcontextprotocol.io/
- **Claude Code MCP Docs**: https://docs.claude.com/en/docs/claude-code/mcp
- **MCP SDK**: @modelcontextprotocol/sdk
- **Testing**: Use `claude --debug` and `/mcp` command

