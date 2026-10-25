# R48ExecRerunC1 — independent acceptance run of C1 at the landed tip (round 48, wave 2)

Report: `.ufo/waves/round-48/w2/R48ExecRerunC1.md`

**Attacked:** the P-C1 acceptance command at the landed tip `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`,
run in-lane with `--jobs 6` and an explicit `--scratch`, against the working-tree instrument
`tools/mori-pin-check.py` (which I first proved is byte-identical to the file at `e4dfff32…`).
I also compared the result with `evidence/after-c1-at-e4dfff32.txt`.

**Verdict: HOLDS — `C1=met`, exit 0, reproduced independently.** Class of the result:
*claim re-measured and confirmed; the claim's own post-landing receipt is missing (an empty,
untracked file), so this run is the first recorded acceptance receipt at the tip.* That receipt
gap is a `landing`-class defect (F1 below), not a predicate failure. I did not re-score anything
and changed no rule.

## 0. Preconditions checked before the run

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ sha256sum tools/mori-pin-check.py
85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1  tools/mori-pin-check.py
$ git show e4dfff32d4f97c7ef250e9a7538fa75d4f284492:tools/mori-pin-check.py | sha256sum
85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1  -
$ git rev-parse HEAD
e4dfff32d4f97c7ef250e9a7538fa75d4f284492
$ git diff --stat e4dfff32 -- tools/mori-pin-check.py SKILL.md .ufo/waves/round-48/count-c1.py
(no output — the three files the claim is about are the committed bytes at R)
$ git status --porcelain --untracked-files=no
(no output — no tracked path dirty before or after my run)
```

So the `--tool <working-tree path>` form the assignment specifies measures exactly P-C1's
"`tools/mori-pin-check.py` at R". Frozen instrument bytes, each against `evidence/freeze-sha256.txt`:

```
$ sha256sum .ufo/waves/round-48/count-c1.py .ufo/waves/round-48/contract.md \
    .ufo/waves/round-48/v3-spec.md .ufo/waves/round-48/controls/stub-always-met.py \
    .ufo/waves/round-48/controls/stub-always-unmet.py .ufo/waves/round-48/controls/tool-v2-entering.py
7a2a6aa09b923ef8521a1182fb1bc11f4f92ed7450e9eba86882e454284e4b97  .ufo/waves/round-48/count-c1.py
052a2bf9be032545202ecf5dfae90a50ab2d2001116356493c4005b3a9bc75dd  .ufo/waves/round-48/contract.md
f93ef57fd977b67fba2068cec21d6161ea2ab14ab083676bf9a78b2cda0d9808  .ufo/waves/round-48/v3-spec.md
c6f12be844264304fd2007b1f30c4b9a15d4a5414c918588d800021221987b2d  .ufo/waves/round-48/controls/stub-always-met.py
5b716abc437e1dab2cbf66c304f01e644993f3bc3000345e9f703dcb87c63bf2  .ufo/waves/round-48/controls/stub-always-unmet.py
9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6  .ufo/waves/round-48/controls/tool-v2-entering.py
```

All six match the manifest rows 1-7; the manifest's twelfth row (`tools/mori-pin-check.py`
`9832e38c…`) is the *entering* digest — see F3.

## 1. The acceptance run (exact command)

```
$ mkdir -p /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRerunC1/c1
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRerunC1 \
  python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-48/count-c1.py \
    --tool /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
    --scratch /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRerunC1/c1 \
    --jobs 6
