# RevR17JJ — r36 routed debt (d): `mori-round17-jj-regressions.py` scoped side-effect assertion

Date: 2026-10-23 · Seat: mori-r37-w1-RevR17JJ · Tip attacked: e57c58b57c025364e79d130fbdf764d2674d83d6

## What this item attacks

The r37 claim that the r36 routed defect (d) is resolved: the `jj_config_redirected`
side-effect assertion in `tools/mori-round17-jj-regressions.py` was rescoped (r36 w2 ran
9/204 red because the old assertion demanded positive jj-file evidence that cannot fire in
git-only sandboxes) and must still have teeth — i.e. it must reject a run whose config
redirect leaks outside the case home. The r37 rescoping lives at
`tools/mori-round17-jj-regressions.py:1041-1069`: `redirect_ok` requires `HOME`,
`XDG_CONFIG_HOME` (`<case home>/.config`), and `JJ_CONFIG` (`<case home>/jjconfig.toml`)
all resolved inside the case home, the case home to be neither the operator's home nor an
ancestor of it, and — only when a jj workspace exists — positive `.config/jj` evidence.

## Measurements

### M1 — Lane selftest (assigned command)

```
command: cd mori-shokunin && python3 tools/mori-round17-jj-regressions.py --selftest --scratch .ufo/waves/round-37/scratch-rev
observed: "SELFTEST ok: guard_output_repo_root,…,ok_failed_zero,…"  EXIT=0
```

Lane selftest exit code: **0**.

### M2 — Honest run retains `jj_config_redirected` in the assertion universe

```
command: python3 tools/mori-round17-jj-regressions.py --selftest --keep-scratch --scratch /fast/scratch/hyaku/mori-r37/RevR17JJ/lane-keep
observed: SELFTEST ok, EXIT=0; out-ok/run-manifest.json: 17 cases, all "match", failed=0;
          "jj_config_redirected" ok=true in all 9 jj-* cases, absent (skipped) in the 7
          git-only cases ("jj" not in tools — resolve_tools finds no jj there is false;
          jj IS present at ~/.local/bin/jj, so the check genuinely fires in jj cases).
detail sample (jj-commit-no-bookmark): home=<case>/home
          xdg=<case>/home/.config jj_config=<case>/home/jjconfig.toml
          jj_workspace=False operator_home_inside=False
```

Denominator is 204 assertions (matches the receipt `.ufo/waves/round-37/evidence/r17-jj-selftest-r37.txt`:
pre_fix 9/204 red, post-fix exit 0 — reproduced independently here).

### M3 — Mutant: `census_env` XDG escape

Built in scratch only (lane untouched; `mutant-jj-regressions.py` is a byte copy of the
lane tool except one line). Mutation at the `census_env.update` block
(lane line 457; the copy's identical-text line in `sanitized_env()` at lane line 225 was
left intact so only the census override env leaks):

```diff
             "HOME": str(home),
-            "XDG_CONFIG_HOME": str(home / ".config"),
+            "XDG_CONFIG_HOME": str(home.parent / "leaked-xdg"),
             "XDG_CACHE_HOME": str(home / ".cache"),
             "JJ_CONFIG": str(home / "jjconfig.toml"),
```

`home` is the case home, so `home.parent / "leaked-xdg"` points XDG_CONFIG_HOME outside
the case home (into the case dir), simulating a redirect leak that could collide across
cases / escape the per-case sandbox.

```
command: cd /fast/scratch/hyaku/mori-r37/RevR17JJ && python3 mutant-jj-regressions.py --selftest --keep-scratch --scratch ./scratch-mutant
observed: SELFTEST FAIL: ok_rc0: rc=1 … cases=17 match=8 mismatch=9 … assertions=204 failed=9
          ; ok_failed_zero: failed=9; keep_rc0: rc=1
          EXIT=1
```

Mutant result: **assertion fails** — `jj_config_redirected` goes red in exactly the 9
jj-* cases (each `failed=1`, sole red assertion; the 7 git-only cases stay `match`,
failed=0), the selftest-level `ok_rc0` / `ok_failed_zero` / `keep_rc0` arms then fail, and
`--selftest` exits 1 (`run_selftest` failure path,
`tools/mori-round17-jj-regressions.py:1775-1779`; case-level gate `ok_failed_zero` at
`:1688-1689`). Red detail confirms the tripwire fired on the right conjunct:
`xdg=<case>/leaked-xdg` (≠ `<case>/home/.config`), everything else unchanged.

### M4 — Control: layout neutrality

```
command: cp tools/mori-round17-jj-regressions.py control-jj-regressions.py   # sha256 7ca4a1ac…bf016, byte-identical to lane tool
         python3 control-jj-regressions.py --selftest --keep-scratch --scratch ./scratch-control   (same cwd/layout as mutant)
observed: SELFTEST ok, EXIT=0
```

The unmutated copy run from the identical scratch layout exits 0, so the mutant's failure
is attributable solely to the one-line XDG escape.

## Findings by severity

None. No defect found in the scoped assertion.

- The rescoped `jj_config_redirected` assertion is live (fires in all 9 jj-cases, M2),
  passes on the honest gate (M1, M2), and kills the targeted XDG-escape mutant on exactly
  its property conjunct with full selftest propagation to exit 1 (M3). The r36 routed debt
  (d) closure claim holds.

## Residual risk

- The workspace-positive conjunct (`tools/mori-round17-jj-regressions.py:1062-1063`:
  require `<case home>/.config/jj` to exist when `.jj/repo/config-id` is present) is never
  exercised by the selftest — every sandbox is git-only by design, `jj_workspace=False`
  in all 9 details (acknowledged in the in-code comment at `:1041-1049`). A regression
  confined to that branch would not be caught by `--selftest`. This is a coverage gap of
  the fixture universe, not a defect of the landed assertion; my mutation attacked the
  env-conjunct path, which is the only path the selftest can express.
- The assigned M1 command left an empty parent dir `.ufo/waves/round-37/scratch-rev/`
  in the lane (selftest removes its mkdtemp work tree but creates the `--scratch` parent;
  verified empty). Harmless, allowed territory (.ufo/waves), no lane file mutated.

## Verification gaps

- No selftest case carries a jj workspace, so the positive-file-evidence branch is
  unverifiable through `--selftest` alone; verifying it would require a workspace-carrying
  fixture case (out of scope for this reviewer seat; detection only).

## Tooling installs

None (no pacman, no uv/cargo/npm installs; only `cp` of the lane tool into scratch).

Scratch artifacts retained under `/fast/scratch/hyaku/mori-r37/RevR17JJ/`:
`mutant-jj-regressions.py`, `control-jj-regressions.py`, `lane-keep/`,
`scratch-mutant/mori-r17-jj-selftest-vdt_2w34/` (mutant manifests),
`scratch-control/mori-r17-jj-selftest-ar5i0pfv/`.

VERDICT: PASS
