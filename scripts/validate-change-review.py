#!/usr/bin/env python3
"""
Validate change-review demo (or instance) artifact sets against schema-registry.

Usage:
  python3 scripts/validate-change-review.py users/demo/change-review
  python3 scripts/validate-change-review.py path/to/dir --allow-placeholders
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "change_proposal.json",
    "change_decision.json",
    "identity_diff.json",
    "change_review_queue.json",
    "change_event_log.json",
]

SCHEMA_BY_FILE = {
    "change_proposal.json": "schema-registry/change-proposal.v1.json",
    "change_decision.json": "schema-registry/change-decision.v1.json",
    "identity_diff.json": "schema-registry/identity-diff.v1.json",
    "change_review_queue.json": "schema-registry/change-review-queue.v1.json",
    "change_event_log.json": "schema-registry/change-event-log.v1.json",
}


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate change-review artifact directory")
    ap.add_argument("directory", type=Path, help="e.g. users/demo/change-review")
    ap.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Require files + JSON parse only; skip jsonschema validation",
    )
    args = ap.parse_args()

    target = (REPO_ROOT / args.directory).resolve() if not args.directory.is_absolute() else args.directory
    if not target.is_dir():
        print(f"Not a directory: {target}", file=sys.stderr)
        sys.exit(1)

    failed = False
    for name in REQUIRED_FILES:
        p = target / name
        if not p.is_file():
            print(f"Missing: {p.relative_to(REPO_ROOT)}", file=sys.stderr)
            failed = True
    if failed:
        sys.exit(1)

    readme = target / "README.md"
    if readme.stat().st_size < 10:
        print("README.md too small", file=sys.stderr)
        sys.exit(1)

    instances: dict[str, dict] = {}
    for jname in SCHEMA_BY_FILE:
        path = target / jname
        try:
            instances[jname] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"Invalid JSON {path}: {e}", file=sys.stderr)
            sys.exit(1)

    if args.allow_placeholders:
        print("validate-change-review: OK (placeholder mode, schema validation skipped)")
        return

    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print(
            "jsonschema is required for strict validation. pip install -r scripts/requirements-seed-phase.txt\n"
            "Or use --allow-placeholders.",
            file=sys.stderr,
        )
        sys.exit(1)

    for jname, schema_rel in SCHEMA_BY_FILE.items():
        schema_path = REPO_ROOT / schema_rel
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        errs = sorted(validator.iter_errors(instances[jname]), key=lambda e: e.path)
        if errs:
            print(f"Schema errors in {jname}:", file=sys.stderr)
            for e in errs[:20]:
                print(f"  {list(e.path)}: {e.message}", file=sys.stderr)
            if len(errs) > 20:
                print(f"  ... and {len(errs) - 20} more", file=sys.stderr)
            sys.exit(1)

    print("validate-change-review: OK (strict schema validation)")


if __name__ == "__main__":
    main()
