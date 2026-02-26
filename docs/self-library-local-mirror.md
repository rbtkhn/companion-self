# Self-library: local mirror of PD sources

## Feasibility

**Yes.** Downloading all Project Gutenberg sources referenced in `users/_template/self-library.md` and storing them locally or on GitHub is feasible.

- **Volume:** ~31 distinct etexts (by numeric PG ID in the template). Aggregate ~7.5M words → **roughly 8–15 MB** as plain UTF-8 text (depending on PG edition and line endings). Well within normal repo size.
- **PG terms:** Content is public domain; PG allows redistribution with attribution. See [Linking to Project Gutenberg](https://www.gutenberg.org/policy/linking.html) and their [copyright policy](https://www.gutenberg.org/policy/permission.html).
- **GitHub:** Repo stays small (tens of MB). No need for Git LFS. If you prefer to keep the main repo lean, use a **separate repo** (e.g. `companion-self-library-texts`) or put the mirror in a path that is **gitignored** and document how to run the download script.

## Options

| Option | Pros | Cons |
|--------|------|------|
| **Local only** (e.g. `library/pg/` in repo, add to `.gitignore`) | No clone bloat; full control | Others must run the script to get texts |
| **Same repo, committed** | One clone gives texts; offline use | Repo ~15–50 MB larger |
| **Separate repo** (e.g. submodule or standalone) | Main repo small; mirror versioned separately | Extra clone or submodule step |

## How to mirror

1. **Automated:** From repo root run:
   ```bash
   ./scripts/download-self-library-pg.sh
   ```
   Optional: `./scripts/download-self-library-pg.sh [path/to/self-library.md] [output_dir]`.  
   The script parses the library file for `pd_url` lines that point to `gutenberg.org/ebooks/<number>`, deduplicates IDs, and downloads plain text to `library/pg/<id>.txt` (1s delay between requests).
2. **Manual:** For each numeric etext ID, download:
   - Plain text: `https://www.gutenberg.org/cache/epub/<id>/pg<id>.txt`
   - Save as e.g. `library/pg/<id>.txt`.

**Note:** Entries that point to `gutenberg.org/ebooks/author/37` or `author/68` (Dickens, Austen author pages) are not single-file etexts; the script only handles numeric etext IDs. The story-level entries already use specific novel IDs (e.g. 730, 766, 1342, 161), so all referenced works are covered by the numeric-ID list.

## Index for companion-self utilization

After downloading, run the index builder so APIs or skill-read can resolve LIB-ids and filter by maturity:

```bash
./scripts/build-library-index.sh
```

This writes **`library/index.json`** (relative to repo root, or the path you pass as second arg). Paths in the index are relative to `library/` (e.g. `pg/2591.txt` → `library/pg/2591.txt`).

| Key | Use |
|-----|-----|
| **by_lib** | Resolve a self-library entry to a local file: `by_lib["LIB-0025"].path` → `"pg/2591.txt"`, plus `maturity`, `pg_id`, `title`, `volume`. |
| **by_pg** | Look up by PG etext ID: `by_pg["2591"]` → `path`, `maturities[]`, `lib_ids[]`, `volume`, `title`. |
| **by_maturity** | List all local paths for a maturity level: `by_maturity["1"]` → `["pg/10.txt", "pg/21.txt", ...]` for age-appropriate lookup. |

Use the index to (1) open the right file for a given LIB-id (e.g. evidence linking), (2) restrict lookup to maturity 1/2/3 for the companion's level, (3) list all texts in a tier without scanning the filesystem. Regenerate the index after editing `self-library.md` or adding/removing entries.

## Attribution

When distributing or displaying the mirrored texts, include Project Gutenberg attribution (e.g. “This eBook is for the use of anyone anywhere at no cost…”) as in the PG files, and do not use the Project Gutenberg trademark in a misleading way.
