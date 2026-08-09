# Grafana Alloy

**Project:** RevChatham Homelab

**Document ID:** doc-000

**Document:** Grafana Alloy Service README

**Document Version:** 1.0.0

**Last Reviewed:** 2026-08-09

**Status:** Operational

---

# Overview

Grafana Alloy is the log collection and forwarding service for the
RevChatham Homelab observability environment.

Alloy discovers Docker containers, collects their logs, reads Recovery
Automation logs from the host filesystem, applies identifying labels,
and forwards the resulting log streams to Loki.

------------------------------------------------------------------------

# Purpose

Alloy provides:

-   Docker container discovery
-   Docker log collection
-   Recovery Automation log collection
-   Log stream labeling
-   Forwarding of logs to Loki
-   Persistent Alloy runtime state

------------------------------------------------------------------------

# Components

  Component           Purpose
  ------------------- ----------------------------------------
  Docker Discovery    Discovers running Docker containers
  Docker Log Source   Collects Docker container logs
  File Log Source     Collects Recovery Automation logs
  Relabeling          Adds useful container and image labels
  Loki Writer         Sends collected logs to Loki

------------------------------------------------------------------------

# Docker Image

  Component   Image             Version
  ----------- ----------------- -----------
  Alloy       `grafana/alloy`   `v1.18.1`

------------------------------------------------------------------------

# Configuration

Alloy configuration is stored in:

``` text
grafana/alloy/config.alloy
```

The Docker deployment is stored in:

``` text
grafana/alloy/compose.yml
```

The configuration defines two primary log sources:

-   Docker container logs
-   Recovery Automation logs

------------------------------------------------------------------------

# Docker Log Collection

Alloy discovers containers through:

``` text
unix:///var/run/docker.sock
```

Docker log streams receive identifying labels including:

-   `job="docker"`
-   `container`
-   `image`

Docker logs are processed and forwarded to Loki.

------------------------------------------------------------------------

# Recovery Automation Log Collection

Alloy reads the Recovery Automation scheduler log from:

``` text
/var/log/recovery/cron.log
```

It also reads individual Recovery Point execution logs from:

``` text
/var/log/recovery-points/RP-*/logs/recovery.log
```

These paths correspond to read-only host mounts from:

``` text
/home/angel/homelab/automation/recovery/logs
/home/angel/homelab/automation/recovery/output
```

Recovery Automation streams use:

``` text
job="recovery-automation"
```

and are distinguished with:

``` text
log_type="cron"
log_type="recovery-point"
```

------------------------------------------------------------------------

# Loki Integration

Alloy forwards collected logs to:

``` text
http://loki:3100/loki/api/v1/push
```

Alloy and Loki communicate over the shared external Docker network:

``` text
homelab
```

------------------------------------------------------------------------

# Persistent Data

  Volume         Purpose
  -------------- ---------------------
  `alloy-data`   Alloy runtime state

Alloy stores its runtime state at:

``` text
/var/lib/alloy/data
```

------------------------------------------------------------------------

# Security Notes

-   The Docker socket is mounted read-only.
-   Recovery Automation log directories are mounted read-only.
-   Alloy does not require a host-published application port for the
    current logging workflow.
-   Alloy communicates with Loki through the internal `homelab` Docker
    network.
-   The repository configuration pins Alloy to the tested `v1.18.1`
    release.

------------------------------------------------------------------------

# Deployment

Start:

``` bash
cd ~/homelab/grafana/alloy
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

Alloy was operationally verified on 2026-08-09.

Verification confirmed:

-   Docker logs were visible through Grafana and Loki.
-   Recovery Automation cron logs were visible through Grafana and Loki.
-   Recovery Point execution logs were visible through Grafana and Loki.
-   Severity information from Recovery Automation could be identified in
    Grafana.
-   Alloy resumed log collection after Docker restart.
-   No new Alloy error, failure, fatal, or panic entries were found
    during the final post-restart check.

Historical `entry too far behind` ingestion errors from initial setup
remain searchable in Loki as historical troubleshooting evidence.

------------------------------------------------------------------------

# Related Documentation

``` text
grafana/README.md
grafana/loki/README.md
automation/recovery/
```

---

Grafana Alloy Service README v1.0.0
