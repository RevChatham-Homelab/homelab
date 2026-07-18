#!/usr/bin/env bash
#
# ==============================================================================
# RevChatham Homelab
#
# Recovery Automation Library
# Library: documentation.sh
# Version: 1.0.0
#
# Purpose:
# Creates documentation backups for Recovery Points.
# ==============================================================================

backup_documentation() {

    local DOCUMENTATION_SOURCE
    local DOCUMENTATION_DESTINATION

    DOCUMENTATION_SOURCE="${RECOVERY_ROOT}/../../docs"
    DOCUMENTATION_DESTINATION="${RECOVERY_POINT_PATH}/documentation"

    echo "Creating documentation backup..."

    if tar -czf \
       "${DOCUMENTATION_DESTINATION}/documentation.tar.gz" \
       -C "${DOCUMENTATION_SOURCE}/.." \
       "$(basename "${DOCUMENTATION_SOURCE}")"
    then
	echo "Documentation backup created."

	update_manifest_status "Documentation" "Complete"
    else
       rm -f "${DOCUMENTATION_DESTINATION}/documentation.tar.gz"
       echo "Documentation backup failed."
    return 1
    fi

    return 0
}
