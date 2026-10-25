# Round 45 verifier spot-check

author: hyaku closure (non-author integrator, @m_flash)

Reviewed committed bytes at lane tip `12c89ea63491fcca0f46169d809740711d3d052e` (counter inputs identical to
`baabc9929f0f272f3a99cd0a7816a2cb35fda835`: `git diff --stat baabc992 12c89ea6` → `LOG.md` only). Pre-round lane HEAD
`b1d7269f4f263dc954f31d97208aee4b56055618`; the round's entering contract tip `554ff416459c92f0dea9762f834a556df2990187`
is its parent's ancestor (`b1d7269f` adds only `corpus/lessons/round-44-verifier-spotcheck.md`). I did not author the
round. Lane-owned r45 counters are registered gates (`SKILL.md` rows `r45 ledger counter (C1)` …`(C3)`), so I did
not execute them or any lane selftest: each claim was re-derived with my own plain git/grep/sha256sum/wc
measurement, and the gate verdicts were evidence-verified from committed bytes (`LOG.md` "Round 45" entry,
`.ufo/waves/round-45/evidence/`, `w1/`).

Watchdog digest (copied): `2026-10-25T07:31:38-03:00 launch mori round=45 pgid=271214 driver=hyaku-inline attempt=1`;
`2026-10-25T08:22:30-03:00 lane-dead-no-report mori round=45; retry same round (… content-policy refusal (invalid_prompt); lane work landed at baabc992, report not filed)`;
`2026-10-25T08:22:32-03:00 launch mori round=45 pgid=3993108 driver=hyaku-inline attempt=2`;
`2026-10-25T08:29:29-03:00 complete mori round=45; hyaku-inline attempt=2`.

## Conformance

- Report `.ufo/reports/round-45/mori.md` committed by `mori-shokunin <mori@shokunin.local>` at `308a27ad`
  (08:29:17 -03, after lane commit `12c89ea6` at 08:26:44). `## SHONEN` heading present, four lines, all `[~]`.
- Cited lane commits `3ad8faaa`, `18fd68b0`, `baabc992…`, `12c89ea6…` (and `554ff416`, `b1d7269f`) all resolve and
  `git merge-base --is-ancestor <hash> master` exits 0 for each. `jj-lane.sh state` → `local=remote=12c89ea6…
  ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master`
  → `12c89ea6…`.
- Prompt `.ufo/prompts/mori-round-45.md` §1–5 diffs against `templates/round-prompt.md` only at `{{LANE}}`,
  `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}` substitutions; §6 is the hyaku addendum. Contract carried.
- Not a marker: three attempt-1 commits carry the round's work; status `ok`.
- Defects (status-neutral):
  1. `SCORECARD.md` carries no round-45 claim rows: `git diff b1d7269f 12c89ea6 -- SCORECARD.md` is empty
     (AXES.md "record before→after in `SCORECARD.md`"). The report discloses it.
  2. The freeze-manifest tally is overstated. Report and `LOG.md` (Round 45 entry, line 30 of the entry) say
     `sha256sum -c` gave "29/29". I measured `grep -v '^#' .ufo/waves/round-45/evidence/freeze-r45.txt | sha256sum -c`
     → **27 OK**, rc 0 (28 non-comment lines, one blank). Re-hashing each path with `git show baabc992:<path> |
     sha256sum` also gives 27/27; external census `3fb72615…` matches. The digests hold; only the count is false.
     `LOG.md` is append-only, so it needs a named correction entry.
  3. Two "residual" executor seats (`w1/ExecSelftestOrphans.md`, `w1/ExecSelftestRoutedR24.md`) sit outside the
     committed spec/dispatch, and the residual call allows reviewer/critic seats only. The report discloses this.
     There was one wave (37 + 2 seats) and no wave 2, so the round gets no wave-2 falsification credit.

## Claims

