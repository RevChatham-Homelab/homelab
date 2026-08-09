#!/usr/bin/env bash
#
# ==============================================================================
# RevChatham Homelab
#
# Recovery Automation Library
# Library: logging.sh
# Version: 1.0.0
#
# Purpose:
# Creates and manages Recovery Automation execution logs.
# ==============================================================================

create_execution_log() {

    LOG_FILE="${RECOVERY_POINT_PATH}/logs/recovery.log"

    touch "${LOG_FILE}"

    {
        echo "============================================================"
        echo "Recovery Automation Execution Log"
        echo "============================================================"
        echo "Recovery Point ID : ${RECOVERY_POINT_ID}"
        echo "Started           : $(date)"
        echo
    } >> "${LOG_FILE}"

    echo "Execution Log : ${LOG_FILE}"

    return 0
}

log_message() {

    local LEVEL="${1:-INFO}"
    local MESSAGE="${2:-}"

    case "${LEVEL}" in
        INFO|WARN|ERROR)
            ;;
        *)
            MESSAGE="${LEVEL}${MESSAGE:+ ${MESSAGE}}"
            LEVEL="INFO"
            ;;
    esac

    echo "[${LEVEL}] ${MESSAGE}"

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [${LEVEL}] ${MESSAGE}" >> "${LOG_FILE}"
}
