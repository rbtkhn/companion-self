# Demo change-review artifacts

Synthetic JSON for validating [change-review](../../docs/change-review.md) schemas (`schema-registry/change-*.v1.json`, `identity-diff.v1.json`). Not a live companion Record.

```bash
pip install -r scripts/requirements-seed-phase.txt
python3 scripts/validate-change-review.py users/demo/change-review
```
