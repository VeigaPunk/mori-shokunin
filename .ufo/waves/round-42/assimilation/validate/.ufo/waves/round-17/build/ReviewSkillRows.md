# SKILL.md registry review — round 17

**Seat:** `MoriR17.ReviewSkillRows-5` · **Date:** 2026-10-20  
**Scope:** Review the registry pattern, propose contract-accurate C1/C2 entries, and check the existing “no hidden flags” wording against the available CLI sources. No source or registry files were edited; this report is the only write.

## Verdict

The registry’s eight-column format at `SKILL.md:162-163` supports the three new command surfaces: C1 seat-status probe, C1 regression gate, and C2 census-regression gate. C2 itself modifies the existing `census` entry; it is not a separate production CLI. The rows below use only the round-17 contract and explicitly leave unspecified exit codes, self-tests, and digest pins unspecified rather than carrying forward old tallies.

**The delivered implementation could not be reviewed:** `tools/` has no `mori-seat-terminal.py`, `mori-round17-seat-regressions.py`, or `mori-round17-jj-regressions.py`; the round-17 fixtures directory is absent. The searched round-17 worktrees likewise contain no C1 tool or either named regression gate. The only matching `mori-round17-*.py` found there was `mori-round17-context-check.py`, a different tool. Thus the proposed entries are contract-derived, not observed runtime behavior, and no claim that the new CLIs have “no hidden flags” is supportable yet.

The sentence called the “r16 no hidden flags” sentence is actually in the **r15 regressions** row (`SKILL.md:169`); rows 170–172 register r16 tools and do not make that claim. The r15 wording is partly too absolute (finding below).

## Finding (low severity)

**`SKILL.md:169` overstates strict rejection of CLI input.** `tools/mori-round15-regressions.py:2306-2320` constructs a default `argparse.ArgumentParser` and calls `parse_args`; it does not set `allow_abbrev=False`. The parser declares `--output` at line 2312. **[INFERENCE]** Python argparse’s default permits unambiguous long-option prefixes, so `--out` can be treated as `--output`; “any unknown argument is refused” is not a safe literal claim unless “unknown” means unrecognized after abbreviation. In addition, the `--selftest` guard at lines 2325–2328 tests `args.output or args.pin_fixtures`, not whether either option was supplied. **[INFERENCE]** An empty-string value can therefore bypass that guard. The named removed switches (`--selftest-child`, `--no-frozen-control`) are absent from the parser text, but the broader rejection wording is not established by that fact.

Minimal correction: either make the parser strict and check option presence, or narrow the registry sentence to the verified removal of those two switches and accurately describe the current guard. Do not generalize this r15 statement to r17 CLIs.

## Contract-derived candidate registry rows

These are proposed rows, not evidence that the implementations or gates have landed. `not specified` below is intentional; do not replace it with an assumed `--selftest`, exit code, or digest pin.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| seat terminal status (r17 C1) | probe | `python3 tools/mori-seat-terminal.py --sessions-dir DIR [--prefix P ...] [--max-tail-bytes N] [--max-files N]` (or `--selftest`) | 0 scan complete with zero `dead_*` · 1 complete with ≥1 `dead_*` (`MORI_SEAT_TERMINAL_DEAD`) · 2 setup/unavailable directory (`MORI_SEAT_TERMINAL_SETUP`) | `--selftest` is specified; result/tally not observed | none specified | none: read-only; one JSON document on stdout; bounded regular `*.jsonl` tails, no symlink following, no emitted `errorMessage` text/content/usage | mori |
| r17 seat regressions | gate | `python3 tools/mori-round17-seat-regressions.py --tool PATH --fixtures DIR --output DIR` | 0 only when every case matches · missing tool path gives rc1 and `capability_absent` for every case · other mismatch/setup rc not specified | not specified by contract | `.ufo/waves/round-17/fixtures/seat/expected.json` provides expected per-case rc/finding/totals/seats; no digest pin specified | writes `run-manifest.json` under `DIR`, with per-case status and input SHA-256 before/after; other output files not specified | mori |
| r17 jj census regressions | gate | `python3 tools/mori-round17-jj-regressions.py --census PATH --output DIR` | counts failed case assertions; exit mapping not specified by contract | not specified by contract | compare entering census (`git show 24526ea:tools/mori-census.sh`) with delivered census; no digest pin specified | `DIR` evidence plus gate-owned temporary colocated-jj sandboxes outside the lane/fleet | mori |

**Existing census row:** retain one `census` entry. Once delivered behavior is reviewed, add its C2 summary there: resolve the lane branch by the contract’s fallback chain, use `refs/heads/<branch>` for report-closure and authorship probes, and report `HEAD_BRANCH_MISMATCH` / `LANE_AUTHOR_MISMATCH` as drift. Keep the existing `104/104 at 8d22d18` value at `SKILL.md:164` explicitly historical (r14); it is not evidence for C2. Only append the delivered census digest and measured r17 gate result after L1 records them.

## Evidence and verification gaps

- `SKILL.md:162-172` — existing registry columns and r13–r16 row patterns; `SKILL.md:169` is the r15 no-hidden-flags sentence, while `:170-172` are r16.
- `contract.md:24-67` — C1 tool CLI, field/output restrictions, classes, and exits; `:69-78` — C1 fixtures/gate; `:80-94` — C2 behavior and regression-gate interface.
- `tools/mori-round15-regressions.py:2306-2328` — parser options and selftest guard.
- `jj -R /home/vgpnk/Projects/shokunin/mori-shokunin status` — successful read (rc 0): modified `.gitignore`, untracked `.ufo/waves/round-17/`.
- `jj -R /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat` and `jj -R /home/vgpnk/Projects/shokunin/mori-shokunin diff --git` — successful reads (rc 0): only `.gitignore` changed, adding `.ufo/worktrees/`; no `SKILL.md` or tool-source diff.
- `glob` of lane `tools/` showed only pre-round-17 source CLIs; literal `grep` for C1/C2 names under that directory found no matches. Round-17 fixture path lookup returned not found. Literal searches are fallback location checks, not semantic proof.
- LSP is unavailable in this session: `read xd://lsp` returned “No such tool” and the mounted-device list has no `lsp`. Consequently no LSP status, references, definition, or diagnostics were available; source conclusions above come from the directly read lines, and the new CLI semantics remain unverified.
- No CLI, selftest, test suite, or URL was run/opened. No tools were installed or updated. No VCS mutations were performed.

## Residual risk

Until the three named implementations, fixtures, and a delivered census are present, the new rows cannot be upgraded from contract-derived proposals to reviewed behavior. In particular, new parser options, abbreviated/unknown-argument behavior, selftest guards, output side effects, exact nonzero exits, and current expected-value pins remain unobserved.