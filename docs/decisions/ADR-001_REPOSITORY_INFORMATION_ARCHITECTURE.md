# ADR-001: Repository Information Architecture

**Project:** RevChatham Homelab

**Decision ID:** ADR-001

**Status:** Accepted

**Date:** 2026-07-16

**Decision Owner:** RevChatham

---

# Purpose

This Architecture Decision Record (ADR) establishes the long-term information architecture of the RevChatham Homelab repository.

The objective is to organize documentation according to its purpose and intended audience, allowing technicians to quickly locate operational procedures during an incident while preserving engineering knowledge and project governance.

---

# Problem Statement

As the repository has grown, the number of documents has increased significantly.

Without a defined information architecture, operational procedures, engineering guidance, standards, philosophies, and historical records risk becoming intermixed.

During an incident, excessive navigation increases the time required to locate critical documentation.

---

# Decision

Repository documentation shall be organized according to **how and when it is used**, rather than solely by document type.

Operational documentation shall remain separate from engineering guidance.

---

# Information Architecture

The repository is organized into the following conceptual layers:

1. Foundation
2. Governance
3. Operations
4. Records
5. History

These layers describe the purpose of documentation rather than prescribing a specific folder structure.

---

# Foundation

Foundation contains the engineering knowledge that explains **why** the repository is designed and maintained in its current form.

Examples include:

- Engineering philosophies
- Engineering principles
- Documentation principles
- Naming standards
- Change management guidance

These documents support future engineering work and are generally not required during incident response.

---

# Governance

Governance defines how the repository is managed.

Examples include:

- Charters
- Standards
- Policies
- Templates

---

# Operations

Operational documentation provides step-by-step procedures used while performing work.

Examples include:

- Backup procedures
- Restore procedures
- Recovery manuals
- Runbooks
- Service procedures

These documents must be easy to locate during an incident.

---

# Records

Records capture evidence of work that has already occurred.

Examples include:

- Incident Reports
- Recovery Points
- Audit reports
- Verification evidence

Records should remain immutable once finalized except where updates are explicitly permitted.

---

# History

Historical documentation records the evolution of the project.

Examples include:

- CHANGELOG
- Archived documentation
- Previous Recovery Points

---

# Design Principles

The repository shall prioritize:

- Fast navigation during incident response.
- Separation of operational procedures from engineering guidance.
- Minimal navigation depth for frequently used documentation.
- Consistent organization across all documentation areas.

---

# Consequences

This decision establishes the basis for future repository restructuring.

Future improvements may include introducing a `foundational/` directory beneath `docs/engineering/` to organize engineering philosophies, principles, and related foundational guidance.

Any future structural changes should remain consistent with the architectural principles established by this ADR.

---

# Related Documentation

- docs/engineering/
- docs/BACKUP_RESTORE_RECOVER/
- docs/incidents/
- docs/templates/

---

ADR-001 v1.0.0
