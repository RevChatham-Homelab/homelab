# Uptime Kuma Unable to Monitor Portainer After Docker Compose Migration

**Date:** 2026-07-09

## Overview

After migrating Portainer from a standalone `docker run` container to a Docker Compose deployment, Uptime Kuma reported the Portainer service as **Offline**, even though Portainer was fully functional and accessible through the browser.

This document explains the troubleshooting process, root cause, and final resolution.

---

# Environment

- Ubuntu Server
- Docker Engine
- Docker Compose
- Portainer CE
- Uptime Kuma
- Nginx Proxy Manager
- Cloudflare Tunnel

---

# Symptoms

- Portainer accessible through:
  - `https://portainer.revchatham.com`
- Portainer accessible locally in the browser.
- `curl` returned:

```http
HTTP/1.1 200 OK
```

- Uptime Kuma reported:

```
Portainer - Internal
Status: DOWN
```

---

# Initial Investigation

## Verify Portainer was Running

```bash
cd ~/portainer
docker compose ps
```

Confirmed the Portainer container was running.

---

## Verify the Web Server

```bash
curl -I https://localhost:9443 -k
```

Result:

```http
HTTP/1.1 200 OK
```

This confirmed the issue was **not** Portainer itself.

---

## Check Published Ports

```bash
docker ps
```

Relevant output:

```
portainer
9443 -> 9443
9000/tcp
```

Unlike the previous installation, Portainer was **not publishing port 9000 to the host**.

Additionally, Authentik was already using host port 9000.

This meant the original monitor configuration could no longer function correctly.

---

# Docker Network Investigation

Verified existing Docker networks:

```bash
docker network ls
```

Confirmed both containers existed.

Attempted to connect both containers to the shared network:

```bash
docker network connect homelab portainer
docker network connect homelab uptime-kuma
```

Docker returned:

```
endpoint already exists in network homelab
```

This confirmed both containers were already attached to the same Docker network.

---

# Root Cause

The internal monitor was attempting to reach Portainer through the host network using:

```
https://192.168.1.101:9443
```

Although this worked from a browser, it was not the most reliable path for communication between Docker containers.

Since both containers already shared the same Docker bridge network (`homelab`), Docker's internal DNS should be used instead.

---

# Resolution

Updated the Uptime Kuma monitor.

Old URL:

```
https://192.168.1.101:9443
```

New URL:

```
https://portainer:9443
```

Additional setting:

```
✓ Ignore TLS/SSL errors
```

After saving the monitor, Uptime Kuma immediately reported the service as **Online**.

---

# Why This Works

Docker automatically provides internal DNS resolution for containers on the same network.

Instead of routing traffic:

```
Uptime Kuma
        │
        ▼
Host Network
        │
        ▼
Portainer
```

the traffic now follows:

```
Uptime Kuma
        │
        ▼
Docker DNS
        │
        ▼
portainer
```

This avoids unnecessary routing through the host network and follows Docker networking best practices.

---

# Lessons Learned

- Always verify the service itself before troubleshooting monitoring software.
- `curl` is an excellent first step when validating web services.
- Docker Compose deployments may expose different ports than previous `docker run` deployments.
- Container names can be used as hostnames when containers share a Docker network.
- Docker's internal networking is generally preferred over using host IP addresses for container-to-container communication.

---

# Final Recommended Configuration

## Internal Monitor

```
Type: HTTP(s)

URL:
https://portainer:9443

Ignore TLS Errors:
Enabled
```

Purpose:

- Verify Portainer container health.
- Independent of DNS, Cloudflare, or reverse proxy configuration.

---

## External Monitor

```
Type: HTTP(s)

URL:
https://portainer.revchatham.com
```

Purpose:

Verify the complete public access path:

```
Internet
      │
Cloudflare DNS
      │
Cloudflare Tunnel
      │
Nginx Proxy Manager
      │
Portainer
```

This monitor confirms that remote users can successfully access the service.

---

# Outcome

- ✅ Portainer functioning correctly.
- ✅ Internal monitoring restored.
- ✅ External monitoring operational.
- ✅ Docker networking configured according to best practices.
