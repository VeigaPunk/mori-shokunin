# Wave-2 falsification — ReRunCountC2 (C2 freeze mechanics at f2de0eed)

Verdict: **partial** — the C2 counter, the freeze-commit identity, the blob stability and the
concatenated-assembly all hold at `f2de0eedcd60d2e354da75265ea6122bc3896073`; one sub-check fails as
written: LOG.md records no freeze hash at all at that revision (the hash first enters LOG.md two commits
after the first tool-run evidence commit).

## 1. Counter re-runs (from /tmp; working-tree script, sha256 `a7536fc5a404…`, byte-equal to
`git show f2de0eed:.ufo/waves/round-28/count-c2.sh`)

`bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-28/count-c2.sh 6ebd518f`:

```
rev=6ebd518f10e53057da926353d99442d51267ccaf
tool_blob=3fb78bbc2612c38e463e04083bdb213954647568
frozen_blob=match
frozen32_selftest=PASS 32/32
freeze_commit=none
freeze_path=none
freeze_adds=0
freeze_adds_raw=0
freeze_renames=0
freeze_deletes=0
freeze_edits=0
freeze_blob_versions=0
cases_changed_since_freeze=1
a2_schema=absent
a2_cases=0
a2_selftest=absent
C2=unmet
exit=1
```

`... f2de0eedcd60d2e354da75265ea6122bc3896073`:

```
rev=f2de0eedcd60d2e354da75265ea6122bc3896073
tool_blob=3fb78bbc2612c38e463e04083bdb213954647568
frozen_blob=match
frozen32_selftest=PASS 32/32
freeze_commit=d21b8bd38b1bf72ec903a19ed543c615564e8278
freeze_path=tools/fixtures/mori-oom-killers/cases-a2.json
freeze_adds=1
freeze_adds_raw=1
freeze_renames=0
freeze_deletes=0
freeze_edits=0
freeze_blob_versions=1
cases_changed_since_freeze=0
tool_blob_at_freeze=3fb78bbc2612c38e463e04083bdb213954647568
a2_schema=ok
a2_cases=30
a2_ids=unique
a2_distinct_inputs=30
a2_rules_covered=10/10
a2_A2-01=cases=3 distinct=3 field=3 nonactive=0
a2_A2-02=cases=3 distinct=3 field=3 nonactive=0
a2_A2-03=cases=3 distinct=3 field=3 nonactive=0
a2_A2-04=cases=3 distinct=3 field=3 nonactive=0
a2_A2-05=cases=3 distinct=3 field=3 nonactive=0
a2_A2-06=cases=3 distinct=3 field=3 nonactive=0
a2_A2-07=cases=3 distinct=3 field=2 nonactive=0
a2_A2-08=cases=3 distinct=3 field=3 nonactive=2
a2_A2-09=cases=3 distinct=3 field=3 nonactive=0
a2_A2-10=cases=3 distinct=3 field=3 nonactive=0
a2_rule_checks=ok
a2_selftest=PASS 30/30
C2=met
exit=0
```

Matches the contract's declared before/after (`a2_cases=0`/`unmet`/exit 1 at `6ebd518f`; `met`/exit 0 at
tip). Note A2-07 `field=2`: only 2 of 3 cases pin `earlyoom.earlier_invocation_send_lines` — the counter
requires ≥1, so `met` still holds.

## 2. Freeze commit — holds

- `git log --diff-filter=A --follow -- tools/fixtures/mori-oom-killers/cases-a2.json` → exactly one
  commit: `d21b8bd38b1bf72ec903a19ed543c615564e8278` (2026-10-22 15:50:55 -0300). The counter's
  `--full-history -m` pass agrees (`freeze_adds=1`, `freeze_adds_raw=1`, `freeze_renames=0`,
  `freeze_deletes=0`, `freeze_edits=0`, `freeze_blob_versions=1`).
- `git show --stat d21b8bd` → touches only `LOG.md` (+2) and `cases-a2.json` (+1287). No tool or
  reader changes ride along — it is its own batch.
- Blob identical: `git rev-parse d21b8bd:…/cases-a2.json` = `git rev-parse f2de0eed:…/cases-a2.json` =
  `7ba553d45e3b00d507e57132cc3c28fb140f83fd`; `cases_changed_since_freeze=0`; sha256 of the bytes =
  `ec04a74a3eb6…` (verified).
- `git merge-base --is-ancestor d21b8bd f2de0eed` → yes; `d21b8bd^` = `7b75f45a` (the counter commit,
  15:50:53) — so the counter is committed before the cases, and all ten `CaseA2rNN.md` reports were
  already committed at `7b75f45a` before the freeze. Between freeze and tip there is exactly one
  commit: `f2de0eed` itself, the first tool-run evidence commit (adds `evidence/c2-freeze-selftest.txt`,
  which reads "first tool run, 2026-10-22T18:51:02Z … PASS 30/30 … exit=0").

