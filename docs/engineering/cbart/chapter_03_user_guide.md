# Chapter 3 – User Guide

**Project:** RevChatham Homelab

**Document ID:** cbart_manual-003

**Document:** Chapter 3 – User Guide

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-26

**Status:** Draft

---

## 3.1 Purpose

This chapter introduces the day-to-day operation of the Chatham Backup and Recovery Tool (CBART). After completing the installation described in Chapter 2, the operator will learn how to navigate the application, execute common tasks, review generated artifacts, and interpret operational feedback.

## 3.2 Starting CBART

Launch CBART from the repository root.

```bash
cd ~/homelab
./automation/recovery/bin/run-recovery-point
```

Confirm that the application initializes without errors before proceeding.

## 3.3 Understanding the Interface

CBART follows the navigation standard established by the project.

- Keys `1`–`6` perform screen-specific operations.
- `7` is reserved for **Next** when applicable.
- `8` is reserved for **Back**.
- `9` is reserved for **Refresh**.
- `0` exits the application.
- `F1`–`F5` and `F10` provide global utilities.

Operations, Utilities, and Navigation are always presented as separate sections.

## 3.4 Running a Recovery Point

Typical workflow:

1. Open **Backup Operations**.
2. Select **Generate Recovery Point**.
3. Review the displayed configuration.
4. Confirm execution.
5. Monitor progress until completion.
6. Review the summary.

## 3.5 Monitoring Progress

During execution CBART reports:

- Current task
- Warnings
- Errors
- Completion status
- Recovery Point identifier

A successful run concludes with the generated Recovery Point location.

## 3.6 Understanding Generated Output

Each Recovery Point contains organized artifacts including:

- Documentation
- Docker configuration
- Proxmox information
- Manifest
- Verification report
- Checksums
- Execution logs

## 3.7 Reviewing Results

After every run:

- Read the manifest.
- Review the verification report.
- Confirm checksum generation.
- Inspect the execution log for warnings.

## 3.8 Common Tasks

Daily operation includes:

- Creating Recovery Points
- Verifying previous Recovery Points
- Reviewing logs
- Exporting reports
- Browsing Recovery Point history

## 3.9 Best Practices

- Generate a Recovery Point before major changes.
- Verify every Recovery Point.
- Keep generated Recovery Points out of Git.
- Archive important Recovery Points.
- Review warnings even when the overall result is successful.

## 3.10 Troubleshooting

If unexpected behavior occurs:

- Verify the repository location.
- Review execution logs.
- Confirm required permissions.
- Compare output against expected directory structure.
- Follow the troubleshooting guide when necessary.

## 3.11 Chapter Summary

The operator should now understand the standard workflow for using CBART, interpreting its output, and following established operational practices.

## Key Takeaways

- Operate CBART through its standardized interface.
- Verify every Recovery Point.
- Treat logs and verification reports as operational evidence.
- Follow documented workflows to ensure consistent results.

## Next Chapter

**Chapter 4 – Interface**

---

Chapter 3 – User Guide v1.0.0
