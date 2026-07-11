# Changelog

All notable changes to the **RevChatham Homelab** project are documented here.

This project follows the principles of **Semantic Versioning (SemVer)** and **Keep a Changelog**.

---

## [Unreleased]

### Planned

- Repository-wide consistency review
- GitHub milestone verification
- Backup and disaster recovery implementation
- Architecture diagrams
- Infrastructure screenshots
- Service deployment guides
- Security hardening phase

---

## [0.5.0] - 2026-07-11

### Added

- Service-specific `.gitignore` files for all production services.
- Standardized `README.md` documentation for all production services.
- Standardized `.env.example` files using Environment Standard v1.0.
- Completed Prometheus service documentation.
- Completed Portainer service documentation.
- Completed Uptime Kuma service documentation.
- Completed Nginx Proxy Manager service documentation.
- Added `SERVICE_REVIEW_CHECKLIST.md` to document the repository review process.

### Audited

- Grafana
- Prometheus
- Portainer
- Uptime Kuma
- Nginx Proxy Manager

### Standardized

- Docker Compose files validated against production deployments.
- Service documentation aligned with README Template v1.0.
- Service audits aligned with Audit Template v1.0.
- Environment files aligned with Environment Standard v1.0.
- Repository layout reviewed for consistency across all production services.

### Fixed

- Corrected Docker Compose issues discovered during repository review.
- Corrected missing repository `.gitignore` files.
- Corrected documentation inconsistencies identified during the service review process.
- Corrected Markdown formatting issues discovered during audit validation.

---

## [0.4.0] - 2026-07-06

### Added

- GitHub repository
- SSH authentication for Git
- Documentation framework
- Project roadmap
- Audit summary
- Documentation standards
- Root README
- MIT License
- Root .gitignore
- CHANGELOG

### Audited

- Homepage
- Pi-hole
- Authentik

### Standardized

- Environment variable templates (.env.example)
- Service README format
- Audit report format

---

## [0.3.0]

### Added

- Homepage
- Pi-hole
- Authentik
- Grafana
- Prometheus
- Uptime Kuma
- Nginx Proxy Manager
- Portfolio Website

---

## [0.2.0]

### Added

- Docker Engine
- Docker Compose
- Shared Docker network

---

## [0.1.0]

### Added

- Proxmox VE
- Ubuntu Server VM
- Initial networking
