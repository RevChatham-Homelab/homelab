# Incident Report

**Project:** RevChatham Homelab

**Document:** Incident Report

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-16

**Status:** Operational

---

**Incident ID:** IR-20260709-001

**Incident Title:** Portainer Migration from Docker Run to Docker Compose

**Incident Date:** 2026-07-09

**Incident Directory:** docs/incidents/2026-07-09/001_portainer-compose-migration/

**Severity:** Medium

**Incident Status:** Resolved

---

# Incident Summary

After migrating Portainer from a standalone `docker run` deployment to a Docker Compose deployment, Portainer presented the initial setup screen and prompted for a new administrator account.

Although the service started successfully, all previously configured users, endpoints, and settings appeared to be missing.

---

# Environment

- Ubuntu Server
- Docker Engine
- Docker Compose
- Portainer Community Edition

---

# Symptoms

- Administrator setup wizard displayed.
- Existing user accounts were unavailable.
- Existing Docker environments were missing.
- Existing configuration appeared lost.

---

# Impact

- Portainer administration temporarily unavailable.
- Existing configuration appeared to be lost.
- No data loss occurred.
- No other Docker services were affected.

---

# Initial Assessment

The migration appeared to have created a fresh Portainer installation instead of reusing the existing configuration.

The initial concern was that the existing Portainer database had been lost during the migration.

---

# Investigation

The existing Portainer container was inspected.

The deployment was confirmed to have been created outside Docker Compose because the following command returned no working directory:

```bash
docker inspect portainer --format='{{ index .Config.Labels "com.docker.compose.project.working_dir" }}'
```

The available Docker volumes were then reviewed:

```bash
docker volume ls | grep portainer
```

This revealed two volumes:

```text
portainer_data
portainer_portainer_data
```

The original deployment was using `portainer_data`.

Docker Compose had created `portainer_portainer_data`.

---

# Root Cause

The original Portainer deployment was created using `docker run`.

Docker automatically created the persistent volume:

```text
portainer_data
```

When Docker Compose was introduced, it automatically created a new project-specific volume:

```text
portainer_portainer_data
```

Since the new volume was empty, Portainer initialized as a fresh installation rather than using the existing database.

---

# Resolution

The Docker Compose configuration was updated to reference the original Docker volume as an external volume.

```yaml
volumes:
  portainer_data:
    external: true
```

The service was then recreated.

Portainer immediately recognized the existing database and restored:

- Administrator account
- Authentication configuration
- Docker environments
- Application settings
- Historical data

No data was lost.

---

# Verification

The incident was considered resolved after confirming:

- Existing administrator account accessible.
- Existing Docker environments present.
- Existing configuration restored.
- Existing authentication functional.
- Portainer operating normally after restart.

---

# Commands Executed

Determine whether the container was created with Docker Compose:

```bash
docker inspect portainer --format='{{ index .Config.Labels "com.docker.compose.project.working_dir" }}'
```

List Docker volumes:

```bash
docker volume ls | grep portainer
```

Inspect the existing volume:

```bash
docker volume inspect portainer_data
```

Restart the Docker Compose deployment:

```bash
docker compose up -d
```

---

# Recovery Point

**Recovery Point Used:** None

**Recovery Required:** No

---

# Lessons Learned

- Docker Compose automatically creates project-scoped volumes unless instructed otherwise.
- Existing Docker volumes should always be identified before migrating applications to Docker Compose.
- Existing volumes should be declared as `external: true` when reused.
- An application appearing to reset does not necessarily indicate data loss.

---

# Follow-Up Actions

| Action | Owner | Target Milestone | Status |
|--------|-------|------------------|--------|
| Continue documenting Docker migration procedures. | Project Owner | v0.7.0 | Completed |

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
