# RevCensus — round-38 census revalidation

## Scope

Re-run `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`,
compare with `evidence/census-start.txt`, and count registry rows at
`e33bb561712b32f46861362a3fa43762fa70ae4f` (entering tip) and
`f725f3076972e6e70595b5ac8279be524a111ff8` (scored tip).

## Result: PASS (no findings)

### Validator output vs baseline

Command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`

- **Exit code: 0** (same as baseline `CENSUS_EXIT=0`).
- Output is **line-identical** to `.ufo/waves/round-38/evidence/census-start.txt`:
  `diff` reports only `17d16 < CENSUS_EXIT=0` — i.e. the receipt's exit-code trailer;
  the 16 validator lines match verbatim.
- Composition: **15× W04** (same-URL-across-scopes warnings: S035, S037, S073, S074,
  S075, S076, S147, S148, S149, S150, S166, S168, S201, S218, S220) plus
  `mori\tok\t…/corpus/SOURCES.md`.
- **Zero E-lines**; zero new warning lines. No new error line → no FAIL trigger.

### Registry row counts

Method: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show <commit>:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3}'`.
No E12 was emitted by validate, so all `| S`-shaped rows sit inside `## Registry`.

- `e33bb561…` (entering tip): **225 rows**
- `f725f307…` (scored tip): **226 rows**
- Delta: **exactly +1** → within acceptance bound.

`git diff` between the two commits on `corpus/SOURCES.md` shows a single added row
and no removed/modified rows:

```
+| S226 | Python `os.path.realpath` documentation — https://docs.python.org/3/library/os.path.html#os.path.realpath | docs | A | … | mined | 2026-10-23 | on-release | corpus/knowledge/containment-timed-supersede-r38.md |
```

Row health corroborated by the validator itself: S226 emits no E01–E12 finding
(malformed, bad id, dup id/url, enum, date, recheck, tier-A community, dangling
used-by, out-of-section all absent) and no W0x finding — its URL joins no existing
scope and its used-by path resolves on disk. `opened=2026-10-23` is a
present-day ISO date; `recheck=on-release` is a symbolic cadence (E09-clean).

### Consistency notes

- +1 row aligns with the frontier claim "S226 opened this round".
- S226's `teaches` text asserts `supersedes S069` — consistent with C3's
  `stale_supersede` expectation; census/validate does not adjudicate supersession
  semantics (gate's domain), only row shape.

## Verification gaps / residual risk

- Row counting is textual (`| S\d{3}` rows); a maliciously crafted non-row line
  could evade the grep while still parsing as a row — but validate emits E12 for
  out-of-section rows and no E-line fired, so the count is trustworthy here.
- W04 warnings are pre-existing and unchanged; they are warnings by design
  (exit stays 0) and out of this check's acceptance.
- No tooling installed or upgraded this run.

## Lane compliance

Read-only: ran the lane's own script and `git show`/`git diff` only. Wrote exactly
one file: this report. No lane files modified; no pacman transactions.
