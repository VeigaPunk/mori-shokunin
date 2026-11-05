# DigestScout — round 96 w1, C2 read-only reconnaissance

Seat: DigestScout (scout). Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering HEAD `66c5518e239eeacd6070be26d78085ef702392cb`; lane HEAD moved during the wave to
`9bde9322` (sibling DigestExec landing). No file outside this report was written; no git/jj mutation
was run; no host setting was touched; no tool was installed (nothing needed).

## 0. Tool-under-test facts (read from `tools/mori-source-digest.py`)

- Docstring `tools/mori-source-digest.py:1-77`; row parse `parse_rows` (`:113`), copy-path extraction
  `extract_copy_paths` (`:129`), digest extraction `extract_digests` (`:152`), `byte_counts_near`
  (`:181`), `resolve_path` (`:192`), `pair_verdict` (`:239`), `combine` (`:247`), pinned-copy search
  (`:322-354`), pairing (`:357-433`), supersession (`:449-457`), counts (`:458-470`), `exit_code` (`:472`).
- `PATH_RE` (`:84`) = `(?<![\w/.-])((?:corpus|\.ufo)/[A-Za-z0-9_./~%\-]+)` — a path preceded by `/` or by
  `owner/repo/` is **not** a local copy reference (docstring: "Paths under `../` or `owner/repo/`
  prefixes are not treated as local copies").
- `PINNED_LOC_RE` (`:93`) makes any `corpus/evidence/…` or `.ufo/waves/…` path a copy reference.
- `NONCOPY_ATTR_RE` (`:94`) exempts digests attributed to `script|git blob|entry bytes|tarball`.
- `pair_verdict` (`:239-245`): `ok` iff recorded == actual; `prefix-only` iff `len(recorded) < len(actual)`
  and actual startswith recorded; **everything else is `mismatch`** (equal-length differing hex included).
- pinned-copy-search branch (`:322-354`): only for rows with the phrase "the pinned copy" **and no
  explicit copy path**; candidates = every file under `<pinned-dir>` recursively; score `(2,0)` on a
  recorded byte-count match, else `(1,cpl)` when the file digest shares ≥8 leading hex with the recorded
  digest; the best score must be **unique**, otherwise `missing.append("<ambiguous pinned copy>")`
  (`:352`); no candidate at all → `"<unpinned copy>"` (`:354`).
- `resolve_path` (`:192-215`) is tried against `roots = [repo_root, pinned_dir, md_dir]` where
  `repo_root` = parent of `corpus/` (the lane root), `pinned_dir` = the CLI arg, `md_dir` = `corpus/`.
  A directory reference expands one level to its regular files.
- `exit_code` (`:472-473`): exit 1 whenever `mismatch|prefix-only|unpinned` is non-zero. With
  `prefix_only=31` frozen as out of scope, **exit code 0 is unreachable**; the contract's P2 is written
  against the printed counters, not the exit code.
- Supersession (`:449-457`): a row whose 7th cell begins "supersedes S<id>" supersedes S<id> only if
  S<id> classifies **mismatch** and the successor classifies **ok**.

## 1. Registry rows for the six targets (full text, `corpus/SOURCES.md`)

### S125 — line 131
```
| S125 | Sibling lane tsukuroi, Memory pressure and systemd-oomd — round 25 entry — https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md (tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md at commit 157ee255, git blob be3065ae512f3fefec115a23c0e8fee2cbca9fc4) | docs | B | The sibling lane's own dated host diagnosis of this host's userspace OOM killers — systemd-oomd inactive and disabled, earlyoom active and enabled, and the `auto` default reading — cited as adjacent evidence and never absorbed as mori's own OS or unit ownership; not a primary source for any systemd, earlyoom or kernel fact, not mori's own host capture, and not a host-wide unit census | commit 157ee255 (on pushed origin/master), git blob be3065ae512f3fefec115a23c0e8fee2cbca9fc4, entry bytes sha256 ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25 (27,828 B), section MP4 (lines 196-232), "How to read this entry" > "Userspace killers" (lines 40-42), "What this entry does not claim" (lines 363-367) and the wave-2 corrections block (line 387); receipts .ufo/waves/round-25/capture/capture.txt sha256 e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136 (lines 73, 76, 79, 112-113, 121-122, 130-131, 139-140) and .ufo/waves/round-25/capture/capture-earlyoom.txt sha256 7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309 (lines 6, 9, 12, 16, 22-31) | A sibling lane's dated, digest-pinned capture can show this host's earlyoom active and enabled while systemd-oomd is inactive and disabled, and can show that systemd-oomd's `auto` default is not monitoring, without mori owning unit, package or OS state — mori cites the diagnosis and keeps the ownership | mined | 2026-10-22 | 90d | corpus/knowledge/userspace-oom-killers-r26.md |
```
- URL: `https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md`
- Anchor cell names the sibling path `tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md` (commit
  `157ee255`, git blob `be3065ae…`) **and** the two receipt copies `.ufo/waves/round-25/capture/capture.txt`
  and `.ufo/waves/round-25/capture/capture-earlyoom.txt`.
- sha256 values in the row: `ecafdcdd…` (entry bytes — exempt, "entry bytes sha256"), `e60f1bbc…`
  (capture.txt), `7adbe069…` (capture-earlyoom.txt). `git blob be3065ae…` is 40-hex, not a digest.

### S612 — line 394
```
| S612 | POSIX.1-2024 Shell Command Language, 2.9.3 Lists (AND-OR operators) — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | spec | A | AND-OR list evaluation order: which operand of each list operator runs, and their precedence; the language, not any shell implementation | §2.9.3 Lists, tag-stripped lines 1385-1386 of the pinned copy (sha256 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd, 357953 bytes, fetched 2026-11-05); quote at 1385-1386: "shall have equal precedence and shall be evaluated with left associativity" | The two AND-OR list operators associate left to right at equal precedence, so a literal left operand's status decides whether the right operand can run. | mined | 2026-11-05 | 90d | corpus/knowledge/branch-reachability-r90.md |
```
- No copy path in the row; "of the pinned copy" only. Digest `0889867a…`, 357953 bytes.

### S615 — line 397
```
| S615 | Python 3.15.2 documentation, ast — Abstract syntax trees (ast.walk and ast.get_source_segment) — https://docs.python.org/3/library/ast.html | docs | A | the structural facts a call-site pin may rely on: walk gives descendants in no specified order, and a source segment is None when location fields are missing; not execution order | ast.walk entry, tag-stripped lines 1907-1908 of the pinned copy (sha256 7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0, 362493 bytes, fetched 2026-11-05); quote at 1907-1908: "Recursively yield all descendant nodes in the tree starting at node (including node itself), in no specified order."; get_source_segment at 1881-1882: "If some location information (lineno, end_lineno, col_offset, or end_col_offset) is missing, return None." | A call-site pin keys on node identity, never on walk order, and treats a missing source segment as a failed match rather than a pass. | mined | 2026-11-05 | 90d | corpus/knowledge/branch-reachability-r90.md |
```
- No copy path; "of the pinned copy" only. Digest `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0`, 362493 bytes.

### S616 — line 398
```
| S616 | Python 3.15.2 documentation, tokenize — Tokenizer for Python source — https://docs.python.org/3/library/tokenize.html | docs | A | which tokens a tokenize scan yields, comments included; not a parse tree and not what an interpreter executes | module introduction, tag-stripped lines 38-39 of the pinned copy (sha256 6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72, 53982 bytes, fetched 2026-11-05); quote at 38-39: "The scanner in this module returns comments as tokens as well" | A comment is a token of this scanner, so a check that must see or skip a comment reads the token stream. | mined | 2026-11-05 | 90d | corpus/knowledge/branch-reachability-r90.md |
```
- No copy path; "of the pinned copy" only. Digest `6842ed0f…`, 53982 bytes.

### S622 — line 403
```
| S622 | git-log(1) — https://git-scm.com/docs/git-log | docs | A | the --diff-filter status filter (the A filter that selects added paths) and the --format=<format> option with its %h abbreviated-hash placeholder, as used to derive a file's admission commit | OPTIONS, Commit Formatting subsection, --format=<format> option, tag-stripped lines 4915-4926 of the pinned copy; DIFF FORMATTING section, --diff-filter option, tag-stripped lines 6730-6744; PRETTY FORMATS section, "Placeholders that expand to information extracted from the commit", %h placeholder, tag-stripped lines 5493-5504; git-log documentation last updated in 2.56.0, page fetched 2026-11-05, HTTP 200, 375834 bytes, sha256 f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b; quotes: "Select only files that are Added (A), Copied (C), Deleted (D), Modified (M), Renamed (R), have their type" and "abbreviated commit hash" | The A filter selects only added paths and %h prints the abbreviated commit hash, so the commit that added a path is named by an abbreviated hash rather than a full object name. | mined | 2026-11-05 | on-release | corpus/lessons/round-93.md |
```
- No copy path; "of the pinned copy" only. Digest `f206647f…`, 375834 bytes.

### S623 — line 404
```
| S623 | Python command line and environment — https://docs.python.org/3/using/cmdline.html | docs | A | the -I (isolated mode) interpreter option, as used to run the lane's counters hermetically | section 1.1.3 Miscellaneous options, -I option, tag-stripped lines 527-535 of the pinned copy; Python 3.15.2 documentation, page fetched 2026-11-05, HTTP 200, 171073 bytes, sha256 90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0; quotes: "Run Python in isolated mode. This also implies -E, -P and -s options." and "All PYTHON* environment variables are ignored, too." | Under -I the interpreter ignores PYTHON* environment variables and leaves the script directory and the user site-packages off sys.path, so a counter run under python3 -I is not steered by the caller's environment. | mined | 2026-11-05 | on-release | corpus/lessons/round-93.md |
```
- No copy path; "of the pinned copy" only. Digest `90ac3b25…`, 171073 bytes.

## 2. Resolution branch per target row (tool-internal probe)

Probe: import `tools/mori-source-digest.py` as a module, replay `extract_copy_paths` / `extract_digests` /
`resolve_path` / the pinned-search scoring on each row. Raw:

```
S125 copyrefs ['.ufo/waves/round-25/capture/capture.txt', '.ufo/waves/round-25/capture/capture-earlyoom.txt'] | allpaths ['.ufo/waves/round-25/capture/capture.txt', '.ufo/waves/round-25/capture/capture-earlyoom.txt']
   digests ['e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136', '7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309']
   exempt ['ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25']
   sizes [27828]
   pinned_phrase False same_as False
S612 copyrefs [] | allpaths []
   digests ['0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd']
   exempt []
   sizes [357953]
   pinned_phrase True same_as False
S615 copyrefs [] | allpaths []
   digests ['7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0']
   exempt []
   sizes [362493]
   pinned_phrase True same_as False
S616 copyrefs [] | allpaths []
   digests ['6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72']
   exempt []
   sizes [53982]
   pinned_phrase True same_as False
S622 copyrefs [] | allpaths []
   digests ['f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b']
   exempt []
   sizes [375834]
   pinned_phrase True same_as False
S623 copyrefs [] | allpaths []
   digests ['90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0']
   exempt []
   sizes [171073]
   pinned_phrase True same_as False
S619 copyrefs ['.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html'] | allpaths ['.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html', 'corpus/lessons/round-91.md']
   digests ['7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5']
   exempt []
   sizes [362493]
   pinned_phrase True same_as False
```

Branches:

| row | branch | why |
|---|---|---|
| S125 | **named path** (2 receipt copies) | `.ufo/waves/…` paths are copy refs via `PINNED_LOC_RE`; no "the pinned copy" phrase, so the pinned-search branch does not apply. The sibling path `tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md` is **not** a copy reference (`PATH_RE` lookbehind rejects `owner/repo/`), and its digest `ecafdcdd…` is **exempt** ("entry bytes sha256"). |
| S612 | **pinned-copy-search** (byte count 357953) | no path, phrase present, no "same bytes as S<n>". |
| S615 | **pinned-copy-search** (byte count 362493) | same shape; no named path, no directory ref. |
| S616 | **pinned-copy-search** (byte count 53982) | same shape. |
| S622 | **pinned-copy-search** (byte count 375834) | same shape. |
| S623 | **pinned-copy-search** (byte count 171073) | same shape. |

No target uses the "same bytes as S<n>" branch; no target uses a directory reference; only S125 uses a
named path. Only 5 rows in the whole registry use the pinned-search branch — exactly S612/S615/S616/S622/S623.

## 3. What each target needs under `corpus/evidence/` to resolve (no row edit)

Names below are the file names I would use; for the five pinned-search rows the **name is arbitrary**
(resolution is by byte count, then digest prefix), the **content** is what matters, and the file must sit
under `corpus/evidence/` (the `pinned-dir` argument) — the search walks that directory recursively.

- **S612** → `corpus/evidence/posix-shell-v3-chap02.html`: the POSIX `V3_chap02.html` bytes, exactly
  357953 B, sha256 `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`.
  Live fetch reproduces it exactly (HTTP 200, 357953 B, same digest, two fetches byte-identical):
  ```
  V3_chap02.html http=200 357953 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd
  V3_chap02.b.html http=200 357953 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd
  ```
  → resolves **ok**. (Already placed at HEAD as `corpus/evidence/posix-shell-v3-chap02.html`.)
- **S622** → `corpus/evidence/git-log-docs.html`: the git-log(1) page bytes, 375834 B, sha256
  `f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b`. Live fetch reproduces it exactly:
  ```
  git-log.html http=200 375834 f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b
  git-log.b.html http=200 375834 f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b
  ```
  → resolves **ok**. (Already placed at HEAD as `corpus/evidence/git-log-docs.html`.)
- **S125** → two files under `corpus/evidence/.ufo/waves/round-25/capture/`:
  `capture.txt` (5607 B, sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`) and
  `capture-earlyoom.txt` (1037 B, sha256 `7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309`).
  These byte values exist in the **sibling lane**:
  ```
  e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136  tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt
  7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309  tsukuroi-shokunin/.ufo/waves/round-25/capture/capture-earlyoom.txt
  ```
  Mirroring them under `corpus/evidence/.ufo/waves/round-25/capture/` resolves S125 **ok** (measured;
  also already placed at HEAD by the sibling seat).
- **S616** → `corpus/evidence/python-tokenize-3.15.2.html`: the tokenize.html bytes of the **00:37 UTC
  build**, 53982 B, sha256 `6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72`. That exact
  file is already in the lane and matches the recorded digest exactly:
  ```
  6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72  mori-shokunin/.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-tokenize-3.15.2.html
  ```
  → resolves **ok**. **The live page fetched today does NOT match** (see §5b): it hashes
  `91bea7a659ed4cf3ea66d9552480c3f2c4cb02066219c527b2c56f0594106758`.
- **S623** → `corpus/evidence/python-cmdline-3.15.2.html`: the cmdline.html bytes of the **08:02 UTC
  build**, 171073 B, sha256 `90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0`. No such
  file exists in the lane or in the fleet; it is reproducible byte-exactly from today's live page by
  restoring the single differing line (`Last updated on Nov 05, 2026 (08:02 UTC)`); the result hashes to
  the recorded digest:
  ```
  patched sha 90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0 want 90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0 equal True
  ```
  → resolves **ok**.
- **S615** → **no file can make it `ok`** (see §5a). What it needs to leave the `unpinned` bucket is one
  resolvable candidate of the recorded byte count 362493 (or ≥8 shared digest prefix) under
  `corpus/evidence/`, e.g. `corpus/evidence/python-ast-3.15.2.html` holding the 00:37 UTC ast.html bytes
  (362493 B, sha256 `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5`, present in the lane
  at `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html`). The tool then classifies S615
  `mismatch`, and successor row **S619** (already `ok`, teaches cell begins "supersedes S615") supersedes
  it, so S615 prints `superseded-by S619` and is counted neither in `mismatch=` nor in `unpinned=`.
  Measured: `DIGEST S615 superseded-by S619`.

Placement hazards measured (negative controls, scratch copies of `corpus/evidence`):
- A second file with the same recorded byte count makes the best score non-unique → `"<ambiguous pinned
  copy>"` → the row falls back to `unpinned`:
  ```
  NEG3 (duplicate 357953-byte copy): DIGEST S612 unpinned … ; DIGEST_CHECK rows=124 ok=90 mismatch=0 superseded=2 prefix_only=31 unpinned=1
  ```
  → place **exactly one** file per recorded byte count (357953 / 362493 / 53982 / 375834 / 171073 are all
  distinct, so the five placements do not collide with each other).
- A same-size file with wrong content → `mismatch`, not `ok`:
  ```
  NEG2: DIGEST S612 mismatch recorded=0889867a… actual=4ff5d5f097b94df89f0ee2e30c87c570e6459a3dbda09579a1866c316c2262fa
  ```
- Corrupting one S125 receipt → S125 `mismatch`:
  ```
  NEG1: DIGEST S125 mismatch recorded=e60f1bbc… actual=e60f1bbc…
  ```

## 4. Does anything already under `corpus/evidence/` match a target's recorded digest?

Entering HEAD `66c5518e` tree of `corpus/evidence` (345 files), full sha256 over every file:

```
$ git archive 66c5518e… corpus/evidence | tar -x -C $S/enter-evidence ; find … -type f | wc -l
345
$ grep -cE '^(0889867a…|7891c588…a6f0|6842ed0f…|f206647f…|90ac3b25…|e60f1bbc…|7adbe069…)' enter-evidence.sha256
0
--- prefix>=8 hits:
prefix>=8 hits: 0
```
→ **At the entering HEAD, no file under `corpus/evidence/` matched any of the six targets' recorded
digests — not exactly, not even by an 8-hex prefix.**

Whole-lane scan (31 054 files) and lane git-object scan (23 361 objects) for the same digests:

```
HIT S612 mori-shokunin/.ufo/waves/round-89/evidence/sources-r89/posix-shell-v3-chap02.html
HIT S612 mori-shokunin/.ufo/waves/round-90/w1/Mo90S01Sources/sources/posix-shell-v3-chap02.html
HIT S616 mori-shokunin/.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-tokenize-3.15.2.html
GIT-HIT S612 d9cf6d822b5c1bf1233e23d9fbe4d5504027ba4c 357953
GIT-HIT S616 70cced558632b5d791034504fac1bbf527295331 53982
```
- **S615's recorded digest matches nothing** in the lane tree or in lane git history.
- **S623's recorded digest matches nothing** in the lane tree or in lane git history.
- S612's and S616's recorded digests match archived copies already inside the lane (r89 / r90 wave dirs).
- S125's two receipt digests match only files in the **sibling lane** `tsukuroi-shokunin`
  (`.ufo/waves/round-25/capture/*`); mori has no copy of them at the entering HEAD.
- After the sibling seat's landing commit `9bde9322`, `corpus/evidence/` now holds
  `posix-shell-v3-chap02.html`, `git-log-docs.html`, `.ufo/waves/round-25/capture/capture.txt`,
  `.ufo/waves/round-25/capture/capture-earlyoom.txt`, and the tool run at HEAD reports
  `DIGEST_CHECK rows=124 ok=89 mismatch=0 superseded=1 prefix_only=31 unpinned=3`
  (remaining unpinned: S615, S616, S623).

## 5. Impossibilities, with the causing line

### 5a. S615 can never be `ok` — its recorded digest is a corrupted hex string
The recorded digest `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0` shares its first
**51 hex chars** with the true sha256 of the ast.html copy (`…c82587ac94b0f83b9a8a42f5`) — the tail
`8f1a60ad1a6f0` vs `0f83b9a8a42f5` is transcription damage, not a different document:

```
common leading hex chars: 51 of 64 -> shared prefix 204 bits
rec tail 8f1a60ad1a6f0 | true tail 0f83b9a8a42f5
```
A 204-bit shared prefix cannot arise by chance between two independent sha256 values, so the recorded
value is a corrupted transcription of the true digest; no byte string can hash to it.
- Causing lines: `corpus/SOURCES.md:397` (anchor cell records the corrupted digest) and
  `tools/mori-source-digest.py:239-244` (`pair_verdict`: equal-length differing hex → `mismatch`, never
  `ok`, and `prefix-only` needs `len(recorded) < len(actual)`).
- Consequence for the frozen P2 (`unpinned=0 mismatch=0 prefix_only=31 ok=92`): S615 can leave
  `unpinned` only via `mismatch` → `superseded-by S619`, i.e. it is counted in `superseded=`, **not** in
  `ok=`. Measured landing with all six copies in place (scratch copy of `corpus/evidence`, real
  `corpus/SOURCES.md`):
  ```
  DIGEST S125 ok / DIGEST S612 ok / DIGEST S615 superseded-by S619 / DIGEST S616 ok / DIGEST S622 ok / DIGEST S623 ok
  DIGEST_CHECK rows=124 ok=91 mismatch=0 superseded=2 prefix_only=31 unpinned=0
  ```
  So the achievable counter set by copy placement alone is **ok=91, superseded=2, unpinned=0,
  mismatch=0, prefix_only=31** — one short of the contract's `ok=92`. Reaching `ok=92` needs one
  additional registry row (e.g. a new `supersedes S615` row recording the correct ast.html digest
  `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5` and naming the placed copy),
  which would make rows=125, ok=92, superseded=2. That is a row addition, i.e. executor/L1 territory,
  not a scout edit — reported, not done.
  (S619 already carries that digest and already resolves `ok` via its own named path
  `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html`, which resolves under
  `repo_root`.)
- Historical corroboration in-repo: `.ufo/waves/round-91/w1/Mo91Sc02Lesson.md:12,44-45` and
  `.ufo/waves/round-92/w1/Mo92E01Digest.md:21` record exactly this corruption and its correction.

### 5b. S616 and S623 cannot be pinned from a *fresh live fetch* — the recorded digests are build-specific
`docs.python.org` pages embed a per-build line `Last updated on Nov 05, 2026 (HH:MM UTC)`, so the served
bytes change with each rebuild. The two fetches I took minutes apart are byte-identical (same build),
but the build moved since the round-90/93 fetches:

```
$ grep -o 'Last updated on[^<]*' ast.html        -> Last updated on Nov 05, 2026 (12:03 UTC)
$ grep -o 'Last updated on[^<]*' tokenize.html   -> Last updated on Nov 05, 2026 (12:03 UTC)
$ grep -o 'Last updated on[^<]*' cmdline.html    -> Last updated on Nov 05, 2026 (12:03 UTC)
live ast.html      5e531ef083fe5255fe45b6148bf07eec5d595bf8d9791537aa307242832ab696   (recorded S615: 7891c588…a6f0)
live tokenize.html 91bea7a659ed4cf3ea66d9552480c3f2c4cb02066219c527b2c56f0594106758   (recorded S616: 6842ed0f…)
live cmdline.html  f0a033694b4368dad6f54616e94d7f13452a59ce28cc0b29d9bb91ef85a53cdf   (recorded S623: 90ac3b25…)
diff r90 tokenize copy vs live tokenize:
704c704
<       Last updated on Nov 05, 2026 (00:37 UTC).
---
>       Last updated on Nov 05, 2026 (12:03 UTC).
```
- S616's recorded digest equals the 00:37 build (archived in-lane, byte-exact) → the archived bytes
  resolve it `ok`; a fresh fetch yields `mismatch` (equal length, differing hex → `pair_verdict`).
- S623's recorded digest equals the 08:02 build; no such file exists in the fleet (two fleet scans — all
  files ≤500 k with `.git` excluded, and all files of the three recorded byte sizes 362493 / 171073 /
  53982 — found only the two tsukuroi S125 receipts and the mori r90 copies; a byte-exact copy would be
  171073 B, so the size scan covers every candidate) — the only byte-exact route is the
  timestamp-restored reconstruction, whose sha256 equals the recorded digest.
- Causing lines: `corpus/SOURCES.md:398` and `:404` (anchor cells record build-specific digests) plus
  the page content itself; the tool line that turns a differing equal-length digest into `mismatch` is
  `tools/mori-source-digest.py:239-244`.
- Contract tension to flag: the contract's method constraint says "a copy is pinned only if its **live
  bytes, fetched this round** with an access date, hash to the row's recorded digest". Under that literal
  rule S616 and S623 stay unpinned and are named stale, and C2 is unmet; under the tool's own measurement
  (what P2 measures) the archived/reconstructed bytes that hash to the recorded digests resolve both rows
  `ok`. I did not edit the row and did not decide this; it is the L1's call which reading governs.

### 5c. S125 — the sibling-repo path is not a local copy reference (not an impossibility, but a trap)
`corpus/SOURCES.md:131` names `tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md`; `PATH_RE`'s
lookbehind (`tools/mori-source-digest.py:84`) rejects `owner/repo/`-prefixed paths, and the row's
`ecafdcdd…` digest is exempt as "entry bytes sha256" (`NONCOPY_ATTR_RE`, `:94`). The row's *checkable*
copies are therefore only the two `.ufo/waves/round-25/capture/*` receipts, which exist byte-exactly in
the sibling lane and are mirrorable. Nothing is impossible here; the sibling-lane path simply does not
participate in resolution.

## 6. Unrun / not done

- Fleet-wide byte-for-byte digest scan of every file in `/home/vgpnk/Projects/shokunin` at **all** sizes —
  **unrun**: the first pass hit the 300 s cap and I stopped the next pass on L1 instruction. Coverage
  achieved instead: entire lane tree (31 054 files) + all lane git objects (23 361), the entering-HEAD
  `corpus/evidence` tree (345 files), a fleet scan of all files ≤500 k excluding `.git` (completed, 3.4 s),
  and a fleet scan restricted to the three recorded byte sizes 362493 / 171073 / 53982 (completed).
- No `curl` fetch of the sibling lane's GitHub raw URL for S125 (the receipt files were taken from the
  local sibling clone instead) — **not run**.
