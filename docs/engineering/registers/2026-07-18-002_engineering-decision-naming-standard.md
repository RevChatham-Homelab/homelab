# Engineering Decision Naming Standard

## Document Information

**Project:** RevChatham Homelab

**Date:** 2026-07-18

**Document Type:** Engineering Standard

**Status:** Approved

**Category:** Documentation Governance

---

# Purpose

This document establishes the naming convention for Engineering Decision
Records.

The goal is to provide consistent identification, chronological
organization, and maintainability as the engineering documentation
library grows.

---

# Naming Convention

Engineering Decision Records will use the following format:

    YYYY-MM-DD-###_description.md

Example:

    2026-07-18-001_recovery-automation-proxmox-service-account.md

---

# Format Breakdown

## Date

    YYYY-MM-DD

The date the engineering decision was recorded.

---

## Sequence Number

    ###

A sequential identifier for engineering decisions created on that date.

Example:

    001
    002
    003

---

## Description

A short, descriptive name that identifies the technical subject.

Example:

    recovery-automation-proxmox-service-account

---

# Storage Location

Engineering Decision Records are stored in:

    docs/engineering/registers/

---

# Document Classification

Engineering Decision Records:

-   Explain how technical solutions are implemented.
-   Document engineering choices.
-   Preserve technical context for future maintainers.

They are different from:

## Incident Records

Incident Records document:

-   What happened
-   Troubleshooting performed
-   Root cause
-   Resolution

## Management Decision Records

Management Decision Records document:

-   Why an architectural choice was made
-   Business or operational reasoning
-   High-level impact

---

# Versioning Standard

Engineering Decision Records are not template documents.

They do not use document version numbers.

They are identified by:

-   Date
-   Decision ID
-   Document status

Template documents may use version numbers when they define reusable
standards.

---

# Footer Standard

Non-template engineering documents will follow the established
RevChatham Homelab footer convention.

---

# Final Standard

Approved.

All future Engineering Decision Records will follow this naming
convention.

---

-End- of Engineering Decision Naming Standard
