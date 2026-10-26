# Mo51RevPinCheckDiff — review of the v5 change to `tools/mori-pin-check.py`

Seat: Mo51RevPinCheckDiff (reviewer, wave w1) · round 51 · 2026-10-26
Reviewed pair: entering `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd` → data `87e0c374537557754bf71dd68036ded3ddc6699c`, `git diff … -- tools/mori-pin-check.py`
(+108/-29, 1 file). Working tree is at the entering tip; all data bytes were read
via `git show 87e0c374:<path>` into scratch and reviewed/executed from those bytes.

Method / environment:
- No LSP device is mounted in this session (not among `xd://` devices or MCP routes), so
  all semantic checks used `read`/`grep`/`git show` over committed bytes plus direct
  execution. Text findings below are backed by runnable probes, not grep-only claims.
- Host tools used: `git 2.56.0`, `python3 3.14.8`. No tool installed or updated
  (operator directive 2026-10-19: nothing to record).
- Scratch: `/fast/scratch/hyaku/mori-r51/Mo51RevPinCheckDiff/` (TMPDIR set there; disk
  guard checked before runs: 588G free on `/fast/scratch`).
- Host reads only; never mutated the lane, its jj state, or git index.

## 1. export_rev — shared clone, `--no-checkout`, `checkout --detach` (lines 870–886)

Code: `git rev-parse --verify <rev>^{commit}` in the source, then `git clone -q --shared
--no-checkout <repo> <dest>/tree`, then `git -C <tree> checkout -q --detach <full>`.

Probe results (fixture repos built in scratch; assert toplevel == fixture before commits):

| rev kind | result |
|---|---|
| branch ref | ok (clone head == resolved sha, working tree clean) |
| full sha / short sha / HEAD | ok |
| lightweight tag / annotated tag | ok (peels through `^{commit}`) |
| dangling (unreferenced) commit sha | ok (objects reachable via alternates) |
| true shallow source (`file:// --depth 1`, `.git/shallow` present) | ok for HEAD/tag/sha |
| empty repo (no commits) | returns None → `main` exits 2 `PIN_CHECK_SETUP unresolvable revision` (correct) |
| unresolvable string | returns None → exit 2 (correct) |
| source path containing spaces | ok |

Source-repo mutation: in every probe, `count-objects -v`, `for-each-ref`,
`status --porcelain` and `.git/objects/info/alternates` were byte-identical before and
after. The alternates file exists **only in the clone** and points at the source object
dir (verified: `.git/objects/info/alternates` → `<src>/.git/objects`). No write ever
hits the source repo. The `--shared` clone is thin (no object copy), so clone+checkout
of the ~305 MiB lane tree completes in seconds with the 300 s/600 s timeouts.

Defect (LOW, `pincheck-v5.py:879-885` + `main:920-922`): any clone/checkout failure — a
pre-existing non-empty `dest/tree`, a proxy/host error, a lock — collapses into the same
`return None` as an unresolvable revision, and `main` prints
`PIN_CHECK_SETUP unresolvable revision`. The message is misleading when the revision
resolved but the export failed. Unreachable in the normal flow (dest is a fresh
`mkdtemp`), so LOW.

## 2. Default scratch — `tempfile.gettempdir()` (line 912)

When `--scratch` is absent, `scratch_parent = tempfile.gettempdir()`. The measured
worktree at the data commit is **319,680,383 bytes (~305 MiB)** (`git ls-tree -r -l
87e0c374 | sum`). A bare `python3 tools/mori-pin-check.py --rev R` therefore writes a
>50 MiB tree under `/tmp`, which the operator directive 2026-10-25 caps at 50 MiB
("/tmp only for files under 50 MB"). The frozen counter always passes TMPDIR (arms A/B)
so scoring is compliant, but the tool's default mode violates the directive transiently.
The dir is removed on exit (finally rmtree), so the failure mode is peak disk use, not
residue. **MED** — recommend documenting/requiring `--scratch` or TMPDIR for large
repos (the docstring at 129–131 says "default: the TMPDIR temp dir" but not the size
implication).

## 3. rmtree on every path

