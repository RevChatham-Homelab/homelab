# Incident Report

**Project:** RevChatham Homelab

**Document:** Incident Report

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-16

**Status:** Operational

---

**Incident ID:** IR-20260709-002

**Incident Title:** Proxmox Authentik OIDC Redirect URI Error

**Incident Directory:** docs/incidents/2026-07-09/002_authentik-oidc-redirect-uri/

**Incident Date:** 2026-07-09

**Incident Start Time:** Unknown

**Incident End Time:** Unknown

**Incident Status:** Resolved

**Severity:** Medium

---

# Incident Summary

After restarting Docker and validating homelab services, Proxmox remained accessible using the local PAM realm, but authentication through the Authentik OpenID Connect (OIDC) realm failed.

The incident affected only the SSO authentication flow. Proxmox itself remained fully operational.

---

# Environment

- Proxmox VE
- Ubuntu Server
- Authentik
- Docker
- Cloudflare Tunnel
- Homepage Dashboard

---

# Symptoms

- Proxmox reachable at:

```text
https://192.168.1.100:8006
```

- PAM authentication succeeded.
- Authentik/OIDC authentication failed.
- Authentik displayed:

```text
Redirect URI Error

The request fails due to a missing, invalid, or mismatching redirection URI (redirect_uri).
```

---

# Impact

- Single Sign-On (SSO) unavailable for Proxmox.
- Local PAM administration remained fully operational.
- No infrastructure downtime.
- No data loss.
- No impact to other Docker services.

---

# Initial Assessment

Initial investigation suggested either:

- an Authentik configuration issue,
- an OIDC configuration mismatch, or
- a Proxmox realm configuration problem.

Because PAM authentication remained functional, the issue was determined to be isolated to the OIDC authentication flow.

---

# Investigation

## Verify Proxmox Operation

Logging in through the PAM realm confirmed Proxmox itself was operational.

---

## Verify Authentik Services

Docker confirmed Authentik services were running.

```bash
docker ps
```

Relevant containers:

```text
authentik-server-1
authentik-worker-1
authentik-postgresql-1
```

---

## Verify Proxmox Realm

The configured authentication realms were reviewed.

```bash
pveum realm list
```

Output included:

```text
authentik    openid
pam          pam
pve          pve
```

---

## Verify Redirect URI

The browser authorization request was examined.

The request contained:

```text
redirect_uri=https%3A%2F%2Fproxmox.revchatham.com
```

Decoded:

```text
https://proxmox.revchatham.com
```

This did not match the Redirect URI configured within Authentik.

---

# Evidence Collected

- Browser Redirect URI error
- Docker container status
- Proxmox realm configuration
- Browser authorization request
- Authentik provider configuration

---

# Commands Executed

```bash
docker ps

pveum realm list
```

---

# Root Cause

The Authentik provider was configured with an incorrect allowed Redirect URI.

Auth0/OIDC security requires an exact Redirect URI match.

Proxmox requested:

```text
https://proxmox.revchatham.com
```

while Authentik permitted a different URI.

The mismatch caused Authentik to reject the authentication request.

---

# Resolution

The Authentik OAuth2/OpenID Provider was updated.

Correct Redirect URI:

```text
Strict | Authorization | https://proxmox.revchatham.com
```

After saving the provider configuration, authentication through Authentik succeeded.

---

# Verification

Successful verification included:

- PAM authentication remained operational.
- Authentik OIDC authentication succeeded.
- Homepage linked correctly to Proxmox.
- Browser redirect completed successfully.
- Proxmox authenticated through the Authentik realm.

---

# Recovery Point

**Recovery Point Used:** None

**Recovery Required:** No

---

# Lessons Learned

- Maintain PAM as the emergency administrative login.
- Troubleshoot SSO one configuration change at a time.
- OAuth/OIDC Redirect URIs must match exactly.
- Browser authorization URLs provide valuable troubleshooting information.
- The `redirect_uri=` parameter identifies the exact URI being presented by the client.
- Authentik must explicitly allow that exact Redirect URI.

---

# Follow-Up Actions

| Action | Owner | Target Milestone | Status |
|--------|-------|------------------|--------|
| Continue documenting Authentik and OIDC deployment standards. | Project Owner | v0.7.0 | Completed |

---

# Related Documentation

- Authentik Service README
- Authentik Service Audit
- Engineering Principles
- Incident Report Standard

---

# Supporting Files

None.

---

Incident Report v1.0.0