| claim | my plain re-derivation (committed bytes) | gate evidence verified | verdict |
|---|---|---|---|
| C1 operability — ledger gate stops being vacuous | Each `figures.tsv` command, with `@REV@` substituted, run at `baabc992` and at `554ff416`: **15 rows, mismatches=0, moved=5** (F01 245→246, F02 73→75, F03 54→55, F05 43→53, F08 28→33), **const=10** (every non-moving row carries `CONST=`); duplicate ids 0, duplicate commands 0; classes `checks,corpus,evidence,registry,wave`. Witnesses: `w-dup.tsv` 1 dup id + 1 dup cmd, `w-head.tsv` 8 `HEAD` rows, `w-revconst.tsv` 12 rows with no `CONST=`; each embodies its class. | `LOG.md` r45: `C1=met`, `witnesses=3/3`, `C1_SELFTEST pass=16 fail=0`. Before: `w1/ExecWitnesses.md:120-127`, the round-44 counter prints `C1=met` on all 3 witnesses. Freeze digest `5f2deea0…` matches. | **improved** |
| C2 calibration — registry stops overstating | Population `tools/*.{py,sh}` + `.ufo/waves/round-4[45]/count-c*.py`: **36 → 39** members. Unregistered (path absent from every gate/probe row): **3 → 0**; that is coarser than the counter's row attribution, whose before is 14. Non-comment `--selftest` absent: **5 → 0**. Duplicate row names 0 → 0. Eight-cell table headers **7** (F06). Gate/probe rows 43 → 53. | `LOG.md` r45: `C2=met tables=7 unregistered=0`; report: `population_members=39 mutant=killed`, `C2_SELFTEST pass=14`. Freeze digest `153423c4…` matches. | predicate verified; axis **harmed** (below) |
| C3 depth — sourced level-naming entry | `census-cgroup-levels-r45.md` is absent at `554ff416` and present at `baabc992` with `source:`/`verified-at:`/`recheck:`/`coverage-map:` (4 lines). `SOURCES.md:252` S473: status `mined`, used-by = the entry; absent at entering. README map row at `corpus/README.md:50` (0 before). Census run by me (TMPDIR unset): `mori ok`, rc 0, W04 warnings only. | `LOG.md` r45: `C3=met`, `C3_SELFTEST pass=19`; the SKILL row pins `37fd7c24…`, which matches the committed bytes. | **improved** |

