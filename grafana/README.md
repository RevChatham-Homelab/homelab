# Grafana

**Project:** RevChatham Homelab  
**Service:** Monitoring & Visualization Platform  
**Status:** Production  
**Version:** 1.0.0  
**Last Updated:** 2026-07-08

---

# Overview

Grafana provides centralized dashboards and visualization for the RevChatham Homelab. It integrates with Prometheus to display infrastructure and container metrics while using Authentik for centralized authentication through OpenID Connect (OIDC).

---

# Purpose

Grafana provides:

- Infrastructure dashboards
- System monitoring
- Container monitoring
- Data visualization
- Prometheus integration
- Centralized authentication through Authentik

---

# Components

| Component | Purpose |
|-----------|---------|
| Grafana | Dashboard and visualization platform |

---

# Docker Images

| Component | Image | Version |
|-----------|-------|---------|
| Grafana | `grafana/grafana-oss` | `13.0.2` |

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

| Volume | Purpose |
|--------|---------|
| grafana-data | Dashboards, users, data sources, and application configuration |

---

# Networking

Grafana connects to the shared Docker network:

```text
homelab
```

Grafana is currently accessible through Docker port mapping and is published through Nginx Proxy Manager.

---

# Security Notes

- Secrets are stored in `.env`.
- `.env` is excluded from Git.
- Grafana administrator credentials are not stored in the compose file.
- Authentik OAuth credentials are stored in `.env`.
- Docker image version is pinned.
- Authentication is provided through Authentik using OpenID Connect (OIDC).

---

# Deployment

Start:

```bash
docker compose up -d
```

Restart:

```bash
docker compose restart
```

Stop:

```bash
docker compose down
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
docs/audits/grafana.md
```

---

README Template v1.0
