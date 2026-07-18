#!/usr/bin/env bash
#
# ==============================================================================
# RevChatham Homelab
#
# Recovery Automation Library
# Library: recovery_point.sh
# Version: 1.0.0
#
# Purpose:
# Creates and manages Recovery Point identifiers and directories.
# ==============================================================================

get_next_recovery_point_id() {

    local DATE_PREFIX
    local NEXT_NUMBER

    DATE_PREFIX="$(date +%Y%m%d)"

    NEXT_NUMBER=$(
    find "${RECOVERY_ROOT}/output" \
    -maxdepth 1 \
    -type d \
    -name "RP-${DATE_PREFIX}-[0-9][0-9][0-9]" |
    sed -E "s/.*RP-${DATE_PREFIX}-([0-9]{3})$/\1/" |
    sort -n |
    tail -1
    )

    if [[ -z "${NEXT_NUMBER}" ]]; then
        NEXT_NUMBER=1
    else
        NEXT_NUMBER=$((10#${NEXT_NUMBER} + 1))
    fi

    printf -v NEXT_NUMBER "%03d" "${NEXT_NUMBER}"

    RECOVERY_POINT_ID="RP-${DATE_PREFIX}-${NEXT_NUMBER}"

    export RECOVERY_POINT_ID
}


create_recovery_point() {

    get_next_recovery_point_id

    RECOVERY_POINT_PATH="${RECOVERY_ROOT}/output/${RECOVERY_POINT_ID}"

    if [[ -e "${RECOVERY_POINT_PATH}" ]]; then
        echo "ERROR: Recovery Point already exists:"
        echo "${RECOVERY_POINT_ID}"
        return 1
    fi

    mkdir -p "${RECOVERY_POINT_PATH}"

    mkdir -p "${RECOVERY_POINT_PATH}/documentation"
    mkdir -p "${RECOVERY_POINT_PATH}/docker"
    mkdir -p "${RECOVERY_POINT_PATH}/proxmox"
    mkdir -p "${RECOVERY_POINT_PATH}/manifest"
    mkdir -p "${RECOVERY_POINT_PATH}/checksums"
    mkdir -p "${RECOVERY_POINT_PATH}/verification"
    mkdir -p "${RECOVERY_POINT_PATH}/logs"

    export RECOVERY_POINT_PATH

    echo "Recovery Point ID : ${RECOVERY_POINT_ID}"
    echo "Recovery Point    : ${RECOVERY_POINT_PATH}"

    return 0
}
