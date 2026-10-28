# Mo60Reviewer06 — H1 grammar-routing review (round 60, wave w1)

Seat scope: verify that the hardened r60 entry-claims verifier's H1 grammar arm
actually blocks a malformed claim line appended to the real entry, and that the
r59 counter (frozen at its data revision) reproduces the routed hole — the
grammar reason was produced but orphaned by the met verdict.

Read-only over the lane. No lane VCS mutation, no fleet/sibling writes, no
commits. All money commands ran from
`/fast/scratch/hyaku/mori-r60/Mo60Reviewer06` (`$S` below); the lane was read
through `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show`; every git
write ran in the throwaway clone `$S/repo` (`git clone --no-local <lane> repo`,
`git -C "$S/repo" rev-parse --show-toplevel` →
`/fast/scratch/hyaku/mori-r60/Mo60Reviewer06/repo` before each commit).

## Pins used (every derivation is revision-pinned)

| object | pin |
|---|---|
| contract | `ac496c7cde8cad965079858accae3bedfe4a73f2` (amended freeze) |
| frozen counter `count-c2.py` | sha `8c4814f5…` — byte-identical at `ac496c7c` and tip `b3c25613` |
| contract bytes | sha `a444e270…` — byte-identical at `ac496c7c` and tip `b3c25613` |
| verifier `tools/mori-entry-claims-check.py` | sha `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` == `PIN_EC`, identical at `ac496c7c` and `b3c25613` |
| entry `corpus/knowledge/wave-settlement-artifacts-r59.md` | sha `441a751de67f1cef9db265666a6f77734d7a9d964fe2efcf3756e4394716ce21` — identical at `ddfb12fb`, `7b86704d`, `ac496c7c`, `b3c25613` |
| r59 counter | `git show 7b86704d…:.ufo/waves/round-59/count-c2.py` → sha `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be` (464 lines; tool at that rev absent, as expected) |

## F1 — VERIFIED: H1 blocks a malformed claim line (real entry, pinned rev)

Driver `$S/h1_direct.py` materialized `ENTRY + corpus/SOURCES.md + 6 copies` at
`ac496c7c` and executed the *pinned* tool blob exactly as `count-c2.py`'s
`run_pinned` does. Entry has 47 lines; variants append one line at line 48.

```
rev=ac496c7c… tool_sha=cffe9f33…e6e69 pin_match=True
baseline (real entry):          exit=0 ok=True  reasons=[]  stats claims=13 files=6 spans=13 min_span=12
V1 "- **K99** — dangling claim with no pin or span":
                                exit=1 ok=False reasons=["grammar:- **K99** — dangling claim with no pin o"] other=[]
V2 "- **K98** — … pin not-a-sha":
                                exit=1 ok=False reasons=["grammar:- **K98** — claim whose pin field is not"] other=[]
```
No collateral reasons: the grammar line is the only delta, stats unchanged
(13/6/13). Arm: `tools/mori-entry-claims-check.py:112-117`
(`if "**K" in ln or (ln.lstrip().startswith("-") and "Quote:" in ln)`).

End-to-end counter confirmation at the *r60 tree*: commit
`f4702151ff537a63e8bc926afa06dac8719bcfc4` (= tip `b3c25613` + the same one
line; entry sha `4e89aa9723a1ebe463b38a3cefa42d0947f898f980de32d9008eb0617b7de0ac`):

```
python3 <lane>/.ufo/waves/round-60/count-c2.py f4702151… --repo $S/repo --scratch $S/rs60-var
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok tree=ok \
claims=13 files=6 spans=13 rev=f4702151… failed=entry         (exit 1)
```
Baseline at the same tip and at the amended freeze rev are byte-equal to the
frozen evidence:
```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=b3c25613…   (exit 0)
C2=met … spans=13 rev=ac496c7c…   (exit 0)   == .ufo/waves/round-60/evidence/c2-at-freeze.txt (byte-equal)
```
Arm: `count-c2.py:329-332` — `entry_ok` requires `p.returncode == 0 and
out["ok"] is True` and the stats floor, so an unparseable/absent tool verdict
is fail-closed, and a grammar reason can never ride a met verdict.

