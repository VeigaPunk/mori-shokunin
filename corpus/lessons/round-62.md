# Round 62 — mori (L1 MoriR62, attempt 2, recovery of the pre-seat freeze)

author: mori L1 (MoriR62)
round: 62
date: 2026-10-31
entering: `2f5b0626`
inherited freeze: `43cfbb10` + pre-seat amendments `56b47179`, `6d98b5cd`

Recovery: the prior r62 attempt (2026-10-30 15:43 -03) froze the round pair
pre-seat — `count-c1.py` (sound r61-ledger instrument: 1-word / ≥8-distinct-byte
quote floor over multi-line hay, statuses re-derived from the pinned v7.2/v7.3
byte copies, Registry-id binding via `ID_MAP`) and `count-c2.py` (probe
capability + sourced entry, blobrefusal, TOKEN_MAP, SCORECARD/SOURCES arms) —
plus `tools/mori-cgroup-pressure.py`, its fixture battery, the v7.2 pin
baseline, the entry `corpus/knowledge/cgroup-pressure-r62.md` (K1–K12) and a
Linux live receipt, then died before dispatching: `.ufo/waves/round-62/` held
only the counters and a census-start receipt — no wave, no dispatch, no
results. This attempt inherited the frozen bytes unchanged; pins re-verified
before reuse (sha256sum over the working tree: tool `aa5bfc37…` = PIN_TOOL,
cases `42551edb…` = PIN_CASES); no counter or contract edited; no wave
dispatched.

## Fresh start (r57–r61 rejected closures re-read; what was ruled out)

MANIFEST rounds 59–61 all `rejected-honest-stop`; §7 digests read. Spot-checks
run this round before declaring:

- r61 honest stop reproduced from the frozen counter:
  `python .ufo/waves/round-61/count-c2.py 986d4b46db6e67682ef84091f606d125f987ecbc`
  → `C2=unmet … failed=quote_words:` ×14, rc 1 — byte-for-byte the same 14
  anchors the r61 lesson names (`evidence/r61-counter-spotcheck.txt`,
  `.ufo/waves/round-62/evidence/`).
- r59/r60 cited evidence exists (`git cat-file -e` PRESENT:
  `986d4b46:.ufo/waves/round-59/evidence/control-c2-do-nothing.txt`,
  `b3c25613:.ufo/waves/round-60/evidence/c2-at-freeze.txt` — the latter shows
  the `C2=met` the r60 closure decertified).

Ruled out as r62 claims, and why: (1) re-declaring entry-claims-class depth via
the decertified r59/r60 instruments — the closures' verified met-flip
counterexamples stand and those bytes are frozen, so any `met` they print is
decertified by the lane's own record; (2) score moves without a closure-stated
number — no lane convention licenses an L1-authored scalar move (round-24/50
precedent); (3) claims resting on the old Linux host's live surfaces
(journalctl, cgroupfs, tmux, `/proc/pressure`) — absent on this Windows
workspace host; the honest reading here is `unavailable`, never zero (probe
receipt). The declared pair are the frozen new instruments built to the r61
lesson's routed fixes, each red at the entering revision (controls), each
measured at the data tip.

## Gate

S571 opened this round (fetched with `curl -sS -m 60` from the kernel.org plain
URL into scratch; sha256 `c4edc1e7c18ca76e6e29668093fa0b26d4251cb088f2d5feab24681f285ec63f`
byte-identical to the pinned copy `corpus/evidence/sources-r61/psi.c`; 1725
lines; all twelve K-claim anchors re-verified line-located against the fetched
bytes):

- S571 `psi.c` v7.3 — https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/kernel/sched/psi.c?h=v7.3 —
  opened 2026-10-31 — quote (psi.c:1251): "int psi_show(struct seq_file *m,
  struct psi_group *group, enum psi_res res)" (14 words).

Registry row S571 lands `mined`, used-by `corpus/knowledge/cgroup-pressure-r62.md`
(S568 stays the second entry source). Scope is the cgroup pressure interface —
a distinct scope from S566 (whole-file v7.3 recheck), hence the new row rather
than a used-by edit.

reject sample: none met

Census (validator): start receipt `evidence/census-start-r62.txt` (prior
attempt, Linux host, 2026-10-30, rc 0, 343 rows) → end receipt
`evidence/census-end-r62.txt` (this host, 2026-10-31, rc 0, 344 rows; W04
duplicate-URL warnings unchanged).

## Mistakes

1. class: freeze-time host assumption (CRLF) — both frozen counters'
   `--selftest` fail unaccommodated on this Windows workspace host: the
   selftests write their synthetic fixture files in Python text mode (CRLF on
   disk) and this host's user gitconfig sets `core.autocrlf=false`, so the
   throwaway repos' blobs hash differently from the LF pins — every ok=True
   arm fails `copy72_pin:`/`copy_pin:` (measured 2026-10-31 pre-data). The
   real-repo measurement path is unaffected (committed blobs are read via
   `git cat-file` and hash byte-exact). captured-by: this round's round-start
   host-portability check (run the selftests before trusting any verdict on a
   new host). fix (routed to r63 instruments; frozen bytes untouched this
   round): write fixture files in binary mode or compute pins over the written
   bytes; this round's selftests ran under a disclosed accommodation —
   `GIT_CONFIG_GLOBAL=<scratch>/gitconfig-crlf-true` (`autocrlf=true`, the
   selftest's throwaway repos only) — receipts
   `evidence/selftest-c1.txt` (15/15), `evidence/selftest-c2.txt` (8/8).
2. class: stale-host instruction — the r61 lesson's Mistakes item 5 fix names
   only a Linux path (`/home/vgpnk/...`) as the required misroot-free output
   root, and the frozen r62 census-start receipt's argv cites `/home/vgpnk/...`
   paths that do not exist here; same class as the 67 kasegi recheck lines (L0
   kasegi round-50). captured-by: the fresh-start host re-verification of
   carried instructions. fix: output-root rules must name the campaign root by
   role and resolve per host; r63 wave contexts must state the Windows
   workspace path explicitly when this host is the target.

Dispatch-surface disclosure (not a mistake, recorded for the closure): the
MISSION's ≥8-L2 batched AgentSwarm dispatch has no surface in this session (no
dispatch tool on this host). Round 62 ran L1-only; an L0 line is filed
(`mori | round-62 |` AgentSwarm surface absent — confirm waiver or supply the
surface); the PROVINCE host note records the shape with date. No wave-based
evidence is claimed this round.

## Wave

None — no dispatch surface on this host (disclosure above). The frozen pair
verifies over committed bytes; the round's evidence is controls + counters +
receipts run by the L1: do-nothing controls at entering `2f5b0626…` both unmet
(`evidence/control-c1-do-nothing.txt`, `evidence/control-c2-do-nothing.txt`);
C1 `met` and C2 `met` at the data tip (`evidence/c1-at-data.txt`,
`evidence/c2-at-data.txt`, measured-verdicts batch). Probe on this host:
selftest 12/12 rc 0, live `PRESSURE_UNAVAILABLE … absent=4` rc 2
(`evidence/probe-selftest-win-host.txt`, `evidence/probe-live-win-host.txt`).

## Assimilation

considerthese mined (2026-10-19…2026-10-26 files): the 2026-10-26 proposal 3
(re-execute what closures only evidence-verified) was partially executed by
this round's r61 counter spot-check — the exact shape it asks for; considered,
not formally adopted (a standing re-execution practice is beyond one round).
No other implementable proposal taken. Assimilation: none — shokuknow
unreachable.
