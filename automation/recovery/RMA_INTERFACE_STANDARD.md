# Recovery Manager Application (RMA) Interface Standard

**Project:** RevChatham Homelab

**Document:** Recovery Manager Application (RMA) Interface Standard

**Document Version:** 1.0.0

**Last Reviewed:** 2026-07-22

**Status:** Approved

---

# RevChatham Homelab

## Recovery Manager Application Interface Standard

| Field | Value |
|---|---|
| Document | RMA Interface Standard |
| Project | RevChatham Homelab |
| Application | Recovery Manager Application (RMA) |
| Framework | Recovery Automation Framework (RAF) |
| Version | 1.0.0 |
| Status | Approved |
| Classification | Engineering Standard |
| Applies To | All RMA terminal screens and operator interactions |
| Repository Path | `automation/recovery/RMA_INTERFACE_STANDARD.md` |
| Last Reviewed | 2026-07-22 |

---

## 1. Purpose

This document defines the visual, structural, and interaction standards for the
Recovery Manager Application.

The Recovery Manager Application must present itself as a cohesive operator
application rather than a collection of unrelated scripts.

Every RMA screen must use consistent:

- screen widths;
- borders;
- titles;
- information panels;
- section dividers;
- menus;
- navigation choices;
- prompts;
- status messages;
- success screens;
- warning screens;
- error screens;
- confirmation screens;
- terminology;
- spacing;
- alignment.

The standard exists to ensure that the operator can move between screens without
having to relearn the application.

---

## 2. Scope

This standard applies to:

- the Recovery Manager Application launcher;
- all RMA menus;
- settings screens;
- Recovery Point generation screens;
- destination-selection screens;
- verification screens;
- Recovery Point browsing screens;
- reporting screens;
- Git integration screens;
- configuration screens;
- status summaries;
- validation messages;
- success screens;
- warning screens;
- error screens;
- confirmation screens;
- future RMA modules.

This standard does not define:

- Recovery Automation Framework execution logic;
- Recovery Point contents;
- backup implementation;
- Git command behavior;
- sanitization algorithms;
- verification algorithms;
- storage paths;
- network transport methods.

Those responsibilities belong to the Recovery Automation Framework and its
supporting engineering specifications.

---

## 3. Architectural Context

The Recovery Manager Application and the Recovery Automation Framework are
separate architectural layers.

```text
Recovery Manager Application (RMA)

    User Interface
    Navigation
    Settings
    Reports
    Validation
    Operator Feedback

                    ↓

Recovery Automation Framework (RAF)

    Recovery Point Generation
    Verification
    Sanitization
    Backup Operations
    Git Operations
    Framework Execution
```

The RMA is the operator control center.

The RAF is the execution engine.

The interface must never expose unnecessary framework complexity to the
operator.

---

## 4. Interface Design Philosophy

The Recovery Manager Application must feel predictable, deliberate, and safe.

Every screen should:

1. identify the current screen immediately;
2. communicate the purpose of the screen;
3. separate information from actions;
4. use consistent navigation;
5. use logical terminology instead of hardware-specific terminology;
6. minimize manual path entry;
7. confirm destructive or high-impact actions;
8. provide clear success or failure feedback;
9. avoid visual clutter;
10. preserve the operator's sense of location within the application.

The interface must prioritize readability over decoration.

Visual elements must have a defined purpose.

---

## 5. Standard Screen Width

The RMA interface standard uses a width of 72 characters.

All primary borders, panels, and section dividers must align to this width.

Standard full-width border:

```text
========================================================================
```

Standard full-width Unicode divider:

```text
────────────────────────────────────────────────────────────────────────
```

Standard information-panel border:

```text
+----------------------------------------------------------------------+
```

Screen-rendering helpers should calculate centering dynamically rather than
hard-coding title spacing.

---

## 6. Visual Hierarchy

The RMA uses three primary visual levels.

