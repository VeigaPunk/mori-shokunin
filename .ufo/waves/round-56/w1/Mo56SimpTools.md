# Mo56SimpTools — dead-weight review (round 56, w1)

Seat: Mo56SimpTools (simplifier). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`,
reviewed at freeze tip `8be2717b0809281d07dffe83dad424a4859e0747` (entering tip
`5b295eeebd87ebd610d8d39bfe2035742f740cfa`). Detection and report only; no fleet,
lane, jj or git-index mutation was issued from this seat.

## Axes

Correctness of the five artifacts, retained behaviour (selftest tallies, counter
verdict lines), and surface weight (lines a reader must hold while checking a
claim). A deletion is kept only if it improves weight and harms none of the other
two.

## Files under review (freeze bytes, sha256 verified against `evidence/freeze-sha256.txt`)

| file | sha256 @8be2717b | wc -l |
|---|---|---|
| `tools/mori-driver-liveness.py` | `6b3dba74c639190e…ee6dd39bf7be997` | 479 |
| `tools/mori-vote-bind.py` | `8be1acdbb36cd68d…d288dfa6bca` | 447 |
| `.ufo/waves/round-56/count-c1.py` | `c4e58eedadda2f70…f127047f71d` | 208 |
| `.ufo/waves/round-56/count-c2.py` | `4b350c773a3c31e5…2492812465` | 170 |
| `.ufo/waves/round-56/controls/controls.py` | `5bf65ac0d7e70a5a…2b6a6d491` | 117 |

Working-tree bytes of all five equal the freeze bytes (`sha256sum` above matches
`freeze-sha256.txt` and the two `PIN` constants verbatim; receipt below). The
`git diff --stat` of the lane working tree at review time showed only
`LOG.md`, `SCORECARD.md`, `SHONEN.md` — integration files owned by the L1 and
other seats, not written by this seat; none of the five reviewed files appears
in that diff.

```
$ sha256sum tools/mori-driver-liveness.py tools/mori-vote-bind.py \
    .ufo/waves/round-56/count-c1.py .ufo/waves/round-56/count-c2.py \
    .ufo/waves/round-56/controls/controls.py
6b3dba74… tools/mori-driver-liveness.py
8be1acdb… tools/mori-vote-bind.py
c4e58eed… .ufo/waves/round-56/count-c1.py
4b350c77… .ufo/waves/round-56/count-c2.py
5bf65ac0… .ufo/waves/round-56/controls/controls.py
exit=0
```

### Reference proof method

The `lsp` device is **not mounted in this session** (`write xd://lsp` →
`No such tool: xd://lsp`), so no semantic `references` query was possible. In its
place: an AST bare-call census (which module-level names are ever the callee of a
`Call` with a bare `Name` func) plus repo-wide text grep. Both are recorded as
literal fallbacks, never as LSP evidence.

## Baseline — frozen behaviour re-run before any edit

All runs from a materialised copy of the freeze tree (`git show` per file +
`git archive <freeze> .ufo/waves/round-56/fixtures/driver`), scratch `TMPDIR`.

```
$ python3 tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
exit=0
$ python3 tools/mori-vote-bind.py --selftest
VOTE_BIND_SELFTEST pass=16 fail=0
exit=0
$ python3 tools/mori-vote-bind.py tally --ledger corpus/knowledge/kernel-v7.3-recheck-r55.md \
    --results .ufo/waves/round-55/w1-results.json --verb RECHECK --voter Mo55Rc01 … Mo55Rc16
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
exit=0
$ python3 .ufo/waves/round-56/count-c1.py 8be2717b… --repo <lane>
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
exit=0
$ python3 .ufo/waves/round-56/count-c2.py 8be2717b… --repo <lane>
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b…
exit=0
$ python3 .ufo/waves/round-56/count-c1.py 3f494b49… --repo <lane>
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=3f494b49cde612d929e82887a48e1660c022c359
exit=0
```

