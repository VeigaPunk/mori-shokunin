# Mo56RevNoHarm — no-harm audit of the round-56 freeze diff

Seat: Mo56RevNoHarm (reviewer). Scope: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat 5b295eeebd87ebd610d8d39bfe2035742f740cfa 8be2717b0809281d07dffe83dad424a4859e0747` — every changed tracked file, audited for harm on all six axes. Read-only throughout: nothing in the lane repo, fleet repo, or host was written by this seat.

## Method and shape of the diff

- `git diff --stat` → 34 files, 2942 insertions, 0 deletions. `git diff --summary` → 33 `create` entries and one modified file (`corpus/SOURCES.md`). Purely additive.
- Commit chain (`git log --oneline 5b295eee..8be2717b`): `c419fe6d` data → `6ced9da9` data correction (docstring norem) → `3f494b49` freeze (contract+pins+controls) → `8be2717b` freeze correction (fence mutant pattern) + controls + receipts.
- The whole `8be2717b` tree was materialized with `git archive | tar -x` into seat scratch `/fast/scratch/hyaku/mori-r56/Mo56RevNoHarm/8be2/` and every changed file read there. Working tree HEAD is `acc62f54` with unrelated dirt (`M LOG.md/SCORECARD.md/SHONEN.md`, `?? w1/`, `?? corpus/lessons/round-56.md`) — outside the assigned diff.
- The only file with pre-existing bytes touched is `corpus/SOURCES.md` (S544, S545 appended after S543, before `## Paths`; no existing line modified).

## Axis verdicts

### Coverage — NOT HARMED

- The FR5 advance is the exact ground the frontier row names: `corpus/README.md:345` (FR5) carries "Round 33: ... reading the driver's `launch`/`complete` lines in `.ufo/watchdog.log` as a second liveness source is open coverage ground". `corpus/knowledge/driver-liveness-r56.md:6` cites this correctly; nothing else on the coverage map was touched (README unchanged in the diff).
- Registry append: `corpus/SOURCES.md` `^| S` rows 316 (entering) → 318 (freeze). S544/S545 consume the next free ids; `mined`, `2026-10-27`, and used-by naming the entry present in both rows (verified by reading the diff hunk).
- Census behavior: the census runner is `scripts/sources-census.sh validate` (fleet repo, read-only). S545's URL `rfc8259.txt` is unique in the registry (S062/S209 are RFC 8785; the 4 pre-existing `rfc8259` grep hits are `.src` evidence bodies, not URLs) and S544 is own-work — so the W04 set stays exactly the 23 listed in `evidence/census-start.txt`, and `ok` + exit 0 shape is preserved. Row grammar `| S<id> | ... |` (11 cells, same shape as S541–S543) verified visually.
- Registry-row pointers: the 49 entering-tip `S544| S545` refs are all in frozen round-44–50 artifacts (assimilation `staged-ids`, `renumber-map.tsv` — old S544→S547/S548 per `round-45/assimilation/renumber-map.tsv:97-101`) plus `corpus/lessons/round-49.md`, which explicitly records those staged ids as **not adopted** (`:75` "against `reg-ids` → `0`", `:85` "are not adopted"). No live entry resolves S544/S545 to different content than the new rows. Named limit: grep-over-history for S544/S545 now hits both the old maps and the new rows (LOW, residual ambiguity).

### Operability — NOT HARMED

- Re-ran both frozen counters from the archive-extracted tree at the true freeze tip:
  `python3 .ufo/waves/round-56/count-c1.py 8be2717b...` → `C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747` (exit 0).
  `python3 .ufo/waves/round-56/count-c2.py 8be2717b...` → `C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747` (exit 0).
- C1/C2 are separable as contracted: distinct counters, tools, fixtures; shared surface is only the SOURCES append (distinct rows, one commit).
- The contrast arm re-executes the frozen round-55 C1 counter at R over committed artifacts; all three inputs (`corpus/knowledge/kernel-v7.3-recheck-r55.md`, `.ufo/waves/round-55/w1-results.json`, `.ufo/waves/round-55/count-c1.py`) exist at 8be2 (git ls-files: 3/3).
- Do-nothing controls at entering tip: `controls.txt` shows `failed=tool_absent` / `C2=unmet` at `5b295eee` — consistent with tools absent before `c419fe6d`.

### Depth — NOT HARMED

