# Engineering Decision Record

## Recovery Automation Proxmox Service Account

## Document Information

**Project:** RevChatham Homelab

**Date:**\
2026-07-18

**Decision ID:**\
ENG-2026-07-18-001

**Document Type:**\
Engineering Decision Record

**Status:**\
Approved

**Category:**\
Recovery Automation

---

# Decision

Recovery Automation will use a dedicated Proxmox service account with
SSH key authentication and restricted sudo permissions instead of using
root SSH access.

---

# Context

The Recovery Automation system requires access to Proxmox metadata
including:

-   Host information
-   Virtual machine inventory
-   Storage information
-   Backup information

Direct root SSH access was avoided to improve security, maintainability,
and auditability.

---

# Technical Implementation

## Service Account

Created:

    recovery@proxmox

Purpose:

Dedicated service account used by Recovery Automation workflows.

---

## Authentication

Implemented:

    SSH key authentication

Key:

    id_ed25519_recovery

---

## SSH Configuration

Configured SSH alias:

    proxmox-recovery

The alias provides consistent automation access to the Proxmox host.

---

## Privilege Model

The recovery account uses restricted sudo permissions for required
Proxmox collection commands.

Approved commands:

    /usr/sbin/qm
    /usr/sbin/pvesm
    /usr/bin/pveversion

This allows metadata collection without requiring root SSH access.

---

# Validation

Validated successful execution of:

    sudo /usr/sbin/qm list

Result:

VM inventory successfully collected.

---

Validated successful execution of:

    sudo /usr/sbin/pvesm status

Result:

Storage information successfully collected.

---

Validated successful execution of:

    sudo /usr/bin/pveversion

Result:

Proxmox version information successfully collected.

---

# Security Considerations

Benefits:

-   Eliminates root SSH dependency
-   Uses a dedicated automation identity
-   Limits elevated access
-   Improves auditability
-   Supports least privilege principles

---

# Future Considerations

Potential improvements:

-   Replace sudo-based collection with Proxmox API token authentication
-   Add automated permission validation
-   Expand recovery automation security controls as the platform grows

---

# Final Decision

Approved.

Recovery Automation will use a dedicated Proxmox recovery account
following least privilege principles.

---

# Documentation Metadata

**Document Type:**\
Engineering Decision Record

**Project:**\
RevChatham Homelab

**Category:**\
Recovery Automation

**Related Components:**

-   Proxmox
-   Ubuntu Server VM
-   Recovery Automation
-   SSH Authentication
-   Sudo Privilege Management

**Decision Date:**\
2026-07-18

**Document Status:**\
Approved

**Maintained By:**\
RevChatham Homelab Documentation

---

-End- of Engineering Decision Record
