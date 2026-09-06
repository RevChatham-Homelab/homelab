# Prometheus

**Project:** RevChatham Homelab

**Document ID:** doc-000

**Document:** Prometheus Service README

**Document Version:** 1.1.0

**Last Reviewed:** 2026-09-06

**Status:** Operational

---

# Overview

Prometheus provides centralized metrics collection for the RevChatham
Homelab.

It collects host and Docker container metrics through Node Exporter and
cAdvisor and serves those metrics to Grafana for visualization.

Prometheus is maintained under `grafana/prometheus/` as the metrics
subsystem of the broader observability environment.

------------------------------------------------------------------------

# Purpose

Prometheus provides:

-   Time-series metrics collection
-   Host operating system monitoring
-   Docker container monitoring
-   Metrics storage
-   Grafana metrics integration
-   Site-specific Nginx website-traffic collection for Project Liquid Alert

------------------------------------------------------------------------

# Components

  Component             Purpose
  --------------------- -------------------------------------
  Prometheus            Metrics collection and storage
  Node Exporter         Host operating system metrics
  cAdvisor              Docker container metrics
  Nginx Log Exporter    Site-specific website traffic metrics

------------------------------------------------------------------------

# Docker Images

  Component             Image                                                         Version
  --------------------- ------------------------------------------------------------- -----------
  Prometheus            `prom/prometheus`                                             `v3.13.0`
  Node Exporter         `prom/node-exporter`                                          `v1.11.1`
  cAdvisor              `gcr.io/cadvisor/cadvisor`                                    `v0.55.1`
  Nginx Log Exporter    `quay.io/martinhelmich/prometheus-nginxlog-exporter`           `v1.11.0`

------------------------------------------------------------------------

# Environment Variables

Runtime environment variables are stored in:

``` text
.env
```

A repository-safe example configuration is provided in:

``` text
.env.example
```

The production `.env` file is excluded from Git.

------------------------------------------------------------------------

# Persistent Data

  Volume / File       Purpose
  ------------------- ---------------------------------
  `prometheus_data`   Time-series metrics database
  `prometheus.yml`    Prometheus scrape configuration

------------------------------------------------------------------------

# Networking

Prometheus, Node Exporter, and cAdvisor connect to the shared external
Docker network:

``` text
homelab
```

Published service ports:

  Component       Port
  --------------- --------
  Prometheus      `9090`
  Node Exporter   `9100`

The Nginx log exporter is published only on host loopback:

``` text
127.0.0.1:4040
```

Prometheus reaches the exporter privately through the `homelab` Docker
network at `nginxlog-exporter:4040`.

Grafana accesses Prometheus across the shared Docker network for
dashboard visualization.

------------------------------------------------------------------------

# Security Notes

-   Docker image versions are pinned.
-   Runtime metrics data is stored in a Docker volume.
-   Node Exporter mounts the host filesystem as read-only.
-   cAdvisor requires elevated Docker access to collect container
    metrics.
-   `.env` is excluded from Git.
-   Repository-safe environment examples do not contain production
    secrets.

------------------------------------------------------------------------

# Deployment

Start:

``` bash
cd ~/homelab/grafana/prometheus
docker compose up -d
```

Stop:

``` bash
docker compose down
```

Restart:

``` bash
docker compose restart
```

Update:

``` bash
docker compose pull
docker compose up -d
```

------------------------------------------------------------------------

# Observability Integration

Prometheus is the metrics subsystem of the RevChatham Homelab
observability environment.

The repository groups Prometheus beneath:

``` text
grafana/prometheus/
```

Grafana provides visualization for Prometheus metrics while Loki and
Alloy provide the complementary centralized logging pipeline.

The Prometheus service configuration itself was not changed as part of
the 2026-08-09 repository relocation.

The `nginx_website` scrape job collects site-specific request, response
status, transferred-byte, and origin response-time metrics from the Nginx
log exporter. This job uses a five-second scrape interval to support the
Project Liquid Alert website-traffic card.

------------------------------------------------------------------------

# Recovery Automation Integration

Recovery Automation backs up Prometheus configuration through the nested
Grafana observability hierarchy.

Recovery Point `RP-20260809-004` verified:

-   Prometheus backup creation: `PASS`
-   Prometheus Compose file read test: `PASS`

------------------------------------------------------------------------

# Operational Verification

Following the Docker daemon restart on 2026-08-09:

-   Prometheus restarted successfully.
-   Prometheus returned `Prometheus Server is Ready.`
-   Node Exporter restarted successfully.
-   cAdvisor restarted successfully and reported healthy.
-   Grafana displayed current Node Exporter metrics after the restart.
-   Nginx Log Exporter returned website-specific metrics.
-   Prometheus reported `up{job="nginx_website"}` as `1`.
-   Exporter access-log parse errors remained at `0`.
-   The five-second scrape cadence was verified.

------------------------------------------------------------------------

# Related Documentation

Parent observability documentation:

``` text
grafana/README.md
```

Historical audit documentation:

``` text
docs/audits/prometheus.md
```

---

Prometheus Service README v1.1.0