Fixture malformed counts reproduced exactly as frozen (hyaku-pairing 0,
attempt-rollover 0, legacy-grammar 0, in-flight 0, malformed 5, fails-and-dead 0,
state-shapes 0, two-lanes 0, variants 0), and the do-nothing control still reads
`C1=unmet … failed=tool_absent` exit 1 at the entering tip. `controls.py` re-run
at the entering tip is byte-identical to `evidence/controls.txt` (`rc 0`,
`equals frozen receipt: True`).

The live fleet log was used as an extra, larger input for the driver probe
(read-only, `--now` pinned so ages are deterministic):

```
$ python3 tools/mori-driver-liveness.py --log /home/vgpnk/Projects/shokunin/.ufo/watchdog.log \
    --state-dir /home/vgpnk/Projects/shokunin/.ufo/state --now 1793000000
json: verdict DRIVER_LIVENESS_OK, log.lines=1730, log.malformed=0, lanes=23, rc=0
```

## Deletion candidates (each proven verdict-neutral)

"Neutral" means: the narrow existing check that carries the claim is byte-identical
before and after. For tools that is `--selftest` plus every frozen fixture JSON plus
the live-log JSON; for counters it is the printed verdict line and exit code at both
`8be2717b` and `3f494b49` and at the entering tip; for `controls.py` it is its full
stdout and exit code.

| # | site (freeze line) | dead weight | proof |
|---|---|---|---|
| D1 | `count-c1.py:57-62` | `git_ls()` — never called (the fixture walk in `materialize_fixtures` shells `ls-tree` itself) | AST census: `dead_module_defs=['git_ls']`; verdict line identical at 2 revs + enter tip; `C1_COUNTER_SELFTEST pass=1 fail=0` identical |
| D2 | `count-c1.py:121,165,187` | `evaluate()` returns a 3-tuple whose first element (the expected selftest string) no caller reads | identical verdict line at both revs + enter tip |
| D3 | `count-c1.py:88-114,127` | `materialize_fixtures()` return values `(cwd, n)` unused at the only call site; the `n` counter exists only for that return | identical verdict line at both revs |
| D4 | `count-c1.py:140` | `rc` from the fixture `run_tool` rebind never read (only `out` is) | identical verdict line at both revs |
| D5 | `mori-driver-liveness.py:112,129` | per-lane `attempts` dict — populated, never emitted (output row schema has no `attempts`) | selftest identical, 9/9 fixture JSONs byte-identical, live-log JSON byte-identical |
| D6 | `mori-driver-liveness.py:104-108` | dead guard: `ts` comes from the token `parse_ts` already accepted two lines earlier, so `if ts is None: _bad(raw); continue` cannot fire; `ts_tok` binding unused after it | same three-way byte identity as D5 |
| D7 | `mori-driver-liveness.py:207,215,220,243` | `report["rc"]` duplicates the process exit code; no in-repo reader (`grep '\["rc"\]'` over `round-56/` → none) | identical JSON **minus** the `rc` key on all 9 fixtures + live log; counter arms unaffected |
| D8 | `mori-vote-bind.py:57` | `import hashlib` — module never calls it | `--selftest` and tally line identical |
| D9 | `mori-vote-bind.py:45` | usage docstring advertises `[--disposition-cols N]`; no such argument exists in the parser | same as D8 |
| D10 | `mori-vote-bind.py:94,106` | `"seq"` field on every vote dict — never read by `final_votes`, `tally` or `extract` | selftest, tally and `extract` output identical |
| D11 | `mori-vote-bind.py:161,202,349,376,418,438` | `--min` / `min_votes` — parsed, threaded, stored as `"min"`, never used in classification and never printed | selftest + tally line identical with the flag and parameter gone |
| D12 | `controls/controls.py:13,54-62` | `import re` (only appears inside a mutant *string literal*) and `run()` (never called) | full stdout + rc identical (`identical stdout: True`, rc 0 both) |

Combined effect, `wc -l` freeze → variant:

