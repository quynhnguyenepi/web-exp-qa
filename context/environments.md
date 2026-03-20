# Environments — Web Experimentation

## Optimizely App URLs

| Environment | URL | Mo ta |
|-------------|-----|-------|
| **Inte** | https://app.optimizely.com (inte instance) | Integration testing |
| **Prep** | https://app.optimizely.com (prep instance) | Pre-production |
| **Prod** | https://app.optimizely.com | Production |

> Lien he lead QA de co exact URLs va credentials cho tung environment.

---

## Visual Editor URLs

VE duoc load trong iframe khi click variation tren Monolith:

```
Pattern: {monolith-url}/v2/projects/{projectId}/experiments/{experimentId}/variations/{variationId}
```

VE tu dong nhan OAuth token qua URL query params khi duoc load.

---

## Test Sites

| Site | URL | Mo ta |
|------|-----|-------|
| Commerce Demo | https://quynhnguyenepi.github.io/ai-variation-builder-opti/Index.html | Site co snippet Optimizely inject san |

---

## API Endpoints

| API | Base URL | Mo ta |
|-----|----------|-------|
| Frontdoor API | `https://api.optimizely.com` | VE doc/ghi experiment data |
| Monolith API | `https://api.optimizely.com/v1` | Events, views, projects |

### Key Endpoints (VE su dung)
```
GET  /v2/experiments/{id}              <- Fetch experiment data
PUT  /v2/experiments/{id}              <- Save A/B, MAB, Campaign
PUT  /v2/experiments/sections/{id}     <- Save MVT (KHAC ENDPOINT)
GET  /api/v1/projects/{id}/events      <- Fetch events
POST /api/v1/projects/{id}/events      <- Create event
GET  /api/v1/views                     <- Fetch pages
```

---

## Deployment Pipeline

```
Feature Branch -> PR -> Review -> Merge to main
                    -> CI/CD (GitHub Actions: .github/workflows/pr-pipeline.yaml)
                    -> Deploy to inte
                    -> QA sign-off
                    -> Deploy to prep
                    -> Deploy to prod
```
