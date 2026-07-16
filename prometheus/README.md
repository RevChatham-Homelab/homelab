# Prometheus

**Project:** RevChatham Homelab

**Service:** Prometheus

**Document:** Service README

**Document Version:** 1.0.0

**Service Status:** Production

**Last Reviewed:** 2026-07-16

---

# Overview

Prometheus provides centralized metrics collection for the RevChatham Homelab.

It collects metrics from the host operating system and Docker containers while serving as the primary metrics source for Grafana dashboards.

---

# Purpose

Prometheus provides:

- Time-series metrics collection
- Host monitoring
- Docker container monitoring
- Metrics storage
- Grafana integration

---

# Components

| Component | Purpose |
|-----------|---------|
| Prometheus | Metrics collection and storage |
| Node Exporter | Host operating system metrics |
| cAdvisor | Docker container metrics |

---

# Docker Images

| Component | Image | Version |
|-----------|-------|---------|
| Prometheus | `prom/prometheus` | `v3.13.0` |
| Node Exporter | `prom/node-exporter` | `v1.11.1` |
| cAdvisor | `gcr.io/cadvisor/cadvisor` | `v0.55.1` |

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

| Volume / File | Purpose |
|---------------|---------|
| `prometheus_data` | Time-series metrics database |
| `prometheus.yml` | Scrape configuration |

---

# Networking

The monitoring stack connects to the shared Docker network:

```text
homelab
```

Published ports:

```text
9090
9100
```

---

# Security Notes

- Docker image versions are pinned.
- Runtime metrics data is stored in a Docker volume.
- Node Exporter mounts the host filesystem as read-only.
- cAdvisor requires elevated access to collect Docker metrics.
- `.env` is excluded from Git.

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
docs/audits/prometheus.md
```

---

Prometheus README

Document Version 1.0.0
