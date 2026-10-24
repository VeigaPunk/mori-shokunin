# Round 25 wave 1 — D2KnowledgeFix (knowledge entry correction sweep, claim C1 item D2)

Seat: MoriR25.D2KnowledgeFix (scribe, leaf). Surface:
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/system-pressure-r24.md` lines 94–95 (K5
"refreshed on each read"), 170 (K4 row 1, "a shorter spike between two reads can be invisible") and 171
(P3, "`null` means *undefined*"), plus a new K4 bullet for the entry's `## Corrections` section.

**This seat edits no product file.** The lane entry is byte-identical to HEAD before and after this
report: `git show HEAD:corpus/knowledge/system-pressure-r24.md | sha256sum` and
`sha256sum corpus/knowledge/system-pressure-r24.md` both print
`5d3a322aadb00c6ba3700b6c5b31d4e5b5305b404731f0eb37a5a3474c019ce5`; lane HEAD is
`6a92d5eebe91d7062c371e8341b23bab89de0d9c`; `git status --porcelain -- corpus/knowledge/system-pressure-r24.md`
prints nothing. Everything below is a ready-to-apply patch for the integration owner, verified on a
patched copy in `/tmp`, not applied.

## Result

- The three routed body lines are rewritten in place, each with an inline correction note naming round 25.
- One new K4 bullet is added inside the existing `## Corrections` section (exactly one such heading remains).
- The three phrases the contract forbids outside a `## Corrections` section drop from **1 occurrence each**
  to **0 each**; `(K4)` goes from **0** to **1** inside the Corrections section.
- The precedence banner "Where this section and a later line disagree, this section wins" is deleted from
  the file (it was the only occurrence of that phrase in the corpus), because the routed D2 remedy is to
  fix the body in place and stop relying on the banner
  (`corpus/lessons/round-24-verifier-spotcheck.md:143`).
- Verification: patched copy passes the contract's literal D2 predicate (`.ufo/waves/round-25/contract.md:20`),
  the stricter predicate proposed by seat `MoriR25.CriticC1Predicates` (F1), and the A1/A3 predicate stated
  by seat `MoriR25.BuildRoutedR24Tool`. Base = 17 failing checks, patched = 0.

## Sources read this round (all read-only)

| What | Where |
|---|---|
| Round-24 wave-2 critic (K4, K5, P3 corrections and their smallest corrections) | `.ufo/waves/round-24/w2/CriticKnowledgeOverclaim.md:85-104,173-186` |
| Round-24 wave-2 knowledge reviewer (M1 replacement text, M4 on the banner) | `.ufo/waves/round-24/w2/ReviewKnowledgeFacts.md:48-56,74-77` |
| Round-24 wave-2 table reviewer (F-6: 16 body-vs-corrections disagreements) | `.ufo/waves/round-24/w2/ReviewKnowledgeTable.md:54-63` |
| The routed defect text this item repairs | `corpus/lessons/round-24-verifier-spotcheck.md:135-146` (D2 at :138-143) |
| The contract's D2 predicate | `.ufo/waves/round-25/contract.md:20` |
| Entry's own `## Corrections` section (target of the new K4 bullet) | `corpus/knowledge/system-pressure-r24.md:8-42` |
| Entry's own Limits text, which already carries the corrected K4 wording | `corpus/knowledge/system-pressure-r24.md:186-188` |
| Sibling critic on the C1 predicates (stronger normalized predicate) | `.ufo/waves/round-25/w1/CriticC1Predicates.md:62-84` |

Upstream v7.2 sources re-opened by me this round into `/tmp/mori-r25-d2/` (raw.githubusercontent.com tag
`v7.2`): `kernel/sched/psi.c` (1725 lines), `Documentation/accounting/psi.rst` (188),
`include/linux/psi_types.h` (216), `kernel/sched/sched.h` (4216); plus the commit message of
`52b1364ba0b1` from git.kernel.org. Anchors re-verified by line number in those bytes:

