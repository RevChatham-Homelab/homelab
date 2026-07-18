# Engineering Decision Record

## Recovery Point Development Separation

## Document Information

**Project:** RevChatham Homelab

**Date:** 2026-07-18

**Decision ID:** ENG-2026-07-18-003

**Document Type:** Engineering Decision Record

**Status:** Approved

**Category:** Recovery Automation

------------------------------------------------------------------------

# Decision

Recovery Point development and testing artifacts will be separated from
official Recovery Points.

Official Recovery Points will remain in the production recovery output
directory, while failed, experimental, or development Recovery Points
will be preserved in a dedicated development location.

------------------------------------------------------------------------

# Context

During Recovery Automation testing, a failed Recovery Point was moved
out of the production output directory.

This exposed an important lifecycle consideration: Recovery Point IDs
should represent the official recovery timeline and should not be reused
because of failed development attempts.

------------------------------------------------------------------------

# Implementation

Production Recovery Points:

    automation/recovery/output/

Development Recovery Points:

    automation/recovery/output/development/

------------------------------------------------------------------------

# Operational Rules

## Production Recovery Points

The production output directory contains official Recovery Points only.

Example:

    automation/recovery/output/
    ├── RP-20260718-010
    ├── RP-20260718-011
    └── RP-20260718-012

------------------------------------------------------------------------

## Development Recovery Points

Failed or experimental Recovery Points are preserved for engineering
review.

Example:

    automation/recovery/output/development/
    └── RP-20260718-011

------------------------------------------------------------------------

# Reasoning

This approach preserves:

-   Recovery timeline integrity
-   Troubleshooting history
-   Auditability
-   Engineering investigation capability

A missing or separated Recovery Point should indicate an intentional
lifecycle event that can be investigated through logs, incidents, and
engineering records.

------------------------------------------------------------------------

# Alternatives Considered

## Recursive Recovery Point ID Search

Rejected.

Searching development directories when generating Recovery Point IDs
could create:

-   Duplicate history confusion
-   Ambiguous recovery timelines
-   Difficulty determining production status

------------------------------------------------------------------------

# Final Decision

Approved.

Recovery Point IDs will only represent official Recovery Points.

Development and failed Recovery Points will be preserved separately
without affecting the production recovery timeline.

------------------------------------------------------------------------

**Document Status:** Approved

**Maintained By:** RevChatham Homelab Documentation

------------------------------------------------------------------------

-End- of Recovery Point Development Separation
