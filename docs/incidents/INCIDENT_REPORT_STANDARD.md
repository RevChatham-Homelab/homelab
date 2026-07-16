# Incident Report Standard

**Project:** RevChatham Homelab

**Document:** Incident Report Standard

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-16

**Status:** Operational

---

# Purpose

This standard defines the approved format, content, governance, and lifecycle of Incident Reports within the RevChatham Homelab.

Incident Reports preserve operational knowledge by documenting incidents, troubleshooting activities, verified root causes, resolutions, and lessons learned.

The objective is to ensure incident documentation remains accurate, consistent, reproducible, and useful for future engineering, maintenance, and recovery activities.

---

# Scope

This standard applies to all operational incidents documented within:

```text
docs/incidents/
```

Every incident recorded in the repository shall comply with this standard.

---

# Incident Definition

An incident is any unplanned event that disrupts, degrades, prevents, or significantly impacts the normal operation of the homelab.

Examples include:

- Service failures
- Authentication issues
- Docker failures
- Network connectivity problems
- Backup failures
- Recovery events
- Configuration errors
- Infrastructure outages

Routine maintenance activities are not considered incidents unless an unexpected operational issue occurs.

---

# Incident Identification

Each incident shall be assigned a unique identifier.

Format:

```text
IR-YYYYMMDD-###
```

Example:

```text
IR-20260709-001
```

The identifier consists of:

- IR — Incident Report
- YYYYMMDD — Incident date
- ### — Sequential incident number for that day

---

# Required Sections

Every Incident Report shall contain the following sections.

- Incident Identification
- Incident Summary
- Environment
- Symptoms
- Impact
- Initial Assessment
- Investigation
- Evidence Collected
- Commands Executed
- Root Cause
- Resolution
- Verification
- Recovery Point
- Lessons Learned
- Follow-Up Actions
- Related Documentation
- Supporting Files

Additional sections may be added when operationally necessary.

---

# Supporting Evidence

Incident Reports may include supporting evidence such as:

- Command logs
- Terminal output
- Screenshots
- Application logs
- System logs
- Configuration files
- Exported data
- Other operational artifacts

Supporting files should be stored within the incident directory whenever practical.

---

# Incident Directory Structure

Incident documentation shall follow the approved repository structure.

```text
docs/incidents/
└── YYYY-MM-DD/
    └── 001_incident-name/
        ├── INCIDENT_REPORT.md
        ├── COMMAND_LOG.md
        ├── TERMINAL_OUTPUT.txt
        ├── screenshots/
        ├── logs/
        ├── configs/
        └── attachments/
```

Supporting directories should be created only when required.

---

# Documentation Requirements

Incident Reports shall:

- Document facts rather than assumptions.
- Distinguish verified root causes from suspected causes.
- Record investigation steps in chronological order.
- Document the final resolution.
- Record verification activities.
- Capture lessons learned.
- Reference related documentation where appropriate.

---

# Security

Incident documentation shall not contain:

- Passwords
- API tokens
- Private keys
- Authentication secrets
- Sensitive personal information

Sensitive information shall be removed or redacted before publication.

---

# Governance

Incident Reports are controlled engineering documents.

Completed Incident Reports become part of the permanent operational history of the RevChatham Homelab and shall not be deleted solely because an incident has been resolved.

Changes to this standard require approval from the project owner.

---

# Related Documentation

- Documentation Standard
- Incident Report Template
- Engineering Principles
- Design Philosophy

---

Incident Report Standard v1.0.0
