#!/usr/bin/env bash
#
# ==============================================================================
# RevChatham Homelab
#
# Recovery Automation Library
# Library: docker.sh
# Version: 1.0.0
#
# Purpose:
# Creates Docker deployment backups for Recovery Points.
# ==============================================================================

backup_docker() {

    local DOCKER_SOURCE
    local DOCKER_DESTINATION

    DOCKER_SOURCE="${RECOVERY_ROOT}/../.."
    DOCKER_DESTINATION="${RECOVERY_POINT_PATH}/docker"

    local DOCKER_SERVICES=(
        authentik
        grafana
        homepage
        nginx-proxy-manager
        pihole
        portainer
        prometheus
        uptime-kuma
        website
    )

    echo "Creating Docker backup..."

    mkdir -p "${DOCKER_DESTINATION}"

    for SERVICE in "${DOCKER_SERVICES[@]}"; do

        if [[ -d "${DOCKER_SOURCE}/${SERVICE}" ]]; then

            echo "Backing up ${SERVICE}..."

            mkdir -p "${DOCKER_DESTINATION}/${SERVICE}"

            rsync -a \
                --include="compose.yml" \
                --include="docker-compose.yml" \
                --include=".env.example" \
                --include="README.md" \
                --exclude="*" \
                "${DOCKER_SOURCE}/${SERVICE}/" \
                "${DOCKER_DESTINATION}/${SERVICE}/"

        else

            echo "Warning: ${SERVICE} directory not found."

        fi

    done

    echo "Docker backup created."

    update_manifest_status "Docker Backup" "Complete"

    return 0
}
