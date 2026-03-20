# Feature Experimentation - Detailed Reference

**This file contains exhaustive API tables, configuration details, datafile schemas, and service internals. For core product knowledge, see SKILL.md.**

## Scheduling API (Full Reference)

### Base Endpoints
```
POST   /projects/{project_id}/flags/{flag_key}/schedules        -- Create schedule
GET    /projects/{project_id}/flags/{flag_key}/schedules        -- List schedules
GET    /projects/{project_id}/flags/{flag_key}/schedules/{id}   -- Get schedule
PATCH  /projects/{project_id}/flags/{flag_key}/schedules/{id}   -- Update schedule
DELETE /projects/{project_id}/flags/{flag_key}/schedules/{id}   -- Delete schedule
```

### Schedulable Actions

| Action | Subject Type | Value |
|---|---|---|
| Flag status change | flag | "on" or "off" |
| Rule status change | rule | "on" or "off" |
| Rule percentage change | rule | 0-10000 |
| Rule audience change | rule | audience_conditions array |

### Schedule Request Format

```json
{
  "environment": "production",
  "schedule": {
    "date": "2025-06-15",
    "time": "14:30",
    "time_zone": "America/New_York"
  },
  "actions": [
    {
      "subject": { "key": "my_flag", "type": "flag" },
      "changed_element": "status",
      "value": "on"
    }
  ]
}
```

### Schedule Status Lifecycle

```
PENDING -> IN_QUEUE -> COMPLETED | FAILED | PARTIALLY_FAILED
PENDING -> CANCELED (if deleted before execution)
PENDING -> FAILED_TO_QUEUE (Pub/Sub failure)
```

## Change Approvals API (Full Reference)

### Endpoints
```
POST   /projects/{project_id}/flags/{flag_key}/approval                    -- Create approval
GET    /projects/{project_id}/flags/{flag_key}/approval/{id}               -- Get approval
POST   /projects/{project_id}/flags/{flag_key}/approval/{id}/status        -- Accept/reject/withdraw
POST   /projects/{project_id}/flags/{flag_key}/approval/{id}/archive       -- Archive approval
GET    /projects/{project_id}/flags/approvals                              -- List approvals
```

### Approval Status Workflow

```
PENDING -> ACCEPTED (approval granted, schedule executes)
PENDING -> REJECTED (denied, reason required, max 350 chars)
PENDING -> WITHDRAWN (requester withdrew)
```

### Environment Approval Settings

```
GET/PATCH  /projects/{project_id}/environments/{env_id}/preferences       -- Environment settings
PATCH      /projects/{project_id}/environments/{env_id}/flags/{flag_id}/preferences  -- Per-flag override
```

Settings include: `require_approval_on_new_entities`, `default_preferences`, approver list, notification recipients.

## Holdouts API (Full Reference)

### Holdout Properties

- **key**: Unique per project+environment (max 64 chars)
- **name**: Display name (max 255 chars)
- **scope/scope_type**: Granularity (user-level vs session-level)
- **traffic_allocation**: 0-10000 (percentage in basis points)
- **status**: `draft`, `active`, `inactive`, `concluded`
- **audience_conditions**: JSON targeting with AND/OR logic
- **metrics**: Events to measure holdout impact

### Endpoints

```
GET    /projects/{project_id}/holdouts              -- List holdouts
POST   /projects/{project_id}/holdouts              -- Create holdout
GET    /projects/{project_id}/holdouts/{key}         -- Fetch holdout
PATCH  /projects/{project_id}/holdouts/{key}         -- Update holdout
DELETE /projects/{project_id}/holdouts/{key}         -- Delete holdout
```

## Mutual Exclusion Groups API

### Endpoints

```
GET    /projects/{project_id}/groups              -- List groups
POST   /projects/{project_id}/groups              -- Create group
PATCH  /projects/{project_id}/groups/{key}        -- Update group
DELETE /projects/{project_id}/groups/{key}        -- Delete group
```

### Key Rules
- No SDK changes required -- `Decide` and `Track` automatically evaluate exclusion groups
- All experiments in a group should start simultaneously
- Do not add/remove running experiments from a group
- Groups can be archived and unarchived

## Custom Fields API

### Endpoints

```
GET    /projects/{project_id}/custom_fields              -- List custom fields
POST   /projects/{project_id}/custom_fields              -- Create custom field
PATCH  /projects/{project_id}/custom_fields/{id}         -- Update custom field
```

