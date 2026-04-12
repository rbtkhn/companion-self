# Unified export CLI (`scripts/export.py`)

This **companion-self** tree ships the same **dispatcher** as the grace-mar instance ([`export.py`](https://github.com/rbtkhn/grace-mar/blob/main/scripts/export.py) contract). Subcommands invoke `scripts/export_*.py` modules next to this file.

**Inventory:** As of introduction, the template repo may **not** yet include all of `export_fork.py`, `export_prp.py`, `export_user_identity.py`, `export_manifest.py`, `export_runtime_bundle.py`. If a target file is missing, `export.py` exits with a clear error. Promote the implementation modules from the instance repo per the operator merge checklist ([grace-mar MERGING-FROM-COMPANION-SELF](https://github.com/rbtkhn/grace-mar/blob/main/docs/MERGING-FROM-COMPANION-SELF.md)).

**Usage:** Same as [grace-mar docs/EXPORT-CLI.md](https://github.com/rbtkhn/grace-mar/blob/main/docs/EXPORT-CLI.md) — `python scripts/export.py --help` once modules exist.

**Default user:** `_template` when `users/grace-mar` is absent; `grace-mar` when present; override with `GRACE_MAR_USER_ID` or `-u`.
