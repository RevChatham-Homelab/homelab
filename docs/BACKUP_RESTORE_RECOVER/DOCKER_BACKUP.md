# Docker Backup Procedure

**Project:** RevChatham Homelab

**Document:** Docker Backup Procedure

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-16

**Status:** Operational

---

# Purpose

This document defines the approved procedure for creating, verifying, and documenting Docker service backups within the RevChatham Homelab.

The procedure preserves service configuration and persistent application data required to restore Docker services as part of an approved Recovery Point.

---

# Scope

This procedure applies to Docker services hosted by the Ubuntu Server VM.

The procedure covers:

- Docker Compose files
- Environment files
- Service documentation
- Bind-mounted configuration
- Bind-mounted persistent data
- Docker named volumes
- Container state records
- Docker network and volume inventories
- Backup integrity verification
- Recovery Point documentation

This procedure does not replace the Proxmox VM backup.

---

# Backup Philosophy

Docker services are backed up individually whenever practical.

Each service should be capable of being restored independently without requiring restoration of unrelated services.

Every Docker backup shall belong to an approved Recovery Point.

A backup is not considered complete until:

- The required archives have been created.
- Archive readability has been verified.
- SHA-256 checksums have been generated.
- SHA-256 verification has completed successfully.
- The backup has been documented.

---

# Preconditions

Before beginning the Docker backup procedure, verify:

- Backup media is connected and mounted.
- The target Recovery Point exists.
- Sufficient storage is available on the backup media.
- Docker Engine is operational.
- Production container status has been reviewed.
- No Docker maintenance or migration is currently in progress.
- The Git repository is committed and synchronized.
- The operator has permission to read all required service data.
- A maintenance window has been approved if services must be stopped.

Do not continue until failed prerequisites have been resolved or documented.

---

# Recovery Point Variables

Set the Recovery Point paths before running the backup commands.

Example:

```bash
RP="/mnt/homelabbrr/RevChatham-Homelab/Recovery_Points/RP-20260716-001"
DOCKER_BACKUP="$RP/docker"
DOCKER_VERIFY="$RP/verification"
```

Create the required directories:

```bash
mkdir -p "$DOCKER_BACKUP" "$DOCKER_VERIFY"
```

Confirm the variables:

```bash
printf 'Recovery Point: %s\nDocker Backup: %s\nVerification: %s\n' \
"$RP" "$DOCKER_BACKUP" "$DOCKER_VERIFY"
```

Confirm that the backup media is mounted:

```bash
findmnt /mnt/homelabbrr
```

Confirm available storage:

```bash
df -h "$RP"
```

---

# Production Services

Current production Docker services include:

| Service | Primary Directory | Backup Requirement |
|---------|-------------------|--------------------|
| Homepage | `/home/angel/homepage` | Required |
| Authentik | `/home/angel/authentik` | Required |
| Grafana | `/home/angel/grafana` | Required |
| Prometheus | `/home/angel/prometheus` | Required |
| Pi-hole | `/home/angel/pihole` | Required |
| Portainer | `/home/angel/portainer` | Required |
| Uptime Kuma | `/home/angel/uptime-kuma` | Required |
| Nginx Proxy Manager | `/home/angel/nginx-proxy-manager` | Required |
| Portfolio Website | `/home/angel/website` | Required when present |

The service inventory shall be compared against the active Docker deployment before every backup.

---

# Production Inventory Verification

Before creating backup archives, compare the documented service inventory against the active Docker environment.

Record active containers:

```bash
docker ps --format \
'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
```

Record all containers, including stopped containers:

```bash
docker ps -a --format \
'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
```

Record all named volumes:

```bash
docker volume ls
```

Record all container mounts:

```bash
docker inspect \
$(docker ps -aq) \
--format '{{.Name}} {{range .Mounts}}{{.Type}}:{{.Name}}:{{.Source}}:{{.Destination}} {{end}}'
```

The operator shall identify:

