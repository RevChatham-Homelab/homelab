# Authentik

**Project:** RevChatham Homelab  
**Service:** Identity Provider (IdP)  
**Status:** Production  
**Version:** 1.0.0  
**Last Updated:** 2026-07-10

---

# Overview

Authentik provides centralized identity and access management for the RevChatham Homelab.

It serves as the primary Identity Provider (IdP) and provides Single Sign-On (SSO) and OpenID Connect (OIDC) authentication for supported homelab applications.

---

# Purpose

Authentik provides:

- Single Sign-On (SSO)
- OpenID Connect (OIDC)
- User and group management
- Authentication portal
- Application and provider management
- Centralized identity services

---

# Components

| Component | Purpose |
|-----------|---------|
| Authentik Server | Web interface, API, and identity provider |
| Authentik Worker | Background processing and scheduled tasks |
| PostgreSQL | Persistent database backend |

---

# Docker Images

| Component | Image | Version |
|-----------|-------|---------|
| Authentik Server | `ghcr.io/goauthentik/server` | `2026.5.3` |
| Authentik Worker | `ghcr.io/goauthentik/server` | `2026.5.3` |
| PostgreSQL | `postgres` | `16-alpine` |

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

| File / Directory | Purpose |
|------------------|---------|
| `data/` | Authentik application data |
| `certs/` | Certificates used by Authentik |
| `custom-templates/` | Custom branding and templates |
| PostgreSQL volume | Database storage |

---

# Networking

Authentik connects to the shared Docker network:

```text
homelab
```

Published ports:

```text
9000
9444
```

---

# Security Notes

- Secrets are stored in `.env`.
- `.env` is excluded from Git.
- PostgreSQL credentials are not stored directly in `compose.yml`.
- Docker image versions are pinned.
- PostgreSQL health checks are enabled.
- Runtime data and certificates are excluded from Git.

The Authentik Worker mounts the Docker socket:

```text
/var/run/docker.sock
```

This enables Docker integration features and grants elevated access to the Docker daemon.

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
docs/audits/authentik.md
```

---

README Template v1.0
