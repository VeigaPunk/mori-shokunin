# Mo50bRevReexecMethod — review: re-executing closure-verified counters (round 48 C1)

Seat: mori round 50, wave a2w1. MACHINE_ID=432d02b544a5459ebbff9c42ec68334d.
Environment: Python 3.14.8, git 2.56.0, linux x64. Tooling authorization unused — nothing
installed or upgraded, no pacman. Disk guard checked before the run: `/fast/scratch/hyaku`
24% used, 612.7G free. Scratch `/fast/scratch/hyaku/mori-r50/Mo50bRevReexecMethod/` was
created for this seat and removed at the end; every cited output is copied into this report.

**Attacked:** considerthese 2026-10-26 suggestion 3 — "re-execute what closures only
evidence-verified". The r47–r49 closures state their gate verdicts come from committed
receipts, not runs (`corpus/lessons/round-48-verifier-spotcheck.md`, header: "No lane gate or
selftest was executed as a verdict source … gate verdicts … are evidence-verified from
committed receipts"). I picked round 48's C1 counter, recovered its scored revision
independently, re-ran the frozen counter once in a `git archive` extract under scratch against
a `git clone --shared` object database, and compared the output byte-for-byte with the
committed receipt. No frozen predicate, counter, control or kill rule is proposed to change;
data corrections are not mine to make (L1 owns those).

## 1. Independent recovery of the scored revision

Round 48's C1 counter: `.ufo/waves/round-48/count-c1.py`. LOG.md's Round 48 section
(`LOG.md:2700-2716`) names entering `e5dbac05` and freeze `4387cf94` but **never names the
scored revision**. I recovered it without LOG.md, from three independent traces that agree:

- receipt filename `.ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt` (committed with
  content at `91fbbc2a6a35`, the wave-2 settle commit — `git log --follow
  --name-status` shows it added there; at the scored revision itself the path does not
  exist, and the freeze-commit hit under `--follow` is a 51%-similarity copy pairing with
  `control-c1-stub-always-unmet.txt`, which is the file actually added at the freeze);
- the closure lesson §2 ("after: `evidence/after-c1-at-e4dfff32.txt` → … rev=e4dfff32… rc 0");
- the round-48 lane report, which lives in the **fleet** repo at
  `.ufo/reports/round-48/mori.md`, committed as fleet commit `e60eb167…` ("round-48: mori
  report", author mori-shokunin, 2026-10-25 20:27:04 -03): line 4 says "data commit
  `e4dfff32d4f97c7ef250e9a7538fa75d4f284492` (tool and counter bytes unchanged since)".

Scored revision: **`e4dfff32d4f97c7ef250e9a7538fa75d4f284492`** (authored 2026-10-25
19:30:50 -0300, "round-48: data — pin-check v3 + pin repair, …"). Freeze: `4387cf94b69dd…`
(17:53:38 committer date). Counter identity across the three points I care about:

```
git show 4387cf94:.ufo/waves/round-48/count-c1.py | sha256sum
  -> 7a2a6aa09b923ef8521a1182fb1bc11f4f92ed7450e9eba86882e454284e4b97
git show e4dfff32:.ufo/waves/round-48/count-c1.py | sha256sum  -> same
sha256sum <archive extract>/.ufo/waves/round-48/count-c1.py    -> same
git diff --stat 4387cf94 HEAD -- .ufo/waves/round-48/count-c1.py count-c2.py
  -> empty (bytes unchanged from freeze through the current tip)
row 1 of e4dfff32:.ufo/waves/round-48/evidence/freeze-sha256.txt -> 7a2a6aa0…  count-c1.py  (match)
```

The instrument the counter executes, `tools/mori-pin-check.py` at the score, is
`85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1` (v3). It has **no
absolute host path and no network reference** (`grep -nE '/home|/fast|http'` over
`git show e4dfff32:tools/mori-pin-check.py` → rc 1, no hits). Note the freeze manifest's
`tools/mori-pin-check.py` row pins the *entering* v2 bytes `9832e38c…`, not the v3 subject —
already routed in round 48 wave 2 (`w2/R48ExecRerunC1Clone.md` O1, `w2/R48ExecRerunC1.md` F3);
I re-confirmed both digests and do not re-route it, but it drives receipt-format requirement
R4 below.

## 2. The re-run (method, exact commands, result)

Constraints honored: one `git clone --shared` (worktree unused; object reads only), one
`git archive` extract supplying every **executing** byte, no lane mutation of any kind, all
temp state under the seat scratch with `TMPDIR` exported.

```
S=/fast/scratch/hyaku/mori-r50/Mo50bRevReexecMethod
export TMPDIR=$S/tmp
git clone --shared /home/vgpnk/Projects/shokunin/mori-shokunin $S/repo
test "$(git -C $S/repo rev-parse --show-toplevel)" = "$S/repo"        # toplevel-ok
git -C $S/repo rev-parse --verify e4dfff32d4f97c7ef250e9a7538fa75d4f284492^{commit}
git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive --format=tar \
    e4dfff32d4f97c7ef250e9a7538fa75d4f284492 | tar -x -C $S/wt
# executing bytes verified: counter 7a2a6aa0…, instrument 85a89a3b… (both above)
cd $S/wt
python3 -I -B .ufo/waves/round-48/count-c1.py \
  --tool $S/wt/tools/mori-pin-check.py \
  --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 \
  --repo $S/repo \
  --scratch $S/tmp/c1run
```

Wall time 322.32 s under fleet load (the lane's own runs took 633 s / 449 s; not a
performance claim). Exit code **0**. Full stdout (verbatim):

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

Comparison with the committed receipt `evidence/after-c1-at-e4dfff32.txt` (identical at
`91fbbc2a` and at the current tip — `git diff 91fbbc2a HEAD -- <path>` empty): the receipt is
the 14 lines above plus a final `rc=0` line. `diff <rerun stdout> <receipt minus last line>`
→ empty. **Byte-exact agreement, 14/14 lines, exit 0.** The baseline `2d85e33d1419…` (the
counter's frozen `BASELINE`) resolves in the shared clone
(`git show 2d85e33d…:SKILL.md` → exit 0), so the instrument's `baseline=yes` state is
reproduced too.

This is the third independent configuration to reproduce the verdict at this revision: the
lane's wave-2 seats ran it in-lane at a clean detached tip (`w2/R48ExecRerunC1.md`, `--jobs 6`,
633 s) and from a foreign clone at `/tmp` (`w2/R48ExecRerunC1Clone.md`, `--jobs 4`, 7m29s);
mine adds archive-extracted executing bytes against a shared-clone object store with the live
lane untouched at its current tip. All three stdout blocks are character-identical.

## 3. What the re-run proves and does not prove

**Proves (observed):**

- **Frozen bytes execute and reproduce.** The counter bytes sha-pinned at the freeze
  (`7a2a6aa0…` = `freeze-sha256.txt` row 1 = score revision = current tip) produce, at the
  scored revision, exactly the committed verdict line and exit code, on a fresh tree, with a
  2026 interpreter and git. The receipt is a reproducible measurement, not prose.
- **The instrument's pins really pass at R.** Each of the 13 arms runs the pin reconciler at
  `e4dfff32` over that revision's SKILL.md (including executing the pinned selftests —
  `PIN_CHECK_SELFTEST pass=60`, `C2_SELFTEST pass=22`, the r40 archived gate — via the tool's
  own `git archive` of R), so the agreement covers the registry's substance at R, not just a
  string comparison.
- **Portability.** No path-, job-count- or worktree-state dependence: my run used a different
  path, scratch root and extraction method than the lane's two runs; identical output.
- **Offline capability.** Static surface: no network imports in counter or instrument
  (`grep -nE 'urllib|requests|socket|http'` over both → 0 hits); every input flows through
  local `git show` / `git archive` / `rev-parse` on the local object DB; `python3 -I -B`
  isolates the run. The counter **can** run network-free.

**Does not prove (named limits):**

- **That the original receipt came from a run at scoring time.** Provenance is asymmetric:
  agreement shows the receipt is *reproducible*, not *when or by whom it was first produced*.
  Concretely: the receipt file was empty and untracked when the lane's wave-2 re-runs found it
  (`w2/R48ExecRerunC1.md` §2) and gained its content only at the settle commit `91fbbc2a`
  (20:25:48), after those runs — so the committed bytes most likely are (or are copied from)
  the wave-2 output, and my run cannot distinguish "L1 ran the counter" from "L1 committed the
  re-executor's output". Byte agreement is exactly why this is invisible. A closure that wants
  first-run provenance needs the receipt committed with a `cmd:` line by the runner (R6 below).
- **Frozen instrument bytes from the freeze.** Only the *counter* was frozen at `4387cf94`;
  the v3 instrument did not exist yet, and the freeze manifest's tool row pins the entering
  bytes. "Frozen bytes" for the pair (counter, instrument) holds *via the scored revision*,
  not via the freeze receipt. A re-run proves the pair at R is consistent; it cannot prove
  anything about a counter executed against a *different* tool than the one at R.
- **Same fleet MANIFEST revision — not applicable here, and that is the point.** Both r48
  counters contain zero `MANIFEST` references (`grep -c MANIFEST count-c1.py count-c2.py` →
  0, 0): round 48's C1 is lane-local, so its re-run says nothing about the fleet manifest.
  Round 50's C1 is different — its verdict line embeds `manifest=a94551c5bc8d` (fleet MANIFEST
  revision measured) and its calibration binds to fleet MANIFEST at `e0144996…`. For r50, a
  re-run is comparable only if the manifest revision is unchanged; a moved manifest is expected
  divergence, not a counter failure. Receipts for manifest-reading counters must record the
  manifest rev (r50 already does) and closures must compare that field first.