### 6.1 Level 1: Screen Header

The screen header identifies the current screen.

Format:

```text
========================================================================
                              Settings
========================================================================
```

Requirements:

- use the `=` character;
- use the full 72-character width;
- center the screen title;
- place the header at the top of every screen;
- use only one Level 1 header per screen;
- follow the header with one blank line.

Examples:

```text
========================================================================
                    Recovery Manager Application
========================================================================
```

```text
========================================================================
                     Destination Configuration
========================================================================
```

```text
========================================================================
                    Recovery Point Destination
========================================================================
```

```text
========================================================================
                         Recovery Statistics
========================================================================
```

---

### 6.2 Level 2: Information Panel

The information panel names an important content block.

Format:

```text
+----------------------------------------------------------------------+
|                    Current Configuration                             |
+----------------------------------------------------------------------+
```

Requirements:

- use `+` for panel corners;
- use `-` for the horizontal panel border;
- use `|` for the title row;
- center the title inside the panel;
- use the full 72-character width;
- use panels for important information, summaries, configuration, or status;
- do not use panels around ordinary menus;
- follow the panel with one blank line.

Approved uses:

- Current Configuration;
- Recovery Manager Settings;
- Recovery Point Summary;
- Repository Status;
- Recovery Point Details;
- Verification Results;
- Destination Status;
- Operation Summary;
- Confirmation context;
- Error title;
- Warning title;
- Success title.

Example:

```text
+----------------------------------------------------------------------+
|                 Recovery Manager Settings                            |
+----------------------------------------------------------------------+
```

---

### 6.3 Level 3: Section Divider

The section divider separates information from actions or separates multiple
content areas.

Format:

```text
────────────────────────────────────────────────────────────────────────
                           Menu Options
────────────────────────────────────────────────────────────────────────
```

Requirements:

- use the Unicode box-drawing horizontal character;
- use the full 72-character width;
- center the section title;
- place one divider above and one divider below the title;
- use one blank line after the divider block.

Approved section names include:

- Menu Options;
- Actions;
- Configuration;
- Recovery Points;
- Verification;
- Destinations;
- Repository Actions;
- Display Options;
- Framework Options.

---

## 7. Main Application Header

The main application screen may include application branding.

Approved format:

```text
========================================================================
                    Recovery Manager Application
                              Version 1.0.0
========================================================================

Recovery Automation Framework
RevChatham Homelab
```

The main screen is the only screen that should display full application
branding by default.

Subscreens should use only the current screen title.

---

## 8. Information Layout

Information should be displayed as readable label-and-value blocks.

Preferred format:

```text
Primary Storage
    Ubuntu Server

Backup Storage
    Flash Drive

Offsite
    Lenovo T14
```

For compact summaries, aligned label-and-value pairs are also permitted:

```text
Recovery Points : 6
Verified        : 6
Sanitized       : 6
Backup Storage  : Flash Drive
Offsite         : Lenovo T14
```

Rules:

- labels should use title case;
- values should be indented consistently;
- related values should be grouped;
- avoid excessive borders;
- avoid dense tables unless comparison is necessary;
- do not expose secrets;
- do not print tokens, credentials, or private keys;
- redact sensitive values when configuration details are displayed.

---

## 9. Menu Standard

Menu options must use numeric choices.

Format:

```text
1. Configure Destinations
2. Configure Git
3. Configure Display
4. Configure Recovery Framework
5. View Configuration

8. Back
```

Rules:

- use a number followed by a period;
- use concise action-oriented wording;
- use one option per line;
- group navigation choices below operational choices;
- place a blank line before `8. Back`;
- do not mix letters and numbers;
- do not use `Y/N` as the primary interaction model;
- do not renumber existing options without review when stable workflows depend
  on them.

---

## 10. Universal Navigation

The following navigation conventions are approved.

### 10.1 Back

```text
8. Back
```

`8. Back` returns to the parent screen.

