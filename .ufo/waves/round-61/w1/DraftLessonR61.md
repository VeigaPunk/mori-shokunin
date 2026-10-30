# Draft — mori round 61 lesson (skeleton; the L1 owns the final file)

**Status:** draft only. Produced by seat `Mo61ScribeLesson` (scribe, leaf) at wave w1.
The L1 integrates this into `corpus/lessons/round-61.md`; nothing here is committed
by this seat. Amendments to the frozen contract or counters are barred — the
findings below are routed, not applied.

Round 61, L1 `MoriR61`. Entering revision `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`;
freeze `7370a731abcafc4c803111de7c22cd6264d63be1` (controls + selftests committed
pre-dispatch; pre-seat amendments 1–2 recorded in `.ufo/waves/round-61/contract.md`).
Claims: C1 calibration (gate registry r52–60, 25 manifest paths), C2 freshness (PSI
v7.3 recheck ledger), C3 operability (counter execution boundary v2).

---

## Gate

### Candidates considered

Six new registry rows, one per pinned v7.3 copy opened this round. Each candidate
below is measured: the URL was re-fetched at tag `v7.3` and byte-compared against the
committed copy (MATCH for all six), the sha256 equals the pin frozen in
`.ufo/waves/round-61/count-c2.py:30-37`, and the quote is a byte-located span of that
pinned copy (≤25 words, ≥8 distinct bytes).

| id | file | URL (tag v7.3) | opened | sha256 | located quote (line range in the pinned copy) |
|---|---|---|---|---|---|
| S565 | `Documentation/accounting/psi.rst` | `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/accounting/psi.rst?h=v7.3` | 2026-10-30 | `11c6b712…b82692` | :37–38 — "Pressure information for each resource is exported through the respective file in /proc/pressure/ -- cpu, memory, and io." |
| S566 | `kernel/sched/psi.c` | `…/plain/kernel/sched/psi.c?h=v7.3` | 2026-10-30 | `c4edc1e7…85ec63f` | :1282–1283 — "/* CPU FULL is undefined at the system level */ if (!(group == &psi_system && res == PSI_CPU && full)) {" |
| S567 | `include/linux/psi_types.h` | `…/plain/include/linux/psi_types.h?h=v7.3` | 2026-10-30 | `483269b2…b3618ccc` | :50–56 — "/* Pressure states for each resource: SOME: Stalled tasks & working tasks FULL: Stalled tasks & no working tasks */" |
| S568 | `Documentation/admin-guide/cgroup-v2.rst` | `…/plain/Documentation/admin-guide/cgroup-v2.rst?h=v7.3` | 2026-10-30 | `2750c11a…2611b68` | :1073–1074 — "This control attribute is not hierarchical, so disable or enable PSI accounting in a cgroup does not affect PSI accounting in descendants" |
| S569 | `init/Kconfig` | `…/plain/init/Kconfig?h=v7.3` | 2026-10-30 | `d37de2a1…77e0d` | :736–737 — "If you say Y here, the kernel will create /proc/pressure/ with the pressure statistics files cpu, memory, and io." |
| S570 | `Documentation/admin-guide/kernel-parameters.txt` | `…/plain/Documentation/admin-guide/kernel-parameters.txt?h=v7.3` | 2026-10-30 | `b5a13c03…4cb39a` | :5540–5542 — "psi= [KNL] Enable or disable pressure stall information tracking. Format: <bool>" |

Fetch log: `.ufo/waves/round-61/w1/Mo61ExecFetch.md` (six `MATCH` verdicts, one URL
and sha256 per file, access times 2026-10-30T05:16:47Z–05:16:50Z).
Quote-location receipts: this seat's report
`.ufo/waves/round-61/w1/Mo61ScribeLesson.md` (per-file `in_hay=True`, word counts
11–24, distinct-byte counts 25–37, sha256 == pin for all six).

### Admitted

- **Admit S565–S570 (tier A, code/docs, one row per pinned v7.3 copy).** Opened
  2026-10-30; each row's anchor cell cites the tag, the line ranges used above, the
  sha256 and the committed copy path `corpus/evidence/sources-r61/<file>`; status
  `mined`; recheck `on-release`; used-by `corpus/knowledge/psi-v73-recheck-r61.md`.
  Reason: these six copies are the only artifacts the C2 ledger's quotes can be
  byte-located in, and `count-c2.py`'s `rows_src` arm requires, per cited copy, a
  SOURCES row naming the copy path, `mined`, and used-by the ledger entry.
  Measured constraint on the row text (scratch mirror of the lane corpus, census
  validator run against the mirror, exit code recorded):
  - the six rows must sit **inside the `## Registry` section** — appending them after
    the last section yields `E12 <id> row outside Registry section` per row;
  - `used-by corpus/knowledge/psi-v73-recheck-r61.md` must **exist on disk** when the
    census runs — with the ledger entry absent, all six rows raise
    `E11 <id> missing used-by corpus/knowledge/psi-v73-recheck-r61.md`;
  - the six rows must **not reuse the scope text** of the round-55 v7.3 twins
    (S529–S533): same URL + same scope raises
    `E04 <id> duplicate url … within scope …` and turns the lane's census exit
    code to 1; with distinct scope text the same URLs raise only
    `W04 duplicate url … across scopes` (a warning that does not change lane status).
  Measured census result with the six rows inserted at the end of the `## Registry`
  table and the ledger entry present: exit 0, 0 E-codes, 343 rows
  (337 + 6), W-codes 25 → 30 (the five new W04s; S569's `init/Kconfig?h=v7.3` URL
  has no earlier row, so it produces none).

