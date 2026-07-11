# Backup Inventory

**Project:** RevChatham Homelab
**Document:** Backup Inventory
**Version:** 1.0.0
**Approved:** 2026-07-11
**Status:** Approved Standard

---

# Purpose

This document identifies every asset that requires backup as part of the RevChatham Homelab.

It serves as the master inventory for backup planning and disaster recovery.

Every backup procedure and restore procedure should reference this inventory.

---

# Backup Categories

The backup inventory is divided into the following categories:

- Documentation
- Source Control
- Docker Services
- Application Data
- Virtual Machines
- Infrastructure Configuration
- External Services

---

# Inventory

| Asset | Location | Backup Required | Priority | Restore Reference | Notes |
|--------|----------|:---------------:|:--------:|-------------------|-------|
| Git Repository | GitHub / `~/homelab` | ✅ | High | GITHUB_BACKUP.md | Source of truth for project documentation |
| Homepage | `~/homepage` | ✅ | Medium | DOCKER_BACKUP.md | Dashboard configuration |
| Authentik | `~/authentik` | ✅ | High | DOCKER_BACKUP.md | Includes PostgreSQL database |
| Grafana | `~/grafana` | ✅ | Medium | DOCKER_BACKUP.md | Dashboards and configuration |
| Prometheus | `~/prometheus` | ✅ | Medium | DOCKER_BACKUP.md | Metrics configuration |
| Pi-hole | `~/pihole` | ✅ | High | DOCKER_BACKUP.md | DNS configuration |
| Portainer | `~/portainer` | ✅ | Medium | DOCKER_BACKUP.md | Container management |
| Uptime Kuma | `~/uptime-kuma` | ✅ | Medium | DOCKER_BACKUP.md | Monitoring database |
| Nginx Proxy Manager | `~/nginx-proxy-manager` | ✅ | High | DOCKER_BACKUP.md | Reverse proxy and SSL certificates |
| Portfolio Website | `~/website` | ✅ | Medium | DOCKER_BACKUP.md | Website content |
| Ubuntu Server VM | Proxmox | ✅ | Critical | PROXMOX_BACKUP.md | Primary application host |

---

# Recovery Priority

Recovery should occur in the following order:

| Priority | Component |
|----------|-----------|
| Critical | Proxmox Host |
| Critical | Ubuntu Server VM |
| High | Git Repository |
| High | Nginx Proxy Manager |
| High | Authentik |
| High | Pi-hole |
| Medium | Homepage |
| Medium | Portainer |
| Medium | Grafana |
| Medium | Prometheus |
| Medium | Uptime Kuma |
| Medium | Portfolio Website |

---

# Inventory Maintenance

The Backup Inventory should be reviewed whenever:

- A new service is deployed.
- A service is retired.
- Backup locations change.
- Recovery priorities change.
- Infrastructure changes significantly.

The inventory should always reflect the current production environment.

---

# Related Documentation

- BACKUP_STRATEGY.md
- BACKUP_SCHEDULE.md
- GITHUB_BACKUP.md
- DOCKER_BACKUP.md
- PROXMOX_BACKUP.md
- OFFSITE_BACKUP.md
- RESTORE_PROCEDURES.md
- DISASTER_RECOVERY.md
- SYSTEM_RECOVERY_RUNBOOK.md

---

Backup Inventory v1.0.0