- `main`: `finally: shutil.rmtree(scratch, ignore_errors=True)` (947–948) covers success,
  setup exits, and unresolvable-rev returns (the inner `return 2` still runs the finally).
- `run_cmd`: `finally: shutil.rmtree(tmp, ignore_errors=True)` (558–559) per-instrument
  tmpdir (under the measured tree's `.scratch`, which itself lives in scratch in `--rev`
  mode).
- `selftest`: `finally: shutil.rmtree(base, ignore_errors=True)` (1493–1494).
- No path creates a temp dir outside these three scopes. The only documented leftover is a
  SIGKILLed `--rev` run, which leaves the clone under scratch — never in the repo it
  reads (arm A evidence `c1-at-data.txt`: `kill_residue=0`). No gap found.

## 4. env/stale classification — every `mismatches` site classed

There are exactly five `counts["mismatches"] += 1` sites (grep), and each increments a
class in the same branch:
- 709 (truncated digest) → stale (710)
- 726 (line-count pin path not bound to the instrument) → stale (727), line ends `class=stale`
- 737 (line-count mismatch) → stale (738), line ends `class=stale`
- 820 (tally mismatch) → `kind = "env" if observed is None else "stale"` (824), `counts[kind] += 1` (825), line ends `class=env|stale` (826)
- 839 (full digest) → stale (840), line ends `class=stale`

`env` is incremented only at the tally site; every mismatch site therefore adds exactly
one class, so **env + stale == mismatches** structurally. Verified empirically over the
116 `PIN_CHECK=` summary lines of my selftest run: 0 violations. Match lines carry no
class; `unparsed`/`no_command`/`misattributed`/`env_unexpanded`/`dropped`/`rebound`/
`duplicate`/`hidden` are separate counters and do not enter `mismatches` (correct per arm
C, which counts only the five tally rows).

I rebuilt the frozen five-row fixture (`count-c1.py` FIXTURES/ROWS, exact sources) and ran
the data-bytes tool `--root` on it. Output reproduced the counter's expected lines
verbatim (matches `c1-at-data.txt`):

```
pin line=3 kind=tally prefix=ENVA_SELFTEST state=mismatch pinned='pass=3 fail=0' observed=None rc=2 cmd='python3 tools/enva.py --selftest' class=env
pin line=4 kind=tally prefix=ENVB_SELFTEST state=mismatch pinned='pass=4 fail=0' observed=None rc=1 cmd='python3 tools/envb.py --selftest' class=env
pin line=5 kind=tally prefix=STLA_SELFTEST state=mismatch pinned='pass=4 fail=0' observed='pass=5 fail=0' rc=0 cmd='python3 tools/stla.py --selftest' class=stale
pin line=6 kind=tally prefix=STLB_SELFTEST state=mismatch pinned='pass=2 fail=0' observed='pass=2 fail=0' rc=1 cmd='python3 tools/stlb.py --selftest' class=stale
pin line=7 kind=tally prefix=OKAY_SELFTEST state=match pinned='pass=1 fail=0' observed='pass=1 fail=0' rc=0 cmd='python3 tools/okay.py --selftest'
PIN_CHECK=unmet tally_pins=5 digest_pins=0 mismatches=4 … env=2 stale=2
```

Named limit (frozen rule, not offered as a fix — recorded): the env/stale split is
"no tally line ⇒ env; different tally or contradicting rc ⇒ stale". Two rule edges land
in the wrong bucket by design: an instrument that prints a partial tally then crashes on a
missing host path ⇒ `stale` (environmental); an instrument that prints two disagreeing
tally lines ⇒ `observed=None` ⇒ `env` (it ran). Both are consistent with the contract's
named limit and are analyzed in more depth by seat `Mo51CritClassRule`; no count in the
frozen fixture hits them.

## 5. Summary format change — consumers

The `PIN_CHECK=` line gained trailing ` env=N stale=N` (857–866). Consumer survey (grep of
the whole lane + fleet `scripts/hyaku`):
- `count-c1.py` (frozen): arm B `last.startswith("PIN_CHECK=met")` (OK); arm C
  `last.endswith(" env=2 stale=2")` (OK, verified above); arm D parses the separate
  `PIN_CHECK_SELFTEST pass=N fail=0` line (OK). No consumer breaks.
