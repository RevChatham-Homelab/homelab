# Authentik Audit

**Project:** RevChatham Homelab

**Document:** Authentik Audit

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-15

**Status:** Operational

---

# Executive Summary

Authentik provides centralized identity and access management for the RevChatham Homelab.

The deployment has been standardized using Docker Compose, pinned Docker images, environment files, persistent storage, PostgreSQL, service-specific Git exclusions, and repository-safe documentation.

The service is operational and provides Single Sign-On (SSO) and OpenID Connect (OIDC) authentication for homelab applications.

---

# Service Overview

| Component | Purpose |
|-----------|---------|
| Authentik Server | Identity provider, web interface, and API |
| Authentik Worker | Background processing and scheduled tasks |
| PostgreSQL | Persistent database backend |

---

# Docker Images

| Component | Image | Version |
|-----------|-------|---------|
| Authentik | `ghcr.io/goauthentik/server` | `2026.5.3` |
| PostgreSQL | `postgres` | `16-alpine` |

---

# Deployment Review

| Category | Status | Notes |
|----------|:------:|------|
| Docker Compose | ✅ | Deployment managed through `compose.yml` |
| Environment Variables | ✅ | Uses `.env` |
| Version Pinning | ✅ | Images pinned |
| Persistent Storage | ✅ | Uses bind-mounted application data |
| Database | ✅ | PostgreSQL backend configured |
| Docker Networking | ✅ | Uses shared `homelab` network |
| Restart Policy | ✅ | Uses `unless-stopped` |
| Runtime Health | ✅ | Server, Worker, and PostgreSQL operational |
| OIDC Provider | ✅ | Operational |
| SSO Integration | ✅ | Operational |

---

# Security Review

## Environment Configuration

Authentik uses environment variables for:

- Docker image configuration
- PostgreSQL credentials
- Secret key
- Database configuration

Sensitive values are stored only within the production `.env` file.

Result:

✅ Passed

---

## Runtime Data

| Item | Commit to Git |
|------|:-------------:|
| `.env` | ❌ |
| `.env.example` | ✅ |
| `data/` | ❌ |
| `certs/` | ❌ |
| `custom-templates/` | ❌ |
| `compose.yml` | ✅ |
| `.gitignore` | ✅ |
| `README.md` | ✅ |

---

## Persistent Data

Persistent application data is stored within:

```text
data/
```

Additional runtime directories include:

```text
certs/
custom-templates/
```

These locations contain:

- Identity provider configuration
- User accounts
- Applications
- Providers
- Flows
- Certificates
- Branding assets

Result:

✅ Passed

---

## Docker Socket

The Authentik Worker mounts:

```text
/var/run/docker.sock
```

This enables Docker integration features and grants elevated access to the Docker daemon.

The configuration is intentional and documented.

Result:

✅ Passed

---

## Git Exclusions

The service-specific `.gitignore` excludes:

```text
.env
data/
certs/
custom-templates/
*.bak
*.log
*.tmp
```

Result:

✅ Passed

---

# Documentation Review

| Item | Status |
|------|:------:|
| README | ✅ |
| `.env.example` | ✅ |
| `.gitignore` | ✅ |
| Compose Documentation | ✅ |
| Audit Documentation | ✅ |

---

# Improvements Completed

- Docker images pinned to specific versions
- Standardized `.env`
- Standardized `.env.example`
- Created service-specific `.gitignore`
- Created README using README Template v1.0
- PostgreSQL deployment documented
- Docker socket usage documented
- OIDC configuration documented
- Runtime data excluded from Git
- Repository-safe files copied to `~/homelab/authentik`

---

# Audit Result

**Status:** 🟢 Passed

Authentik has been standardized according to the RevChatham Homelab deployment, documentation, environment, and security standards.

The service is operational and provides centralized identity management, Single Sign-On (SSO), and OpenID Connect (OIDC) authentication for the homelab.

---

Authentik Audit v1.0.0
