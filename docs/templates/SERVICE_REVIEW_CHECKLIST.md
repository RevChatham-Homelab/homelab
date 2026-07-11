# Service Review Checklist

**Project:** RevChatham Homelab  
**Document:** Service Review Checklist  
**Version:** 1.0.0  
**Last Updated:** 2026-07-10

---

# Purpose

This checklist is used to verify that each homelab service conforms to the approved project standards before being committed to the repository.

The checklist does not introduce new requirements. It summarizes the existing documentation, environment, deployment, and repository standards.

---

# Service Information

**Service:**  
**Review Date:**  
**Reviewed By:**  
**Service Version:**  

---

# Version Review

- [ ] Running application version confirmed
- [ ] Docker image version pinned
- [ ] Version documented in `README.md`
- [ ] Version documented in the service audit
- [ ] `.env` and `.env.example` use the approved image tag

---

# Docker Compose Review

- [ ] `compose.yml` exists
- [ ] Image is defined using environment variables
- [ ] Container name is defined
- [ ] Restart policy is configured
- [ ] Required Docker networks are configured
- [ ] Required ports are configured
- [ ] Persistent storage is configured
- [ ] Runtime paths and volumes have been verified
- [ ] `docker compose config` completes successfully
- [ ] Containers start successfully
- [ ] Container health and logs have been reviewed

---

# Environment File Review

- [ ] `.env` exists in the production service directory
- [ ] `.env.example` exists in the repository
- [ ] `.env` is excluded from Git
- [ ] `.env.example` contains no production secrets
- [ ] Environment sections follow `ENVIRONMENT_STANDARD.md`
- [ ] Only applicable category headers are included
- [ ] Placeholder values are used where secrets are required
- [ ] Placeholder environment header is included when no secrets are used
- [ ] `.env` and `.env.example` contain matching variable names

---

# Git Exclusion Review

- [ ] Service-specific `.gitignore` exists
- [ ] `.env` is ignored
- [ ] Runtime data is ignored
- [ ] Database files are ignored
- [ ] Backup directories and files are ignored
- [ ] Logs and temporary files are ignored
- [ ] Certificates and private keys are ignored where applicable
- [ ] No secrets are currently tracked by Git

---

# README Review

- [ ] `README.md` exists
- [ ] README follows `README_TEMPLATE.md`
- [ ] Service metadata is complete
- [ ] Overview is accurate
- [ ] Purpose is documented
- [ ] Components are documented
- [ ] Docker image and version are documented
- [ ] Environment variables are documented
- [ ] Persistent data is documented
- [ ] Networking is documented
- [ ] Security notes are documented
- [ ] Deployment commands are documented
- [ ] Documentation path is correct
- [ ] Final line is `README Template v1.0`

---

# Audit Review

- [ ] Service audit exists in `docs/audits/`
- [ ] Audit follows `AUDIT_TEMPLATE.md`
- [ ] Executive Summary is complete
- [ ] Service Overview is complete
- [ ] Docker Images section is complete
- [ ] Deployment Review is complete
- [ ] Security Review is complete
- [ ] Documentation Review is complete
- [ ] Improvements Completed is complete
- [ ] Audit Result is complete
- [ ] Final line is `Audit Template v1.0`

---

# Repository Copy Review

- [ ] Repository service directory exists
- [ ] `compose.yml` has been copied
- [ ] `.env.example` has been copied
- [ ] `.gitignore` has been copied
- [ ] `README.md` has been copied
- [ ] Additional safe configuration files have been copied
- [ ] Production `.env` was not copied
- [ ] Runtime data was not copied
- [ ] Backup data was not copied

---

# Final Git Review

- [ ] `git status` reviewed
- [ ] Staged file list reviewed
- [ ] No `.env` files staged
- [ ] No database files staged
- [ ] No runtime directories staged
- [ ] No certificates or private keys staged
- [ ] No passwords, tokens, or secrets staged
- [ ] Commit message accurately describes the completed work
- [ ] Repository is ready to push

---

# Review Result

**Status:**  
- [ ] Passed
- [ ] Passed after approved corrections
- [ ] Requires additional work

**Notes:**

---

Service Review Checklist v1.0
