# Recovery Point Standard

**Project:** RevChatham Homelab

**Document:** Recovery Point Standard

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-15

**Status:** Operational

---

# Purpose

This document defines the standard structure for every Recovery Point created for the RevChatham Homelab.

A Recovery Point represents a complete snapshot of the system at a specific point in time.

Every Recovery Point should be self-contained, verifiable, and suitable for restoring the homelab to a known operational state.

---

# Philosophy

The Recovery Point exists to support system restoration.

It is not merely a collection of backup files.

Every Recovery Point should contain everything necessary to restore the portions of the system captured during that backup session.

Recovery Points should be:

- Repeatable
- Verifiable
- Consistent
- Self-documenting

---

# Naming Convention

Recovery Points will use the following format:

```text
Recovery_Point_YYYY-MM-DD_HH-MM-SS
```

Example:

```text
Recovery_Point_2026-07-11_20-45-17
```

---

# Directory Structure

Every Recovery Point should follow the same layout.

```text
Recovery_Point_YYYY-MM-DD_HH-MM-SS/

├── documentation/
├── docker/
├── proxmox/
├── verification/
├── manifests/
└── notes/
```

---

# Directory Purpose

## documentation/

Contains project documentation and Git repository archives.

Examples:

- homelab.tar.gz

---

## docker/

Contains Docker application backups.

Examples:

- homepage.tar.gz
- authentik.tar.gz
- grafana.tar.gz
- prometheus.tar.gz
- pihole.tar.gz
- portainer.tar.gz
- uptime-kuma.tar.gz
- nginx-proxy-manager.tar.gz
- website.tar.gz

---

## proxmox/

Contains exported virtual machine backups.

---

## verification/

Contains files used to verify backup integrity.

Examples:

- checksums.sha256
- verification.log

---

## manifests/

Contains metadata describing the Recovery Point.

Examples:

- manifest.md

---

## notes/

Contains operational notes related to the Recovery Point.

Examples:

- notes.md

---

# Required Files

Every Recovery Point should include:

- Project documentation backup
- Docker application backups
- Verification data
- Manifest
- Operational notes

Virtual machine backups should be included whenever they are created.

---

# Verification Requirements

A Recovery Point is not considered complete until:

- Archives have been created successfully.
- Archives can be opened.
- Checksums have been generated.
- Verification has completed successfully.

Completion is measured by successful verification rather than archive creation.

---

# Automation

Recovery Point creation should ultimately be automated using Python.

Automation should:

- Create the Recovery Point directory.
- Generate timestamps.
- Archive required resources.
- Generate verification files.
- Produce manifests.
- Record logs.

---

# Manual Operations

The following activities require operator involvement:

- Copying Recovery Points to the Lenovo T14.
- Copying Recovery Points to removable USB media.
- Verifying off-site copies.
- Long-term archive management.

Automation should simplify these tasks but not eliminate operator verification.

---

# Related Documentation

- BACKUP_STRATEGY.md
- BACKUP_SCHEDULE.md
- BACKUP_INVENTORY.md
- GITHUB_BACKUP.md
- DOCKER_BACKUP.md
- PROXMOX_BACKUP.md
- OFFSITE_BACKUP.md
- SYSTEM_RECOVERY_MANUAL.md

---

Recovery Point Standard v1.0.0
