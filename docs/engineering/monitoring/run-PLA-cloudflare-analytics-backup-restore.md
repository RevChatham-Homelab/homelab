# PLA Cloudflare Analytics Backup and Restore Runbook

Status: Implemented and verified 2026-09-06 EDT / 2026-09-07 UTC  
Scope: Ubuntu VM 100 (`UbuntuServer24.04`) and PLA Cloudflare analytics

## 1. Recovery layers

### Layer 1: Live analytics database

- Authoritative database: `/var/lib/pla/analytics/traffic.sqlite`
- Owner: `pla-analytics:pla-analytics`
- Storage timezone: UTC
- Writes are idempotent by `(hour_utc, hostname)`.
- The hourly collector overlaps recent hours so a restored database can catch up
  within Cloudflare's available retention window.

### Layer 2: Daily consistent SQLite snapshots

- Directory: `/var/backups/pla-analytics/`
- Filename format: `traffic-YYYYMMDDTHHMMSSZ.sqlite`
- Timer: `pla-cloudflare-analytics-backup.timer`
- Schedule: approximately 02:15 UTC, with systemd random delay
- Retention: 14 snapshots
- Method: SQLite online-backup API followed by `PRAGMA integrity_check`

These snapshots protect against database-level corruption and accidental
changes. They are on the Ubuntu VM and are not sufficient for host or NVMe
failure by themselves.

### Layer 3: Nightly Proxmox VM backup

- Proxmox job: `pla-ubuntu-nightly`
- Guest: VM 100 only
- Schedule: 23:00 America/New_York (03:00 UTC while EDT applies)
- Mode: snapshot
- Compression: Zstandard
- Storage ID: `hdd-backups`
- Physical target: separate 1 TB HDD mounted at `/mnt/fileserver-data`
- Archive directory: `/mnt/fileserver-data/dump/`
- Retention: 7 daily, 4 weekly, and 3 monthly
- Mount safeguard: `is_mountpoint 1`

The backup directory is outside `/mnt/fileserver-data/shared`, so the VM
archives are not exposed through the fileserver's Samba share.

### Layer 4: Source repository

- Repository path: `/home/angel/homelab/website/cloudflare-analytics/`
- Initial implementation commit: `6557bc2`
- Remote repository contains source, example configuration, unit files, tests,
  the change manifest, and rollback documentation.
- Runtime configuration, Cloudflare identifiers, token, databases, and backups
  are intentionally excluded.

## 2. Items containing secrets

`/etc/pla/cloudflare.env` contains the Cloudflare API token. It must never be
placed in Git, QML, API responses, Prometheus labels, logs, or unencrypted
general-purpose storage.

The Proxmox VM archive contains the entire Ubuntu VM and therefore contains
this protected file. Treat VM archives as sensitive and keep their directory
root-only. For off-site storage, encrypt the backup before transfer.

## 3. Routine verification

### Collector and API health

Run on Ubuntu:

```bash
systemctl is-active pla-cloudflare-analytics.timer
systemctl is-active pla-cloudflare-analytics-backup.timer
systemctl is-active pla-traffic-api.service

sudo -u pla-analytics \
    /usr/bin/python3 \
    /usr/local/lib/pla-cloudflare-analytics/collector.py \
    --config /etc/pla/cloudflare-analytics.conf \
    check --full

curl --fail --silent --show-error \
    http://100.105.250.86:9468/health | jq
```

### Latest SQLite snapshot

Run on Ubuntu:

```bash
sudo -u pla-analytics python3 -c 'import glob,sqlite3;p=max(glob.glob("/var/backups/pla-analytics/traffic-*.sqlite"));c=sqlite3.connect("file:"+p+"?mode=ro",uri=True);print("Backup:",p);print("Integrity:",c.execute("PRAGMA integrity_check").fetchone()[0]);print("Rows:",c.execute("SELECT COUNT(*) FROM hourly_traffic").fetchone()[0]);c.close()'
```

### Latest Proxmox archive

Run on Proxmox:

```bash
pvesh get /cluster/backup --output-format yaml
pvesm status
pvesm list hdd-backups --content backup --vmid 100
```

Review the most recent task log in the Proxmox web interface under
Datacenter > Tasks. A successful task must end with `TASK OK` or the CLI
equivalent `Backup job finished successfully`.

Periodically test the newest archive's compressed stream:

```bash
zstd --test --verbose /mnt/fileserver-data/dump/NEWEST_ARCHIVE.vma.zst
```

Replace `NEWEST_ARCHIVE.vma.zst` with the exact filename returned by
`pvesm list`; do not use an unreviewed wildcard for restore operations.

## 4. Restore only the analytics database

Use this when Ubuntu is healthy but the live analytics database is damaged or
contains unwanted changes.

1. Select an exact snapshot filename from `/var/backups/pla-analytics/`.
2. Verify the selected snapshot before stopping services.
3. Stop collection and the API.
4. Move the current database and sidecar files into a dated recovery directory.
5. Install the verified snapshot with the correct ownership and mode.
6. Run the collector manually. This verifies the database, catches up available
   hours, and republishes the API snapshot.
7. Re-enable normal operation only after integrity and API checks pass.

