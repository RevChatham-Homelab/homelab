# RevChatham Homelab Recovery Manager

**Project:** RevChatham Homelab

**Document:** Recovery Manager README

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-22

**Status:** Draft

---

# Overview

The RevChatham Homelab Recovery Manager is the operator-facing console for the Recovery Automation Framework.

It provides a single, consistent interface for generating, copying, browsing, sanitizing, verifying, and reviewing Recovery Points. It also provides controlled access to Recovery Manager audit information and safe Git repository workflows.

The Recovery Manager is not intended to replace the Recovery Automation Framework.

The Recovery Automation Framework remains the recovery engine.

The Recovery Manager provides the convenient, guided interface through which authorized users operate that engine.

---

# Purpose

The Recovery Manager exists to make recovery operations:

- Simple
- Consistent
- Verifiable
- Auditable
- Accessible to authorized users
- Resistant to accidental misuse

The tool should reduce repetitive work without removing accountability or human judgment.

---

# Entry Point

The Recovery Manager will be launched from the root of the repository:

```text
~/homelab/recovery-manager.py
```

Typical execution:

```bash
cd ~/homelab
./recovery-manager.py
```

The entry point remains directly accessible from the repository root so that it can be located and used quickly during routine operations or recovery events.

---

# Relationship to the Recovery Automation Framework

```text
Recovery Manager
        |
        v
Recovery Automation Framework
        |
        v
Recovery Point Generation
Verification
Sanitization
Backup Copying
Operational Logging
```

The Recovery Manager coordinates approved framework operations but does not replace the framework's underlying scripts, verification logic, or Recovery Point standards.

---

# Approved Main Menu

```text
========================================================================
                RevChatham Homelab Recovery Manager
========================================================================

 Repository : ~/homelab
 Framework  : Recovery Automation Framework v1.0
 Status     : Ready

 Latest Recovery Point:
   RP-YYYYMMDD-###
   Created: YYYY-MM-DD HH:MM
   Size: 00 MB

========================================================================

 1. Generate a Recovery Point

 2. Generate a Recovery Point and Backup

 3. Sanitize an Existing Recovery Point

 4. Browse Recovery Points

 5. Verify Recovery Point

 6. Recovery Statistics

 7. GitHub Repository

 8. Exit
========================================================================
```

The number `8` is the universal navigation control for:

- Back
- Cancel
- Exit

---

# Recovery Point Generation and Backup

Recovery Points are always generated on the server first.

The approved backup destination menu is:

```text
1. Server, Flash Drive, T14
2. Server, Flash Drive
3. Server, T14
8. Back
```

The server copy is always retained, even when a secondary destination fails.

A failed copy to a flash drive or the Lenovo T14 must never remove or invalidate the server copy.

---

# Browsing Recovery Points

The user-facing term is:

```text
Browse Recovery Points
```

The interface displays five Recovery Points at a time.

Example:

```text
1. RP-20260722-004
2. RP-20260721-009
3. RP-20260721-008
4. RP-20260721-007
5. RP-20260721-006

6. Older 5
7. Newer 5
8. Back
```

The same five-item selection pattern is used when choosing a Recovery Point for sanitization or verification.

---

# GitHub Repository Menu

The approved GitHub Repository submenu is:

```text
========================================================================
                         GitHub Repository
========================================================================

 1. Show Git Status
 2. Show Recent Commits
 3. Commit Changes
 4. Push to GitHub
 5. Commit and Push
 6. Pull from GitHub
 7. Pull, Commit, and Push
 8. Back
========================================================================
```

Approved safe commands include:

```bash
git status --short
git status -sb
git log --oneline --decorate -10
git pull --ff-only
```

Automatic merge resolution is intentionally disabled.

The Recovery Manager must display the following warning when local and remote branches have diverged:

```text
------------------------------------------------------------------------
Note:
If the local and remote branches have diverged, STOP and consult the
project manager before proceeding. Automatic merge resolution is
intentionally disabled.
------------------------------------------------------------------------
```

The Recovery Manager must never automatically rewrite Git history.

---

# Audit and Access Control

The Recovery Manager maintains a protected audit trail of all significant operations.

The audit trail exists to support:

- Accountability
- Troubleshooting
- Operational review
- Recovery Point traceability
- Incident investigation
- Verification of completed work

## Access Policy

| Role                 | Read |            Create Entries           | Edit | Delete |
| -------------------- | :--: | :---------------------------------: | :--: | :----: |
| System Administrator |   ✅  |                  ✅                  |   ✅  |    ✅   |
| Technician           |   ✅  | ✅ *(through Recovery Manager only)* |   ❌  |    ❌   |
| Standard User        |   ❌  |                  ❌                  |   ❌  |    ❌   |

Formal documentation must use the full title **System Administrator**.

The abbreviated term `sysadmin` may be used conversationally but must not replace the formal role title in project documentation.

