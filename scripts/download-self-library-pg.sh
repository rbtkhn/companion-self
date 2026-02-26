#!/usr/bin/env bash
# Download Project Gutenberg plain-text files for all pd_url etext IDs
# referenced in users/_template/self-library.md (or path given as first arg).
# Saves to library/pg/<id>.txt. Be nice to PG: 1s delay between requests.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LIBRARY_MD="${1:-$REPO_ROOT/users/_template/self-library.md}"
OUT_DIR="${2:-$REPO_ROOT/library/pg}"

if [[ ! -f "$LIBRARY_MD" ]]; then
  echo "Usage: $0 [path/to/self-library.md] [output_dir]" >&2
  echo "Default: users/_template/self-library.md -> library/pg/" >&2
  exit 1
fi

# Extract numeric PG etext IDs from pd_url lines (skip author/37, author/68)
IDS=($(grep -oE 'gutenberg\.org/ebooks/[0-9]+' "$LIBRARY_MD" | sed 's/.*\///' | sort -nu))

mkdir -p "$OUT_DIR"
echo "Downloading ${#IDS[@]} Project Gutenberg etexts to $OUT_DIR"

for id in "${IDS[@]}"; do
  out="$OUT_DIR/${id}.txt"
  if [[ -f "$out" ]]; then
    echo "  skip $id (already exists)"
    continue
  fi
  url="https://www.gutenberg.org/cache/epub/${id}/pg${id}.txt"
  if curl -sf -o "$out" "$url"; then
    echo "  ok $id"
  else
    echo "  fail $id ($url)" >&2
    rm -f "$out"
  fi
  sleep 1
done

echo "Done. Total files: $(ls -1 "$OUT_DIR"/*.txt 2>/dev/null | wc -l)"