It should be used consistently across all nested menus.

### 10.2 Exit

```text
0. Exit
```

`0. Exit` is reserved for leaving the Recovery Manager Application.

It should normally appear only on the main menu.

### 10.3 Cancel

For confirmation workflows, use:

```text
8. Cancel
```

`8. Cancel` returns without performing the proposed operation.

### 10.4 Return

After a completed operation, use:

```text
8. Return
```

The label may reflect the destination when useful:

```text
8. Return to Main Menu
```

or:

```text
8. Return to Recovery Points
```

---

## 11. Prompt Standard

Input prompts must clearly describe the expected choice.

Preferred format:

```text
Select an option:
```

For a menu-specific prompt:

```text
Select a settings option:
```

For destination selection:

```text
Select a Recovery Point destination:
```

Rules:

- end prompts with a colon;
- do not use vague prompts such as `Choice?`;
- do not expose implementation terminology;
- validate input before continuing;
- preserve the current screen after invalid input whenever practical.

---

## 12. Invalid Input Handling

Invalid input should not terminate the application.

Approved message:

```text
Invalid selection. Enter one of the listed menu numbers.
```

For a screen-based error:

```text
========================================================================
                                Error
========================================================================

+----------------------------------------------------------------------+
|                        Invalid Selection                             |
+----------------------------------------------------------------------+

The selected option is not available.

────────────────────────────────────────────────────────────────────────
                              Actions
────────────────────────────────────────────────────────────────────────

8. Back
```

Simple invalid menu input may be displayed inline.

Repeated or context-sensitive failures may use a full error screen.

---

## 13. Settings Menu Standard

Approved Settings screen:

```text
========================================================================
                              Settings
========================================================================

+----------------------------------------------------------------------+
|                 Recovery Manager Settings                            |
+----------------------------------------------------------------------+

Current Configuration

    Primary Storage
        Ubuntu Server

    Backup Storage
        Flash Drive

    Offsite
        Lenovo T14

────────────────────────────────────────────────────────────────────────
                           Menu Options
────────────────────────────────────────────────────────────────────────

1. Configure Destinations
2. Configure Git
3. Configure Display
4. Configure Recovery Framework
5. View Configuration

8. Back
```

The Settings menu is the central configuration area for the application.

Operational workflows must not become configuration screens.

---

## 14. Destination Configuration Standard

Approved screen:

```text
========================================================================
                     Destination Configuration
========================================================================

+----------------------------------------------------------------------+
|                    Current Configuration                             |
+----------------------------------------------------------------------+

Primary Storage
    Ubuntu Server

Backup Storage
    Flash Drive

Offsite
    Lenovo T14

────────────────────────────────────────────────────────────────────────
                           Configuration
────────────────────────────────────────────────────────────────────────

1. Change Backup Storage
2. Change Offsite Destination
3. Test Destinations
4. Reset to Defaults

8. Back
```

Destination configuration must use logical roles.

Approved logical destination names:

- Primary Storage;
- Backup Storage;
- Offsite.

Hardware names should appear only as configured values.

Examples:

```text
Backup Storage
    Flash Drive
```

```text
Backup Storage
    Network Attached Storage
```

```text
Offsite
    Lenovo T14
```

```text
Offsite
    Remote Server
```

The menu structure should remain stable even when the underlying hardware
changes.

---

## 15. Recovery Point Destination Standard

Destination selection is an operational decision.

Destination configuration is an application setting.

These concepts must remain separate.

Approved destination-selection screen:

```text
========================================================================
                    Recovery Point Destination
========================================================================

+----------------------------------------------------------------------+
|                      Available Destinations                          |
+----------------------------------------------------------------------+

Primary Storage
    Ubuntu Server

Backup Storage
    Flash Drive

Offsite
    Lenovo T14

────────────────────────────────────────────────────────────────────────
                           Menu Options
────────────────────────────────────────────────────────────────────────

1. Primary Storage
2. Primary Storage and Backup Storage
3. Primary Storage and Offsite
4. All Configured Destinations

8. Back
```

