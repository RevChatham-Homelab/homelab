# Decision Record

## Recovery Automation Security Model

## Document Information

**Project:** Revchatham Homelab

**Date:** 2026-07-18

**Decision ID:** DEC-2026-07-18-001

**Document Type:** Management Decision Record

**Status:** Approved

**Category:** Security Architecture

---

# Decision

Recovery Automation will use dedicated service identities and least
privilege access instead of root-based automation.

---

# Context

The Recovery Automation system requires controlled access to
infrastructure resources in order to collect recovery metadata.

Using root SSH access would create unnecessary security exposure and
reduce auditability.

---

# Reasoning

The selected security model provides:

-   Clear ownership of automation access
-   Reduced administrative exposure
-   Improved auditing
-   Easier future security improvements

---

# Approved Architecture

    Recovery Automation
            |
            SSH Key
            |
            v
    recovery@proxmox
            |
            Limited sudo access
            |
            v
    Proxmox metadata collection

---

# Operational Impact

This decision establishes:

-   Dedicated automation identities
-   Least privilege access
-   Separation between human and automation accounts
-   Improved recovery workflow security

---

# Future Considerations

Potential improvements:

-   Proxmox API token authentication
-   Centralized secrets management
-   Automated access validation
-   Expanded identity management controls

---

# Final Decision

Approved.

Recovery Automation will follow least privilege security practices.

---

# Footer

**Document Status:** Approved

**Maintained By:** RevChatham Homelab Documentation

---

-End- of Decision Record
