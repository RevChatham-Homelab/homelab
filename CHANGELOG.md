# Changelog

**Project:** RevChatham Homelab

**Document:** Project Changelog

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-15

**Status:** Operational

---

All notable changes to the **RevChatham Homelab** project are documented here.

This project follows the principles of **Semantic Versioning (SemVer)** and **Keep a Changelog**.

---

## [Unreleased]

### Planned

- Repository quality assurance
- Architecture diagrams
- Infrastructure screenshots
- Portfolio website development
- Automation framework (v0.7.0)
- Security hardening

---

## [0.6.1] - 2026-07-16

### Added

- Created the Incident Documentation Framework.
- Added `INCIDENT_REPORT_STANDARD.md`.
- Added `INCIDENT_REPORT_TEMPLATE.md`.
- Added the `docs/incidents/` documentation hierarchy.
- Introduced standardized Incident IDs using the `IR-YYYYMMDD-###` format.

### Changed

- Renamed the `docs/troubleshooting/` directory to `docs/incidents/`.
- Standardized historical incident reports to the Incident Report Standard.
- Standardized repository headers and footers across governance and recovery documentation.
- Updated repository documentation to reference the Incident Documentation framework.
- Refined documentation governance by separating standards from templates.

## [0.6.0] - 2026-07-13

### Added

- Established the Backup, Restore, and Recovery Framework.
- Implemented the Recovery Point Standard v1.0.0.
- Created the System Recovery Manual (SRM-1.0.0).
- Created the System Recovery Runbook (SRB-1.0.0).
- Created standardized procedures for GitHub, Docker, Proxmox, Offsite, and Disaster Recovery.
- Created the Restore Procedures index.
- Created the first standardized Recovery Point (`RP-20260711-001`).
- Added Recovery Point templates and verification templates.
- Implemented Recovery Point verification using SHA-256 checksums.
- Integrated Proxmox VM backup documentation into the Recovery Point standard.

### Completed

- Completed Backup, Restore, and Recovery documentation for Milestone v0.6.0.
- Completed Recovery Point `RP-20260711-001`.
- Completed the initial Backup, Restore, and Recovery operational standard.

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


Project Changelog v1.0.0
