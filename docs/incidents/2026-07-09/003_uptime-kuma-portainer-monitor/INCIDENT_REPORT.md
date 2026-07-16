# Incident Report

**Project:** RevChatham Homelab

**Document:** Incident Report

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-16

**Status:** Operational

---

**Incident ID:** IR-20260709-003

**Incident Title:** Uptime Kuma Unable to Monitor Portainer After Docker Compose Migration

**Incident Directory:** docs/incidents/2026-07-09/003_uptime-kuma-portainer-monitor/

**Incident Date:** 2026-07-09

**Incident Start Time:** Unknown

**Incident End Time:** Unknown

**Incident Status:** Resolved

**Severity:** Low

---

# Incident Summary

After migrating Portainer from a standalone `docker run` deployment to Docker Compose, Uptime Kuma reported the Portainer service as **Offline**, even though Portainer remained fully operational and accessible.

The incident affected only monitoring accuracy. No production service outage occurred.

---

# Environment

- Ubuntu Server
- Docker Engine
- Docker Compose
- Portainer Community Edition
- Uptime Kuma
- Nginx Proxy Manager
- Cloudflare Tunnel

---

# Symptoms

- Portainer accessible through:
  - `https://portainer.revchatham.com`
- Portainer accessible locally.
- `curl` returned:

```http
HTTP/1.1 200 OK
```

- Uptime Kuma reported:

```text
Portainer - Internal
Status: DOWN
```

---

# Impact

- False monitoring alert generated.
- Portainer service remained operational.
- Public access unaffected.
- Administrative access unaffected.
- No data loss.

---

# Initial Assessment

The initial assumption was that either:

- Portainer was unavailable,
- Docker networking had changed during migration, or
- the monitor configuration was no longer valid after migrating to Docker Compose.

---

# Investigation

## Verify Portainer Operation

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

This confirmed the issue was not Portainer itself.

---

## Verify Published Ports

```bash
docker ps
```

Relevant output:

```text
9443 -> 9443
9000/tcp
```

Port 9000 was no longer published to the host.

Authentik was already using host port 9000.

---

## Verify Docker Networking

Existing Docker networks were reviewed.

```bash
docker network ls
```

Container connectivity was verified.

```bash
docker network connect homelab portainer
docker network connect homelab uptime-kuma
```

Docker returned:

```text
endpoint already exists in network homelab
```

confirming both containers were already connected to the shared Docker bridge network.

---

# Evidence Collected

- Docker Compose status
- Docker published ports
- Docker network configuration
- HTTP response validation
- Uptime Kuma monitor status

---

# Commands Executed

```bash
cd ~/portainer
docker compose ps

curl -I https://localhost:9443 -k

docker ps

docker network ls

docker network connect homelab portainer

docker network connect homelab uptime-kuma
```

---

# Root Cause

The internal monitor attempted to communicate with Portainer using the host network.

```text
https://192.168.1.101:9443
```

Although functional, this path was unnecessary.

Because both containers already shared the Docker bridge network (`homelab`), Docker's internal DNS provided a more reliable communication path.

---

# Resolution

The internal Uptime Kuma monitor was updated.

Old URL:

```text
https://192.168.1.101:9443
```

New URL:

```text
https://portainer:9443
```

Additional setting:

```text
Ignore TLS/SSL Errors: Enabled
```

The monitor immediately reported the service as **Online**.

---

# Verification

Successful verification included:

- Portainer accessible locally.
- Portainer accessible publicly.
- Internal monitor reported Online.
- External monitor remained operational.
- Docker networking validated.

---

# Recovery Point

**Recovery Point Used:** None

**Recovery Required:** No

---

# Lessons Learned

- Verify the application before troubleshooting monitoring software.
- `curl` is an effective first validation tool.
- Docker Compose may expose services differently than `docker run`.
- Docker container names should be used for container-to-container communication whenever possible.
- Docker internal DNS is preferred over host networking for internal service communication.

---

# Final Recommended Configuration

## Internal Monitor

```text
Type: HTTP(s)

URL:
https://portainer:9443

Ignore TLS Errors:
Enabled
```

Purpose:

- Monitor Portainer container health.
- Independent of DNS, Cloudflare, and reverse proxy availability.

---

## External Monitor

```text
Type: HTTP(s)

URL:
https://portainer.revchatham.com
```

Purpose:

Validate the complete public access path.

---

# Follow-Up Actions

| Action | Owner | Target Milestone | Status |
|--------|-------|------------------|--------|
| Continue documenting Docker networking best practices. | Project Owner | v0.7.0 | Completed |

---

# Related Documentation

- Portainer Service README
- Portainer Service Audit
- Docker Backup Procedure
- Incident Report Standard

---

# Supporting Files

None.

---

Incident Report v1.0.0
