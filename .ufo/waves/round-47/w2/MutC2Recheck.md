# MutC2Recheck — wave-2 re-run of wave-1 M5 (count-c2 used-by survivor) + killer arm

Lane: mori-shokunin, round 47, wave w2. Leaf seat, scratch-only mutations. No tooling installed (no pacman, no uv, no downloads). Tip T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63`; tracked `.ufo/waves/round-47/count-c2.py` was clean at start (`git status --porcelain` empty for the file) and its sha256 equals wave-1's baseline.

Scratch root: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-MutC2Recheck/` (all commands below ran with `TMPDIR=` that dir).

## Target of attack

The S475 used-by conjunct in `evaluate()` of `.ufo/waves/round-47/count-c2.py` (lines 161–166):

```python
    if cells and len(cells) == 11:
        kind, tier, status, used = cells[2], cells[3], cells[7], cells[10]
        if (kind == "code" and tier == "A" and status == "mined"
                and "v7.2" in cells[1] and "include/trace/events/oom.h" in cells[1]
                and ENTRY in [u.strip() for u in re.split(r"[,;]", used)]):
            srow = "ok"
```

Mutation M5 (wave-1 mutant (b), `w1/MutC2Source.md`): delete the used-by conjunct, i.e. the `and ENTRY in [u.strip() for u in re.split(r"[,;]", used)]` line, leaving `... in cells[1]):`. This is the smallest behavior-bearing point for the "whose used-by names the entry" clause of frozen predicate P-C2.

## Baseline (pristine detector)

Command: `TMPDIR=$S python3 $S/pristine.py --selftest` (pristine.py = exact `cp` of the tracked file).

- pristine.py sha256 `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e` — identical to the tracked bytes at T and to wave-1's recorded pristine hash.
- Output tail: `C2_SELFTEST pass=13 fail=0`; exit code 0. Matches wave-1's baseline exactly.

## Survivor M5 re-run

Command: `TMPDIR=$S python3 $S/mutant_m5.py --selftest` (mutant_m5.py = pristine copy with the used-by conjunct removed via edit on the scratch path only).

- mutant_m5.py sha256 `cc9503af56e4023ce0b09d25d5a3366403b2f197408c71bc12a9bc99e2e874e0`.
- Output tail: `C2_SELFTEST pass=13 fail=0`; exit code 0. All 12 fixture arms plus `cli_not_a_repo_rc2` PASS; no arm fails.

Verdict on the re-run: **survivor reproduced** — the wave-1 finding holds. The selftest does not detect removal of the used-by check.

Why it survives: the only two `source_row` arms are `no_source_row` (SOURCES.md has no S475 row at all — `cells` is None) and `source_row_queued` (status cell `queued` — the `status == "mined"` term fails). No arm leaves a well-formed `code`/`A`/`mined`/v7.2/oom.h row whose used-by cell names a different entry, so the `ENTRY in [...]` term is the only predicate term with zero coverage.

Note: wave-1 recorded mutant sha `0844ebbd6c11881bc16ba8b2998d031e8290f140dcc6467b703e3f5eaa963e51`; my removal is semantically the same deletion but not byte-identical to wave-1's edit (their exact removal form is not recorded). The survivor behavior is identical: selftest 13/13, exit 0. [INFERENCE: wave-1's differing hash comes from a cosmetically different deletion, e.g. keeping the line and emptying the clause.]

## Killer arm (minimal selftest case that kills M5)

One arm appended to `cases` in the selftest, immediately after `source_row_queued` and before `fails = 0` — an otherwise honest tree whose S475 row is perfect except the used-by cell names a different entry:

```python
    f, p = fake_tree([A, B]); f["corpus/SOURCES.md"] = f["corpus/SOURCES.md"].replace(ENTRY, "corpus/knowledge/unrelated-r47.md")
    cases.append(("used_by_not_entry", f, p, False, "source_row"))
```

Two armed scratch copies were built (identical arm, one on pristine code, one on the mutant):

- `pristine_killer.py` sha256 `0aa598d57542fffd835fe1f2c1ad1486e7ec72ad1940462cad883ae1345b6c47`
- `mutant_killer.py` sha256 `a6eb28f1da0eafe93473c8ed998f08ba9158810f43296f9fb3069387805bfe44`

