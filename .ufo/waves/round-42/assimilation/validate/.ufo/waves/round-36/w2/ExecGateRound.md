# ExecGateRound — round landing gate checks (mori, round 36, wave 2)

Seat: `ExecGateRound` (executor). L1: MoriR36. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`
(read-only for this seat; jj-colocated, git backend). No lane file was edited; the only file written is
this report. No `git add/commit/push/fetch/reset`, no mutating `jj` command, no pacman, no installs
(nothing to record). Scratch only under `/fast/scratch/hyaku/mori-r36/ExecGateRound/`.

## 1. What this item attacks

The **round landing gate** of the round-36 data commit: the two invocations of the registered gate
`tools/mori-sources-appendonly.py` at landed tip `bf0df77` (round base `6bd57097`), the identity of the
`ids` list it prints, and the per-id `supersedes S###` disposition coverage at the tip. It also executes
the **verification recipe the assignment prescribed** for those checks (two of whose premises turn out to
be false, §6) and audits the routed round-35 append-only debt the same 18 ids carry (§7).

## 2. Gate run A — with `--round-base` (expect `round_changed=[]`, exit 0)

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097
changed S041 superseded_by=S206
changed S044 superseded_by=S207
changed S051 superseded_by=S208
changed S062 superseded_by=S209
changed S064 superseded_by=S210
changed S069 superseded_by=S073
changed S179 superseded_by=S211
changed S180 superseded_by=S212
changed S181 superseded_by=S213
changed S182 superseded_by=S201
changed S183 superseded_by=S214
changed S184 superseded_by=S215
changed S185 superseded_by=S216
changed S186 superseded_by=S217
changed S188 superseded_by=S218
changed S189 superseded_by=S219
changed S190 superseded_by=S220
changed S193 superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
EXIT=0
```

Matches the expectation exactly. Round range `6bd57097..bf0df77` holds five commits
(`c081375`, `da12b37`, `c1a026c`, `5842dc0`, `bf0df77`) and only `bf0df77` touches
`corpus/SOURCES.md`; that commit is `16 0` insertions/deletions on the path
(`git diff --numstat 6bd57097..bf0df77 -- corpus/SOURCES.md` → `16	0`), a pure append. So
`round_changed=[]` is the honest verdict.

## 3. Gate run B — without `--round-base` (expect 18 ids, exit 1)

```
$ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151
… (the same 18 `changed` lines as run A) …
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
EXIT=1
```

Matches the expectation: 18 ids, exit 1.

## 4. The `ids` list is right, verified three independent ways

`ids` is exactly the 18 ids above. Cross-checks:

- **The frozen counter's own oracle agrees byte-for-byte.** `UFO/waves/round-36/evidence/c2-after.txt:6`
  carries `oracle: appendonly_violations=18 ids=[S041,…,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]`,
  and the receipt's tool line above it is identical. (That receipt's real arm runs at rev `6bd57097`,
  round base `f10a320d`, per P-C2; re-running the gate with those arguments reproduces it exactly:
  `python3 tools/mori-sources-appendonly.py 6bd57097 --round-base f10a320d` → `superseded=[S069,S182,S193]`,
  `round_changed=[S182,S193]`, `EXIT=1`.)
- **My own re-implementation from the contract definitions reproduces it.** Scratch script
  `oracle_full.py` (no import of gate code) re-walks the path history, applies the 11-cell/8-immutable-cell
  rule and prints all four lists. At `bf0df77` it returns the same 18 ids, `deleted=[]`, all 18 superseded,
  `round_changed=[]`.
- **Merge simplification does not hide anything.** The same oracle run with `--full-history` (49 commits
  instead of 48) returns the identical 18 ids and identical lists (`oracle_merges.py`: `flags=[] commits=48`
  and `flags=['--full-history'] commits=49` both give `ids=18 … round_changed=[]`).

The gate's exit-code contract also holds where it is documented to: bad revision → exit 2
(`git rev-parse --verify` failure), absent path → exit 2, `--selftest` → `pass=8 fail=0`, exit 0.
The companion index gate is live-clean: `bash tools/mori-index-clean.sh <lane>` →
`MORI_INDEX_CLEAN staged=0 intent_to_add=0`, exit 0 (self-test `pass=4 fail=0`).

## 5. Per-id disposition coverage — 18/18, exactly one each

Parsing the tip's registry by header position and testing the `teaches` cell with the gate's own anchor
rule (`^supersedes\s+(S\d{3})\b`) gives **34 registry rows whose teaches opens `supersedes S###`**
(34 distinct targets), and for each of the 18 carried ids exactly one:

