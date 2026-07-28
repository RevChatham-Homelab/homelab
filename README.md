# RevChatham Homelab

**Project:** RevChatham Homelab

**Document:** Repository README

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-27

**Status:** Operational

---

> A production-inspired homelab built to develop practical skills in Linux administration, Docker, networking, identity management, monitoring, documentation, and infrastructure security.

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-v1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

# About

This repository documents the design, deployment, maintenance, and continuous improvement of my self-hosted homelab.

The project is designed to develop hands-on experience with technologies commonly used in IT Operations, Systems Administration, DevOps, and Cybersecurity while building a professional portfolio of real-world infrastructure projects.

Every service is deployed using Docker, documented, audited, and version controlled to mirror professional infrastructure management practices.

---

# Project Philosophy

The RevChatham Homelab is guided by a documented engineering philosophy that emphasizes accuracy, verification, continuous improvement, and practical engineering experience.

The philosophy defines the principles used when making technical, documentation, and project governance decisions.

See:

- `DESIGN_PHILOSOPHY.md`

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
| Portainer | Docker Management | ✅ |
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
├── grafana/
├── homepage/
├── nginx-proxy-manager/
├── pihole/
├── portainer/
├── prometheus/
├── uptime-kuma/
├── website/
├── docs/
│   ├── audits/
│   ├── BACKUP_RESTORE_RECOVER/
│   ├── decisions/
│   ├── draft_proposals/
│   ├── engineering/
│   ├── templates/
│   └── incidents/
├── CHANGELOG.md
├── LICENSE
└── README.md
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

Comprehensive project documentation is maintained in the `docs/` directory and includes architecture, engineering standards, recovery procedures, audits, incident reports, and project planning.

- Backup, Restore, and Recovery Framework
- Service Documentation
- Service Audits
- Engineering Standards
- Templates
- Draft Proposals
- Incident Documentation
- Project Roadmap

---

# Project Roadmap

| Milestone | Title | Status |
|-----------|-------|:------:|
| **v0.6.0** | Backup, Restore & Recovery Framework | ✅ Completed |
| **v0.7.0** | Recovery Automation & CBART | ✅ Completed |
| **v0.8.0** | Website, Portfolio & Security | 🚧 In Progress |
| **v0.9.0** | Reserved for Future Development | 📌 Reserved |
| **v1.0.0** | Initial Public Release | 🎯 Target |

---

## Current Milestone

**v0.8.0 — Website, Portfolio & Security**

### Milestone Objectives

- Develop the public portfolio website
- Publish engineering documentation
- Complete portfolio content
- Integrate security improvements
- Prepare the project for public release

---

# Guiding Principles

This project follows several principles:

- Functional infrastructure before polish
- Security first
- Documentation before optimization
- Version controlled infrastructure
- Continuous improvement
- Learn by building
- Standards before automation

---

# Lessons Learned

One of the primary goals of this homelab is documenting not only successful deployments, but also troubleshooting steps, design decisions, and lessons learned along the way.

Incident documentation is stored in:

```text
docs/incidents/

```

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.


Repository README v1.0.0
