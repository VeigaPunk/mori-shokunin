# W1 review — QUALITY 81 gate `check-row-identity.py` (MoriR28.ReviewRowIdentityCheck)

Seat: reviewer, leaf (no subagents). Subject: `.ufo/waves/round-27/check-row-identity.py`, blob taken at
`df886be1` (the round-27 QUALITY 81 gate that round-28 C1 relies on; `corpus/QUALITY.md:372-376` states the
criterion: a row keeps its first-published cells, only `status`/`recheck`/`used-by` change in place, the check
"must print `changed=0`, exit 0").

**Verdict: the gate is sound for the lane as it exists (merges: proven; committed-bytes-only: proven;
id-reuse-after-delete: caught; escaped pipes, duplicates, malformed rows: caught). Three fail-open paths found,
one of them real-but-latent (file rename), one a wording/semantics gap (whitespace vs "byte-equal"), one a
missing guard (table that never parses). Fixes are one-to-five lines each; none block C1's declared before
state, which I reproduce exactly.**

Tooling: nothing installed (python 3.14.8 and git 2.56.0 already present; pacman transactions are paused
host-wide and no install was needed). Sandbox: scratch clone `sb2` (`git clone --no-hardlinks`) plus tiny
standalone repos, all under `/fast/scratch/hyaku/mori-r28/MoriR28.ReviewRowIdentityCheck/`. Scripts kept there:
`repro2.sh`, `repro3.sh` (an earlier `repro.sh` had section-contamination bugs of my own and is superseded).

## 1. Runs at the two revs (lane, read-only; paste-ready)

The blob is identical at both revs (`git show <rev>:… | diff` → IDENTICAL), and the worktree copy is identical
to the `df886be1` blob (`git diff df886be1 --stat -- .ufo/waves/round-27/check-row-identity.py` → empty).

```sh
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 -I -B .ufo/waves/round-27/check-row-identity.py 6ebd518f; echo EXIT=$?
changed S096 cells=teaches
changed S097 cells=anchor,teaches
changed S101 cells=teaches
rows=144 changed=3 removed=0 bad=0
EXIT=1
$ python3 -I -B .ufo/waves/round-27/check-row-identity.py df886be1; echo EXIT=$?
changed S096 cells=teaches
changed S097 cells=anchor,teaches
changed S101 cells=teaches
rows=144 changed=3 removed=0 bad=0
EXIT=1
```

This matches the contract's declared before state (`row_identity=rows=144 changed=3 removed=0 bad=0`, exit 1,
`.ufo/waves/round-28/contract.md` C1 section) and routed defect 3
(`corpus/lessons/round-27-verifier-spotcheck.md:142-145`: S096/S097/S101 still differ from first-published).

## 2. Semantics (blob `df886be1`, line numbers from `git show df886be1:<path>`)

- `:22` mutable cells = `{"status","recheck","used-by"}` — matches QUALITY 81 (`corpus/QUALITY.md:373-374`).
- `:23` a "row" is any line with ≤3 leading spaces, a pipe, then `S<digit>`; `:24` cells split on unescaped
  pipes (`(?<!\\)\|`); `:37` every cell stripped; `:25` id must fullmatch `S[0-9]{3,}`.
- `:56` reads `<rev>:corpus/SOURCES.md`; `:64` first-published candidates from
  `git log --full-history --topo-order --reverse <rev> -- corpus/SOURCES.md`; `:66-67` `first.setdefault` per
  id in walk order; `:73` an id with no history compares against itself (new rows always pass); `:74` diff of
  non-mutable cells; `:79` exit 1 if changed/removed/bad else 0; exit 2 for bad rev / no arg / missing file
  (verified: `bad_rev`=2, usage=2, `missing_file`=2).

## 3. The seven assigned questions, each with repro and result

### 3.1 Merges — survives (proven two ways)
- Sandbox (sb2, S3): branch m1 adds row S200, branch m2 edits S100's `status` (mutable), both merged `--no-ff`:
  `rows=145 changed=3 removed=0 bad=0` (baseline defects only) — new ids and mutable edits through merges are
  handled, and the merged rows are compared like any other.
- Evil merge (S4): conflicting edits of S060's `teaches` resolved to a third value ("EVIL") — the gate prints
  `changed S060 cells=teaches` (plus `duplicate S060 line=69`, an artifact of my conflict resolution leaving two
  S060 rows — which incidentally confirms duplicate detection). `--full-history` includes merge results that
  differ from all parents.
