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
# Generates Recovery Point verification reports and terminal summaries.
# ==============================================================================


VERIFICATION_RESULTS=()
VERIFICATION_OVERALL_STATUS="PASS"
VERIFICATION_FILE=""


record_verification_result() {

    local CHECK_NAME="$1"
    local CHECK_STATUS="$2"

    VERIFICATION_RESULTS+=("${CHECK_NAME}|${CHECK_STATUS}")

    if [[ "${CHECK_STATUS}" != "PASS" ]]; then
        VERIFICATION_OVERALL_STATUS="FAIL"
    fi
}


write_verification_result() {

    local CHECK_NAME="$1"
    local CHECK_STATUS="$2"
    local OUTPUT_FILE="$3"

    printf '%s:\n%s\n\n' \
        "${CHECK_NAME}" \
        "${CHECK_STATUS}" \
        >> "${OUTPUT_FILE}"
}


print_recovery_verification_summary() {

    local RESULT
    local CHECK_NAME
    local CHECK_STATUS

    printf '\n'
    printf '%s\n' "============================================================"
    printf '%s\n' "Recovery Verification Summary"
    printf '%s\n' "============================================================"

    for RESULT in "${VERIFICATION_RESULTS[@]}"; do

        IFS='|' read -r CHECK_NAME CHECK_STATUS <<< "${RESULT}"

        printf '%-44s | %s\n' \
            "${CHECK_NAME}" \
            "${CHECK_STATUS}"

    done

    printf '%s\n' "------------------------------------------------------------"
    printf '%-44s | %s\n' \
        "Overall Verification Status" \
        "${VERIFICATION_OVERALL_STATUS}"
    printf '%s\n' "============================================================"
}


