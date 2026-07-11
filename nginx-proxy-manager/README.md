# Nginx Proxy Manager

**Project:** RevChatham Homelab  
**Service:** Reverse Proxy  
**Status:** Production  
**Version:** 1.0.0  
**Last Updated:** 2026-07-10

---

# Overview

Nginx Proxy Manager provides centralized reverse proxy management for the RevChatham Homelab.

It manages HTTPS certificates, reverse proxy hosts, and external access to homelab services through Cloudflare Tunnel.

---

# Purpose

The service provides:

- Reverse proxy management
- SSL certificate management
- HTTPS termination
- Internal service publishing
- Cloudflare Tunnel integration

---

# Components

| Component | Purpose |
|-----------|---------|
| Nginx Proxy Manager | Reverse proxy and web management |
| SQLite Database | Stores configuration and proxy hosts |
| Let's Encrypt | SSL certificate management |

---

# Docker Images

```text
jc21/nginx-proxy-manager:2.15.1
```

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

Persistent application data:

```text
data/
```

SSL certificates:

```text
letsencrypt/
```

---

# Networking

Docker Network:

```text
homelab
```

Published Ports:

```text
80
81
443
```

Container Name:

```text
nginx-proxy-manager
```

---

# Security Notes

The following are excluded from Git:

```text
.env
data/
letsencrypt/
*.bak
*.log
*.tmp
```

Runtime data and SSL certificates are intentionally excluded from version control.

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
letsencrypt/
```

---

README Template v1.0
