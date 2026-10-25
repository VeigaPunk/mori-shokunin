# R48CritFreeze — round 48 w2 freeze-integrity critic

Seat: R48CritFreeze (leaf, no subagents). Scratch: `.scratch/r48w2-R48CritFreeze/`
(TMPDIR set to it for every lane-tool run). No tool installed or upgraded this session.
No tracked file modified: `git status --porcelain | grep -cE '^( M|M |A |D |R |UU)'` → `0`.

**What I attacked.** (a) byte drift of the frozen instrument set between the freeze commit
`4387cf94b69ddce455051a1ff38e93795c2e6cde` and the landed tip
`e4dfff32d4f97c7ef250e9a7538fa75d4f284492`; (b) the freeze receipt
`evidence/freeze-sha256.txt` against freeze bytes, tip bytes and worktree bytes; (c) the landed
`contract.md` wording against the landed `count-c1.py` / `count-c2.py` predicates; (d) whether any
predicate moved after the wave-1 seats scored; (e) whether the frozen control surface still
discriminates at R (anchors, honest pins, real registry) and whether it can be satisfied for the
wrong reason.

**Verdict: HOLDS on the assigned freeze-integrity questions.** No frozen byte drifted, the receipt
is exact at freeze, at the landed tip and in the worktree, the landed contract wording still equals
both counters on every measured point, and no predicate changed after wave-1 scoring (counters are
byte-identical from freeze to tip and the wave-1 seats scored at the freeze revision with those same
bytes). **One BREAKS-class finding, against the counter's discrimination power rather than against
freeze integrity:** `C1=met` is reachable by a tool that reads no registry content at all — it only
sniffs the scratch filename the counter itself chooses (F1, demonstrated). Three further findings are
drift/wording hazards that do not change either verdict under the specific predicate (F2, F3, F4).

## 1. Freeze byte integrity — clean

Assigned diff, verbatim, at the lane root:

```
$ git diff --stat 4387cf94… e4dfff32… -- .ufo/waves/round-48/contract.md \
    .ufo/waves/round-48/count-c1.py .ufo/waves/round-48/count-c2.py \
    .ufo/waves/round-48/controls .ufo/waves/round-48/v3-spec.md \
    corpus/evidence/sources-r48/xfs_quota.8.html corpus/evidence/sources-r48/quotactl.2.html \
    corpus/evidence/sources-r48/errno.h corpus/evidence/sources-r48/aliyun-nas-quota.html
(no output)   EXIT=0
```

sha256 of all 12 receipt entries, computed three ways (`git show 4387cf94:<p>`, `git show
e4dfff32:<p>`, worktree file) — identical in all three columns:

| path | sha256 | freeze = tip = worktree |
|---|---|---|
| `.ufo/waves/round-48/count-c1.py` | `7a2a6aa0…284e4b97` | yes |
| `.ufo/waves/round-48/count-c2.py` | `0055aed1…734ee561` | yes |
| `.ufo/waves/round-48/contract.md` | `052a2bf9…9bc75dd` | yes |
| `.ufo/waves/round-48/v3-spec.md` | `f93ef57f…da0d9808` | yes |
| `controls/stub-always-met.py` | `c6f12be8…21987b2d` | yes |
| `controls/stub-always-unmet.py` | `5b716abc…87c63bf2` | yes |
| `controls/tool-v2-entering.py` | `9832e38c…1bc2b6` | yes |
| `corpus/evidence/sources-r48/aliyun-nas-quota.html` | `747fef1b…4e22719f` | yes |
| `corpus/evidence/sources-r48/errno.h` | `66a5ad60…c51622be` | yes |
| `corpus/evidence/sources-r48/quotactl.2.html` | `0d4ab273…ba8b6ee8` | yes |
| `corpus/evidence/sources-r48/xfs_quota.8.html` | `6375e40e…2c437d5f` | yes |
| `tools/mori-pin-check.py` (SUT, not frozen) | freeze/entering `9832e38c…`, tip `85a89a3b…` | expected change |