| id | superseder | location |
|---|---|---|
| S041 | S206 | corpus/SOURCES.md:212 |
| S044 | S207 | corpus/SOURCES.md:213 |
| S051 | S208 | corpus/SOURCES.md:214 |
| S062 | S209 | corpus/SOURCES.md:215 |
| S064 | S210 | corpus/SOURCES.md:216 |
| S069 | S073 | corpus/SOURCES.md:79 |
| S179 | S211 | corpus/SOURCES.md:217 |
| S180 | S212 | corpus/SOURCES.md:218 |
| S181 | S213 | corpus/SOURCES.md:219 |
| S182 | S201 | corpus/SOURCES.md:207 |
| S183 | S214 | corpus/SOURCES.md:220 |
| S184 | S215 | corpus/SOURCES.md:221 |
| S185 | S216 | corpus/SOURCES.md:222 |
| S186 | S217 | corpus/SOURCES.md:223 |
| S188 | S218 | corpus/SOURCES.md:224 |
| S189 | S219 | corpus/SOURCES.md:225 |
| S190 | S220 | corpus/SOURCES.md:226 |
| S193 | S202 | corpus/SOURCES.md:208 |

Every mapping above is exactly the `superseded_by=` value the gate printed in §2. No id lacks a
disposition; no id has two.

## 6. DEFECT — the prescribed verification recipe is false in two places

The assignment's own check text, `.ufo/waves/round-36/gen-w2-spec.py:94-98`, says:

> Verify the ids list equals **the 18 ids QUALITY 104 names** and that every id has a `supersedes S0NN`
> row at the tip (**`grep -c 'supersedes S0' corpus/SOURCES.md`** and the exact list).

Both halves are wrong as instruments.

**6a. QUALITY 104 names no ids.** `corpus/QUALITY.md:829-836` is criterion 104 in full; extracting every
`S###` token from those eight lines yields **nothing** (`sed -n '829,836p' corpus/QUALITY.md | grep -oE 'S[0-9]{3}'` → empty).
Criterion 104 is about *which command runs the check* and *deleted-row coverage*, not about an id list.
The only place in `corpus/QUALITY.md` that carries the count is line **809** (criterion 102:
`while 18 ids stay listed (S069, S182 and S193 superseded; 15 not)`) — and that sentence is scoped to
round 35's tip and names only 3 of the 18. The enumerated 18-id list lives in the receipt
(`.ufo/waves/round-36/evidence/c2-after.txt:6`) and in the gate's own output.

**6b. `grep -c 'supersedes S0' corpus/SOURCES.md` = 17, and the pattern cannot verify the claim.**
Measured:

```
$ grep -c 'supersedes S0' corpus/SOURCES.md
17
```

The number is 17, not 18, and its composition is not the disposition set:

- only **6 of the 17** lines target one of the 18 carried ids (line 79 → S069, 212–216 → S041/S044/S051/S062/S064);
- **9** target ids outside the 18 (lines 80,81,82,93,94,149,150,151,152 → S071,S070,S067,S083,S084,S090,S093,S096,S097);
- **1** is not a superseder row at all: `corpus/SOURCES.md:211` is the **S205** row, whose `teaches` cell
  *quotes the fleet rule template* — "corrections are new rows whose teaches opens supersedes S0NN —." —
  so it matches the substring without being a disposition;
- **1** is prose: `corpus/SOURCES.md:261`, in the search-log block, mentions "S073 supersedes S069 …".