The operator should select logical destinations.

The application should resolve configured paths and transport methods.

---

## 16. Success Screen Standard

Approved format:

```text
========================================================================
                               Complete
========================================================================

+----------------------------------------------------------------------+
|                 Recovery Point Successfully Created                  |
+----------------------------------------------------------------------+

Recovery Point

    RP-20260722-008

Location

    automation/recovery/output

Verification

    Passed

────────────────────────────────────────────────────────────────────────
                              Actions
────────────────────────────────────────────────────────────────────────

1. View Recovery Point

8. Return
```

Success screens must show:

- what completed;
- the affected Recovery Point or object;
- the resulting location when appropriate;
- verification status when applicable;
- the next available action.

---

## 17. Error Screen Standard

Approved format:

```text
========================================================================
                                Error
========================================================================

+----------------------------------------------------------------------+
|                     Recovery Point Not Found                         |
+----------------------------------------------------------------------+

The selected Recovery Point no longer exists.

It may have been removed manually.

────────────────────────────────────────────────────────────────────────
                              Actions
────────────────────────────────────────────────────────────────────────

8. Back
```

Error screens must:

- state the failure clearly;
- avoid exposing stack traces by default;
- provide actionable context;
- provide a safe navigation option;
- write technical details to logs when appropriate.

---

## 18. Warning Screen Standard

Approved format:

```text
========================================================================
                               Warning
========================================================================

+----------------------------------------------------------------------+
|                    Destination Is Unavailable                        |
+----------------------------------------------------------------------+

Backup Storage could not be reached.

Configured Destination

    Flash Drive

The Recovery Point can still be created on Primary Storage.

────────────────────────────────────────────────────────────────────────
                              Actions
────────────────────────────────────────────────────────────────────────

1. Continue with Primary Storage
2. Test Destination Again

8. Cancel
```

Warnings must communicate:

- the condition;
- the affected component;
- the consequence;
- safe choices.

Warnings must not imply that an action completed successfully.

---

## 19. Confirmation Screen Standard

Approved format:

```text
========================================================================
                           Confirmation
========================================================================

+----------------------------------------------------------------------+
|                        Delete Recovery Point                         |
+----------------------------------------------------------------------+

Recovery Point

    RP-20260722-008

This operation cannot be undone.

────────────────────────────────────────────────────────────────────────
                              Actions
────────────────────────────────────────────────────────────────────────

1. Continue

8. Cancel
```

Rules:

- destructive operations require confirmation;
- the affected object must be identified;
- the consequence must be stated;
- the safe option must be visually available;
- `Y/N` should not replace the standard menu interaction;
- the default behavior after unexpected input must be cancellation.

---

## 20. Status Screen Standard

Approved format:

```text
========================================================================
                         Recovery Statistics
========================================================================

+----------------------------------------------------------------------+
|                    Recovery Point Summary                            |
+----------------------------------------------------------------------+

Recovery Points : 6
Verified        : 6
Sanitized       : 6
Backup Storage  : Flash Drive
Offsite         : Lenovo T14

────────────────────────────────────────────────────────────────────────
                              Actions
────────────────────────────────────────────────────────────────────────

1. View Recovery Point Index
2. Generate Statistics Report

8. Back
```

Status screens should prioritize meaningful operator information.

Do not display raw internal state unless it helps diagnose a problem.

---

## 21. Git Repository Screen Standard

Approved format:

```text
========================================================================
                          GitHub Repository
========================================================================

+----------------------------------------------------------------------+
|                       Repository Status                              |
+----------------------------------------------------------------------+

Repository
    RevChatham-Homelab/Homelab

Branch
    main

Working Tree
    Clean

Remote
    Reachable

────────────────────────────────────────────────────────────────────────
                         Repository Actions
────────────────────────────────────────────────────────────────────────

1. View Repository Status
2. Review Pending Changes
3. Commit Approved Changes
4. Push Approved Changes

8. Back
```

