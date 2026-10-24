# Round 6 log-entry draft (scribe seat, goal wave)

Integration target: append as a `## Round 6 — … (goal wave)` entry at the end of `LOG.md`
(parent-owned; append-only — nothing above the new section changes). `[PARENT: …]` marks
what only the integration commit/acceptance can bind; `[PENDING: …]` marks values unlanded
at this draft's clock (v3, 2026-10-15T19:07Z; v1 was a stale partial from the interrupted
dispatch).

---

## Round 6 — R1 stdout-backchannel + R2 content-keyed forgery closed (goal wave)

**Round 6 — goal-wave admission (2026-10-15).** Motivating evidence: the round-5
correction (`SCORECARD.md:264-273`; `corpus/knowledge/verdict-machine-r5.md` §4) — two
residuals at `7143ccc2…`: (R1) a census reads the run header (`SHUFFLE_SEED`/`RUN_NONCE`/
`CASE_ORDER`) from the oracle's own stdout via `/proc/<ppid>/fd/1` mid-run (and the pinned
seed from `/proc/<ppid>/environ`) and replays by position — 28/28 exit 0; (R2) a memorized
content→state table passes because the nonce binds no fixture content — 28/28 exit 0.
Scribe re-measured both first-hand before the impl landed (18:45–18:47Z: R1 leak 28/28 +
header readable 29/29 mid-run, pinned seed readable 29/29, seed-reader pinned 28/28; R2
stale 28/28 and a fresh memorizer 28/28; fixture fingerprints run-invariant, nonce in
content 0/29; scratch `/tmp/mori-scribe-r6/before2/`). Landed (evidence commit `[PARENT]`):
oracle `3307761a…` (1082 lines; +133/-24 vs HEAD; the receipts-writer's final set was
re-captured at these same `3307761a…` bytes, 19:12–19:13Z) — run header printed only AFTER
the case loop (`:1070-1072`); pins removed from the process tree by a one-shot re-exec
before any census runs (`:207-221`; the revision records that a runtime `unset` does not
scrub `/proc/<pid>/environ`); per-run `RUN_SALT` (never printed, never pinnable) woven into
fixture bodies/commit messages plus salt/blob files (`:239-240`, `:309-315`, `:417-419`);
FAIL texts redact the nonce token (`:545`). Census `af2d4e79…` frozen and verified
unchanged (oracle-only round); registry (`CASE_IDS`, want args) byte-identical. Mid-wave,
an intermediate revision `e64cc067…` still exposed the pins via environ (29/29; seed-reader
28/28 — measured by the scribe battery); the landed revision closes it (environ-pinned 0/29;
seed-reader pinned 1/28). Artifacts landed: seven receipts
`corpus/evidence/backchannel-r6-20261015T191216Z-{oracle-1,oracle-2,oracle-3,selftest,live,attack-r1,attack-r2}.log`
(before-legs at `7143ccc2…`; per-leg addenda with tallies), note
`corpus/knowledge/verdict-machine-r6.md`, lesson
`corpus/lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md`, SKILL row
(`SKILL.md` working tree sha `35c67fd4…`), `corpus/evidence/README.md` index rows and
`corpus/README.md` rows. Wave:
`[PARENT: bind wave record — batch shape, seat completion/loss counts, any backfill]`.

**Parent acceptance (`[PARENT: r6 timestamp]`).** Scribe pre-acceptance battery at
`3307761a…` + frozen census (receipts-writer's final set at the same `3307761a…` bytes):
selftest 30/30 exit 0; honest oracle 28/28 exit 0 across two fresh seeds and two pinned
runs, sorted grade tuples byte-identical to before (sha `a70af583…`), pinned pair
byte-identical stdout (receipts oracle-1/2/3 agree; header at lines 29–31, last case 28);
R1 leak 0/28 exit 1, seed-reader pinned 1/28 exit 1, fd1 mid-run header hits 0/29, environ
pinned 0/29 (receipt legs all 0/28); R2 stale 0/28, fresh unpinned 0/28 and same-pin 0/28,
nonce-normalizing variant 0/28 (receipts), fingerprints share 0/29 across runs; nonce in
fixture content 28/29 (exception `repo-missing-unavailable`). `[PENDING: parent re-runs
above + live census; bind figures]`.

**Verdicts.** `[PARENT: bind admission]`. Expected on the evidence:
**ADMIT-with-correction** — both registered residuals are closed for the enumerated/naive
classes at the landed bytes with the honest census unharmed, but two wider channels survive
and are named with witnesses (note `verdict-machine-r6.md` §4/§5.3): (1) the full-grammar
pattern-normalizing memorizer `6b79f776…` reaches `28/28` exit 0 (four seats agree);
(2) a pin in a *surviving ancestor's* exec-time environ reaches `28/28` under the
wrapper/CI pattern (the plain `env VAR=… bash oracle.sh` prefix is closed). Fix directions:
semantically varying content (r5 countermeasure #1, still unapplied) and entropy that never
transits any environment. Per-axis before→after: SCORECARD Round 6 section (draft in this
directory).

**Boundaries held.** Detection/report only; no remediation/kills; fixtures `/tmp`; seats
committed nothing; parent integrates under the mori identity; fleet root read-only for
seats.

Round report: `[PARENT: path, likely .ufo/reports/round-6/mori-goalwave.md]` · Verified
lane rounds: `[PARENT: 5 → 6]`.

---

## Scribe worksheet — what each `[PENDING]` binds to (delete/ignore at integration)

| Pending | Filled from |
|---|---|
| receipts/note/lesson/README rows | directory listings of `corpus/evidence/`, `corpus/knowledge/`, `corpus/lessons/`; `git status`/`git diff --stat` |
| parent acceptance block + admission | parent only — never scribe |
| wave record | parent |
| note's residual class | `corpus/knowledge/verdict-machine-r6.md` (watcher armed; scribe will fold in if it lands before handoff) |