- Production containers
- Supporting production containers
- Disposable or test containers
- Active production named volumes
- Legacy or unused named volumes
- Bind-mounted service data
- Stateful services requiring consistency handling

The active mount inventory determines whether a named volume is part of the production backup scope.

Objects that are not part of the production deployment shall be excluded and documented in `BACKUP_MANIFEST.md`.

Current known exclusions include:

- `serene_margulis` — exited `hello-world` test container without persistent data
- `portainer_portainer_data` — unused Portainer migration volume

---

# Data Consistency

Configuration files may generally be archived while services are running.

Persistent application data may change while an archive is being created. Archiving actively changing databases or application data may produce an inconsistent backup.

Before backing up stateful application data:

1. Identify the service and its persistent storage.
2. Determine whether an application-native export is required.
3. Stop or pause the affected service when necessary.
4. Create the archive.
5. Restart the service.
6. Verify normal operation.

Examples of stateful components include:

- PostgreSQL databases
- SQLite databases
- Application databases
- Authentication data
- Monitoring databases
- Container-management databases

The service interruption and restart shall be documented in the Docker Backup Manifest.

---

# Phase 1 — Preparation

## Verify Docker

```bash
docker version
docker compose version
```

## Record Container State

```bash
docker ps --format \
'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' \
> "$DOCKER_VERIFY/docker-container-state.txt"
```

Record all containers, including stopped containers:

```bash
docker ps -a --format \
'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' \
> "$DOCKER_VERIFY/docker-all-container-state.txt"
```

## Record Docker Networks

```bash
docker network ls \
> "$DOCKER_VERIFY/docker-networks.txt"
```

## Record Docker Volumes

```bash
docker volume ls \
> "$DOCKER_VERIFY/docker-volumes.txt"
```

## Record Container Mounts

```bash
docker inspect \
$(docker ps -aq) \
--format '{{.Name}} {{range .Mounts}}{{.Type}}:{{.Name}}:{{.Source}}:{{.Destination}} {{end}}' \
> "$DOCKER_VERIFY/docker-mount-inventory.txt"
```

If no containers exist, document that condition instead of running `docker inspect` with an empty container list.

Review the mount inventory before creating archives:

```bash
cat "$DOCKER_VERIFY/docker-mount-inventory.txt"
```

---

# Phase 2 — Service Directory Archives

Navigate to the user's home directory:

```bash
cd /home/angel
```

Create one archive for each existing production service directory:

```bash
for service in \
homepage \
authentik \
grafana \
prometheus \
pihole \
portainer \
uptime-kuma \
nginx-proxy-manager \
website
do
    if [ -d "/home/angel/$service" ]; then
        sudo tar -czf \
        "$DOCKER_BACKUP/${service}.tar.gz" \
        -C /home/angel \
        "$service"

        sudo chown angel:angel \
        "$DOCKER_BACKUP/${service}.tar.gz"

        printf 'CREATED: %s\n' "${service}.tar.gz" \
        | tee -a "$DOCKER_VERIFY/docker-backup-results.txt"
    else
        printf 'SKIPPED: /home/angel/%s does not exist\n' "$service" \
        | tee -a "$DOCKER_VERIFY/docker-backup-warnings.txt"
    fi
done
```

This phase protects service directories, including applicable:

- Compose files
- Environment files
- Documentation
- Bind-mounted configuration
- Bind-mounted persistent data stored beneath the service directory

Secrets required for restoration may be included on approved backup media but shall not be committed to GitHub.

---

# Phase 3 — Docker Named Volumes

Named volumes are not necessarily contained within service directories.

Only named volumes that are required by the active production deployment shall be included in the Recovery Point.

The container mount inventory is the authoritative source for determining which named volumes are actively referenced.

Review the recorded mount inventory:

```bash
cat "$DOCKER_VERIFY/docker-mount-inventory.txt"
```

List every Docker volume:

```bash
docker volume ls
```

Identify containers using each volume:

