# Mo60Reviewer02 — C3 re-derivation at freeze `ac496c7c`

Scope: re-derive C3 (operability) at freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`,
byte-compare with `evidence/c3-at-freeze.txt`, and confirm the r59 old-counter control arm
still reproduces the EXEC-MARKER. Read-only on the lane; no commits, no VCS mutation, no
fleet/sibling writes.

Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Reviewer02` (`mkdir -p`, `TMPDIR=$S/tmp`,
explicit `--scratch`). Disk guard at start: `/fast/scratch/hyaku` 26% used, 599.6G free — green.
No tool installs/updates were needed.

## Verdict

**C3 re-derives `met` at the freeze revision, byte-identically, and both arms behave as the
contract requires** — the pinned r60 counter never executes the unpinned blob, the r59 counter
still does (marker reproduced three independent ways), containment holds, and the expect-tamper
flag fires only on the tampered fixture. **No finding blocks `C3=met`.** Three non-blocking
findings (one diagnostic-honesty, two evidence/robustness), one informational note, and one
transient unattributed observation follow.

## 1. Re-derivation receipts

| Check | Command (from lane root) | Exit | Output / evidence |
|---|---|---|---|
| freeze run | `python3 .ufo/waves/round-60/count-c3.py ac496c7cde8cad965079858accae3bedfe4a73f2 --scratch $S/c3f` | **0** | `C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=ac496c7cde8cad965079858accae3bedfe4a73f2` |
| byte-compare | `cmp -l .ufo/waves/round-60/evidence/c3-at-freeze.txt $S/c3f.out` | — | **no differing bytes**; both sha256 `d6dc7e0b8ec00c2dbd764d1812bbec4e6ca2ee7d5133791e46fd80d05d82bee3` |
| determinism | second run → `$S/c3f2.out` | 0 | `cmp` with run 1 and with the committed evidence: identical |
| committed blob | `git show HEAD:.ufo/waves/round-60/evidence/c3-at-freeze.txt \| sha256sum` | — | `d6dc7e0b…` = worktree file (no uncommitted divergence) |
| selftest | `python3 .ufo/waves/round-60/count-c3.py --selftest` | **0** | `C3_SELFTEST pass=3 fail=0` (frozen requirement) |
| do-nothing control | `… ddfb12fb0838b4307c445194a844f0c4b1950195 --scratch $S/c3d` | **1** | `C3=unmet toolgate=bad containment=bad expectgate=bad cases=1 rev=ddfb12fb… failed=count_c1_absent,count_c2_absent,g1_new_skipped,g2_skipped,g3_skipped` — `cmp` with `evidence/control-c3-do-nothing.txt`: **identical** |

Instrument/pin consistency (so this is a revision-consistent read, not a working-tree guess):

- `count-c3.py` at `ac496c7c` = at `HEAD` (`b3c25613`) = worktree, sha256 `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514`.
- `PIN_C1` matches `git show ac496c7c:.ufo/waves/round-60/count-c1.py | sha256sum` → `795c1f31…ddbae`;
  `PIN_C2` matches → `8c4814f5…df976`.
- `R59_C2` at `7b86704d` → `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be` (unchanged).
- `tools/mori-entry-claims-check.py` at R → `cffe9f33…6e69` (= `PIN_EC`); `tools/mori-settlement-scan.py` at R → `4c04bf21…ac9a9` (= contract H5 pin).
- Entering-rev absence is truthful, not a token artifact: `git cat-file -e ddfb12fb:.ufo/waves/round-60/count-c1.py` → *"exists on disk, but not in 'ddfb12fb…'"* (same for `count-c2.py`).
- No absolute host path in any r60 instrument: `grep -n "/home/\|/fast/\|/tmp/" count-c1.py count-c2.py count-c3.py` → none.

## 2. Old-counter control arm reproduces the EXEC-MARKER (required check)

Reproduced **three independent ways**, so it is not a stale artifact of one scratch dir:

