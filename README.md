# RevChatham Homelab

> A production-inspired homelab built to develop practical skills in Linux administration, Docker, networking, identity management, monitoring, documentation, and infrastructure security.

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-v0.4.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

# About

This repository documents the design, deployment, maintenance, and continuous improvement of my self-hosted homelab.

The project was created to gain hands-on experience with technologies commonly used in IT Operations, Systems Administration, DevOps, and Cybersecurity while building a professional portfolio of real-world infrastructure projects.

Every service is deployed using Docker, documented, audited, and version controlled to mirror professional infrastructure management practices.

---

# Current Infrastructure

| Service | Purpose | Status |
|---------|---------|:------:|
| Homepage | Dashboard | ✅ |
| Pi-hole | DNS Filtering | ✅ |
| Authentik | Identity Provider / SSO | ✅ |
| Grafana | Monitoring Dashboards | ✅ |
| Prometheus | Metrics Collection | ✅ |
| Uptime Kuma | Service Monitoring | ✅ |
| Nginx Proxy Manager | Reverse Proxy | ✅ |
| Portfolio Website | Personal Website | 🚧 |

---

# Technology Stack

## Operating Systems

- Proxmox VE
- Ubuntu Server
- Linux

## Containerization

- Docker
- Docker Compose

## Networking

- Cloudflare Tunnel
- Nginx Proxy Manager
- Pi-hole

## Identity

- Authentik
- OpenID Connect (OIDC)
- Single Sign-On (SSO)

## Monitoring

- Grafana
- Prometheus
- Uptime Kuma

## Development & Documentation

- Git
- GitHub
- Markdown
- Visual Studio Code

---

# Repository Structure

```text
homelab/
├── authentik/
├── docs/
│   ├── architecture/
│   ├── audits/
│   ├── backups/
│   ├── decisions/
│   ├── engineering/
│   ├── setup/
│   ├── templates/
│   └── troubleshooting/
├── grafana/
├── homepage/
│   └── config/
├── nginx-proxy-manager/
├── pihole/
├── portainer/
└── prometheus/
```

---

# Project Goals

- Learn Linux system administration.
- Build experience with Docker and containerized services.
- Practice infrastructure documentation.
- Implement centralized authentication using Authentik.
- Develop monitoring and observability solutions.
- Improve infrastructure security through periodic audits.
- Maintain reproducible deployments using Git.

---

# Documentation

Detailed documentation is available in the `docs/` directory.

- Project Roadmap
- Service Audits
- Setup Guides
- Troubleshooting Notes
- Backup Strategy
- Architecture Documentation

---

# Project Roadmap

Current Phase:

**Phase 2 – Service Audit & Standardization**

Completed:

- Core infrastructure deployment
- Homepage audit
- Pi-hole audit
- Authentik audit
- Documentation framework
- GitHub repository setup

# Upcoming

- Uptime Kuma audit
- Backup strategy
- Architecture diagrams
- Security hardening
- README v1.1 documentation pass
- Audit v1.1 documentation pass
- Architecture Decision Records

---

# Guiding Principles

This project follows several principles:

- Functional infrastructure before polish
- Security first
- Documentation before optimization
- Version controlled infrastructure
- Continuous improvement
- Learn by building

---

# Lessons Learned

One of the primary goals of this homelab is documenting not only successful deployments, but also troubleshooting steps, design decisions, and lessons learned along the way.

Troubleshooting documentation is stored in:

```text
docs/troubleshooting/

```

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.
