# Offsite Backup Procedure

**Project:** RevChatham Homelab

**Document:** Offsite Backup Procedure

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-13

**Status:** Operational

---

# Purpose

This document defines the approved procedure for maintaining offsite backups of the RevChatham Homelab.

The objective is to ensure that Recovery Points remain available following catastrophic events such as hardware failure, theft, fire, flood, or other incidents affecting the primary homelab location.

---

# Backup Philosophy

Recovery Points are first created and verified locally.

Only verified Recovery Points are eligible for offsite storage.

Offsite backups provide geographic redundancy and are considered a critical component of the overall disaster recovery strategy.

---

# Approved Offsite Media

Current approved media include:

- Lenovo ThinkPad T14
- External USB storage

Future approved media may include:

- Network Attached Storage (NAS)
- Secure cloud storage

---

# Backup Procedure

1. Verify the Recovery Point is complete.

2. Confirm all verification checks have passed.

3. Copy the Recovery Point to the selected offsite storage device.

4. Verify the copied files.

5. Record the backup date and destination.

---

# Verification

Confirm:

- Recovery Point copied successfully.
- Directory structure matches the source.
- Files are readable.
- Checksums match the original Recovery Point.

---

# Restore Procedure

1. Locate the required Recovery Point.

2. Copy the Recovery Point to the recovery workstation.

3. Verify the Recovery Point integrity.

4. Continue recovery using:

- DISASTER_RECOVERY.md
- SYSTEM_RECOVERY_MANUAL.md

---

# Recovery Validation

Offsite recovery preparation is complete when:

- Recovery Point is available.
- Recovery Point integrity is verified.
- Recovery procedures may begin.

---

# Notes

At the time of publication, offsite backups are performed manually.

Future automation may assist with verification and reporting, but transfer to removable media will remain a manual process unless otherwise approved.

---

Offsite Backup Procedure v1.0.0