1. Freeze run: `$S/c3f/g1-old/st2/EXEC-MARKER` = `executed --selftest --scratch …/c3f/g1-old/st2`.
2. My own rerun of the materialized r59 counter (sha `2df3ae84…`, bytes `git show 7b86704d:.ufo/waves/round-59/count-c2.py`) against the same PoC repo at a **fresh** scratch `$S/indep/old` → `$S/indep/old/st2/EXEC-MARKER`, same content; old counter exit 1.
3. The do-nothing control run at the entering revision also leaves `$S/c3d/g1-old/st2/EXEC-MARKER` — the failing state recorded in `control-c3-do-nothing.txt` is the preserved hole, not an empty arm (note the control's `failed=` list contains only `g1_new_skipped`, never `g1_old_*`).

Counterweight (the new arm is genuinely closed): the R-pinned count-c2 run by me against the same
PoC repo (`$S/indep/g1new*`) produced `failed=` containing `tool_sha` and **zero** markers under
its scratch; `cases` accounting (1 new + 1 old + 3 containment + 1 tamper = 6) matches the receipt.

## 3. Discrimination checks (gates are not vacuous)

- **G1 no false negative:** fixture repo `$S/exp/real-tools` (rev `fb21ffc0…`) containing only the
  *real pinned* entry+scan tool bytes → pinned count-c2 output has **no** `tool_sha` / `scan_tool_sha`
  token and `selftest=ok`. So the PoC's `tool_sha` is sha-specific, not a blanket "refuse the repo".
- **G3 negative + positive controls:** pinned count-c2 against the lane at R →
  `C2=met selftest=ok scan=ok … rev=ac496c7c…` with `grep -c expect_tamper` = **0** (and that output
  is byte-identical to `evidence/c2-at-freeze.txt`, a useful independent corroboration of C2's receipt);
  against the tampered fixture (`$S/c3f/poc-expect`, rev `ecf2ac2f…`, committed
  `expect.txt` = `grammar\nTAMPERED-EXTRA\n`) → `expect_tamper:h02-malformed-claim` in stdout. The flag is discriminating.
- **G2 primitive (R-pinned module, imported from a scratch copy):** `materialize(g2,"../escape.txt")` → `False`, no `escape.txt` anywhere; `"a/b/c.txt"` → `True`; rel `"/etc/hosts-mori-probe"` (absolute) → `False`, file absent; symlinked-root → `False`; a genuine out-of-root symlink target → `contained()` `False` with nothing written.

## 4. Findings

### F1 — medium, diagnostic honesty (does not change `met`): summary tokens cannot report a real gate failure
`count-c3.py:298-306` builds `toolgate=`/`containment=`/`expectgate=` as
`"ok" if "<gate-name>" not in failed and "<x>_skipped" not in failed else "bad"`. No failure token
contains the strings `toolgate`, `containment` or `expectgate`, so those fields are `bad` **only**
when a `*_skipped` token fires; every real failure token (`g1_new_no_tool_sha`,
`g1_new_executed:…`, `g1_old_control_did_not_reproduce`, `g2_parent_escape`, `g2_inside_rejected`,
`g2_symlink_escape`, `g2_escape_written`, `g3_no_tamper_flag`) is invisible to them.

Evidence (real `main()` driven with `measure` returning unmet + each token; module copy
`$S/exp/c3-copy.py`, `PYTHONDONTWRITEBYTECODE=1`, nothing written to the lane):

```
failed=g1_new_executed:/x/EXEC-MARKER   exit=1  C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 … failed=g1_new_executed:/x/EXEC-MARKER
failed=g2_symlink_escape                exit=1  C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 … failed=g2_symlink_escape
failed=g3_no_tamper_flag                exit=1  C3=unmet toolgate=ok containment=ok expectgate=ok cases=6 … failed=g3_no_tamper_flag
```
(all seven tokens behave this way). An unmet receipt would therefore read as if all three gates
held — the same class of "summary token that cannot fail" the r59 audit flagged. The met line in
the frozen target is unaffected (it is produced from the same booleans), so the claim stands; the
fix belongs in a future revision (map each gate to its own token set, or emit the gate booleans).

### F2 — low, evidence degeneracy (closure still holds): the "symlink-parent escape" arm does not escape
`count-c3.py:215` creates `(g2/"ln").symlink_to("nowhere")` — dangling, and resolving **inside**
the root. The required `r3 is False` holds only because `contained()` (`count-c2.py:114-125`)
refuses *any* symlink ancestor: I verified `contained(root, root/"ln_in"/"f.txt")` is `False`
for a symlink pointing at an in-root directory. So the arm proves "no symlink parent", not the
escape construction the claim names; a symlink whose target is genuinely outside the root is
never exercised by the counter (I exercised it by hand: refused, nothing written). Same degenerate
construction is in C2's own selftest at `count-c2.py:437-445` (`ln -> nowhere-escape`) — flagged
here because it is the shared primitive; C2's owner may want it on that claim's record.

### F3 — low, robustness (cannot fake a pass): substring tokens collide
`count-c3.py:174` `gated = "tool_sha" in out and "tool_absent" not in out` scans the whole stdout,
and `"tool_absent"` is a substring of `"scan_tool_absent"` (`"tool_sha"` of `"scan_tool_sha"`).
Verified false-negative: PoC repo with the evil entry blob only (`$S/exp/poc-entry-only`, rev
`02670208…`, no scan blob) writes **no** marker and the entry tool *is* gated, yet the expression
evaluates `False` → would record `g1_new_no_tool_sha` and `C3=unmet`. The frozen fixture supplies
both blobs, so the met arm is unaffected; the hazard is a false negative under fixture drift, and a
real execution always leaves a marker, so it cannot create a false pass.

### F4 — informational
- `count-c3.py:259-274`'s selftest is constant-shape only (pins are 64 hex, blob contains
  `EXEC-MARKER`/`--scratch`, tamper path suffix) — it never runs G1/G2/G3. That satisfies the frozen
  `pass=3 fail=0`, but note the only G1/G2 regression detectors are the marker scan and the
  old-counter control.
- Lane hygiene observation: `.ufo/waves/round-60/__pycache__/count-{c2,c1}.cpython-314.pyc` appeared
  at 13:15:10 / 13:15:27 during the wave (gitignored via `.gitignore:3:__pycache__/`, untracked →
  no revision contamination). Not mine: every import I performed ran from copies under `$S`. Worth a
  seat reminder that importing lane counters in place writes into the lane tree, against the
  "never trust an unpinned working-tree read" discipline.

### F5 — observation (unattributed, transient): an EXEC-MARKER was written into the lane root mid-wave
At 13:17–13:18 one `git status --porcelain` in the lane showed an extra untracked `?? EXEC-MARKER`
at the lane root; the next command, seconds later, showed the lane clean and `EXEC-MARKER` absent
(`ls: cannot access 'EXEC-MARKER'`), so I could not read it or attribute it. Not mine: every arm I
ran passes `--scratch` (all markers landed only at `$S/…/st2/EXEC-MARKER` and were removed with the
scratch), and no process of mine executed a PoC blob with a lane cwd. The only write path that
produces that file is the `EVIL_BLOB` fallback `base = sc if sc is not None else pathlib.Path(".")`
(`count-c3.py:62-70`) — i.e. some in-flight seat ran the PoC tool without `--scratch` while cwd was
the lane root. Recorded as a live observation for the L1: G1's motivating failure mode is reachable
inside the wave, not only on paper. No remediation performed; nothing in the lane was touched by me.

## 5. Residual risk / verification gaps

- G2's "nothing written outside the scratch root" assertion is narrow: it checks only
  `<scratch>/escape.txt` and `g2/nowhere/f.txt` (`count-c3.py:218,227`); an escape to any other
  name/path would go unnoticed. The refusal itself is solid (verified `..`, absolute rel, symlink
  parent, symlinked root — all refused, nothing written).
- `materialize()` is check-then-write (TOCTOU). Not reachable from repo bytes here: hostile trees
  materialize regular-file bytes only, and git cannot store a `..` component or create a symlink
  through this path. Noted only.
- `contained()` fail-closes if the scratch root is reached via a symlinked ancestor; `/fast/scratch/hyaku`
  is a real directory (`readlink -f` returns itself), so not triggered.
- The hole reproduction rests on the r59 counter at `7b86704d` (sha `2df3ae84…`, committed); no arm
  I exercised executed an unpinned working-tree blob.

## 6. Hygiene

- Lane untouched: the final `git status --porcelain` shows only pre-existing untracked entries
  (`evidence/c1-at-data.txt`, `w1.ready*`, `w1/`); no commits, no `git` mutation, no fleet/sibling
  writes. Fixture repos were created only under `$S` with explicit `git -C <path>` (toplevel asserted
  by `make_fixture_repo` and re-checked by me: `/fast/scratch/.../exp/real-tools`). One transient
  `EXEC-MARKER` appeared at the lane root at 13:18 and was gone at the final check — unattributed,
  not mine (F5).
- Scratch receipts used above are quoted inline; scratch removed after filing.
