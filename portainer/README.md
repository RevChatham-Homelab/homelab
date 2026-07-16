# Portainer

**Project:** RevChatham Homelab  
**Service:** Container Management  
**Status:** Production  
**Version:** 1.0.0  
**Last Updated:** 2026-07-09

---

# Overview

Portainer provides centralized management of Docker containers, images, networks, volumes, and stacks through a web-based interface. It simplifies day-to-day administration of the RevChatham Homelab while integrating with Authentik for authentication.

---

# Purpose

Portainer provides:

- Docker container management
- Stack deployment and management
- Volume management
- Network management
- Container image management
- Docker host monitoring
- Web-based administration

---

# Components

| Component | Purpose |
|-----------|---------|
| Portainer CE | Docker management platform |

---

# Docker Images

| Component | Image | Version |
|-----------|-------|---------|
| Portainer CE | `portainer/portainer-ce` | `2.39.3` |

---

# Environment Variables

Configuration is stored in:

```text
.env
```

An example configuration is provided in:

```text
.env.example
```

---

# Persistent Data

| Volume / Directory | Purpose |
|--------------------|---------|
| `portainer_data` | Portainer database, users, endpoints, settings, and application data |

---

# Networking

Portainer connects to the shared Docker network:

```text
homelab
```

The service exposes:

| Port | Purpose |
|------|---------|
| 9443 | HTTPS Web Interface |
| 8000 | Edge Agent |

---

# Security Notes

- Docker image version is pinned.
- Configuration is managed through `.env`.
- `.env` is excluded from Git.
- Persistent application data is stored in the `portainer_data` Docker volume.
- Portainer mounts the Docker socket:

```text
/var/run/docker.sock
```

This provides administrative access to the Docker daemon and is required for container management. Access to the Portainer web interface should be restricted to authorized administrators.

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
docs/audits/portainer.md
```

Migration from Docker Run to Docker Compose:

```text
docs/incidents/2026-07-09/001_portainer-compose-migration/INCIDENT_REPORT.md
```

---

README Template v1.0
