# Nginx Proxy Manager

## Overview

Nginx Proxy Manager provides a web interface for managing reverse proxy hosts, SSL certificates, and access to internal homelab services.

In this homelab, it is used to route public service URLs to internal applications.

## Service Details

| Item | Value |
|---|---|
| Container | `nginx-proxy-manager` |
| Image | `jc21/nginx-proxy-manager:2.15.1` |
| Network | `homelab` |
| Admin UI | `http://SERVER-IP:81` |
| HTTP | `80` |
| HTTPS | `443` |

## Directory Layout

```text
nginx-proxy-manager/
├── compose.yml
├── .env
├── .env.example
├── .gitignore
├── data/
└── letsencrypt/
```

## Start

```bash
docker compose up -d
```

## Stop

```bash
docker compose down
```

## Restart

```bash
docker compose restart
```

## View Logs

```bash
docker compose logs -f
```

## Update

Update the image tag in `.env`, then run:

```bash
docker compose pull
docker compose up -d
```

## Backup

Back up these folders:

```text
data/
letsencrypt/
```

Example:

```bash
tar -czf nginx-proxy-manager-backup.tar.gz data letsencrypt compose.yml .env.example README.md
```

## Restore

```bash
tar -xzf nginx-proxy-manager-backup.tar.gz
docker compose up -d
```

## Notes

- `.env` is not committed because it may contain local configuration.
- `data/` and `letsencrypt/` are not committed because they contain runtime data and certificates.
- Nginx Proxy Manager uses the shared `homelab` Docker network.
- Public DNS and Cloudflare Tunnel route traffic to this service.
