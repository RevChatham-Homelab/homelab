# Documentation Standard

**Project:** RevChatham Homelab

**Document:** Documentation Standard

**Document Version:** 2.0.0

**Last Reviewed:** 2026-07-15

**Status:** Operational

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

**Document:** Document Name

**Document Version:** x.y.z

**Last Reviewed:** YYYY-MM-DD

**Status:** Draft | Operational | Deprecated | Archived
```

---

## Metadata Classification

Governed documentation shall use metadata appropriate to the document type.

### Controlled Documents

Use:

- Project
- Document
- Document Version
- Last Reviewed
- Status

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
- Document Version
- Last Reviewed
- Status

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
- Document Version
- Last Reviewed
- Status

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
- Document
- Document Version
- Last Reviewed
- Status

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

Project Improvement Register v1.0.0
```

The footer provides document identification for printed or separated pages and serves as a quick reference to the document version.

Documents assigned controlled identifiers may include those identifiers beneath the footer.

Example:

```text
System Recovery Manual v1.0.0

Recovery Manual ID: SRM-1.0.0
```

---

## Change Control

This document is a controlled engineering standard.

Changes to this standard require explicit approval from the project owner.

Repository documentation shall be reviewed for compliance during repository audits.

---

Documentation Standard v2.0.0
