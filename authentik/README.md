# Authentik

**Project:** RevChatham Homelab  
**Service:** Identity Provider (IdP)  
**Status:** Production  
**Version:** 1.0.0

---

# Purpose

Authentik provides centralized identity management for the homelab.

Current responsibilities include:

- Single Sign-On (SSO)
- OpenID Connect (OIDC)
- Authentication Portal
- User Management
- Future application integration

---

# Containers

| Container | Purpose |
|-----------|---------|
| PostgreSQL | Database |
| Authentik Server | Web UI / API |
| Authentik Worker | Background jobs |

---

# Docker Images

| Component | Image | Version |
|-----------|-------|---------|
| Authentik Server | `ghcr.io/goauthentik/server` | `2026.5.3` |
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

| Directory | Purpose |
|-----------|---------|
| data/ | Authentik application data |
| certs/ | TLS certificates |
| custom-templates/ | Custom branding and templates |

---

# Networking

Authentik connects to the shared Docker network:

```text
homelab
```

---

# Security Notes

- Secrets are stored in `.env`.
- `.env` is excluded from Git.
- PostgreSQL password is never stored in the compose file.
- Image version is pinned.
- PostgreSQL health checks are enabled.

The worker container mounts the Docker socket:

```text
/var/run/docker.sock
```

This allows Docker integration features but grants elevated access to the Docker daemon. Review this requirement before modifying the deployment.

---

# Deployment

Start the stack:

```bash
docker compose up -d
```

Stop the stack:

```bash
docker compose down
```

Restart:

```bash
docker compose restart
```

---

# Documentation

Additional documentation can be found in:

```text
docs/audits/authentik.md
```
