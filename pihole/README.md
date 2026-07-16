# Pi-hole

**Project:** RevChatham Homelab

**Service:** Pi-hole

**Document:** Service README

**Document Version:** 1.0.0

**Service Status:** Production

**Last Reviewed:** 2026-07-16

---

# Overview

Pi-hole provides network-wide DNS filtering and advertisement blocking for the RevChatham Homelab. It serves as the primary DNS server for the network, improving privacy, reducing unwanted traffic, and providing centralized DNS management.

---

# Purpose

Pi-hole provides:

- Network-wide advertisement blocking
- DNS filtering
- Local DNS resolution
- Query logging and analytics
- Network privacy enhancements

---

# Components

| Component | Purpose |
|-----------|---------|
| Pi-hole | DNS filtering and ad blocking |

---

# Docker Images

| Component | Image | Version |
|-----------|-------|---------|
| Pi-hole | `pihole/pihole` | `v6.4.3` |

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
| etc-pihole/ | DNS configuration, gravity database, query history, and application settings |
| etc-dnsmasq.d/ | Custom DNSMasq configuration |

---

# Networking

Pi-hole connects to the shared Docker network:

```text
homelab
```

The service exposes DNS on port **53** and the web administration interface through Docker port mapping.

---

# Security Notes

- Pi-hole web credentials are stored in `.env`.
- `.env` is excluded from Git.
- Docker image version is pinned.
- Persistent DNS data is stored outside the container.
- Runtime configuration is separated from repository documentation.

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
docs/audits/pihole.md
```

---

Pi-hole README

Document Version 1.0.0
