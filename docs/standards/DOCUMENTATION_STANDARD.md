# Documentation Standard

**Project:** RevChatham Homelab

**Document ID:** doc-001

**Document:** Documentation Standard

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-22

**Status:** Draft

**Author:** Adrian Chatham

---

# Purpose

This standard defines the approved structure, formatting, lifecycle, and governance of documentation within the RevChatham Homelab.

The objective of this standard is to ensure repository documentation remains accurate, consistent, maintainable, and easily identifiable throughout the project lifecycle.

---

# Document Structure

All governed documentation shall follow the structure defined below.

---

## Header

Every governed document shall begin with standardized metadata appropriate to the document type.

### Controlled Documents

```markdown
# Document Title

**Project:** RevChatham Homelab

**Document ID:** doc-000

**Document:** Document Name

**Document Version:** x.y.z

**Last Reviewed:** YYYY-MM-DD

**Status:** Draft | Approved | Released - YYYY-MM-DD | Deprecated | Archived

**Author:** Adrian Chatham
```

---

## Metadata Classification

Governed documentation shall use metadata appropriate to the document type.

### Controlled Documents

Use:

- Project
- Document ID
- Document
- Document Version
- Last Reviewed
- Status
- Author

Examples:

- Backup Strategy
- Recovery Point Standard
- Engineering Principles
- System Recovery Manual

---

### Service Documentation

Service documentation describes a deployed application or infrastructure service.

Use:

- Project
- Service
- Document ID
- Document Version
- Last Reviewed
- Status
- Author

Examples:

- Homepage
- Pi-hole
- Grafana
- Portainer

---

### Directory Documentation

Directory documentation describes the purpose and organization of a repository directory.

Use:

- Project
- Directory
- Document ID
- Document Version
- Last Reviewed
- Status
- Author

Examples:

- Engineering
- Templates
- Incidents
- Decisions

---

### Overview Documentation

Overview documentation introduces a repository or documentation collection.

Use:

- Project
- Document ID
- Document
- Document Version
- Last Reviewed
- Status
- Author

Examples:

- Repository README
- Documentation Overview

---

### Controlled Identifiers

Controlled identifiers may be included when they uniquely identify a governed document.

Examples include:

- Recovery Manual ID
- Recovery Runbook ID
- Recovery Point ID

Controlled identifiers supplement the required metadata and shall not replace required metadata fields.

---

## Document Prefix Naming Convention

Document prefixes identify the document namespace.

Repository-wide documentation categories shall use lowercase prefixes.

Examples:

- doc
- eng
- arc

Project or system acronyms shall use uppercase prefixes.

Examples:

- RMA
- RAF
- RP
- SRM

Document IDs combine the document prefix with a reserved document number.

Examples:

```text
doc-001
eng-001
arc-003
RMA-001
RAF-003
RP-001
SRM-001
```

This convention provides a clear visual distinction between repository-wide documentation and project-specific systems while maintaining consistent document identification.

---

## Reserved Document Numbers

The following document numbers are reserved across the repository.

| Number | Purpose |
|---------|--------------------------|
| 000 | README / Overview |
| 001 | Standard |
| 002 | Template |
| 003 | Architecture |
| 004 | Principles |
| 005 | Design Specification |
| 006 | Implementation Guide |
| 007 | Runbook |
| 008 | Troubleshooting Guide |
| 009 | Reference |

These reserved identifiers shall remain consistent throughout the repository.

---

## Document Lifecycle

Documentation follows the lifecycle below.

```text
Version: 1.0.0
Status: Draft

↓

Review

↓

Version: 1.0.0
Status: Approved

↓

Version: 1.0.0
Status: Released - YYYY-MM-DD
```

A review is considered an activity rather than a document status.

---

## Body

The body of the document shall clearly communicate the purpose of the document.

Information shall remain technically accurate, concise, and maintainable.

Documentation shall be written for long-term operational use.

---

## Tail / Footer

Governed documentation shall conclude with a human-readable footer that identifies the document and its version.

Format:

```text
Document Title vX.Y.Z
```

### Examples

```text
Documentation Standard v1.0.0

Repository README v1.0.0

Project Changelog v1.0.0

Backup Schedule v1.0.0

Engineering Principles v1.0.0
```

The footer provides document identification for printed or separated pages and serves as a quick reference to the document version.

Documents assigned controlled identifiers may include those identifiers beneath the footer.

Example:

```text
System Recovery Manual v1.0.0

Document ID: SRM-001
```

---

## Revision History

Every governed document shall maintain a revision history.

Example:

| Version | Date | Description | Author |
|----------|------------|---------------------------|----------------|
| X.Y.Z | YYYY-MM-DD | Description | Adrian Chatham |

---

## Change Control

This document is a controlled engineering standard.

Changes to this standard require explicit approval from the project owner.

Repository documentation shall be reviewed for compliance during repository audits.

---

Documentation Standard v1.0.0