- `conform.py` at the data commit: zero `PIN_CHECK` references (grep). Not a consumer.
- `scripts/hyaku` (fleet): zero files reference `PIN_CHECK`.
- Round-49 `controls/tool-*.py`, `stub-*.py`, `count-c1.py`: historical fixtures that run
  the v3 tool; they never run v5 and are not invoked by this round's automation.
- The SKILL.md self-pin cell was updated in the same data commit: `pass=114` →
  `pass=119`, `--scratch DIR` added, class semantics documented. Consistent (the selftest
  floor is N ≥ 114; 119 clears it).

## 6. The five new selftest arms (1441–1483)

| arm | what it pins | can it fail? |
|---|---|---|
| `v5_class_env_setup_error` | envtool.py exits 2 with a setup-error line, no tally → exactly one line ending `class=env`, summary ` env=1 stale=0` | yes — fails if classification changes |
| `v5_class_env_timeout` | reuses existing `tools/slow.py`, tmo=2 → `TimeoutExpired` → `(None,"timeout")` → env | yes — exercises the timeout path (run_cmd 554–555) |
| `v5_class_stale_tally` | foo.py prints a different tally → stale | yes |
| `v5_class_stale_digest` | full 64-hex digest pin of `tools/foo.py` with zeros → stale | yes |
| `v5_rev_export_outside_repo` | full CLI `--rev HEAD --repo <grepo> --scratch <xs>`: rc=0, `PIN_CHECK=met`, grepo clean, no `<grepo>/.scratch`, `xs` emptied | yes — fails if the export lands in the repo, leaves residue, or breaks clone/checkout |

All five PASS in my run from the data-commit bytes; the run printed **119 PASS / 0 FAIL,
`PIN_CHECK_SELFTEST pass=119 fail=0`, rc=0** (entering 114 + 5 new arms = 119), matching
`c1-at-data.txt` (`selftest=pass=119,fail=0`). No arm is vacuous; each asserts a
characteristic string that the corresponding regression would break.

## 7. Removed tarfile import

No `import tarfile` remains; grep for `tar` shows only unrelated words/`startswith`
calls. The `git archive`/`tarfile.extractall` path is fully gone from `export_rev`
(verified in the v5 bytes).

## Findings

- **MED** — default scratch is `tempfile.gettempdir()`; a bare `--rev` run writes a
  ~305 MiB worktree (data-commit `ls-tree` sum 319,680,383 B) under `/tmp`, above the
  operator's 50 MiB `/tmp` cap (directive 2026-10-25). Removed on exit, so transient.
  `tools/mori-pin-check.py:912` (docstring 129–131).
- **LOW** — any clone/checkout failure collapses into `PIN_CHECK_SETUP unresolvable
  revision`, hiding the real cause (e.g. non-empty `dest/tree`). `tools/mori-pin-check.py:879-885, 920-922`.
- **LOW (named limit, frozen rule)** — classifier edges misstate env vs stale: partial
  tally then crash ⇒ stale; two disagreeing tally lines ⇒ env. Not a change proposal —
  recorded per contract. `tools/mori-pin-check.py:824-826`.
- **INFO / verified clean** — export_rev handles branches, shas, HEAD, tags, dangling
  commits, shallow sources, empty repos; never writes into the source (alternates only in
  the clone); rmtree covers every normal and error path; env+stale==mismatches holds at
  all five sites (0 violations over 116 summary lines); summary format breaks no consumer
  (`count-c1.py` startswith/endswith checks pass; `conform.py` and `scripts/hyaku` don't
  parse it); the five new selftest arms each fail independently and all pass; tarfile
  import cleanly removed.

Residual gaps: I did not rerun the full `--rev` score or the SIGKILL arm against the real
lane (that is the frozen counter's run; evidence `c1-at-data.txt` covers it, and the L1
re-runs counters); bubblewrap arm B portability is the counter's arm, not reviewed here.
