# Recovery Point Index

**Project:** RevChatham Homelab

**Document:** Recovery Point Index

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-16

**Status:** Operational

---

# Purpose

This index provides a centralized inventory of all official Recovery Points created for the RevChatham Homelab.

Each Recovery Point represents a verified snapshot of the homelab at a specific point in time. This document serves as the authoritative catalog for locating Recovery Points, identifying their contents, and tracking their verification status.

The detailed documentation for each Recovery Point is maintained within the Recovery Point itself.

---

# Recovery Point Register

| Recovery Point | Date | Project Version | Status | Primary Media | Verification |
|----------------|------------|----------------|-------------|----------------|--------------|
| RP-20260711-001 | 2026-07-11 | v0.6.0 | Archived | BRR-USB-001 | ✅ Verified |
| RP-20260716-001 | 2026-07-16 | v0.6.1 | In Progress | BRR-USB-001 | 🟡 Repository Verified |

---

# Recovery Point Lifecycle

Recovery Points progress through the following lifecycle:

| Status | Description |
|---------|-------------|
| In Progress | Recovery Point is currently being created. |
| Pending Verification | Backup artifacts have been created but have not yet been verified. |
| Verified | Backup integrity has been successfully verified. |
| Operational | Recovery Point is approved for restoration. |
| Archived | Recovery Point has been superseded by a newer verified Recovery Point but remains available for historical recovery. |

---

# Naming Convention

Recovery Points use the following format:

```text
RP-YYYYMMDD-###
```

Example:

```text
RP-20260716-001
```

---

# Required Contents

Each Recovery Point should contain, at minimum:

- Recovery Point documentation
- Repository backup
- Verification files
- Backup notes

Additional artifacts such as Docker backups, Proxmox backups, configuration exports, or supporting evidence may be included as appropriate.

---

# Storage Locations

| Media ID | Volume Label | Filesystem | Purpose |
|----------|--------------|------------|---------|
| BRR-USB-001 | homelabbrr | ext4 | Primary removable backup media |

Additional backup media shall be recorded here as they are introduced into the Backup, Restore, and Recovery framework.

---

# Related Documentation

- Backup Strategy
- Backup Inventory
- Backup Schedule
- Recovery Point Standard
- System Recovery Manual
- System Recovery Runbook

---

Recovery Point Index v1.0.0
