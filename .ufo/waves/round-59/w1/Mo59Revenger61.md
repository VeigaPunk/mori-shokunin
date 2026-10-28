# Mo59Revenger61 — `report_file` extra keys: which rounds, when, and what the writer history shows

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only; no commits, no VCS mutation,
no production/corpus/SCORECARD/LOG edits). Frozen contract read at
`.ufo/waves/round-59/contract.md`; frozen counters read at
`.ufo/waves/round-59/count-c1.py`, `.ufo/waves/round-59/count-c2.py`.
Freeze `60b3a76ad0524c8978cc51922940be1c8c388915`, entering
`2b9f03975bfb6e508f35074ac8181ec8bf54e805`, lane HEAD at read time
`8ff344ff18924c1ea63d46c3b3969f9fea05bc51`.

## Question

The round-59 C2 scan arm asserts (§Contract C2, scan arm): the five r54–r58
`*-results.json` MUST scan OK with `members==seats`, and
`.ufo/waves/round-53/w1-results.json` MUST scan FAIL "(`report_file` extra keys —
schema drift, reported not fixed)". This seat asks: which rounds carry that field, when
did it appear/disappear, and what the pattern implies about settlement-writer versions.

## Bounded method

1. Enumerated every `*-results.json` under `.ufo/waves/` (16 files) and parsed every JSON
   file under `.ufo/waves/` (1,813 files) looking for an object key `report_file`,
   anywhere in the tree.
2. Ran `grep -rl '"report_file"' .` at lane root (all file types, whole lane).
3. Per-artifact-history check: `git log --all -p -- <file> | grep -c '^+.*"report_file"'`
   for every `*-results.json`.
4. Added-file provenance: `git log --diff-filter=A --format='%h %ad' --date=iso-strict -1 -- <file>`
   for every `*-results.json`.
5. Reproduced the frozen scan arm with the frozen tool (sha256 =
   `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9`, equal at HEAD and at
   freeze `60b3a76`; absent at entering `2b9f0397`, where `git show` prints
   `path 'tools/mori-settlement-scan.py' exists on disk, but not in '2b9f0397…'`).
6. Isolation control: copied r53 results to scratch, removed only the `report_file` keys,
   rescanned. Scratch: `$HYAKU_SCRATCH/mori-r59/Mo59Revenger61/` (removed at end; receipts
   transcribed below).

## Findings

### F1 — The field exists in exactly one artifact, one round

- `grep -rl '"report_file"' .` (lane root) → only
  `.ufo/waves/round-53/w1-results.json`.
- Full JSON walk of 1,813 `.ufo/waves/**/*.json` files → exactly **67 objects** with a
  `report_file` key, all at `/.ufo/waves/round-53/w1-results.json` `/results[i]`.
- In that file the key appears on **67/67** member objects, at lines 16 → 478
  (first `Mo53Fr01`, last `Mo53ExecSelftestReceipts`).
- No dispatch/spec/seal artifact carries it either: r59 `w1-spec.json`, `w1-dispatch.json` and
  `build-w1-spec.py` each contain the token once, and only inside assignment prose (my own
  seat text), not as a key.

### F2 — Which rounds have a settlement artifact at all, and which carries the key

Settlement artifacts (top-level `{lane,round,wave,seats,results}` shape) and first-add commits:

```
r47/w1 68d66ca5 2026-10-25T17:06:52-03:00   canonical
r47/w2 356fb94a 2026-10-25T17:27:09-03:00   canonical
r48/w1 e4dfff32 2026-10-25T19:30:50-03:00   canonical
r48/w2 91fbbc2a 2026-10-25T20:25:44-03:00   canonical
r50/a2w1 bae8656e 2026-10-26T09:31:37-03:00  canonical
r51/w1 70e68cdd 2026-10-26T20:02:41-03:00   canonical
r52/w1 e7e056b8 2026-10-26T21:52:13-03:00   canonical
r53/w1 0df80303 2026-10-26T23:28:22-03:00   SALVAGE — report_file on all members
r53/a2r1 0b36d23e 2026-10-27T00:41:20-03:00 canonical
r54/w1 f111d4b0 2026-10-27T02:15:42-03:00   canonical
r55/w1 a27ec482 2026-10-27T03:41:17-03:00   canonical
r56/w1 eac193ca 2026-10-27T11:41:54-03:00   canonical
r57/w1 6f3f8482 2026-10-27T12:36:47-03:00   canonical
r58/w1 874cb413 2026-10-27T14:21:36-03:00   canonical
```