- Decisive, on the real history (S14 probe, sb2 at 6ebd518f): I rebuilt the first-published map from the gate's
  log walk (31 commits touch the path) and from a full `git rev-list --topo-order --reverse` walk (243 commits,
  file present in 202): `ids-log=144 ids-full=144`, `only-in-full=none only-in-log=none cell-mismatches=none`.
  The lane has 2 merges at `df886be1`; none hide a blob from the gate. Every id's first-published commit is
  found: S096→`df4db54a`, S101→`90ed9b77`, S144→`df886be1` (useful for the scribe restoring rows).

### 3.2 Renames — fail-closed as written, FAIL-OPEN once the gate path is repointed (latent: 0 renames in lane)
Repro (sb2, S6): commit moves `corpus/SOURCES.md` → `docs/SOURCES.md` **and** edits S070's `teaches` in the
same commit, then run the gate twice:

```text
# gate as written (PATH=corpus/SOURCES.md):
missing_file
exit=2                      ← fail-closed
# same commit, PATH repointed to docs/SOURCES.md (the realistic repair):
rows=144 changed=0 removed=0 bad=0
exit=0                      ← FAIL-OPEN: the S070 teaches edit smuggled into the rename commit escapes
```

Root cause: `git log --full-history -- <path>` (script `:64`) starts at the rename commit; pre-rename history is
invisible. `--follow` does NOT rescue it: `git log --follow --full-history --topo-order --reverse` on the moved
path returned **1 commit** (git 2.56.0) — the combo silently degrades. Lane exposure: 0 renames of
`corpus/SOURCES.md` in history (`git log --follow --name-status` → no `R` entries), so this is latent, not
exercised. **Fix (boring, proven):** replace the path-bounded log with
`git rev-list --topo-order --reverse <rev>` and `git show c:PATH` whenever present — measured cost 243 vs 31
`git show` calls, and S14 proves it yields the identical first-published map. It is rename-proof and
merge-proof by construction. Do not use `--follow`.

### 3.3 Whitespace-only cell changes — pass by design; "byte-equal" claim wording is stronger than the gate
Repro (sb2, S7redo): S080's `source` cell padded with one space on each side — bytes differ
(`1 file changed, 1 insertion(+), 1 deletion(-)`; diff shows `| S080 | Linux…` → `| S080 |  Linux…`) —
summary stays `rows=144 changed=3 removed=0 bad=0` (no new changed line). Cause: `:37` strips every cell, and
the diff at `:74` compares stripped cells. In a clean repo this prints `changed=0 … exit=0` for non-byte-equal
content. The gate implements QUALITY 81's "keeps its first-published cells" (cell-level equality modulo
surrounding whitespace) — but the C1 claim sentence "restored **byte-equal** to their first-published cells"
(`contract.md` C1) promises more than the gate enforces. **Fix:** either compare raw cell text for non-mutable
columns (one-line change at `:74`), or soften the claim wording to "cell-equal (surrounding whitespace
ignored)". L1's call; not a C1 blocker.

### 3.4 Escaped pipes — fail-closed in both directions
Repro (sb2, S8): cell gains `a\|b` (escaped): still 13 cells, the backslash stays in the content →
`changed=4` including `S090 cells=teaches` — caught as a content change. Cell gains raw `a|b`: 14 cells →
`removed=1 bad=1` — caught as malformed. The real table has zero escaped pipes at 6ebd518f
(`grep -cF '\|'` on the blob = 0). Edge, reasoned not repro'd: a cell ending in a literal backslash before a
separator (`\\|`) is misread as an escaped pipe, merging two cells → malformed → still fail-closed.

### 3.5 Row moved to another line — intended pass
Repro (sb2, S9): S100's row moved above other rows: `rows=144 changed=3 removed=0 bad=0` (baseline only).
Identity is id-keyed (`:66-67`); line numbers appear only in malformed/duplicate diagnostics. CORPUS constrains
cells, not position, so this is correct behavior.

### 3.6 Id reused after delete — caught; the C1 repair shape passes
Repro (sb2, S5, across a merge): delete S096, merge the deletion, then
- re-add the **exact first-published line** (from commit `df4db54a`): `changed=2` — S096 is cleared, only the
  pre-existing S097/S101 defects remain, `removed=0` → the exact repair C1 declares is accepted;
- re-add with one mutated cell: `changed S096 cells=teaches` → caught.

Sub-case, two incomparable introductions (orphan branch merged with `--allow-unrelated-histories`, standalone
repo): with the merge result set to the orphan variant, the gate printed `changed S001 cells=teaches`, exit 1 —
in the observed ordering it picked the main-line root as first-published and caught the mutation. Caveat:
`first.setdefault` (`:67`) resolves a tie between incomparable introductions by `--topo-order` position, which
is deterministic per git build but not ancestry-defined. Low severity; see FO-4.