generate_verification() {

    local VERIFICATION_DIRECTORY
    local DOCUMENTATION_ARCHIVE
    local CHECK_NAME
    local CHECK_STATUS
    local SERVICE
    local SERVICE_DIRECTORY
    local SERVICE_COMPOSE_FILE
    local RECOVERY_STRUCTURE_STATUS

    VERIFICATION_DIRECTORY="${RECOVERY_POINT_PATH}/verification"
    VERIFICATION_FILE="${VERIFICATION_DIRECTORY}/${RECOVERY_POINT_ID}_VERIFICATION.md"
    DOCUMENTATION_ARCHIVE="${RECOVERY_POINT_PATH}/documentation/documentation.tar.gz"

    VERIFICATION_RESULTS=()
    VERIFICATION_OVERALL_STATUS="PASS"

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

---

# Documentation Verification

EOF

    CHECK_NAME="Documentation Archive Created"

    if [[ -f "${DOCUMENTATION_ARCHIVE}" ]]; then
        CHECK_STATUS="PASS"
    else
        CHECK_STATUS="FAIL"
    fi

    record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
    write_verification_result \
        "${CHECK_NAME}" \
        "${CHECK_STATUS}" \
        "${VERIFICATION_FILE}"


    CHECK_NAME="Documentation Archive Read Test"

    if [[ -f "${DOCUMENTATION_ARCHIVE}" ]] &&
       tar -tzf "${DOCUMENTATION_ARCHIVE}" >/dev/null 2>&1; then
        CHECK_STATUS="PASS"
    else
        CHECK_STATUS="FAIL"
    fi

    record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
    write_verification_result \
        "${CHECK_NAME}" \
        "${CHECK_STATUS}" \
        "${VERIFICATION_FILE}"


    CHECK_NAME="System Recovery Manual Present"

    if [[ -f "${DOCUMENTATION_ARCHIVE}" ]] &&
       tar -tzf "${DOCUMENTATION_ARCHIVE}" 2>/dev/null |
           grep -E '(^|/)SYSTEM_RECOVERY_MANUAL\.md$' >/dev/null; then
        CHECK_STATUS="PASS"
    else
        CHECK_STATUS="FAIL"
    fi

    record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
    write_verification_result \
        "${CHECK_NAME}" \
        "${CHECK_STATUS}" \
        "${VERIFICATION_FILE}"


    CHECK_NAME="Recovery Point Manifest Present"

    if [[ -f "${MANIFEST_FILE}" ]]; then
        CHECK_STATUS="PASS"
    else
        CHECK_STATUS="FAIL"
    fi

    record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
    write_verification_result \
        "${CHECK_NAME}" \
        "${CHECK_STATUS}" \
        "${VERIFICATION_FILE}"


    cat <<EOF >> "${VERIFICATION_FILE}"
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

        SERVICE_DIRECTORY="${RECOVERY_POINT_PATH}/docker/${SERVICE}"

        if [[ -f "${SERVICE_DIRECTORY}/compose.yml" ]]; then
            SERVICE_COMPOSE_FILE="${SERVICE_DIRECTORY}/compose.yml"
        elif [[ -f "${SERVICE_DIRECTORY}/docker-compose.yml" ]]; then
            SERVICE_COMPOSE_FILE="${SERVICE_DIRECTORY}/docker-compose.yml"
        else
            SERVICE_COMPOSE_FILE=""
        fi

        printf '## %s\n\n' "${SERVICE}" >> "${VERIFICATION_FILE}"


        CHECK_NAME="${SERVICE} Backup Created"

        if [[ -d "${SERVICE_DIRECTORY}" ]] &&
           find "${SERVICE_DIRECTORY}" -mindepth 1 -type f -print -quit |
               grep -q .; then
            CHECK_STATUS="PASS"
        else
            CHECK_STATUS="FAIL"
        fi

        record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
        write_verification_result \
            "${CHECK_NAME}" \
            "${CHECK_STATUS}" \
            "${VERIFICATION_FILE}"


        CHECK_NAME="${SERVICE} Compose File Read Test"

        if [[ -n "${SERVICE_COMPOSE_FILE}" ]] &&
           [[ -r "${SERVICE_COMPOSE_FILE}" ]] &&
           [[ -s "${SERVICE_COMPOSE_FILE}" ]]; then
            CHECK_STATUS="PASS"
        else
            CHECK_STATUS="FAIL"
        fi

        record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
        write_verification_result \
            "${CHECK_NAME}" \
            "${CHECK_STATUS}" \
            "${VERIFICATION_FILE}"

    done


    cat <<EOF >> "${VERIFICATION_FILE}"
---

# Proxmox Verification

EOF

    CHECK_NAME="Virtual Machine Inventory Created"

    if [[ -s "${RECOVERY_POINT_PATH}/proxmox/vm-inventory.txt" ]]; then
        CHECK_STATUS="PASS"
    else
        CHECK_STATUS="FAIL"
    fi

    record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
    write_verification_result \
        "${CHECK_NAME}" \
        "${CHECK_STATUS}" \
        "${VERIFICATION_FILE}"


    CHECK_NAME="Backup Status Report Created"

    if [[ -s "${RECOVERY_POINT_PATH}/proxmox/backup-status.txt" ]]; then
        CHECK_STATUS="PASS"
    else
        CHECK_STATUS="FAIL"
    fi

    record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
    write_verification_result \
        "${CHECK_NAME}" \
        "${CHECK_STATUS}" \
        "${VERIFICATION_FILE}"


    CHECK_NAME="Proxmox Host Information Created"

    if [[ -s "${RECOVERY_POINT_PATH}/proxmox/host-information.txt" ]]; then
        CHECK_STATUS="PASS"
    else
        CHECK_STATUS="FAIL"
    fi

    record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
    write_verification_result \
        "${CHECK_NAME}" \
        "${CHECK_STATUS}" \
        "${VERIFICATION_FILE}"


    CHECK_NAME="Proxmox Storage Information Created"

    if [[ -s "${RECOVERY_POINT_PATH}/proxmox/storage-information.txt" ]]; then
        CHECK_STATUS="PASS"
    else
        CHECK_STATUS="FAIL"
    fi

    record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
    write_verification_result \
        "${CHECK_NAME}" \
        "${CHECK_STATUS}" \
        "${VERIFICATION_FILE}"


    CHECK_NAME="Checksum File Created"

    if [[ -s "${RECOVERY_POINT_PATH}/checksums/SHA256SUMS.txt" ]]; then
        CHECK_STATUS="PASS"
    else
        CHECK_STATUS="FAIL"
    fi

    record_verification_result "${CHECK_NAME}" "${CHECK_STATUS}"
    write_verification_result \
        "${CHECK_NAME}" \
        "${CHECK_STATUS}" \
        "${VERIFICATION_FILE}"


    RECOVERY_STRUCTURE_STATUS="PASS"

    for REQUIRED_DIRECTORY in \
        documentation \
        docker \
        proxmox \
        manifest \
        checksums \
        verification \
        logs
    do

        if [[ ! -d "${RECOVERY_POINT_PATH}/${REQUIRED_DIRECTORY}" ]]; then
            RECOVERY_STRUCTURE_STATUS="FAIL"
            break
        fi

    done

    CHECK_NAME="Recovery Point Structure"

    record_verification_result \
        "${CHECK_NAME}" \
        "${RECOVERY_STRUCTURE_STATUS}"

    write_verification_result \
        "${CHECK_NAME}" \
        "${RECOVERY_STRUCTURE_STATUS}" \
        "${VERIFICATION_FILE}"


    cat <<EOF >> "${VERIFICATION_FILE}"
---

# Overall Verification

Overall Status:
${VERIFICATION_OVERALL_STATUS}

Recovery Point Completion:
$( [[ "${VERIFICATION_OVERALL_STATUS}" == "PASS" ]] && echo "COMPLETE" || echo "INCOMPLETE" )

---

Template Version: 1.1.0
EOF


    if [[ ! -s "${VERIFICATION_FILE}" ]]; then

        echo "Verification report failed."
        return 1

    fi

    echo "Verification report created."

    if [[ "${VERIFICATION_OVERALL_STATUS}" == "PASS" ]]; then
        update_manifest_status "Verification" "Complete"
    else
        update_manifest_status "Verification" "Failed"
    fi

    export VERIFICATION_FILE
    export VERIFICATION_OVERALL_STATUS

    return 0
}
