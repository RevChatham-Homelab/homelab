#!/usr/bin/env bash
#
# ==============================================================================
# RevChatham Homelab
#
# Recovery Automation Library
# Library: checksum.sh
# Version: 1.0.0
#
# Purpose:
# Generates SHA256 checksums for Recovery Points.
# ==============================================================================


generate_checksums() {

    local CHECKSUM_DIRECTORY
    local CHECKSUM_FILE

    CHECKSUM_DIRECTORY="${RECOVERY_POINT_PATH}/checksums"
    CHECKSUM_FILE="${CHECKSUM_DIRECTORY}/SHA256SUMS.txt"


    echo "Generating checksums..."


    mkdir -p "${CHECKSUM_DIRECTORY}"


    find \
        "${RECOVERY_POINT_PATH}" \
        -type f \
        ! -path "${CHECKSUM_DIRECTORY}/*" \
        ! -path "${RECOVERY_POINT_PATH}/logs/*" \
        ! -path "${RECOVERY_POINT_PATH}/verification/*" \
        ! -path "${RECOVERY_POINT_PATH}/manifest/*" \
        -print0 |
    sort -z |
    xargs -0 sha256sum > "${CHECKSUM_FILE}"


    if [[ -f "${CHECKSUM_FILE}" ]]; then

        echo "Checksum file created."

        update_manifest_status "Checksums" "Complete"

    else

        echo "Checksum generation failed."
        return 1

    fi


    return 0
}