Types: text, number, boolean, link, label. Feature-flagged via `fx_custom_fields`.

## Reports API

### Endpoints

```
GET    /projects/{project_id}/reports                        -- List reports
GET    /projects/{project_id}/reports/{key}                  -- Fetch report
DELETE /projects/{project_id}/reports/{key}                  -- Delete report
POST   /projects/{project_id}/reports/{key}/archived         -- Archive report
POST   /projects/{project_id}/reports/{key}/unarchived       -- Unarchive report
POST   /projects/{project_id}/reports/{key}/reset_results    -- Reset results
```

Reports contain metrics, confidence levels, outcomes, and days_running data.

## REST API (Full Endpoint Reference)

### Base URL
`https://api.optimizely.com`

### Authentication
```
Authorization: Bearer YOUR_API_TOKEN
```

### Flags
- `POST /flags/v1/projects/{project_id}/flags` -- Create
- `GET /flags/v1/projects/{project_id}/flags` -- List (filterable by `flag_status`)
- `GET /flags/v1/projects/{project_id}/flags/{flag_key}` -- Fetch
- `PATCH /flags/v1/projects/{project_id}/flags` -- Update (JSON Patch)
- `POST .../flags/archived` / `.../flags/unarchived` -- Archive/unarchive
- `POST .../flags/duplicate` -- Duplicate flag
- `DELETE .../flags/{flag_key}` -- Delete

### Variables
- `POST .../flags/{flag_key}/variable_definitions` -- Create
- `PATCH .../flags/{flag_key}/variable_definitions` -- Update
- `DELETE .../flags/{flag_key}/variable_definitions/{variable_key}` -- Delete

### Variations
- `POST .../flags/{flag_key}/variations` -- Create
- `PATCH .../flags/{flag_key}/variations` -- Update
- `DELETE .../flags/{flag_key}/variations/{variation_key}` -- Delete
- `POST .../flags/{flag_key}/variations/archived` / `.../unarchived`
- `POST .../flags/{flag_key}/brainstorm_variations` -- AI suggestions (Opal)

### Rulesets
- `GET .../rulesets/{environment_key}` -- Fetch
- `PATCH .../rulesets/{environment_key}` -- Update (JSON Patch: add/remove/replace)
- `POST .../rulesets/{environment_key}/enable` / `/disable`

### Rules
- `GET /flags/v1/projects/{project_id}/rules` -- List all rules
- `GET .../rules/{rule_id}` -- Get by ID
- `GET .../rules/by_experiment_id/{experiment_id}` -- Get by experiment ID

### Datafile
- `GET .../environments/{environment_key}/datafile` -- v1
- `GET .../environments/{environment_id}/datafile` -- v2

### PATCH Pattern

For `PATCH` requests: GET current object -> merge changes -> send PATCH with JSON Patch format. Supported operations: `add`, `remove`, `replace`, `move`, `copy`, `test`. Must disable a rule before removing it from a ruleset.

## Change History for FX (Full Reference)

**FX-specific entity types**: `flag`, `rule`, `ruleset`, `variation`, `variable`, `environment`, `permission`, `team`, `report`, `custom_field`

**UI URL patterns for FX entities:**

| Entity | URL |
|---|---|
| flag | `/v2/projects/{project_id}/flags/manage/{flag_key}` |
| rule | `/v2/projects/{project_id}/flags/manage/{flag_key}/rules/{env_key}/edit/{rule_key}` |
| ruleset | `/v2/projects/{project_id}/flags/manage/{flag_key}/rules/{env_key}` |
| variation | `/v2/projects/{project_id}/flags/manage/{flag_key}/variations` |
| variable | `/v2/projects/{project_id}/flags/manage/{flag_key}/variables/edit/{variable_key}` |
| environment | `/v2/projects/{project_id}/settings/implementation` |
| team | `/v2/accountsettings/teams` |

## Permission Service for FX (Full Reference)

### Entity Types with Permissions
- **flags**: Per-flag permissions (admin, publish, toggle, edit, view, none)
- **environments**: Per-environment permissions (restricted environments enforce stricter access)
- **audiences**: Context-dependent permissions

### Permission Actions

