# Docker Backup Procedure

**Project:** RevChatham Homelab

**Document:** Docker Backup Procedure

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-13

**Status:** Operational

---

# Purpose

This document defines the approved procedure for backing up Docker applications used within the RevChatham Homelab.

The objective is to preserve service configurations, documentation, and persistent application data required to restore Docker services following a system failure.

---

# Backup Philosophy

Docker services are backed up individually.

Each service should be capable of being restored independently without requiring the restoration of unrelated services.

All Docker backups become part of a Recovery Point (RP).

---

# Backup Scope

Each Docker service backup should include, when applicable:

- Docker Compose file
- README documentation
- Environment example (`.env.example`)
- Service configuration
- Persistent application data
- Runtime configuration

The following items are intentionally excluded:

- Temporary files
- Cache files
- Runtime logs
- Recovery Point documentation
- VM backups

---

# Docker Services

The current production services include:

- Homepage
- Authentik
- Grafana
- Prometheus
- Pi-hole
- Portainer
- Uptime Kuma
- Nginx Proxy Manager
- Portfolio Website

---

# Backup Procedure

For each service:

1. Navigate to the user's home directory.

```bash
cd ~
```

2. Create the service archive.

Example:

```bash
tar -czf \
"$RP/docker/homepage.tar.gz" \
homepage
```

3. Verify the archive.

```bash
tar -tzf \
"$RP/docker/homepage.tar.gz" | head -20
```

4. Record the result in:

- verification.log
- RP_MANIFEST.md

5. Repeat for each production service.

---

# Special Procedures

Some Docker services contain privileged files.

Examples:

- Pi-hole
- Nginx Proxy Manager

These services may require elevated privileges.

Example:

```bash
sudo tar -czf \
"$RP/docker/nginx-proxy-manager.tar.gz" \
nginx-proxy-manager
```

After creating the archive:

```bash
sudo chown angel:angel \
"$RP/docker/nginx-proxy-manager.tar.gz"
```

Future automation should verify administrative privileges before beginning the backup process.

---

# Verification

Each Docker backup must pass:

- Archive created successfully.
- Archive read test completed.
- Verification log updated.
- Recovery Point Manifest updated.

---

# Restore Procedure

Docker services should be restored only after:

1. Proxmox Host
2. Ubuntu Server VM
3. Networking

have been successfully restored.

Individual services should then be restored according to the System Recovery Manual.

---

# Recovery Validation

Recovery is complete when:

- Docker services start successfully.
- Containers are healthy.
- Volumes are accessible.
- Homepage links function.
- Service health checks pass.

---

Docker Backup Procedure v1.0.0