`evidence/freeze-sha256.txt` itself is unchanged: `git show 4387cf94:…/freeze-sha256.txt |
sha256sum` = worktree = `cb12c0251535b84055b13ec49b83440c56140df3659968e2711cce830702deff`.
The receipt's 12th line (`9832e38c… tools/mori-pin-check.py`) equals the 7th
(`controls/tool-v2-entering.py`) and equals `git show e5dbac05:tools/mori-pin-check.py`
(`9832e38c…`) — the entering tool, as the contract states.

Freeze ordering: freeze commit `4387cf94` has parent `e5dbac05` and time `2026-10-25 17:53:38
-0300`; `w1-dispatch.json` mtime `17:53:45`, `w1.ready.dispatched` `18:32:59`, earliest wave-1
report `w1/CritContractFreeze.md` `18:39:18`. The freeze stat adds exactly 25 files
(contract, 2 counters, v3-spec, 3 controls, 9 evidence files, 4 copies, 5 scratch artefacts),
3538 insertions, 0 deletions.

No receipt was rewritten after the freeze: `git diff --stat 4387cf94 e4dfff32 --
.ufo/waves/round-48/evidence` → empty. `corpus/SOURCES.md` changed `+6 -0` (append-only; zero
deletion lines). The landed commit is a single commit on top of the freeze.

## 2. Frozen control receipts still reproduce at the landed tip

| receipt (frozen) | content | re-observed now |
|---|---|---|
| `control-c1-tool-v2-entering.txt` | `C1=unmet junk_met=8 honest_unmet=0 real=met errors=0 variants=12 rev=e5dbac05…`, rc 1 | matches wave-1 replay; control sha = tool@e5dbac05 |
| `control-c1-stub-always-met.txt` | `C1=unmet junk_met=8 …`, rc 1 | consistent with a 2-line always-met stub |
| `control-c1-stub-always-unmet.txt` | `C1=unmet junk_met=0 honest_unmet=4 real=unmet …`, rc 1 | consistent with an always-unmet stub |
| `control-c2-donothing.txt` | `C2=unmet claims=0 … failed=entry_absent,pins`, rc 1 | entry absent at `e5dbac05` |
| `selftest-c1.txt` | `C1_SELFTEST pass=34 fail=0` | `python3 .ufo/waves/round-48/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0`, rc 0 |
| `selftest-c2.txt` | `C2_SELFTEST pass=22 fail=0` | `python3 .ufo/waves/round-48/count-c2.py --selftest` → `C2_SELFTEST pass=22 fail=0`, rc 0 |

