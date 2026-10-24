# mori round 6 — goal-wave report draft (scribe seat)

Integration target: the round report (idiom of `.ufo/reports/round-5/mori-goalwave.md`;
final path `[PARENT]`, likely `.ufo/reports/round-6/mori-goalwave.md`). Parent owns the
final path, the identity and the commit binding. Every figure is bound to a landed artifact,
a receipt, or a command run at a pinned SHA; `[PARENT: …]`/`[PENDING: …]` as elsewhere.

- Status: `[PARENT: completion statement + verified-round-count claim 5 → 6]`
- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Baseline: `848b3a6` (round-5 records; evidence `a420deb7`)
- Wave: `[PARENT: bind the wave record — batch shape, seat completion/loss counts, any backfill]`
- Report time: `[PARENT]`
- Draft status: **v6** by the scribe seat. Before-side at `7143ccc2…` (970 lines),
  18:45–18:47Z; after-side at the landed `3307761a…` (1082 lines), 19:07–19:08Z; the
  receipts-writer's final set pins the same `3307761a…` (captured 19:12–19:13Z); note and
  lesson figures at `b2ebe5e7…` (comment-only delta vs `3307761a…`, re-verified by three
  seats); census `af2d4e79…` frozen, sha-verified across every run. Scratch
  `/tmp/mori-scribe-r6/{before2,after2}/` (one-command battery `after2/run-all.sh`).

## Work performed

- Selected axis **operability** — close the two residuals registered as round 6's claim by
  the round-5 admission (`SCORECARD.md:264-273`): **R1 stdout-backchannel** (census reads
  the oracle's run header via `/proc/<ppid>/fd/1` mid-run and replays by position; plus the
  sibling pinned-seed `/proc/<ppid>/environ` channel) and **R2 content-keyed forgery**
  (memorized content→state tables).
- Registered claim: before — header prints secrets before the case loop and fixture content
  is nonce-free/run-invariant, so both attackers reach `matched=28 total=28` exit 0 with
  zero grading logic (measured); after — header prints only after the case loop and fixture
  content carries the run nonce/salt and varies per run, so both attackers fail while the
  honest census stays 28/28 exit 0 across shuffles with byte-identical tuples; registry
  byte-identical; census frozen (oracle-only round).
- Scribe measured the before-side first-hand, validated the fresh-memorizer chain at the r5
  bytes (finding and fixing its own generator defect: dropped census rc → 7 spurious
  `rc want=1 got=0` fails), then ran the full battery at the landed bytes.
- Mid-wave, the battery measured an intermediate revision `e64cc067…` with the pinned-seed
  environ channel still open (29/29 readable; seed-reader 28/28) — the landed revision
  replaced the ineffective `unset` with a one-shot re-exec and measures closed. Recorded,
  not dropped.

## Landed changes (evidence commit `[PARENT]`)

- `tools/mori-silence-cases.sh` → `3307761a…` (1082 lines; +133/−24 vs HEAD, plus
  comment-only polish): run header printed only AFTER the case loop (`:1066-1072`);
  one-shot re-exec when pins are present (`:206-224`; pipe fd `:211`, `exec bash "$SELF"
  "$CENSUS"` `:214`, drained `:219`); per-run `RUN_SALT` (never printed, never pinnable) in
  fixture bodies/commit messages/salt-blob files (`:239-240`, `:309-315`, `:417-419`) and
  the four untracked/dirty fixtures (`:823`, `:836`, `:899`, `:921`); FAIL fragments redact
  the nonce token (`:545`); nonce failure texts name no token (`:599`). Registry
  (`CASE_IDS`, wants) byte-identical.
- `tools/mori-census.sh`: **unchanged** `af2d4e79…` (frozen; sha verified before/after).
- `SKILL.md` working tree (sha `35c67fd4…`): r5+r6 contract row.
- `corpus/knowledge/verdict-machine-r6.md` (note-writer);
  `corpus/lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md`
  (lessons-distiller); `corpus/README.md` r6 rows + anti-sniff bullet; receipts + index rows
  in `corpus/evidence/README.md`.
- Receipts: `corpus/evidence/backchannel-r6-20261015T191216Z-{oracle-1,oracle-2,oracle-3,selftest,live,attack-r1,attack-r2}.log`
  (PINNED_SHAS oracle `3307761a…`, census `af2d4e79…`; before-legs at `7143ccc2…`).

## Before → after measurements

Before: scribe 18:45–18:47Z at `7143ccc2…` (validation sweep 18:55Z; receipts' before-legs
18:44Z; lesson/note before rows double-source). After: scribe 19:07–19:08Z at `3307761a…`;
receipts 19:12–19:13Z at the same bytes; note/lesson at `b2ebe5e7…` (comment-only
equivalent); census `af2d4e79…` both sides (sha-verified).