- `psi.c:161` — `#define PSI_FREQ (2*HZ+1) /* 2 sec intervals */`
- `psi.c:342-360` — `calc_avgs()`, the exponential decay (`calc_load` with `EXP_10s/60s/300s`)
- `psi.c:362-415` — `collect_percpu_times()`; `:408-411` the cumulative `total` update (no decrement path)
- `psi.c:525-575` — `update_averages()`; `:551` `sample = group->total[PSI_AVGS][s] - group->avg_total[s]`;
  `:571-572` `group->avg_total[s] += sample; calc_avgs(...)`
- `psi.c:600-602` — the averages work item recomputing on its own schedule
- `psi.c:1268` — `collect_percpu_times(group, PSI_AVGS, NULL)` inside `psi_show` (runs on every read)
- `psi.c:1269-1270` — `if (now >= group->avg_next_update) group->avg_next_update = update_averages(group, now);`
- `psi.c:1017-1018` — `if (!curr->pid) return;` (IRQ time charged only to a non-idle current task)
- `psi.rst:60-65` — the total is exported "to allow detection of latency spikes which wouldn't necessarily
  make a dent in the time averages"
- `psi_types.h:57-70` — `enum psi_states` has `PSI_IRQ_FULL` and no IRQ `some` state
- commit `52b1364ba0b1` message — "we don't use PSI_IRQ_SOME since IRQ/SOFTIRQ always happen in the current
  task on the CPU … so we only use PSI_IRQ_FULL"

## The patch, ready to apply

### 1. Lines 94–96 → F4 body (K5)

Old (3 lines, `:94`, `:95`, `:96`):

```
The averages are exponentially decayed, sampled at `PSI_FREQ = (2*HZ+1)` ("2 sec intervals"), and refreshed
on each read ([psi.c:160-164](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c),
[psi.c:1265-1272](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
```

New (6 lines, in the same place):

```
The averages are exponentially decayed (`psi.c:342-360`), sampled at `PSI_FREQ = (2*HZ+1)` ("2 sec intervals")
([psi.c:160-164](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)). Each read collects the per-CPU
times that feed `total` ([psi.c:1268](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)); the averages are recomputed only when the next 2-second update is due — on a read
([psi.c:1269-1270](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)) or by the averages work item
([psi.c:600-602](https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/sched/psi.c)).
[Round 25 correction (K5): the round-24 body overstated the averaging refresh; corrected in place, matching the corrections section above.]
```

Why this wording: the wave-2 critic's K5 smallest correction is "the total is collected on each read; the
averages are recomputed on a read only when the next 2-second update is due (psi.c:1268-1270)"
(`.ufo/waves/round-24/w2/CriticKnowledgeOverclaim.md:102-104`), and the wave-2 knowledge reviewer's M1
replacement text adds the averages work item as the second recompute path
(`.ufo/waves/round-24/w2/ReviewKnowledgeFacts.md:52-54`). The new text carries both, and it states the
"only when the next 2-second update is due" clause **outside** the Corrections section, which the C1 tool
needs as a positive. The old `psi.c:1265-1272` window is replaced by the tighter `psi.c:1269-1270` gate plus
`psi.c:1268` and `psi.c:600-602`.

### 2. Line 170 → decision-table row 1 (K4)

Old (`:170`, 527 chars):

```
| All four files present, kernel shape (F2), low values | each resource `ok` | `PRESSURE_OK`, exit 0 | That there was no stall: `avg10` is a decayed 10-second trend resampled every ~2 s (F4), so a shorter spike between two reads can be invisible. That the host is healthy. That the reading covers per-cgroup pressure (F9). That the local threshold was meaningful (F11). That accounting was running: a root `cgroup.pressure` of 0 freezes the totals and decays the averages, so `PRESSURE_OK` can stand under real pressure (U7). |
```

New:

