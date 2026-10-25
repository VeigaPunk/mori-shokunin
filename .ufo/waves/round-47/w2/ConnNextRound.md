# ConnNextRound — round-48 synthesis (r47 w2)

Seat: ConnNextRound (connector, leaf — no subagent dispatch). Date: 2026-10-25.
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Landed tip T = `68d66ca5`
(commit message states after-receipts at `af2250d8`; `tools/mori-pin-check.py` at T is v2,
sha256 `9832e38c…`; frozen v1 `e3ef425a…` at freeze `63eecf27`). Source: r47 w1 seat reports
(`.ufo/waves/round-47/w1/*.md`), the lesson `corpus/lessons/round-47.md`, contract
`.ufo/waves/round-47/contract.md`, `considerthese/2026-10-25.md`, and read-only byte readings of
the two landed instruments plus small scratch probes (all under
`.scratch/r47w2-ConnNextRound/`; TMPDIR set there for every lane-tool run).

## 1. Executive summary

| # | routed item | state at T | verdict |
|---|---|---|---|
| D1 | count-c2 used-by arm | open (frozen counter) | the used-by check exists in the counter but no selftest arm pins it; mutant (b) survived; successor counter needs a used-by arm |
| D2 | line-count pins | open (contract named limit) | neither v1 nor v2 measures line-count claims (e.g. `743 lines`); drift invisible |
| D3 | truncated digests | open (contract named limit) | a shortened digest pin never equals a file sha256 → always `mismatch`; class not validated, unverifiable |
| D4 | v2 residuals | open (3 reproduced) | L2 `\\|` mis-split, L4 pin-not-at-span-start silently skipped, L5 setup exits 1 with traceback; minor L6/L7 remain |
| D5 | scored instrument gap | open (recorded) | P-C1 was scored with the *frozen v1* bytes (demonstrated false-green-capable); v2 is the standing tool, not the scored bytes |
| S2–S5 | considerthese 2026-10-25 suggestions | 2/3/5 no artifact; 4 practice-only | all four still unimplemented as instruments |
| X1 | cross-claim pattern | candidate for r48 | wave-counter registration couples C1 to C2 (r45 stale-cell class); conflict with the gate-registry auditor requirement |

## 2. Open defects (D1–D5)

### D1 — count-c2 used-by arm (open; lesson M5)
- Mutant history: `w1/MutC2Source.md:18` — "skip used-by check" mutant survives the selftest
  (`C2_SELFTEST pass=13 fail=0`, exit 0). The counter's used-by arm exists in production:
  `count-c2.py:162-165` requires the SOURCES row's `used-by` cell (cells[10]) to contain the
  entry, but `selftest()` (`count-c2.py:253-330`) never exercises it — `no_source_row` deletes
  the row and `source_row_queued` mutates the status cell, neither touches the used-by cell; a
  future deletion of lines 164-165 is invisible to the suite.
- Two sibling C2 parser defects, also open and recorded in lesson M5 (`corpus/lessons/round-47.md:68`):
  - 0–3-space row matching: `count-c2.py:96` `r"^ {0,3}\|…"` rejects rows indented ≥4 spaces
    (`w1/RevCountC2Code.md:5-10`, reproducer printed `None`). False `source_row` failure.
  - one-path-per-cell: a correct path plus a bogus extra path in one `emitted in` cell is not
    flagged (`w1/CritC2Predicate.md:49`, V4 → `C2=met`).
- Verdict: open. A successor counter needs a used-by selftest arm, indentation-tolerant row
  matching, and strict one-path-per-cell; `count-c2.py` is frozen and will not be changed in
  r47 (lesson M5 fix column: "Not fixed: the counter is frozen").

### D2 — line-count pins (open; contract named limit)
- `contract.md:44`: "Named limits: line-count pins (`743 lines`) … are not checked." Both v1
  and v2 measure only two pin kinds — `PREFIX_SELFTEST`-prefixed tallies with a digit and full
  64-hex digests (`tools/mori-pin-check.py:14-21` docstring). A self-test cell that pins a
  length/line claim (real instance: the `GATE_REGISTRY` row's own cell carries `743 lines`,
  `SKILL.md:184`; carried into the r47 registry rows per `w1/ScribeScorecardLog.md:122`) is
  ignored, so a stale line count drifts undetected — the same number-drift class as M1, on a
  pin kind the replacement tool still does not cover.
- Verdict: open. Not addressed by v2 (no new pin kind in the v1→v2 diff).

### D3 — truncated digests (open; contract named limit)
- `contract.md:45`: "truncated digests (`37fd7c24ff52…`) are not checked." Digest matching is
  strict equality against `sha256_file` of files named in the row
  (`tools/mori-pin-check.py:371-382`), so a shortened digest (a) can never verify, and (b) is
  counted as a plain `mismatch` — the class is not recognized, not warned about, and a registry
  that legitimately uses abbreviated digests (as prose does at `SKILL.md:184` and elsewhere)
  cannot be pinned. Fails safe (red), but unverifiable; same in v1 and v2.
