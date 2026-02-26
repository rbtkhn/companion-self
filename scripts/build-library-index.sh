#!/usr/bin/env bash
# Build library/index.json from users/_template/self-library.md so companion-self
# can resolve LIB-id -> local path and filter by maturity. Run after download.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LIBRARY_MD="${1:-$REPO_ROOT/users/_template/self-library.md}"
OUT_JSON="${2:-$REPO_ROOT/library/index.json}"

if [[ ! -f "$LIBRARY_MD" ]]; then
  echo "Usage: $0 [path/to/self-library.md] [path/to/library/index.json]" >&2
  exit 1
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

current_id=""
current_maturity=""
current_pg=""
current_volume=""
current_title=""
in_yaml=0

while IFS= read -r line; do
  if [[ "$line" == '```yaml' ]]; then in_yaml=1; continue; fi
  if [[ "$line" == '```' ]] && [[ $in_yaml -eq 1 ]]; then in_yaml=0; continue; fi
  [[ $in_yaml -ne 1 ]] && continue

  if [[ "$line" =~ ^[[:space:]]+-[[:space:]]+id:[[:space:]]+(LIB-[0-9]+) ]]; then
    if [[ -n "$current_id" ]] && [[ -n "$current_pg" ]]; then
      echo "${current_id}|${current_maturity}|${current_pg}|${current_volume}|${current_title}"
    fi
    current_id="${BASH_REMATCH[1]}"
    current_maturity=""
    current_pg=""
    current_volume=""
    current_title=""
  elif [[ "$line" =~ ^[[:space:]]+maturity:[[:space:]]+([0-9]+) ]]; then
    current_maturity="${BASH_REMATCH[1]}"
  elif [[ "$line" =~ ^[[:space:]]+pd_url:.*gutenberg\.org/ebooks/([0-9]+) ]]; then
    current_pg="${BASH_REMATCH[1]}"
  elif [[ "$line" =~ ^[[:space:]]+volume:[[:space:]]+\"(.*)\" ]]; then
    current_volume="${BASH_REMATCH[1]}"
  elif [[ "$line" =~ ^[[:space:]]+title:[[:space:]]+\"(.*)\" ]]; then
    current_title="${BASH_REMATCH[1]}"
  fi
done < "$LIBRARY_MD" > "$TMP/rows.txt"
if [[ -n "$current_id" ]] && [[ -n "$current_pg" ]]; then
  echo "${current_id}|${current_maturity}|${current_pg}|${current_volume}|${current_title}" >> "$TMP/rows.txt"
fi

mkdir -p "$(dirname "$OUT_JSON")"

python3 -c "
import json
from collections import defaultdict

rows = []
with open('$TMP/rows.txt') as f:
    for line in f:
        line = line.strip()
        if not line or '|' not in line:
            continue
        parts = line.split('|', 4)
        if len(parts) < 3:
            continue
        lib_id, maturity, pg_id = parts[0], parts[1], parts[2]
        volume = parts[3] if len(parts) > 3 else ''
        title = parts[4] if len(parts) > 4 else ''
        rows.append({'lib_id': lib_id, 'maturity': int(maturity) if maturity.isdigit() else None, 'pg_id': pg_id, 'volume': volume, 'title': title})

by_pg = {}
by_lib = {}
by_maturity = defaultdict(list)

for r in rows:
    pg_id = r['pg_id']
    path = 'pg/' + pg_id + '.txt'
    lib_id, maturity, volume, title = r['lib_id'], r['maturity'], r['volume'], r['title']
    if pg_id not in by_pg:
        by_pg[pg_id] = {'path': path, 'maturities': [], 'lib_ids': [], 'volume': volume or None, 'title': title or None}
    if maturity is not None and maturity not in by_pg[pg_id]['maturities']:
        by_pg[pg_id]['maturities'].append(maturity)
    if lib_id not in by_pg[pg_id]['lib_ids']:
        by_pg[pg_id]['lib_ids'].append(lib_id)
    by_lib[lib_id] = {'path': path, 'pg_id': pg_id, 'maturity': maturity, 'volume': volume or None, 'title': title or None}
    if maturity is not None and path not in by_maturity[str(maturity)]:
        by_maturity[str(maturity)].append(path)

for k in by_pg:
    by_pg[k]['maturities'].sort()

out = {
    'source': 'users/_template/self-library.md',
    'by_pg': by_pg,
    'by_lib': by_lib,
    'by_maturity': {k: sorted(v) for k, v in sorted(by_maturity.items())},
}
with open('$OUT_JSON', 'w') as f:
    json.dump(out, f, indent=2)
" || exit 1

echo "Wrote $OUT_JSON ($(wc -l < "$TMP/rows.txt") entries, $(python3 -c "import json; d=json.load(open('$OUT_JSON')); print(len(d['by_pg']), 'pg ids,', len(d['by_lib']), 'lib ids')")"
