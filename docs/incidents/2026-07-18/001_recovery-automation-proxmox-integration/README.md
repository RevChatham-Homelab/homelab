# Recovery Automation Proxmox Integration Incident

## Incident Information

**Project:** RevChatham Homelab

**Date:** 2026-07-18

**Incident ID:** INC-20260718-001

**Severity:** Medium

**Status:** Resolved

**Affected Component:** Recovery Automation

**Affected Systems:**

-   Ubuntu Server VM
-   Proxmox Host

------------------------------------------------------------------------

# Summary

During development of the Recovery Automation system, the Proxmox
collection phase failed while attempting to collect virtualization host
information.

The Recovery Automation workflow successfully created Recovery Points,
backed up documentation, and backed up Docker service configurations.

Failure occurred when the automation attempted to collect Proxmox
metadata.

------------------------------------------------------------------------

# Symptoms

The Recovery Automation process stopped during:

    Collecting Proxmox information...

Initial error:

    bash: line 5: qm: command not found

After correcting command paths, the following error appeared:

    ipcc_send_rec[1] failed: Is a directory
    ipcc_send_rec[2] failed: Is a directory
    ipcc_send_rec[3] failed: Is a directory
    Unable to load access control list: Is a directory

------------------------------------------------------------------------

# Investigation

## SSH Authentication

Verified the dedicated recovery account could authenticate successfully.

Test:

    ssh proxmox-recovery hostname

Result:

    proxmox

SSH key authentication was successful.

------------------------------------------------------------------------

## Command Path Validation

Verified Proxmox command locations:

    /usr/sbin/qm
    /usr/sbin/pvesm
    /usr/bin/pveversion

Automation was updated to use absolute command paths.

------------------------------------------------------------------------

## Permission Investigation

The recovery account could access the Proxmox host but did not have
sufficient permissions to query Proxmox management services.

Affected commands:

    qm list
    pvesm status

------------------------------------------------------------------------

# Root Cause

Recovery Automation had working SSH connectivity but lacked a defined
privilege model for collecting Proxmox metadata.

------------------------------------------------------------------------

# Resolution

Implemented a dedicated Proxmox recovery service account.

Created:

    recovery@proxmox

Configured:

    SSH key authentication

Configured SSH alias:

    proxmox-recovery

Added restricted sudo access for:

    /usr/sbin/qm
    /usr/sbin/pvesm
    /usr/bin/pveversion

------------------------------------------------------------------------

# Validation

Successful tests:

    ssh proxmox-recovery "sudo /usr/sbin/qm list"

Returned VM inventory successfully.

    ssh proxmox-recovery "sudo /usr/sbin/pvesm status"

Returned Proxmox storage information successfully.

------------------------------------------------------------------------

# Lessons Learned

-   SSH authentication does not equal application authorization.
-   Infrastructure automation requires explicit privilege design.
-   Automation should use dedicated service accounts.
-   Absolute command paths prevent environment-related failures.
-   Recovery workflows should validate each phase independently.

------------------------------------------------------------------------

# Future Improvements

-   Replace sudo-based collection with Proxmox API token authentication.
-   Add automated permission validation before execution.
-   Add Proxmox connectivity checks before backup phases.

------------------------------------------------------------------------

# Final Status

Resolved.

Recovery Automation can now authenticate to Proxmox and collect required
infrastructure metadata using a dedicated recovery service account.

---

# Documentation Metadata

**Document Type:**  
Incident Report

**Project:**  
RevChatham Homelab

**Category:**  
Recovery Automation

**Related Components:**

- Proxmox
- Ubuntu Server VM
- Recovery Automation
- SSH Authentication
- Sudo Privilege Management

**Resolution Date:**  
2026-07-18

**Document Status:**  
Closed

**Maintained By:** 
RevChatham Homelab Documentation

---

# End of Incident Report
