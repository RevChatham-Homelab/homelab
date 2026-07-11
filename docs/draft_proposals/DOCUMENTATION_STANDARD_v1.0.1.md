# Documentation Standard

**Proposal:** Documentation Standard
**Candidate Version:** 1.0.1
**Status:** Draft Proposal
**Created:** 2026-07-11

---

# Purpose

This document records proposed improvements to the Documentation Standard.

Draft proposals are not official project standards.

They exist to capture lessons learned during project development and will be reviewed during the next scheduled standards review.

Only after approval by the project owner will a proposal become part of an official standard.

---

# Draft Proposal 001

## Title

Intentional Redundancy for Critical Operational Information

---

### Proposal

Critical operational information may be intentionally duplicated across reference documentation and operational documentation when doing so improves recoverability, reduces ambiguity, or minimizes context switching during backup and disaster recovery.

This duplication should be:

- intentional
- documented
- reviewed during scheduled standards reviews
- kept synchronized whenever the approved standard is updated

---

### Rationale

Reference documentation and operational documentation serve different purposes.

Reference documentation explains the system.

Operational documentation enables someone to operate or recover the system.

When the same critical information significantly improves recovery, duplication is preferable to forcing the reader to navigate multiple documents during an incident.

---

### Examples

Examples of acceptable intentional redundancy include:

- Recovery order
- Recovery priorities
- Critical dependencies
- Required prerequisites
- Recovery validation checkpoints

Detailed implementation steps should remain in a single authoritative document whenever practical.

---

### Philosophy

> Duplicate information only when it reduces operational risk.

Convenience alone is not sufficient justification.

---

### Review Status

Pending review during the next scheduled Documentation Standard review.

No changes to the approved Documentation Standard have been made.

---

End of Draft Proposal 001
