# Environment Variable Standard

**Project:** RevChatham Homelab  
**Document:** Environment Variable Standard  
**Version:** 1.0.0  
**Last Updated:** 2026-07-08

---

# Purpose

This document defines the standards for `.env` and `.env.example` files used throughout the RevChatham Homelab.

The objective is to provide a consistent structure for configuration management while ensuring sensitive information is never committed to the repository.

---

# Scope

This standard applies to:

- `.env`
- `.env.example`

for every Dockerized service in the homelab.

---

# Environment File Responsibilities

## .env

The `.env` file contains the production configuration for a service.

It may contain:

- Passwords
- API keys
- OAuth secrets
- Database credentials
- Hostnames
- Docker image versions
- Service configuration

The `.env` file **must never** be committed to Git.

---

## .env.example

The `.env.example` file documents the required environment variables for a service.

It contains:

- Placeholder values
- Default values where appropriate
- No production secrets

This file **must** be committed to Git.

---

# Placeholder Environment Files

Some services do not require sensitive environment variables.

For these services:

- `.env` and `.env.example` may contain identical values.
- `.env.example` should include a short header indicating that it serves as the template for the production `.env` file.
- No placeholder values are required unless secrets are introduced in the future.

Example:

```dotenv
# ==========================================
# Placeholder Environment File
# ==========================================

# This service currently contains no sensitive
# environment variables.
#
# This file serves as the template for the
# production .env file.
```

---

# File Organization

Environment files should be organized into logical sections.

Only include the sections that apply to the service.

Unused sections should be omitted to reduce clutter and improve readability.

Recommended order:

```dotenv
# ==========================================
# Docker Image
# ==========================================

# ==========================================
# Container
# ==========================================

# ==========================================
# Networking
# ==========================================

# ==========================================
# Application
# ==========================================

# ==========================================
# Authentication
# ==========================================

# ==========================================
# Database
# ==========================================

# ==========================================
# Monitoring
# ==========================================

# ==========================================
# Email
# ==========================================
```

Unused sections should be omitted.

---

# Section Guidelines

| Section | Purpose |
|----------|---------|
| Docker Image | Image name and pinned version (`*_IMAGE`, `*_TAG`) |
| Container | Container runtime settings such as `PUID`, `PGID`, `TZ`, `UMASK`, etc. |
| Networking | Ports, domains, hostnames, allowed hosts, and networking configuration |
| Application | Service-specific configuration |
| Authentication | Passwords, OAuth settings, API keys, tokens, and authentication configuration |
| Database | Database connection information and credentials |
| Monitoring | Metrics, logging, and telemetry configuration |
| Email | SMTP and email notification configuration |

---

# Docker Image Policy

Every Dockerized service should define both an image name and an image tag.

Example:

```dotenv
SERVICE_IMAGE=example/image
SERVICE_TAG=v1.0.0
```

Docker Compose should reference these variables:

```yaml
image: ${SERVICE_IMAGE}:${SERVICE_TAG}
```

Docker images should be pinned to a specific version whenever possible.

Avoid using:

```yaml
image: example/image:latest
```

unless a pinned version is unavailable.

---

# Variable Naming

Environment variables should:

- Use uppercase letters
- Use underscores between words
- Use descriptive names

Example:

```dotenv
GRAFANA_IMAGE=
GRAFANA_TAG=

AUTHENTIK_IMAGE=
AUTHENTIK_TAG=

PIHOLE_IMAGE=
PIHOLE_TAG=
```

---

# Placeholder Values

`.env.example` should use obvious placeholder values.

Example:

```dotenv
PASSWORD=change_me
CLIENT_SECRET=replace_with_secret
API_KEY=replace_with_api_key
```

Production values belong only in `.env`.

---

# Secrets

Secrets include:

- Passwords
- Client secrets
- API keys
- Tokens
- Database credentials

Secrets must never appear in:

- Git
- Documentation
- README files
- Audit files

---

# Comments

Use standardized comment separators for section headers.

Example:

```dotenv
# ==========================================
# Docker Image
# ==========================================
```

This formatting should be consistent across all environment files.

---

# Repository Policy

Commit:

- `.env.example`

Do not commit:

- `.env`

---

# Change Control

This document is a controlled project standard.

Changes to this standard require explicit approval from the project owner before implementation.

---

Environment Standard v1.0
