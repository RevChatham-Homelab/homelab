# Grafana Loki

**Project:** RevChatham Homelab

**Document ID:** doc-000

**Document:** Grafana Loki Service README

**Document Version:** 1.0.0

**Last Reviewed:** 2026-08-09

**Status:** Operational

---

# Overview

Grafana Loki provides centralized log storage and querying for the
RevChatham Homelab observability environment.

Alloy forwards Docker and Recovery Automation logs to Loki. Grafana
queries Loki so logs can be searched, filtered, visualized, and used
during troubleshooting.

------------------------------------------------------------------------

# Purpose

Loki provides:

-   Centralized log storage
-   Log querying
-   Docker log retention
-   Recovery Automation log retention
-   Grafana log data source functionality
-   Historical troubleshooting evidence

------------------------------------------------------------------------

# Docker Image

  Component   Image            Version
  ----------- ---------------- ---------
  Loki        `grafana/loki`   `3.7.0`

------------------------------------------------------------------------

# Configuration

Loki configuration is stored in:

``` text
grafana/loki/loki-config.yml
```

The Docker deployment is stored in:

``` text
grafana/loki/compose.yml
```

Loki listens internally on:

``` text
3100
```

The service is not directly published to a host port in the current
deployment.

------------------------------------------------------------------------

# Storage

Loki uses filesystem-backed storage with TSDB indexing.

Configuration includes:

-   Filesystem object storage
-   TSDB store
-   Schema `v13`
-   24-hour index period
-   Replication factor `1`
-   In-memory ring suitable for the current single-instance deployment

Persistent Loki data is stored in:

``` text
/loki
```

through the Docker volume:

``` text
loki-data
```

------------------------------------------------------------------------

# Networking

Loki connects to the shared external Docker network:

``` text
homelab
```

Alloy forwards logs to Loki at:

``` text
http://loki:3100/loki/api/v1/push
```

Grafana queries Loki over the Docker network.

------------------------------------------------------------------------

# Authentication

Loki application authentication is disabled in the current
configuration:

``` text
auth_enabled: false
```

This configuration is used with Loki kept on the internal Docker network
and without a directly published host port.

------------------------------------------------------------------------

# Deployment

Start:

``` bash
cd ~/homelab/grafana/loki
docker compose up -d
```

Restart:

``` bash
docker compose restart
```

Stop:

``` bash
docker compose down
```

Validate configuration:

``` bash
docker compose config
```

------------------------------------------------------------------------

# Verification

Loki was operationally verified on 2026-08-09.

Verification confirmed:

-   Loki reached the `ready` state.
-   Loki resumed normally after Docker restart.
-   Grafana successfully queried Loki logs.
-   Docker logs collected by Alloy were searchable.
-   Recovery Automation logs collected by Alloy were searchable.
-   No new Loki error, failure, fatal, or panic entries were found
    during the final post-restart check.

During startup, Loki may temporarily report that the ingester is waiting
after becoming ready. The service subsequently returned `ready` during
verification.

Historical log entries generated during troubleshooting remain available
for later analysis.

------------------------------------------------------------------------

# Security Notes

-   Loki is not directly published to a host port.
-   Loki communicates with Alloy and Grafana over the shared Docker
    network.
-   Persistent log data is stored in a Docker volume.
-   The Docker image is pinned to version `3.7.0`.

------------------------------------------------------------------------

# Related Documentation

``` text
grafana/README.md
grafana/alloy/README.md
```

---

Grafana Loki Service README v1.0.0
