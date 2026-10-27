# Mo56ExecReceiptStage — round 56 w1 (routed-defect-2 machinery / receipt stamping)

Lane: mori-shokunin. Freeze tip `8be2717b0809281d07dffe83dad424a4859e0747`; entering tip
`5b295eeebd87ebd610d8d39bfe2035742f740cfa`. Read-only seat: no repo mutation, no commit, no
counter/control/contract change. Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ExecReceiptStage/`
(removed at end). No tools installed (nothing needed beyond python3/git already present).

## 1. `receipt-stage.py` — usage, run, and scope

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/checks/receipt-stage.py` accepts a
revision and an optional `--repo`:

```
usage: receipt-stage.py <rev> [--repo DIR]
Output: one FLAG line per flagged citation, then
        RECEIPT_STAGE rev=<rev8> cited_intermediate=N flagged=N
Exit 0 when flagged=0, 1 otherwise, 2 on setup error.
```

Runs performed (all from the seat scratch, absolute paths):

| command | output | exit |
|---|---|---|
| `python3 …/round-54/checks/receipt-stage.py 8be2717b… --repo /home/vgpnk/Projects/shokunin/mori-shokunin` | `RECEIPT_STAGE rev=8be2717b cited_intermediate=5 flagged=0` | 0 |
| same, at entering tip `5b295eee…` | `RECEIPT_STAGE rev=5b295eee cited_intermediate=5 flagged=0` | 0 |
| same, run from the lane root without `--repo` | `RECEIPT_STAGE rev=8be2717b cited_intermediate=5 flagged=0` | 0 |
| same, run from the fleet root `/home/vgpnk/Projects/shokunin` (default `--repo .`) | `setup: cannot read SCORECARD.md at 8be2717b…` | 2 |

The fleet root is a different git repository from the lane (`git rev-parse --show-toplevel` →
`/home/vgpnk/Projects/shokunin` vs `/home/vgpnk/Projects/shokunin/mori-shokunin`), so the literal
command in the seat brief only works when run from the lane root or with an explicit `--repo`.
Operational note only; the tool behaves as documented.

## 2. Round-55 rows: do the After cells cite the landed revision consistently?

Yes — confirmed by three independent methods.

**(a) The detector's own view.** `cited_intermediate=5 flagged=0` at both revisions. The five
intermediate citations are all in older rounds, not round 55:

```
round 50 line 2668 a2-c1-at-data      round 50 line 2669 a2-c2-at-data
round 53 line 2796 c1-at-salvage      round 53 line 2797 c2-at-salvage, c2-at-data
```

Each is covered by a `**Round-50 correction:**` / `**Round-53 correction:**` paragraph naming the
landed receipt, which is the tool's documented escape.