| Action | Required Level | Used For |
|---|---|---|
| read (READ) | view or higher | Read/view entity data |
| modify (MODIFY) | edit or higher | Change entity settings |
| toggle (TOGGLE) | edit or higher | Enable/disable flags/rules |
| publish (PUBLISH) | publish or higher | Publish changes |
| admin (ADMIN) | admin | Manage permissions |

### Key Business Rules

- Flag creator is auto-assigned **Admin** role
- Creating a flag requires access to at least one environment
- Regular environments: `FLAGS_MODIFY` sufficient for most operations
- Restricted environments: `FLAGS_TOGGLE` required for enable/disable
- Variation updates in restricted environments require `FLAGS_TOGGLE`
- Team-based permissions: teams can have per-entity permissions
- Default team role for environments: "view", others: "none"

### Scheduling Permissions

- `FLAGS_SCHEDULING_ACCESS`: Access scheduling features
- `FLAGS_MODIFY`: Modify/delete schedules
- `FLAGS_TOGGLE`: Turn flags on/off in schedules
- `FX_CHANGE_APPROVALS`: Create/manage approvals
- `FX_WAREHOUSE_NATIVE_EXPERIMENTATION`: Create rules without metrics
- `FX_CMAB`: Create/modify CMAB rules

## Datafile Build Service (DBS) - Full Reference

### How DBS Works

1. **Trigger**: Every write to the Flags service publishes a Pub/Sub message to `datafile-ingress-point` topic
2. **Message format**: `{ project_id, environment_id, type: "build"|"force_build"|"delete", dry_run, publisher: "flags"|"monolith" }`
3. **Ordering key**: `"{project_id}_{environment_id}"` ensures sequential processing per environment
4. **Build process**: Fetch data from Flags + Monolith concurrently -> merge -> validate JSON schema -> upload -> purge CDN cache -> notify Monolith

### DBS Data Sources

**From Flags Service** (`GET /projects/{project_id}/environments/{environment_id}/datafile_data`, HMAC auth):
- experiments, featureFlags, rollouts, groups, events, holdouts

**From Monolith** (`POST /api/v1/projects/{project_id}/environments/{environment_id}/datafile_data`, token auth):
- audiences, attributes, events, integrations, botFiltering, anonymizeIP, projectStatus, revision, subscriptionStatus, pciEnabled, region

### Datafile Structure (V4)

```json
{
  "version": "4",
  "projectId": "string",
  "accountId": "string",
  "revision": "string",
  "region": "string",
  "audiences": [{ "id": "string", "name": "string", "conditions": "string|object" }],
  "typedAudiences": [{ "id": "string", "name": "string", "conditions": "object" }],
  "attributes": [{ "id": "string", "key": "string" }],
  "experiments": [{
    "id": "string", "key": "string", "status": "string", "layerId": "string",
    "audienceIds": ["string"], "audienceConditions": ["string"],
    "variations": [{ "id": "string", "key": "string", "featureEnabled": "boolean", "variables": [{ "id": "string", "value": "string" }] }],
    "trafficAllocation": [{ "entityId": "string", "endOfRange": "int" }],
    "forcedVariations": { "userId": "variationId" },
    "cmab": { "trafficAllocation": "int", "attributeIds": ["string"] }
  }],
  "featureFlags": [{
    "id": "string", "key": "string", "rolloutId": "string", "experimentIds": ["string"],
    "variables": [{ "id": "string", "key": "string", "type": "string", "defaultValue": "string" }]
  }],
  "rollouts": [{ "id": "string", "experiments": ["Experiment"] }],
  "groups": [{ "id": "string", "policy": "string", "trafficAllocation": ["..."], "experiments": ["..."] }],
  "events": [{ "id": "string", "key": "string", "experimentIds": ["string"] }],
  "holdouts": [{
    "id": "string", "key": "string", "status": "string",
    "audienceIds": ["string"], "audienceConditions": ["string"],
    "variations": ["..."], "trafficAllocation": ["..."],
    "includedFlags": ["string"], "excludedFlags": ["string"]
  }],
  "botFiltering": "boolean",
  "anonymizeIP": "boolean",
  "integrations": [{ "key": "string", "publicKey": "string", "host": "string" }]
}
```

### Audience Condition Match Operators

`exact`, `substring`, `lt`, `gt`, `le`, `ge`, `exists`, `semver_eq`, `semver_lt`, `semver_gt`, `semver_le`, `semver_ge`, `qualified`

