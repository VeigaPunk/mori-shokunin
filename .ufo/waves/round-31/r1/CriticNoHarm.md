# Round 31 no-harm check (CriticNoHarm, non-author critic)

Range: base `a12c68ae` → measured tip `a29f3e3f7f7259afb07df29c5ee8f68882712e96` (lane HEAD equals the tip; `git status --porcelain` shows only untracked files, no tracked edits). Committed bytes judged only. All execution in a sandbox clone at `/fast/scratch/hyaku/mori-r31/CriticNoHarm/clone` (detached at the tip, `git status --porcelain` empty after every run). No tools installed or updated.

## Verdict

No axis harmed. One LOW provenance gap, introduced by the in-place correction D4, should be closed before admission (see the end of this report). It is fixable and is not a tradeoff.

## Commanded checks

| Check | Result |
|---|---|
| `git diff --stat a12c68ae <tip>` | 97 files, 19309 insertions, 6 deletions. Every changed path is new (`A`) except the in-place edits in `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/earlyoom-invocation-scope-r30.md` (`git diff --name-status`) |
| `git diff --diff-filter=D --name-only` | empty, exit 0 |
| `git diff a12c68ae <tip> -- .ufo/waves/round-30 tools/mori-oom-killers.py tools/mori-census.sh` | 0 lines (`| wc -l` → `0`): round-30 evidence and both existing tools are byte-unchanged |
| Retention scan at the tip (sandbox clone, exact commanded argv) | exit 1 (structural, same as base); `"metric":4,"non_author":5,"routed":0`, policy sha256 `db06e981…3128`; hits 113, allowlisted 104, unallowlisted 4, warnings 0, forbidden_allowlist 0. Base (`.ufo/waves/round-31/w1/RetentionBase.md:42-46`): metric 4, 113/104. The four unallowlisted hits have the same path/line/class as at base: `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json` lines 8 R2, 11 R5, 12 R6, 14 R8 (matches `RetentionBase.md:50-55`) |
| SCORECARD `## Axes` table | byte-identical: `diff` of the `## Axes` section base vs tip → no output, `AXES_IDENTICAL`. All six scores unchanged (coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6) |
| PROVINCE | `PROVINCE.md` is absent from `git diff --stat` and `--name-status`: unchanged |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | exit 0, `mori ok …/corpus/SOURCES.md`; 12 advisory `W04` lines |

## Every removed line (`git diff -U0`)

All 6 removed lines are in one file, `corpus/knowledge/earlyoom-invocation-scope-r30.md`. Both hunks are intended in-place corrections, each recorded in the appended section `## Round-31 correction (routed D4 …)` at tip lines 141-153. No other file loses a line. Every other `-` header in the `-U0` output is `--- /dev/null` (new file) or a pure `@@ -N,0 …` insertion.