- Entry↔row↔tool binding verified: `driver-liveness-r56.md` names S544 and the tool; `vote-binding-r56.md` names S545 and the tool; both entries carry measured sections that match committed receipts.
- `driver-liveness-r56.md:49-51` claims live numbers (1728 lines, 0 malformed, 121 other_lines, mori 66 launches/39 completes/17 deads/in_flight/unclosed 10); `evidence/driver-liveness-live.txt` carries the identical mori row (`:195-206`: completes 39, deads 17, in_flight true, launches 66, unclosed 10).
- The tally receipt (`evidence/tally-r55.txt` `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15`) is reproduced by the counter at R (run above).
- Fixture content is coherent with selftest expectations (e.g. `malformed/watchdog.log` yields malformed=5, other_lines=1; `variants/` yields the multi-lane variant shapes the tool's docstring enumerates). Counter `fixtures=ok` at R covers all 9 EXPECT_FIX entries including the symlink-bearing `state-shapes` fixture.

### Freshness — NOT HARMED; verified current

- S544's grammar extract `corpus/evidence/sources-r56/watchdog-log-grammar.txt` byte-equals the live writer lines read today: `awk 'NR==149||NR==176||NR==182' /home/vgpnk/Projects/shokunin/scripts/hyaku/inline.sh` and `NR==266||NR==405||NR==448' /home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh` printed exactly the six extract lines.
- S545's copy `corpus/evidence/sources-r56/rfc8259.txt` sha256 `61a5378f…` equals a live fetch of `https://www.rfc-editor.org/rfc/rfc8259.txt` today (`sha256sum` identical, 899 lines).
- Tool shas at freeze tip equal the data-commit shas in `freeze-sha256.txt` (driver `6b3dba74…`, vote `8be1acdb…`); counter PIN constants match the same values, so no pin is stale relative to the tip.

### Calibration — NOT HARMED; two LOW notes

- Full pin chain verified at 8be2: `contract.md` `088761f3…`, `count-c1.py` `c4e58eed…`, `count-c2.py` `4b350c77…`, `controls.py` `5bf65ac0…` — all matching `evidence/freeze-sha256.txt`.
- `controls.py` legitimately changed between `3f494b49` and `8be2717b` (blob `e6860bb0` → `81d600b6`, the fence-mutant-pattern correction); the pin file lands at 8be2 and matches the corrected bytes. No stale pin left behind.
- LOW (calibration, route to round 57): `evidence/census-start.txt` carries 23 W04 lines + `ok` + `exit=0` but **no stamped revision and no row count** — the contract's defect-2 parenthetical "(receipts here stamp the measured revision themselves)" holds for the counter receipts (`rev=3f494b49` present in `c1-at-freeze.txt`/`c2-at-freeze.txt`) but not for this census receipt; the "316 rows" figure is only re-derivable (I re-derived it: 316 `^| S` rows at `5b295eee`). A before→after row cannot cite a revision from these bytes.
- Informational: at-freeze counter receipts stamp `rev=3f494b49`, one commit below the tip; harmless because contract/counters/tools blobs are identical between `3f494b49` and `8be2717b` (verified via `git rev-parse`) and both counters re-verify `met` at `8be2717b` (runs above). `controls.txt` was captured at `8be2717b` alongside the corrected module.

### Adjacency — NOT HARMED

- No path outside the mori lane's own `corpus/`, `tools/`, and `.ufo/waves/round-56/` appears in the diff; nothing under kumitate/tsukuroi/souji/kama/kagi or the fleet root was touched.
- Write surface of every executable artifact: tools and counters open inputs read-only (`open(path, "r")`, `git show`/`ls-tree`/`rev-parse`); all writes go to `tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))` (driver-liveness `t_empty_log`, vote-bind selftest fixtures, counter materialization). No sysctl/cgroup/systemctl/watchdog.log/state writes; `state_shapes()` never reads `.round` values and never follows symlinks.
- `tools/mori-driver-liveness.py` reads the fleet-level `.ufo/watchdog.log` (default fleet root = parent of the lane) — reading the fleet log is mori's assigned surface (fleet liveness); fixture `variants/` includes other lanes' names only as log-shape parse input.
- S544 cites fleet-repo scripts (`scripts/hyaku/inline.sh`, `scripts/shokunin-watchdog.sh`) as the source — own-work pattern, read-only, no ownership crossing.

## Residual risk and verification gaps

- The 10 `single` tally rows are carried honestly by the binder (dispatch-coverage validator remains planned, per contract); not a harm, but the round-55 coverage hole persists unchanged.
- The binder binds on `output` fields of `w1-results.json`; a seat whose votes reach the results file only inside a report file or under a fence still binds — covered by selftest arms, no drift observed.
- UNVERIFIED: end-census run (contract schedules it at closure); I verified the append cannot add W04 rows and preserves row grammar, which is the only census-visible change the diff makes.
- `corpus/README.md` knowledge index lacks rows for the two r56 entries at the freeze tip; integration rounds update the index at closure (round-52/55 history shows this pattern). Named so it is not lost (LOW).

## Findings

- LOW — registry-id reuse ambiguity: S544/S545 appear as different (rejected/renumbered) identities in frozen round-44–50 artifacts (`.ufo/waves/round-45/assimilation/renumber-map.tsv:97-101`, `corpus/lessons/round-49.md:66,75,85,105`); historical-grep collision only, no live pointer broken. Not introduced wrongly by this diff (ids were the next free), but the ambiguity now exists in the corpus.
- LOW — `evidence/census-start.txt` lacks a stamped revision and row count; contract defect-2 claim "receipts stamp the measured revision" does not hold for the census arm (only for the counter receipts). Route: stamp revision + row count on round-57 census receipts.
- LOW — `corpus/README.md` index has no rows for `driver-liveness-r56.md` / `vote-binding-r56.md` at the freeze tip; expected at closure but must not be forgotten by the integration pass.
- Informational (no defect): at-freeze receipts stamp `rev=3f494b49` while the freeze tip is `8be2717b`; counters re-verified `met` at `8be2717b` by independent re-run, so nothing is stale.

Report: .ufo/waves/round-56/w1/Mo56RevNoHarm.md
