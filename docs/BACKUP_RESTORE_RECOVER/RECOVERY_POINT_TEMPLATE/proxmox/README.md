# Proxmox Recovery Artifacts

This directory contains Proxmox-related recovery artifacts included in a Recovery Point.

Expected contents may include:

- Virtual machine backup files
- Container backup files
- Proxmox configuration exports
- Storage configuration records
- Network configuration records
- Backup job information
- Virtual machine and container inventory

Large Proxmox backup files may be stored outside the Git repository. Their storage location, filename, checksum, and recovery instructions should be recorded in `RP_MANIFEST.md`.
