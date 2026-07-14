# Milestone-Based Changelog Standard

## Purpose

The RevChatham Homelab uses milestone-based versioning to document the evolution of the project rather than individual file changes.

The CHANGELOG should communicate the project's history at a high level and provide meaningful milestones for future reference.

---

# Versioning Standard

The project follows Semantic Versioning (SemVer) with milestone-based releases.

| Version | Meaning |
|----------|---------|
| **0.x.0** | Major project milestone |
| **0.x.y** | Bug fixes, documentation corrections, and minor improvements |
| **1.0.0** | First production-ready release |
| **2.0.0** | Major architectural redesign or platform evolution |

---

# Changelog Structure

Each release should follow this structure when applicable.

```markdown
## [Version] - YYYY-MM-DD

### Added

...

### Changed

...

### Fixed

...

### Audited

...

### Standardized

...

### Documentation

...

### Infrastructure

...
```

Not every section is required.

Only include sections that apply to the milestone.

---

# Unreleased

The **Unreleased** section should contain only work that has not yet been completed.

Once a milestone is completed, move those items into the appropriate released version.

---

# Philosophy

The changelog should describe:

- What the project gained.
- What standards were established.
- What infrastructure changed.
- What documentation improved.

It should not become a commit history.

The Git history records commits.

The CHANGELOG records milestones.

---

# Goal

A reader should be able to understand the evolution of the project by reading only the CHANGELOG.

---

Template Version v1.0