Observed outputs (same `--selftest` command, tail lines):

- pristine_killer: `PASS used_by_not_entry  C2=unmet events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=bad provenance=ok rev=fixture failed=source_row` then `C2_SELFTEST pass=14 fail=0`; exit 0. The arm is a valid detector: the real predicate flags the defect.
- mutant_killer: `FAIL used_by_not_entry  C2=met events=2 rows=2 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=fixture` then `C2_SELFTEST pass=13 fail=1`; exit 1. **The arm kills M5.**

## End-to-end confirmation at CLI level (real git_reader path)

Fixture repo `$S/fixture` (commit `ea0c277d1489d9a7bbad6a407c9d37413d77958a`): tree extracted from T via `git -C <lane> show T:<path>` for exactly the six files the counter reads (`corpus/knowledge/oom-tracepoints-r47.md`, `corpus/SOURCES.md`, `corpus/evidence/sources-r47/{include_trace_events_oom.h,mm_oom_kill.c,mm_page_alloc.c,fs_proc_base.c}`), then one cell of the S475 row rewritten: used-by `corpus/knowledge/oom-tracepoints-r47.md` → `corpus/knowledge/unrelated-r47.md`. `git -C "$D" rev-parse --show-toplevel` verified equal to `$D` before the commit; all git calls used `-C "$D"`; the lane repo was only read.

- `TMPDIR=$S python3 $S/pristine.py HEAD --repo $S/fixture` → `C2=unmet events=8 rows=8 … source_row=bad … failed=source_row`, exit 1.
- `TMPDIR=$S python3 $S/mutant_m5.py HEAD --repo $S/fixture` → `C2=met events=8 rows=8 … source_row=ok provenance=ok`, exit 0 — a full false green through the CLI path.
- Both lines show `pin_mismatch=0`: the pinned blobs are byte-identical to T, so the fixture's only defect is the used-by cell.

Control: `TMPDIR=$S python3 $S/pristine.py 68d66ca53d89be5c34a62f46af7c37449d9f9b63 --repo <lane>` (read-only) → `C2=met … provenance=ok`, exit 0 — matches claim C2 and proves the fixture differs from T only in the rewritten cell.

## Verdict

**Breaks (coverage finding, reproduced):** removing the used-by check from `count-c2.py` is invisible to the counter's own selftest (survivor M5, wave-1 mutant (b)). The predicate code itself is correct — the pristine counter rejects a wrong used-by (`failed=source_row`) — but nothing in the selftest exercises that term. The minimal killer arm `used_by_not_entry` (above) kills the mutant: pristine passes it as `unmet/failed=source_row`, the mutant reports `met/source_row=ok`.

## Routed defect for the successor counter

Add the `used_by_not_entry` arm verbatim to the selftest `cases` list (after `source_row_queued`, before `fails = 0`), which grows the detector from 13 to 14 checks. Expected behavior with the arm in place: pristine selftest `pass=14 fail=0` exit 0; any counter that drops or weakens the used-by conjunct fails with `FAIL used_by_not_entry … C2=met … source_row=ok` and exit 1. This seat did not modify the tracked counter; the arm adoption is the successor's change to make.

## Restoration evidence

- Every edit was applied to scratch copies only (`pristine.py`, `mutant_m5.py`, `pristine_killer.py`, `mutant_killer.py`, fixture `corpus/SOURCES.md`); no tracked lane path was ever passed to an edit tool.
- Tracked `.ufo/waves/round-47/count-c2.py` sha256 after all runs: `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e` — equal to the before hash and to the scratch pristine copy.
- `git -C <lane> status --porcelain -- .ufo/waves/round-47/` shows only pre-existing untracked w2 dispatch artifacts (`w2-dispatch.json`, `w2-spec.json`, `w2.ready`, `w2.ready.dispatched`, `w2/`); no tracked file modified. The lane's git index and jj state were never touched.
- Scratch artifacts retained for audit under `.scratch/r47w2-MutC2Recheck/` (pristine.py, mutant_m5.py, pristine_killer.py, mutant_killer.py, fixture/).

## UNVERIFIED

- Wave-1's exact mutant bytes (`0844ebbd…`) were not reproduced byte-for-byte; equivalence is behavioral (same survivor outcome), not byte-level.