1. Base lines 23-25 (hunk `@@ -23,3 +23,4 @@`): the `Restart=always` bullet cited S159 alone. It is replaced at tip lines 23-26 by a version that names S159 (the commit that introduced the line) and S120 (`earlyoom.service.in` at v1.9.0, `:17`). This is routed LOW-1. I checked it upstream: `curl …/rfjakob/earlyoom/v1.9.0/earlyoom.service.in | sed -n 15,18p` puts `Restart=always` at line 17, and the S159 patch has the quoted commit message at `:6` and `Restart=always` at `:36`. The statement is accurate.
2. Base lines 53-55 (hunk `@@ -53,3 +54,5 @@`; the correction note cites 52-55, which includes the unchanged opening line 52 of the same sentence): "reports its version" is replaced at tip lines 54-58 (the note's 53-58 again includes the unchanged opening line) by "reports the last version line inside that retained scope (`earlyoom.version` is `null` when no version line is at or after the stamp …)". This is routed D4. I checked it against the unchanged tool at the tip: `tools/mori-oom-killers.py:360` `version = None`, `:389-396` assigns it only on version lines in `scoped`, `:320` `if stamp >= aetm:` sits inside the cited `:305-322`, and `:518` emits `"version": version`. The statement is accurate.

The correction's own line cites hold at the tip: tip lines 23-26 and 53-58 are the corrected text, and base lines 23-25 and 52-55 are the old text (`git show <rev>:… | sed -n`).

Other in-place modified files: their diffs contain only `+` lines. `corpus/README.md` gets one inserted map row at tip line 44 (routed D5, `@@ -43,0 +44 @@`) plus an appended section, `SCORECARD.md` and `LOG.md` get appended sections, and `corpus/SOURCES.md` gets the S161-S174 rows appended. `python3 -I -B .ufo/waves/round-27/check-row-identity.py <tip>` in the clone → `rows=174 changed=0 removed=0 bad=0`, exit 0 (QUALITY 81 holds: no first-published SOURCES cell changed).

## Per-axis judgment

| Axis | Verdict | Evidence |
|---|---|---|
| coverage | not harmed | No file deleted. The README map and frontier sections are insert/append only (new map row for the round-30 entry, new `Round-31 coverage additions` section). PROVINCE unchanged. The Axes score is unchanged |
| operability | not harmed | Both existing tools are byte-unchanged (0-line diff). Selftests at the tip in the clone: `mori-oom-killers.py --selftest` → `PASS 32/32`; `--cases cases-a2.json` → `PASS 30/30`; `--cases cases-r31-dryrun-flips.json` → `PASS 2/2`; `bash tools/mori-census.sh --selftest` → `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)`, which equals the 134 the Axes row cites. The new fixture is opt-in (the default cases file is `fixtures/mori-oom-killers/cases.json`, `tools/mori-oom-killers.py:15,806`), so no existing selftest picks it up. New `tools/mori-blind-check.sh --selftest` → `PASS`, exit 0; its selftest writes only under a temp root removed by `trap 'rm -rf …' EXIT` (`:241`), and my `TMPDIR` dirs were empty afterwards |
| depth | not harmed | The only removed knowledge text is replaced by more precise, source-checked text (see the two hunks above). The new entry `watchdog-identity-r31.md` is additive. The depth score is unchanged |
| freshness | not harmed | No `verified-at:` or `recheck:` line was removed or edited. The entry's metadata lines 1-3 have no `-` lines in the diff. New SOURCES rows carry `2026-10-22` / `365d`. No drift pin was touched |
| calibration | not harmed (one LOW gap, below) | SCORECARD additions declare claims and before-values but move no Axes score; the Axes table is byte-identical. The A1 tightening is recorded as an append. Retention metric is 4 = base 4 with an identical unallowlisted set. Privacy sweep of every `+` line for `user-<digits>.slice`, `user@<digits>.service`, `/run/user/<digits>`, `uid=<digits>`: no matches |
| adjacency | not harmed | The new tool only reads (`git rev-parse`, `git cat-file`, and `grep` on committed bytes) and has no `kill`, `systemctl`, `sudo`, `pacman` or `.omp` access (pattern grep over the tool: only lines 81, 82, 85, 241, 243, 352, 354, 365, all read-only or selftest temp). The SKILL Round31 rows say "Detection and report only: no row advises starting, stopping, signalling or locking a process" and the entry says it "changes no probe and claims no host liveness". A `flock -n` probe "is never run" (`watchdog-identity-r31.md:34`) |

## Census warning delta (advisory, not a harm)

To compare the census at base and tip I snapshotted both revisions with `git archive` into `/fast/scratch/hyaku/mori-r31/CriticNoHarm/{base,tip}/mori-shokunin` and ran `validate <dir>` on each. Both exit 0 and print `ok`. Base has 10 `W04` lines and the tip has 12. The two new lines are `S166 duplicate url …/v7.2/fs/proc/base.c` and `S168 duplicate url …/v7.2/Documentation/filesystems/proc.rst`. Both are rows with status `rejected` (`corpus/SOURCES.md:172,174`) whose own text names the existing carriers (S127/S148 and S082). The lane already had 17 rejected rows at base (`grep -c '| rejected |'`), and the census header says W04 warnings "do not affect clean lanes" (`scripts/sources-census.sh:33`). I classify this as recorded rejection, not duplicate authority.

## Counterexample (LOW, fixable): the D4 correction cites S120 without linking it

- Counterexample: after the correction, the entry body cites S120 (tip lines 24-25, and the correction note at lines 151-153). The entry's `source:` line still lists only S118 S119 S122 S154-S160 (`git show <tip>:corpus/knowledge/earlyoom-invocation-scope-r30.md | sed -n 1p | grep -oE 'S1[0-9]{2}'` → no S120). S120's `used-by` cell lists only `corpus/knowledge/userspace-oom-killers-r26.md, corpus/knowledge/oom-victim-selection-r27.md` (`corpus/SOURCES.md:126`). The lane does keep this link for the sibling source: S159's used-by names this entry (`corpus/SOURCES.md:165`). The new README map row at tip line 44 also claims "S118–S120" for the entry, so the README says S120 grounds the entry while SOURCES and the entry header say it does not.
- Why it is not a regression: at base the entry did not cite S120 at all (`grep S120` on the base entry → no match), so no linked fact lost provenance. This is new incomplete provenance on a corrected line, not a lost one. The census does not check citation-to-used-by consistency (it passes).
- Impacted axes: calibration and depth (provenance completeness). Not harmed against base.
- Smallest safe correction: append `corpus/knowledge/earlyoom-invocation-scope-r30.md` to S120's `used-by` cell (an in-place change QUALITY 81 permits; `check-row-identity.py` should still print `changed=0`), and add `S120 (earlyoom.service.in v1.9.0 \`:17\` — \`Restart=always\`)` to the entry's `source:` line. Alternatively, record in the lesson why S120 is cited but not linked.

## Commands the integration owner may re-run

- `git -C <lane> diff --diff-filter=D --name-only a12c68ae <tip>` → empty
- `python3 -I -B tools/mori-retention-gate.py scan --repo <clone> --rev <tip> --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json` → `metric 4`
- `python3 -I -B .ufo/waves/round-27/check-row-identity.py <tip>` → `changed=0`
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0

Scratch kept under `/fast/scratch/hyaku/mori-r31/CriticNoHarm/` (clone, snapshots, outputs). No process left running.