```
count-c1.py               208 → 197   (D1-D4)
tools/mori-driver-liveness.py 479 → 475   (D5,D6; 471 with D7)
tools/mori-vote-bind.py   447 → 444   (D8-D11)
controls.py               117 → 105   (D12)
```

Exact receipts for the decisive runs:

```
$ python3 count-c1.py 8be2717b… --repo <lane>       # c1_all (D1-D4 applied)
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
exit=0
$ python3 count-c1.py 3f494b49… --repo <lane>       # c1_all
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=3f494b49cde612d929e82887a48e1660c022c359
exit=0
$ python3 count-c1.py 5b295eee… --repo <lane>       # c1_all, do-nothing control
C1=unmet selftest=bad fixtures=bad entry=bad row=bad norem=bad failed=tool_absent rev=5b295eee…
exit=1
$ python3 count-c1.py --selftest                    # c1_all
C1_COUNTER_SELFTEST pass=1 fail=0
```

```
drv_att / drv_ts / drv_both:  selftest same: True   DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
                              fixtures byte-same: True (9/9)   live byte-same: True
drv_rc:                       selftest same: True   fixtures same-minus-rc: True   live same-minus-rc: True
                              raw diff keys: ['rc']
```

```
vb_final (D8-D11):  selftest same: True | tally same: True
                    TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15
                    extract same: True
```

Variant sha256 (for byte-level reproduction by the L1):

```
5623ef7a70dbf7d93da5fabfa75492076fc66ac3ee39d06dcad07b9b34fd7ddd  count-c1.py (c1_all)
650b22371fc777c3c8bde1a8cf2e6ca99f6dbe95dbf1ffde06fdafa43b02fd35  mori-driver-liveness.py (D5+D6)
cb4b085787b1f4dde49eaf472b6ef1fcf0221da60c278753377d74ccd64fc66f  mori-vote-bind.py (D8-D11)
b810d77d2f69483dbffa1113a86f1eff9a8c0de0c504eae9e2bd63fa6f770a4e  controls/controls.py (D12)
```

`count-c2.py` was reviewed and yielded **no** deletion candidate: every import,
constant and arm is on a live path, and its only redundancy (the `PIN`/`sha`
guard) is the frozen predicate itself.

## End-to-end proof (variants + re-pin, in a scratch clone)

Because both counters pin the tool bytes, a tool deletion is *not* verdict-neutral
until the pin moves. Two scratch commits in a `git clone --shared` of the lane
(verified `rev-parse --show-toplevel` == clone dir before the first commit)
separate the two effects:

```
commit A (variants, pins unchanged), rev c1e107b8…  # full history incl. ca52426e
C1=unmet selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=c1e107b8… failed=pins   exit=1
C2=unmet selftest=bad tally=ok control=ok contrast=voted0 entry=ok row=ok rev=c1e107b8… failed=pins   exit=1

commit B (variants + PIN := variant tool sha256), rev 36142cce…
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=36142cce0d27be58b5737ef8cd3dc9b1afe22aee   exit=0
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=36142cce0d27be58b5737ef8cd3dc9b1afe22aee   exit=0
```

So the *only* consequence of D1-D11 is a re-pin of the two `PIN` constants; every
executed arm keeps its frozen value. `contrast=voted0` still holds in commit B,
i.e. the round-55 C1 counter still reads `voted=0` on the same committed bytes —
the C2 contrast survives the tool rewrite.

## Rejected candidates (deleting these would harm an axis)

1. **Cross-file helper de-duplication** (`git_show` ×3, `sha` ×2 across
   `count-c1.py`, `count-c2.py`, `controls.py`; byte-identical bodies for
   `git_show`/`sha` between the two counters, a 4-line variant in `controls.py`).
   The counters *materialise only the tool file* into `TMPDIR` and execute it
   there (`run_tool` writes `cwd/tool/tools/mori-driver-liveness.py`; `count-c2`
   writes only tool + ledger + results). A shared module would have to be copied
   too, and both counters are frozen; the move would add two more pinned files to
   save ~8 lines. Harmed axis: frozen-artifact surface. Not taken.