### DBS Build Optimizations

- **Skip build**: If recent build found and no changes detected, skip upload
- **Rate limiting**: If >30 requests in 60s window without changes, skip
- **Deferred publishing**: Batches requests (idle timeout 10s, active timeout 60s, max 100 environments)
- **Force build**: Ignores cache, always uploads and increments revision

### DBS Upload Destinations

| Destination | Path Pattern | Cache |
|---|---|---|
| S3 (public) | `/public/{account_id}/artifacts/{project_id}_DATAFILE_V{version}/{revision}_{hash}` | max-age=120 |
| S3 (PCI) | Same pattern, encrypted bucket | max-age=120 |
| S3 (private) | Separate bucket, STS role | N/A |
| Cloudflare KV | datafile-kv namespace | Per policy |
| Cloudflare CDN | Cache purge on update | Edge cached |

### DBS Special Cases

- **Archived project**: Datafile injected with comment: `// This Optimizely project has been archived`
- **Dry run mode**: Uploads to `/dbs-dry-run` prefix, no revision increment, no Monolith notification
- **Dummy audience**: ID `$opt_dummy_audience` injected when datafile has no audiences (SDK compatibility)
- **Dead letter queue**: After 10 failed delivery attempts, messages go to `dead-letter-datafile-ingress-point`

## Datafile Access Tokens (DAT) - Full Reference

### Architecture

```
SDK -> Authorization Worker (Cloudflare) -> Validates token hash -> Returns private datafile
UI  -> REST API (K8s) -> API CRUD Worker (Cloudflare) -> Cloudflare KV (token whitelist)
```

### REST API Endpoints

```
POST   /projects/{projectId}/datafiles/{datafileId}/datafile-access-tokens    -- Create token (201)
GET    /projects/{projectId}/datafiles/{datafileId}/datafile-access-tokens    -- List tokens (200)
DELETE /projects/{projectId}/datafiles/{datafileId}/datafile-access-tokens/{accessTokenId}  -- Revoke (204)
```

### Token Format

**Plaintext** (returned once at creation, never stored):
```
base64("{version}:{projectId}:{accessTokenId}:{randomUuid}")
Example decoded: 1:99999:dfaab973-0301-49f3-899a-cf94c9cf7610:fa4f6490-90ab-4459-9201-091977abcd93
```

**Stored in KV** (key: `{projectId}:{datafileId}:{accessTokenId}`):
```json
{ "accessTokenId": "uuid-v4", "name": "string", "datafileId": "string", "hash": "sha256-hex", "lastFourChars": "xxxx" }
```

### Token Permissions

- `datafile_access_tokens.read`: Required for listing tokens
- `datafile_access_tokens.modify`: Required for creating and revoking tokens

### SDK Authorization Flow

1. SDK sends `GET /datafiles/auth/{datafileId}.json` with `Authorization: Bearer {plaintext}`
2. Worker decodes plaintext, extracts version/projectId/accessTokenId
3. Computes SHA256 hash of plaintext
4. Looks up KV entry: `{projectId}:{datafileId}:{accessTokenId}`
5. Verifies hash matches and datafileId matches
6. Returns datafile JSON (200) or 403 if validation fails

### Token API Business Rules

