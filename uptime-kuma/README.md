# Uptime Kuma

**Project:** RevChatham Homelab

**Service:** Uptime Kuma

**Document:** Service README

**Document Version:** 1.0.0

**Service Status:** Production

**Last Reviewed:** 2026-07-16

---

# Overview

Uptime Kuma provides monitoring for the homelab infrastructure.

It continuously monitors internal and external services, allowing quick identification of outages and service interruptions.

---

# Purpose

The service is responsible for:

- Monitoring service availability
- Monitoring HTTP/HTTPS endpoints
- Monitoring Docker-hosted services
- Providing uptime history
- Providing a centralized monitoring dashboard

---

# Components

- Docker Compose
- Uptime Kuma 2.4.0
- SQLite Database
- Shared Docker Network (`homelab`)
- Persistent application data

---

# Docker Images

```text
louislam/uptime-kuma:2.4.0
```

---

# Environment Variables

Managed through:

```text
.env
```

Current variables:

```dotenv
UPTIME_KUMA_IMAGE=louislam/uptime-kuma
UPTIME_KUMA_TAG=2.4.0
UPTIME_KUMA_PORT=3001
```

---

# Persistent Data

Persistent application data is stored in:

```text
./data
```

This directory contains:

- SQLite database
- Monitor configuration
- Notification configuration
- Application settings

---

# Networking

Docker Network:

```text
homelab
```

Published Port:

```text
3001
```

Container Name:

```text
uptime-kuma
```

---

# Security Notes

The following are excluded from Git:

```text
.env
data/
data-backup-*/
*.bak
*.log
*.tmp
```

No secrets are currently stored within the environment variables.

---

# Deployment

Deployment Method:

```text
Docker Compose
```

Restart Policy:

```text
unless-stopped
```

Health Check:

```text
Healthy
```

---

# Documentation

Repository files:

```text
compose.yml
.env.example
.gitignore
README.md
```

Runtime files excluded from Git:

```text
.env
data/
data-backup-*/
```

---

Uptime Kuma README

Document Version 1.0.0
