# ReopenS145 — verdict: holds (one residual: Q77 sweep left two live false claims in round-24 w1 reports)

seat: MoriR28.ReopenS145 (leaf; no subagents, no background jobs)
attacked: row S145 (supersedes S096) at f2de0eedcd60d2e354da75265ea6122bc3896073
scratch: /fast/scratch/hyaku/mori-r28-w2/MoriR28.ReopenS145/ (committed bytes dumped there; lane untouched)
lane writes: this report only. All `git` in the lane was read-only (`show`, `log`, `grep`, `merge-base`).

## Checks run

| # | check | verdict |
|---|---|---|
| 1 | Source URL re-opened by curl now | holds |
| 2 | Gate line: quote verbatim, sha256 = my fetch, <=25 words | holds |
| 3 | Every S145 cell vs the bytes | holds |
| 4 | Round-24 F1 defect fixed, not copied | holds |
| 5 | Every used-by path cites S145 | holds |
| 6 | No named live reader states the defective wording (QUALITY 77) | holds for named readers; residual below |

## 1–2. Source re-open + Gate line

- `curl -sSL https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1.patch` at
  2026-10-22T18:53:28Z → HTTP 200, 8899 bytes, 282 lines,
  sha256 `a255f4471b9388ba3d5bfdf64a093dec35a66cd8080473fb4bd2d4b49dce7cd6`.