- **Network-free original.** My run proves the counter runs offline; it does not prove the
  original receipts were produced offline (packet-level absence UNVERIFIED — no sniffer was
  used; the claim rests on the import/command-surface scan above).
- **Calibration sufficiency or entailment.** C1 is calibration: 12 frozen variants passing
  does not saturate the junk space (the closure names the filename-sniff survivor class and
  v3's 7-of-14 new-probe rate), and says nothing about whether entries are true. A green re-run
  inherits exactly the frozen predicate's strength — no more.
- **Same-semantics guarantee.** Agreement across Python 3.14.8/git 2.56.0 here and the lane's
  runs is strong evidence of version stability for this counter, but a re-run cannot prove a
  future interpreter change preserves semantics — that is what re-running again is for.
- **No host mutation historically.** My run wrote only inside my scratch (clone `.scratch` and
  `TMPDIR`); it cannot retroactively attest what the original run touched.

**Method note for future re-executors (rounds 47/49 seats):** the archive-extract form is the
strictest: executing bytes come from `git archive <rev>` (verifiable by sha256 against the
freeze receipt), and only object reads touch the shared clone, so the live lane can sit at any
tip and nothing in it is even read. It costs nothing extra beyond the clone the lane's own
method already used.

## 4. Receipt format the lane should commit

Existing convention to build on: r48 `after-c1-at-e4dfff32.txt` (14 stdout lines + `rc=0`);
r50 `a2-c1-at-data.txt` (item lines, verdict embedding `manifest=` + `rev=`, final `exit=0`).
Gaps observed: revision not always in the filename; no instrument digest; no command line; no
environment; freeze manifest not verifiable from one cwd (r48 `freeze-sha256.txt` uses four
path bases — `w2/R48ExecRerunC1Clone.md` O2); byte-identical control receipts distinguishable
only by filename (O4).

Proposed: **one file per run**, committed beside the round's evidence, named
`c1-at-<rev12>.txt` (same for `c2-`, `selftest-`), content:

```
# mori <C1|C2|selftest> receipt
counter: .ufo/waves/round-<R>/count-c1.py sha256=<64hex>
instrument: tools/mori-pin-check.py sha256=<64hex>     # omit line if the counter runs alone
rev: <40-hex>                                          # the revision measured (full hash)
baseline: <40-hex|->                                   # counter's BASELINE, as passed
manifest: <40-hex|->                                   # fleet MANIFEST rev measured, if read
cmd: python3 -I -B .ufo/waves/round-<R>/count-c1.py --tool tools/mori-pin-check.py \
      --rev <40-hex> [--repo <repo-or-dot>] [--scratch <path>]
env: python=<X.Y.Z> git=<X.Y.Z> machine=MACHINE_ID
--- stdout (verbatim) ---
<every line the counter printed, unmodified>
--- exit ---
rc=<n>
```

Requirements, each tied to an observed failure it prevents:

- **R1 full 40-hex `rev:`** — r48's LOG.md omits the scored revision entirely (F1 below); the
  filename's 8-hex (r48) or "data" (r50 `a2-c1-at-data.txt`) must not be the only carrier.
- **R2 verbatim stdout + exit code** — enables byte-level `diff` by a closure; r50 already
  ends with `exit=0`; keep it.
- **R3 `manifest:` line** — mandatory for manifest-reading counters (r50 C1); lets a closure
  separate "expected divergence: manifest moved" from "counter failure". r48-style lane-local
  counters write `-`.
- **R4 instrument digest** — the freeze manifest's tool row pinned the entering bytes
  (`9832e38c…` ≠ subject `85a89a3b…`); the score receipt, not the freeze, is where the subject
  bytes belong.
- **R5 `env:` line** — makes interpreter/git divergence attributable instead of mysterious.
- **R6 `cmd:` line, written by whoever ran it** — restores first-run provenance (the exact gap
  §3 names) and distinguishes byte-identical control receipts (O4).
- **R7 repo label when a hash is not lane-local** — closures and reports cite both lane
  commits (`4387cf94 e4dfff32 91fbbc2a 14c5110d`) and fleet commits (report `e60eb167…`) in
  one breath; the fleet hash is unresolvable in the lane repo (see F2). A receipt citing a
  fleet-repo hash writes `fleet: <40-hex>`, lane hashes stay bare.
- **R8 freeze manifests get per-base verify commands** — record, per path base, the
  `(cd <base> && sha256sum -c -)` line that verifies it, so `sha256sum -c` works from one
  documented place.

## 5. Bounds

Leaf seat; no subagent. No lane file touched except this report; the only git verbs used in
the lane were read-only (rev-parse/show/log/diff/ls-tree/archive); the clone and archive live
under the seat scratch and were removed after this report was written; no `jj` command; no
pacman; nothing installed; no kernel log read; no network tool runs. The one `checkout`-free
method (archive + shared clone) avoided detached-tip checkouts entirely.

## Findings

- **MED — LOG.md does not record round 48's scored revision.** `LOG.md:2700-2716` names
  entering `e5dbac05` and freeze `4387cf94` but not `e4dfff32…`; recovery required the receipt
  filename, the closure, or the fleet-repo report. A future re-executor following the lane log
  alone cannot pick the revision to re-run. (Receipt format R1; LOG.md wording is data the L1
  may correct.)
- **MED — closure receipts mix lane-repo and fleet-repo hashes without labels.**
  `corpus/lessons/round-48-verifier-spotcheck.md` §1 verifies "cited lane commits" `4387cf94
  e4dfff32 91fbbc2a 14c5110d` (lane repo) and, in the adjacent row, report commit `e60eb167…`
  — which exists only in the **fleet** repo (`git -C /home/vgpnk/Projects/shokunin log -1
  e60eb167…` → "round-48: mori report"; `merge-base --is-ancestor e60eb167… HEAD` true; the
  lane repo's entire object DB does not contain it — `git cat-file --batch-all-objects` grep
  count 0, and `git rev-parse e60eb167` fails in the lane). Resolved, not a fabrication — but
  a re-executor resolving all five hashes in the lane repo fails on the fifth, as I did first.
  (Receipt format R7.)
- **LOW — the committed r48 C1 receipt is (most plausibly) wave-2 re-executor output, not a
  scoring-time run.** Empty untracked file at the score (`w2/R48ExecRerunC1.md` §2), content
  appears at settle `91fbbc2a` (20:25:48) after the wave-2 runs (19:37–20:0x). Byte-reproducible
  (this seat: 14/14 lines identical, rc 0), so the claim holds — the finding is provenance
  only. (Receipt format R6.)
- **LOW — freeze manifest's instrument row pins entering, not subject, bytes; manifest needs
  four cwds to verify.** `evidence/freeze-sha256.txt` row 12 `9832e38c…  tools/mori-pin-check.py`
  vs subject `85a89a3b…`; rows span four path bases so no single `sha256sum -c` cwd works.
  Both already routed in r48 w2 (O1/F3/O2); re-confirmed still true; carried here only as
  motivation for receipt R4/R8. No new route.
- **LOW — r50 receipt filename drops the revision** (`a2-c1-at-data.txt` vs r48's
  `after-c1-at-e4dfff32.txt`); the verdict line still carries the full rev, so this is
  convention drift, not information loss. (Receipt format R1.)
- **INFO — the counter's verdict line carries ` rev=<40-hex>` beyond the contract's quoted
  string** (routed as F2 in `w2/R48ExecRerunC1.md`); closures must compare fields/prefix, not
  literal equality. Confirmed in all four runs I examined.

**Verification gaps (stated, not worked around):** packet-level network absence UNVERIFIED
(static import/command-surface scan only); one re-run per assignment (no selftest re-run, no
mutation probing — mutation seats own that); timings taken under fleet load; the shared clone
reuses the lane's object store, so a corrupt local object would corrupt both — a re-executor
wanting independence should `git clone --mirror` from a remote (not attempted; one-clone rule).
