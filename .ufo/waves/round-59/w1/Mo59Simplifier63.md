# Mo59Simplifier63 — review of `tools/mori-register-check.py` + `tools/mori-settlement-scan.py`

Round 59, wave `w1`, seat `Mo59Simplifier63` (simplifier, leaf — no subagent dispatch).
Read-only review. No production, counter, fixture, corpus, SCORECARD, LOG or VCS edits.
Scratch: `/fast/scratch/hyaku/mori-r59/Mo59Simplifier63` (removed after this report was written).

- Freeze: `60b3a76ad0524c8978cc51922940be1c8c388915`; entering: `2b9f03975bfb6e508f35074ac8181ec8bf54e805`; lane HEAD at review: `8ff344ff`.
- Disk guard at start: `use 27%, free 592.6G` — green.
- Frozen-byte check (`git diff 60b3a76..HEAD` over contract + both counters + both tools): **empty**; per-file sha256 SAME for all five. Kill rule intact.

## Verdict

Both tools match their frozen pins exactly:

```
38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8  tools/mori-register-check.py
4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  tools/mori-settlement-scan.py
```

**No dead code.** `pyflakes 4.0.3` and `vulture 2.16` (min-confidence 0) both report zero findings on either tool. Dead/false-positive surface is behavioural, not lexical (§Adversarial).

**Critical constraint on every recommendation below:** both tools are sha-pinned by `PIN` in their counters, so *any* edit — including the cosmetic ones — flips C1 to `tool_sha` / C2 to `pin`. These are **round-60 candidates**, not round-59 actions.

## Method (bounded)

1. Static: `pyflakes 4.0.3`, `vulture 2.16 --min-confidence 0` on both tools.
2. Differential probes through the public CLI only, fixture roots built under scratch: vacuous requirement set, name-boundary classes, short/empty evidence rows, non-existent/directory targets, unknown and value-less flags, zero-member and bool-typed JSON fields.
3. Receipts reproduced: both selftests (`REGCHECK_SELFTEST pass=12 fail=0`, `SETSCAN_SELFTEST pass=10 fail=0`), all 13 `fixtures-c1` and 12 `trees-c2` expect tokens cross-read, and both frozen counters at the freeze revision.

Counter receipts at freeze revision (read-only, `--scratch` under seat dir):

```
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915      exit 0
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0  exit 1
   failed=copy_absent:.../w1-results-r54..r58.json, copy_absent:.../w1-settlement-r58.json, entry_absent, tree
```

C2 `unmet` at freeze is the intended pre-data control (entry, copies and rows land after the wave), not a defect. The r53 drift arm does fire for the frozen reason: `SETTLEMENT_SCAN_FAIL` with `member[0..66]:extra_keys=report_file` (`report_file` is member-level, not top-level — contract wording holds).

## Simplification candidates (safe; no behaviour change; round-60 only)

| # | Site | Weight | Why safe |
|---|---|---|---|
| S1 | `mori-register-check.py:93` `if not tok or not tok.strip()` | dead clause | `not tok.strip()` is already true for every `tok` where `not tok` holds; `""`/whitespace/`None`-like all short-circuit on the second test. Collapses to `if not tok.strip():`. |
| S2 | `mori-register-check.py:152` `m = KEY_CELL.match(cells[0])` | redundant re-match | `keymap` is populated only from rows where `KEY_CELL.match` succeeded (line 123), so `m` at 152 cannot be `None`. Carry `(ri, cai)` out of the line-123 loop instead of re-parsing and relying on an impossible branch. |
| S3 | `mori-register-check.py:161` `"manifest:lane=%r"` | unclear text + inconsistency | Every sibling reason appends the required key (`manifest:index_missing=%s`, `manifest:entry_missing=%s`, `manifest:lane_round=%s`); this one does not. With the counter's two requires a foreign lane emits two byte-identical reasons (observed: `["manifest:lane='kotoba'", "manifest:lane='kotoba'"]`), so the failing row is unidentifiable. Append ` % want`; the frozen expect `f10` token is `manifest:lane`, matched by `startswith`, so the prefix survives. |
| S4 | `mori-register-check.py:182` `"pointers:bad=%s" % p` | unclear text | An empty backtick cell (``` `` ```) yields `p == ""` → the reason renders as `pointers:bad=` with no payload, indistinguishable from a malformed path. Observed verbatim: `'pointers:bad='`. Split the empty case into `pointers:empty=%s`; still covered by frozen expect `f13` token `pointers`. |
| S5 | `mori-settlement-scan.py:152` `import io, contextlib` | repeated import | Inside `case()`, re-executed for all 9 selftest cases; hoist to module scope. |
| S6 | `mori-settlement-scan.py:122,126` | duplicated expression | `"SETTLEMENT_SCAN_OK" if (files and not failures)` and `return 0 if (files and not failures)` compute the same predicate twice; bind `ok = files and not failures` once. |

