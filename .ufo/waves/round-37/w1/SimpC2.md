# SimpC2 — round-37 w1 (UFO-FSD simplifier, godspeed seat)

Scope attacked: `tools/mori-source-drift.py` round-37 additions (the `huge_cap` and
`redirect_private_refused` selftest arms, diff 1caa242→e57c58b = +20 lines) and
`.ufo/waves/round-37/count-c2.py` (new file this round).

Axes: weight (dead code, duplicate checks), convention (one authority per decision),
contract preservation (P-C2 counter behavior, selftest arm semantics), provenance.

Reference policy: no Python LSP server answers in this environment, so semantic-absence
proofs use the verified-contract method instead — `fetch()`'s documented/implemented
return shape plus end-to-end execution of mutated copies. Text grep used only to locate
call sites (3 `selftest(` calls in count-c2.py; `probe_timeout` nowhere but the docstring).

## Measurements

Baseline (pristine lane, read-only):
```
$ python3 .ufo/waves/round-37/count-c2.py e57c58b57c025364e79d130fbdf764d2674d83d6
check tool_present   PASS
check selftest       PASS (exit=0 arms=[6 arms incl. huge_cap, redirect_private_refused])
check cap_kill       PASS (exit=1 huge_cap=FAIL)
check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
check knowledge      PASS (rows=[S205,S221..S225] cited_commit=True)
check capability     PASS   check readme   PASS   check live   PASS
C2=met   exit=0    (13.8s wall)
```

Mutant A (tool, dead conjunct removed) — copy at `/fast/scratch/hyaku/mori-r37/SimpC2/tool-mut.py`,
deletion `and body_at is not None`:
```
$ python3 tool-mut.py --selftest
selftest huge_cap PASS … MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases), exit=0
```

Mutant B (counter, `cat-file -e` pre-check deleted from `show()`) — copy
`/fast/scratch/hyaku/mori-r37/SimpC2/c2-mut.py`:
```
$ python3 c2-mut.py e57c58b…   → all 8 checks PASS, C2=met, exit=0  (13.8s)
$ python3 c2-mut.py bf0df774   → live FAIL present=False, C2=unmet (absent-path path works)
```

Ground truth: `git show e57c58b:nonexistent/path` → `fatal: … rc=128`; the surviving
`git show` check in `show()` maps that to `None` identically to `cat-file -e`.

## Ranked deletion list

1. **`tools/mori-source-drift.py:407` — `and body_at is not None`** (pure dead conjunct).
   `fetch()` (lines 140–199) returns exactly `("body", bytes)` or `("unavailable", None)`;
   `body_at is None` is unreachable when `outcome_at == "body"`, and when
   `outcome_at == "unavailable"` the arm already fails via `outcome_at == "body"`.
   Deleting changes nothing and harms nothing — the discriminating terms are
   `outcome_over == "unavailable"` (kills `1 << 40` cap mutants) and
   `len(body_at) == cap_body` (kills off-by-one cap mutants). Verified: mutant A above.
   Zero tradeoff.

2. **`count-c2.py:104–107` — `cat-file -e` pre-check in `show()`** (duplicate authority).
   `git show rev:path` already returns non-zero on absent paths → same `None`, verified at
   scored rev and absent-path rev (mutant B). The pre-check is also the *only* subprocess
   in the counter that skips `clean_env()`, so it can disagree with `show` under a
   polluted `GIT_DIR` — a small consistency win on top of the weight cut, and it halves
   git spawns (5 calls/site → −5). Convention cost: count-c1.py:611 keeps the same
   pre-check shape; deleting here leaves two conventions (harm none per-axis, still
   net-positive, but note it — or apply the same cut to c1 in its own seat's scope).

3. **`count-c2.py:127` — `selftest()`'s third return value `out` + docstring
   `probe_timeout` claim (lines 30–31).** All three call sites discard `out` (`_`/ignored;
   lines 160, 169, 176). The docstring promises "the check reports `probe_timeout`", yet on
   `ProbeTimeout` the returned string is discarded and the check detail prints only
   `exit=None` — the promised token never reaches output. Two clean resolutions, pick one:
   (a) drop the third return and trim the docstring to "never a silent pass" (pure
   weight cut); (b) surface `out` in the failing-check detail so the docstring becomes
   true (diagnostic gain, zero cost). Either removes dead weight *or* an unbacked claim.
   Ranked below 1–2 only because option (b) is arguably the better fix for reviewers.

4. **`tools/mori-source-drift.py:402–403` — split mid-expression comment**
   (`cap_body = 4 * 1024 * 1024  # the frozen cap value, literal: a mutated cap must` /
   `# not resize this fixture`). Cosmetic; fold into one line above the assignment.
   Keeps the literal (deliberate mutation-resistance choice — see keep list).

## Keep (checked, load-bearing — not deletion candidates)

- `cap_body` literal `4 * 1024 * 1024` instead of `FETCH_MAX_BYTES`: intentional — the
  fixture must not resize when the counter mutates the cap constant; comment says so.
- `at_cap` half of the `huge_cap` arm (`outcome_at == "body" and len == cap_body`):
  kills lower-cap and always-unavailable mutants; off-by-one coverage.
- `len(lines) >= 6` in the `selftest` check: pins total arm count (currently exactly 6).
- `clean_env()`, `run()` process-group kill, `mkdtemp` scratch, `argparse`/`tempfile`/
  `signal`/`shutil` imports: all used, all load-bearing (r36 debts f/g).
- `PREDICATE`, `LIVE_SENTENCE`, `HARDENING_COMMIT` constants: the bound contract.
- `routes["/redir"] = ("redir", "/fresh")` + `body % {"port":…}` at line 279: wart
  (`/fresh` lacks `%(port)s`, format is a no-op) but *pre-round-37 code* — out of scope.
- r36 `_fetchable_initial`/`_public_redirect_target`/`fetch` policies: the arms under
  measurement; not r37 additions.

## Preserved contract

Counter exit semantics (0/1/2), all eight checks, the P-C2 predicate text, and both
selftest arms' behavior are unchanged by candidates 1–4 (each verified or trivially
cosmetic). No provenance deleted — comments citing w2/SentCensus and r36 debts stay.

## Tradeoffs

- Candidate 2 creates a c1/c2 divergence unless the sibling counter follows (or is
  already justified separately — c1's use distinguishes "rename/delete" but `git show`
  gives the same `None`, so the same argument applies there).
- Candidate 3 option (b) is a behavior-visible fix (failure details gain the timeout
  string) rather than a pure deletion; either resolution is small.

## Installs

None. No tools installed or upgraded this seat. No pacman transactions (host-wide pause).

## Evidence integrity

Lane tree untouched (read-only honored): all mutations ran on copies under
`/fast/scratch/hyaku/mori-r37/SimpC2/`; the only lane write is this report.

VERDICT: PASS
