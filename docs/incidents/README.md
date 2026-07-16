# Incident Documentation

**Project:** RevChatham Homelab

**Directory:** Incidents

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-15

**Status:** Operational

---

# Purpose

This directory contains incident records and troubleshooting documentation for operational issues encountered during the development, maintenance, and operation of the RevChatham Homelab.

An incident records what occurred.

Troubleshooting records the investigation, evidence, actions, and decisions used to identify and resolve the incident.

Together, these records preserve operational knowledge and support future maintenance, recovery, and engineering review.

---

# Directory Structure

Incident records are organized by date and incident number.

```text
incidents/
├── README.md
├── INCIDENT_REPORT_TEMPLATE.md
├── YYYY-MM-DD/
│   ├── 001_incident-name/
│   │   ├── INCIDENT_REPORT.md
│   │   ├── COMMAND_LOG.md
│   │   ├── TERMINAL_OUTPUT.txt
│   │   ├── screenshots/
│   │   ├── logs/
│   │   ├── configs/
│   │   └── attachments/
│   └── 002_incident-name/
└── ...
