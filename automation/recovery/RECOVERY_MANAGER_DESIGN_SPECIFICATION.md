# Recovery Manager Design Specification

**Project:** RevChatham Homelab

**Document:** Recovery Manager Design Specification

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-22

**Status:** Draft

---

# Purpose

This document defines the approved design requirements for the RevChatham Homelab Recovery Manager before implementation.

It records the intended user experience, navigation model, security controls, audit behavior, Git safeguards, privilege model, and implementation boundaries.

This document defines what the Recovery Manager must do.

Implementation details may evolve, but they must remain consistent with the approved behavior documented here.

---

# Scope

The Recovery Manager is the operator console for the Recovery Automation Framework.

The initial scope includes:

- Recovery Point generation
- Recovery Point backup copying
- Recovery Point sanitization
- Recovery Point browsing
- Recovery Point verification
- Recovery statistics
- GitHub repository workflows
- Protected operational auditing

The initial scope does not include:

- Automatic Git conflict resolution
- Automatic history rewriting
- Silent privilege escalation
- Unrestricted restore operations
- Audit Log editing
- Audit Log deletion
- Shared-user accountability

---

# Entry Point Requirement

The application entry point must be located at:

```text
~/homelab/recovery-manager.py
```

The location must remain obvious and directly accessible from the repository root.

The Recovery Manager may use internal modules stored elsewhere in the repository, but the operator must not be required to remember an internal framework path.

---

# Proposed Internal Structure

```text
~/homelab/
├── recovery-manager.py
└── automation/
    └── recovery/
        ├── manager/
        │   ├── __init__.py
        │   ├── audit.py
        │   ├── backup.py
        │   ├── browse.py
        │   ├── configuration.py
        │   ├── github.py
        │   ├── recovery.py
        │   ├── statistics.py
        │   ├── ui.py
        │   ├── utils.py
        │   └── verify.py
        ├── bin/
        ├── lib/
        ├── output/
        └── output.example/
```

The internal structure may be refined during implementation.

The user-facing entry point must remain unchanged.

---

# Navigation Standard

The number `8` is the universal navigation control.

It represents:

- Back
- Cancel
- Exit

Menus must not use `0` for navigation.

The same navigation pattern must be applied consistently across the application.

---

# Main Menu Requirement

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

The header should display:

- Repository location
- Framework version
- Readiness status
- Latest Recovery Point
- Latest Recovery Point creation time
- Latest Recovery Point size

If no Recovery Point exists, the interface must state that clearly rather than displaying invalid placeholder data.

---

# Generate Recovery Point

The generation workflow must:

1. Display the intended action.
2. Identify the authenticated Linux account.
3. Assign an Audit ID.
4. Invoke the approved Recovery Point generator.
5. Detect the new Recovery Point.
6. Display the Recovery Point ID.
7. Display the server location.
8. Display verification status.
9. Record success or failure.
10. Return to the main menu.

A Recovery Point must not be reported as successful when framework verification fails.

---

# Generate Recovery Point and Backup

The approved destination menu is:

```text
1. Server, Flash Drive, T14
2. Server, Flash Drive
3. Server, T14
8. Back
```

The server copy is created first and is mandatory.

Secondary copy failures must be handled independently.

Example:

```text
Server copy: SUCCESS
Flash Drive copy: FAILED
T14 copy: SUCCESS
Overall operation: PARTIAL SUCCESS
```

A failed secondary copy must not delete, invalidate, or overwrite the server Recovery Point.

Each destination result must be recorded in the audit event.

---

# Sanitize Existing Recovery Point

The sanitize workflow displays the most recent five Recovery Points.

Example:

```text
1. RP-20260722-004
2. RP-20260721-009
3. RP-20260721-008
4. RP-20260721-007
5. RP-20260721-006

8. Back
```

The sanitizer must:

- Preserve the original Recovery Point
- Create a separate sanitized example
- Remove or replace sensitive values
- Regenerate checksums
- Verify the sanitized result
- Record the source and output identifiers
- Record success or failure

---

# Browse Recovery Points

The approved term is:

```text
Browse Recovery Points
```

The interface displays five Recovery Points per page.

Navigation:

```text
6. Older 5
7. Newer 5
8. Back
```

Each displayed Recovery Point should include, when available:

- Recovery Point ID
- Creation time
- Size
- Verification status
- Backup destination status

Selecting a Recovery Point may open a read-only detail view.

---

# Verify Recovery Point

The verification workflow must:

- Display the five most recent Recovery Points
- Allow older and newer pagination
- Run approved verification checks
- Display individual PASS or FAIL results
- Display the overall verification status
- Record the Recovery Point ID
- Record the Audit ID
- Record success or failure
- Preserve the Recovery Point

Verification must not modify Recovery Point contents unless an approved verification design explicitly requires generated verification output.

---

# Recovery Statistics

The statistics interface may display:

- Total Recovery Points
- Total storage consumed
- Most recent Recovery Point
- Oldest Recovery Point
- PASS count
- FAIL count
- Partial backup count
- Copies by destination
- Recovery Points created by user
- Recovery Points created by date range

Statistics must be derived from existing Recovery Points and protected audit data.

The statistics view must remain read-only.

---

# GitHub Repository Menu

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

Approved commands:

```bash
git status --short
git status -sb
git log --oneline --decorate -10
git pull --ff-only
```

The Git workflow must not:

