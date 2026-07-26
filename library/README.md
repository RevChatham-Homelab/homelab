# RevChatham Homelab Documentation Library

**Project:** RevChatham Homelab

**Document ID:** lib-000

**Document:** Documentation Library Overview

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-22

**Status:** Draft

**Author:** Adrian Chatham

---

# Purpose

The RevChatham Homelab Documentation Library provides a centralized navigation layer for project documentation.

The library is designed to give administrators, technicians, contributors, and future documentation tools a simple way to locate important documents without requiring knowledge of the repository's underlying directory structure.

---

# Library Design

The authoritative versions of project documents remain in their designated locations under the `docs/` directory.

The `library/` directory does not contain duplicate copies of those documents.

Instead, the library uses symbolic links that point to the authoritative documents.

This design provides:

- A single source of truth
- Centralized document navigation
- Reduced document duplication
- Easier document discovery
- Stable access paths for future scripts and applications
- Flexible repository organization

---

# Directory Structure

```text
library/
├── README.md
├── Standards/
├── Templates/
├── Architecture/
├── Operations/
├── Recovery/
├── Security/
└── Services/
```

---

# Library Categories

## Standards

The `Standards/` directory provides access to approved project standards and governance documents.

Examples include:

- Documentation standards
- Naming standards
- Git standards
- Docker standards
- Network standards
- Security standards
- Backup and recovery standards

---

## Templates

The `Templates/` directory provides access to reusable documentation templates.

Examples include:

- General document templates
- Engineering standard templates
- Architecture templates
- Design specification templates
- Implementation guide templates
- Runbook templates
- Troubleshooting templates
- Audit templates
- Incident report templates
- Changelog templates

---

## Architecture

The `Architecture/` directory provides access to documents describing the structure and design of the homelab environment.

Examples include:

- System architecture
- Network architecture
- Service dependencies
- Data flows
- Infrastructure diagrams
- Repository architecture

---

## Operations

The `Operations/` directory provides access to documents used for routine administration and maintenance.

Examples include:

- Runbooks
- Maintenance procedures
- Upgrade procedures
- Monitoring procedures
- Validation procedures
- Administrative references

---

## Recovery

The `Recovery/` directory provides access to backup, restoration, verification, and disaster recovery documentation.

Examples include:

- Recovery Point documentation
- Recovery automation documentation
- Backup procedures
- Restore procedures
- Verification standards
- System recovery manuals

---

## Security

The `Security/` directory provides access to security-related standards, procedures, and references.

Examples include:

- Authentication standards
- Access-control procedures
- Secret-management requirements
- Security-hardening guides
- Audit procedures
- Incident-response documentation

---

## Services

The `Services/` directory provides access to documentation associated with individual homelab services.

Examples include:

- Authentik
- Cloudflare Tunnel
- Grafana
- Homepage
- Nginx Proxy Manager
- Pi-hole
- Portainer
- Prometheus
- Uptime Kuma
- Website services

---

# Symbolic Link Standard

Documents placed within the library should normally be symbolic links.

The general format is:

```bash
ln -s <authoritative-document> <library-link>
```

Example:

```bash
ln -s ../../docs/templates/RUNBOOK_TEMPLATE.md \
  Templates/RUNBOOK_TEMPLATE.md
```

Relative symbolic links should be preferred when the source and destination are both located within the repository.

Relative links improve repository portability because they do not depend on the absolute filesystem path of a specific computer.

---

# Source of Truth

The `docs/` directory remains the authoritative source for project documentation.

Documents should be edited in their canonical locations.

The symbolic links inside the library provide access to those documents but do not create separate document versions.

---

# Future Development

The library may later be used as the navigation source for a technician-facing script or application.

Potential future functionality may include:

- Category-based navigation
- Specialty-based navigation
- Document search
- Service selection
- Document previews
- Runbook access
- Troubleshooting workflows
- Recovery workflow integration

This future functionality is outside the current scope of the library implementation.

---

## Related Documentation

- doc-001 Documentation Standard
- doc-002 Document Template

---

## Revision History

| Version | Date | Description | Author |
|----------|------------|---------------------------|----------------|
| X.Y.Z | YYYY-MM-DD | Description | Adrian Chatham |

---

RevChatham Homelab Documentation Library v1.0.0
