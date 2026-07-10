# Portainer Migration from Docker Run to Docker Compose

**Project:** RevChatham Homelab  
**Category:** Troubleshooting  
**Document Version:** 1.0.0  
**Date:** 2026-07-09

---

# Issue

After migrating Portainer from a standalone `docker run` deployment to a Docker Compose deployment, Portainer presented the initial setup screen and prompted for a new administrator account.

Although the service started successfully, all previously configured users, endpoints, and settings appeared to be missing.

---

# Root Cause

The original Portainer deployment was created using `docker run`.

Docker created a persistent volume named:

```text
portainer_data
```

When Docker Compose was introduced, it automatically created a new project-specific volume:

```text
portainer_portainer_data
```

Since this new volume was empty, Portainer initialized as a fresh installation.

---

# Symptoms

- Administrator setup wizard displayed.
- Existing user accounts were unavailable.
- Existing Docker environments were missing.
- Existing configuration appeared lost.

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

# Lessons Learned

Docker Compose automatically creates project-scoped volumes unless instructed otherwise.

When migrating an existing Docker container into Docker Compose:

1. Identify the original persistent volume.
2. Reuse the existing volume whenever possible.
3. Declare the volume as `external: true` if it already exists.

Failure to do so may result in an application appearing to reset, even though the original data still exists.

---

# Verification

The migration was considered successful after confirming:

- Existing administrator account accessible
- Existing Docker environments present
- Existing configuration restored
- Existing authentication functional

---

# Commands Used

Determine whether the container was created with Docker Compose:

```bash
docker inspect portainer --format='{{ index .Config.Labels "com.docker.compose.project.working_dir" }}'
```

List Docker volumes:

```bash
docker volume ls | grep portainer
```

Inspect existing volumes:

```bash
docker volume inspect portainer_data
```

Restart the Compose deployment:

```bash
docker compose up -d
```

---

Troubleshooting Document v1.0