### Rejected / not admitted

- **The round-55 v7.3 twin rows are not re-admitted as this round's rows.** S529
  (psi.rst), S530 (psi.c), S531 (psi_types.h), S532 (kernel-parameters.txt) and
  S533 (cgroup-v2.rst) already carry five of the six v7.3 URLs with sha256s
  byte-identical to the count-c2 pins, opened 2026-10-27, used-by
  `corpus/knowledge/kernel-v7.3-recheck-r55.md`. They are not this round's rows:
  the contract's C2 target requires a row opened this round whose `used-by` names
  this round's ledger entry, and their copy paths are `corpus/evidence/sources-r55/…`.
  Flip: they stay mined for their own entry; the new rows are scoped to the r61
  ledger and carry the r61 copy paths.
- **`init/Kconfig` at v7.3 has no earlier registry row anywhere in the lane**
  (grep over `corpus/` finds no v7.3 Kconfig row) — S569 is that file's first row,
  which is why it alone produces no duplicate-URL warning.
- **The `merge/mori` staged theme is not adopted.** The collisions file lists 94
  ids (S471–S564) and the staged theme's ids fall inside it; the contract's rule
  is mass id drift → L0 question + adopt nothing. The L0 question is raised in the
  fleet repo (commit `1aea7343`, "round-61: L0 question — merge/mori id drift
  (94 collisions), adoption closed this round"). Adoption this round: none.

### Registry sweep and census

- Pre-append census: 337 rows, `sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin mori` → exit 0, 0 E-codes, 25 standing W04s,
  `mori ok …/mori-shokunin/corpus/SOURCES.md` (receipt
  `.ufo/waves/round-61/w1/Mo61ExecCensusMid.md`; re-measured by this seat, same
  output and exit code).
- Post-append expectation (measured on a scratch mirror, not on the lane): 343
  rows, exit 0, 0 E-codes, 30 W04s, per the E04/E11/E12 constraints above.

### Quarantine slice (re-derived, 3 rows)

`.ufo/waves/round-61/assimilation/quarantine-slice` names S244, S262, S268.
Fresh verdicts from `.ufo/waves/round-61/w1/Mo61ExecQuarantine.md`:
S262 PRESENT (DOI `10.1109/TSC.2026.3698682`, abstract carrier OpenAlex, quote
located), S268 PRESENT (same work, publisher full-text anchor at
`corpus/SOURCES.md:257`), S244 PRESENT **via a DOI-matched companion preprint**
(arXiv 2403.18832) while the ACM version of record is still not fetchable.
Discrepancy for the L1 to reconcile: the round-59 lesson recorded S244 as
"unverifiable, not fabricated", and the contract says the quarantine verdicts are
"maintained"; the r61 re-derivation describes S244 as present through a companion
source rather than unverifiable. No row was fabricated and no registry change was
made; the "not fabricated" conclusion is unchanged.

### Spot-check material

≥1 admit (S565–S570) and ≥1 not-admit (the round-55 twins S529–S533, kept for their
own entry) are recorded above, so the non-author closure has material to re-open.

---

## Mistakes

One mistake is mined this round, out of the round-60 wave's defect record.

1. **class landing** · evidence: `.ufo/waves/round-60` dispatch — the round-60
   dispatch payload carried the invocation line but not the directive body, so the
   bytes did not land in what the seats received · captured-by: none — no round-60
   gate or seat checked the payload body; the wave-shape reviewer verified only
   that every task body *starts* with `/skill:godspeed`
   (`.ufo/waves/round-60/w1/Mo60Reviewer16.md:116`), and the defect surfaced only
   as a prose note in the round-60 lesson's wave section
   (`corpus/lessons/round-60.md:102-105`) · fix: embed + verify at dispatch time.

   Measured shape of the defect and of the fix:
   - round-60 dispatch commit `76904b21`: `.ufo/waves/round-60/build-w1-spec.py`
     at that commit built every prompt as `"/skill:godspeed\n" + text + BOUNDS`
     (line 31) — it never read the directive file, so **0 of 64** task bodies in
     `.ufo/waves/round-60/w1-dispatch.json` contain the directive body (checked at
     `76904b21` and at HEAD).
   - round 59's builder did embed it explicitly:
     `.ufo/waves/round-59/build-w1-spec.py:9` reads
     `~/.agents/skills/godspeed/directive.md` and line 139 prepends it; the r59
     dispatch payload carries the body in **64 of 64** task bodies.
   - the round-60 lesson's own attribution ("this round's spec builder relied on
     renderer injection that did not happen") is not what the bytes show: the r60
     builder contained no renderer-injection path at all — it simply omitted the
     embed. The correction belongs to the r60 lesson's own wave-section prose; the
     bytes, not the renderer, are the cause.
   - the builder fix landed only in the later round-60 integrate commit
     `bc05a145` (adds the `GODSPEED` read and the `lead =` prepend), so round 60's
     wave shipped without the body and the fix only protects later rounds.
   - round 61 embeds and verifies at dispatch time: `.ufo/waves/round-61/build-w1-spec.py:57-69`
     reads `~/.agents/skills/godspeed/directive.md` and prepends it to every
     prompt; the r61 dispatch payload (sha256
     `c21329857418461e073dd71c7195cbc434d7d30ed57d5626f19220ba143c4121`, 99448 B)
     carries the directive body in **64 of 64** task bodies, checked by this seat
     against the committed file and independently by the wave's own dispatch check
     (`.ufo/waves/round-61/w1/Mo61ExecGodspeed.md`: `TOTAL tasks=64 ok=64 missing=0`).
   - residual gap for the next round (routed, not fixed here): the verification is
     performed by a seat reading the dispatch file, and the round-61 dispatch
     payload is still an **untracked** working-tree file
     (`git status --porcelain` shows `?? .ufo/waves/round-61/w1-dispatch.json`),
     whereas round 60's payload was committed with its dispatch. Until the payload
     is committed, the "verified at dispatch time" receipt is not reproducible
     from the repository. A committed, mechanically checked dispatch payload is the
     durable form of this fix.

---

## Wave w1

One v2 wave, 64 seats, one dispatch (`w1-dispatch.json`, sha256
`c21329857418461e073dd71c7195cbc434d7d30ed57d5626f19220ba143c4121`, 99448 B),
`w1.ready` present, `w1-dispatch.stderr` empty. Policy v2 band 64–128 applies
(`waveMinLanes 64`, `waveMaxLanes 128`, total 64 — at the band's floor).
Role mix measured from the dispatch payload: scribe 13, executor 12, scout 5,
connector 2, revenger 3, simplifier 2, reviewer 9, critic 7, mutation-tester 8,
sentinel 3 — total 64. Attack share (reviewer + critic + mutation-tester +
sentinel) = 27/64 = 42.2%, above the contract's ≥25%. No duplicate seat names; no
unknown role; every task body starts with `/skill:godspeed` and carries the
directive body.

Settlement: **pending** — no `.ufo/waves/round-61/w1-results.json` at the time of
this draft; 38 seat reports had landed under `w1/`. The L1 fills the settled count
and the `mori-settlement-scan.py` verdict after the wave settles.

### Per-claim verdicts (L1 fills from the wave's receipts)

- **C1 (calibration) —** pending: the 25-row registry draft, the dry-run against
  the freeze, and the frozen met line
  `C1=met gates=25 registered=25 missing=0 thin=0 dup=0 unres=0 noselftest=0 noowner=0 rev=<rev>`.
- **C2 (freshness) —** pending: the ledger with one row per enumerated pointer
  (47 pointers at the contract's floor 40), the provenance trio, the six mined
  SOURCES rows and the frozen met line
  `C2=met pointers=N rows=N quotes_ok=N spans_ok=N sources>=4 rows_src=ok provenance=ok failed=none`.
  Receipt already in hand: the control replay is byte-identical to the committed
  do-nothing receipt (`.ufo/waves/round-61/w1/Mo61ExecReplay.md`).
- **C3 (operability) —** pending: the repaired counter's own arms. The counter
  reads met against the lane repo (`--repo …/mori-shokunin`), but from the
  fleet-root cwd with the default `--repo` it prints
  `r60hole=FAIL … livepins=FAIL` because the r60 counter path does not exist in
  the fleet repo — see the wave's own C3 report
  (`.ufo/waves/round-61/w1/Mo61ExecC3Run.md`) and this seat's reproduction. The
  L1 should record which invocation form backs the claim.

### Instrument defects routed from this wave (frozen bytes stand)

1. C2's undocumented five-word quote minimum (`count-c2.py:136-139`) rejects a
   contract-valid short source line: the contract fixes only an upper bound of 25
   words and a lower bound of 8 distinct bytes
   (`.ufo/waves/round-61/w1/Mo61Reviewer05.md`, with a measured false negative).
   Routed to round 62; the counter is frozen for this round.
2. C2's selftest receipt is not reproducible at the default floor: with the
   default `--floor 40` the selftest prints `C2_SELFTEST pass=9 fail=1` (the
   synthetic good case carries six pointers and fails `pointer_floor:6<40`), while
   `--floor 6` gives `pass=10 fail=0` — i.e. the committed selftest receipt
   implies a floor override the frozen command line does not carry
   (`.ufo/waves/round-61/w1/Mo61ExecReplay.md`; reproduced by this seat).
3. The r61 dispatch payload is untracked, so the dispatch-time verification
   (Mistake 1's fix) is not yet reproducible from the repository.

### Non-author spot-check material

≥1 admit (S565–S570) and ≥1 not-admit (S529–S533) are recorded in `## Gate`.
