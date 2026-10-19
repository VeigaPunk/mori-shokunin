# drift pin r10 — the census's own behavioral baseline: design, the volatile contract and its measured rationale, the masking risks, the adopted lane baseline, and the admission ritual

source: `tools/mori-census.sh` entering this round `1c49238a7fd87277151ff5776acfb4d62fadd9d69764a02f0ede03ef0d3902d2`
(r9 bytes, `VERSION=census-r5`, 2394 lines) → **settled** `d7710981aa1c7571ff9d6fd7f75822811173010e5f4e298ac3c47fab274a0b20`
(`git diff --numstat` = 475 +, 36 −; 2833 lines; `VERSION` still `census-r5`, so the revision is
distinguished by SHA, not by a version bump). The implementation was written in several visible
steps between 21:57:55Z and 22:12Z (observed shas `ef787505…`, `72da04b8…`, `c37b2ee6…`,
`6d61ff16…`, `4897df03…`, `62e76cfd…`, `1ddb7ff8…`, `d7710981…`); two of them carry the
substance: `1ddb7ff8…` (the whole pin/drift mechanism — header contract, normalize, pin, drift,
reporting, 10 selftest cases) and `d7710981…` (+14 lines: `run_drift` now also compares the
baseline's recorded `volatile_fields` list against the current one, plus the selftest arm for
it). **All line numbers below are `d7710981…`'s**; both substantive revisions are cited where a
claim was read or run at `1ddb7ff8…`. The oracle `tools/mori-silence-cases.sh`
`448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` is byte-frozen this round
(not this seat's check: the receipts-writer's run at the revision their receipts pin, `1ddb7ff8…`,
is `MORI_SILENCE_CASES: matched=28 total=28` with `CASE_IDS` diff vs HEAD `0 added / 0 removed`;
staged at `/tmp/mori-r10-receipts/out/oracle.log`, and the committed set lands under
`corpus/evidence/` as `pin-r10-*.log`).

verified-at: 2026-10-15T22:06:01–22:17Z, two arms, one per revision:

- **`1ddb7ff8…`** (frozen snapshot `/tmp/mori-r10-note/census-snap.sh`, taken so the evidence
  stayed bound to one revision while the lane file churned under it): the full 9-leg cycle
  (`/tmp/mori-r10-note/cycle/cycle.log`) plus the three-pair mask holdout
  (`/tmp/mori-r10-note/holdout.sh`).
- **`d7710981…`** (the settled bytes): `--selftest` → `PASS (66 cases, 66 passed, 0 failed)`
  exit 0 (`/tmp/mori-r10-note/selftest-at-settled.out`), `--drift` against the **committed**
  lane baseline → `MORI_DRIFT: none` exit 0 (§4), and the re-run of the pin/drift legs at the
  settled bytes (`/tmp/mori-r10-note/cycle2/cycle2.log`).

Instruments and raw logs: `/tmp/mori-r10-note/`. A reader re-running any leg must re-check the
census SHA first.

scope: detection and report only. This seat wrote no lane file but this note; no remediation,
kill, restart or config change; fixtures, snapshots and baselines under `/tmp`. The lane's own
committed baseline is the receipts-writer's artifact (§4).

## 1. Design at `d7710981…`

The round-9 verdict registered this as the last carried freshness item: *"a committed
behavioral baseline plus a `--drift` mode with a declared volatile-fields list, so census
behavioral drift is itself detected"* (`SCORECARD.md:475-478`). Rounds 2–9 relied on seat
discipline to notice a census behavioral regression; nothing in the lane could see one.

Contract (declared in the file header, `tools/mori-census.sh:145-188`; usage `:330-348`):