2. **`case()` / `CASES` de-duplication** between the two tools. Same reason, and
   stronger: each tool must remain a single self-contained file or the counters'
   materialisation breaks. **This self-containedness is a retained contract, not
   an accident.**
3. **`LAUNCH_REST_RE` unused capture groups** (`driver=`, `pid=`, `mission=`,
   `runId=`, `slot=`). They are unused values but each one is what *admits* an
   observed live-log variant (1730-line live log parses with 0 malformed); making
   them non-capturing renumbers `group(4)` (attempt) and risks the pairing logic
   for no weight win. Not taken.

## Named limits found while reading (route, do not fix here)

L1: these are limit statements plus routed items, not proposed edits — the
predicates and kill rules are frozen.

1. **The tally's second advertised verb is silently empty.** `read_ledger` only
   assigns a disposition when `verb == "RECHECK"` (`tools/mori-vote-bind.py:152`),
   so a tally run with the other grammar verb returns a *successful* all-zero line
   where the 78-row ledger is present:
   `TALLY rows=0 agree=0 double=0 single=0 zero=0 dissent=0 voters=16 bound_voters=0`
   (exit 0). The docstring says the other tables "share the same trailing shape
   here" without a demonstrated case. A future round that binds the entailment arm
   on this tool would read a green zero. Route: round 57 — either evidence the
   entailment ledger's disposition column, or refuse the unsupported verb with a
   setup exit.
2. **`--min` is inert** (D11): `--min 1` and `--min 99` print byte-identical
   lines, which is the concrete blocker on the planned ≥2-voters-per-row
   dispatch-coverage validator. Independently reported by `Mo56ExecBinderSelftest`
   (MED) and `Mo56RevBinder` (LOW); this seat adds the deletion proof only.
3. **Fixtureless selftest is green at the tool level.** With the fixtures absent a
   bare `--selftest` prints `DRIVER_LIVENESS_SELFTEST pass=2 fail=0 skipped=11` and
   exits **0**. C1 is protected because it requires the exact `pass=13 … skipped=0`
   string, but any other caller keying on the exit code would accept a run in which
   11 of 13 arms never executed.
4. **`count-c2.py` mislabels a pin failure as `selftest=bad`**
   (`count-c2.py:158` folds `"pins"` into the selftest field). Receipt from commit
   A above: every other field `ok`, `failed=pins`, yet the printed line reads
   `selftest=bad`. Verdict correct, receipt field misleading.
5. **`rc` inside the driver's JSON** (D7) duplicates the exit code and is read by
   nothing in the repo. Removed in the proven variant, but flagged LOW rather than
   recommended: it is part of the emitted object and an out-of-repo reader could
   key on it.

## Preserved contract

- C1 receipt at `3f494b49` and `8be2717b`: `C1=met selftest=ok fixtures=ok entry=ok
  row=ok norem=ok`, exit 0.
- C2 receipt at `8be2717b`: `C2=met selftest=ok tally=ok control=ok contrast=voted0
  entry=ok row=ok`, exit 0; tally line
  `TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15`.
- Entering-tip control: `C1=unmet … failed=tool_absent`, exit 1 (both original and
  de-letioned counter).
- `controls.py` stdout and exit code byte-identical to `evidence/controls.txt`
  before and after D12.
