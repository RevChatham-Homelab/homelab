# Recovery Point Example

Recovery Point ID:
RP-20260721-006.example

Source Recovery Point:
RP-20260721-006

Generated:
2026-07-22 01:08:03 UTC

Generator:
Recovery Framework Sanitizer v1.0.0

---

## Purpose

This directory is a sanitized example generated from a real Recovery Point.

It demonstrates the Recovery Framework structure, collected artifacts,
verification process, and checksum output without exposing private
environment-specific information.

---

## Sanitization

The sanitization process replaces or removes environment-specific values,
including:

- Usernames
- Hostnames
- Home-directory paths
- Internal IPv4 addresses
- Domain names
- Email addresses
- Other matched environment identifiers

The documentation archive is extracted, sanitized, and rebuilt.

Checksums are regenerated after sanitization.

---

## Important

This example is not intended to be used for disaster recovery.

Operational Recovery Points are generated separately under:

```text
automation/recovery/output/
```

Those operational artifacts are excluded from version control.