```

Run in the background (13 tool invocations, ~2 min each); wall time **633.31 s**. stdout and
stderr captured separately to
`.scratch/r48w2-R48ExecRerunC1/c1-out.txt` and `.scratch/r48w2-R48ExecRerunC1/c1-err.txt`.

**Full stdout (669 bytes, verbatim):**

```
variant name=J1 expect=unmet got=unmet rc=1
variant name=J2 expect=unmet got=unmet rc=1
variant name=J3 expect=unmet got=unmet rc=1
variant name=J4 expect=unmet got=unmet rc=1
variant name=J5 expect=unmet got=unmet rc=1
variant name=J6 expect=unmet got=unmet rc=1
variant name=J7 expect=unmet got=unmet rc=1
variant name=J8 expect=unmet got=unmet rc=1
variant name=H1 expect=met got=met rc=0
variant name=H2 expect=met got=met rc=0
variant name=H3 expect=met got=met rc=0
variant name=H4 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
```

**stderr:** 0 bytes (empty).
**Exit code:** `EXIT=0` (appended to the captured file by the wrapper; the counter's own
`sys.exit(0 if met else 1)` path).

Against P-C1's sentence: `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12` — every
field matches, in the contract's order; exit 0. The counter appends ` rev=<rev>`, which the
contract's quoted string does not contain (F2). No `errors`, no `timeout`, no `C1_SETUP` line, so
no variant anchor was absent at R.

## 2. Comparison with `evidence/after-c1-at-e4dfff32.txt`

The file exists but there is nothing to compare:

```
$ wc -c .ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt
0 .ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt
$ stat -c '%n %s %y' .ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt
.ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt 0 2026-10-25 19:37:41 -0300
$ git ls-tree -l e4dfff32 .ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt
(no output — path absent from the commit)
$ git status --porcelain -- .ufo/waves/round-48/evidence/
?? .ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt
?? .ufo/waves/round-48/evidence/after-c2-at-e4dfff32.txt
```

So the post-landing C1 receipt is a **0-byte, untracked** file whose mtime (`19:37:41`) is
*after* the landed commit (`e4dfff32` committed `19:30:50 -0300`) and after wave-2 dispatch
(`w2/` created `19:32`). It carries no measurement. My §1 output is therefore the first recorded
`C1=met` receipt at this tip; the sibling C2 receipt is likewise untracked but at least non-empty
(152 B, `C2=met …`). §1 and the C2 analogue are the only two post-landing receipts the claim has.

## 3. Corroboration (independent of the counter's own verdict line)

**(a) The real arm, run directly** — the tool under test against R's registry, not through the
counter (121.86 s wall, exit 0). Last two lines:

```
pin line=973 kind=tally prefix=UNLANDED_SELFTEST state=match pinned='pass=13 fail=0' observed='pass=13 fail=0' rc=0 cmd='python3 tools/mori-unlanded-check.py --selftest'
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
```

31 tally pins (floor 26), 8 digest pins, and every new v3 counter (`rebound`, `duplicate`,
`hidden`) at zero; the round-48 counter's own selftest pin is re-observed live
(`pin line=971 … prefix=C1_SELFTEST pinned='pass=34 fail=0' observed='pass=34 fail=0' rc=0`).

**(b) The variants are real edits at R, not no-ops.** The counter writes each variant into the
scratch dir; each differs from `git show e4dfff32:SKILL.md` and from every other variant:

```
SKILL-at-R.md   62602b2e438a2fe572b48055e7c62cf169d94f2fa5afb14bb8e3262212e3a77d   979 lines
variant-J1.md   a87bbe60ef3042160790e0acb83b6534568449356fb2b0b3c82e1f47172e216b   979 lines  (6 diff lines)
variant-J2.md   55cdfa21621ff7cbdeec920a632e3a0414abed1732e80fa1cf8b5b7293af1b15   980 lines  (1)
variant-J3.md   34c1ad5cafb96aca67bb89d358f04fffda811a8e2b31f375a2192fbf39ca0d11   980 lines  (1)
variant-J4.md   1d97a7687bf69ac3b917f00ce6f057919b78aef5a83dec7143074e89c772785d   980 lines  (1)
variant-J5.md   b23a5e2d91410546e17548ae3b57e8dd2ef6293927ed652158a37bec7089aefe   981 lines  (6)
variant-J6.md   1c300ea6f371fc280c1d3e9fe359681db7ca2e8adbdbbed5c108288533575c36   980 lines  (3)
variant-J7.md   6f8c6831ba25ab1cf98bdd5c71c3d288ec53fd5d90f43d2c52c4b1eb6e5e84a6   979 lines  (2)
variant-J8.md   68a40aad902d36b66b02a12dd628229ac02c0937a4392755510a8de51c38243e   979 lines  (2)
variant-H1.md   3c073102dd664d2a178646363db9636c74d55ab4d68f0e410c401917abffd2b8   981 lines  (2)
variant-H2.md   0885bf28ea2d53056b133b82517300948c609ccab3510f60bfd36e92b2ce9e5c   979 lines  (2)
variant-H3.md   0107b35c6c5e04e2ae310ba639530f9a851b0d4809a05407c3d4b103a4b0fef9   979 lines  (2)
variant-H4.md   1396557c957a547309a8ddf4ae173df71bfe94667d25214669054955d689b757   980 lines  (1)
```

The 8 junk and 4 honest bodies are pairwise distinct and each carries its declared edit, so the
`got=` column is a measurement of the declared edits at R rather than of R itself.

**(c) Cross-run agreement with the off-host sibling.** `w2/R48ExecRerunC1Clone.md` (§2) ran the
same predicate from a clone at `/tmp/tmp.F1d7NAFaxc/lane` with the counter's default `--jobs 4`.
Its 13 `variant …` lines and final `C1=met … rev=e4dfff32…` line are character-identical to mine;
my run adds a different path, a different scratch root and `--jobs 6`. Two independent
configurations, one output — the classification is not job-count- or path-dependent.

## 4. Findings (detection and report only; none re-scores C1)

**F1 — the C1 post-landing receipt does not exist as evidence (`landing` class).** A 0-byte
untracked file named for the run is not a receipt; the claim's `Before`/control receipts are all
committed with content, and the `Target after` side is empty. This is the same shape as the
contract's named "Mistake: round-47 routed defect 1 (late seat results never committed, a
`landing` class)". Round-end should write §1's block into
`evidence/after-c1-at-e4dfff32.txt` (or a sibling receipt) and commit it, with the exit code, or
P-C1 has no landed receipt even though it holds.

**F2 — the frozen counter's verdict line is not the contract's quoted string (format only).**
`contract.md` P-C1 quotes `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12`;
`count-c1.py:verdict()` prints that plus ` rev=<rev>`, and the same shape appears in all three
committed control receipts and in the counter docstring. A literal equality check against the
contract sentence fails; a prefix/field check passes. Substance unaffected (all six named fields
and the exit code match), but round-end should quote the counter's full line so a later reader
does not read the mismatch as a violation.

**F3 — the freeze manifest's tool row pins the entering bytes, not the subject (observed, already
routed).** `evidence/freeze-sha256.txt` row 12 reads `9832e38c…  tools/mori-pin-check.py`, which is
`controls/tool-v2-entering.py` and the tool at `e5dbac05`; the landed tip's tool is `85a89a3b…`
(both digests re-measured in §0). Taken literally, the contract's fallback sentence ("measured
with `git show <freeze>:<path>`") would route C1's instrument to the pre-hardening tool, whose
receipt is `C1=unmet junk_met=8 … rc=1`. P-C1's own wording ("the tool bytes under test at R") is
what §1 measures. Recorded here as corroboration of `w2/R48ExecRerunC1Clone.md` O1 and
`w1/CritContractFreeze.md`; the claim is not in doubt, the manifest row simply cannot serve as the
subject's pin.

## 5. Limits of this seat

- One run per configuration (mine: in-lane, `--jobs 6`; sibling: clone, `--jobs 4`). I did not
  run a third configuration, and I did not mutate the tool or the counter — the mutation seats own
  that.
- I measured the tool *at R as bytes* (`85a89a3b…`), not the semantics of every new v3 rule; the
  rules' kill-ability is the mutation wave's question. My run only shows the 12 frozen variants
  and the real registry are classified as P-C1 requires.
- Wall time (633 s) is under fleet load from sibling seats; it is not a performance measurement.
- A dispatched seat is not an independent judge: I report observed output and exit codes, and I
  leave the met/unmet judgement for the claim to the L1's round-end, where the receipts land.
- No tool installs or upgrades were needed; nothing outside my scratch and this report was
  written. `git status --porcelain --untracked-files=no` was empty before and after.

## 6. Reproduce

```
mkdir -p /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRerunC1/c1
cd /home/vgpnk/Projects/shokunin/mori-shokunin
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRerunC1 \
python3 .ufo/waves/round-48/count-c1.py \
  --tool /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py \
  --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
  --scratch /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ExecRerunC1/c1 \
  --jobs 6 ; echo "EXIT=$?"
```

Artifacts: `.scratch/r48w2-R48ExecRerunC1/c1-out.txt` (669 B), `c1-err.txt` (0 B),
`SKILL-at-R.md`, `c1/variant-*.md` (12 bodies), `c1/c1-*/` (13 per-variant TMPDIRs).
