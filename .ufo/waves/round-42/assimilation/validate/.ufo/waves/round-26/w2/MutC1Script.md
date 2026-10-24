# MutC1Script — mutation test of the committed C1 counter (round 26, wave 2)

Seat: `MoriR26.MutC1Script` (mutation tester, leaf; no subagents, no background jobs).
Lane: `mori-shokunin`; lane tip under attack `16935e24c93fa7e7567413d7ec091339a5df1474` (branch
`master`, read with git; the lane working tree was never written to except for this report).
Target under test: `.ufo/waves/round-26/count-c1.sh` (lane sha256
`014a0ecdc6b56132e87f51cfc284cf29be9bbc41e8a14cb877e81662156519aa`; byte-identical to
`git show 16935e24:.ufo/waves/round-26/count-c1.sh`).
Sandbox clone: `/fast/scratch/hyaku/mori-r26/wt-w2mutC1` (branch `r26-wt-w2mutC1`, base
`16935e24`, clean before and after; 19 mutant commits kept on `mutant/M01` … `mutant/M19`).
Harness and raw results: `/fast/scratch/hyaku/mori-r26/MutC1Script/{mutate_c1.py, count-c1-local.sh,
results.json}`.

## Method

1. The counter was copied to `count-c1-local.sh` with **only** the `L=` value changed to the sandbox
   clone (`diff` of the two scripts shows one changed line: `L=/fast/scratch/hyaku/mori-r26/wt-w2mutC1`
   vs the lane path). Every other byte, including the phrase-list commit `28b04940`, is the committed
   one.
2. The counter reads committed bytes only, so each mutant is a **content mutation committed to the
   clone**; the counter is then run at that mutant commit (`bash count-c1-local.sh <mutant-sha>`).
3. After every run the clone is reset to the base commit and the four touched files are re-hashed;
   the before/after sha256 pairs are in `results.json` (`restored: true` for all 19).

**Baseline (pristine base, same counter):**
`stale_present=0`, `r26_entry=present`, `r26_new_source_ids=13`, `r12_names_r26=4`, exit 0 — i.e. the
declared C1 after-state of amendment A1.

**Kill rule used here:** a mutant is *killed* when the counter's output differs from the clean
after-state (it must report `stale_present=0`, `r26_entry=present`, `r26_new_source_ids` ≥ 1,
`r12_names_r26` ≥ 1 and exit 0). A mutant is a *survivor* when the counter prints exactly the clean
after-state on mutated bytes. No baseline failure occurred, so no result is inconclusive.

## Verdict table — 19 mutants, 14 killed, 5 survived

| Id | Site | Mutation | Expected detector | Counter output | Verdict |
|---|---|---|---|---|---|
| M01 | F1 r12 | reinsert F1 `On this host both services are inactive` verbatim | `stale_present≥1` | `stale_present=1` | killed |
| M02 | F2 r12 | reinsert `` `systemctl is-active earlyoom.service` → `inactive` `` verbatim | `stale_present≥1` | `stale_present=1` | killed |
| M03 | F3 r12 | reinsert F3 `Both service units are inactive` verbatim | `stale_present≥1` | `stale_present=1` | killed |
| M04 | F4 README | reinsert `inactive on this host` verbatim in the r12 row | `stale_present≥1` | `stale_present=1` | killed |
| M05 | F1 r12 | F1 with a **double space** (`On this  host both …`) | `stale_present≥1` | `stale_present=1` | killed |
| M06 | F1 r12 | F1 wrapped in `**` | `stale_present≥1` | `stale_present=1` | killed |
| M07 | F1 r12 | F1 with a **line break at a space boundary** (`both` / `services`) | `stale_present≥1` | `stale_present=1` | killed |
| M08 | F1 r12 | F1 with a **line break inside a word** (`servi` / `ces`) | `stale_present≥1` | `stale_present=0` | **survived** |
| M09 | F1 r12 | F1 with `_` emphasis (`are _inactive_`) | `stale_present≥1` | `stale_present=0` | **survived** |
| M10 | F1 r12 | F1 with the word in a code span (`` are `inactive` ``) | `stale_present≥1` | `stale_present=0` | **survived** |
| M11 | F1, other file | F1 verbatim added to `corpus/knowledge/oom-kill-counter-kernel-only-r12.md` | `stale_present≥1` | `stale_present=0` | **survived** |
| M12 | r12 file | **delete r12 entirely** | counter must not report clean | `missing=corpus/knowledge/userspace-oom-killers-r12.md`, exit 2 | killed |
| M13 | r12 pointer | **drop the r12 → r26 pointer** (all 4 mentions) | `r12_names_r26≥1` | `r12_names_r26=0` | killed |
| M14 | r26 source line | **empty the `source:` line** | `r26_new_source_ids≥1` | `r26_new_source_ids=0` | killed |
| M15 | r26 source line | **source: line cites only S113** | `r26_new_source_ids≥1` | `r26_new_source_ids=0` | killed |
| M16 | r26 entry | delete the r26 entry | `r26_entry=present` | `r26_entry=absent`, `r26_new_source_ids=0` | killed |
| M17 | r26 source line | a *first* `source:` line citing only S100 (the S114 line moves to second) | `r26_new_source_ids≥1` | `r26_new_source_ids=0` | killed |
| M18 | r26 source line | round-26 row id written lower case (`source: s114`) | `r26_new_source_ids≥1` | `r26_new_source_ids=0` | killed |
| M19 | F4 README | F4 with the tail in a code span (`` inactive on `this host` ``) | `stale_present≥1` | `stale_present=0` | **survived** |

