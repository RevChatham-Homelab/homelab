# Chapter 2 – Installation

**Project:** RevChatham Homelab

**Document ID:** cbart_manual-002

**Document:** Chapter 2 – Installation

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-26

**Status:** Draft

---

## Table of Contents

- 2.1 Purpose
- 2.2 System Requirements
- 2.3 Supported Operating Systems
- 2.4 Software Prerequisites
- 2.5 Directory Structure
- 2.6 Installing CBART
- 2.7 Verifying the Installation
- 2.8 First Launch
- 2.9 Understanding the Initial Environment
- 2.10 Troubleshooting Installation
- 2.11 Chapter Summary

---

## 2.1 Purpose

This chapter provides a repeatable process for installing CBART, validating the installation, and preparing the environment for operational use.

## 2.2 System Requirements

Minimum requirements:

- 64-bit Linux
- Bash
- Python 3
- Git
- GNU core utilities
- Read/write access to the repository
- Storage for Recovery Point generation

## 2.3 Supported Operating Systems

CBART is developed and tested primarily on Ubuntu Server and other Ubuntu-based distributions.

## 2.4 Software Prerequisites

Verify the required software before installation.

```bash
git --version
python3 --version
bash --version
```

## 2.5 Directory Structure

Expected documentation location:

```text
~/homelab/docs/engineering/cbart/installation.md
```

Expected automation location:

```text
~/homelab/automation/recovery/
```

Maintaining the documented repository layout ensures predictable operation and simplifies future maintenance.

## 2.6 Installing CBART

1. Obtain the repository.
2. Change to the repository root.
3. Verify executable permissions.
4. Review configuration.
5. Launch CBART.

## 2.7 Verifying the Installation

Confirm that:

- CBART launches successfully.
- Logging initializes.
- A Recovery Point is generated.
- A manifest is created.
- A verification report is produced.

## 2.8 First Launch

Treat the first execution as an environment validation rather than production use. Review the generated output before considering the installation complete.

## 2.9 Understanding the Initial Environment

CBART depends on a consistent repository layout, repeatable workflows, and documented engineering standards.

## 2.10 Troubleshooting Installation

If problems occur:

- Verify installed prerequisites.
- Confirm repository paths.
- Verify executable permissions.
- Review execution logs.
- Compare the installation with the documented structure.

## 2.11 Chapter Summary

You should now understand the installation requirements, repository layout, validation process, and first-launch workflow for CBART.

## Key Takeaways

- Follow the documented repository layout.
- Verify prerequisites before execution.
- Validate the installation before production use.
- Preserve repeatable engineering practices.

## Next Chapter

**Chapter 3 – User Guide**

---

Chapter 2 – Installation v1.0.0