- Gate line at `corpus/lessons/round-28.md:65`: sha256 cell equals my fetch exactly; access time
  2026-10-22T17:59:57Z (draft seat's time; my later fetch gives the same bytes — no drift).
- Located quote verified against my bytes: patch `:15-17` reads "IRQ/SOFTIRQ always happen in the current task on
  the CPU, make nothing productive could run even if it were runnable, so we only use PSI_IRQ_FULL." — verbatim,
  25 words, at the stated lines. Decision cell `admit, A, mined` matches cells tier/status.

## 3. Cell-by-cell (SOURCES.md:151, 11 cells, 3091 bytes)

- id/source/kind/tier/scope: conventional; scope identical to S096 (holds against patch, see below).
- anchor vs patch bytes: `:11-13` CONFIG_IRQ_TIME_ACCOUNTING dependency (:11 "When CONFIG_IRQ_TIME_ACCOUNTING…"),
  `:15-17` only PSI_IRQ_FULL, psi_types.h `:58-60` PSI_IRQ and `:69-71` PSI_IRQ_FULL each under #ifdef — all exact.
  psi.c `:144-145` psi_account_irqtime, `:190-194`/`:202-203` only_full mechanics, `:211-213` irq trigger refused
  unless PSI_IRQ_FULL (line 212 is `if (res == PSI_IRQ && --state != PSI_IRQ_FULL)` — the paraphrase is fair),
  `:240` psi_irq_proc_ops, `:250-262` psi_proc_init (`if (psi_enable)` :252, #ifdef :257, proc_create("pressure/irq")
  :258), cgroup.c `:87-102` (show/write fns) and `:111-120` (`irq.pressure` cftype :113), sched/core.c `:132`
  (`psi_account_irqtime(rq->curr, irq_delta)`), cgroup-v2.rst `:40-43` (added `irq.pressure` doc :42) — all hold.
- v6.1/v6.0 psi.c re-fetched via api.github.com contents (raw.githubusercontent.com was HTTP 429 at 18:55Z):
  v6.1 43235 B/1537 lines sha256 `f3038de87e41da91a1050093d367084c201e68784336de24e1428d3b0db67ab6`;
  v6.0 39513 B/1403 lines sha256 `126479b39bc86ac4c27cbd5c134266eb03b5d3fa9333df22eda4314a870790aa` — both match
  the anchor prefixes. v6.1 line claims verified: `:145-154` psi_enable/setup_psi/`__setup("psi=")`, `:202-206`
  psi_init early return, `:914-915`/`:937` irqtime + times[PSI_IRQ_FULL], `:1145`/`:1161`/`:1164`/`:1178` only_full,
  `:1206-1209` trigger refusal, `:1497-1498`/`:1512` psi_irq_show/proc_ops, `:1522-1533` psi_proc_init
  (`if (psi_enable)` :1524, #ifdef :1529, proc_create :1530), `:1353-1537` CONFIG_PROC_FS block — all hold.
  v6.0 grep `PSI_IRQ|psi_account_irqtime|pressure/irq` → 0 matches: "first ships in Linux 6.1" verified.
- "authored 2022-08-26, committed 2022-09-09": api.github.com commit object → author 2022-08-25T16:41:08Z
  (= 26 Aug +0800, patch line 3), committer 2022-09-09T09:08:32Z. Holds.
- teaches: opens `supersedes S096 — ` (em dash); status `mined`; opened `2026-10-22`; recheck `on-release`.
- used-by (cell 12): `corpus/knowledge/system-pressure-r24.md, SKILL.md, PROVINCE.md, corpus/lessons/round-28.md`.

## 4. Defect fixed, not copied

- Named defect (round-24 `ReopenS094S097.md:12,18,21`; w1 `SupersedeS096.md` row 7): first-published teaches said
  "an absent irq file is a build-configuration fact" — one cause; the commit's own hunk gates the file under
  `if (psi_enable)` too (patch `:250-252`; v6.1 `:1524`).
- S145 teaches names the old clause, refutes it with the bytes, and states three causes (option not built in,
  PSI off at boot via psi=0/CONFIG_PSI_DEFAULT_DISABLED, kernel <6.1) — all verified against v6.1 `:145-154`,
  `:202-206`, `:1524-1530` and v6.0 grep=0. New wording, not a copy of the defective cell nor of the in-place edit.
- Provenance: first `| S145 |` commit is `1c4c186` (ancestor of attack rev); the only cell changed by `f2de0ee` is
  used-by — rewritten from files that cite S096 to files that cite S145, per the commit subject. Legitimate.

## 5. used-by citation check (at f2de0ee)

- `system-pressure-r24.md`: cites S145 at `:1`, `:30`, `:41`, `:61`, `:110`, `:177`. Holds.
- `SKILL.md:619` cites S145. `PROVINCE.md:257` cites S145. `corpus/lessons/round-28.md:11,65` cite S145. All hold.
- S096 at `:102` is restored to first-published bytes (teaches ends "…a build-configuration fact and never a zero
  reading.") — C1-mandated restore; the 81-vs-77 conflict is logged at `round-28.md:9-11`.

## 6. QUALITY 77 sweep

- Named readers clean: `build-configuration fact` and any `build-config` variant → 0 hits in SKILL.md, PROVINCE.md,
  corpus/README.md, all 35 corpus/knowledge/*.md files. `system-pressure-r24.md:179` already carries the
  multi-cause wording ("a missing file is consistent with either … a kernel older than 6.1"). Holds.
- Tree-wide (`git grep 'build-config' f2de0ee`): remaining live (non-falsification) statements —
  `.ufo/waves/round-24/w1/SrcPsiIrqCommit.md:112-113,161` and `CriticC2Semantics.md:169` still assert the claim;
  the w1 report called these "live false claim in a seat report" and recommended the L1 correct or log them
  (`SupersedeS096.md:146-158`). At f2de0ee neither file carries a correction block and `round-28.md` does not name
  them. Other hits are falsification records (round-24 w2 reports, `round-24.md:40` log, round-28 w1 analyses) —
  correctly kept. Restored `SOURCES.md:102` states it — contract-mandated, logged.

## Findings

- F-1 (Low): QUALITY 77's letter ("every place that states it … carries the corrected wording at the commit that
  carries the correction") is unmet at f2de0ee for `.ufo/waves/round-24/w1/SrcPsiIrqCommit.md:112-113,161` and
  `CriticC2Semantics.md:169`: the false claim still stands with no correction block and no disposition in the
  round-28 lesson. Archived seat reports, not readers in any used-by set — but a reader opening them gets the
  defective claim unmarked.
- F-2 (Info): restored S096 used-by lists `corpus/knowledge/system-pressure-r24.md` and `corpus/lessons/round-24.md`;
  the former now cites S145, not S096 — stale pointer inside a byte-frozen row (QUALITY 81 vs reality; logged
  consequence of the restore, same shape as S143/S144 in M4).

## Residual risk / gaps

- `psi_types.h` v6.1 file itself not re-fetched (429 on raw.github at 18:55Z; patch hunks verify the anchors).
- "merged into v6.1-rc1 by bd9a3dba185c" carried from round 24, not re-opened (also a stated gap in w1 report).
- S096's restored teaches is false wording standing in the registry — contract-required; conflict logged, not resolved.

## Tooling / privacy

- No installs (pacman paused host-wide). Used: curl 8.23.0, git 2.56.0, python3 (json parse only), sha256sum.
- No uid/pid/session/unit/settings values in this report; lane retention untouched.