All eight mutation designs named in the seat assignment are covered (M01–M04 verbatim, M07 line break,
M06 `**`, M05 double spaces, M12 delete r12, M14 empty source line, M15 S113-only, M13 drop the r12
pointer), plus 11 further mutants.

## Survivors — does the survivor keep a stale statement alive?

**Yes for four of the five; the fifth keeps the claim alive in a degraded form.** The counter's
normalisation is `tr -s ' \n\t' '   ' | tr -d '*'` (`count-c1.sh:9`): whitespace runs are squeezed to
one space and **asterisks only** are deleted. Everything else in the file survives into the fixed-string
search.

* **M09 (`_` emphasis) — stale statement FULLY alive.** Mutated r12 line 6 reads
  `On this host both services are _inactive_. systemd-oomd v261 records …`. Markdown renders that as
  *On this host both services are inactive.* — byte-for-byte the stale present-tense claim, in the very
  file the counter inspects. The counter's own view of the file is
  `On this host both services are _inactive_. systemd` (underscores survive `tr -d '*'`), so the
  fixed-string search for `On this host both services are inactive` fails and `stale_present=0` is
  reported.
* **M10 (code span) — stale statement FULLY alive, and the most realistic escape.** Mutated r12 line 6:
  `On this host both services are \`inactive\`. systemd-oomd v261 records …` → renders as *On this host
  both services are inactive.* Backticks are this corpus's own inline-code convention (the r12 and r26
  entries use them throughout), so a stale sentence written in code style is invisible to the counter.
  Counter view: `On this host both services are \`inactive\`. systemd`.
* **M19 (code span in README) — stale statement FULLY alive.** Mutated `corpus/README.md:34`:
  `… and earlyoom kill paths; inactive on \`this host\` → \`unavailable (inactive)\`, never 0; …` →
  renders as *inactive on this host*, the F4 present-tense summary, in the file the counter inspects.
  Counter view: `kill paths; inactive on \`this host\` → \`unavailable`.
* **M11 (a different corpus file) — stale statement FULLY alive in the corpus.** The sentence
  `On this host both services are inactive.` was added under `## Claim` of
  `corpus/knowledge/oom-kill-counter-kernel-only-r12.md`. The frozen phrase list names two files only
  (`c1-phrases.txt` at `28b04940`), so the counter never looks there; `stale_present=0`.
* **M08 (line break inside a word) — claim alive but degraded.** Mutated r12 line 6:
  `On this host both servi` / `ces are inactive. …`. The squeeze turns the break into a space, giving
  `On this host both servi ces are inactive.` — a broken word, so the claim survives in a mangled form
  rather than verbatim. This is the only survivor that does not leave a clean present-tense sentence.

