# Proxmox Authentik OIDC Redirect URI Error

**Date:** 2026-07-09

## Overview

After restarting Docker and testing homelab services, Proxmox was accessible using the local PAM login, but logging in through the Authentik OpenID Connect realm failed.

The issue affected the Authentik SSO login flow only. Proxmox itself remained online and accessible through PAM.

## Symptoms

- Proxmox was reachable at:

```text
https://192.168.1.100:8006
```

- PAM login worked.
- Authentik/OIDC login failed.
- Authentik displayed:

```text
Redirect URI Error

The request fails due to a missing, invalid, or mismatching redirection URI (redirect_uri).
```

## What Was Verified

### Proxmox Was Working

Logging in with the PAM realm confirmed that Proxmox itself was functional.

### Authentik Was Running

Docker showed Authentik services running and healthy:

```bash
docker ps
```

Relevant containers:

```text
authentik-server-1
authentik-worker-1
authentik-postgresql-1
```

### Proxmox Realm Existed

The Proxmox shell confirmed the Authentik realm existed:

```bash
pveum realm list
```

Output included:

```text
authentik    openid
pam          pam
pve          pve
```

## Root Cause

The Authentik provider had the wrong allowed redirect URI.

The browser authorization request showed the exact redirect URI Proxmox was sending:

```text
redirect_uri=https%3A%2F%2Fproxmox.revchatham.com
```

Decoded, this equals:

```text
https://proxmox.revchatham.com
```

However, Authentik was configured to allow a different redirect URI, such as:

```text
https://192.168.1.100:8006
```

Because OAuth/OIDC redirect URIs must match exactly, Authentik rejected the login request.

## Resolution

In Authentik, the Proxmox OAuth2/OpenID provider was updated.

Correct redirect URI:

```text
Strict | Authorization | https://proxmox.revchatham.com
```

After saving the provider settings, Proxmox Authentik login worked.

## Final Working Configuration

### Authentik Provider

```text
Redirect URI:
https://proxmox.revchatham.com
```

### Proxmox Realm

```text
Realm:
authentik

Type:
openid

Issuer URL:
https://auth.revchatham.com/application/o/proxmox/

Username claim:
username

Autocreate users:
enabled
```

### Homepage Link

```yaml
href: https://proxmox.revchatham.com
```

## Lessons Learned

- PAM should remain available as the emergency/admin login path.
- Do not troubleshoot SSO by changing multiple settings at once.
- OAuth/OIDC redirect URIs must match exactly.
- The fastest way to solve redirect URI errors is to inspect the browser authorization URL.
- The `redirect_uri=` parameter shows what the client is actually sending.
- Authentik must allow that exact redirect URI.

## Outcome

- Proxmox remained accessible through PAM.
- Authentik OIDC login was restored.
- Homepage Proxmox link works through the public service URL.
- The issue was confirmed as a redirect URI mismatch, not a Docker, Proxmox, or Authentik service failure.