## 3. LOG.md freeze-hash ordering — not met as written (one finding)

- At `f2de0eed`, LOG.md contains the freeze-batch line added by `d21b8bd` itself
  (`git show f2de0eed:LOG.md` lines 1887–1888): "C2 freeze batch (committed 2026-10-22T18:50:55Z by the
  L1) … 30 cases … no tool run on it exists before this commit." — a timestamp and count, **no hash**.
  `grep -n 'd21b8bd\|7ba553d4'` on `git show f2de0eed:LOG.md` returns no match (exit 1).
- `f2de0eed` does not touch LOG.md at all (its stat: 6 files, LOG.md absent).
- The first hash record is the 8-char `d21b8bd3` in working-tree LOG.md:1889 ("Measured at `6b695b02`:
  … C2 freeze `d21b8bd3`, first tool run `PASS 30/30` …"), added by commit `84abe93e` (15:55:05); the
  full 40-hex hash + sha256 `ec04a74a…` enter at LOG.md:1893–1895 via `ac696ad3` (15:57:40,
  `git log -S 'd21b8bd38b1bf72ec903a19ed543c615564e8278' -- LOG.md`). Both are *after* `f2de0eed`
  (15:51:32), the first tool-run evidence commit.
- The L1 disclosed this at LOG.md:1893–1895: "freeze commit `d21b8bd38b1…` … (the freeze batch's LOG
  line named a time and a count but no hash)."
- Assessment: the contract line "the freeze hash is written to `LOG.md` in the freeze commit's own
  batch" is unsatisfiable as literally written (a commit cannot contain its own hash); a timestamp pin
  is weaker than a hash since committer dates are freely settable [INFERENCE]. F8's intent (compare the
  counter's printed `freeze_commit`/`tool_blob_at_freeze` against a LOG pin before runs) is only
  satisfiable retroactively here. The operative ordering — freeze committed before any tool run on the
  cases — does hold in the commit graph. Working-tree runs before `d21b8bd` cannot be excluded by git
  alone [INFERENCE]; the LOG line asserts none existed.

## 4. Concatenation / no-L1-edits — holds

Extracted each report's first fenced block that parses as a JSON array (bytes at `d21b8bd`), in rule
order r01–r10 (script: `/fast/scratch/hyaku/mori-r28-w2/ReRunCountC2/concat_check.py`):

- 10 reports × 3 cases = 30, each report's cases all `rule` = A2-0N matching its slot; ids
  `a2-0N-<slug>`, unique; concatenated order matches the frozen `cases` order exactly.
- `concat == frozen["cases"]` → True (parsed deep equality).
- Byte proof: the frozen file equals `json.dumps(frozen, indent=1)` + `"\n"`, and also equals
  `json.dumps({**frozen, "cases": concat}, indent=1)` + `"\n"` — i.e., the file is a canonical
  serialization of `{schema, frozen_with, note, cases}` with the `cases` array identical to the writer
  concatenation. Only the three sibling metadata keys are L1-authored (the `note` key itself states
  "Assembled … without edits … (first fenced JSON array of each, in rule order)").
- All ten report blobs identical between `d21b8bd` and `f2de0eed` (e.g. r01 `a06041ef…`, r10
  `a8736202…`); the writers' bytes never changed after the freeze.

## Residual risk / out of my scope

- Blindness disclosure (LOG.md:1894–1897): CaseA2r03 read `w1/CriticC2Design.md` lines 1–45 (tool
  output columns) before writing; r01 after finalising; r07 read the round-27 counter; r04–r07 read the
  round-28 contract, which carries the tool-derived A2-07 field fact. No seat claims to have read
  `tools/mori-oom-killers.py` itself; whether the disclosed exposures taint the cases is the A2
  judge-seats' call, not mine.
- `A2-07 field=2` (1 of 3 cases lacks the rule-named pin; counter needs ≥1) — acceptable by the
  counter's rule but worth noting for completeness.

## Tooling record

No installs. Used system `git` (read-only: `show`, `log`, `rev-parse`, `ls-tree`, `merge-base`,
`cat-file` via the counter), `python3` (system, `-I -B`), `sha256sum`. Scratch under
`/fast/scratch/hyaku/mori-r28-w2/ReRunCountC2/`. Repo-wide `grep` bg job hit a 60s timeout and was
superseded by targeted `git show` greps; no information lost.

Report: .ufo/waves/round-28/w2/ReRunCountC2.md
