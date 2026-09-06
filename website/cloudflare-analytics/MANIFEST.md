# Change Manifest

## Existing server changes already completed

- Added system user and group `pla-analytics`.
- Added `/etc/pla` with ownership `root:pla-analytics`, mode `0750`.
- Added `/etc/pla/cloudflare.env`, ownership `root:pla-analytics`, mode `0640`.
- Added `/etc/pla/cloudflare-analytics.conf`, ownership `root:pla-analytics`, mode `0640`.
- Added `/var/lib/pla/analytics`, ownership `pla-analytics:pla-analytics`, mode `0750`.

## Changes made when this bundle is installed

- Add `/usr/local/lib/pla-cloudflare-analytics/collector.py`.
- Add the four collector and backup systemd unit files listed in `README.md`.
- Add `/var/backups/pla-analytics`.
- Add a source copy under the homelab repository.
- Create `/var/lib/pla/analytics/traffic.sqlite` during the first successful run.
- Enable two timers only after manual collection, integrity, and idempotency tests pass.

## Version 1.1 API additions

- Add system user/group `pla-analytics-api`.
- Add `/etc/pla-api/traffic-api.conf` with no secrets.
- Add `/var/lib/pla-api/traffic.sqlite` as the atomically replaced API snapshot.
- Add `/usr/local/lib/pla-cloudflare-analytics/api.py`.
- Add `/etc/systemd/system/pla-traffic-api.service`.
- Add one Tailscale-interface UFW allowance for TCP port 9468.
- Add `pla-analytics` to the `pla-analytics-api` group so only the collector can
  atomically replace the snapshot read by the API.
- Do not expose the API through Cloudflare, Nginx Proxy Manager, or the public LAN interface.

## Explicitly unchanged

- PLA/QML visual design
- Prometheus and its retention
- `prometheus-nginxlog-exporter`
- Nginx, Nginx Proxy Manager, and Cloudflare Tunnel
- Existing Docker Compose projects
