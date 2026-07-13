# GitHub Backup Procedure

**Project:** RevChatham Homelab

**Document:** GitHub Backup Procedure

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-13

**Status:** Operational

---

# Purpose

This document defines the procedure for protecting and restoring the RevChatham Homelab Git repository.

The GitHub repository serves as the authoritative source for project documentation, standards, Docker Compose files, templates, and operational procedures.

This procedure ensures that repository contents remain synchronized with the local working copy and can be restored if necessary.

---

# Backup Philosophy

GitHub is not a replacement for system backups.

GitHub protects project documentation and configuration.

Recovery Points protect the operational state of the homelab.

Both systems are required for complete recovery.

---

# Backup Scope

The GitHub repository includes:

- Documentation
- Standards
- Templates
- Docker Compose files
- Environment examples
- Service documentation
- Audit documentation
- Recovery documentation
- Architecture documentation

The following items are intentionally excluded:

- Runtime data
- Docker volumes
- Secrets
- `.env` files
- Recovery Point archives
- VM backups
- Log files
- Temporary files

---

# Backup Procedure

1. Review local repository changes.

```bash
git status
```

2. Stage approved changes.

```bash
git add .
```

3. Commit changes.

```bash
git commit -m "<descriptive commit message>"
```

4. Push to GitHub.

```bash
git push
```

5. Verify the push completed successfully.

6. Confirm GitHub reflects the latest commit.

---

# Verification

Confirm:

- Working tree is clean.
- Commit completed successfully.
- Push completed successfully.
- Repository reflects the latest commit.
- No unintended files were committed.

---

# Restore Procedure

If restoring the repository:

1. Install Git.
2. Clone the repository.

```bash
git clone <repository-url>
```

3. Verify repository contents.

4. Review project documentation.

5. Continue recovery using the System Recovery Manual.

---

# Recovery Validation

Recovery is complete when:

- Repository clones successfully.
- Directory structure matches the repository standard.
- Documentation is present.
- Compose files are present.
- Templates are present.
- Repository passes review.

---

End of GitHub Backup Procedure