- Verdict: open.

### D4 — v2 residuals (three reproduced at T; k L6/L7 remain)
v2 closed the w1 false-green classes: argv allowlist with `SAFE_PATH`/no `-c`/no `.scratch`/
no `..` (`tools/mori-pin-check.py:95-109`), all prefix-led tally lines must agree (stale-echo
class), exact equality (weakened-pin class), fence-aware parsing, entry column from header,
`rebound`/`duplicate` counters, digest-path containment (`w1/RevPinCheckCode.md` M1/M2/M3/L1,
`w1/SentPinExec.md` F1/F2/F3; evidence at `.ufo/waves/round-47/evidence/v2/`; v2 selftest
34/34, `PIN_CHECK_SELFTEST pass=34 fail=0`, rc 0 — run at T by this seat). Residuals, each
reproduced on the landed v2 bytes (`--root` fixture, TMPDIR in scratch):

| id | class | reproducer (run at T) | observed |
|---|---|---|---|
| L2 | GFM `\\|` mis-split | row `… a\\| `python3 tools/foo.py --selftest` → `FOO_SELFTEST pass=3 fail=0` …` (8-cell header) | `pin line=3 kind=row state=unparsed cells=6 header=8` → `PIN_CHECK=unmet … unparsed=1`, rc 1 (false red; `tools/mori-pin-check.py:115` `(?<!\\)\|` unchanged; `w1/RevPinCheckCode.md:132-145`) |
| L4 | pin not at span start silently skipped | self-test cell `` `python3 tools/foo.py --selftest` → `run: FOO_SELFTEST pass=3 fail=0` `` | zero `pin` lines, `PIN_CHECK=unmet tally_pins=0`, rc 1 only via the floor; the pinned claim is never measured and no diagnostic names it (`tools/mori-pin-check.py:188` `re.match(…, span)` requires prefix at span start; `w1/RevPinCheckCode.md:161-169`) |
| L5 | setup-class failures exit 1 with traceback | `--rev HEAD --repo /nonexistent-r47-connnextround` | `PermissionError: [Errno 13] Permission denied` traceback, rc 1 (documented contract exit is 2; `tools/mori-pin-check.py:244,438` `makedirs` uncaught; `w1/RevPinCheckCode.md:171-182`) |

- L6/L7 (informational, unchanged): dead `scratch` params (`run_cmd`/`check`), `REV_WORDS`
  bare `REV` stays literal in `--root` mode, `strip_env` silently drops leading `VAR=value`
  words (`w1/RevPinCheckCode.md:184-201`).
- One security note remains even under v2: the tool executes every committed `.py`/`.sh` under
  `tools/` and `.ufo/waves/round-N/` that a row names — by design, but the RCE surface of a
  compromised registry is now bounded to committed instruments only (F1/F2 contained;
  `w1/SentPinExec.md:21-31`).

### D5 — scored instrument gap (recorded, worth naming for r48)
- P-C1's `PIN_CHECK=met` at T was produced by the **frozen v1** bytes
  (`after-c1-v1-frozen.txt`; lesson `corpus/lessons/round-47.md:4-5`), the very tool w1 showed
  green on four junk edits (`w1/CritC1Predicate.md:45-51` v2/v3/v7/v8). The standing v2 also
  passes the honest registry (`after-c1-v2.txt`, `PIN_CHECK=met tally_pins=28 … rebound=0
  duplicate=0`, rc 0), so the claim's *content* holds, but the scored instrument is the weaker
  one. For r48: state explicitly which bytes score any re-run of C1.
- Consequences already visible at T: SKILL.md now registers **both** rows
  (`SKILL.md:938` pin-check v2, `SKILL.md:939` r47 tracepoint catalogue C2) — see X1.

## 3. considerthese 2026-10-25.md suggestions 2–5 (all still unimplemented)

Per `w1/ScoutConsider.md` (adoption census) and the suggestion file itself:

