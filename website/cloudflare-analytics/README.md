# PLA Cloudflare Analytics Collector and Read-Only API

This bundle archives public edge traffic for `revchatham.com` and
`www.revchatham.com` from Cloudflare's official GraphQL Analytics API.
It intentionally does not replace or combine with the existing Nginx/Prometheus
origin metrics.

## Confirmed Cloudflare Free-plan limits (2026-09-06)

- Dataset: `httpRequestsAdaptiveGroups`
- Retention: 691,200 seconds (8 days)
- Maximum query duration: 86,400 seconds (24 hours)
- Maximum page size: 10,000
- Maximum fields per query: 40

The collector discovers these limits during every run and initially backfills
all complete hourly buckets still available. It queries no more than the
reported maximum duration.

## Stored data

The primary key is `(hour_utc, hostname)`. Repeated collection uses an upsert,
so overlapping runs update hours instead of creating duplicates.

Stored hourly fields include requests, visits, request/response bytes, cached
and uncached requests, origin-contacting requests, cached/uncached response
bytes, blocked requests, 4xx and 5xx counts, Cloudflare-observed origin latency,
sampling interval, and collection timestamp.

SQLite views provide daily, Monday-based weekly, monthly, and yearly rollups.
Storage is UTC. Percentiles remain hourly because percentiles cannot be
mathematically averaged into valid long-range percentiles.

## Sampling

`httpRequestsAdaptiveGroups` is adaptive. Cloudflare returns estimated totals
when sampling is active. The database records `sample_interval` and
`is_sampled` with every hourly row. At low traffic volume, the interval is
normally 1.0.

## Cache definitions

Following Cloudflare's published definitions:

- Cached requests: `HIT`, `STALE`, `UPDATING`, `IGNORED`
- Cached response bytes: the above plus `REVALIDATED`
- Uncached requests/bytes: all other cache statuses
- Origin requests: rows where `originResponseStatus` is non-zero

Uncached and origin-contacting requests are deliberately separate because an
edge-generated or blocked response can be uncached without reaching Nginx.

## Security model

- The API token exists only in `/etc/pla/cloudflare.env`.
- The collector never writes the token into SQLite or logs.
- systemd runs the collector as the non-login `pla-analytics` user.
- The collector can write only `/var/lib/pla/analytics`.
- The backup service can additionally write `/var/backups/pla-analytics`.
- PLA reads a separate snapshot through a read-only API; it never receives the
  token or direct database access.

## Local backup

The daily backup uses Python's SQLite online-backup API, validates the source
and destination with `PRAGMA integrity_check`, atomically renames the completed
snapshot, and retains 14 snapshots.

This protects against accidental database damage but is not a disaster backup
because it resides on the same VM. Include `/var/lib/pla/analytics` and
`/var/backups/pla-analytics` in an external Proxmox/fileserver backup.

## Files installed

- `/usr/local/lib/pla-cloudflare-analytics/collector.py`
- `/usr/local/lib/pla-cloudflare-analytics/api.py`
- `/etc/systemd/system/pla-cloudflare-analytics.service`
- `/etc/systemd/system/pla-cloudflare-analytics.timer`
- `/etc/systemd/system/pla-cloudflare-analytics-backup.service`
- `/etc/systemd/system/pla-cloudflare-analytics-backup.timer`
- `/etc/systemd/system/pla-traffic-api.service`
- `/etc/pla/cloudflare-analytics.conf` (already created separately)
- `/etc/pla/cloudflare.env` (already created separately; never stored here)
- `/etc/pla-api/traffic-api.conf` (contains no secret)
- `/var/lib/pla/analytics/traffic.sqlite` (created at first collection)
- `/var/lib/pla-api/traffic.sqlite` (read-only API snapshot)
- `/var/backups/pla-analytics/` (created during installation)

## Rollback

1. Stop and disable both timers and `pla-traffic-api.service`.
2. Delete the UFW rule allowing TCP 9468 on `tailscale0`.
3. Remove the five systemd unit files and reload systemd.
4. Remove `/usr/local/lib/pla-cloudflare-analytics`.
5. Preserve or archive `traffic.sqlite` unless deliberate deletion is desired.
6. Revoke the token in Cloudflare only when retiring the collector completely.
7. Only after preserving desired data, remove `/etc/pla`, `/var/lib/pla`,
   `/etc/pla-api`, `/var/lib/pla-api`, the backup directory, and the
   `pla-analytics` and `pla-analytics-api` system accounts/groups.

No existing PLA visual files, Prometheus configuration, Nginx configuration,
or Docker services are modified by this collector.

## Read-only PLA interface

Version 1.1 adds a separate Tailscale-only JSON API. The collector publishes an
integrity-checked SQLite snapshot at `/var/lib/pla-api/traffic.sqlite` with an
atomic rename after each successful run. The API opens that snapshot in
read-only immutable mode and never opens the live writer database.

The API runs as `pla-analytics-api`, which cannot traverse `/etc/pla` and cannot
read the Cloudflare token. Its systemd sandbox also marks both Cloudflare
configuration files and the live database inaccessible.

It binds only to the server's Tailscale address on TCP 9468. UFW permits that
port only on `tailscale0`; it is not published through Docker, Cloudflare,
Nginx Proxy Manager, or the LAN address. Any device allowed by the tailnet ACL
can read these aggregate traffic statistics, so tailnet access remains the
authorization boundary.

Endpoints:

- `GET /health`
- `GET /v1/summary?hostname=all&start=...&end=...`
- `GET /v1/series?interval=hour|day|week|month|year&hostname=all&start=...&end=...`

Only fixed aggregate fields and whitelisted intervals are available. The API
does not accept SQL, file paths, credentials, or write methods.

`start` and `end` are optional UTC timestamps in ISO 8601 format. `end` is
exclusive. `hostname` may be `all`, `revchatham.com`, or
`www.revchatham.com`. Responses include `contains_sampled_data` so PLA can
label estimated Cloudflare data accurately.
