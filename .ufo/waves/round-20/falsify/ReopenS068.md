# ReopenS068 — re-open S068 (Python os docs) and verify row + Gate quote

**Verdict: HOLDS** — all five fields hold; no material discrepancy found.

## Row and Gate under test

- Row: `corpus/SOURCES.md:74` (column order per header `corpus/SOURCES.md:5`: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by)
- Gate: `corpus/lessons/round-20.md:43`

## Per-field results

### 1. Quote present verbatim at stated location — HOLDS
Gate: "This function normally follows symlinks; to stat a symlink add the argument follow_symlinks=False, or use lstat()." — claimed location: os.stat entry.

I re-opened https://docs.python.org/3/library/os.html myself. In the reader text the os.stat signature is at line 2759 (`os.stat(*path*, **, dir_fd=None, follow_symlinks=True)`) and the sentence at line 2764: "This function normally follows symlinks; to stat a symlink add the argument `follow_symlinks=False`, or use [`lstat()`](#os.lstat "os.lstat")." — byte-for-text identical after flattening inline-code markup; no other wording difference. Raw-HTML existence check (reader text alone cannot prove raw bytes): `curl -s https://docs.python.org/3/library/os.html | grep -c 'This function normally follows symlinks; to stat a symlink add the argument'` → `1`, exit 0. Disambiguation: `os.DirEntry.stat` (os.html reader lines 2727–2730) carries a near-miss variant ("follows symbolic links by default; to stat a symbolic link add the `follow_symlinks=False` argument" — no "normally", no "or use lstat()"), so the Gate quote can only be the os.stat entry, exactly as stated. The other anchors named by the row also check out: os.lstat entry "Similar to stat(), but does not follow symbolic links" (reader lines 2235–2238); the follow_symlinks section exists as `<ul id="follow-symlinks">` ("not following symlinks: If follow_symlinks is …", raw grep) with 13 inbound `(#follow-symlinks)` links from function entries (e.g. reader line 2766); page title "Python 3.15.0 documentation" (reader line 17) matches the row's "Python 3.15.0 docs opened 2026-10-21".

### 2. ≤25 words — HOLDS
`printf '%s' '<quote>' | wc -w` → `16` (whitespace tokens; even splitting `follow_symlinks=False,` / `lstat().` on punctuation gives 18). Either counting convention is under 25.

### 3. Tier honest for scope — HOLDS
Row tier A; Gate "Admit A". No written A/B/C rubric exists in SOURCES.md (checked header :5, registry :6–78, footer Paths/Search-log :78–115; `SKILL.md:206` defers tiers to SOURCES.md itself), so this is judged by registry precedent [INFERENCE on the rubric, observed on the rows]: official normative docs for the exact declared scope = A (S001, S062, S064, S066); official docs kept only for vocabulary with a scope caveat = B (S071, `SOURCES.md:77`); official docs demoted to C where the claimed scope exceeded the page (S063, S065). S068 declares a narrow scope — "os.stat versus os.lstat symlink following (final path component)" — and the official CPython 3.15.0 docs are the normative authority for precisely that behavior; the scope matches what the page supports, so A is honest.

### 4. Teaches grounded — HOLDS
Teaches (`SOURCES.md:74`): "A report-presence check must lstat the final component: os.stat follows a symlink by default, lstat inspects the link itself." Both clauses are grounded in the opened page: default-following from the os.stat entry quote (line 2764), link-itself semantics from the os.lstat entry (lines 2235–2238). The application to report presence is expressed and implemented, not asserted: `corpus/knowledge/wave-settlement-r20.md:6` cites S068 and its decision table `:26–30` classes `present` only for a "regular non-symlink file, size > 0"; the tool implements it (`tools/mori-wave-settlement.py:66–68` `_lstat` → `os.lstat`, "never following a final-component symlink"; `:125–126` "Read a lstat-confirmed regular file without opening a final symlink") and tests it (selftest case `symlink-report`, `:472–480`; independent harness `build/OracleHarness/c2-oracle.py:124–130` has its own symlink case). Consistent with mori's detect-only scope — no remediation claim anywhere.

### 5. Status/used-by consistent — HOLDS
status `mined` matches the Gate admission ("Admit A") and a landed consumer; used-by `corpus/knowledge/wave-settlement-r20.md` exists and cites S068 at line 6; it is the only used-by path, and it is the file the lesson routes C2 through. Lesson corroborations: `round-20.md:15–16` "Sourced: S068, S069, S071" for C2; `:48–50` "The L1 re-opened all seven URLs this round and matched each quote byte-for-text … Status/recheck/used-by changes to existing rows: none" — consistent with the row's opened=2026-10-21, recheck=on-release (sibling r20 rows S066/S069/S070 use the same opened/recheck pattern), and unchanged used-by. Note `round-20.md:43` access date 2026-10-21 = today, matching my live fetch of the same 3.15.0 page.

## Method disclosure
- Tools: `read` (URL reader + files), `grep` (device) on the URL and named lane files; two `curl -s … | grep` fact pipelines for raw-HTML checks, because the grep device serves only reader-normalized text for URLs and the verbatim/byte-level claims needed raw bytes. Exit 0 both. No tools installed (no pacman/uv/npm activity; tooling directive: nothing needed).
- Line numbers for os.html are from the reader markdown conversion, not raw HTML byte offsets; raw verification quoted above compensates.
- Unobserved: none material. [INFERENCE] items are labeled above (tier-rubric reconstruction; counting-convention note).

Scratch files: none (all evidence cited in place).
