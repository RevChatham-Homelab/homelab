#!/usr/bin/env bash
#
# ==============================================================================
# RevChatham Homelab
#
# Recovery Automation Library
# Library: proxmox.sh
# Version: 1.0.0
#
# Purpose:
# Collects Proxmox host recovery metadata.
# ==============================================================================

backup_proxmox() {

    local PROXMOX_DESTINATION

    PROXMOX_DESTINATION="${RECOVERY_POINT_PATH}/proxmox"

    echo "Collecting Proxmox information..."

    mkdir -p "${PROXMOX_DESTINATION}"

    echo "Collecting host information..."

    ssh proxmox-recovery "
        echo 'Proxmox Host Information'
        echo '======================='
        echo
        hostname
        echo
        sudo /usr/bin/pveversion
        echo
        uname -a
    " > "${PROXMOX_DESTINATION}/host-information.txt"


    echo "Collecting VM inventory..."

    ssh proxmox-recovery "
        echo 'Virtual Machine Inventory'
        echo '========================'
        echo
        sudo /usr/sbin/qm list
    " > "${PROXMOX_DESTINATION}/vm-inventory.txt"


    echo "Collecting storage information..."

    ssh proxmox-recovery "
        echo 'Storage Information'
        echo '=================='
        echo
        sudo /usr/sbin/pvesm status
    " > "${PROXMOX_DESTINATION}/storage-information.txt"


    echo "Collecting backup information..."

    ssh proxmox-recovery "
        echo 'Backup Information'
        echo '================='
        echo
        ls -lah /var/lib/vz/dump 2>/dev/null || echo 'No local backup directory found.'
    " > "${PROXMOX_DESTINATION}/backup-status.txt"


    echo "Proxmox information collected."

    update_manifest_status "Proxmox Backup" "Complete"

    return 0
}