| element | behavior | site |
|---|---|---|
| `--pin <path>` | runs the live census read-only, normalizes its **full** output, writes `<path>`; records `census_sha256`, `pinned_ts` and the `volatile_fields` list in the file header. Write failure → exit 2. Success → `MORI_PIN: ok path=…` exit 0 | `run_pin` `:1795-1812` |
| `--drift <path>` | runs the census, normalizes with the **current** script's list, byte-compares against the baseline: equal → `MORI_DRIFT: none` exit 0; differ → `MORI_DRIFT: <changed non-volatile field names>` exit 1; baseline missing/unreadable/malformed → exit 2. Writes nothing | `run_drift` `:1815-1878` |
| both without a path | `die_usage`, exit 2 | `main` `:2811-2812` |
| precedence | `--selftest` > `--pin` > `--drift` > live | `main` `:2806-2833` |

Design decisions that carry weight:

- **The pin's exit code is not the census's roll.** `run_pin` records the roll inside the
  canonical block (`MORI_CENSUS: DRIFT (findings=<V> …)`) and exits 0 — pinning a DRIFT host is
  still a pin. Measured at both revisions: my pin at 22:06:01Z (`1ddb7ff8…`) wrote a 5614-byte
  baseline (`/tmp/mori-r10-note/cycle/baseline.txt`, sha `a03c1b9d…`), and at 22:14:09Z
  (`d7710981…`) another 5614-byte baseline (`/tmp/mori-r10-note/cycle2/base.txt`, sha
  `62adad5d…`), each on a host whose census rolled DRIFT, each exit 0.
- **Normalization is one `sed` pass over a here-string** (`drift_normalize` `:1652-1667`), and
  the census output is captured into a variable first (`cap_census` `:1673-1678`, `set +e`,
  rc kept). No consumer reads a live pipe in this section — the r9 flake class
  (`corpus/knowledge/selftest-flake-r9.md`) is avoided by construction, not by luck.
- **The comparison is behavioral, not revision-bound.** `census_sha256` is informational; a
  revision whose canonical output is identical reports `none`. Measured three times: the
  selftest's own mutants carry a *different* `SCRIPT_SHA256` yet are graded on output alone; at
  `d7710981…` (a revision landed after my `1ddb7ff8…` pin) `--drift` against the
  `1ddb7ff8…`-pinned **committed** baseline returned `MORI_DRIFT: none` exit 0 (§4); and the
  `d7710981…` addition (comparing the baseline's recorded volatile list) is itself reported only
  when the list differs — the two revisions' lists are identical, so `none` is the correct
  answer there, not a swallowed change.
- **Reporting grammar** (`drift_report` `:1749-1792`, `drift_field_report` `:1724-1742`,
  `drift_scan` `:1701-1717`, `drift_line_id` `:1683-1692`): three passes — exact-line multiset
  match, then same-id pairing (`SURFACE:<name>`, `FINDING:<id>`, `VERDICT`, `HEADER`) naming
  changed keys / `-key` / `+key`, then added lines. A difference that lives *outside* key=value
  tokens (a state word, command text, the roll) falls back to naming the line's id; a pure
  reorder is named `output-order`; a changed volatile contract is named `volatile_fields`.
  Tokens are sorted `-u` and space-joined, so the report is deterministic.
- **The default path is untouched**: no `run_census`/`emit_*` edit in the diff, so the
  no-flag output is the r9 bytes' output (the oracle's frozen wants and the receipts' key-set
  diff are the round's proof of that; not this seat's measurement).

## 2. The volatile contract, and why each class is in it

The masked set is recorded **verbatim in every baseline header** (`# volatile_fields=…`), which
is what makes the "none" auditable: the file says what was not looked at.

Six special rules plus a counter list (`DRIFT_VOLATILE_SPECIAL` `:1647`,
`DRIFT_COUNTER_KEYS` `:1636-1645`):