Git operations must clearly distinguish:

- review;
- commit;
- push;
- status.

The interface must not silently commit or push changes.

---

## 22. Display Configuration Standard

Display settings may include:

- terminal width;
- Unicode support;
- color support;
- compact mode;
- verbose status;
- clear-screen behavior.

Approved screen:

```text
========================================================================
                       Display Configuration
========================================================================

+----------------------------------------------------------------------+
|                       Current Display                                |
+----------------------------------------------------------------------+

Terminal Width
    72 columns

Unicode Borders
    Enabled

Color
    Disabled

Clear Screen
    Enabled

────────────────────────────────────────────────────────────────────────
                           Configuration
────────────────────────────────────────────────────────────────────────

1. Change Terminal Width
2. Toggle Unicode Borders
3. Toggle Color
4. Toggle Clear Screen
5. Reset Display Defaults

8. Back
```

Color must not be the only indicator of status.

The interface must remain readable without color.

---

## 23. Recovery Framework Configuration Standard

Approved screen:

```text
========================================================================
                 Recovery Framework Configuration
========================================================================

+----------------------------------------------------------------------+
|                    Current Framework Settings                        |
+----------------------------------------------------------------------+

Verification
    Enabled

Sanitization
    Enabled

Checksum Generation
    Enabled

Report Generation
    Enabled

────────────────────────────────────────────────────────────────────────
                           Configuration
────────────────────────────────────────────────────────────────────────

1. Configure Verification
2. Configure Sanitization
3. Configure Checksums
4. Configure Reports
5. View Framework Configuration

8. Back
```

The RMA may configure framework behavior, but it must not duplicate framework
implementation logic.

---

## 24. Screen-Clearing Behavior

The application may clear the terminal before rendering a new screen.

Screen clearing should:

- be configurable;
- avoid clearing information needed for troubleshooting;
- be disabled automatically when output is redirected;
- not interfere with log capture;
- not be required for correct operation.

The rendering system should support both interactive and non-interactive use.

---

## 25. Unicode and ASCII Compatibility

The preferred menu divider uses Unicode:

```text
────────────────────────────────────────────────────────────────────────
```

An ASCII fallback must be available:

```text
------------------------------------------------------------------------
```

The application should detect or configure whether Unicode rendering is
supported.

Information panels and screen headers already use ASCII-compatible characters.

---

## 26. Terminology Standard

Approved terms:

- Recovery Manager Application;
- RMA;
- Recovery Automation Framework;
- RAF;
- Recovery Point;
- Primary Storage;
- Backup Storage;
- Offsite;
- Destination;
- Verification;
- Sanitization;
- Configuration;
- Repository;
- Settings.

Avoid:

- hard-coded hardware names as menu concepts;
- vague labels such as `Drive 1`;
- unexplained abbreviations;
- inconsistent capitalization;
- terms that expose internal implementation unnecessarily.

Hardware names may appear as configured destination values.

---

## 27. Sensitive Information Standard

The RMA must not display:

- passwords;
- API tokens;
- private keys;
- authentication secrets;
- full environment files;
- sensitive host details in sanitized reports;
- confidential network information in portfolio examples.

When values must be shown, use redaction.

Example:

```text
Git Token
    XXXXXXXX
```

or:

```text
Credential
    Configured
```

The interface should communicate configuration state without exposing secrets.

---

## 28. Logging Standard

Operator-facing screens and diagnostic logs serve different purposes.

The screen should display:

- concise status;
- useful warnings;
- actionable errors;
- operation results.

Logs may contain:

- command output;
- timestamps;
- return codes;
- stack traces;
- detailed validation results;
- destination test details.

Sensitive values must still be redacted from logs.

---

## 29. Accessibility and Readability

