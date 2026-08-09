# Grafana Observability

**Project:** RevChatham Homelab

**Document ID:** doc-000

**Document:** Grafana Observability README

**Document Version:** 1.0.0

**Last Reviewed:** 2026-08-09

**Status:** Operational

---

# Overview

Grafana is the visualization and exploration interface for the
RevChatham Homelab observability environment.

The `grafana/` repository directory groups the services used to collect,
store, query, and visualize infrastructure metrics and logs. Grafana
provides dashboards and log exploration, Prometheus provides metrics
collection and storage, Loki provides centralized log storage and
querying, and Alloy provides log discovery and forwarding.

The observability services are organized together in the repository
while remaining independently deployable through their respective Docker
Compose files.

------------------------------------------------------------------------

# Purpose

The observability environment provides:

-   Infrastructure dashboards
-   Host operating system metrics
-   Docker container metrics
-   Centralized Docker log collection
-   Recovery Automation log collection
-   Log search and filtering
-   Severity-based log identification
-   Historical troubleshooting data
-   Centralized authentication for Grafana through Authentik

------------------------------------------------------------------------

# Architecture

``` text
                         ┌─────────────┐
                         │   Grafana   │
                         │ Dashboards  │
                         │   Explore   │
                         └──────┬──────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
              ┌────────────┐          ┌──────────┐
              │ Prometheus │          │   Loki   │
              │  Metrics   │          │   Logs   │
              └─────▲──────┘          └────▲─────┘
                    │                      │
          ┌─────────┴─────────┐            │
          │                   │            │
     Node Exporter         cAdvisor       Alloy
        Host               Docker          │
       Metrics             Metrics     ┌────┴─────┐
                                     Docker     Recovery
                                      Logs        Logs
```

------------------------------------------------------------------------

# Repository Structure

``` text
grafana/
├── alloy/
│   ├── compose.yml
│   ├── config.alloy
│   └── README.md
├── docker-compose.yml
├── loki/
│   ├── compose.yml
│   ├── loki-config.yml
│   └── README.md
├── prometheus/
│   ├── compose.yml
│   ├── prometheus.yml
│   └── README.md
└── README.md
```

Runtime secrets and local environment files are excluded from Git.

------------------------------------------------------------------------

# Components

  Component       Purpose
  --------------- --------------------------------------------------------------
  Grafana         Dashboards, visualization, and log exploration
  Prometheus      Metrics collection and time-series storage
  Node Exporter   Host operating system metrics
  cAdvisor        Docker container metrics
  Loki            Centralized log storage and querying
  Alloy           Docker and Recovery Automation log collection and forwarding

------------------------------------------------------------------------

# Docker Images

  Component       Image                        Version
  --------------- ---------------------------- -----------
  Grafana         `grafana/grafana-oss`        `13.0.2`
  Prometheus      `prom/prometheus`            `v3.13.0`
  Node Exporter   `prom/node-exporter`         `v1.11.1`
  cAdvisor        `gcr.io/cadvisor/cadvisor`   `v0.55.1`
  Loki            `grafana/loki`               `3.7.0`
  Alloy           `grafana/alloy`              `v1.18.1`

------------------------------------------------------------------------

# Grafana Configuration

Grafana is deployed from:

``` text
grafana/docker-compose.yml
```

Grafana uses:

-   Host port `3002`
-   Container port `3000`
-   Persistent volume `grafana-data`
-   External Docker network `homelab`
-   Authentik Generic OAuth / OpenID Connect authentication

Secrets and authentication credentials are stored in `.env` and are not
committed to Git.

A sanitized example is maintained in:

``` text
grafana/.env.example
```

------------------------------------------------------------------------

# Metrics Pipeline

Prometheus collects infrastructure metrics from:

-   Node Exporter
-   cAdvisor

Grafana queries Prometheus to display host and Docker container metrics
in dashboards.

Prometheus is maintained under:

``` text
grafana/prometheus/
```

------------------------------------------------------------------------

# Logging Pipeline

Alloy discovers Docker containers through the Docker socket and forwards
Docker logs to Loki.

Alloy also reads Recovery Automation logs from:

``` text
automation/recovery/logs/
automation/recovery/output/RP-*/logs/
```

Recovery Automation logs are labeled so cron execution logs and
individual Recovery Point logs can be queried separately.

Loki stores the collected logs and Grafana provides search, filtering,
visualization, and severity identification.

------------------------------------------------------------------------

# Recovery Automation Integration

Recovery Automation recognizes the observability hierarchy under
`grafana/`.

Recovery Point backups include the repository-safe configuration for:

-   Grafana
-   Alloy
-   Loki
-   Prometheus

Recovery Point `RP-20260809-004` verified that the nested observability
structure was successfully backed up and that Grafana, Alloy, Loki, and
Prometheus passed their backup and Compose-file verification checks.

------------------------------------------------------------------------

# Operational Verification

The observability environment was validated on 2026-08-09 after a Docker
daemon restart.

Verification confirmed:

-   Grafana returned and displayed current metrics.
-   Prometheus returned `Prometheus Server is Ready.`
-   Loki returned `ready` after its normal startup readiness delay.
-   Alloy resumed Docker and Recovery Automation log collection.
-   Grafana Explore successfully queried Loki logs.
-   No new Alloy or Loki error, failure, fatal, or panic entries were
    found during the final post-restart check.

Historical Alloy ingestion errors generated during initial configuration
remain available in Loki for troubleshooting and audit purposes.

------------------------------------------------------------------------

# Security Notes

-   Grafana authentication is integrated with Authentik.
-   Grafana OAuth credentials are stored outside the repository in
    `.env`.
-   Loki is not published directly to a host port.
-   Alloy accesses the Docker socket using a read-only mount.
-   Recovery Automation log directories are mounted read-only into
    Alloy.
-   Repository-safe `.env.example` files contain placeholders rather
    than production secrets.
-   Docker image versions are pinned in repository configuration.

------------------------------------------------------------------------

# Deployment

Each observability component is independently deployable from its own
directory.

Grafana:

``` bash
cd ~/homelab/grafana
docker compose up -d
```

Prometheus:

``` bash
cd ~/homelab/grafana/prometheus
docker compose up -d
```

Loki:

``` bash
cd ~/homelab/grafana/loki
docker compose up -d
```

Alloy:

``` bash
cd ~/homelab/grafana/alloy
docker compose up -d
```

------------------------------------------------------------------------

# Documentation

Component documentation:

``` text
grafana/alloy/README.md
grafana/loki/README.md
grafana/prometheus/README.md
```

Historical audit documentation:

``` text
docs/audits/grafana.md
docs/audits/prometheus.md
```

---

Grafana Observability README v1.0.0