**Calibration ruling (the report's harm candidate).** The registry rows this round wrote or rendered stale pin
values that the committed instruments do not have. I measured with `git show baabc992:<path> | sha256sum`/`wc -l`:

| SKILL.md cell | pinned | committed at `baabc992` (= tip) |
|---|---|---|
| `:190` r45 C1 | `count-c1.py` `f80e75ac7421…`, `C1_SELFTEST pass=10` | `5f2deea0b35c…` (1172 lines); evidence `pass=16` |
| `:191` r45 C2 | auditor `64db765e60e3…`, 622 lines; `count-c2.py` `e8ee29eb8852…` `pass=10`; mutant `d67ffacdb3ec…` | auditor `8b82ac999091…`, **743** lines; `count-c2.py` `153423c48ca9…` (evidence `pass=14`); mutant `9850b3fcc888…` |
| `:184` r44 gate registry | `GATE_REGISTRY_SELFTEST pass=6` (tool replaced in place by v2) | evidence `pass=15` |
| `:194` r44 superseding row | v2 `pass=10`, `64db765e…`, 622 lines | `8b82ac99…`, 743, evidence `pass=15` |

`:191` is wrong in more places than the report says: it lists only the auditor pin, but the counter and
mutant digests are false too. The auditor was already `8b82ac99…`/743 at `18fd68b0`, the very commit that wrote
`:191`. `w1/CritAxisHarm.md` §1b flagged these cells inside the round, before `baabc992` landed, and they shipped
unmarked in `SKILL.md`. Calibration is "SHONEN/SCORECARD entries match observed repo state" (AXES.md). The round's
own calibration claim lowered unregistered paths while adding false self-description to the same registry. That is
a trade, and a trade is not an improvement (AXES.md, "a trade anywhere is not an improvement"). Disclosing it in the
report does not repair the committed cells. **calibration: harmed.** No other owned axis was harmed:
`SCORECARD.md` is byte-unchanged, and the round-44 ledger's new inadmissibility does not touch SCORECARD's r44
pointer (frozen r44 counter, `w1/CritAxisHarm.md` item 2).

Per-axis: operability improved · calibration harmed · depth improved · coverage unchanged · freshness unchanged
(S472 re-opened, `evidence/s472-reopen-l1.txt`; no freshness claim) · adjacency unchanged (both rejects keep kumitate
ground out).

## Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `census-cgroup-levels-r45.md` (S473) | admit | `curl https://cdn.jsdelivr.net/gh/torvalds/linux@v7.2/Documentation/admin-guide/cgroup-v2.rst` → 133236 B, sha256 `a9433bb0…` (matches row and entry); `:1468`, `:1474-1477`, `:1517-1519` read; `tools/mori-census.sh:1708-1712`, `:1862` read | agree | Kernel text: `memory.events` is hierarchical, `.events.local` is local. The census fills `local_oom_kill` from the service's hierarchical `memory.events` on the fallback branch, under the "local" name. The claim is narrow and grounded, and the overlap with r7/r12 entries is disclosed. |
| `who-sets-the-scope-cap-r45.md` | reject | `/home/vgpnk/Projects/shokuknow/merge/mori/knowledge/corpus/knowledge/who-sets-the-scope-cap-r45.md:4-7,14-19` | agree | `source:` S528 is a `file://` campaign note (own-work, not a lane SOURCES row). The subject is `kumitate-shokunin/scripts/cap-run.mjs`, which is adjacent ground. S530 (an upstream issue) does not ground "who sets the cap". |
| `cap-control-wording-r52.md` | reject | same dir, `cap-control-wording-r52.md:10-45` | agree | Despite its Limits section, the body ("Two traditions, one advice"; the throttle-then-kill shape "is the manual's recommendation") argues a `MemoryHigh=` change to the kumitate runner. `PROVINCE.md:16` says "Detection and report only — never remediation." |

SOURCES row check: I re-opened `corpus/SOURCES.md:252` (S473). Its quote "Similar to memory.events but the fields in
the file are local to the cgroup i.e. not hierarchical." is **17 words** (≤25) and appears verbatim at re-opened
`cgroup-v2.rst:1518-1519`. The row is tier A `docs`, `mined`, and used-by names the entry. Census:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` →
`mori ok`, rc 0.

## Trends

- **expansion — improved:** registry rows 245 → 246 (F01 re-run), knowledge 54 → 55 (F03), and one README map row.
  The admitted entry holds narrow new ground (fallback mislabel) on FR1/FR12, citing a `mined` row.
- **quality — harmed:** the C1/C2 instruments do reject the r44 vacuity classes. But false registry pins found
  in-round were left unmarked in `SKILL.md` (table above), and `LOG.md` records a false 29/29 tally.
- **discernment — improved:** a non-author agrees with the gate on 1 admit and 2 rejects, with the sources
  re-opened.

## Routed defects (lane, round 46)

1. Re-pin `SKILL.md:184,190,191,194` to the committed bytes, via superseding rows: `5f2deea0…`, `153423c4…`,
   `9850b3fc…`, `8b82ac99…`/743, and evidence tallies 16/14/15. Then sweep every other mention.
2. Append a named `LOG.md` correction: the freeze manifest is 27/27, not 29/29 (report and LOG round 45).
3. Add the round-45 claim rows and outcome to `SCORECARD.md`. Record calibration as harmed per this closure.
4. Carry the report's items: key the `--selftest` rule on parser keys (lesson M3–M5), scrub `GIT_*` in selftests
   (M11), and make the round-44 ledger admissible or supersede it.
5. The SHONEN boxes stay `[~]`. Lines 1 and 3 cite the stale registry cells, so they are not non-author-checkable
   until item 1 lands. Promotion is operator-owned.