```bash
for volume in $(docker volume ls -q)
do
    echo "=================================================="
    echo "Volume: $volume"

    docker ps -a \
    --filter volume="$volume" \
    --format 'Container={{.Names}} Image={{.Image}} Status={{.Status}}'
done
```

Classify each named volume as:

- Active production volume
- Legacy volume
- Orphaned volume
- Unknown pending investigation

Unknown volumes shall remain unknown until verified.

The current active production named volumes are:

| Volume | Service | Required |
|--------|---------|:--------:|
| `authentik_database` | Authentik PostgreSQL | Yes |
| `grafana_grafana-data` | Grafana | Yes |
| `portainer_data` | Portainer | Yes |
| `prometheus_prometheus_data` | Prometheus | Yes |

The following known legacy volume is excluded:

| Volume | Reason |
|--------|--------|
| `portainer_portainer_data` | Unused volume created during the Portainer Docker Compose migration |

For each required named volume, use:

```bash
docker run --rm \
-v VOLUME_NAME:/source:ro \
-v "$DOCKER_BACKUP":/backup \
alpine \
tar -czf /backup/VOLUME_NAME-volume.tar.gz -C /source .
```

Replace `VOLUME_NAME` with the exact Docker volume name.

Example:

```bash
docker run --rm \
-v portainer_data:/source:ro \
-v "$DOCKER_BACKUP":/backup \
alpine \
tar -czf /backup/portainer_data-volume.tar.gz -C /source .
```

Do not assume every volume returned by `docker volume ls` belongs in the backup.

Named volumes containing actively changing data shall follow the Data Consistency requirements defined in this procedure.

All included and excluded volumes shall be recorded in `BACKUP_MANIFEST.md`.

---

# Phase 4 — Archive Verification

List the created archives:

```bash
find "$DOCKER_BACKUP" \
-maxdepth 1 \
-type f \
-name '*.tar.gz' \
-printf '%f\n' \
| sort
```

Test every archive:

```bash
for archive in "$DOCKER_BACKUP"/*.tar.gz
do
    [ -e "$archive" ] || continue

    if tar -tzf "$archive" >/dev/null; then
        printf 'PASS: %s\n' "$(basename "$archive")"
    else
        printf 'FAIL: %s\n' "$(basename "$archive")"
    fi
done | tee "$DOCKER_VERIFY/docker-archive-read-test.txt"
```

Every required archive must report:

```text
PASS
```

Review the results:

```bash
cat "$DOCKER_VERIFY/docker-archive-read-test.txt"
```

---

# Phase 5 — SHA-256 Verification

Navigate to the Docker backup directory:

```bash
cd "$DOCKER_BACKUP"
```

Generate checksums:

```bash
sha256sum *.tar.gz \
> docker-backups.sha256
```

Verify the checksums:

```bash
sha256sum -c docker-backups.sha256 \
| tee "$DOCKER_VERIFY/docker-checksum-verification.txt"
```

Every archive must report:

```text
OK
```

Review the results:

```bash
cat "$DOCKER_VERIFY/docker-checksum-verification.txt"
```

---

# Phase 6 — Backup Manifest

Create the following file on the backup media:

```text
docker/BACKUP_MANIFEST.md
```

The manifest shall record:

- Recovery Point ID
- Backup date
- Backup start time
- Backup completion time
- Operator
- Services included
- Service directories archived
- Named volumes archived
- Application-native exports created
- Services stopped during backup
- Services restarted after backup
- Files intentionally excluded
- Warnings or skipped services
- Archive verification results
- SHA-256 verification results
- Operator notes

The manifest documents the Docker portion of the Recovery Point.

---

# Required Backup Contents

The Docker backup directory should contain applicable files resembling:

```text
docker/
├── BACKUP_MANIFEST.md
├── authentik.tar.gz
├── grafana.tar.gz
├── homepage.tar.gz
├── nginx-proxy-manager.tar.gz
├── pihole.tar.gz
├── portainer.tar.gz
├── prometheus.tar.gz
├── uptime-kuma.tar.gz
├── website.tar.gz
├── named-volume archives when required
└── docker-backups.sha256
```

