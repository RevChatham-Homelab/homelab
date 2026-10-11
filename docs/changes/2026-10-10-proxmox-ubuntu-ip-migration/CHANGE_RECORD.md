# Infrastructure Change Record
## Proxmox and Ubuntu Server IP Migration

**Change date:** 2026-10-10
**Change type:** Planned infrastructure maintenance
**Status:** Operationally complete; follow-up checks outstanding
**Environment:** RevChatham Homelab
**Repository:** RevChatham-Homelab/homelab

---

## 1. Purpose

Reassign the primary Dell Proxmox host and Ubuntu Server VM
to their intended management addresses while preserving
connectivity to hosted services.

Goals:
- Proxmox Dell 7060: 192.168.1.99
- Ubuntu Server VM 100: 192.168.1.100
- Preserve fileserver connectivity at 192.168.1.102
- Update dependent services and configuration references
- Verify persistence across reboot
- Preserve historical records and rollback information

## 2. Address Changes

| System | Previous IP | New IP |
|---|---|---|
| Dell Proxmox pve7060 | 192.168.1.100 | 192.168.1.99 |
| Ubuntu Server VM 100 | 192.168.1.101 | 192.168.1.100 |
| Fileserver CT 102 | 192.168.1.102 | Unchanged |

Historical note:
Proxmox previously used 192.168.1.110 during an earlier
configuration period. A reference remains in
/etc/network/interfaces.bak.

Network:
- Subnet: 192.168.1.0/24
- Gateway: 192.168.1.1
- Router: Netgear Nighthawk R7000

## 3. Proxmox Configuration

Host: pve7060.revchatham.com

Persistent configuration:
- /etc/network/interfaces
- /etc/hosts

Verified:
- vmbr0: 192.168.1.99/24
- Gateway: 192.168.1.1
- Bridge interface: nic0
- Hostname resolves locally to 192.168.1.99
- SSH access successful
- Ubuntu Server can reach Proxmox by ICMP

Existing nic0 ethtool settings were preserved.

Searches of /etc/pve, /etc/network, and /etc/hosts
found no stale .101 or .110 references in the examined
active configuration files.

The historical /etc/network/interfaces.bak was retained.

## 4. Ubuntu Server Configuration

System: Ubuntu Server 24.04
VMID: 100
Interface: ens18

Persistent network configuration:
- /etc/netplan/50-cloud-init.yaml

Verified:
- Static IP: 192.168.1.100/24
- Default gateway: 192.168.1.1
- DNS: 1.1.1.1 and 8.8.8.8
- systemd-networkd active
- cloud-init disabled

The resolver configuration was updated to remove the
previous 192.168.1.101 reference.

Ubuntu was rebooted successfully.

After reboot:
- Static IP persisted
- Default route persisted
- DNS resolution worked
- SSH access worked
- Docker services restarted successfully

## 5. Cloudflare Tunnel

Configuration:
- /etc/cloudflared/config.yml

Updated ingress destinations for services hosted by
Proxmox and Ubuntu Server.

Proxmox:
- 192.168.1.99:8006

Ubuntu services:
- Nginx Proxy Manager: 192.168.1.100:81
- Portainer: 192.168.1.100:9443
- Uptime Kuma: 192.168.1.100:3001
- Authentik: 192.168.1.100:9000
- Grafana: 192.168.1.100:3002

The cloudflared service was restarted and verified active.

## 6. Homepage

Live configuration:
- /home/angel/homepage/.env
- /home/angel/homepage/config/services.yaml

Repository configuration:
- /home/angel/homelab/homepage/config/services.yaml

Updated five service URLs:
- Pi-hole
- Nginx Proxy Manager
- Uptime Kuma
- Prometheus
- Authentik

All five changed from 192.168.1.101 to 192.168.1.100.

HOMEPAGE_ALLOWED_HOSTS was updated for the new IP.

Only the Homepage container was recreated.

Verified:
- http://192.168.1.100:3000
- https://home.revchatham.com

Git commit:
f3328a7 fix(homepage): update service links for IP migration

Commit successfully pushed to origin/main.

## 7. Grafana and Authentik

Grafana configuration:
- /home/angel/grafana/.env