## F2 — VERIFIED: the r59 hole is "reason emitted, verdict orphaned"

Same variant bytes driven through the r59 counter imported from the pinned
blob (`$S/r59-count-c2.py`):

```
r59 eval_entry V1: ok=False claims=13 files=6 reasons=['grammar:- **K99** — dangling claim with no pin o']
r59 eval_entry V2: ok=False claims=13 files=6 reasons=['grammar:- **K98** — claim whose pin field is not']
```
So detection existed in r59. The orphaning is in `measure()`, at the pinned
rev's `r59-count-c2.py`:

- line 122 — `reasons.append("grammar:%.40s" …)` (reason produced);
- line 300 — `entry_ok_all, reasons, stats = eval_entry(root)` — the returned
  `ok` is discarded;
- lines 303-306 — `entry_ok = not any(r.startswith(("frontmatter","distinct",
  "claims_min","files","span","entry_absent")) for r in reasons)` — the prefix
  tuple has no `"grammar"`, so a grammar-only failure computes `entry_ok=True`
  and line 309 never appends `entry` to `failed`.

I extracted that exact expression from the pinned source with `ast`
(`get_source_segment`) and evaluated it on the reasons r59 itself returned:

```
r59 measure entry_ok expression: not any(r.startswith(("frontmatter", "distinct", "claims_min",
                                         "files", "span", "entry_absent"))
                           for r in reasons)
V1: r59 measure entry_ok=True  -> "entry" appended to failed = False
V2: r59 measure entry_ok=True  -> "entry" appended to failed = False
```
`grep -n grammar r59-count-c2.py` shows the counter's only runtime mention is
line 122 (plus docstring/selftest); `measure()` never reads it.

End-to-end reproduction of the routed hole on the r59 tree: commit
`0ccec4946ad79b3780601b316a014d8657adb5b5` (= `7b86704d` + the same one line;
entry sha `4e89aa97…de0ac`, byte-identical to the r60 variant above):

```
python3 $S/r59-count-c2.py 0ccec494… --repo $S/repo --scratch $S/rs59-var
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok \
claims=13 files=6 rev=0ccec494…                                  (exit 0)
```
Baseline `7b86704d` in the same clone is also `C2=met … claims=13 files=6
rev=7b86704d…` (exit 0). Net: identical malformed entry bytes
(`4e89aa97…`) score **met** under the pinned r59 counter and **unmet
(failed=entry)** under the pinned r60 counter. The routed defect is closed.