| Check | Before (`7143ccc2…`) | After (landed) | Exit |
|---|---|---|---|
| R1 header-leak census (stdout→regular file) | `28/28` | `0/28` (receipt `r1-redirect-r6` 0/28; note §3 0/28) | 0 → 1 |
| R1 fd1 mid-run header read | 29/29 invocations | 0/29 (lesson: empty at INV=1) | — |
| R1 environ probe, pinned seed (oracle surface) | 29/29 expose the seed | 0/29 (lesson: `seed=[]` from inv 1); receipt leg 0/28 | — |
| R1 seed-reader attacker (fd/environ) | unpinned `1/28`; pinned `28/28` | unpinned `1/28`; pinned `1/28` | 1 / 0 → 1 / 1 |
| R1 surviving-ancestor pin (wrapper pattern) | n/a | **`28/28` EXIT 0** — named residual (note §5.3; critic `EV-r1p-export.log`) | — |
| nonce tokens in oracle stdout of attacker runs | (r5 named `want=[nonce-N]`) | 0 | — |
| R2 stale content memorizer | `28/28` | `0/28` (receipt `r2-oldtable-r6` 0/28) | 0 → 1 |
| R2 fresh memorizer (learn one run, replay) | `28/28` unpinned and same-pin | `0/28` both modes (receipt `r2-fresh-replay-r6`; lesson 0/29 hits) | 0 → 1 |
| R2 nonce-only normalizer (receipts-writer) | n/a | `0/28` (receipt `r2-normalize-replay-r6`; lesson `44051479…` 0/29) | — |
| R2 bracket-grammar normalizer (note-writer) | n/a | `24/28` EXIT 1 — four discriminating cases (note §4) | — |
| R2 full-grammar pattern normalizer (`6b79f776…`) | n/a | **`28/28` EXIT 0** — named residual (note §4; lesson; critic `EV-norm2.log`) | — |
| fixture nonce in content (excl. dedicated artifacts) | 0/29 | 1–3 files per case (28/29 invocations; exception `repo-missing-unavailable`) | — |
| fingerprint F shared values across two runs | 29/29 identical (`929a5dc1…`) | 0/29 shared | — |
| honest census across shuffles | `28/28` exit 0 | `28/28` exit 0 ×2 fresh + receipt oracle-1/2/3; tuples sha `a70af583…` (same as before); header at lines 29–31 after last case | 0 |
| honest pinned pair | n/a (pins exposed) | `28/28` ×2, stdout byte-identical | 0 |
| selftest (frozen census) | `PASS (30 cases, 30 passed, 0 failed)` | `PASS (30 cases, 30 passed, 0 failed)` | 0 |
| live census | `[from r5 receipt]` | `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)`; 9/9 progressing; tmux unavailable | 1 |
| registry (28 ids/wants) vs HEAD | reference | `CASE_IDS`/wants byte-identical (note §2.3); 2 redacted failure messages | — |

Acceptance re-run at integration `[PARENT: re-run and bind — expect the after column; the
`6b79f776…` normalizer and the survivor-pin wrapper are expected to PASS as the named
residuals; battery: /tmp/mori-scribe-r6/after2/run-all.sh; re-run recipes:
`corpus/evidence/README.md` round-6 section]`.

## Corrections named (round 7 registered claim)

- **R1-class residual — surviving-ancestor exec-time environ pin** (note §5.3): a pin in an
  ancestor shell exec'd with it and alive for the whole run is outside the oracle's
  process surface; reaches `28/28` under the wrapper/CI invocation pattern (note-writer
  `G-r1-liveanc.out`; critic `EV-r1p-export.log`); the plain `env VAR=… bash oracle.sh`
  prefix is closed (measured both). Fix direction: entropy that never transits any process
  environment, or operator-owned private fd/file (parent's call).
- **R2-class residual — full-grammar pattern-normalizing memorizer** (`6b79f776…`, note §4;
  lesson): strips both annotation grammars and reaches `28/28` exit 0 with zero grading
  logic (four seats' agreement); the binding fix is r5's still-unapplied countermeasure #1 —
  make semantically relevant content vary per run so a memorized row is *wrong*, not merely
  stale.
- Intermediate-revision record: `e64cc067…` exposed the oracle's own environ pins (29/29;
  seed-reader 28/28), closed at `b2ebe5e7…`+ by the re-exec; no claim carried on the
  intermediate bytes.
- Carried unchanged: frozen-behavioral drift pin (`silence-cutover-r3.md:253-254`); row-6
  report-body presence-only residual (`silence-cutover-r3.md:250-252`); blocked-attempt
  receipt-binding and role-routing debts (`SCORECARD.md:128-131`).

## Axis and learning verdicts

Expected shape `[PARENT: bind]`: operability **improved** (registered classes closed, honest
census unharmed); coverage **unchanged** (registry byte-identical, census frozen); depth
**improved** (note + lesson); freshness **improved narrowly** (receipts + index rows);
calibration **improved** (multi-seat batteries; survivors named); adjacency **unchanged**.
Admission expected **ADMIT-with-correction** (two named wider channels, § above; round-5
precedent). Learning trends: expansion/quality **improved**, discernment **unchanged**.
Per-axis before→after evidence: `scorecard-verdict-draft.md` (this directory), to be
appended to `SCORECARD.md` by the parent.

## SHONEN

`[PENDING: mirror the round-5 report's SHONEN block — all `[ ]` at r5 (decision tables,
end-to-end task logged, executable without oral context, no cross-domain bleed; no named
non-author verifier); state whether r6 changes any]`

Boundaries held: detection and report only — fixtures under `/tmp`, no kill/pkill of real
processes, no systemctl or host config edits, no lane-side commits (parent integrates);
fleet root read-only for seats; oracle+census shas verified before/after every run.
`[PARENT: confirm from the integration diff]`