---

# Audit Log

The approved audit log location is:

```text
/var/log/recovery-manager.log
```

Recommended ownership:

```text
Owner: root
Group: recovery-audit
Permissions: 0640
```

Expected file representation:

```text
-rw-r----- root recovery-audit /var/log/recovery-manager.log
```

The System Administrator controls:

- Log configuration
- Log rotation
- Archival
- Administrative modification
- Administrative deletion

Approved Technicians may:

- Read the audit log
- Search the audit log
- Review failures
- Generate new entries through Recovery Manager operations

Technicians may not:

- Edit audit records
- Truncate the log
- Delete the log
- Clear prior mistakes
- Rewrite operational history

The Recovery Manager must not provide menu options to edit, clear, or delete audit records.

---

# Audit Event Submission

The Recovery Manager should submit audit events to the operating system logging service rather than writing directly to the protected audit file.

```text
Authorized User
      |
      v
Recovery Manager
      |
      v
System Logging Service
      |
      v
/var/log/recovery-manager.log
```

This design allows authorized users to generate audit events without granting them direct write access to the log file.

---

# Audit Information

Every significant operation should record:

- Audit ID
- Timestamp
- Linux username
- Hostname
- Session type
- SSH source address, when applicable
- Action
- Recovery Point ID, when applicable
- Backup destinations, when applicable
- Git branch and commit, when applicable
- Result
- Exit code
- Failure reason, when applicable

The Linux account used to perform the operation is the accountable identity.

Each user must use an individually assigned account. Shared credentials are not an acceptable accountability model.

---

# Audit ID Standard

Every Recovery Manager operation receives a unique Audit ID.

Format:

```text
AUD-YYYYMMDD-###
```

Example:

```text
AUD-20260722-003
```

The Audit ID provides a stable reference for:

- Incident reports
- Troubleshooting
- Documentation
- Recovery Point verification
- Operational review

Example entry:

```text
Audit ID: AUD-20260722-003
User: angel
Action: Generate Recovery Point
Recovery Point: RP-20260722-009
Result: SUCCESS
```

---

# User Identification

The Recovery Manager records the authenticated Linux account that launched the operation.

For normal execution:

```text
Created By: angel
```

If an account is compromised, actions taken under that account remain attributable to that account. Credential compromise is handled as a separate security incident.

The Recovery Manager is not responsible for determining the physical identity of the individual at the keyboard.

---

# Privilege Model

Normal Recovery Manager operations should not require `sudo`.

Operations expected to run without elevated privileges include:

- Generate Recovery Point
- Copy Recovery Point to approved destinations
- Browse Recovery Points
- Sanitize Recovery Point
- Verify Recovery Point
- Review Recovery Statistics
- Review the Audit Log
- Show Git status
- Show recent commits
- Commit changes
- Push changes
- Pull changes

Future actions involving system services, protected storage, Docker administration, or restore operations may require controlled elevation.

Privilege escalation must remain explicit.

The Recovery Manager must not silently elevate privileges.

---

# Operational Behavior

Every meaningful operation must:

1. State what is about to occur.
2. Require confirmation when the action could overwrite, alter, or publish data.
3. Perform the approved action.
4. Record the authenticated user.
5. Assign an Audit ID.
6. Record success or failure.
7. Display a clear result.
8. Return the user to the appropriate menu.

The Recovery Manager must never silently hide an error.

---

# Design Principles

- Recovery should be simple.
- Verify before trusting.
- Never overwrite without confirmation.
- Never hide errors.
- Recovery Points should be reproducible.
- Git history is never rewritten automatically.
- When in doubt, STOP and investigate.
- Convenience must not eliminate accountability.
- Authorized users should receive only the access required for their role.
- Operational history must remain reviewable and protected.

---

# Planned Capabilities

The Recovery Manager roadmap may include:

- Recovery Point generation
- Multi-destination backup
- Recovery Point browsing
- Recovery Point sanitization
- Recovery Point verification
- Recovery statistics
- Audit Log review
- GitHub repository operations
- Recovery Point comparison
- Restore assistance
- Settings
- Configuration validation
- Version information
- Structured error reporting

Each planned capability must follow the RevChatham Development Standard before implementation.

---

# Development Status

The Recovery Manager remains under design.

Approved requirements documented in this README must be reviewed against the implementation before the tool is released as version 1.0.0.

---

# Related Documentation

- `automation/recovery/README.md`
- `automation/recovery/ARCHITECTURE.md`
- `docs/BACKUP_RESTORE_RECOVER/RECOVERY_POINT_STANDARD.md`
- `docs/engineering/REVCHATHAM_DEVELOPMENT_STANDARD.md`
- Recovery Manager Design Specification
- Recovery Automation Framework Implementation Documentation

---

Recovery Manager README v1.0.0