- Rounds 47–58 have 14 settlement artifacts; **13 are canonical**
  (`top = [lane,round,wave,seats,results]`, member keys exactly
  `{name,agent,output,note}`) and **1 (r53/w1) is the odd one**.
- Round 49 has no settlement results artifact at all
  (`ls .ufo/waves/round-49/` → `w1-*.json`, `w2/`, no `*-results.json`).
- Rounds 13–46 have no member-shaped settlement artifact; the two
  `round-23/falsify/*/bounded-results.json` files are a different per-seat falsification
  schema (no `name/agent/output` member objects).

### F3 — Appearance: one commit, whole-cloth, never removed

- `git log --diff-filter=A` → the file is added by `0df80303` (round-53 salvage; author
  `2026-10-26T23:28:22-03:00`, committer `2026-10-27T00:15:36-03:00`), and an identical
  byte-copy exists in `7c38bcf9` (reachable only as `refs/jj/keep/7c38bcf9…`; the two commits
  differ only in eight unrelated `round-40/scratch` files, `git diff --stat 7c38bcf9 0df80303`).
- File sha256 `0d644e0fb9c50101a00f47c4ef95e637bb1b1cf1168b5e49bdd19c2f0e584260`, identical at
  `7c38bcf9`, at freeze `60b3a76`, and at HEAD.
- Never removed: `git log --oneline 0df80303..HEAD -- .ufo/waves/round-53/w1-results.json` is
  empty. Per-file `-S`-style scan (`git log --all -p | grep '^+.*"report_file"'`) reports
  `134` added lines for r53/w1 = 67 keys × the two identical commits, and **0** for every other
  `*-results.json`.

### F4 — The field is co-introduced with a unique recovery header and repurposed `note`

r53/w1 top-level keys (lines 1–11):

```
lane, round, wave, seats, spawned:67, outputs_recovered:66,
settled_by:"orchestrator session exit (no seat live)", note:"The orchestrator omp session
exited at 2026-10-26T23:57:36-03:00 (SIGHUP during an operator-requested `omp update`) …"
```

- This is the only settlement artifact with any of `spawned`, `outputs_recovered`,
  `settled_by`, `note` at top level.
- `note`: r53/w1 has 67/67 non-null (per-seat provenance text, e.g. line 15
  `"note": "output recovered from the orchestrator session transcript (job Mo53Fr01-2, …)"`);
  all 13 canonical artifacts have `notes_nonnull = 0` (frozen scanner field).

### F5 — Values are derived by the writer, not copied from seat outputs

- `0/67` r53 member `output` strings contain the token `report_file`; 9 contain `report_path`;
  58 contain neither.
- Yet 66 members get `report_file = ".ufo/waves/round-53/w1/<name>.md"` (path-uniform; 0
  mismatches) and the single `null` is exactly `Mo53RevLedgerProse` (lines 187–192), the seat
  the top-level note calls dead, whose report file is absent on disk
  (`ls .ufo/waves/round-53/w1/Mo53RevLedgerProse.md` → `No such file or directory`).
- The canonical writer does **not** track reports at all: r54/55/57/58 have 1/1/2/6 report
  files missing from disk (all with non-null `output`) and no marker in the artifact.

### F6 — Frozen scan arm reproduces exactly

- Five-file arm (scratch receipt, `SETTLEMENT_SCAN_OK`, `failures: []`, rc 0):
  r54 74/74, r55 64/64, r56 64/64, r57 64/64, r58 64/64 `seats==members`,
  `notes_nonnull=0`, `empty_output=0`.
- r53/w1 arm: `SETTLEMENT_SCAN_FAIL`, rc 1, **67 failure reasons**, and the distinct reason
  set is exactly `{member[i]:extra_keys=report_file}` — no other reason kind appears.
  Tool check: `extra = set(m) - MEMBER_KEYS` at `tools/mori-settlement-scan.py:78`,
  `MEMBER_KEYS = {"name","agent","output","note"}` at line 41.
