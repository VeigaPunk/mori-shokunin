# Mo54MutC1 — mutation test of the frozen round-54 C1 counter (wave w1)

Seat Mo54MutC1 (mutation-tester), lane mori-shokunin, 2026-10-27. MACHINE_ID: 432d02b544a5459ebbff9c42ec68334d (host plazir27).

Target: `.ufo/waves/round-54/count-c1.py` as landed at data commit `78295c764093ff1f6cee08d7246679900bde7265`, sha256 `e97a11986694b60f3a5d9d50b151553072f08a8a8d46cbea8f4b63a90dff433c`. The frozen file was never written by this seat; every mutation lived in a scratch copy and was restored.

## Method

- Detector, the same bounded behavioral detector on pristine, mutated and restored bytes: `python3 <working copy> --selftest` — the counter's own in-memory fixture suite (57 checks). Killed iff exit != 0. A run that died without printing a `C1_SELFTEST` summary would have been recorded inconclusive; none occurred (every killed run printed its summary with fail>=1, every survivor printed `pass=57 fail=0`).
- Scratch (operator directive 2026-10-25): everything under `/fast/scratch/hyaku/mori-r54/Mo54MutC1/` — `pristine-count-c1.py`, the working copy at `lane/.ufo/waves/round-54/count-c1.py` (placed at the same four-directory depth so the selftest's `lane_root()` resolves inside the scratch), the eight committed v7.3 copies the selftest reads (`lane/corpus/evidence/sources-r54/{memcontrol.c,oom_kill.c,percpu_counter.c,percpu_counter.h,errno.h}.v7.3`, `cgroup-v2.7.3.html`, `lane/corpus/evidence/sources-r53/{util.c,mm_init.c}.v7.3`), `tmp/` as TMPDIR, `evidence/` for raw detector outputs. `disk-guard.sh status` before the run: `/fast/scratch/hyaku 25% 604.3G` free — no ENOSPC. Scratch removed at the end of the seat.
- Protocol per mutation: write pristine bytes to the working copy, apply one exact-string mutation (anchor required to occur exactly once in the pristine source), hash the mutant, run the detector, write the pristine bytes back, re-hash (must equal the pristine hash), run the detector on the restored bytes (must exit 0). All 20 anchors matched exactly once; all 20 restorations verified byte-exact with a passing re-run.
- No git/jj command touched the lane, the fleet root, or any index. The only git use was read-only against the lane (`rev-parse`/`show`/`ls-tree` inside the counter itself, plus one `diff --stat` for the M13 characterization below). No tool was installed or upgraded (the 2026-10-19 tooling authorization went unused; pacman untouched per the 2026-10-20 pause).
- Baseline on pristine bytes: exit 0, `C1_SELFTEST pass=57 fail=0`. The eight copies in the scratch lane hash-match their frozen pins (listed under Restoration evidence), which the baseline's honest-met and pin checks exercise.

## Result table

19 listed single-point mutations plus one variant probe (M05b) of the same point as M05. Verdict killed = selftest exit 1; survived = exit 0 with `pass=57 fail=0`.

| id | single-point mutation (count-c1.py line) | verdict | killing check(s) |
|---|---|---|---|
| M01 | `MIN_VOTES = 2` -> `1` (line 61) | killed | one_voter_unmet, same_voter_twice_unmet, voter_not_in_results_unmet |
| M02 | vote-reader fence toggle dropped (final_votes, lines 256-261) | killed | fenced_votes_unmet, fenced_dissent_ignored_met, fenced_quote_proposal_ignored_met |
| M03 | last-wins -> first-wins on a voter's repeated line (line 263) | killed | revised_dissent_met |
| M04 | results-file binding dropped (line 252) | killed | voter_not_in_results_unmet, results_absent_unmet, results_malformed_unmet, results_wrong_key_unmet, results_bare_list_unmet, unsettled_dissent_ignored_met |
| M05 | name check dropped: any result accepted, `settled.add(r.get("name"))` (lines 246-247) | survived (equivalent) | — |
| M05b | variant of M05: a name-less result settles every voter (`settled.update(VOTERS)`) | killed | voter_not_in_results_unmet, results_wrong_key_unmet, unsettled_dissent_ignored_met |
| M06 | authorship subtraction dropped (line 348) | killed | author_vote_not_counted_unmet |
| M07 | status always `held` (line 322) | killed | honest_met, held_labelled_absent_unmet, html_line_located_met, row_opened_r53_day_met, indented_rows_met, voters_in_results_met, revised_dissent_met, fenced_dissent_ignored_met, unsettled_dissent_ignored_met, fenced_quote_proposal_ignored_met, all_changed_with_votes_met |
| M08 | quote check without `q == q72` for held rows (line 328) | killed | held_with_other_quote_unmet |
| M09 | line arm accepts line +/- 1 (line 331) | killed | line_off_by_one_unmet |
| M10 | line arm skipped: `failed.append("line")` -> pass (line 360) | killed | line_off_by_one_unmet, line_blank_unmet, line_zero_unmet, line_leading_zero_unmet |
| M11 | norm_map HTML entity decoding dropped (line 133) | killed | norm_map_html_lines, html_norm_equals_r50_normalise |
| M12 | word bounds 6..25 dropped (line 327) | killed | replacement_too_short_unmet |
| M13 | scope read at R instead of ENTERING (line 426) | survived | — |
| M14 | r53-hash exclusion dropped (line 232) | killed | scope_reader |
| M15 | used-by check dropped (line 338) | killed | row_usedby_unmet, row_usedby_r53_ledger_only_unmet |
| M16 | OPENED widened to any date (line 338) | killed | row_opened_earlier_unmet |
| M17 | v7.3 URL check dropped (line 337) | killed | row_v72_url_unmet, row_other_path_unmet |
| M18 | pins enforcement skipped (line 281) | killed | pin_tampered_unmet |
| M19 | `rows == len(d)` clause dropped (line 353) | survived (equivalent) | — |

Score: 16 of the 19 listed mutants killed; 3 survived (M05, M13, M19); the M05 variant probe killed. No mutant was inconclusive.

## Exact anchors applied (old -> new)

Fenced for reproduction; each `old` occurred exactly once in the pristine source (verified by the harness before each run).

````python
MUTS = [
    ("M01", "MIN_VOTES 2 -> 1", "MIN_VOTES = 2", "MIN_VOTES = 1"),
    ("M02", "drop the vote-reader fence toggle",
     '            if line.lstrip()[:3] in ("```", "~~~"):\n                fence = not fence\n                continue\n            if fence:\n                continue\n            m = RECHECK_RE.match(line)',
     '            m = RECHECK_RE.match(line)'),
    ("M03", "last-wins -> first-wins",
     'votes.setdefault(m.group(1), {})[voter] = m.group(2)',
     'votes.setdefault(m.group(1), {}).setdefault(voter, m.group(2))'),
    ("M04", "drop the results-file binding",
     'if path not in present or voter not in settled:', 'if path not in present:'),
    ("M05", "accept any name-less result",
     'if isinstance(r, dict) and isinstance(r.get("name"), str):\n                settled.add(r["name"])',
     'if isinstance(r, dict):\n                settled.add(r.get("name"))'),
    ("M05b", "VARIANT of M05: a name-less result settles every voter",
     'if isinstance(r, dict) and isinstance(r.get("name"), str):\n                settled.add(r["name"])',
     'if isinstance(r, dict):\n                settled.update(VOTERS)'),
    ("M06", "drop the authorship subtraction",
     'if word == disp and q not in proposed.get(w, {}).get(h, set())]', 'if word == disp]'),
    ("M07", "status always held",
     'derived = "held" if q72 in text else "absent"', 'derived = "held"'),
    ("M08", "quote check without q == q72 for held rows",
     'and q in text\n                    and (derived != "held" or q == q72)):\n                c["quote_ok"] += 1',
     'and q in text):\n                c["quote_ok"] += 1'),
    ("M09", "line arm accepts line +/- 1",
     'and int(lv) in lines_of(raw, text, offs, q):',
     'and (int(lv) in lines_of(raw, text, offs, q) or int(lv) - 1 in lines_of(raw, text, offs, q)\n                     or int(lv) + 1 in lines_of(raw, text, offs, q)):'),
    ("M10", "line arm skipped", '            failed.append("line")', '            pass  # line arm skipped'),
    ("M11", "norm_map HTML drops entity decoding",
     'rep = html.unescape(tok) if tok.startswith("&") else " "', 'rep = " "'),
    ("M12", "word bounds dropped", 'MIN_WORDS <= len(q.split(" ")) <= MAX_WORDS', 'True'),
    ("M13", "scope read at R instead of ENTERING",
     '    d = scope(git_reader(repo, ENTERING), git_lister(repo, ENTERING))\n    if not d:',
     '    d = scope(git_reader(repo, full), git_lister(repo, full))\n    if not d:'),
    ("M14", "r53-hash exclusion dropped", 'if q is None or h in done:', 'if q is None:'),
    ("M15", "used-by check dropped",
     ' and LEDGER in [u.strip() for u in re.split(r"[,;]", srow[10])])', ')'),
    ("M16", "OPENED widened to any date", 'and srow[8] in OPENED', 'and True'),
    ("M17", "v7.2 URL accepted", 'and V73[key][2] in srow[1]', 'and True'),
    ("M18", "pins check skipped", '        failed.append("pins")', '        pass  # pins check skipped'),
    ("M19", "rows == len(d) clause dropped",
     'if c["matched"] != len(d) or c["rows"] != len(d):', 'if c["matched"] != len(d):'),
]
````

## Survivor arm text (routed limits, not fixes — the counters are frozen this round)

### M13 — the selftest never executes main()'s revision branch, so the entering-tip binding of D is unguarded (MED)

The selftest exercises `scope()` only through a synthetic entering tree (count-c1.py line 715) and returns before main()'s revision branch runs, so a counter that read the frozen scope D at the scored revision instead of the entering tip (line 426) still passes its own selftest. Characterization on the real lane (read-only runs, cwd scratch):

- pristine: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/count-c1.py 78295c764093ff1f6cee08d7246679900bde7265` -> exit 1, `C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=votes` — byte-identical to the recorded receipt `evidence/c1-at-data.txt`.
- M13 mutant (same rev, `--repo` the real lane): exit 1, the same line byte-for-byte.
- `git diff --stat 39dcf4d7..78295c76 -- corpus/knowledge/`: only two new files (`kernel-v7.3-recheck-r54.md` +109, `memory-failure-kills-r54.md` +86); no entry table edited — and the identical `scope=31` in both runs shows D read at R equals D read at the entering tip on this data.

So the mutant is live in principle (a future data commit that edits an entry's claim table, or adds a v7.2-pinned SOURCES row, would diverge) but inert on the round-54 data, and the selftest cannot see it either way. Routed limit for round 55: the selftest has no fixture whose entering tree differs from the scored tree, so the "D is read at the entering tip only" property rests on the frozen source text, not on a test.

### M05 — the name-presence check in the results binding is redundant (LOW, equivalent mutant)

`settled` is queried only against the VOTERS strings (line 252), so a result whose `name` is missing or non-string can never settle a voter: dropping the guard (M05) changes `settled` only by entries like `None` that match nothing, on every input. The mutant passes the selftest with `pass=57 fail=0` — an equivalent mutant, not a missed kill. The harsher reading of the same point — a name-less result settling every voter (M05b) — is killed by three checks. Recorded so a future mutation pass does not re-flag this point as a hole; there is nothing to fix.

### M19 — the `rows == len(d)` clause is implied by `matched == len(d)` plus bad_rows (LOW, equivalent mutant)

Every row that increments `rows` without incrementing `matched` increments `bad` (wrong cell count, unknown hash, duplicate hash — lines 306-316), and `matched <= rows`, so `rows != len(d)` while `matched == len(d)` forces `bad > 0`, which already fails the run at line 355-356. Dropping the clause (M19) is unobservable on every input (`pass=57 fail=0`); the extra-row and duplicate-row fixtures kill through `bad_rows` instead. Redundancy, not a hole.

## Restoration evidence

- Pristine sha256 (before each mutation and after each restore, and of the final working copy): `e97a11986694b60f3a5d9d50b151553072f08a8a8d46cbea8f4b63a90dff433c`.
- Per-mutant sha256 while mutated, and the restored-bytes detector run (all exit 0):

| id | mutant sha256 | restored rc |
|---|---|---|
| M01 | 45d6f03cfa2c4dd774b984802fbc202da3c2af9e60ee40093b11ca993f19d006 | 0 |
| M02 | 298949cdab7cfc3ac6e59c9d33695538103e16e4c2837e387972d52192926ff7 | 0 |
| M03 | 3dc8490ff1e2b764ceab836d2dad3ef10ad84e2df871b5bb94306befc1a359f6 | 0 |
| M04 | c5300585a101a9a6d9120758c891085f368f32b49db968ff3e60e6b05d82a679 | 0 |
| M05 | 2aeb91ce185d3e1f0bc3aee6cc9e4208c2c4fa9cd6bcb00ead364610641cac5e | 0 |
| M05b | 7f7555a9ea8f7760d56c056da3b99e521ab310d5ce2f73e5ca944a3d4966efff | 0 |
| M06 | 2eaad5dc4d4584afd0cda51af8fd760ed5f2f20e8be41a8b10307af335d0762d | 0 |
| M07 | 720a0a07592d2d3d113bb3991f8f34e3ef267a06a48ca7d967c7c973e686a3c9 | 0 |
| M08 | 1208fa0c952a84e29c9a26ac631f2755628b16d853637bce6a93611293e7e459 | 0 |
| M09 | ce29cc90ec30a0eb84c27f9953da65bad94a95146543f0ff0911db9114c7b3f2 | 0 |
| M10 | 1114bfcf9bc662d21dd1ac14c3840c7feb97536f27ac8dd7afafbd5f72eeaf81 | 0 |
| M11 | 6e39f53dc598d11c9219b09034121ae99ab8eb8d9a933fc3f226b5d5f3dbd1de | 0 |
| M12 | 7391889b5b6ca331b54909a204034382265762e6b2c04e3182c9fde14f77282c | 0 |
| M13 | 5c61280b128a017f86ff2386bf6bddd48876066b865c1b58a2009e105c1301ba | 0 |
| M14 | ee3a69b9fda206b6829ba90e10ba8b1dadeacf3917791fafc73ee38078331519 | 0 |
| M15 | b8faf7624a0aad5969656edaf3c03c755a3630b1e5302a6352c1bc58224e2f34 | 0 |
| M16 | 27a80374a221083b479a9ae0f67c219eb40c9f9d85f3a7ec9d0ee51e777c157e | 0 |
| M17 | 50820d47e68ac169590e8295ee92f8c6824d41145a708dc91241e893201ea8c3 | 0 |
| M18 | 4ac2738912978c5a29b4542894e128099bc758fc5cb2ec76876ca2fd225f09ce | 0 |
| M19 | 3412c9d526a3b0c080c3e4e76907ca0bb05c1a27093d9d8d0811276f1e04bb14 | 0 |

- The eight evidence copies staged into the scratch lane matched their frozen pins: cgroup-v2.7.3.html `b478c1ba…f3d4b`, errno.h.v7.3 `66a5ad60…1622be`, memcontrol.c.v7.3 `bdb6159c…c41a1`, oom_kill.c.v7.3 `452f1348…56b4e`, percpu_counter.c.v7.3 `2c26e677…130d6d`, percpu_counter.h.v7.3 `4a107bc3…ef896`, mm_init.c.v7.3 `67841000…f976c`, util.c.v7.3 `4dfcce2b…9e1f2` (full digests as frozen in the counter's `_COPIES`).
- The frozen file itself, re-hashed after the seat: `e97a11986694b60f3a5d9d50b151553072f08a8a8d46cbea8f4b63a90dff433c` — unchanged.

## Tooling

Nothing installed or upgraded. Full-system packages untouched (pacman paused per the orchestrator ruling of 2026-10-20; not needed — the detector is the counter's own `--selftest` under the host's python3).

## Findings

- MED — `.ufo/waves/round-54/count-c1.py`, main() lines 426-429 vs selftest line 715: the selftest never executes main()'s revision branch, so the "frozen scope D read at the entering tip only" binding is unguarded by `--selftest`; mutant M13 (scope read at the scored rev) survives. Inert on the round-54 data (byte-identical counter lines at `78295c76`, and the data commit edits no entry table), live in principle. Routed item for round 55: a selftest fixture whose entering tree differs from the scored tree, asserting D stays the entering one.
- LOW — `.ufo/waves/round-54/count-c1.py` lines 246-247: the `isinstance(r.get("name"), str)` guard is redundant (settled is only queried against VOTERS strings at line 252); dropping it is an equivalent mutant (M05, survived). The harsher variant M05b is killed. No weakness; do not re-flag.
- LOW — `.ufo/waves/round-54/count-c1.py` line 353: the `c["rows"] != len(d)` clause is implied by `matched == len(d)` plus the bad_rows failure; dropping it is an equivalent mutant (M19, survived). Redundancy, not a hole.
- LOW — `.ufo/waves/round-54/count-c1.py` selftest assertion robustness, e.g. lines 529, 536, 540, 562: the token half of several assertions (`"rows" in line`, `"status" in line`, `"line" in line`) is vacuous because the token also occurs inside the counter's own metric names (`rows=`, `status_ok=`, `line_ok=`); the verdict half (`not met`, the exact `line_ok=3`/`status_ok=3` substrings) carries those kills — M07 and M10 were still killed. Margin note for any future tightening of the selftest; no action this round.