The interface must:

- remain readable in monochrome terminals;
- avoid relying only on color;
- use consistent indentation;
- avoid excessive capitalization;
- avoid blinking text;
- avoid dense blocks of uninterrupted text;
- provide blank lines between logical sections;
- use clear action verbs;
- use stable menu positions where practical.

Titles should be concise enough to fit within the 72-character standard.

---

## 30. Screen Design Workflow

Every new RMA screen must be designed before implementation.

Approved workflow:

1. **Design**
   - Sketch the complete screen in plain text.
   - Define title, panel, information, actions, and navigation.

2. **Review**
   - Review wording, terminology, spacing, and operator safety.

3. **Approve**
   - Freeze the screen layout for the milestone.

4. **Implement**
   - Write code that matches the approved screen.

5. **Test**
   - Test rendering, navigation, invalid input, and terminal compatibility.

6. **Document**
   - Update this standard when a new reusable interface pattern is introduced.

Implementation must not begin from an undefined screen concept.

---

## 31. Milestone 1 Requirements

Milestone 1 validates the interface.

Milestone 1 should focus on:

- screen rendering;
- navigation;
- menu hierarchy;
- terminology;
- settings organization;
- logical destination naming;
- input validation;
- approved interface patterns.

Milestone 1 should not perform:

- Recovery Point generation;
- backup copying;
- sanitization;
- verification;
- Git commits;
- Git pushes;
- destructive operations;
- framework execution.

Operational behavior belongs to later milestones after the interface is approved.

---

## 32. Proposed Main Menu

Approved conceptual structure:

```text
========================================================================
                    Recovery Manager Application
                              Version 1.0.0
========================================================================

Recovery Automation Framework
RevChatham Homelab

+----------------------------------------------------------------------+
|                         Application Status                           |
+----------------------------------------------------------------------+

Framework
    Available

Configuration
    Loaded

Destinations
    Primary Storage configured

────────────────────────────────────────────────────────────────────────
                           Menu Options
────────────────────────────────────────────────────────────────────────

1. Generate Recovery Point
2. Generate Recovery Point and Backup
3. Browse Recovery Points
4. Verify Recovery Point
5. Recovery Statistics
6. GitHub Repository
7. Settings

0. Exit
```

Milestone 1 may render these options without executing operational functions.

---

## 33. Rendering Components

The application should eventually centralize interface rendering.

Recommended conceptual helpers:

```python
render_screen_header(title)
render_panel(title)
render_section(title)
render_label_value(label, value)
render_menu(options)
render_prompt(text)
render_success(...)
render_warning(...)
render_error(...)
render_confirmation(...)
```

These helpers should enforce:

- width;
- centering;
- spacing;
- border characters;
- terminology;
- consistent navigation.

Individual screens should not manually reproduce border logic when shared
rendering helpers are available.

---

## 34. Testing Requirements

Interface tests should validate:

- every border is 72 characters wide;
- titles are centered;
- panels are correctly closed;
- Unicode fallback works;
- menu options are displayed in the correct order;
- `8. Back` returns to the parent screen;
- `0. Exit` exits only from approved screens;
- invalid input does not crash the application;
- destructive actions require confirmation;
- screen content does not expose secrets;
- logical destination names are used;
- hardware names are treated as configuration values;
- screen output remains readable without color.

Snapshot-style output testing may be used for stable screens.

---

## 35. Change Control

Changes to this standard require review because interface inconsistency affects
every operator workflow.

A proposed change should identify:

- the existing rule;
- the proposed rule;
- the reason;
- affected screens;
- migration requirements;
- compatibility impact;
- approval status.

Minor wording fixes do not require a version change unless they alter behavior.

Structural changes should update the document version.

---

## 36. Versioning

This standard uses semantic versioning.

- Major version: incompatible interface-standard change.
- Minor version: new approved pattern or substantial extension.
- Patch version: clarification, typo correction, or formatting fix.