Variant anchors at R (the counter's own exit-2 surface): all 12 edit functions applied to
`git show e4dfff32:SKILL.md` (155904 bytes, 980 lines) without raising `Anchor`, each
deterministic (apply twice → equal) and each actually changing the text:

```
J1..J8 expect=unmet  applied=True deterministic=True
H1..H4 expect=met    applied=True deterministic=True
ALL_ANCHORS_OK
```

The two anchors that could have gone stale through the landed registry repair are both still
true at R: `(743 lines)` occurs once and `tools/mori-gate-registry.py` is 743 lines with sha256
`8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832` (the row's digest pin);
`37fd7c24ff52…` occurs once and is a true prefix of `.ufo/waves/round-45/count-c3.py` at R.

Real-registry leg of P-C1, measured at the landed tip with the SUT at R (worktree tool `cmp`-
identical to `git show e4dfff32:tools/mori-pin-check.py`, `IDENTICAL`):

```
$ python3 tools/mori-pin-check.py --rev e4dfff32… --repo $PWD \
    --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 \
rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32… baseline=yes
rc=0            (387 s wall; 41 `pin … state=match` lines — 31 tally, 8 digest,
                 2 line-count — none red)
```

## 3. Landed contract wording vs landed counters — equal on every measured point

Both counters are byte-identical to the freeze bytes, so this is the same audit wave 1 ran at the
freeze, re-checked against the landed tree. Spot-verified constants and semantics:

- P-C1 `--min-tally-pins 26 --baseline-rev 2d85e33d…` every run: `count-c1.py:39-40`
  (`BASELINE`, `MIN_TALLY`), passed unconditionally in `run_tool()` (`:203-206`).
- P-C1 "eight junk J1-J8 unmet, four honest H1-H4 met, plus R's unedited SKILL.md":
  `VARIANTS` (`:186-190`) has exactly J1-J8 `unmet`, H1-H4 `met`; `measure()` appends the
  `real` job (`:246`); `verdict()` requires `junk_met==0 and honest_unmet==0 and real=="met"
  and errors==0` (`:262`).
- P-C1 "a crash, setup exit or timeout is `errors`, never `unmet`": `run_tool()` (`:216-222`)
  maps rc∉{0,1}, a missing `PIN_CHECK` line, or met/rc disagreement to `error`, timeout to
  `timeout`; both are counted in `errors`. Per-variant `got` is never rewritten to `unmet`.
- P-C1 output line: `C1=%s junk_met=%d honest_unmet=%d real=%s errors=%d variants=%d rev=%s`
  (`:263-265`); exit `0 if met else 1` (`:303`), `C1_SETUP` + rc 2 on usage/unresolvable
  revision/anchor (`:281,:290,:297`). The contract's target line omits the counter's trailing
  `rev=R` field (same observation as wave 1; not drift).
- P-C1 `variants=12` = `len(results)-1` (`:266`).
- P-C2 entry contract: `MIN_CLAIMS=8`, `MIN_SOURCES=3`, `MIN_WORDS,MAX_WORDS=6,25`,
  `OPENED="2026-10-25"` (`count-c2.py:31-34`); one backticked span per quote cell
  (`len(quotes)!=1 → bad`), uniqueness via `seen_quotes`, SOURCES row must have 11 cells with
  cell 7 `mined`, cell 8 `OPENED`, entry path in cell 10 split on `,;`, and one of the four
  `COPIES` URLs inside cell 1 (`:145-170`); quote located in `norm[url]` = tags stripped,
  `html.unescape`, whitespace collapsed (`:59-62`).
- P-C2 "every committed copy matches its frozen sha256": `pins` hashes each of the four
  `COPIES` paths and compares to the in-script digest (`:103-110`); the four in-script digests
  equal the four freeze-receipt lines. (Scope of "every committed copy" — see F2.)
- P-C2 "at R": the counter reads everything through `git show <rev>:<path>`
  (`git_reader`, `:194-199`); nothing is read from the worktree except by the selftest.
- P-C2 output line and `failed=` list: `:186-190`, exit `0/1`, `C2_SETUP` + rc 2 (`:213,:220`).

At R the entry carries the header the predicate asks for (`source:` ×6, `verified-at:
2026-10-25`, `recheck:` ×5) and a 15-row `claim | source | quote` table over S479-S482 = the four
frozen URLs, so the target shape (`claims=N≥8`, `sources=S≥3`) is reachable; the untracked
receipt `evidence/after-c2-at-e4dfff32.txt` records `C2=met claims=15 located=15 quote_missing=0
bad_rows=0 sources=4 source_rows=ok pins=ok provenance=ok rev=e4dfff32…`.

## 4. No predicate moved after the wave-1 seats scored

- Wave-1 scored revision: `w1/CritC1Counter.md:4-5` and `w1/CritC2Counter.md:13-14` record
  scoring against `--rev 4387cf94…` with `count-c1.py` sha256 `7a2a6aa09b92…` and
  `count-c2.py` sha256 `0055aed101bd…`; `w1/MutC1Variants.md:244-245` and
  `w1/SimpCounters.md:14` record the same two digests. Those are the freeze, tip and worktree
  bytes (§1), so no wave-1 score was produced by a different counter.
- No wave-1 report mentions the landed tip: `grep -rlc 'e4dfff32' .ufo/waves/round-48/w1/*.md`
  → no output, exit 1. The build wave scored the freeze/worktree state; the land then moved only
  the SUT, the registry, the entry, SOURCES, and the new copies.
- The only wave-1 run against a counter *copy* was `w1/SimpCounters.md`, whose scratch copy
  carried the frozen digest — a copy, not a mutation.
- Neither counter is modified by the landed commit (assigned diff empty, §1). The landed commit's
  only hit on a frozen pathspec is inside `corpus/evidence/sources-r48/`, and it is the two added
  files of F2 — none of the four pinned copies changed.

## 5. Findings

### F1 — BREAKS (calibration, counter discrimination): `C1=met` is reachable without reading the registry

`count-c1.py` writes each variant to `<scratch>/variant-<name>.md` and hands it to the tool as
`--skill <path>` (`measure()`, `:238-246`). The name carries the expected answer (`variant-J*` /
`variant-H*`). A tool that reads nothing but that filename passes every leg of P-C1.

Demonstrated with a 12-line scratch stub (`.scratch/r48w2-R48CritFreeze/sniff-tool.py`) that
parses only `--skill`, prints `PIN_CHECK=unmet` when the basename starts with `variant-J`, and
`PIN_CHECK=met` otherwise:

```
$ python3 .ufo/waves/round-48/count-c1.py --tool .scratch/r48w2-R48CritFreeze/sniff-tool.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --scratch .scratch/r48w2-R48CritFreeze/sniff-run
variant name=J1..J8 expect=unmet got=unmet rc=1
variant name=H1..H4 expect=met   got=met   rc=0
variant name=real   expect=met   got=met   rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32…
rc=0
```

Impacted axis: **calibration** (C1). The honest edits and the real registry do not exclude it,
because the stub is green on both by construction. `v3-spec.md` forbids the behaviour ("no rule
may special-case a variant by name or by its edit text") but the contract's P-C1 does not measure
it, and the contract's named limits do not mention it — so a landed tool's honesty rests on an
unmeasured build rule. This does not falsify the *landed* tool (other seats run the real counter
and reviewers audit the rules); it falsifies the sentence that P-C1 alone certifies the junk was
rejected on content.

Smallest safe correction (round 49 — the counter is frozen this round and the contract forbids
re-scoring under a changed counter): give the variant files opaque names that do not encode the
expectation, e.g. `case-<first 8 hex of sha256(content)>.md`, and keep the name→expectation map
only inside the counter. Optionally add a thirteenth arm: an honest edit stored under a
J-formerly-looking name, so a name-sniffing tool lands in `honest_unmet>0`.

### F2 — drift (frozen-surface widening, no false pass): two unpinned copies added to the frozen copy directory

The landed commit adds `corpus/evidence/sources-r48/arch-mips-errno.h` (134 lines) and
`arch-sparc-errno.h` (122 lines). Neither appears in `evidence/freeze-sha256.txt` nor in
`count-c2.py`'s `COPIES`; the directory now holds six copies against four frozen digests.

- Effect on P-C2 under the contextual reading ("the committed copy of that row's URL"): **none** —
  the 15 table rows use S479-S482 only, and the entry marks S483/S484 "(boundary, not in the
  claims table)" in its `source:` lines; quotes are located only in the four pinned copies. The
  counter cannot be turned green by them.
- Effect under a loose reading ("every committed copy" = every file in the directory): the sentence
  is not literally true at R. Wording is loose, not violated in substance.
- Provenance gap that is real either way: the two new copies' digests are declared only inside the
  SOURCES evidence cells (`corpus/SOURCES.md:262-263`, `006286df…`, `530c3cc2…`) and are verified
  by no gate. `tools/mori-source-drift.py` resolves a copy as
  `corpus/evidence/sources-r<N>/<sid>.<ext>` (`:11,:76`), so these two — and, by the same lane
  convention, the four frozen ones — classify `no-copy`; that mapping is pre-existing (round-47
  copies are basename-named too), so the drift is the missing pin, not the naming.

Smallest safe correction: pin the two boundary copies (add them to the C2 `COPIES`-style map or to
the next freeze receipt), or move boundary copies out of the frozen directory. Round 49; the
freeze receipt must not be edited now.

### F3 — wording / duplicate authority: the freeze receipt pins the SUT at its entering bytes

`evidence/freeze-sha256.txt` lists `tools/mori-pin-check.py` = `9832e38c…` (v2), a duplicate of
`controls/tool-v2-entering.py`. The contract preamble says "Frozen instrument bytes (sha256) are
printed in `evidence/freeze-sha256.txt` … If the working-tree bytes ever differ, the claim is
measured with `git show <freeze>:<path>`." At the landed tip the worktree tool is `85a89a3b…`
(v3) ≠ the listed digest, so a literal application of that fallback would measure C1 with the
**v2** tool, which the frozen receipt itself scores `C1=unmet junk_met=8`. P-C1 is the specific
predicate and explicitly says "the tool at R" and "with the tool at R", so P-C1 governs and C1 is
measurable and met-able; the conflict is in the preamble sentence, and it was invisible at freeze
because the tool was unchanged then (both wave-1 freeze audits read this line as a receipt).

Smallest safe correction: in the next contract, scope the fallback sentence to the eleven frozen
paths and annotate (or drop) the tool line, since `controls/tool-v2-entering.py` already carries
the entering bytes.

### F4 — evidence gap (landing class, not freeze): the C1 after-receipt is empty

`evidence/after-c1-at-e4dfff32.txt` was 0 bytes (mtime `19:37:41`, unchanged at my last read
~19:40); `after-c2-at-e4dfff32.txt` is 152 bytes with a complete `C2=met … rev=e4dfff32…` line.
Both are untracked, so neither is bound to the landing commit — the same shape as round-47's
routed defect 1 (`landing` class: seat results never committed). A concurrent w2 executor may
still be writing it; I record the observation, not a conclusion about that seat. The predicate is
unaffected (receipts are explicitly "not part of the predicate"), but the after-value of C1 has no
recorded bytes as of this review.

## 6. Precision notes (not defects)

- **O1** `freeze-sha256.txt` does not hash the eight frozen receipts even though the preamble says
  the controls "under `controls/` and `evidence/`" are frozen. The empty freeze→tip diff of
  `.ufo/waves/round-48/evidence` proves none was rewritten, so the gap is unexercised.
- **O2** `count-c1.py` measures the tool bytes at the `--tool` path on disk, not at R. At the landed
  tip the worktree tool is `cmp`-identical to `git show e4dfff32:tools/mori-pin-check.py`, and the
  tracked-dirty count is 0, so "the tool at R" holds now; it is a process guarantee, not a counter
  guarantee.
- **O3** A junk variant whose tool run crashes increments both `junk_met` and `errors`
  (`verdict()`, `:258`). The verdict is unchanged because both must be zero; the contract's
  "never unmet" holds for the per-variant `got` column.
- **O4** The landed registry repair leaves the two v3-exposed pins true at R (743 lines; `8b82ac99…`;
  `37fd7c24ff52…`), and the tool's own selftest pin (`PIN_CHECK_SELFTEST pass=60 fail=0`,
  `SKILL.md:938`) reproduces — so the honest-control leg is not passing on a stale registry.

## 7. Not verified here (owned by other seats)

- The 8-junk / 4-honest acceptance of the *landed* v3 tool (I verified only the real-registry leg
  and that all 12 variants are applicable and deterministic at R).
- The claim-by-claim review of the entry's 15 quotes (claim-follows-from-quote is a named limit of
  P-C2).
- The C2 after-run and the census/portability frontier items.

Report: .ufo/waves/round-48/w2/R48CritFreeze.md