- Both tools stay single-file and executable from a lone copy (required by the
  counters' materialisation).

## Tradeoff

D1-D12 remove 30 lines and one never-true branch across four files, at the price of
one re-pin of both `PIN` constants (tool sha) and — for D1-D4/D12 — re-issuing the
counter/controls pins in a successor freeze. Under this round's rules the counters
and controls are frozen after any seat scores, so **D1-D4, D11 and D12 are proposals
for round 57**, while **D5, D6, D8, D9, D10** (tool-side, output-identical) are
eligible for L1 correction *only together with the C1/C2 `PIN` update*, which is
itself a freeze-material change. No candidate here is claimed as a fix for round 56.

## Environment / cleanup

- Scratch `/fast/scratch/hyaku/mori-r56/Mo56SimpTools/` (`work/`, `fixture/`,
  `clone/`), `TMPDIR` set inside it; disk guard reported 584.3G free before the
  heavy step (clone + 344MB tree). Removed at the end of this seat.
- One shared clone (`git clone --shared`), one `git archive` extraction into a
  `git init` fixture (toplevel asserted equal before the first commit, throwaway
  identity via `-c`/env inside the fixture only).
- No pacman (host-wide pause), no network fetch, no tool install or upgrade.
- No path written outside the scratch dir and this report.

## Findings

| # | severity | finding | file / line |
|---|---|---|---|
| F1 | MED | The tally's second grammar verb produces a successful all-zero line (`rows=0 … bound_voters=0`, exit 0) instead of refusing: `read_ledger` assigns a disposition only under the first verb, while the docstring asserts the tables share the column shape without evidence. A future entailment binder on this tool reads green zeros. | `tools/mori-vote-bind.py:152` (guard), docstring `:140` |
| F2 | MED | `--min` / `min_votes` is inert metadata: the flag is parsed and forwarded, stored as `"min"`, never used in classification and never printed; `--min 1` and `--min 99` are byte-identical. Blocker for the planned ≥2-voter dispatch-coverage validator (also reported by `Mo56ExecBinderSelftest`, `Mo56RevBinder`). Deletion proven neutral (D11). | `tools/mori-vote-bind.py:161,202,349,376,418,438` |
| F3 | MED | A fixtureless run of the probe's selftest exits 0 with `pass=2 fail=0 skipped=11`; 11 of 13 arms silently skip. C1 is safe only because it matches the exact `pass=13 … skipped=0` string. | `tools/mori-driver-liveness.py:435-436,448` (selftest skip path), observed from a fixtureless tree |
| F4 | LOW | A pinned-bytes mismatch is printed as `selftest=bad` although the selftest arm passed and `failed=pins` is the true cause. | `.ufo/waves/round-56/count-c2.py:158` |
| F5 | LOW | `git_ls()` is dead in the C1 counter (the fixture walk shells `ls-tree` directly). Deletion proven: identical verdict line at two revs and at the entering tip, identical counter selftest. Proposal for a successor (counter frozen). | `.ufo/waves/round-56/count-c1.py:57-62` |
| F6 | LOW | `evaluate()` returns a three-tuple whose first element is never read; `materialize_fixtures()` returns `(cwd, n)` never read and keeps an `n` counter only for that return; `rc` from the fixture `run_tool` rebind is never read. Deletion proven neutral. Proposals. | `count-c1.py:88-114,121,127,140,165,187` |
| F7 | LOW | Probe keeps a per-lane `attempts` dict that is populated and never emitted; and an unreachable `if ts is None` guard after the token already passed `parse_ts`. Deletion proven byte-identical on 9 fixtures and the 1730-line live log. | `tools/mori-driver-liveness.py:104-108,112,129` |
| F8 | LOW | `report["rc"]` in the probe's JSON duplicates the exit code; nothing in the repo reads it. Removal proven output-identical modulo that key; recommended only with a schema note. | `tools/mori-driver-liveness.py:207,215,220,243` |
| F9 | LOW | `import hashlib` unused; usage docstring advertises a `--disposition-cols` option the parser never defines; each vote dict carries an unread `"seq"` field. All three deletions proven neutral together with D11 (selftest, tally and extract output identical). | `tools/mori-vote-bind.py:45,57,94,106` |
| F10 | LOW | `controls.py` carries an unused `import re` (the name occurs only inside a mutant string literal) and a `run()` helper that is never called; removal leaves stdout and exit code byte-identical to `evidence/controls.txt`. Proposal (controls frozen). | `.ufo/waves/round-56/controls/controls.py:13,54-62` |
| F11 | LOW | The `lsp` device is unavailable in this session, so no semantic reference proof exists for any deletion; all absence claims rest on an AST bare-call census plus repo-wide grep, recorded as literal fallbacks. | session (no file) |