Example commands on Ubuntu follow. Replace `SELECTED_BACKUP` with one exact,
verified path.

```bash
SELECTED_BACKUP=/var/backups/pla-analytics/traffic-YYYYMMDDTHHMMSSZ.sqlite

sudo -u pla-analytics env SELECTED_BACKUP="$SELECTED_BACKUP" \
    python3 -c 'import os,sqlite3;p=os.environ["SELECTED_BACKUP"];c=sqlite3.connect("file:"+p+"?mode=ro",uri=True);print(c.execute("PRAGMA integrity_check").fetchone()[0]);c.close()'
```

If the result is `ok`, continue:

```bash
sudo systemctl stop pla-cloudflare-analytics.timer
sudo systemctl stop pla-traffic-api.service

restore_hold=/var/lib/pla/analytics/pre-restore-YYYYMMDDTHHMMSSZ
sudo install -d -o pla-analytics -g pla-analytics -m 0750 "$restore_hold"

sudo mv /var/lib/pla/analytics/traffic.sqlite "$restore_hold/"
sudo test ! -e /var/lib/pla/analytics/traffic.sqlite-wal \
    || sudo mv /var/lib/pla/analytics/traffic.sqlite-wal "$restore_hold/"
sudo test ! -e /var/lib/pla/analytics/traffic.sqlite-shm \
    || sudo mv /var/lib/pla/analytics/traffic.sqlite-shm "$restore_hold/"

sudo install -o pla-analytics -g pla-analytics -m 0640 \
    "$SELECTED_BACKUP" \
    /var/lib/pla/analytics/traffic.sqlite

sudo systemctl start pla-cloudflare-analytics.service

sudo -u pla-analytics \
    /usr/bin/python3 \
    /usr/local/lib/pla-cloudflare-analytics/collector.py \
    --config /etc/pla/cloudflare-analytics.conf \
    check --full

sudo systemctl enable --now pla-traffic-api.service
sudo systemctl enable --now pla-cloudflare-analytics.timer

curl --fail --silent --show-error \
    http://100.105.250.86:9468/health | jq
```

Do not restore `/var/lib/pla-api/traffic.sqlite` independently. It is a derived,
read-only snapshot and is regenerated by a successful collector run.

Retain the `pre-restore-*` directory until the restored database has been
verified over at least one scheduled collection cycle.

## 5. Restore the complete Ubuntu VM

Use this for loss of VM 100, its NVMe-backed virtual disk, or the Ubuntu
installation.

1. Confirm that `hdd-backups` is active and the HDD is mounted.
2. Select the exact VM 100 archive in the Proxmox web interface under the
   `hdd-backups` storage.
3. Prefer restoring first to an unused VM ID for a recovery test.
4. Keep the test VM network interface disconnected before first boot; the guest
   has a static address and must not conflict with production VM 100.
5. Boot the isolated test VM and verify the analytics database, services, and
   token permissions.
6. For a production replacement, stop the old VM 100 and preserve it until the
   restored VM passes verification.
7. Reconnect networking only when there is exactly one active guest using the
   production IP address.

Do not overwrite or destroy VM 100 merely to test a restore. A production
restore is a deliberate destructive operation and requires a fresh backup and
explicit approval.

## 6. Configuration rollback

### Disable the scheduled Proxmox job without deleting archives

Run on Proxmox:

```bash
pvesh set /cluster/backup/pla-ubuntu-nightly --enabled 0
```

### Remove the job definition

After confirming the exact job ID:

```bash
pvesh get /cluster/backup --output-format yaml
pvesh delete /cluster/backup/pla-ubuntu-nightly
```

This does not delete existing archive files.

### Remove the Proxmox storage definition

Only after disabling/removing the job:

```bash
pvesm remove hdd-backups
```

This removes the Proxmox storage registration and does not delete the HDD's
backup archives or fileserver data.

### Roll back collector/API v1.1.1

The preserved pre-upgrade files are in:

`/home/angel/backups/pla-cloudflare-analytics-pre-v1.1.1-20260906/`

The detailed collector/API removal sequence is in
`/home/angel/homelab/website/cloudflare-analytics/README.md`. Preserve
`traffic.sqlite` and the backup snapshots before removing accounts or paths.

## 7. Known limitation and next improvement

The first verified Proxmox archive was created successfully in snapshot mode,
but VM 100 did not have the QEMU guest agent enabled, so Proxmox skipped guest
filesystem freezing. The VM archive remains crash-consistent, and the included
SQLite backup is application-consistent.

Recommended follow-up: inspect, install if needed, and enable
`qemu-guest-agent` during a controlled maintenance window. Then confirm that a
subsequent Proxmox task log no longer reports that filesystem freezing was
skipped.

This HDD backup is local to the Proxmox host. Add an encrypted off-site copy in
a later phase to protect against loss of the entire host or both internal
drives.

## 8. First verified archive

- Archive: `vzdump-qemu-100-2026_09_06-20_04_33.vma.zst`
- Size: 13,095,624,716 bytes
- SHA-256: `becf807d0dae5f2120ad41622a2dd0fa6cad18b14fbb9d05f5021fbc700bb8a2`
- Zstandard integrity test: passed
- VM status after backup: running