```
| All four files present, kernel shape (F2), low values | each resource `ok` | `PRESSURE_OK`, exit 0 | That there was no stall: `avg10` is a decayed 10-second trend resampled every ~2 s (F4), so a short event between two reads is counted in `total` and decayed into the averages, but it may leave `avg10` under the threshold, and one read cannot say when it happened (round 25 correction, K4). That the host is healthy. That the reading covers per-cgroup pressure (F9). That the local threshold was meaningful (F11). That accounting was running: a root `cgroup.pressure` of 0 freezes the totals and decays the averages, so `PRESSURE_OK` can stand under real pressure (U7). |
```

Why: the critic's K4 smallest correction for row 1 is "can stay under the threshold" instead of "can be
invisible", and the full correction is "A short event is counted in `total` and decayed into the averages,
but it may leave `avg10` under the threshold, and a single read cannot say when it happened"
(`.ufo/waves/round-24/w2/CriticKnowledgeOverclaim.md:94-96`). The new row is that sentence verbatim in
substance. The word "spike" is deliberately gone from this row, so no fold of the row can match a
`spike … invisible` pattern. The new row also matches the wording the entry already carries in its Limits
bullet at `:186-188`, so the table and the Limits section now say the same thing.

### 3. Line 171 → decision-table row 2 (P3)

Old (`:171`, 361 chars):

```
| IRQ file carries only a `full` line (F5) | `irq` = `ok`, `some: null` | unchanged by the resource itself | That IRQ "some" pressure is zero — the kernel never emits an IRQ `some` line (F5); `null` means *undefined*, not *zero*. That IRQ pressure is low. That the IRQ file is complete for the host: it is created only under `CONFIG_IRQ_TIME_ACCOUNTING` (F6). |
```

New:

```
| IRQ file carries only a `full` line (F5) | `irq` = `ok`, `some: null` | unchanged by the resource itself | That IRQ "some" pressure is zero — the kernel never emits an IRQ `some` line (F5); `null` means *not tracked*, not *zero*: the kernel has no IRQ `some` state (S095; S096 rationale) (round 25 correction, P3). That IRQ pressure is low. That the IRQ file is complete for the host: it is created only under `CONFIG_IRQ_TIME_ACCOUNTING` (F6). What IRQ `full` measures is [UNKNOWN]: no upstream document defines it, and `psi.c:1017` charges IRQ time only to a non-idle current task. |
```

Why: the critic's P3 smallest correction is "`null` means not tracked: the kernel has no IRQ `some` state
(S095; S096 rationale), not zero", plus an `[UNKNOWN]` for IRQ `full`
(`.ufo/waves/round-24/w2/CriticKnowledgeOverclaim.md:185-187`). The row now carries both, and it matches
the Corrections bullet at `:27-29`. "not tracked" sits outside the Corrections section, as the C1 tool's
positive requires.

### 4. New K4 bullet, inserted inside the existing `## Corrections` section

Placement: immediately **before** the existing `- **Averages (K5).**` bullet at `:17`. No heading is added
or moved; exactly one `## Corrections` heading remains in the file.

One physical line (407 chars), containing both the token `(K4)` and the word `total` on the same line:

```
- **Short spikes between reads (K4).** A stall that starts and ends between two reads is still counted in `total` and is decayed into the averages at the next update, but it can leave `avg10` under the threshold, and a single read cannot say when it happened (`psi.rst:60-65`; `psi.c:342-360,408-411,551,572`). The round-24 decision-table row said otherwise; that row was corrected in place in round 25.
```

This is the bullet the routed defect names as missing ("no K4 row in its corrections section",
`corpus/lessons/round-24-verifier-spotcheck.md:138-141`): the wave-2 critic named K4 explicitly but the
Corrections section carried only K3, K5, K6, P2, P3, P4 and the minor-citation rows.

### 5. Lines 10–11 → the Corrections preamble (banner removed)

Old (`:10`, `:11`):

```
Wave-2 seat CriticKnowledgeOverclaim (`.ufo/waves/round-24/w2/CriticKnowledgeOverclaim.md`) contradicted or narrowed
several statements below. Where this section and a later line disagree, this section wins.
```

New:

```
Wave-2 seat CriticKnowledgeOverclaim (`.ufo/waves/round-24/w2/CriticKnowledgeOverclaim.md`) contradicted or narrowed
several statements below. Each bullet names the finding it corrects and the wording that replaces the body text it
contradicts. Where the body has been corrected in place, the body carries the same wording and names the round of
that correction; the K3 and P4 bullets are carried here only, because their body rows still hold the round-24
wording.
```

Why: the routed remedy says "Fix the body lines in place, with a correction note, and stop relying on a
'this section wins' banner" (`corpus/lessons/round-24-verifier-spotcheck.md:143`). Once the three routed
body lines carry their own correction notes, the precedence rule has nothing left to govern; the rewritten
preamble instead states each bullet's status, and it names the two bullets (K3, P4) whose body rows this
patch deliberately does not touch, so no reader is told a stale body line is correct. This sentence was the
only occurrence of "this section wins" in the whole corpus.

## Verification (read-only; the repo file was never written)

Method: I copied the HEAD blob of the entry into memory, applied the five edits above as exact string
substitutions, and re-derived three predicates over the patched copy.

Scripts (outside the lane): `/tmp/mori-r25-d2/d2verify.py` (all three predicates),
`/tmp/mori-r25-d2/d2final.py` (contract + CriticC1Predicates), `/tmp/mori-r25-d2/d2peer.py`
(BuildRoutedR24Tool's A1/A3 predicate). Upstream bytes: `/tmp/mori-r25-d2/{psi.c,psi.rst,psi_types.h,sched.h}`.

| Check | Base | Patched |
|---|---|---|
| contract D2: `refreshed on each read` outside Corrections | 1 | **0** |
| contract D2: `a shorter spike between two reads can be invisible` outside Corrections | 1 | **0** |
| contract D2: `` `null` means *undefined* `` outside Corrections | 1 | **0** |
| contract D2: `(K4)` present in a `## Corrections` section | no | **yes** |
| contract D2: number of `## Corrections` sections | 1 | 1 |
| BuildRoutedR24Tool A1: `refreshed on (each\|every) read` outside | 1 | **0** |
| BuildRoutedR24Tool A1: `spike…invisible` outside | 1 | **0** |
| BuildRoutedR24Tool A1: `null…means…undefined` outside | 1 | **0** |
| BuildRoutedR24Tool A1: `only when the next` outside Corrections | absent | **present** (F4 body) |
| BuildRoutedR24Tool A1: `not tracked` outside Corrections | absent | **present** (row 171) |
| BuildRoutedR24Tool A1: one Corrections line has `(k4)` **and** `total` | no | **yes** (the K4 bullet, one physical line) |
| BuildRoutedR24Tool A1: `## Facts` / `## Decision table` present, table data rows ≥ 11 | yes / yes | yes / yes |
| A3: `this section wins` absent from the whole file | 1 occurrence | **0** |
| CriticC1Predicates F1: `(refresh\|recomput\|updat)\w* (on\|at) (each\|every) read` outside | 1 | **0** |
| CriticC1Predicates F1: `can be invisible` outside | 1 | **0** |
| CriticC1Predicates F1: `null means undefined` outside | 1 | **0** |
| CriticC1Predicates F1: F4 paragraph has `only when the next` | no | **yes** |
| CriticC1Predicates F1: row 1 has `under the threshold` | no | **yes** |
| CriticC1Predicates F1: row 2 has `not tracked` | no | **yes** |
| **failing checks (union of all three predicates)** | **17** | **0** |

Line-count effect: 230 → 237 lines (+7): F4 +3, row 1 ±0, row 2 ±0, K4 bullet +1, preamble +4 −2.

Also checked and unchanged by the patch: the decision table keeps all 11 data rows (the C1 tool's row-count
floor), and `## Facts` and `## Decision table` keep their exact headings.

## Residual defects NOT fixed by this patch (reported, not fixed)

The routed D2 item names only K5, K4 and P3. Four further body-vs-corrections disagreements remain in the
entry after this patch; they are outside the routed item, so I did not touch them, but the L1 should know
that a "corrections sweep every mention" reading of D2 would still see them:

1. **K3 version scope not in the body.** The Corrections bullet at `:13-16` says the two decision-table rules
   hold "on v7.2 only" (system CPU `full` zeroing from 5.19, commit `890d550d7dba`; no CPU `full` line
   before 5.13). The body rows at `:172` ("a nonzero value means the file is not the kernel's system CPU
   pressure file") and `:176` ("`malformed` means *this file is not a kernel PSI file of this resource*")
   carry no version qualifier.
2. **P4 ENOENT cause list not in the body.** The Corrections bullet at `:30-33` lists five possible causes
   for a missing file (PSI boot-disabled, no IRQ time accounting, no `CONFIG_PSI`, kernel older than 6.1,
   a `--root` pointing elsewhere). The body row at `:173` still says "a missing file is consistent with
   either", naming only two.
3. **P4 `[INFERENCE]` label missing on the counter-regressed row.** The body row at `:177` asserts "so a
   decrease means the two samples are not comparable readings of the same counter" without the `[INFERENCE]`
   label the Corrections bullet at `:30-31` requires (the code proves the design, not the absence of a
   defect).
4. **Minor-citation row only partly applied.** The Corrections bullet at `:38-40` gives F3's readers as
   `psi.c:1540,1545,1550` plus the irq reader at `psi.c:1686`; the body at `:86` and `:142` still cites the
   wider `psi.c:1538-1550`.

Two further points for the integration owner, both about the C1 gate rather than the entry:

- The D2 predicate as written in `.ufo/waves/round-25/contract.md:20` is satisfied by the *literal
  absence* of three phrases. Seat `MoriR25.CriticC1Predicates` showed four ways to satisfy it while leaving
  the false statements in place (paraphrase, heading laundering, deleting the rows, indent reflow), so the
  literal form can certify an unfixed entry. The patch above is built to satisfy the stricter normalized
  predicate as well, and the L1 should decide whether `tools/mori-routed-r24.py` gates on the literal form
  or the stricter one.
- A3's banner clause should be gated on the phrase being absent from the **whole** file, not only outside
  the Corrections section: at HEAD the sentence already sits inside that section, so the "outside only"
  reading is satisfied before any fix and cannot distinguish a fixed entry from an unfixed one.

## Coordination

- `MoriR25.BuildRoutedR24Tool` (executor, owns `tools/mori-routed-r24.py`): I sent it the exact K4
  physical line, the banner reading (delete, do not keep, gate the whole file) and the two positive
  placements ("only when the next" in the F4 body, "not tracked" in row 171), so its predicate and this
  patch agree. No repo byte was changed by either seat; the two meet in the L1's integration.
- `MoriR25.CriticC1Predicates` (critic): its F1 stronger predicate is one of the three I verified against.

## Out of scope / not done

- No product file edited; the lane entry is untouched and byte-identical to HEAD.
- No `jj` command was run at the fleet root; no git write of any kind was performed in the lane
  (`git show`, `git status`, `git rev-parse` only, all read-only).
- No tool installed or upgraded: `curl`, `python3` (3.14.8 under `python3 -I -B`) and `git` were already
  present and sufficient.
- K3, P4 and the F3 citation residues listed above were left in place on purpose (outside the routed item).

## Artifact paths

- This report: `.ufo/waves/round-25/w1/D2KnowledgeFix.md` (lane repo).
- Verification scripts, outside the lane, not committed: `/tmp/mori-r25-d2/d2verify.py`,
  `/tmp/mori-r25-d2/d2final.py`, `/tmp/mori-r25-d2/d2peer.py`.
- Upstream v7.2 bytes read this round, outside the lane: `/tmp/mori-r25-d2/psi.c`, `/tmp/mori-r25-d2/psi.rst`,
  `/tmp/mori-r25-d2/psi_types.h`, `/tmp/mori-r25-d2/sched.h`.