**Consequence for the C1 claim.** A clean `stale_present=0` from this counter is *not* evidence that
the four stale statements are absent from the two files: one markup character (`*` → `_` or a backtick)
hides them (M09, M10, M19). The counter's declared intent in amendment A1 — "whitespace folded,
emphasis removed" — is implemented for one emphasis marker only. This is a **coverage defect of the
detector, not a defect of the landed tip**: a spot check of the landed files for the survivor classes
finds no present-tense stale statement in any markup form —
`git show 16935e24:corpus/knowledge/userspace-oom-killers-r12.md` has no occurrence of
`inactive on`, `both services`, `service units are` or `both killer services`; `corpus/README.md:34`
reads `on 2026-10-19 both killer services were inactive here` (dated, past tense, and not the F4
phrase); the r26 entry quotes the old claim only historically (`userspace-oom-killers-r26.md:14`:
"said, in the present tense, that both services are inactive; that was true on 2026-10-19 and is false
now", and `:244` quoting the "inactive on this host" summary) — and because the counter is file-scoped,
those quotations do not produce a false positive. **[INFERENCE]** the landed C1 after-state is real; the
counter would not have certified a reinserted stale sentence written in code-span or underscore form.

## Secondary findings on the counter (killed, but by a brittle route)

1. **M12 — a deleted file aborts the counter instead of counting.** `count-c1.sh:8` treats a missing
   file as a setup error (`missing=…`, exit 2), so the deletion is *detected*, but not as
   `stale_present=1`: the counter never produces a stale count for a file it cannot read. A deletion is
   a regression of the same kind as a stale phrase and is reported in a different shape.
2. **M17 — the r26 source rule reads only the FIRST `source:` line** (`grep -m1 '^source:'`,
   `count-c1.sh:14`). With a first line citing only S100 and the real round-26 line second, the counter
   reports `r26_new_source_ids=0` although the entry does cite S114. Over-strict (false alarm), not a
   missed stale statement.
3. **M18 — the S-id match is case-sensitive** (`grep -oE 'S[0-9]{3}'`, `count-c1.sh:14`): `source:
   s114` yields `r26_new_source_ids=0`. Over-strict (false alarm).
4. `r26_new_source_ids` counts ids **strictly greater than 113**, so S113 itself does not count — this
   matches the contract's wording ("S ids above S113") and M15 confirms the rule works as declared.

## Restoration evidence

Every mutant was reverted with `git reset --hard 16935e24` + `git clean -fd` in the sandbox clone;
the four touched files were re-hashed from the committed base blob after every run and compared with
the pre-run hashes (`results.json` → `restored: true` for all 19 mutants). Base blob sha256:

| File | sha256 |
|---|---|
| `corpus/knowledge/userspace-oom-killers-r12.md` | `aab7c0b81f6f231e1bb18892c98ea6c7d15205982e69720b29b8f3f487bc5e20` |
| `corpus/README.md` | `e6aa217691d16e14f9b927d372ebfaad91f6a695a4b9024e7b8c850593c773e8` |
| `corpus/knowledge/userspace-oom-killers-r26.md` | `73593455be93a6758f30c483e393707bd1e988b87fe9156e250598e33e50b9e5` |
| `corpus/knowledge/oom-kill-counter-kernel-only-r12.md` | `712db7c6f35fdd4ead745773061dfeec4445fdadaa015b8f0214b2d0439f0654` |

Final clone state: `HEAD=16935e24c93fa7e7567413d7ec091339a5df1474`, branch `r26-wt-w2mutC1`,
`git status --porcelain` empty; the counter on the restored tip reproduces the baseline
(`stale_present=0`, `r26_entry=present`, `r26_new_source_ids=13`, `r12_names_r26=4`). The 19 mutant
commits remain reachable on branches `mutant/M01` … `mutant/M19`. The lane repo was never written to
except for this report file (no `git add/commit/checkout/reset` in the lane).

## Tooling record

No package was installed or upgraded; the harness needs only bash, git and Python 3 standard library
(Python 3.14.8, git 2.56.0). No pacman transaction (host-wide pacman pause respected), no `uv tool
install`, no service restart, no network access, no change to operator settings, MCP files, systemd
units or fleet scripts. No `jj` command was run.

## Files written

- This report: `.ufo/waves/round-26/w2/MutC1Script.md` (lane).
- Sandbox clone: `/fast/scratch/hyaku/mori-r26/wt-w2mutC1` (19 mutant commits on `mutant/*`, working
  tree restored to the base commit).
- Harness and evidence: `/fast/scratch/hyaku/mori-r26/MutC1Script/{mutate_c1.py, count-c1-local.sh,
  results.json}`.
