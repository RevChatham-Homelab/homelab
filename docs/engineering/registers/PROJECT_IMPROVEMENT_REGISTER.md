# Project Improvement Register

**Project:** RevChatham Homelab

**Document:** Project Improvement Register

**Document Version:** 1.0.0

**Document Owner:** RevChatham

**Last Reviewed:** 2026-07-16

**Status:** Operational

---

# Purpose

The Project Improvement Register (PIR) serves as the authoritative record of engineering improvements that have been reviewed, approved, and accepted for future implementation.

The register provides engineering traceability between ideas, milestone planning, implementation, repository audits, and completed work throughout the lifecycle of the RevChatham Homelab.

The PIR ensures improvements are evaluated, prioritized, and implemented in a controlled and repeatable manner.

---

# Scope

The Project Improvement Register includes:

- Approved engineering improvements
- Infrastructure enhancements
- Documentation improvements
- Operational improvements
- Security improvements
- Automation initiatives
- Repository improvements

The register intentionally excludes:

- Draft proposals that have not been approved
- Experimental ideas
- Daily operational tasks
- Incident records
- Recovery Point records

---

# Engineering Workflow

Engineering improvements follow the lifecycle below.

```text
Idea
    │
    ▼
Draft Proposal
    │
    ▼
Engineering Review
    │
    ▼
Project Improvement Register
    │
    ▼
Milestone Charter
    │
    ▼
Implementation
    │
    ▼
Repository Audit
    │
    ▼
CHANGELOG
```

---

# Improvement Register

| ID | Improvement | Proposed Milestone | Status | Completed |
|----|-------------|-------------------|--------|-----------|
| PIR-001 | Operational Automation Framework | v0.7.0 | Planned | — |
| PIR-002 | Operational 3-2-1 Backup Implementation | v0.7.0 | Planned | — |
| PIR-003 | Backup Standards Refinement | v0.7.0 | Planned | — |
| PIR-004 | Deploy Dozzle | v0.7.0 | Planned | — |
| PIR-005 | Deploy Grafana Loki | v0.7.0 | Planned | — |
| PIR-006 | Deploy Grafana Alloy | v0.7.0 | Planned | — |
| PIR-007 | Additional Grafana Dashboards | v0.7.0 | Planned | — |
| PIR-008 | README v1.1 Standardization | v0.8.0 | Planned | — |
| PIR-009 | Portfolio Website Development | v0.9.0 | Planned | — |
| PIR-010 | Architecture Diagrams | v0.9.0 | Planned | — |
| PIR-011 | Docker Network Diagrams | v0.9.0 | Planned | — |
| PIR-012 | Authentication Flow Diagrams | v0.9.0 | Planned | — |
| PIR-013 | Reverse Proxy Architecture Diagram | v0.9.0 | Planned | — |
| PIR-014 | PROJECT_RETROSPECTIVE.md | v1.0.0 | Planned | — |

---

# Status Definitions

| Status | Meaning |
|---------|---------|
| Planned | Approved for a future milestone. |
| In Progress | Currently being implemented. |
| Completed | Successfully implemented and verified. |
| Deferred | Approved but intentionally postponed. |
| Cancelled | Removed from future consideration. |

---

# Register Management

The Project Improvement Register is reviewed:

- At the beginning of every milestone.
- During repository engineering reviews.
- At milestone completion.
- Before major version releases.

Engineering improvements identified during an active milestone that are **not required** to complete the current milestone should be recorded in this register and deferred until milestone planning for a future release.

Completed improvements remain in this register to preserve project history, engineering traceability, and project decision history.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| `ROADMAP.md` | Defines the long-term direction of the project. |
| `draft_proposals/` | Records ideas awaiting engineering review. |
| `engineering/charters/` | Defines milestone objectives and deliverables. |
| `docs/decisions/` | Records accepted Architecture Decision Records (ADRs) that guide the long-term architecture of the repository. |
| `CHANGELOG.md` | Records completed work and milestone history. |

---

Project Improvement Register v1.0.0