| # | suggestion (file:line) | status at T | evidence |
|---|---|---|---|
| 1 | registry pin check (`:44-46`) | implemented — QUALITY 123 + `tools/mori-pin-check.py` (v2 standing); lesson `corpus/lessons/round-47.md:51-53` | `w1/ScoutConsider.md:34-44` (first committed instance is the r47 freeze) |
| 2 | host-path portability list (`:47-49`) | **no artifact** — no tracking list or counter exists; `grep` for `portability` in `corpus/QUALITY.md`/lessons/`LOG.md` → no hits | `w1/ScoutConsider.md:229` (reflection's 13-file count reproduces at both revs; wider scopes give 36) |
| 3 | track whether in-round critic flags get fixed (`:50-52`) | **no artifact** — the r45 instance the proposal cites is real (`w1/ScoutConsider.md:230`; `corpus/lessons/round-45-verifier-spotcheck.md:62-66`), but no flagged-versus-fixed counter exists | `w1/ScoutConsider.md:230` |
| 4 | track where my own suggestions end up (`:53-55`) | practice-only — the ScoutConsider audit seat *is* the track, and its reports were only committed from r44 on; the r42/r43 instances are lost as files | `w1/ScoutConsider.md:202-203,279-280` |
| 5 | track retries (`:56-58`) | **no artifact** — `lane-dead-no-report` lines appear only inside closure files; `grep -n 'lane-dead-no-report' LOG.md` → no hits | `w1/ScoutConsider.md:231` |

Verbatim proposal texts at `considerthese/2026-10-25.md:47-58`.

## 4. Cross-claim pattern worth a future claim (X1)

**Wave-counter registration couples C1 to C2 — the r45 stale-cell class, re-created at
`SKILL.md:939`.** The w1 connector recommended omitting the wave counter row (`w1/ConnCrossClaim.md:17,200-206`;
`contract.md:80-84` requires C1 and C2 to be runnable with the other reverted); the integrator
kept it because the lane's gate-registry auditor requires an attribution row for every
instrument (`w1/ExecRegistryAudit.md:30-33,105-111`, `REGISTRY=unmet` without it). Result:
`tools/mori-pin-check.py` now executes `count-c2.py --selftest` on every C1 run
(`SKILL.md:939`), so any future round that edits or retires the r47 counter must also re-pin
line 939 or C1 goes red — precisely the r45 harm class (wave counters registered in SKILL.md
went stale; `corpus/lessons/round-45-verifier-spotcheck.md:50-68`; `considerthese/2026-10-25.md:31-40`).

Future-claim shape (bounded, one axis, falsifiable): decouple wave-instrument registration from
the permanent gate registry — e.g. a wave-instruments manifest (`.ufo/waves/round-N/instruments.json`)
or a distinct non-SKILL.md table that the auditor reads but C1 does not measure; claim would be
that C1 stays met across a wave-counter edit/retirement (red control: retire the r47 counter
without touching `SKILL.md:939`; expect `PIN_CHECK=met`), scored with the v2 standing bytes.
Axes: calibration (protects C1 from wave churn) × operability (auditor still sees every
instrument). Contradiction to state, not smooth over: the auditor requirement (register
everything) and C1's separability requirement (measure only permanent gates) conflict at
`SKILL.md:939`; either the auditor accepts a non-gate instrument surface or C1 must exclude
round-scoped rows.

## 5. Evidence (observed, this seat)

Reads/runs at T (`68d66ca5`); all lane tools run with `TMPDIR=<lane>/.scratch/r47w2-ConnNextRound`:

- `git show T:tools/mori-pin-check.py | sha256sum` → `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6`.
- `git show T:.ufo/waves/round-47/count-c2.py | sha256sum` → `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e` (equals the frozen contract bytes).
- v2 selftest at T: `PIN_CHECK_SELFTEST pass=34 fail=0`, rc 0.
- L2 probe: `--root probe --skill probe/l2.md --min-tally-pins 1` → `pin line=3 kind=row state=unparsed cells=6 header=8`, `PIN_CHECK=unmet … unparsed=1`, rc 1.
- L4 probe: 8-cell row, self-test cell ends `` `run: FOO_SELFTEST pass=3 fail=0` `` → no pin lines, `PIN_CHECK=unmet tally_pins=0`, rc 1.
- L5 probe: `--rev HEAD --repo /nonexistent-r47-connnextround` → `PermissionError` traceback, rc 1.
- `git show T:SKILL.md` rows: `:938` registry pin reconciler (v2, `PIN_CHECK_SELFTEST pass=34 fail=0`), `:939` r47 tracepoint catalogue (C2, `C2_SELFTEST pass=13 fail=0`); `:184` GATE_REGISTRY cell carries `(743 lines)`.
- `git show T:.ufo/waves/round-47/evidence/after-c1-v2.txt` tail: `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 … rebound=0 duplicate=0 … baseline=yes`, rc 0; `evidence/v2/skill-v0..v8.txt` present (junk variants unmet under v2).

## 6. Limits / UNVERIFIED

- This seat did not re-run the full C1/C2 claim commands at T (executor peers own those runs);
  after-receipt readings above are byte-reads of committed evidence, not fresh claim runs.
- D2/D3 are read from the contract named limits, the v1→v2 diff (no new pin kinds), and code
  reading; no new fixture was built for them.
- v2 residuals L2/L4/L5 were reproduced on minimal scratch fixtures; the real SKILL.md has zero
  `\\|` and zero non-start-of-span pins (w1 reviews), so they are latent, not live reds.
- Fence/`rebound`/`duplicate` v2 arms were not individually re-probed; they are covered by the
  v2 selftest suite (34/34) and the committed `evidence/v2/` junk receipts.

Report: `.ufo/waves/round-47/w2/ConnNextRound.md` (relative to
`/home/vgpnk/Projects/shokunin/mori-shokunin`). Scratch: `.scratch/r47w2-ConnNextRound/`.
No production file edited; read-only git only; no tool installed.