**(b) Direct byte check of every round-55 citation** (script over `git show 8be2717b:SCORECARD.md`,
resolving each cited `evidence/<name>.txt` to `.ufo/waves/round-55/evidence/<name>.txt` at the same
rev, then comparing the receipt's own `rev=` stamp with the revision quoted in the cell):

```
round | cell   | receipt                     | stamped rev      | cell cites    | verdict
  55  | After  | c1-at-landed.txt            | a27ec48210b13... | a27ec482      | MATCH
  55  | After  | c2-at-landed.txt            | a27ec48210b13... | a27ec482      | MATCH
  55  | Before | control-c1-do-nothing.txt    | ca52426ea496... | ca52426e      | MATCH
  55  | Before | control-c2-do-nothing.txt    | ca52426ea496... | ca52426e      | MATCH
```

The After cells name the **at-landed** receipts (not the at-data ones), and the quoted revision
equals the revision each receipt stamps. The round-55 Before cells name the do-nothing controls
at `ca52426e`, whose receipts stamp `rev=ca52426ea496bc6592e3e867cc9d28843e45f196`.

**(c) The detector is armed for round-55 rows** (positive control in a scratch fixture repo, top
level asserted before every commit): changing the round-55 C1 After cell to cite
`evidence/c1-at-data.txt` while `.ufo/waves/round-55/evidence/c1-at-landed.txt` exists yields
`FLAG line 2888 round 55 cites c1-at-data while …c1-at-landed.txt exists` /
`cited_intermediate=6 flagged=1`, exit 1. Likewise, deleting the `**Round-53 correction:**`
paragraph in the fixture yields `flagged=3`, exit 1 — so `flagged=0` on the real tree is a
suppressed-pass, not a vacuous pass.

Note (recorded, not a round-55 defect): `c1-at-landed.txt` / `c2-at-landed.txt` did not exist at
the revision they stamp (`a27ec482`); they were added later, in `d27d943a`. That is exactly the
contract's stated convention — "receipts here stamp the measured revision themselves" — so the
later commit carrying the receipt is expected.

## 3. Every round-56 receipt, and whether it stamps where it measured

Directory listing (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/evidence`, 11
files, identical at the freeze tip and in the working tree — `git diff 8be2717b -- …/evidence/` is
empty):

| receipt | `rev=` | `exit=` | stamps where measured? |
|---|---|---|---|
| `c1-at-freeze.txt` | `3f494b49cde612d929e82887a48e1660c022c359` (40) | 0 | yes |
| `c2-at-freeze.txt` | `3f494b49cde612d929e82887a48e1660c022c359` (40) | 0 | yes |
| `c2-old-counter-voted0.txt` | `5b295eeebd87ebd610d8d39bfe2035742f740cfa` (40) | 1 | yes |
| `controls.txt` | truncated to 24 and 33 hex chars on the two do-nothing lines; absent on all 8 mutant lines | **absent** | **no** — see F3 |
| `census-start.txt` | **absent** | 0 | **no** — see F6 |
| `tally-r55.txt` | **absent** | 0 | **no** — see F7 |
| `selftest-c1-counter.txt` | **absent** | 0 | no |
| `selftest-c2-counter.txt` | **absent** | 0 | no |
| `selftest-vote-bind.txt` | **absent** | 0 | no |
| `driver-liveness-live.txt` | **absent** | 0 | no (host read; anchors only the log path and `mtime_age_s`) |
| `freeze-sha256.txt` | **absent** | **absent** | pin manifest, not a measurement — see F5, F7 |

So: **3 of 11 receipts carry a full 40-hex `rev=` stamp; 1 carries a truncated stamp; 7 carry no
revision at all.** Only 3 of 11 carry an `exit=` line.

### 3a. The three stamped receipts re-derive exactly

Re-ran each producing command and compared byte-for-byte against the receipt:

```
count-c1.py 3f494b49… --repo <lane>  + "exit=0"  ==  c1-at-freeze.txt      IDENTICAL
count-c2.py 3f494b49… --repo <lane>  + "exit=0"  ==  c2-at-freeze.txt      IDENTICAL
controls.py 5b295eee… --repo <lane>              ==  controls.txt          IDENTICAL
round-55/count-c1.py 5b295eee… + "exit=1"       ==  c2-old-counter-voted0.txt  IDENTICAL
vote-bind.py --selftest + "exit=0"               ==  selftest-vote-bind.txt    IDENTICAL
count-c1.py --selftest / count-c2.py --selftest  ==  selftest-{c1,c2}-counter.txt IDENTICAL
```

Tool pins are stable across the freeze window: `tools/mori-driver-liveness.py` sha256 =
`6b3dba74…997` and `tools/mori-vote-bind.py` sha256 = `8be1acdb…6bca` at `6ced9da9`, `3f494b49`,
`8be2717b` and at the working tree — the values pinned in `count-c1.py` / `count-c2.py` and in
`freeze-sha256.txt`. `count-c1.py` and `count-c2.py` are byte-identical at `3f494b49` and
`8be2717b`. Re-running both counters at the freeze tip reproduces the same verdicts with the tip's
own revision in the `rev=` field:

```
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b…   exit 0
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b…   exit 0
```

The tally line in `tally-r55.txt` also re-derives standalone from the committed bytes at
`8be2717b` (`corpus/knowledge/kernel-v7.3-recheck-r55.md` and `.ufo/waves/round-55/w1-results.json`
are byte-identical at `5b295eee` and `8be2717b`):
`TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15`, exit 0.

### 3b. `census-start.txt` — what it actually is

The round-56 `census-start.txt` is **byte-identical** to round-55's (sha256
`611391325d4d0d20955c8939cc9688dc0fa54d329c11eac7fa25abfc1ef9c61b` in both) and was added in the
data commit `c419fe6d`. Its content is 23 `mori<TAB>W04 …` lines + one `mori<TAB>ok<TAB>…/corpus/SOURCES.md`
line + `exit=0`; it contains no row count (`grep -c 316` → 0) and no revision. A fresh
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` today produces the
same 23 W04 lines and the same `ok` line, exit 0. Registry rows: 316 at `5b295eee`, 318 at
`c419fe6d` and at `8be2717b` (S544/S545 added). There is no `census-end.txt` in round-56 yet
(expected pre-closure; the contract requires it to exit 0).

## 4. Falsification attempts on the receipt-stage detector

All in scratch fixtures (one clone-equivalent per fixture, top level asserted before each commit).

| mutant | change | detector result |
|---|---|---|
| A | round-55 C1 After cell: `evidence/c1-at-landed.txt` at `a27ec482` → at `deadbee` | `flagged=0`, exit 0 — **not detected** (F1) |
| C | round-55 C1 After cell: cite `evidence/c1-at-data.txt` (at-landed exists) | `FLAG line 2888 …`, `flagged=1`, exit 1 — detected |
| B | delete the `**Round-53 correction:**` paragraph (fixture carries the round-53 landed receipts) | 3 FLAG lines, `flagged=3`, exit 1 — suppression path is real |
| D | round-56-style citation `evidence/c1-at-freeze.txt` | never enters `cited_intermediate` — **not covered** (F2) |

## Findings

- **F1 — MED — routed defect 2 is only half mechanised.** `.ufo/waves/round-54/checks/receipt-stage.py`
  (the flag loop, ~lines 60–80) checks *which* receipt a cell names (`-at-data`/`-at-salvage` vs an
  existing `-at-landed`) and whether a correction paragraph excuses it. It never compares the
  revision quoted in the cell with the revision the receipt stamps. Mutant A: a cell citing
  `evidence/c1-at-landed.txt` at `deadbee` passes with `flagged=0`, exit 0. A wrong-revision claim
  is therefore invisible to the lane's only receipt-staging detector. The round-55 rows happen to be
  correct (§2), but the detector would not have said so. Named limit + routed item for round 57
  (the detector is a round-54 check, not a frozen round-56 counter — the L1 owns any change).
- **F2 — MED — the detector has zero coverage of round-56's receipt naming.** Its regex matches only
  `-at-(data|salvage)\.txt` and its landed-name pattern is `-at-landed`; round-56's receipts are
  `-at-freeze`. The L1's draft round-56 rows cite `evidence/c1-at-freeze.txt` /
  `evidence/c2-at-freeze.txt`, so they can never appear in `cited_intermediate` and can never be
  flagged, whatever revision they quote. Named limit + routed item for round 57.
- **F3 — MED — `controls.txt` does not stamp where it measured, and loses the failure cause.**
  `.ufo/waves/round-56/controls/controls.py` writes each do-nothing verdict through
  `verdict[:110]`, so the recorded lines are cut mid-string: `do-nothing-c1 … failed=tool_absent
  rev=5b295eeebd87ebd610d8d39b` (24 hex chars) and `do-nothing-c2 … row=ok
  rev=5b295eeebd87ebd610d8d39bfe2035742` (33 hex chars, and the `failed=tool_absent` cause is
  dropped entirely). The eight `mut:` lines carry no revision and no exit code, and the file has no
  `exit=` line at all. The receipt therefore cannot be checked for what was mutated or where.
  The controls module is FROZEN for this round — named limit + routed item for round 57, not a
  fix here.
- **F4 — MED — the draft round-56 SCORECARD Before cells quote verdict strings that are not in the
  receipt they cite.** In the working-tree `SCORECARD.md` (uncommitted L1 draft, round-56 section
  at line 2897), the C2 Before cell quotes `C2=unmet selftest=ok tally=ok control=ok
  contrast=voted0 entry=ok row=ok failed=tool_absent`; that string occurs **0 times** in
  `.ufo/waves/round-56/evidence/controls.txt` (whose C2 line ends at `…row=ok rev=5b295eee…`,
  truncated). The quoted line is the *reconstructed* full counter output at the entering tip
  (reproduced by running `count-c2.py 5b295eee…`, which prints exactly that string with the
  `rev=` field in the middle), not the receipt's bytes. The C1 Before cell's quote is a verbatim
  substring of `controls.txt` (1 match). L1 owns `SCORECARD.md`; flagging only.
- **F5 — MED — `freeze-sha256.txt` mislabels the provenance of four of its own pins.**
  `.ufo/waves/round-56/evidence/freeze-sha256.txt` heads its first block `# data commit
  6ced9da9b1f9c65065a8158735e0331938e8a599` over `contract.md`, `count-c1.py`, `count-c2.py` and
  `controls/controls.py`, but none of those four paths existed at `6ced9da9` (`git show
  6ced9da9:<path>` yields nothing; the sha256 of the empty result is `e3b0c442…`). They landed at
  the freeze commit `3f494b49`, and `controls/controls.py` changed again at `8be2717b`
  (`08620c17…` → `5bf65ac0…`), which is why the pin file was rewritten in the same commit that
  landed the controls and receipts. The pinned bytes are correct for the freeze tip; the header's
  provenance claim is stale.
- **F6 — MED — the round-56 census receipt is a copy and carries neither a revision nor the row
  count the contract attributes to it.** `.ufo/waves/round-56/evidence/census-start.txt` is
  byte-identical to round-55's and was committed in the data commit `c419fe6d`; it holds 23 W04
  lines + one `ok` line + `exit=0` and no `rev=`. The contract describes it as "exit 0, 316 rows,
  23 W04", but the string `316` occurs 0 times in the receipt and no row count is present at all;
  the W04-only shape cannot distinguish 316 rows from 318. The registry already had 318 rows at the
  commit that added this receipt. Routed defect 1 (census before→after must be captured bytes or
  the counting command) is therefore satisfied only for the W04 half.
- **F7 — LOW — seven round-56 receipts carry no revision stamp, and the freeze pin file does not
  pin the evidence receipts themselves.** `tally-r55.txt` (the receipt the contract quotes for the
  exact tally line), `selftest-c1-counter.txt`, `selftest-c2-counter.txt`, `selftest-vote-bind.txt`,
  `driver-liveness-live.txt` and `census-start.txt` carry `exit=` but no `rev=`;
  `freeze-sha256.txt` carries neither and pins only the contract, the two counters, the controls
  module, the two tools and two `corpus/evidence/sources-r56/*` copies — not the eleven round-56
  receipts it is meant to protect. Every one of these receipts re-derives byte-identically today
  (§3a), so the risk is traceability, not a wrong number.
- **F8 — LOW — the receipt-stage detector's escape hatch is loose.** A `**Round-N correction:**`
  paragraph anywhere later in the file that mentions `<name>-at-landed` suppresses the flag for
  every row of round N, and the flag loop inspects only the After cell. Not exploitable in the
  current file (the two correction paragraphs are specific and accurate); noted as a detector
  sharp-edge for round 57.

### Verified-good, for the L1's integration record

- Round-55 After cells cite the landed receipt and the quoted revision equals the receipt's own
  `rev=` stamp in all four round-55 citations; the Before cells likewise.
- `receipt-stage.py` exits 0 with `flagged=0` at both the entering and freeze tips; its two
  positive controls fire, so the zero is a genuine pass on the current file.
- All three revision-stamped round-56 receipts re-derive byte-identically; the counters, the
  controls and the tool selftests all re-derive at both `3f494b49` and the freeze tip.
- The tool sha256 pins are stable across `6ced9da9`, `3f494b49`, `8be2717b` and the working tree.
- The tally re-derives standalone from the committed round-55 bytes, unchanged between the entering
  and freeze tips.

### Not checked / out of scope

- Whether the L1's draft round-56 SCORECARD numbers should change (the L1's call; the two cells
  quoted here are consistent with the receipts' *verdicts*, only the C2 Before quote is not
  verbatim from the cited receipt — F4).
- No mutation was made to any file in the lane or fleet repo; the only file written is this report.
- `census-end.txt` does not yet exist for round-56 (pre-closure); its exit-0 requirement is
  recorded in the contract but not testable at the freeze tip.
