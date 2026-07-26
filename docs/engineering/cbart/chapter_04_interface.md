# Chapter 4 – Interface

**Project:** RevChatham Homelab

**Document ID:** cbart_manual-004

**Document:** Chapter 4 – Interface

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-26

**Status:** Draft

---

# 4.1 Purpose

This chapter documents the CBART user interface, its design philosophy, and the standards that make every screen consistent.

Rather than documenting individual features, this chapter explains how the interface is organized and why those design decisions were made.

The CBART interface follows the **CBART Navigation Standard** and **CBART Interface Standard**.

---

# 4.2 Design Philosophy

CBART is designed to behave like a professional administrative appliance rather than a collection of scripts.

The interface emphasizes:

- Consistency
- Predictability
- Readability
- Keyboard-first navigation
- SSH compatibility
- Operational efficiency

---

# 4.3 Screen Layout

Every screen follows the same structure:

1. Screen Title
2. Status / Summary
3. Operations
4. Utilities
5. Navigation

This consistent layout allows operators to build muscle memory.

---

# 4.4 Status / Summary

Every screen begins by presenting the current state before offering actions.

Typical information includes:

- Current configuration
- Defaults
- Statistics
- Recovery Point information
- Verification status

---

# 4.5 Operations

Operations perform work.

Examples include:

- Generate Recovery Point
- Verify Recovery Point
- Restore Recovery Point
- Export Recovery Point
- Configure Destinations

Operations are always numbered using the reserved range **1–6**.

---

# 4.6 Utilities

Utilities provide global functions available throughout CBART.

Standard utility assignments:

- F1 — Settings
- F2 — Documentation
- F3 — About
- F4 — Logs
- F5 — Help
- F10 — Print / Export

Utilities are visually separated from operational tasks.

---

# 4.7 Navigation

Navigation controls appear at the bottom of every screen.

Reserved navigation keys:

- 7 — Next
- 8 — Back
- 9 — Refresh
- 0 — Exit

Unused navigation options remain reserved but are omitted when not applicable.

---

# 4.8 Keyboard Interaction

CBART is keyboard-driven.

Numeric selections respond immediately without requiring Enter.

Utility commands are entered as labels (for example, F1 or F10) to maintain compatibility across SSH sessions and terminal emulators.

---

# 4.9 Interface Consistency

Every CBART screen follows the same visual organization.

This consistency:

- Reduces training time
- Improves operator confidence
- Minimizes navigation errors
- Makes future enhancements predictable

---

# 4.10 Accessibility

The interface avoids relying solely on color.

Status is communicated using clear text such as:

- Passed
- Failed
- Warning
- Running

Color may enhance readability but never replaces text.

---

# 4.11 Future Enhancements

Future interface improvements may include:

- Context-sensitive help
- Searchable documentation
- Interactive progress indicators
- Configurable themes
- Enhanced keyboard shortcuts

All future changes must remain compliant with the CBART standards.

---

# 4.12 Chapter Summary

The CBART interface is designed around consistency, operational clarity, and predictable navigation.

Operators who understand one CBART screen should immediately understand the layout of every other screen.

---

## Key Takeaways

- Every screen follows a common structure.
- Operations, Utilities, and Navigation are distinct.
- Navigation is standardized across the application.
- Keyboard-first interaction supports efficient administration.

---

## Next Chapter

**Chapter 5 – Backup & Recovery**

---

Chapter 4 – Interface v1.0.0
