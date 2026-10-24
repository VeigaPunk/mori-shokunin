# RevNgC2Anchors — C2 mutation-anchor attack

Item attacked: whether `count-c2.py`'s text anchors reliably bind the two fetch-policy effects, including under harmless refactoring.

## Reconstructed contract and evidence

The frozen counter reads `tools/mori-source-drift.py` from the requested revision (`count-c2.py:102,151`), runs its `--selftest` on a scratch copy (`:115`), and creates two mutants with literal `str.replace` (`:50-53,168,175`). A kill passes only if the mutant exits 1 and the corresponding named arm prints `FAIL` (`:170,177-180`). The original selftest must report both arms `PASS` (`:161-164`). There is no assertion that either `replace` changed the source.

In the frozen tool, the cap is set at `tools/mori-source-drift.py:54`, applied at `:163-165`; the post-redirect check is at `:158-159`. The corresponding selftest arms call `fetch()` on local fixtures and assert behavior at `:401-416`.

Blob check: the scratch tree was archived from `e57c58b5`; its counter and tool bytes match the frozen pins exactly.

Command: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse e57c58b5:.ufo/waves/round-37/count-c2.py; git -C /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/repo hash-object .ufo/waves/round-37/count-c2.py; git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse e57c58b5:tools/mori-source-drift.py; git -C /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/repo hash-object tools/mori-source-drift.py`

Observed output:

```text
6213cf9a5ada709da8cd867581782737b2f06c71
6213cf9a5ada709da8cd867581782737b2f06c71
162ee87b5b0789c6815f967f3db93d277bab38d9
162ee87b5b0789c6815f967f3db93d277bab38d9
```

## Anchor-breaking edits: fail-closed, but brittle

Baseline command: `python3 /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/counter-v1.py c22b2d6658a3e1fc77d1792c5cd239d7963fbf57 --repo /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/repo` (scratch Git commit of the archived e57 tree).

Observed output: `selftest PASS` (all six parsed arms), `cap_kill PASS`, `redirect_kill PASS`, `knowledge PASS`, `capability PASS`, `readme PASS`, `live PASS`, `C2=met`, `RC=0`.

I made three policy-preserving edits in copies only:

| Variant | Edit preserving behavior | Frozen-counter revision | Observed output |
|---|---|---|---|
| vA | Rename `FETCH_MAX_BYTES` to `MORI_MAX_READ`, including uses | `05908bcc405ba677d462a3c5f6ae666ad449d3a3` | Command: `python3 counter-v1.py 05908bcc405ba677d462a3c5f6ae666ad449d3a3 --repo /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/repo` → `selftest PASS`; `cap_kill FAIL (exit=0 huge_cap=PASS)`; `redirect_kill PASS`; `C2=unmet`; `RC=1`. |
| vB | Change the same 4 MiB value to equivalent `4_194_304` spelling | `63ffe0a74046a5ab79b830dbea9a485035bc0bc5` | Command: `python3 counter-v1.py 63ffe0a74046a5ab79b830dbea9a485035bc0bc5 --repo /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/repo` → `selftest PASS`; `cap_kill FAIL (exit=0 huge_cap=PASS)`; `redirect_kill PASS`; `C2=unmet`; `RC=1`. |
| vC | Split `if not _public_redirect_target(final):` into `final_public = ...; if final_public is False:` | `770d4bd18e5ff947ecbaadf502ec0174cdf1f6a0` | Command: `python3 counter-v1.py 770d4bd18e5ff947ecbaadf502ec0174cdf1f6a0 --repo /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/repo` → `selftest PASS`; `cap_kill PASS`; `redirect_kill FAIL (exit=0 redirect_private_refused=PASS)`; `C2=unmet`; `RC=1`. |

Thus an anchor-breaking, equivalent refactor does **not** pass the gate: `str.replace` becomes a no-op, so the mutant retains the policy, its arm remains `PASS`, and the kill check rejects the revision. That is fail-closed, but makes the gate brittle to ordinary identifier, literal, and condition refactors.

## Anchor presence is not a semantics guarantee

Two further scratch attacks show the boundary of what the mutation check proves:

- **vD, production-path bypass.** Parameterized `fetch(url, cap=FETCH_MAX_BYTES)`; the selftest arms keep calling its default, while production `run()` calls `fetch(url, cap=None)`. I removed S109's selftest copy so its generic row-state assertion did not independently exercise the over-cap production path. The counter's anchor mutants still kill the default-path arms.
- **vE, tool-authored oracle.** Removed the read cap and redirect rejection from `fetch()`, retained the cap definition and redirect anchor as dead text/comment, and made both named arms decide `PASS`/`FAIL` by scanning `__file__` for the counter's mutation strings. The remaining six-arm selftest and corpus checks pass.

Frozen-counter commands and observed results:

- `python3 counter-v1.py 6799175ebd258d730cfff55955040391f60635b3 --repo /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/repo` (vD) → `selftest PASS`; `cap_kill PASS`; `redirect_kill PASS`; all corpus checks PASS; `C2=met`; `RC=0`.
- `python3 counter-v1.py 2efc061e686e467464deb97d6d2d4aeec836a268 --repo /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/repo` (vE) → `selftest PASS`; `cap_kill PASS`; `redirect_kill PASS`; all corpus checks PASS; `C2=met`; `RC=0`.

These are deliberate counterexamples, not claims about the frozen tool: the gate accepts them although the production path no longer enforces one (vD) or either (vE) policy. The measured limitation is that the counter proves the named selftest reacts to textual mutants, not that the policy is bound to every production call path or that the test oracle is independent of the tested tool.

## Cost of a semantics-based check

I prototyped an external CLI check in scratch: a counter-owned two-row corpus, an ephemeral loopback HTTP server, and a subprocess invocation of `tool.py --root <fixture>`. A 4 MiB+4 response with a 100-byte matching copy must classify as `unavailable`; a redirect to loopback with a matching landing copy must also classify `unavailable`. This observes production `run()` behavior and does not call the tool's `--selftest` or inspect anchor text.

Measured harness size: command `wc -l /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/semcheck.py` → `93 /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/semcheck.py`.

Observed commands/results (each was a separate `python3 /fast/scratch/hyaku/mori-r37/RevNgC2Anchors/semcheck.py <tool.py>` run):

| Tool copy | Observed output; exit; elapsed |
|---|---|
| frozen pristine | `semcheck cap=OBSERVED (S901=unavailable) redirect=OBSERVED (S902=unavailable) exit=0`; RC 0; 582 ms |
| vA rename | `semcheck cap=OBSERVED (S901=unavailable) redirect=OBSERVED (S902=unavailable) exit=0`; RC 0; 589 ms |
| vB equivalent literal | `semcheck cap=OBSERVED (S901=unavailable) redirect=OBSERVED (S902=unavailable) exit=0`; RC 0; 594 ms |
| vC split condition | `semcheck cap=OBSERVED (S901=unavailable) redirect=OBSERVED (S902=unavailable) exit=0`; RC 0; 575 ms |
| vD production bypass | `semcheck cap=VIOLATED (S901=excerpt) redirect=OBSERVED (S902=unavailable) exit=0`; RC 1; 577 ms |
| vE self-scan / policies removed | `semcheck cap=VIOLATED (S901=excerpt) redirect=VIOLATED (S902=fresh) exit=0`; RC 1; 581 ms |
| exact cap mutant | `semcheck cap=VIOLATED (S901=excerpt) redirect=OBSERVED (S902=unavailable) exit=0`; RC 1; 610 ms |
| exact redirect mutant | `semcheck cap=OBSERVED (S901=unavailable) redirect=VIOLATED (S902=fresh) exit=0`; RC 1; 588 ms |

Measured cost for this prototype: 93 lines and about 0.58–0.61 s per CLI check, using only local fixtures. **[INFERENCE]** Checking original plus both one-policy mutants at that rate would take about 1.8 s, plus integrating the fixture runner and assertions into the counter. This is not a proof against a tool that deliberately recognizes and special-cases the fixture; the server uses an ephemeral port but fixed paths, so fixture fingerprinting remains possible.

Tool installs: none.

VERDICT: PASS