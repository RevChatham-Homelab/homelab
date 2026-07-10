# Homelab Project Roadmap

**Project:** RevChatham Homelab

---

# Vision

Build and maintain a production-inspired homelab that demonstrates practical experience with Linux administration, Docker, networking, reverse proxies, identity management, monitoring, documentation, and security.

The homelab serves three primary purposes:

- Hands-on learning
- IT portfolio development
- Long-term infrastructure experimentation

---

# Project Phases

## Phase 1 — Core Infrastructure ✅

### Objectives

- Install Proxmox
- Configure networking
- Deploy Docker
- Build Docker network
- Configure Cloudflare Tunnel

### Services

- Homepage
- Pi-hole
- Authentik
- Portainer
- Grafana
- Prometheus
- Uptime Kuma
- Nginx Proxy Manager
- Portfolio Website

**Status:** Complete

---

## Phase 2 — Service Audit & Standardization 🟡 (Current)

### Objectives

- Audit every Docker stack
- Review security
- Remove secrets from Git
- Create `.env.example`
- Standardize compose files
- Review Docker networking
- Improve configuration consistency

### Deliverables

- Service audit reports
- Updated `.gitignore`
- Standardized environment files

---

## Phase 3 — Documentation

### Objectives

Create professional documentation for every service.

### Deliverables

- README files
- Service documentation
- Deployment guides
- Troubleshooting guides
- Architecture documentation
- Audit reports

---

## Phase 4 — Backup & Disaster Recovery

### Objectives

Develop a complete backup strategy.

### Deliverables

- Proxmox backups
- Docker backups
- Configuration backups
- GitHub repository backup
- Recovery documentation

---

## Phase 5 — Security Hardening

### Objectives

Reduce attack surface and improve security.

### Tasks

- Remove unnecessary exposed ports
- Internal Docker networking
- Reverse proxy only access
- TLS improvements
- Docker permission review
- Secret management review
- Container privilege review

---

## Phase 6 — Monitoring & Observability

### Objectives

Expand monitoring capabilities.

### Planned Additions

- Additional Grafana dashboards
- Alerting
- Log aggregation
- Performance monitoring

---

## Phase 7 — Automation

### Objectives

Reduce manual administration.

### Planned Additions

- Update automation
- Backup automation
- Health monitoring
- Scheduled maintenance

---

## Phase 8 — Portfolio Enhancement

### Objectives

Transform the homelab into a polished portfolio project.

### Deliverables

- Public GitHub repository
- Architecture diagrams
- Screenshots
- Technical write-ups
- Lessons learned
- Troubleshooting documentation

---

# Future Projects

## Infrastructure as Code

- Docker Compose improvements
- Configuration templating

## Identity

- Additional OIDC integrations

## Monitoring

- Advanced dashboards
- Custom metrics

## Networking

- VLAN expansion
- Internal DNS improvements

## Security

- Wazuh
- CrowdSec
- Fail2Ban
- Vulnerability scanning

---

# Current Focus

**Phase 2 — Service Audit & Standardization**

Current Service:

- Authentik

Next Service:

- Grafana

---

# Success Criteria

The project is considered complete when:

- Every service has been audited.
- Every service is documented.
- Secrets are excluded from Git.
- Backup strategy is implemented.
- Security hardening is complete.
- Portfolio documentation is published.