- Token `name` is required and non-empty
- `accessTokenId` must be valid UUID v4 for DELETE
- List pagination: `limit` 10-100 (default 25), cursor-based
- DELETE is idempotent (returns 204 even if token doesn't exist)
- Plaintext is shown ONLY at creation time, never retrievable again
- List response shows only `last_four_chars` (not full token)

### Token API Service URLs

| Environment | URL |
|---|---|
| Production | `https://datafile-tokens.optimizely.com` |
| RC | `https://prep.datafile-tokens.optimizely.com` |
| Auth Worker (Prod) | `https://config.optimizely.com/datafiles/auth/` |

## Changelog Elasticsearch (Search Indexing) - Full Reference

### Architecture

```
Monolith -> GCP Pub/Sub ("changelog") -> GCP Cloud Function (SNS bridge) -> AWS SNS -> AWS SQS -> AWS Lambda -> Elasticsearch 6.8
```

### Indexed Entity Types

| Entity Type | Elasticsearch Index | Source |
|---|---|---|
| LayerExperiment / experiment | experiment | FrontDoor API |
| Layer / campaign | campaign | FrontDoor API |
| Audience / audience | audience | FrontDoor API |
| FeatureFlag / feature | feature | FrontDoor API |
| Plugin / extension | extension | FrontDoor API |
| ExperimentSection / section | experimentsection | FrontDoor API |
| Experience (personalization) | experience | FrontDoor API |
| flag | flag | Inline snapshot |
| rule | rule | Inline snapshot |

**Skipped entity types** (not indexed): attribute, section (standalone), variation, group, ruleset, environment

### Changelog Message Format

```json
{
  "entity_type": "LayerExperiment",
  "entity_id": 1225170015,
  "change_type": "create|update|delete|delete_by_query",
  "account_id": 710050122,
  "project_id": 741260028,
  "update_time": "2019-02-07T01:07:14.322997"
}
```

### Key Business Rules

- Flags/rules include full snapshot in message (no FrontDoor API call needed)
- Non-flags entities: snapshot stripped by Cloud Function (SNS 256KB limit), Lambda fetches from FrontDoor API
- Non-personalization campaigns/layers are filtered out (only personalization indexed)
- Personalization experiments stored in "experience" index, trigger campaign audience_details reindex
- `delete_by_query` removes all docs for entity_type + project_id
- 404 from FrontDoor API = non-recoverable (skip), 5xx = recoverable (retry via SQS)
- Cloud Function has `STOP_WORK` env var as emergency stop

### Elasticsearch Service URLs

| Environment | URL |
|---|---|
| Dev | `https://es-changelog-dev.appbe.optimizely.com` |
| RC | `https://es-changelog-rc.appbe.optimizely.com` |
| Production | `https://es-changelog-prod.appbe.optimizely.com` |

## Detailed Test Scenarios

### Datafile Build Service
- Verify datafile rebuilds on flag/rule changes (Pub/Sub trigger)
- Verify V4 datafile schema validation (experiments, featureFlags, rollouts, holdouts)
- Test force_build bypasses cache check
- Test dry_run mode (uploads to dbs-dry-run prefix, no revision increment)
- Verify skip build pattern (no changes = no upload)
- Verify rate limiting (>30 requests/60s deferred)
- Verify Cloudflare CDN cache purge after upload
- Test archived project datafile comment injection
- Verify dummy audience injection when no audiences exist
- Test concurrent data fetch from Flags + Monolith services
- Verify dead letter queue after 10 failed delivery attempts

### Datafile Access Tokens
- Create token and verify plaintext format (base64 of `1:{projectId}:{uuid}:{uuid}`)
- Verify plaintext shown only at creation (not retrievable later)
- List tokens shows only last_four_chars (not full secret)
- Delete token and verify immediate SDK rejection (403)
- Test SDK auth flow: Bearer token -> hash validation -> datafile returned
- Test idempotent delete (204 even if token doesn't exist)
- Test pagination (limit 10-100, cursor-based)
- Test permission enforcement (read vs modify)
- Test invalid UUID format for accessTokenId -> 422
- Test missing/empty token name -> 400

### Search Indexing (Elasticsearch)
- Verify entity changes indexed in Elasticsearch (create/update/delete)
- Verify flag/rule changes include full snapshot (no FrontDoor call)
- Verify non-personalization campaigns filtered out
- Verify personalization experiments indexed in "experience" index
- Test delete_by_query removes all docs for project
- Verify skipped entity types (attribute, variation, group, ruleset) not indexed
- Test FrontDoor API 404 handling (skip, no retry)
- Test FrontDoor API 5xx handling (retry via SQS)

## Reference Links

- **Documentation source**: `fx-docs` repository at `docs/` directory
- **Flags service repo**: `optimizely/flags`
- **Scheduling service repo**: `optimizely/flags-scheduling`
- **Permission service repo**: `optimizely/permission-service`
- **Change History repo**: `optimizely/change-history`
- **Datafile Build Service repo**: `optimizely/datafile-build-service`
- **Datafile Access Tokens repo**: `optimizely/datafile-access-tokens`
- **Changelog Elasticsearch repo**: `optimizely/appx-changelog-elasticsearch`
- **Live developer docs**: https://docs.developers.optimizely.com/feature-experimentation
- **API reference**: https://docs.developers.optimizely.com/feature-experimentation/reference
- **Application URL**: https://app.optimizely.com