Updated:
- GF_AUTH_GENERIC_OAUTH_AUTH_URL
- GF_AUTH_GENERIC_OAUTH_TOKEN_URL
- GF_AUTH_GENERIC_OAUTH_API_URL

All three now reference 192.168.1.100:9000.

Only the Grafana container was recreated.

Verified:
- Grafana container running
- Updated OAuth environment variables loaded
- https://grafana.revchatham.com accessible
- Authentik portal at https://auth.revchatham.com accessible
- Grafana launched successfully from the Authentik portal

Follow-up:
Test a fresh OAuth login without an existing browser session,
including from outside the home network.

The current authorization URL uses the internal HTTP address.
Remote browser redirection must be validated before treating
external SSO as fully verified.

## 8. Monitoring Stack

Prometheus scrape targets were verified operational.

Targets use Docker service names:
- cadvisor:8080
- nginxlog-exporter:4040
- node-exporter:9100
- prometheus:9090

No migration-related IP change was needed for those targets.

Other monitoring services were not unnecessarily recreated.

## 9. Router and DHCP

Router: Netgear Nighthawk R7000
Gateway: 192.168.1.1

DHCP pool:
192.168.1.2 - 192.168.1.50

Verified address reservations:
- Proxmox Dell: 192.168.1.99
- Ubuntu Server: 192.168.1.100
- Fileserver: 192.168.1.102

All three addresses are outside the dynamic DHCP pool.

No router changes were required during final verification.

## 10. Network Validation

Ubuntu ens18:
192.168.1.100/24

Default route:
192.168.1.1

Ubuntu to Proxmox 192.168.1.99:
- 3 packets transmitted
- 3 packets received
- 0% packet loss

Ubuntu to Fileserver 192.168.1.102:
- 3 packets transmitted
- 3 packets received
- 0% packet loss

Proxmox:
- SSH successful
- Hostname: pve7060.revchatham.com
- /etc/hosts mapped hostname to 192.168.1.99
- Persistent vmbr0 configuration verified

## 11. Configuration Audit

The homelab repository was searched for references to
192.168.1.101 and 192.168.1.110.

Remaining matches were historical incident documentation
and migration backups.

No remaining references were found in the examined active
repository configurations.

Proxmox VM and LXC configurations were also checked.

Historical documentation was intentionally preserved.

## 12. Backup and Rollback Considerations

Configuration backups were created during migration.

Known backup locations include:
- /etc/network/interfaces.bak on Proxmox
- /home/angel/homepage/configuration backups
- /home/angel/grafana/.env.before-ip-migration
- Cloudflare Tunnel configuration backup

Exact backup filenames and contents should be verified
before attempting a rollback.

Rollback must be coordinated across:
1. Proxmox static networking and hostname mapping
2. Ubuntu Netplan and DNS
3. Cloudflare Tunnel ingress
4. Homepage configuration
5. Grafana OAuth configuration
6. Router reservations, if required

Do not restore an old IP to one machine while another
machine is actively using that address.

Any rollback should be performed with console access
available to avoid losing remote management.

## 13. Outstanding Follow-Up

- [x] Test fresh Grafana OAuth login from outside LAN (verified via cellular, Wi-Fi disabled)
- [x] Review other services for hardcoded legacy addresses
- [x] Verify migration backup files exist; retention policy not yet established
- [x] Confirm GitHub documentation commit and push

## 14. Post-Migration Hostname Correction

Ubuntu Server's `/etc/hosts` contained a stale mapping:

- Previous: `192.168.1.100 pve7060`
- Corrected: `192.168.1.99 pve7060`

The original hosts file was preserved at
`/etc/hosts.before-ip-migration-fix`.

Verification:
- `getent ahostsv4 pve7060` returned `192.168.1.99`.
- `ping -c 3 pve7060` succeeded with zero packet loss.

## 15. Outcome

The planned IP migration was completed successfully.

Proxmox is operating at 192.168.1.99.
Ubuntu Server is operating at 192.168.1.100.
Fileserver remains at 192.168.1.102.

Core services, networking, repository configuration,
and router reservations were verified.

No unresolved network connectivity failure was identified
during final validation.