- r47w1/w2, r48w1/w2, r50a2w1, r51w1, r52w1, r53a2r1 also scan `SETTLEMENT_SCAN_OK` rc 0.

### F7 — Isolation control: `report_file` is the sole cause (and top-level drift is invisible)

- Sanitized copy in scratch with `report_file` deleted from all 67 members, four top-level
  extras retained → `SETTLEMENT_SCAN_OK`, `failures: []`, rc 0.
- So the frozen FAIL is caused **only** by the member-level key; the scanner validates required
  top-level keys but never rejects extra ones, so the r53 recovery header
  (`spawned`/`outputs_recovered`/`settled_by`/`note`) is schema drift that scans clean.

### F8 — Writer-version reading (INFERENCE, evidence-bound)

The pattern is **not** a version progression of one settlement writer; it is a one-off
recovery writer beside a stable canonical writer:

1. Single round, single artifact, single pair of identical commits (F1/F3).
2. Co-introduced with a header that literally records `settled_by: "orchestrator session exit
   (no seat live)"` — i.e. the normal settlement step never ran for that wave (F4).
3. The canonical shape resumes **73 minutes later** in the same round (`r53/w1` added
   23:28:22; `r53/a2r1` added 00:41:20) and in every later wave, with no carry-over (F2).
4. The value semantics are recovery-only (filesystem-state annotation: path for the 66 reports
   present, `null` for the one dead seat); the canonical writer never records report existence
   even when reports are missing (F5).
5. The canonical writer always leaves `note` null; the recovery writer repurposes it for
   transcript provenance (F4).
6. Round-53's own lesson records the wave record ("`w1-results.json` 67 seats, 66 outputs
   recovered; `Mo53RevLedgerProse` (reviewer) died with no output",
   `corpus/lessons/round-53.md:276`) but never mentions `report_file`; no writer script is
   committed anywhere in the lane (`grep -rln 'outputs_recovered' /home/vgpnk/Projects/shokunin/scripts
   /home/vgpnk/Projects/shokunin/mori-shokunin` → only the artifact itself). The key therefore
   marks an ad hoc separator: **canonical settlement writer vs. orchestrator salvage writer**,
   not writer v1 vs v2.

## Adversarial outcome

**No counterexample to the frozen C2 scan-arm statement.** The statement ("five r54–r58 files
scan OK with members==seats; the r53 file MUST scan FAIL (`report_file` extra keys)") reproduces
verbatim, and `report_file` is provably the sole failing cause (F6/F7). Bounded scope limits
observed, reported not fixed:

- **S1 (scanner under-detects top-level drift).** Removing only `report_file` yields
  `SETTLEMENT_SCAN_OK` while four non-canonical top-level keys remain (F7). If the contract's
  intent were "any schema drift fails", the scanner does not implement it; as written, the
  parenthetical correctly names the member-level cause.
- **S2 (text grep is not key evidence).** r58/w1 has one member whose `output` string contains
  the token `report_file`, while no r58 member has the key. A `grep`-based check would
  false-positive; only parsed-key inspection (F1) is sound.
- **S3 (writer identity is artifact-only).** No writer source for the r53 salvage is committed,
  so "writer version" can be pinned only by shape/semantics, not by code — the inference in F8
  is labelled as such.

## Confidence

High on F1–F7 (reproducible, byte/line-pinned, frozen tool sha matched). Medium on F8's
"one-off recovery writer" attribution — the artifact-shape and semantic evidence is strong, but
the producing script is uncommitted; the claim "not a version progression" rests on the field's
32-hour absence before, immediate non-carry-over after, and its co-introduction with an
explicit salvage header.

## Scratch / receipts

`$HYAKU_SCRATCH/mori-r59/Mo59Revenger61/` held only `scan-five.json` (five-file scanner output,
transcribed in F6) and `r53-sanitized.json` (isolation control, F7). Both transcribed above;
scratch directory removed before yielding. No git writes were issued; all git commands were
read-only (`show`, `log`, `diff`, `merge-base --is-ancestor`, `rev-list`). No tools installed or
updated. Disk guard checked green before work (`/fast/scratch/hyaku` 27% used, 592.6G free).
