#!/usr/bin/env bash
#
# ==============================================================================
# RevChatham Homelab
#
# Recovery Automation Library
# Library: manifest.sh
# Version: 1.0.0
#
# Purpose:
# Generates Recovery Point manifest files.
# ==============================================================================

generate_manifest() {

    MANIFEST_FILE="${RECOVERY_POINT_PATH}/manifest/${RECOVERY_POINT_ID}_MANIFEST.md"

    cat <<EOF > "${MANIFEST_FILE}"
# Recovery Point Manifest

**Project:** RevChatham Homelab

**Recovery Point:** ${RECOVERY_POINT_ID}

**Created:** $(date)

**Automation Version:** 1.0.0

---

# Contents

| Component | Status |
|-----------|--------|
| Documentation | Pending |
| Docker Backup | Pending |
| Proxmox Backup | Pending |
| Checksums | Pending |
| Verification | Pending |

---

# Recovery Point Status

Status:

Under Construction
EOF

    export MANIFEST_FILE

    echo "Manifest : ${MANIFEST_FILE}"

    return 0
}

update_manifest_status() {
    local COMPONENT="$1"
    local STATUS="$2"
    sed -i \
    "s/| ${COMPONENT} | Pending |/| ${COMPONENT} | ${STATUS} |/" \
    "${MANIFEST_FILE}"
    return 0
}
finalize_manifest() {

    sed -i \
    "s/Under Construction/Complete/" \
    "${MANIFEST_FILE}"

    return 0
}
