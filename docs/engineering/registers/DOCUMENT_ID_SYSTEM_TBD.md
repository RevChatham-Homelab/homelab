# Document ID System (TBD)

**Status:** Deferred

---

## Purpose

This document captures the current design discussion regarding the future document identification system.

The intent is to preserve the ideas explored without delaying the completion of the current project.

No implementation decisions have been made.

---

# Why This Was Deferred

The current project priorities are:

1. Complete CBART v1.0
2. Finish remaining project audits
3. Complete repository cleanup
4. Build the RevChatham website/portfolio

The document identification system is important, but it is not currently blocking any engineering work.

Rather than delaying higher-priority milestones, the design has been intentionally postponed.

---

# Discussion Summary

Several document identification strategies were explored.

## Simple Sequential IDs

Example:

```
eng-001
doc-001
```

Advantages:

- Simple
- Easy to read

Disadvantages:

- Limited hierarchy
- Not scalable across multiple projects.

---

## Namespace-Based IDs

Example:

```
hl-eng-001
cbart-eng-001
docman-eng-001
```

Advantages:

- Project separation
- Better scalability.

Disadvantages:

- Still requires manually assigning document numbers.

---

## Human-Readable IDs

Example:

```
pmx-ubs-hom-eng-sta
```

Advantages:

- Immediately understandable.
- No lookup table required.

Disadvantages:

- Difficult to uniquely identify multiple documents of the same type.

---

## SKU-Style Classification

A concept was discussed where every document receives an automatically generated classification similar to a SKU.

Possible hierarchy:

- Platform
- System
- Project
- Discipline
- Subject
- Document Type

Example:

```
001-001-001-005-007-01
```

Potential meaning:

```
Platform
System
Project
Discipline
Subject
Document Type
```

This would be generated automatically rather than manually assigned.

---

## Hexadecimal / Base36

Encoding the classification into hexadecimal or another compact representation was considered.

No decision has been made.

---

# Long-Term Vision

The planned **DocMan** application is expected to become the authoritative document management system.

Possible responsibilities include:

- Automatic document numbering
- Automatic classification
- Metadata generation
- Cross-reference management
- Version control
- Repository indexing
- Search
- Document lifecycle management

Rather than manually creating document IDs, DocMan should generate and manage them.

---

# Temporary Project Decision

Until DocMan exists:

- Existing document IDs remain acceptable.
- Temporary identifiers may be used where necessary.
- The document ID system will not block engineering work.
- A future migration may replace all temporary IDs.

---

# Engineering Decision

The document identification system is intentionally deferred.

The current focus is on completing project deliverables rather than perfecting infrastructure.

Progress takes precedence over premature optimization.

---

# Current Priorities

1. Complete CBART.
2. Finish repository cleanup.
3. Complete remaining audits.
4. Build the RevChatham website.
5. Design and implement DocMan.
6. Revisit the document identification system.