- `--selftest` of `tools/mori-source-digest.py` — **not run** (out of scope for this reconnaissance).
- `scripts/sources-census.sh` (CORPUS §2b census) — **not run** by this seat.
- No edit of `corpus/SOURCES.md`, `tools/`, `corpus/`, SCORECARD.md, LOG.md or MANIFEST.json; no git/jj
  mutation; no host sysctl/service/limit change; no tool installation.

## 7. Summary of verdicts

- S125 — named-path branch; mirror the two sibling receipt bytes to
  `corpus/evidence/.ufo/waves/round-25/capture/{capture.txt,capture-earlyoom.txt}` → `ok` (already done
  at HEAD by the sibling seat).
- S612 — pinned-search; POSIX `V3_chap02.html` bytes (357953 B) → `ok` (already done at HEAD).
- S615 — pinned-search; **cannot be `ok`** (corrupted recorded digest, §5a); a 362493-byte ast.html copy
  makes it `superseded-by S619`, so `unpinned=0`/`mismatch=0` hold but `ok` stays at 91 unless one more
  registry row is added.
- S616 — pinned-search; the 00:37 UTC tokenize.html bytes (53982 B, archived in-lane) → `ok`; a fresh
  fetch is `mismatch` (§5b).
- S622 — pinned-search; git-log(1) page bytes (375834 B, live fetch reproduces) → `ok` (already done at HEAD).
- S623 — pinned-search; the 08:02 UTC cmdline.html bytes (171073 B, reconstructible; sha256 equals the
  recorded digest) → `ok`; a fresh fetch is `mismatch` (§5b).