Nuance worth recording: r59's *hostile-tree* arm was never blind — its
`t12-malformed-claim` tree expects `grammar`, and its tree verdict uses
`eval_entry`'s `ok`, so `trees=ok` in the r59 baseline already encodes that the
tree's grammar failure was seen. The orphaning was specific to the real-entry
arm. This matches the routed wording ("a met entry could carry unlimited
malformed lines") exactly.

## F3 — LOW: H1's claim-shape heuristic has two escapes (no verdict inflation)

Seven malformed shapes appended to the pinned real entry (`$S/h1_shapes.py`;
tool run per shape, then r59 `eval_entry` on the same root):

```
S1-bullet-no-span      r60 exit=1 ok=False grammar=True  | r59 ok=False grammar=True  | claims=13
S2-broken-pin          r60 exit=1 ok=False grammar=True  | r59 ok=False grammar=True  | claims=13
S3-no-asterisk-bullet  r60 exit=1 ok=False grammar=True  | r59 ok=False grammar=True  | claims=13
S4-lowercase-id        r60 exit=0 ok=True  grammar=False | r59 ok=True  grammar=False | claims=13
S5-prose-with-marker   r60 exit=1 ok=False grammar=True  | r59 ok=False grammar=True  | claims=13
S6-quote-no-bullet     r60 exit=0 ok=True  grammar=False | r59 ok=True  grammar=False | claims=13
S7-trailing-junk       r60 exit=1 ok=False grammar=True  | r59 ok=False grammar=True  | claims=13
```
S4 is the concrete escape: `- **k96** — lowercase id, no span at all`. It is a
bullet with a bold claim-id and em-dash body — i.e. claim-shaped in the sense
of the entry grammar — yet `"**K" in ln` is case-sensitive and the line has no
`Quote:`, so it produces neither a claim nor a grammar reason. Counter-level
reproduction, same tip tree plus that one line
(`0af6e2dfc606af967a1bdb6908c250025d5f594c`):

```
python3 <lane>/.ufo/waves/round-60/count-c2.py 0af6e2df… --repo $S/repo --scratch $S/rs60-var-lc
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok \
claims=13 files=6 spans=13 rev=0af6e2df…                         (exit 0)
```
S6 (`Quote: …` at column 0 with no bullet) also escapes, but it is not
bullet-shaped, so I class it as non-claim-shaped prose, consistent with the
heuristic's intent.

Impact: none on the verdict arithmetic — an escaped line adds no claim, span,
file, pin or row, so claims/spans/files/min-span are unchanged (13/13/6/12 in
every probe) and no fabricated claim can hide behind it (any counted claim must
match `CLAIM` and then faces H2-H4). The mismatch is between the documented
predicate ("Any claim-shaped line that fails the frozen CLAIM regex makes the
entry fail", `tools/mori-entry-claims-check.py:9-11`) and the implementation's
narrower detector. The frozen `C2=met` target remains satisfied at its pinned
revisions; this is a wording/coverage residual for a future round, not a
regression against the frozen output, and I am not proposing a change to frozen
bytes.

Feasibility note only (no edit made): the real entry has 13 bullet lines and
all 13 are claim lines (`grep -c '^- '` = 13, `grep -c '\*\*'` = 13), so a
case-insensitive id detector (`\*\*[A-Za-z]\d+\*\*`) or a bare-bullet detector
would not false-positive on this entry; the frozen hostile set exercises only
the uppercase bullet shape (`trees-c2h/h02-malformed-claim/…:19`
`- **K77** — malformed claim line missing quote and pin`, expect `grammar`).

## Contextual observations (not this seat's findings, cross-reference only)

1. The pinned r59 counter writes the repo-supplied tool blob to scratch before
   any sha comparison (`r59-count-c2.py:205-206 tp.write_bytes(tool_b)`, then
   runs it unconditionally at 210/235/258; `tool_ok` only gates the `failed`
   list) —
   the same unhardened execution boundary C3's G1 arm owns. I did not
   re-litigate it here; I only note that my r59 reproduction ran that control
   path inside the sandbox clone.
2. Grammar reasons are truncated to 40 chars (`%.40s`, both counters), so the
   offending line is identifiable but abbreviated. Cosmetic.

## Residual risk

- S4 (and, by construction, any malformed line that avoids `**K` and avoids
  bullet+`Quote:`) can still accompany a met entry. Cannot inflate any counted
  quantity; can still mislead a reader of the entry.
- My shape set is a heuristic sample, not an exhaustive grammar fuzz; a
  systematic corpus of malformed claim shapes is not in this round's frozen
  trees (single malformed tree: `h02` at r60, `t12` at r59).

## Verification gaps

- I did not run `count-c2.py --selftest` in isolation; the counter's baseline
  runs report `selftest=ok`, i.e. the pinned tool's
  `ENTRYCLAIMS_SELFTEST pass=13 fail=0` matched inside the same measured run.
- All counter runs used the sandbox clone as `--repo`; the lane itself was only
  read (`show`/`ls-tree`/`cat-file`-equivalent reads). No lane scratch was
  created.

## Scratch

`$HYAKU_SCRATCH=/fast/scratch/hyaku`, seat dir
`/fast/scratch/hyaku/mori-r60/Mo60Reviewer06` (TMPDIR inside it), removed after
these receipts were copied here. Evidence logs kept inline above:
`h1-direct.log`, `h1-shapes.log`; drivers `h1_direct.py`, `h1_shapes.py`;
throwaway clone `repo` (deleted). `scripts/hyaku/disk-guard.sh status` was green
before the work (26% used, 599.6G free) and no install/update was needed.
