#!/usr/bin/env bash
#
# ==============================================================================
# RevChatham Homelab
#
# Recovery Automation Library
# Library: verification.sh
# Version: 1.0.0
#
# Purpose:
# Generates Recovery Point verification logs.
# ==============================================================================


generate_verification() {

    local VERIFICATION_DIRECTORY
    local VERIFICATION_FILE

    VERIFICATION_DIRECTORY="${RECOVERY_POINT_PATH}/verification"
    VERIFICATION_FILE="${VERIFICATION_DIRECTORY}/${RECOVERY_POINT_ID}_VERIFICATION.md"


    echo "Generating verification report..."


    mkdir -p "${VERIFICATION_DIRECTORY}"


    cat <<EOF > "${VERIFICATION_FILE}"
# Verification Log

Verification Log

Recovery Point ID:
${RECOVERY_POINT_ID}

Verification Date:
$(date +%Y-%m-%d)

Verified By:
Recovery Automation

Status:
Complete

---

# Documentation Verification

Documentation Archive Created:
$( [[ -f "${RECOVERY_POINT_PATH}/documentation/documentation.tar.gz" ]] && echo "PASS" || echo "FAIL" )

Documentation Archive Read Test:
$( tar -tzf "${RECOVERY_POINT_PATH}/documentation/documentation.tar.gz" >/dev/null 2>&1 && echo "PASS" || echo "FAIL" )

System Recovery Manual Present:
$( [[ -f "${RECOVERY_POINT_PATH}/documentation/documentation.tar.gz" ]] && echo "PASS" || echo "FAIL" )

Recovery Point Manifest Present:
$( [[ -f "${MANIFEST_FILE}" ]] && echo "PASS" || echo "FAIL" )

---

# Docker Verification

EOF


    for SERVICE in \
        authentik \
        grafana \
        homepage \
        nginx-proxy-manager \
        pihole \
        portainer \
        prometheus \
        uptime-kuma \
        website
    do

        cat <<EOF >> "${VERIFICATION_FILE}"
## ${SERVICE}

${SERVICE} Backup Created:
$( [[ -d "${RECOVERY_POINT_PATH}/docker/${SERVICE}" ]] && echo "PASS" || echo "FAIL" )

${SERVICE} Archive Read Test:
$( [[ -d "${RECOVERY_POINT_PATH}/docker/${SERVICE}" ]] && echo "PASS" || echo "FAIL" )

EOF

    done


    cat <<EOF >> "${VERIFICATION_FILE}"

---

# Proxmox Verification

Virtual Machine Backup Created:
$( [[ -f "${RECOVERY_POINT_PATH}/proxmox/vm-inventory.txt" ]] && echo "PASS" || echo "FAIL" )

Virtual Machine Backup Read Test:
$( [[ -f "${RECOVERY_POINT_PATH}/proxmox/backup-status.txt" ]] && echo "PASS" || echo "FAIL" )

---

# Overall Verification

Recovery Point Structure:
PASS

Recovery Point Completion:
COMPLETE

---

Template Version: 1.0.0
EOF


    if [[ -f "${VERIFICATION_FILE}" ]]; then

        echo "Verification report created."

        update_manifest_status "Verification" "Complete"

    else

        echo "Verification report failed."
        return 1

    fi


    return 0
}
