# Web Experimentation QA

QA workspace cho Web Experimentation lane — Visual Editor + Monolith.

## Setup cho nguoi moi

### Buoc 1: Clone repo nay
```bash
git clone https://github.com/episerver/web-exp-qa
cd web-exp-qa
```

### Buoc 2: Clone source repos (de doc source code)
```bash
# VE source code (de doc khi can trace implementation)
git clone https://github.com/optimizely/visual-editor

# Monolith source code (optional — neu can doc code monolith)
# git clone https://github.com/optimizely/optimizely
```

### Buoc 3: Cai dat MCP servers
```bash
# Copy .mcp.json va dien credentials cua ban vao
cp .mcp.json.example .mcp.json
# Sua .mcp.json voi tokens cua ban (xem context/repos.md)
```

### Buoc 4: Mo Claude Code
```bash
# Mo trong web-exp-qa/ -> Claude doc CLAUDE.md nay
claude

# Hoac mo trong visual-editor/ -> Claude doc CLAUDE.md cua VE
cd ../visual-editor && claude
```

## Cau truc repo

```
web-exp-qa/
├── CLAUDE.md                    <- Claude Code entry point (doc cai nay dau tien)
├── .mcp.json.example            <- MCP config template (copy thanh .mcp.json)
├── README.md                    <- File nay
│
├── context/                     <- Architecture context tu 3 source repos
│   ├── repos.md                 <- Clone guide, links, branch convention
│   ├── ve-CLAUDE.md             <- VE architecture (sync tu visual-editor)
│   ├── monolith-CLAUDE.md       <- Monolith architecture
│   ├── skills-CLAUDE.md         <- Common skills context
│   ├── cross-repo-flows.md      <- VE change -> verify gi o Monolith
│   └── environments.md          <- inte/prep/prod URLs
│
├── docs/
│   ├── CROSS_REPO_IMPACT_INDEX.md  <- Impact map XUYEN 3 repo
│   ├── IMPACT_INDEX.md             <- VE blast radius lookup
│   ├── UI_Screenshots_Analysis.md  <- Verified Monolith UI behavior
│   ├── test-standards.md           <- Test case format + priority rules
│   └── jira-workflow.md            <- Ticket to test case workflow
│
├── test-designs/
│   └── 2026/                    <- Test design docs theo nam
│
└── skills/                      <- Lane-specific skill overrides
    ├── web-analyze-ticket/
    └── web-create-test-cases/
```

## Khi nao sync context files?

| Event | File can sync |
|-------|--------------|
| Dev merge PR thay doi architecture VE | `context/ve-CLAUDE.md` |
| Dev merge PR thay doi Monolith | `context/monolith-CLAUDE.md` |
| Common skills co version moi | `context/skills-CLAUDE.md` |
| QA phat hien Monolith screen thay doi | `docs/UI_Screenshots_Analysis.md` |

```bash
# Sync ve-CLAUDE.md tu visual-editor
cp ../visual-editor/CLAUDE.md context/ve-CLAUDE.md
git commit -m "sync ve-CLAUDE.md - <mo ta thay doi>"
```

## Contacts

- **Lane QA Lead**: quynh.nguyenthihuong@optimizely.com
- **JIRA Project**: CJS (Web Experimentation)
- **Common Skills Repo**: https://github.com/episerver/claude-qa-skills
