# RevC2Interface — wave 2, round 36 (attempt 2)

Seat: reviewer. Item attacked: **C2 gate `tools/mori-sources-appendonly.py` vs its SKILL.md Round36 registry row (SKILL.md:873) and QUALITY 104 (corpus/QUALITY.md:829-836)**. Verifies entry/verdict-map/selftest claims, `--round-base` semantics, and that 104's stated check command runs as written.

## 1. Tool bytes at the scored rev

The data tip is `bf0df77fee4b6ef54a90aea09335c7617f125151` (HEAD of the lane; `git rev-parse HEAD` → `bf0df77fee4b6ef54a90aea09335c7617f125151`). Working-tree tool is byte-identical to the tool at that rev:

```
$ sha256sum tools/mori-sources-appendonly.py
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  tools/mori-sources-appendonly.py
$ git show bf0df77fee4b6ef54a90aea09335c7617f125151:tools/mori-sources-appendonly.py | sha256sum
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  -
```

So the executed byte checks below exercise the exact gate bytes pinned by the data commit.

## 2. QUALITY 104 stated check command (the pinned command)

Command as written in QUALITY 104 (corpus/QUALITY.md:832-833): `python3 tools/mori-sources-appendonly.py <tip> --round-base <entering tip>`. Executed with the concrete revs:

```
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
$ echo $?
0
```

Exit 0 with `round_changed=[]` — exactly what 104 requires. The 18 `ids` are pre-round in-place-edit debt, each discharged by a superseding row present at the tip (S201/S202/S206–S220; plus S073→S069); none changed or deleted inside `6bd57097..bf0df77`, so the round is clean. This also matches the round-35 debt narrative (spotcheck §6 item 2: 15 ids + S069; 102's own Shown-able-to-fail: 18 ids stay listed with S069/S182/S193 superseded).

Cross-check `--repo DIR` variant from a different cwd (registry entry's `[--repo DIR]`):

```
$ cd /tmp && python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --round-base 6bd57097 | tail -1
appendonly_violations=18 ids=[...] deleted=[] superseded=[...] round_changed=[]
$ echo $?
0
```

Identical result; the `--repo` switch behaves as registered.

## 3. Registry row vs actual behavior (SKILL.md:873)

Registry row: kind `gate`; entry `python3 tools/mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P]`; verdict map "with `--round-base`: 0 `round_changed=[]` · 1 non-empty; without: 0 no `ids` and no `deleted` · 1 otherwise; 2 git or parse error"; self-test "8 sandbox histories through the CLI".

Probes:

```
# without --round-base: ids non-empty -> exit 1 (and round_changed printed [] per contract)
$ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 > /dev/null; echo $?
1

# error paths -> exit 2
$ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --path NOPE; echo $?
error: NOPE is absent at bf0df77fee4b6ef54a90aea09335c7617f125151
2
$ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --repo /tmp/nope-xyz; echo $?
error: git rev-parse --verify bf0df77fee4b6ef54a90aea09335c7617f125151^{commit} failed: fatal: cannot change to '/tmp/nope-xyz': No such file or directory
2
```

Verdict map matches source exactly (main: `return 1 if result["round_changed"] else 0` with `--round-base`; else `return 1 if (result["ids"] or result["deleted"]) else 0`; `GateError` → 2).

Self-test claim — 8 sandbox histories driven through the CLI:

```
$ python3 tools/mori-sources-appendonly.py --selftest
MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0
$ echo $?
0
```

Exit 0, 8/8 pass. Matches the registry's "8 sandbox histories through the CLI" and 104's "`--selftest` exits 0". Selftest cases cover the four lists, round_changed changed-back semantics ("changed-back inside the round" expects `round_changed=[S001]` with `ids=[]` — the "changed back inside the range is listed" rule), deletion output (`deleted=[S002]`, exit 1 — 104's Shown-able-to-fail), and supersedes disposition (`superseded_by=`).

## 4. `--round-base` semantics (contract .ufo/waves/round-36/contract.md:73-77)

Implementation: `round_changed` = ids whose immutable cells changed or which were deleted in any commit in `REV..<rev>` that touches the path, including change-back in range (changed_at from consecutive path states; deleted_at from row disappearance; intersect with `git log base..rev`). Verified in code (analyze, lines 190-267) and by the live run: range `6bd57097..bf0df77` contains exactly the data commit touching `corpus/SOURCES.md` (`git log --oneline 6bd57097..bf0df77 -- corpus/SOURCES.md` → only `bf0df77 round-36: ... SOURCES S205-S220 ...`), and the gate reports `round_changed=[]` — no id edited or deleted in-round.

## 5. QUALITY 104's cross-references

- Lesson cite `corpus/lessons/round-35-verifier-spotcheck.md` §6 items 2-3: item 2 is the SOURCES append-only debt (15 ids + S069; "Not covered: deleted rows" gap) and item 3 is the gate registry requirement (round-35 script had no registry row, no self-test). Both are closed by the registered gate with deletion detection and a fixture self-test — consistent with 104's text.
- Shown-able-to-fail cite `evidence/c0-rescore-v2.txt` J2 and J5: both rows exist and score `C2=unmet` (J2: round-35 script substituted, 0/24 blind match; J5: no-deletion variant, lists differ on `deleted`). Consistent.

## 6. Findings

No divergence found in scope. Registry entry, verdict map, self-test claim, `--round-base` semantics, and 104's stated check command all verified against the actual tool bytes at the scored rev. Residual risk / verification gaps (non-blocking, not defect findings):

- The self-test does not cover a mid-history path absence/rename (the `states.append(None)` branch); deletion attribution would shift to the next non-None state. Irrelevant to this round's history (path present throughout) and not part of the frozen interface claims.
- The gate's `--path` option and `--repo` default (cwd) are as registered; the 104 command presupposes the lane root cwd.

No tools installed; no lane files modified.

## VERDICT: PASS — no defect found for C2 tool vs its SKILL.md registry row and QUALITY 104.