### 3.7 Committed bytes only — proven
Repro (sb2, S2redo): worktree S096 `teaches` edited to `UNCOMMITTED teaches`, an extra `S999` row appended, all
staged: output identical to the clean baseline (`rows=144 changed=3 removed=0 bad=0`) — no worktree bytes, no
index bytes read. Corroborated on the lane itself: the lane worktree is dirty right now
(`M corpus/SOURCES.md`, 18 dirty paths) and the lane runs in §1 are byte-identical to the clean-clone runs
(S1). Rev is passed as an explicit hash; repo is not shallow (`rev-parse --is-shallow-repository` = false), no
replace refs (0), no grafts. `rev-parse`/`show`/`log` are plumbing and take no locks.

## 4. Additional paths probed

- Table indented by 4 spaces on a lane-shaped history (S10): rows unparseable → `rows=0 removed=144` exit 1 —
  a wipe/reformat of the table is caught via `removed`.
- `rows=0` from day one (fresh repo whose table never parses, S12): `rows=0 changed=0 removed=0 bad=0`,
  **exit 0** — fail-open; see FO-3.
- Duplicate id at rev (S11): `bad=1` exit 1 (first occurrence wins, duplicate reported).
- Historical schema stability (S14): every one of the 202 commits carrying the file parses with `bad=0`; row
  count grows 33 → 137 with the same 11-column shape since the first commit `1f07f1dd`. No schema drift, so the
  "first-published" base is never silently reset by a column change.

## 5. Fail-open / fail-closed inventory

| # | Path | Direction | Evidence | Fix |
|---|------|-----------|----------|-----|
| FO-1 | File renamed + gate PATH repointed: pre-rename history invisible | **fail-open** (latent; 0 lane renames) | §3.2 sb2 S6: `changed=0 removed=0` exit 0 over an edited rename commit; `--follow --full-history` returns 1 commit | Full `git rev-list --topo-order --reverse <rev>` walk, parse PATH whenever present (S14-proven equivalent) |
| FO-2 | Whitespace-only cell change vs "byte-equal" claim wording | fail-open (semantics gap) | §3.3 sb2 S7redo: bytes differ, no changed line | Compare raw cells at `:74`, or align claim wording with cell-level equality |
| FO-3 | Table never parses in the whole history | fail-open | §4 S12: `rows=0` exit 0 on fresh repo | Guard: if `not now and not first` → print `empty_registry`, exit 2 (one line before `:79`) |
| FO-4 | Id introduced twice on incomparable roots; `setdefault` tie | ambiguous (observed fail-closed) | §3.6 orphan repo: mutation caught; tie-break is implementation-defined | Count distinct introduction commits per id; >1 → report line counted in `bad` |
| FC-1 | Immutable cell changed (incl. via evil merge) | fail-closed | lane §1; sb2 S4 | — |
| FC-2 | Id deleted then re-added with mutated cells | fail-closed | sb2 S5 r2 | — |
| FC-3 | Raw pipe (cell-count break), duplicate id, non-`SNNN` id | fail-closed | sb2 S8/S11 | — |
| FC-4 | Table wiped/reindented on any repo with row history | fail-closed (via `removed`) | sb2 S10 | — |
| FC-5 | Missing file / bad rev / no arg | fail-closed, exit 2 | sb2 S6; lane badrev probe | — |

## 6. Residual risk and verification gaps

- FO-1 is latent in the lane (no renames ever), but C1's counter and gate share the path constant; if a later
  round moves the registry, the quiet variant is the dangerous one. The rev-list-walk fix removes the whole
  class and costs ~1.4 s at the current history size.
- The `\\|` false-escape edge (§3.4) and the FO-4 tie ordering are reasoned/observed for one shape on
  git 2.56.0; other git versions may order incomparable commits differently (still deterministically).
- I did not fuzz arbitrary malformed markdown beyond the shapes listed; other review seats own the counter
  (`count-c1.sh`) — I verified only the gate it wraps.
- `count-c1.sh` greps the gate's exact summary line; any fix must keep the `rows=… changed=… removed=… bad=…`
  format and the 0/1/2 exit contract (`contract.md` C1 counting command).
- Not checked here (out of seat): whether the round-28 rows themselves restore byte-equal cells — the gate
  would accept whitespace-padded restorations (FO-2); the scribe should use the exact `df4db54a`/`90ed9b77`
  lines (S096/S101 first-published commits, §3.1).