| class | fields | why (measured) |
|---|---|---|
| timestamps / ages | `ts`, `age_s`, `mtime_age_s`, `*_epoch`, `mem_peak_anchor` | pure functions of the reading clock; two live runs 69 s apart differ in all of them |
| gauges (decimals) | `psi_some_avg10`, `psi_full_avg10` | PSI averages move with host load |
| rates | `io_avg_since_boot` (`N Bps/up s` pair; **device names kept**) | since-boot average moves every second; the device identity is *not* masked, so a device change is drift |
| counters / gauges / flags | the `DRIFT_COUNTER_KEYS` list: `pids state_rounds* state_lag state_ahead state_cmp wave tallies journal counts cgroup gauges mem_peak lane/tmux counts verdict tallies DISK sizes rowb_files …` | host-state observations, not gate behavior |
| compounds | `state_val_unread_reasons` (`file:N symlink:N dir:N other:N`) | same, as one token |
| stamps | `script_sha256`, `example` | the revision is deliberately not compared; the row-B example path is an inference artifact |

Measured rationale (this is the part a future editor must not lose):

- **Live output cannot be a baseline raw.** Two live runs 69 s apart at the entering bytes differ
  on 5 of 79 field tokens and on essentially every line (`/tmp/mori-r10-note/live-{1,2}.out`;
  the lessons-distiller's independent 72 s pair measured 6 of 79 tokens and 32 of 33 lines —
  `corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md` §1). The churn is the
  host's clock and counters, not gate nondeterminism: a fixture with pinned inputs is
  byte-identical (same lesson §1).
- **A short-window mask is not enough, so the list is class-based, not window-based.** The
  lesson's longer datums: the journal `segfault=` count moved `104 → 225` over ~69 min, and
  `mem_peak=`/`mem_peak_anchor=` moved within ~7 min when the cgroup instance was recreated
  (same lesson §4). Both are masked here — `segfault` and `mem_peak` are in
  `DRIFT_COUNTER_KEYS`, `mem_peak_anchor` is a special rule — so a baseline pinned in one quiet
  window does not go red inside the hour on a host episode.
