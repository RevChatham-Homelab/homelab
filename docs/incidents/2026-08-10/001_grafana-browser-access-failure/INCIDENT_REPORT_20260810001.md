# Incident Report

**Project:** RevChatham Homelab

**Document:** Incident Report

**Document Version:** 1.0.0

**Last Reviewed:** 2026-08-10

**Status:** Operational

**Incident ID:** IR-20260810-001

**Incident Title:** Grafana Browser Access Failure

**Incident Directory:** docs/incidents/2026-08-10/001_grafana-browser-access-failure/

**Incident Date:** 2026-08-10

**Incident Start Time:** Unknown

**Incident End Time:** 23:52 EDT

**Incident Status:** Resolved

**Severity:** Low

---

# Incident Summary

Browser access to the externally published Grafana service failed while the Grafana application, Docker container, Cloudflare Tunnel, TLS certificate, and Cloudflare Access endpoint remained operational.

Attempts to access `grafana.revchatham.com` through Brave and Firefox produced SSL/TLS protocol errors.

Command-line testing from both the Ubuntu Server and the Pop!_OS workstation successfully established TLS connections to the same hostname and received the expected Cloudflare Access redirect.

The incident was resolved after updating Pi-hole gravity. Browser access to Grafana was restored immediately afterward.

---

# Environment

- Grafana
- Docker
- Ubuntu Server
- Pop!_OS
- Cloudflare Tunnel
- Cloudflare Access
- Pi-hole
- Tailscale
- Brave
- Firefox

---

# Symptoms

Browser access to Grafana failed.

Brave reported:

`ERR_SSL_PROTOCOL_ERROR`

Firefox reported:

`SSL_ERROR_RX_RECORD_TOO_LONG`

The failure occurred when accessing:

`grafana.revchatham.com`

Grafana remained accessible locally through its published Docker port.

---

# Impact

- External browser access to Grafana was temporarily unavailable from the Pop!_OS workstation.
- Grafana itself remained operational.
- Grafana monitoring data and application availability were not shown to be affected.
- Cloudflare Tunnel remained operational.
- Other observed homelab services remained available.

---

# Initial Assessment

Initial investigation considered several possible failure points:

- Grafana container failure.
- Incorrect Grafana port mapping.
- Cloudflare Tunnel failure.
- Incorrect Cloudflare Tunnel ingress configuration.
- TLS certificate failure.
- Cloudflare Access failure.
- IPv6 connectivity.
- Local proxy configuration.
- DNS resolution.
- Browser-specific HTTPS behavior.

Testing was performed before making configuration changes.

---

# Investigation

The Grafana Docker container was verified as running:

```bash
docker ps --filter name=grafana --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

```

The Grafana container was operational, and local access to the application remained available.

Command-line HTTPS testing from Ubuntu Server and the Pop!_OS workstation successfully established TLS connections to `grafana.revchatham.com` and received the expected Cloudflare Access redirect.

These findings indicated that the application and externally published endpoint remained reachable, despite the browser errors.

---

# Root Cause

The precise underlying cause was not conclusively established.

The available evidence pointed toward a local DNS or filtering-related issue involving Pi-hole rather than a Grafana application failure.

Updating Pi-hole gravity immediately preceded restoration of browser access. This establishes a strong operational association but does not independently prove the exact failure mechanism.

---

# Resolution

Pi-hole gravity was updated.

Following the update, browser access to `grafana.revchatham.com` was restored.

No Grafana application repair was documented as necessary to resolve this incident.

---

# Verification

- Grafana remained operational during investigation.
- Command-line HTTPS connections succeeded.
- Cloudflare Access returned the expected redirect.
- Browser access was restored following the Pi-hole gravity update.
- Incident recorded as resolved at 23:52 EDT on 2026-08-10.

---

# Lessons Learned

- Browser TLS errors do not necessarily indicate a server-side TLS failure.
- Compare browser behavior with command-line HTTPS testing.
- Verify application, tunnel, and authentication availability before modifying server configuration.
- Include local DNS and filtering services in troubleshooting.

---

# Follow-Up Actions

- [ ] Capture DNS and browser diagnostic evidence if the problem recurs.
- [ ] Review Pi-hole filtering behavior during any recurrence.
- [ ] Document the precise failure mechanism if subsequently established.

---

# Outcome

Grafana browser access was restored.

The incident is closed as resolved, with the exact underlying cause remaining unconfirmed.

