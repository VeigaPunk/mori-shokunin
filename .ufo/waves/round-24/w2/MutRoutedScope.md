# Wave 2 — MutRoutedScope (C1 R2 scan scope mutation probe)

Seat: `MoriR24.MutRoutedScope`. Lane repo: `mori-shokunin` (never touched; the only file
created inside it is this report). Clone (scratch only):
`/fast/scratch/hyaku/mori-r24-a2/w2/MutRoutedScope/clone`, checked out at measured lane tip
`a730ecfefbdb5c31b1db13aca2c40eecd5e97abc` (base fixed `c725aa37...`).

Environment: `python3` 3.14.8, git 2.56.0, both already present; no tool installs were needed
or made.

## Target and mutants

Attacked invariant: the A1 design decision that the R2 added-line scan is limited to
`R2_SCAN_SCOPE = (SCORECARD.md, PROVINCE.md, SKILL.md, LOG.md, README.md, corpus/)` and
deliberately excludes `.ufo/**` and `tools/**` (quotation, not assertion). Tool:
`tools/mori-routed-check.py` (`PRIVACY_CLEARANCE_TRUE_RE` with `re.IGNORECASE`; `_added_lines`
uses the scope tuple as a git pathspec).

Two smallest behavior-bearing mutants, each applied alone:

- **Mutant A (widen):** add `".ufo/"` to `R2_SCAN_SCOPE` (scope becomes
  `(SCORECARD.md, PROVINCE.md, SKILL.md, LOG.md, README.md, corpus/, .ufo/)`).
- **Mutant B (case-sensitive):** drop `re.IGNORECASE` from the regex compile, so only
  lowercase `privacy_clearance ... true` matches.

Hashes (sha256 of `tools/mori-routed-check.py`): pristine `64921a0c30aed1d9a2a7a03c377825add37ebecd7aded8fbfe8f30c02dafbd14`;
mutant A `5b285b4f9bb16309c0a48eb34b221680949356859313c9c551e99aac581c050d`;
mutant B `3a0a0a7d619ff0a2f17c2f299c2c3bf4d14703a5b0113cc5eabcfdfff3fcbe29`.

## Run matrix (all `python3 -I tools/mori-routed-check.py --repo <clone> --rev <rev> --round N`)

| Tool | Rev | Round | held/items | exit | R2 reasons |
|---|---|---|---|---|---|
| pristine | a730ecf (tip) | 24 | 4/4 | 0 | none (claim reproduces) |
| pristine | a730ecf | 23 | 3/4 | 1 | R4 red (expected baseline failure, matches repair claim) |
| pristine | c725aa37 (base) | 24 | 3/4 | 1 | R4: no round-24 ledger |
| pristine | c725aa37 | 23 | 3/4 | 1 | R4 red (rows precede dispatch commit) |
| **A** | a730ecf | 24 | **3/4** | **1** | **`privacy_clearance_true_line_added` — 12 committed added lines** |
| **A** | d0b4f2a (T1) | 24 | 3/4 | 1 | same 12 + tamper line |
| pristine | d0b4f2a (T1) | 24 | 4/4 | 0 | `.ufo/` tamper invisible |
| **B** | a730ecf | 24 | **4/4** | **0** | none — output byte-identical to pristine |
| **B** | c725aa37 | 24 / 23 | 3/4 | 1 | parity with pristine baseline |
| pristine | b9f190d9 (T2) | 24 | 3/4 | 1 | catches `PRIVACY_CLEARANCE = TRUE` |
| **B** | b9f190d9 (T2) | 24 | **4/4** | **0** | misses the uppercase line |
| **B** | b9f190d9 | 23 | 3/4 | 1 | R4 red parity |

## Committed round-24 bytes that trip mutant A

Widening to `.ufo/**` turns R2 red at the landed tip. The tool reports 12 added lines, all in
committed round-24 wave-1 reports (quoted, not asserted): `BuildRoutedCheck.md` x2 (including
`| M2 | add `privacy_clearance: true` under `corpus/` | R2 red | ... |`) and
`ScoutRoutedBytes.md` x10 (quoting round-22/23 falsify bytes, e.g.
`'privacy_clearance':True,...`, `privacy_clearance=true`, `privacy_clearance: true`).

Independent cross-check (scratch `analyze_added.py`, mirrors the tool's `_added_lines` + regex,
base..tip): 10,352 added lines under `.ufo/` with **12 matches**; 1,692 added lines under
`tools/` with **0 matches** (so widening to `tools/**` alone would not trip); 444 added lines in
the pristine scope with 0 matches. At base, `git grep -i -E` finds exactly **9** matching lines
under `.ufo/waves/` (matches A1's count) — none of them added (diff base..base is empty), so the
widened scan is clean at base.

## Verdicts

- **Mutant A — KILLED by an existing control.** The committed tip itself (a730ecf) is the
  detector: output changes from `held: 4` to `held: 3`, exit 1. The A1 scope restriction is
  load-bearing for the declared after-value; widening the scan to `.ufo/**` would make C1 fail
  on the lane's own committed wave-1 reports. No overclaim found — the shipped restricted scope
  is what keeps `"held": 4` true, exactly as A1 says. Sensitive spot for the future: any
  committed report that quotes the pattern under `.ufo/**` breaks a widened scan.
- **Mutant B — SURVIVES the existing committed-bytes control (output identical to pristine at
  tip and base); KILLED only by a constructed tamper (T2, uppercase in scope).** No committed
  byte in the scan scope exercises the case-insensitive pathway; the `re.IGNORECASE` flag is
  currently latent. Coverage finding: an uppercase `PRIVACY_CLEARANCE = TRUE` line in a scanned
  surface would be missed by the case-sensitive variant (and is caught by the pristine tool).
- No inconclusive runs: every baseline (round-23 red / no-ledger red) reproduced identically in
  pristine and both mutants, so all comparisons are meaningful.

## Tamper commits (created in the scratch clone only)

- **T1** `d0b4f2a26d3f9aa3274d700dfaaf6a9abdbc7d68`: adds
  `.ufo/waves/round-24/w2/mutant-tamper.md` containing `privacy_clearance = true` (assertion
  under `.ufo/**`). Pristine still `held: 4` (invisible); mutant A `held: 3` (caught).
- **T2** `b9f190d96ac2e17bd2cdc0fa65dc352cd2214a80`: adds `corpus/knowledge/mutant-tamper-upper.md`
  containing `PRIVACY_CLEARANCE = TRUE` (uppercase in scope). Pristine `held: 3` (caught);
  mutant B `held: 4` (missed).

## Restoration evidence

Before each mutation and after the final probe, `git checkout -- tools/mori-routed-check.py`
restored exact bytes; final working tree is clean (`git status --short` empty) and the restored
hash equals the pristine hash `64921a0c...`. The scratch clone retains the two tamper commits
(detached HEAD, never pushed; lane repo, its git index and jj state untouched — no
add/commit/stash/checkout/reset in the lane; read-only git only).