## Adversarial findings

### A1 (major, register-check) — vacuous verification surface: zero `--require` prints `REGISTER_MET`

`--require` is `action="append", default=[]` (`:293`) with no minimum. The require loop is the *only* consumer of keys, names, manifest and pointers, so an empty require list verifies nothing and still succeeds:

```
$ python3 tools/mori-register-check.py --scorecard scorecard.md --manifest manifest.json --root _root
{"bound": {}, "pointers": [], "reasons": [], "schema": "mori-register-check-v1", "verdict": "REGISTER_MET"}
rc=0
```

The register in that probe has one valid row and the run reports `bound: {}`, `pointers: []`. The tool's own anti-vacuity instinct is present per-row (`pointers:none=%s` at `:179` fails a required row with no evidence pointer) but is not applied to the requirement set. Fix shape: reject an empty effective require list as a setup fault (exit 2) or emit `REGISTER_UNMET` with `require:none`.

**Not scoring-relevant:** `count-c1.py` always passes both `REQUIRE` tokens and additionally asserts `sorted(bmap) == sorted(BOUND)`, so C1's met-proof cannot be reached through the empty set.

### A2 (major, settlement-scan) — zero-seat settlement scans OK

`seats` is only compared to `len(results)` (`:61-62`), so `0 == 0` passes:

```
{"lane":"mori","round":59,"wave":"w1","seats":0,"results":[]}
→ rc=0 SETTLEMENT_SCAN_OK members=[0] failures=0
```

The tool already refuses file-level vacuity — "nothing scanned is not a scan", zero arguments → exit 1 — but not member-level vacuity. Same principle, applied one level down. A settlement artifact that settles no seats should not carry the OK verdict.

**Not scoring-relevant:** the five real r54–r58 artifacts carry 67–74 members each.

### A3 (minor, settlement-scan) — `bool` satisfies the `int` schema fields

Python treats `bool` as an `int` subclass, so `isinstance(seats, int)` (`:62`) and `isinstance(d.get("round"), int)` (`:67`) accept JSON `true`:

```
{"round": true,  "seats": 1, results:[...] }  → rc=0 SETTLEMENT_SCAN_OK
{"round": 59, "seats": true, results:[...] }  → rc=0 SETTLEMENT_SCAN_OK   (True == 1)
```

`round_bad` is unreachable for `true`, and `seats: true` binds against a one-member wave by accident of `True == 1`. `type(x) is int` or an explicit `not isinstance(x, bool)` guard closes both.

### A4 (unclear text, both tools) — `--scratch` with no value silently falls back to a temp dir

`mori-settlement-scan.py:196-197` and the identical block in `mori-register-check.py:285-286` both compute `scratch = argv[i+1] if 0 <= i < len(argv)-1 else None` and then fall through to `tempfile.mkdtemp`. Observed: `--selftest --scratch` (value omitted) ran green and created `/fast/scratch/.../mori-settlement-scan-zhl759zq` with no diagnostic at all. The round contract requires an explicit scratch path on every counter; a tool that silently substitutes one contradicts that requirement. A value-less `--scratch` should exit 2.

### A5 (unclear text, settlement-scan only) — unknown `--flag` is silently dropped and its value becomes a scan target

`args = [a for a in argv if not a.startswith("--")]` (`:199`) discards the flag but keeps its argument. Observed with a one-character typo:

```
python3 tools/mori-settlement-scan.py --scrath /path/whatever <real r54 results file>
→ failures: [{"path": "/path/whatever", "reasons": ["unreadable"]}]
```