Only existing and applicable services shall be included.

The verification directory should contain applicable evidence resembling:

```text
verification/
├── docker-all-container-state.txt
├── docker-archive-read-test.txt
├── docker-backup-results.txt
├── docker-backup-warnings.txt
├── docker-checksum-verification.txt
├── docker-container-state.txt
├── docker-mount-inventory.txt
├── docker-networks.txt
└── docker-volumes.txt
```

---

# Exclusions

The following may be excluded when they are not required for recovery:

- Temporary files
- Cache files
- Rotated runtime logs
- Docker images that can be retrieved again
- Disposable test containers without persistent data
- Unused or orphaned Docker volumes
- Legacy volumes no longer referenced by production containers
- Duplicate backup artifacts
- Recovery Point documentation stored elsewhere
- Proxmox VM backups

Current known exclusions include:

| Object | Type | Reason |
|--------|------|--------|
| `serene_margulis` | Container | Exited `hello-world` test container with no persistent mounts |
| `portainer_portainer_data` | Named volume | Legacy migration volume not referenced by any active container |

Every exclusion shall be verified before the backup and recorded in `BACKUP_MANIFEST.md`.

Secrets shall not be excluded when required for restoration, but they must remain protected on approved backup media and must never be committed to GitHub.

---

# Failure Handling

If any archive or checksum verification fails:

1. Do not mark the Docker backup complete.
2. Record the failure in the verification evidence.
3. Identify the affected service or volume.
4. Correct the underlying issue.
5. Recreate the failed archive.
6. Repeat archive verification.
7. Repeat SHA-256 verification.
8. Update the Backup Manifest.
9. Update the Recovery Point documentation.

Unknown or failed results shall not be recorded as successful.

---

# Restore Procedure

Docker services should be restored only after the following are operational:

1. Proxmox Host
2. Ubuntu Server VM
3. Storage
4. Networking
5. Docker Engine
6. Shared Docker networks

Individual services shall then be restored according to:

- System Recovery Manual
- Restore Procedures
- Service README documentation
- Applicable service-specific procedures

---

# Recovery Validation

A restored Docker service is considered operational only after verifying:

- Compose configuration is present.
- Required environment files are present.
- Persistent data is accessible.
- Containers start successfully.
- Container health checks pass.
- Authentication works where applicable.
- Internal service communication works.
- Public access works where applicable.
- Monitoring reports the service as available.
- No unexpected errors appear in the service logs.

---

# Completion Checklist

- [ ] Backup media mounted
- [ ] Recovery Point variables defined
- [ ] Sufficient free space confirmed
- [ ] Docker operational
- [ ] Production containers identified
- [ ] Orphaned or disposable containers identified
- [ ] Container state recorded
- [ ] Network inventory recorded
- [ ] Volume inventory recorded
- [ ] Container mount inventory recorded
- [ ] Active production named volumes identified
- [ ] Unused or legacy named volumes documented
- [ ] Data consistency requirements reviewed
- [ ] Service directories archived
- [ ] Required production named volumes archived
- [ ] Required application-native exports created
- [ ] Stopped services restarted
- [ ] Service health verified
- [ ] All required archives passed read testing
- [ ] SHA-256 checksums generated
- [ ] SHA-256 checksums verified
- [ ] Exclusions documented in `BACKUP_MANIFEST.md`
- [ ] `BACKUP_MANIFEST.md` completed
- [ ] Recovery Point documentation updated
- [ ] Recovery Point Index updated when appropriate

---
---

# Related Documentation

- Backup Implementation Plan
- Backup Inventory
- Backup Schedule
- Backup Strategy
- Recovery Point Index
- Recovery Point Standard
- Restore Procedures
- System Recovery Manual
- System Recovery Runbook

---

Docker Backup Procedure v1.0.0