Current version:

```text
1.0.0
```

---

## 37. Approved Decisions

The following decisions are approved:

- RMA is an application, not merely a wrapper script.
- RAF is the execution engine.
- Every screen is designed before implementation.
- The standard width is 72 characters.
- Screen titles use `=` borders.
- Information panels use `+`, `-`, and `|`.
- Section dividers use the Unicode horizontal box-drawing character.
- ASCII divider fallback is supported.
- Information panels are not used around ordinary menus.
- Menus use numeric choices.
- `8. Back` is the universal nested-navigation action.
- `0. Exit` is reserved for leaving the application.
- Confirmation screens use numbered actions instead of `Y/N`.
- Settings are centralized.
- Destination selection and destination configuration remain separate.
- Destination menus use logical roles.
- Hardware names are configuration values.
- Color is optional and cannot be the only status indicator.
- Sensitive values are never displayed unredacted.
- Milestone 1 validates interface behavior only.

---

## 38. Reference Templates

### 38.1 Standard Screen

```text
========================================================================
                           Screen Title
========================================================================

+----------------------------------------------------------------------+
|                         Panel Title                                  |
+----------------------------------------------------------------------+

Information

    Value

────────────────────────────────────────────────────────────────────────
                           Menu Options
────────────────────────────────────────────────────────────────────────

1. First Action
2. Second Action

8. Back
```

### 38.2 Main Screen

```text
========================================================================
                    Recovery Manager Application
                              Version 1.0.0
========================================================================

Recovery Automation Framework
RevChatham Homelab

+----------------------------------------------------------------------+
|                         Application Status                           |
+----------------------------------------------------------------------+

Framework
    Available

────────────────────────────────────────────────────────────────────────
                           Menu Options
────────────────────────────────────────────────────────────────────────

1. Generate Recovery Point
2. Browse Recovery Points
3. Settings

0. Exit
```

### 38.3 Confirmation Screen

```text
========================================================================
                           Confirmation
========================================================================

+----------------------------------------------------------------------+
|                         Confirm Action                               |
+----------------------------------------------------------------------+

Affected Object

    Object Name

This operation cannot be undone.

────────────────────────────────────────────────────────────────────────
                              Actions
────────────────────────────────────────────────────────────────────────

1. Continue

8. Cancel
```

### 38.4 Error Screen

```text
========================================================================
                                Error
========================================================================

+----------------------------------------------------------------------+
|                           Error Title                                |
+----------------------------------------------------------------------+

Clear description of the failure.

Suggested corrective action.

────────────────────────────────────────────────────────────────────────
                              Actions
────────────────────────────────────────────────────────────────────────

8. Back
```

### 38.5 Success Screen

```text
========================================================================
                               Complete
========================================================================

+----------------------------------------------------------------------+
|                        Operation Complete                            |
+----------------------------------------------------------------------+

Result

    Successful

────────────────────────────────────────────────────────────────────────
                              Actions
────────────────────────────────────────────────────────────────────────

1. View Result

8. Return
```

---

## 39. Final Standard

The Recovery Manager Application must communicate with the operator through a
consistent terminal design system.

Every border, title, menu, prompt, and action should reinforce that the operator
is using one application.

The interface must remain:

- consistent;
- readable;
- safe;
- maintainable;
- hardware-independent;
- configuration-driven;
- suitable for future expansion.

This document is the single source of truth for the Recovery Manager
Application interface.

---

## Document Control

| Field | Value |
|---|---|
| Standard | RMA Interface Standard |
| Version | 1.0.0 |
| Status | Approved |
| Owner | RevChatham Homelab |
| Repository | RevChatham-Homelab/Homelab |
| Path | `automation/recovery/RMA_INTERFACE_STANDARD.md` |
| Last Reviewed | 2026-07-22 |

---

Recovery Manager Application (RMA) Interface Standard v1.0.0