- Force-push
- Automatically rebase
- Automatically merge divergent branches
- Reset local work
- Rewrite commit history
- Delete untracked files
- Discard changes without explicit approval

---

# Divergence Warning

When local and remote branches have diverged, display:

```text
------------------------------------------------------------------------
Note:
If the local and remote branches have diverged, STOP and consult the
project manager before proceeding. Automatic merge resolution is
intentionally disabled.
------------------------------------------------------------------------
```

The operation must stop after displaying the warning.

The Recovery Manager must not continue into commit, pull, push, merge, rebase, or reset behavior.

---

# Audit Architecture

The Recovery Manager submits audit events to the system logging service.

```text
Recovery Manager
      |
      v
logger or system logging API
      |
      v
system logging service
      |
      v
/var/log/recovery-manager.log
```

The application must not require direct write permission to the protected audit file.

---

# Audit Log Access Control

```text
Owner: root
Group: recovery-audit
Permissions: 0640
```

Role behavior:

| Role                 | Read |            Create Entries           | Edit | Delete |
| -------------------- | :--: | :---------------------------------: | :--: | :----: |
| System Administrator |   ✅  |                  ✅                  |   ✅  |    ✅   |
| Technician           |   ✅  | ✅ *(through Recovery Manager only)* |   ❌  |    ❌   |
| Standard User        |   ❌  |                  ❌                  |   ❌  |    ❌   |

The Recovery Manager must not provide:

- Clear Audit Log
- Delete Audit Entry
- Edit Audit Entry
- Rewrite Audit History

---

# Audit ID Requirement

Every significant operation receives an Audit ID.

Format:

```text
AUD-YYYYMMDD-###
```

Audit ID generation must avoid duplicate identifiers during concurrent or near-concurrent operations.

The implementation must use a safe sequence mechanism.

Potential approaches include:

- A protected sequence file
- A system logging sequence service
- A timestamp plus atomic counter
- A lock-protected daily sequence

The final mechanism must be documented before implementation.

---

# Required Audit Fields

Every significant operation should record:

```text
audit_id
timestamp
username
hostname
session_type
source_ip
action
recovery_point_id
backup_destinations
git_branch
git_commit
result
exit_code
details
```

Fields not applicable to an operation may be omitted or assigned a clearly defined null value.

Sensitive information must not be included in sanitized public examples.

---

# Identity Requirement

The authoritative operator identity is the authenticated Linux account.

Recommended lookup order when privilege escalation is involved:

```text
SUDO_USER
USER
getpass.getuser()
```

Normal Recovery Manager operations should not require `sudo`.

Each Technician must use an individually assigned Linux account.

Shared accounts are not permitted for accountable operations.

---

# Privilege Requirements

The initial Recovery Manager must run without elevated privileges for normal operations.

Potential future privileged operations include:

- Service restart
- Docker administration
- Protected restore actions
- Mount management
- System configuration changes
- Storage snapshot creation

Privileged operations must:

- Be explicitly identified
- Be separately approved
- Use least privilege
- Require confirmation
- Record the privilege boundary
- Record success or failure
- Never elevate silently

---

# Confirmation Requirements

Confirmation is required before:

- Overwriting an existing destination
- Publishing sanitized examples
- Creating a Git commit
- Pushing to a remote repository
- Pulling remote changes
- Beginning a privileged operation
- Starting a restore operation
- Replacing configuration
- Removing or rotating protected data

Read-only operations do not require confirmation.

---

# Error Handling

Errors must be visible.

The Recovery Manager must:

- Display the failed operation
- Display a clear error summary
- Preserve successful prior results
- Record failure in the audit trail
- Include the exit code when available
- Avoid presenting partial completion as complete success
- Return safely to the appropriate menu

The Recovery Manager must never hide errors or continue through an unsafe state.

---

# Result States

Approved result states include:

```text
SUCCESS
FAILED
PARTIAL SUCCESS
CANCELLED
BLOCKED
```

Examples:

- `SUCCESS`: Every required action completed.
- `FAILED`: The required action did not complete.
- `PARTIAL SUCCESS`: The server Recovery Point succeeded, but one or more secondary copies failed.
- `CANCELLED`: The operator intentionally cancelled the operation.
- `BLOCKED`: A safeguard prevented the operation, such as Git divergence.

---

# Implementation Standard

Implementation must follow the RevChatham Development Standard:

1. Design
2. Review
3. Document
4. Implement
5. Test
6. Verify
7. Commit
8. Release

The approved documentation must be updated when implementation behavior changes.

---

# Release Requirement

Recovery Manager version 1.0.0 may be released only after:

- Main menu behavior is complete
- Navigation is consistent
- Recovery Point generation is validated
- Backup destination behavior is validated
- Sanitization is validated
- Browsing is validated
- Verification is validated
- Git safeguards are validated
- Audit submission is validated
- Audit permissions are validated
- Technician read access is validated
- Documentation matches implementation
- Test results are recorded
- A final review is completed

---

# Open Implementation Decisions

The following details require final implementation approval:

- Audit ID concurrency mechanism
- Logging service configuration
- Audit Log rotation policy
- Technician group enrollment procedure
- Flash drive detection standard
- Lenovo T14 transfer method
- Recovery Statistics data source
- Final module layout
- Configuration file format
- Recovery Manager version display source

These are implementation details and do not invalidate the approved operational design.

---

Recovery Manager Design Specification v1.0.0
