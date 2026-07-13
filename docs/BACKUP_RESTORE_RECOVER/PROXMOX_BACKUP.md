# Proxmox Backup Procedure

**Project:** RevChatham Homelab

**Document:** Proxmox Backup Procedure

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-13

**Status:** Operational

---

# Purpose

This document defines the approved procedure for protecting and restoring the Proxmox Virtual Environment (PVE) and its hosted virtual machines.

The objective is to ensure that virtual machine backups are created, verified, documented, and referenced by the appropriate Recovery Point.

---

# Backup Philosophy

Proxmox backups are the authoritative backups for virtual machines.

Recovery Points document and verify those backups but do not duplicate the VM backup files.

This approach minimizes storage requirements while maintaining complete recovery documentation.

---

# Backup Scope

The Proxmox backup process includes:

- Virtual machine backup
- Backup log
- SHA-256 verification
- Recovery Point documentation
- Recovery Point verification

The following items are intentionally excluded:

- Recovery Point archives
- Docker service backups
- GitHub repository backups

---

# Backup Procedure

1. Log in to the Proxmox host.

2. Verify the virtual machine is running.

```bash
qm list
```

3. Create the virtual machine backup.

Example:

```bash
vzdump 100 --mode snapshot --compress zstd
```

4. Verify the backup exists.

```bash
ls -lh /var/lib/vz/dump
```

5. Generate SHA-256 Checksums

Generate SHA-256 Checksums for both the Proxmox backup log and the virtual machine backup.

Example:

```bash
sha256sum \
/var/lib/vz/dump/vzdump-qemu-100-YYYY_MM_DD-HH_MM_SS.log \
/var/lib/vz/dump/vzdump-qemu-100-YYYY_MM_DD-HH_MM_SS.vma.zst
```

Record both SHA-256 values in:

- RP_MANIFEST.md
- checksums.sha256

6. Record the following in the Recovery Point:

- VMID
- VM Name
- Backup Type
- Backup Filename
- Backup Log Filename
- Backup Location
- SHA-256 values
- Verification Status

7. Update:

- RP_MANIFEST.md
- verification.log
- checksums.sha256

---

# Verification

Confirm:

- Backup completed successfully.
- Backup log exists.
- Backup file exists.
- SHA-256 hashes generated.
- Recovery Point updated.
- Verification log updated.

---

# Restore Procedure

1. Verify the correct Recovery Point.

2. Locate the referenced VM backup.

3. Restore the virtual machine using Proxmox.

Example:

```bash
qmrestore <backup-file> <new-vmid>
```

4. Start the restored VM.

5. Verify networking.

6. Continue recovery using the System Recovery Manual.

---

# Recovery Validation

Recovery is complete when:

- Virtual machine restores successfully.
- VM boots normally.
- Network connectivity is restored.
- Docker services are accessible.
- Recovery continues according to the approved recovery sequence.

---

End of Proxmox Backup Procedure
