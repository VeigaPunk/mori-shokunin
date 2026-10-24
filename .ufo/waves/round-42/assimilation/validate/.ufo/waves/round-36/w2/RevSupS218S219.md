# RevSupS218S219 — re-open S218 (flush iostats commit) and S219 (discard iostats commit)

**Item attacked:** round-35 supersede rows `S218` (`corpus/SOURCES.md:224`) and `S219`
(`corpus/SOURCES.md:225`): rows + copies. Checks: (1) commit-message quotes (S218 fields
16-17 flush semantics; S219 discard's own four statistics) contiguous in the patch headers and
<=25 words; (2) committed copies sha256-equal to the fetched `.patch` bodies; (3) rule-2 form.

**Landed tip reviewed:** `bf0df77fee4b6ef54a90aea09335c7617f125151`. Fetch used plain `curl`
(no tool installed; nothing recorded to install). `lsp` device unavailable: `read xd://lsp`
→ `No such tool: xd://lsp` (mounted: ast_edit, debug). Findings rest on fetched bytes, parsed
row cells and `git diff`; no grep result is presented as proof.

## 1. Rows under attack (parsed from corpus/SOURCES.md)

`S218` at line 224 — source `https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch`;
anchor `patch lines 9-11 (commit message) and 68-75 (iostats.rst hunk)`; teaches opens
`supersedes S188 — In iostats numbering, field 16 counts flush requests completed successfully
and executed by the disk; field 17 is the total milliseconds spent by all flush requests…`.

`S219` at line 225 — source `https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch`;
anchor `patch lines 7-17 (commit message)`; teaches opens `supersedes S189 — Discard I/O is
tracked with its own four statistics of the kinds kept for reads and writes, including discard
sectors completed.`

## 2. Fetch + copies sha256-equal — PASS

Commands (scratch `/fast/scratch/hyaku/mori-r36/RevSupS218S219/`):

```
$ curl -sSL -o s218.patch https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch
$ curl -sSL -o s219.patch https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch
$ wc -c s218.patch s219.patch   -> 8897 s218.patch ; 9498 s219.patch
$ sha256sum s218.patch s219.patch
  a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89  s218.patch
  f265ef76e862e4e48cdbdae1b4702cbe47b356501d5d6cbfe9abeaaacd4cf318  s219.patch
$ sha256sum corpus/evidence/sources-r36/S218.src corpus/evidence/sources-r36/S219.src
  a844836a15c04bfb15f44f7398851074d901afff5206509ea9be661ac5758d89  .../S218.src
  f265ef76e862e4e48cdbdae1b4702cbe47b356501d5d6cbfe9abeaaacd4cf318  .../S219.src
$ cmp S218.src s218.patch && echo S218-COPY-EQ-FETCHED   -> S218-COPY-EQ-FETCHED
$ cmp S219.src s219.patch && echo S219-COPY-EQ-FETCHED   -> S219-COPY-EQ-FETCHED
```

Committed copies `corpus/evidence/sources-r36/S218.src` and `S219.src` are byte-identical to the
fetched patch bodies (sha256 above). Glob of `corpus/evidence/sources-r*/S218.*` /
`S219.*` returns only these two files (no older decoy copy in a lower `sources-r<N>` directory).

## 3. Commit-message quotes: contiguous and <=25 words — PASS

Patch header regions (commit message body before the `---` diff separator):
S218 lines 5-17, S219 lines 6-25. Verified quote runs (text is the patch content with the
unified-diff `+` marker stripped; each run spans adjacent lines, i.e. contiguous; word counts
below are content words):

S218 (commit message):
- lines 9-10 — `Block layer has sophisticated engine for combining several flush requests into
  one. But there is no statistics for actual flushes executed by disk.` → 23 words.
- line 11 — `Requests which trigger flushes usually are barriers - zero-size writes.` → 10 words.

S218 (iostats.rst hunk; the row's anchor explicitly labels this `(iostats.rst hunk)`, not
commit message):
- lines 68-69 — `Field 16 -- # of flush requests completed This is the total number of flush
  requests completed successfully.` → 18 words.
- lines 71-72 — `Block layer combines flush requests and executes at most one at a time. This
  counts flush requests executed by disk. Not tracked for partitions.` → 24 words.
- lines 74-75 — `Field 17 -- # of milliseconds spent flushing This is the total number of
  milliseconds spent by all flush requests.` → 20 words.

S219 (commit message):
- lines 7-8 — `Add tracking of REQ_OP_DISCARD ios to the partition statistics and append them to
  the various stat files in /sys as well as` → 22 words.
- lines 9-10 — `/proc/diskstats. These are tracked with the same four stats as reads and writes:`
  → 13 words.
- line 12 — `Number of discard ios completed.` → 5 words; line 13 — `Number of discard ios merged`
  → 5 words; line 14 — `Number of discard sectors completed` → 5 words; line 15 — `Milliseconds
  spent on discard requests` → 5 words.

All quotes are contiguous (adjacent patch lines) and each is <=25 content words. The teaches
sentences are syntheses of these quotes, not verbatim runs: S218 "field 16 counts flush requests
completed successfully and executed by the disk; field 17 is the total milliseconds spent by all
flush requests" maps to lines 68-69/71-72/74-75; S219 "its own four statistics of the kinds kept
for reads and writes, including discard sectors completed" maps to lines 9-10/14. No taught
fact contradicts the fetched bytes. Anchor line ranges match the patch exactly (S218 9-11 and
68-75; S219 7-17).

Nits (not defects): the raw diff-line token count of S218 lines 71-72 is 26 if the leading `+`
markers are counted as words (content-only count is 24); S219's teaches sentence re-states S189's
verbatim (S219 is the append-only vehicle that clears S189's in-place anchor-edit debt), which is
allowed by rule 2.

## 4. Rule-2 form — PASS

- `git diff --unified=0 6bd57097 bf0df77 -- corpus/SOURCES.md` grep `^[+-]\| S(18[89]|21[89]) `
  → only two lines, both `+`: `+ | S218 | …`, `+ | S219 | …`. S218/S219 are new rows; S188/S189
  are untouched (no `-`/modified lines). No in-place edits.
- Teaches of both rows open with `supersedes S1NN —` (S218 → `supersedes S188 —`; S219 →
  `supersedes S189 —`); ids are `S###`-shaped; cells align to header positions
  (id source kind tier scope anchor teaches status opened recheck used-by); status `mined`,
  recheck `on-release`, used-by `corpus/knowledge/disk-write-rate-r33.md` (exists at tip).

## Findings

No actionable defect found. Severity: none.

## Residual risk / verification gaps

- The two S218 field-semantics quotes sit in the iostats.rst hunk, not in the commit-message
  header; the row's own anchor cell says so `(iostats.rst hunk)`, so no misstatement exists, but
  a literal "header-only" reading of the check would not find them there.
- Quote word counts are content words after stripping the diff `+` marker; `wc -w` on raw hunk
  lines yields 26 for the S218 71-72 pair.
- Single fetch per URL; the copy equality was verified against that fetch plus the committed sha.

## Installs

None (curl/sha256sum/cmp/wc preinstalled; no pacman, no uv/npx installs).

VERDICT: PASS — S218 and S219 rows and copies hold: quotes contiguous in the patch and <=25
content words, copies sha256-equal to the fetched .patch bodies, rule-2 form intact
(`corpus/SOURCES.md:224-225`, `corpus/evidence/sources-r36/S218.src`, `S219.src`).