The run scans the stray path, reports `unreadable` against a directory nobody meant to scan, and stays mixed-in with the real file. `register-check.py` does not share this defect (it uses `argparse` on the non-selftest path). Use `argparse` here too, or reject unknown `--` tokens.

### A6 (doc/code drift, register-check) — the name boundary is wider than the docstring promises

Docstring (`:17-19`): "`name` == string, or string starts with `name (` or `name,` — a bare substring hit does NOT bind". The code (`:169-172`) accepts **any** non-alphanumeric, non-underscore character after the name. Probes, all `REGISTER_MET`:

| manifest entry (name = `alpha bind`) | docstring | actual |
|---|---|---|
| `alpha bind (does a)` | binds | binds |
| `alpha bind, does a` | binds | binds |
| `alpha bind-zzz` | no | **binds** |
| `alpha bind: zzz` | no | **binds** |
| `alpha bind/zzz` | no | **binds** |
| `alpha bindZ` | no | correctly rejected |
| `alpha bind_zzz` | no | correctly rejected |

The frozen substring fixture (`f09`, entry `xxalpha bind`) still fails correctly, so the hostile arm is intact; the exposure is a manifest entry that shares a name prefix with a different capability. Either narrow the code to `(" (", ",")` or widen the docstring sentence; today the docstring overstates the guarantee.

## Candidates rejected (deleting them harms an axis)

- `empties += 1` at `mori-settlement-scan.py:94` and `:98` looks like a double-count but is **not** redundant: the `isinstance(..., str)` guard at `:96` sits between the two; merging them would reorder the `output_bad` classification. Kept.
- `register_table()`'s third return value `n_caps` (`:66,101,117`) is used only in the `binding:` reason, but that reason is the only text explaining *why* a stub or a double-declared register failed. Kept.
- `summary` emission for a file that also appears in `failures` (`:108,118-120`) is deliberate: `files` is the census, `failures` the verdict. Deleting it would lose the per-artifact counts the C2 `scan` arm reads.
- Top-level extra keys are not rejected while member keys are. That asymmetry is in scope of the frozen contract ("member key-set"), not weight to delete; changing it would reject r53/r54's `spawned`/`settled_by` fields and break the `scan=ok` arm.

## Frozen-counter observations (recorded, not actionable — kill rule)

`pyflakes` on the frozen counters reports three unused locals in `count-c1.py`: `got` (`:155`, the normalised-reason set built beside the `startswith` match and then discarded), `spec` (`:216`) and `here` (`:218`) in `selftest()`. None affect the emitted line. They are frozen bytes; any edit invalidates C1. Recorded only so a future round does not rediscover them.

## Preserved contract

- C1 claim unaffected: tool sha equals `PIN`; all 13 `fixtures-c1` expect prefixes still match their emitted reasons; `C1=met` at `60b3a76` reproduced.
- C2 claim unaffected: tool sha equals `PIN`; `SETSCAN_SELFTEST pass=10 fail=0`; r54–r58 scan OK and r53 fails on `report_file`, so `drift=ok` is real, not a docstring artefact.
- `C2=unmet` at the freeze revision is the frozen do-nothing control, not a regression.

## Tradeoff

A1 and A2 are the only findings with a real failure mode, and both need **more** code (one guard each), not less — they are correctly categorised as hardening a future round, not as simplifications. The literal weight that can be removed without semantic loss is S1–S6: one dead clause, one impossible branch, one duplicate predicate, one duplicate import, and two failure strings that say less than their neighbours. Every one of them is blocked in round 59 by the sha pin on both tools.

## Tools installed (channel, version, reason)

| Tool | Version | Channel | Reason |
|---|---|---|---|
| pyflakes | 4.0.3 (Python 3.15.0) | `uv pip install` into seat-local venv at `$HYAKU_SCRATCH/mori-r59/Mo59Simplifier63/.venv` | dead-code/unused-local evidence |
| vulture | 2.16 | same | dead-code evidence |

No pacman transaction run (host-wide pause). Nothing written to any PATH directory; both tools live only in the seat scratch venv, which was removed with the scratch root.