- **Holdout, three independent same-env pairs** (my extraction of the shipped `drift_normalize`
  applied to live captures from three different seats' windows: `/tmp/mori-r10-note/holdout.sh`):
  my pair (69 s), the volatile-spec pair (~1 min), and the lessons-distiller pair (21:50→21:52Z)
  all normalize **CLEAN** — the rules hold outside the window they were derived on.
- **What is deliberately NOT masked** — the code constants and contract words, so that editing
  one is detectable drift: `stale_threshold_s=900`, `threshold_s=7200/900`, `warn_pct=85`,
  `crit_pct=95`, `psi_warn_avg10=10`, `window_s=900`, `severity=`, `basis=row-*`, `rc=`, `log=`,
  `psi_source=`, `mem_peak_source=`, `io_basis=`, `targets=`, `cmd=`, and the `VERSION` token in
  the header line. Measured in my own baseline: those six threshold fields are present unmasked
  next to 26 `<V>` masks. `idle_warn_s` and `gate_s` are in the same class by the mask rules
  (no rule covers them) but were not present in my captures — this host's tmux row is
  `unavailable` and no lane row reached the young/row-8 arm — so their unmasked state is read
  off the rules, not measured.
- **Shape is checked even where magnitude is masked.** The rate rule matches
  `[0-9]+Bps/[0-9]+s`, so a *malformed* rate (a probe that starts emitting `dm-0:garbage`) does
  not match the mask and surfaces as drift; a wrong magnitude inside the masked shape does not.

## 3. The masking risks — over (false green) and under (false red)

**Over-masking (a real regression reads as `none`).** Every masked field is a blind spot; these
are the ones that matter, in the order a reader should care:

1. **Counter magnitudes inside an existing finding id.** `count=<V>` is masked, so a
   `count=1 → count=5` shift inside `KILL_SIGNAL_JOURNAL`, or a `size=`/`rowb_files=` shift, is
   invisible: both canonical lines are equal, so `--drift` says `none`. This is a design
   consequence of the mask + byte comparison (read, not run) and the sharpest hole in the
   design — the honest trade-off of masking counters. It is bounded by the fact that
   *appearance/disappearance* of a finding id is still caught (`-FINDING:<id>` /
   `+FINDING:<id>`), so a regression that *adds or drops* a finding is visible while one that
   only moves a magnitude is not.
2. **Watermarks and gauges** (`mem_peak`, `current`, `host_mem_avail_pct`, `psi_*`, the since-boot
   rate): a probe that misreads a counter (wrong field, wrong divisor) keeps the masked shape and
   is invisible. The disk case is partially covered because the device name is outside the mask.
3. **`*_epoch`** (the launch anchor) and **`round=`**: a lane's lifecycle state can move without
   the row's `basis=`/state word changing; the row's *state word* and `basis` are the visible
   signals.
4. **`example=`**: the row-B inference's example path is masked, so the specific file behind an
   `attribution=inference` row is invisible (the `basis=row-B` token and the finding set remain).
5. **`script_sha256`**: by design — the pin compares behavior, not revision. A comment-only edit
   is `none`; so is a code edit that changes nothing observable.
6. **The verdict tallies** (`findings= drift= unavailable= surfaces=`) are masked. They are
   functions of the emitted line multiset, which *is* compared, so masking them costs little —
   but it does mean the roll's arithmetic is not independently checked.

**Under-masking (churn reads as drift, i.e. a baseline that cries wolf).**

1. **Episodic churn is the reason the list is class-based** (§2); a mask derived only from a
   quiet window would miss it. The residual risk is a churn field that is *not* class-obvious:
   the state/contract tokens listed as unmasked in §2 (`rc=`, `log=`, `psi_source=`,
   `mem_peak_source=`, `io_avg_unavailable=`) change legitimately when the host's state changes
   (a tmux server appearing flips `rc=1 → rc=0`; a device disappearing adds an
   `io_avg_unavailable=` entry). Those reports are *baseline aging*, not masking failure — the
   answer is the re-pin policy (§5), not a wider mask.
2. **The environment is not recorded in the baseline.** Measured: a 9-lane-roster capture and a
   1-lane-roster capture of the same host normalize to 12 changed lines under the shipped rules —
   the ten lane rows (nine in one capture, `lane.mori` in the other) plus the silence row on both
   sides; notably *not* the verdict line, whose tallies are masked
   (`/tmp/mori-r10-note/holdout.sh`, the "cross-seat" pair). So a baseline pinned with one
   `MORI_ROSTER_LANES` (or another `MORI_*` override) and drifted with another reports drift that
   is an env difference, not a behavior change. The baseline header records `census_sha256`,
   `pinned_ts` and the volatile list — **not** the env; the invocation (hence the env) must come
   from the receipt's re-run recipe. This is the one place where a reader could be misled by a red
   baseline.
3. **Direction of safety.** Between a false green and a false red, this design prefers the false
   red: a drift report is a named artifact a human inspects, while a false `none` defeats the
   pin's purpose. The list is therefore key-scoped and conservative, and the *masked set travels
   in the artifact* so the reader can see the blind spot.

**Two mask-shape experiments of my own** (`/tmp/mori-r10-note/`, at the entering bytes):
a key-scoped mask caught both a threshold mutation (`DISK_WARN_PCT 85 → 86`, named
`warn_pct=85/86`) and a renamed finding id; a **digit-blanking** mask (blank every `[0-9]+`)
both corrupted a *key name* (`script_sha256` → `script_sha<N>`, destroying the field contract)
and would have hidden the threshold change. Masking by value-shape rather than by key is how a
drift pin turns vacuous.

## 4. The adopted lane baseline (receipts-writer's artifact)

| fact | value |
|---|---|
| path | `corpus/evidence/baseline-r10-20261015T2210Z.json` |
| baseline sha256 | `bdf464968003ed48014ea8da23045a5112628dbf11cc164755fbdff0af4c5649` (6779 B, 39 lines) |
| header `pinned_ts` | `2026-10-15T22:09:37Z` (the census run's own clock) |
| header `census_sha256` | `1ddb7ff8cc71eebd71fd3bb10e8f98c4793199e925dd196b552e0ebc68a9cd3c` |
| file mtime | `2026-10-15T22:10:11Z` (filename stamp `20261015T2210Z`) |
| written by | `bash tools/mori-census.sh --pin corpus/evidence/baseline-r10-20261015T2210Z.json` → `MORI_PIN: ok`, exit 0 |

The file is the `mori-drift-baseline v1` **text** format (header comments, a
`# --- canonical output follows ---` marker, then the masked canonical output). Despite the
`.json` suffix it is not JSON — a reader reaching for `jq` will fail; the suffix is a naming
observation, not a defect in the contract.

My own check of the committed artifact (not the receipts-writer's): at `d7710981…`, i.e. a
revision landed *after* the pin, `bash tools/mori-census.sh --drift
corpus/evidence/baseline-r10-20261015T2210Z.json` → `MORI_DRIFT: none`, exit 0 (22:12:12Z).
That is the design's central claim working on a live case: the census bytes moved, the
normalized output did not, so the pin reports *behavioral* stability rather than flagging the
revision. It also means the committed baseline remains valid across that revision — and the
`d7710981…` addition (comparing the baseline's recorded volatile list) reports nothing here,
correctly, because the two revisions declare the same list.

The round's hermetic leg at the settled bytes is the selftest:
`bash tools/mori-census.sh --selftest` → `MORI_CENSUS_SELFTEST: PASS (66 cases, 66 passed,
0 failed)` exit 0 (10 of the 66 are the r10 pin/drift cases, `tools/mori-census.sh:2722-2798`;
`/tmp/mori-r10-note/selftest-at-settled.out`).

Re-run recipe (cwd = lane root; the same invocation shape the receipts use, default env):

```sh
sha256sum tools/mori-census.sh                    # 1ddb7ff8… is the sha the baseline's header records
                                                  # (d7710981… also drifts `none` against it — measured)
sha256sum corpus/evidence/baseline-r10-20261015T2210Z.json   # bdf46496…
bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2210Z.json
#   expect: MORI_DRIFT: none  (exit 0) while the fleet state is unchanged in the
#   unmasked fields; a red result names the changed keys, e.g.
#   MORI_DRIFT: basis  /  -FINDING:WATCHDOG_ABSENT  /  +FINDING:DISK_CRITICAL
#   /  volatile_fields (the baseline was pinned under a different masked set)
bash tools/mori-census.sh --pin /tmp/<new>.txt     # re-pin deliberately, with a reason
```

## 5. Recommended admission ritual

1. **Pin on admit.** Immediately after the round's acceptance battery passes, at the admitted
   census bytes, on the live host: `--pin corpus/evidence/baseline-r10-<STAMP>.json`; record the
   path, the header `pinned_ts`, the baseline sha256 and the pinned `census_sha256` in the
   verdict. (That is exactly what round 10 did; §4.)
2. **Drift before each new round.** The first measurement of a round is
   `--drift <the lane baseline>`. A red result is a **named finding in the round's before-state**,
   not something to silence: it either explains an intended change (then re-pin, §3) or is a
   regression the round must address. The failure mode to avoid is re-pinning to make red green —
   the same rule as weakening an oracle's assertions
   (`corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md`, "Applying it" §3).
3. **Re-pin only as a recorded act with a reason.** Baseline aging is expected (a wave settles, a
   lane launches, a tmux server appears). The reason and the new SHA go in the round record.
4. **Keep the baseline in-repo, with the raw capture alongside.** The baseline belongs in
   `corpus/evidence/` so it travels with the lane and is reviewable in the diff; the artifact a
   human reads should be the raw capture (the mask is a *reading*, not a *record* — the r9
   `OUT_FILE` principle).
5. **Run the whole drift battery in the acceptance battery**, because a pin that only passes the
   first leg proves nothing about masking: pin → drift immediately (`none`); drift after ≥60 s of
   live churn (`none` — proves the list absorbs churn); drift from a one-field mutant (exit 1
   naming the field); drift on a missing path (exit 2); and, since `d7710981…`, drift against a
   baseline whose volatile list was rewritten (exit 1 `volatile_fields`). The selftest carries
   these arms (`tools/mori-census.sh:2722-2798`; `PASS (66 cases, 66 passed, 0 failed)` exit 0 at
   the settled bytes, `/tmp/mori-r10-note/selftest-at-settled.out`), and my own cycles reproduced
   them at both revisions (`/tmp/mori-r10-note/cycle/cycle.log` at `1ddb7ff8…`;
   `/tmp/mori-r10-note/cycle2/cycle2.log` at `d7710981…`):
   `--pin` rc 0 / `--drift` rc 0 `none` / 70 s later rc 0 `none` /
   renamed-finding mutant rc 1 `MORI_DRIFT: +FINDING:WATCHDOG_STALE_X -FINDING:WATCHDOG_STALE` /
   one-field mutant rc 1 `MORI_DRIFT: warn_pct` / rewritten volatile list rc 1
   `MORI_DRIFT: volatile_fields` / empty, junk and mode-000 baselines rc 2 `malformed`/`unreadable`.
6. **Cost.** `--drift` is a full live census (~30–45 s wall on this host at wave load), so the
   ritual is per-round, not per-commit. Pin and drift must use the **same invocation** (same
   `MORI_*` env): §3.2 is the measured reason.

## 6. What this note does not claim

- No remediation, kill/restart, host-config change or git commit; every fixture, snapshot and
  baseline of my own lives under `/tmp`; the only lane file this seat wrote is this note.
- The census moved twice while this note was being written (`1ddb7ff8…` → `d7710981…`; the
  second revision adds the baseline-volatile-list comparison and one selftest arm). The design
  claims are read at the settled `d7710981…`; the behavioral legs were run at `1ddb7ff8…` (full
  cycle) and re-run at `d7710981…` (selftest, the committed-baseline drift, and the pin/drift
  legs). A reader re-running §5.5 must re-check the SHA: a later revision that changes the
  volatile list would move these line numbers *and* is reported by `--drift` itself as
  `volatile_fields`.
- The volatile list is a measured contract for **this host at these clocks** (windows 69 s – 69
  min, three seats' captures). It is not universal: another host must re-derive it, and the
  list's own derivation record is §2, not the code.
- The pin sees the census's **output** only. It cannot see internal logic that changes no output,
  a masked magnitude (§3.1), or a code path the pinned environment never exercises (tmux is
  `unavailable` on this host, so the tmux rows' masked counters are unexercised).
- The lane baseline and the receipts are the receipts-writer's artifacts; this note cites them
  and adds one independent drift reading of its own, not their verification.

## Erratum (round 12, 2026-10-19) — dead baseline path in §3 recipe

The path `corpus/evidence/baseline-r10-20261015T2210Z.json` named at lines 195, 200, 209, 226
and 227 above does not resolve at any committed revision (`ls corpus/evidence | grep -c 2210Z`
→ 0; audit finding F03, `corpus/knowledge/audit-r11.md`). It was the round's interim pin,
deleted during receipt regeneration. The adopted baseline is
`corpus/evidence/baseline-r10-20261015T2231Z.json` (header `census_sha256=d7710981…`,
`pinned_ts=2026-10-15T22:26:29Z`). Re-run recipe: `MORI_SHOKUNIN_ROOT=<fleet root> bash
tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json`. At
2026-10-19 it reads red (exit 1); every token is classified in
`corpus/evidence/drift-r12-20261019T2204Z-classification.md` — no census regression; new boot,
souji sweep `e20f4fa`, aggregator evidence row-B → row-C. The text above is kept as filed.