And structurally it cannot reach the other 12 ids: **12 of the 18 are S1xx** (S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193)
and their disposition rows read `supersedes S179 —` etc., which the literal `supersedes S0` never matches.
An executor running the prescribed command and comparing to 18 would report a false mismatch on a
correct round.

Correct instruments, measured on the same bytes:

```
$ grep -cE 'supersedes S[0-9]{3}' corpus/SOURCES.md
35
$ grep -oE 'supersedes S[0-9]{3}' corpus/SOURCES.md | wc -l
37
```

and the semantically right check is the teaches-cell parse in §5 (34 rows whose teaches *opens* the
token; 37 occurrences includes line 261's three prose mentions). The gate itself is not fooled by the
S205 template or by line 261 — its anchor `^supersedes\s+(S\d{3})\b` applied to the `teaches` cell keeps
S205 out (its teaches opens "Rule 2 limits …") and never sees prose.

The defect is confined to the wave-2 spec generator (line 98 is the only `grep -c 'supersedes S0'`
prescription in it; no lane criterion, `SKILL.md`, or lesson instructs that pattern —
`grep -rn "supersedes S0'" SKILL.md corpus/` → empty). `gen-w2-spec.py` is tracked in the lane
(`git ls-files` → present) and clean in the worktree, so the false recipe is in the landed round bytes
that generated the wave-2 prompts.

## 7. FINDING — routed round-35 debt item for S069 is not disposed (gate cannot see it)

The routed repair this round carried, `corpus/lessons/round-35-verifier-spotcheck.md:172-173`, reads:

> **SOURCES append-only debt.** 15 ids changed in place before round 34, not superseded
> (`w2/ScoutAppendDebt.md`), plus S069. Land a **supersede row for each, or a named ruling**.

Round 36 landed `S205–S220` = 16 rows, of which S205 is the corpus-contract row and `S206–S220` are
**15** supersede rows covering exactly the 15 previously-unsuperseded ids (S041,S044,S051,S062,S064,S179,S180,S181,S183,S184,S185,S186,S188,S189,S190).
**Nothing was landed for S069** — no new supersede row and, as far as I can measure, no named ruling.

Evidence:

```
$ git log --oneline --reverse -G 'supersedes S069' -- corpus/SOURCES.md
71abd41 round-20: wave-2 falsification integrated (R7/R8 refinements, vocab guard, register 26/19/5, S073-S076 corrections), …
$ git log -1 --format='%h %ad' 71abd41   ->  Wed Oct 21 08:18:17 2026 -0300
$ git log -1 --format='%h %ad' 62db24c   ->  Thu Oct 22 23:55:24 2026 -0300   (S069's in-place teaches edit)
$ git merge-base --is-ancestor 71abd41 62db24c && echo YES   ->  YES
$ grep -c 'S069' corpus/lessons/round-36.md
0
```

So S069's only disposition row (S073) landed **~40 hours before** the round-33 in-place edit it would have
to dispose of, and it is an ancestor of that edit. QUALITY 102's rule is "**A later row** whose teaches
opens `supersedes S###` is the correction's disposition" (`corpus/QUALITY.md:801`); a row that predates
the change is not a later row. The round-36 lesson (the lane's durable record) does not mention S069 at
all, so no named ruling landed there either. Related seat reports reached "PASS" on this debt
(`w2/RevAppendDebt.md:69,97,101`) by counting presence of a superseder row without checking its ordering
against the change it disposes.

Why the gate cannot flag it: the frozen tool reports `superseded` as "ids in `ids` for which a row present
at `<rev>` has a teaches cell opening `supersedes S###`" (contract §C2; `tools/mori-sources-appendonly.py:243-244`).
Presence at the tip is the whole test, so S069 is reported `superseded_by=S073` and the output reads as if
the item were closed. This is a semantic gap in the gate's *contract*, not a bug in the gate: the tool
matches its frozen definition, the counter's oracle agrees, the exit codes are right, and the 18 ids stay
listed (a superseder is a disposition, not a discharge — `SKILL.md:866`, QUALITY 102). I did not attempt
remediation (mori province: detection and report only), and the lane is read-only for me.

## 8. Drift note — the lane moved during measurement

Mid-session the lane advanced from `bf0df77` through `9ca8f2e`, `6827d6e`, `8ff9bba`, `5a2fe05`,
`4890c2d`, `6b68b2e`, `3c2fe8c` to `842a320` (round 36 closed; round 37 begun). Every measurement above is
at the assigned tip `bf0df77`. For completeness, at `HEAD 842a320` the gate still prints the identical 18
ids and `round_changed=[]` (exit 0 with `--round-base 6bd57097`, exit 1 without); the post-tip
`corpus/SOURCES.md` edits are **`used-by` only** on 13 rows (S205–S209, S212–S219), i.e. the mutable
column — cell-level diff: every changed row lists `changed cols: ['used-by'] IMMUTABLE CHANGED: no` — so
append-only still holds at the later tip. The frozen counter bytes are untouched across the range
(`git diff --stat bf0df77..HEAD -- .ufo/waves/round-36/count-c2.py` empty; sha256
`c7edaacf…ac34` still equals the `evidence/freeze-v2.txt` pin), and the gate tool at the tip is
byte-identical to the worktree copy (sha256 `915527a7…fc89`).

## 9. Residual risk and verification gaps

- The gate's `superseded` field is presence-based and cannot express "the disposition predates the
  change" (§7). Any future claim that the 18-id debt is *closed* rests on a reading the gate cannot
  confirm.
- `c1-after.txt` / `c2-after.txt` were untracked at `bf0df77` and were committed later (`9ca8f2e`); the
  assigned tip carried the gate and the ids but not those receipts. Not a gate defect — recorded so the
  landed-tip evidence set is not over-read.
- My independent oracle is a second implementation of the same contract sentence, so it is not fully
  independent on *interpretation* — only on implementation. The `--full-history` cross-check was run
  specifically to catch merge-simplification blind spots; it found none for this history.
- No LSP device was available or needed (no code refactor); all findings rest on direct file reads and
  read-only gate runs.
- No tool installs or upgrades were performed.

## 10. Artefacts

`/fast/scratch/hyaku/mori-r36/ExecGateRound/` — `oracle_ids.py` (endpoint-comparison oracle),
`oracle_full.py` (all four lists), `oracle_merges.py` (`--full-history` cross-check), `check_sup.py`
(per-id teaches-cell parse), `ids_seq.py` (id-sequence census: 220 rows, 220 unique, S001–S220, no gap),
`p_frozen.txt` / `p_tip.txt` (predicate-sentence diff: byte-identical, 739 B each), plus the sandbox
repos `delsandbox/` (deleted-row arm: `deleted=[S002]`, exit 1) and `idxdirty/`, `idxdirty2/`
(index-clean negative arms: `intent_to_add=1` exit 1; `staged=1` exit 1). Lane repo: only this report
was added.

VERDICT: FAIL — the gate itself and the tip's append-only state are sound (both invocations as expected;
18 ids matching the counter oracle; 18/18 one disposition each), but (i) the assigned recipe is false twice
on landed bytes: "QUALITY 104 names" the 18 ids `.ufo/waves/round-36/gen-w2-spec.py:97` when criterion 104
(`corpus/QUALITY.md:829-836`) names none, and ``grep -c 'supersedes S0' corpus/SOURCES.md``
(`.ufo/waves/round-36/gen-w2-spec.py:98`) returns **17**, cannot match the 12 S1xx ids, and includes two
non-superseder lines (`corpus/SOURCES.md:211` rule-template quote in S205's teaches;
`corpus/SOURCES.md:261` prose); and (ii) the routed round-35 debt item "plus S069 — land a supersede row
for each, or a named ruling" (`corpus/lessons/round-35-verifier-spotcheck.md:172-173`) is undisposed at the
tip: S069's only superseder S073 (`corpus/SOURCES.md:79`) landed `71abd41` 2026-10-21 08:18, an ancestor of
S069's in-place edit `62db24c` 2026-10-22 23:55, and `corpus/lessons/round-36.md` mentions S069 zero times,
so no named ruling landed either.

Report: .ufo/waves/round-36/w2/ExecGateRound.md
