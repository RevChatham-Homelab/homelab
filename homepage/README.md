# Homepage

**Project:** RevChatham Homelab  
**Service:** Dashboard & Service Launcher  
**Status:** Production  
**Version:** 1.0.0  
**Last Updated:** 2026-07-08

---

# Overview

Homepage serves as the central dashboard for the RevChatham Homelab. It provides a clean, organized interface for accessing infrastructure services, monitoring tools, documentation, and self-hosted applications.

---

# Purpose

Homepage provides:

- Centralized service dashboard
- Quick access to homelab applications
- Infrastructure organization
- Service monitoring integration
- Search functionality
- Custom branding and icons

---

# Components

| Component | Purpose |
|-----------|---------|
| Homepage | Dashboard and service launcher |

---

# Docker Images

| Component | Image | Version |
|-----------|-------|---------|
| Homepage | `ghcr.io/gethomepage/homepage` | `v1.13.2` |

---

# Environment Variables

Homepage currently does not require a `.env` file.

Configuration is maintained through YAML configuration files.

---

# Persistent Data

| File / Directory | Purpose |
|------------------|---------|
| config/ | Homepage configuration |
| bookmarks.yaml | Bookmarks |
| services.yaml | Service definitions |
| widgets.yaml | Dashboard widgets |
| settings.yaml | Homepage settings |
| docker.yaml | Docker integration |
| proxmox.yaml | Proxmox integration |
| kubernetes.yaml | Kubernetes integration |
| custom.css | Custom styling |
| custom.js | Custom JavaScript |

---

# Networking

Homepage connects to the shared Docker network:

```text
homelab
```

Homepage is currently accessible through Docker port mapping and will later be served through Nginx Proxy Manager.

---

# Security Notes

- Homepage does not store application secrets.
- Configuration files are safe to version control.
- Custom icons and branding assets are maintained within the repository.
- Docker and Proxmox integrations use separate configuration files.
- Runtime logs are excluded from version control.

---

# Deployment

Start:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

Restart:

```bash
docker compose restart
```

Update:

```bash
docker compose pull
docker compose up -d
```

---

# Documentation

Additional documentation can be found in:

```text
docs/audits/homepage.md
```

---

README Template v1.0
