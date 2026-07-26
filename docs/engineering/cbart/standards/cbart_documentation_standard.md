# CBART Documentation Standard

**Project:** RevChatham Homelab

**Document ID:** app-cbart-001

**Document:** CBART Documentation Standard

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-26

**Status:** Draft

---

# Purpose

This document establishes the documentation standards used throughout the Console Backup and Recovery Tool (CBART) project. Its purpose is to ensure that all documentation remains consistent, professional, maintainable, and easy to navigate.

These standards apply to all documentation contained within the CBART documentation repository unless explicitly stated otherwise.

---

# Document Header

Every CBART document shall begin with the following header.

```md
# Document Title

**Project:** RevChatham Homelab

**Document ID:** app-cbart-###

**Document:** Document Name

**Document Version:** x.y.z

**Last Reviewed:** YYYY-MM-DD

**Status:** Draft | Review | Approved | Archived

---
```

---

# Document Footer

Every CBART document shall conclude with a footer identifying the document title and version.

Example:

```
CBART Documentation Standard v1.0.0
```

---

# Document Identification

Application documentation uses the following identifier format:

```
app-cbart-###
```

Examples:

| Document ID | Purpose |
|-------------|---------|
| app-cbart-000 | Repository README |
| app-cbart-001 | Documentation Standard |
| app-cbart-002 | Template |
| app-cbart-003 | Architecture |
| app-cbart-004 | Principles |
| app-cbart-005 | Design Specification |
| app-cbart-006 | Implementation Guide |
| app-cbart-007 | Runbook |
| app-cbart-008 | Troubleshooting Guide |
| app-cbart-009 | Reference |

User Manual chapters use a separate namespace.

```
cbart_manual-###
```

---

# Repository Organization

Documentation shall be organized according to the following structure.

```
cbart/
├── README.md
├── chapter_*.md
├── appendix_*.md
├── standards/
├── architecture/
├── implementation/
└── images/
```

Documents shall be placed in the directory that best matches their purpose.

---

# Markdown Conventions

Documentation should follow these conventions.

- Use ATX (`#`) headings.
- Leave a blank line before and after headings.
- Use fenced code blocks with language identifiers when appropriate.
- Prefer tables for structured information.
- Use bullet lists for unordered content.
- Keep line lengths readable.
- Use relative Markdown links for cross-references.

---

# Cross References

Whenever practical, documentation should reference existing documents instead of duplicating content.

Examples:

```md
[Chapter 1 – Introduction](../chapter_01_introduction.md)
```

```md
[CBART Navigation Standard](cbart_navigation_standard.md)
```

Relative links should always be used within the repository.

---

# Versioning

Documentation versions follow semantic versioning.

| Version | Meaning |
|----------|---------|
| 0.x.x | Draft |
| 1.x.x | Initial release |
| 2.x.x | Major revision |

---

# Status Values

Approved status values are:

- Draft
- Review
- Approved
- Archived

---

# Guiding Principles

CBART documentation follows these principles.

- Documentation is part of the application.
- Documentation evolves with the application.
- Standards drive implementation.
- One authoritative source for each topic.
- Consistency takes priority over creativity.
- Documentation should be easy to maintain and expand.

---

CBART Documentation Standard v1.0.0
