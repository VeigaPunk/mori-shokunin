# Mo60Executor58 — boundary PoC re-run (evil-blob, both tool paths)

Seat: executor, leaf. Work read-only on the lane. No commits, no VCS mutation,
no fleet/sibling writes. Scratch: `$HYAKU_SCRATCH/mori-r60/Mo60Executor58/`
(`/fast/scratch/hyaku/mori-r60/Mo60Executor58`), `TMPDIR` set there, all
`--scratch` dirs under it, cleaned before yield. Disk guard read green before
heavy work (`scripts/hyaku/disk-guard.sh status`: `/fast/scratch/hyaku` 26%
used, 597.8G free). No tool installed or updated this seat.

Frozen contract read first: `.ufo/waves/round-60/contract.md` (freeze
`ac496c7cde8cad965079858accae3bedfe4a73f2`, entering
`ddfb12fb0838b4307c445194a844f0c4b1950195`). Lane tip observed at
`0f8340cf62b588fd64be8d9176ed7d5444c426b2` (four commits past the freeze; the
lane moved under the wave as the brief warned). Every re-derivation below is
pinned to a named revision via `git show <rev>:<path>`, never to a working-tree
read.

## Verdict

The routed G1 closure **holds for the pinned r60 count-c2 on both tool paths**
(no unpinned blob is ever materialized or executed). The **r59 counter's hole
reproduces** and is in fact wider than the contract's phrasing: the blob is not
merely executed under the counter's scratch — on the scan and drift arms it is
executed with **no `--scratch` at all**, so it writes into the *invoker's cwd*,
which is arbitrary (I reproduced writes at the lane root and at the fleet root
while running from there). The frozen count-c3 G1 `no_exec` assertion only
scans `<scratch>/g1-new`, so a scan-arm-only blob escapes undetected and
`toolgate` still reads `ok`. C3's *published* claim is satisfied; its *control
strength* is weaker than the "closed boundary" reading, and that is routed
below as a finding, not a remediation (frozen bytes stand; kill rule applies).

## Fixtures (git-fixture rule)

Every fixture is an explicit scratch path, `git -C <path> init -q`, toplevel
asserted with `git -C <path> rev-parse --show-toplevel` printing the fixture
dir, throwaway identity per commit, no commit outside the throwaway repo.

| fixture | rev | shape |
|---|---|---|
| `poc-exec.aIAhT5` | `42f76bead8cb49e18ae0be61d2e3affd0d7eb95a` | minimal: both tool paths = frozen `EVIL_BLOB` |
| `poc-full.A1l4k3` | `3b5c6789708ad5cadded60517f60dc85fa81a369` | full lane tree at `ac496c7c` (13 335 tracked files), both tool paths evil |
| `poc-ec-evil` | `f5f65b5dac44734e62255b919ba59ef9c0d4234c` | full tree, EC evil / scan genuine |
| `poc-scan-evil` | `312af9e898f7c5ca40bad25408b5d32b3d9acbaa` | full tree, EC genuine / scan evil |
| `poc-trace` | `25037081185e3ba6593f0a7b9d216afda79e9d86` | full tree, scan path = arm-tracing blob |
| `poc-blind` | `ce145ed25c9750d8611714bda034fa805ad2cdf1` | full tree, scan path = cwd-writing `EXEC-MARKER` blob, EC genuine |
| `poc-gen-clean` | `e703d0b82b18ec3c1fbd509622e3d655ad34a555` | full tree at `ac496c7c`, both tools genuine (baseline) |
| `poc-gen-g3` | `67cb884a15edbfae13a417588e8837d510c3fc79` | genuine tools, `h01` expect.txt tampered |
| `poc-gen-g3h02` | `382d9c6e05fbb1706f3750e967a89d9f1de29e79` | genuine tools, `h02` expect.txt tampered |

`EVIL_BLOB` was extracted **from the frozen counter itself**, not retyped:
`count-c3.py:66-84` at `ac496c7c`, sha256
`c045efed889ad77d81e51c8a6fc12d0fd36d503d9ec5e94649540ab83b85422e`, 480 bytes.
The blob writes `EXEC-MARKER` into `--scratch` when given one and into `"."`
otherwise, then prints both expected selftest lines and exits 0.

Counters materialized and pinned before use:
`r59-count-c2.py` = `git show 7b86704d…:.ufo/waves/round-59/count-c2.py`,
sha256 `2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be`;
`r60-count-c2.py` = `git show ac496c7c…:.ufo/waves/round-60/count-c2.py`,
sha256 `8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976`
= the frozen `PIN_C2` (`count-c3.py:63`).

## A. Minimal PoC, both tool paths evil — `42f76be`

Command shape, both runs:

```
python3 <materialized counter> 42f76be… --repo <poc-exec.aIAhT5> --scratch <dir>
```

**OLD (r59 count-c2 @ 7b86704d), exit 1**, marker **present**:

```
C2=unmet selftest=ok scan=bad drift=bad trees=bad entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=42f76bead8cb49e18ae0be61d2e3affd0d7eb95a failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,…,drift,entry_absent,scan,scan_absent:…,tool_sha
```

`selftest=ok` is the hole in one token: the unpinned blob's forged
`ENTRYCLAIMS_SELFTEST pass=13 fail=0` was accepted. Marker:
`run-old/st2/EXEC-MARKER` = `executed --selftest --scratch …/run-old/st2`.

**NEW (r60 count-c2 @ ac496c7c), exit 1**, marker **absent**:

```
C2=unmet selftest=bad scan=bad drift=bad trees=bad entry=bad rows=bad pins=bad tree=bad claims=0 files=0 spans=0 rev=42f76bead8cb49e18ae0be61d2e3affd0d7eb95a failed=copy_absent:…,drift,entry,entry_absent,pins,rows,scan,scan_absent:…,tool_sha
```

`selftest=bad` and `failed` carries `tool_sha`; `markers_under(run-new)` = 0
and `<scratch>/run-new` contains no files at all — the unpinned bytes were never
even written to disk (`count-c2.py:169` and `:179` gate `write_bytes` on the pin).

## B. Full-tree PoC, both tool paths evil — `3b5c6789`

Same command shape against the 13 335-file tree, so both counters do maximal work.

**OLD, exit 1**, marker **present** (1):

```
C2=unmet selftest=ok scan=bad drift=bad trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=3b5c6789708ad5cadded60517f60dc85fa81a369 failed=drift,scan,tool_sha
```

Everything else — trees, entry, rows, pins, tree — reads **`ok`** because the
evil blob forges both selftest lines and the old counter never re-derives
`entry`/`rows`/`pins` through the tool; the only reasons are the three arms that
independently re-run the blob. `full-old/tool2.py` exists and sha256-equals the
evil blob (`c045efed…422e`).

**NEW, exit 1**, marker **absent** (0):

```
C2=unmet selftest=bad scan=bad drift=bad trees=bad entry=bad rows=bad pins=bad tree=ok claims=0 files=0 spans=0 rev=3b5c6789708ad5cadded60517f60dc85fa81a369 failed=drift,entry,pins,rows,scan,scan_tool_sha,selftest,tool_sha,tree:h00-good-control:tool,…,tree:h12-no-frontmatter:tool,trees
```

`full-new` contains only `real`, `root`, `trees` — no `ec-tool.py`, no
`scan-tool.py`.

## C. Per-path isolation (which path carries the hole)

| fixture | old counter | new counter |
|---|---|---|
| EC evil / scan genuine (`f5f65b5d`) | exit 0 — **`C2=met`** … claims=13 files=6, markers 0 | exit 1 — `failed=…,selftest,tool_sha,tree:*:tool,…` , markers 0 |
| scan evil / EC genuine (`312af9e8`) | exit 1 — `failed=drift,scan,tool_sha`, markers **1** | exit 1 — `failed=drift,scan,scan_tool_sha`, markers 0 |

The old counter's *only* contribution toward safety is the `tool_sha` reason it
appends at `count-c2.py:203` (r59) — a **report** line, not a gate. It does not
short-circuit: `tp.write_bytes(tool_b)` at r59 line **206** happens for *any*
present blob, and the three exec sites (lines **210**, **235**, **258**) all
run unconditionally on `tool_b is not None`. That is why the EC-evil tree scores
a clean `C2=met` while executing an attacker blob.

The new counter gates at `run_pinned` (`count-c2.py:144-150`, sha test at
`:147`) and never materializes on mismatch (`:169`, `:179`).

## D. The wider old hole: execution with no `--scratch` (cwd write)

The contract stub at `contract.md:106-107` says "no marker anywhere under its
scratch". That is *narrower* than the real defect. Numbered from
`git show 7b86704d…:.ufo/waves/round-59/count-c2.py`:

- line **210-211** — selftest arm: `--scratch <scratch>/st2` **is** passed.
- line **235** — scan arm: `["python3", tp] + [paths]`, **no `--scratch`**.
- line **258** — drift arm: `["python3", tp, path]`, **no `--scratch`**.

`EVIL_BLOB`'s fallback is `base = pathlib.Path(".")` when `--scratch` is absent,
so the scan and drift arms make the blob write into the **counter's cwd**.

Proof (counter `--scratch` inside scratch, cwd deliberately elsewhere, full-tree
evil PoC `3b5c6789`):

```
cwd=/…/cwd-yryrNg   counter --scratch=/…/final-old
markers_in_scratch=1   markers_in_cwd=1
cwd contents: EXEC-MARKER
```

Arm attribution via a tracing blob on the scan path (`poc-trace`
`2503708118`), cwd write recorded per arm:

```
TRACE-scan1 :: …/trace-scratch/real2/round-53/w1-results.json
TRACE-scan5 :: …/real2/round-54/… …/round-55/… …/round-56/… …/round-57/… …/round-58/…
markers in --scratch: none
```

Both the drift (1 path) and scan (5 paths) invocations escaped; the selftest
invocation did not (it passes `--scratch`).

**Live consequence, recorded:** because the counter inherits the invoker's cwd,
running the old-counter PoC from the lane root wrote
`/home/vgpnk/Projects/shokunin/mori-shokunin/EXEC-MARKER`, and running it from
the fleet root wrote `/home/vgpnk/Projects/shokunin/EXEC-MARKER`. Both were
untracked and created **solely by my probe**; I copied each byte-for-byte into
scratch (`marker-at-lane-root.txt.evidence`,
`marker-lane-2.txt.evidence`, `marker-fleet-root.txt.evidence`) and deleted them.
Lane `git status --porcelain` is now back to its pre-probe set
(`.ufo/waves/round-60/evidence/c1-at-data.txt`, `w1.ready`,
`w1.ready.dispatched`, `w1/`), lane HEAD still
`0f8340cf62b588fd64be8d9176ed7d5444c426b2`, and no marker remains at either root.
Recorded contents:

```
executed /…/full-old/real2/round-53/w1-results.json
executed /…/se-old/real2/round-53/w1-results.json
executed /…/ap-old/real2/round-53/w1-results.json
```

This is the same class the wave's own lesson
(`corpus/lessons/round-60.md`, "Wave-found instrument defects" item 5) records;
my run reproduces it and adds the attribution the lesson does not state (which
arms, and that the escape target is the invoker's cwd, not the counter's
scratch).

## E. The frozen count-c3 G1 check inherits the same blind spot

`count-c3.py:173` is `no_exec = len(markers_under(s_new)) == 0` — it scans only
`<scratch>/g1-new`, i.e. the *new* counter's scratch. The old-arm control at
`:186-198` runs the r59 counter and looks for markers under `<scratch>/g1-old`,
which catches the **selftest** write. Neither check can see a scan-arm escape
into the invoker's cwd.

Demonstrated on `poc-blind` (`ce145ed2`): full tree at `ac496c7c`, genuine EC
tool, scan tool = blob that writes `EXEC-MARKER` **only** on the scan/drift
shape (no `--scratch`, path args present). Driving the **old** counter exactly
as count-c3's G1-new arm does:

```
old exit=1
markers under s_new      : 0
markers in invoker cwd   : 1  -> scan-arm executed
stdout: C2=unmet selftest=ok scan=bad drift=bad trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 rev=ce145ed25c9750d8611714bda034fa805ad2cdf1 failed=drift,scan,tool_sha
count-c3 G1-new verdict on this run: toolgate = True (gated=True, no_exec=True)
```

`gated` is `"tool_sha" in out and "tool_absent" not in out` (`count-c3.py:174`).
Two independent leniencies make it `True` even here: the token `tool_sha` is a
**substring** of `scan_tool_sha`, and the reason is only *reported*, never gating
execution. So a scan-arm-only attacker scores `toolgate=ok` while having
executed. Two further confirmations of the same check's softness:

- the c3-shaped PoC (tools only, no wave data — `b64f8290`) yields
  `markers=0` and `selftest=ok` on the old counter, so the frozen G1 control
  passes **only** because it happens to route through the selftest arm, which is
  the one arm that passes `--scratch`;
- `toolgate`/`containment`/`expectgate` labels at `count-c3.py:300-305` are
  `"ok" if "toolgate" not in failed and "g1_new_skipped" not in failed`, and
  bare `toolgate`/`containment`/`expectgate` are **never appended** to `failed`
  (`grep` returns none); the label is controlled solely by `*_skipped`. Verbatim
  replay of that expression: `g1_new_executed:…`, `g1_new_no_tool_sha`,
  `g1_old_control_did_not_reproduce`, `g2_parent_escape`, `g2_escape_written`,
  `g2_symlink_escape`, `g3_no_tamper_flag` **all print `ok/ok/ok`**.

This duplicates and independently confirms the wave's routed item 1
(`count-c3` verdict composition, Mo60Reviewer13/02) — my contribution is that the
blind spot is *reachable through the C3 PoC shape itself*, not only through a
pre-seeded marker.

## F. Arms that hold (controls the claim needs)

**Honest baseline, genuine tools** (`poc-gen-clean` `e703d0b8`, full tree at
`ac496c7c`): r60 count-c2 **exit 0**

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=e703d0b82b18ec3c1fbd509622e3d655ad34a555
```

markers 0. On the real lane the same line reproduces at the freeze
(`ac496c7c`) and at the tip (`0f8340cf`), both exit 0, markers 0 — identical to
`evidence/c2-at-freeze.txt`.

**G2 containment**, independent probe of the pinned module's `materialize()`
(not count-c3's own script):

```
dotdot=False inside=True symlink_parent=False symlink_abs_escape=False abs_rel=False
escape.txt written: no;  writes into symlink target dir: none;  absolute rel written: no
```

Note the symlink cases hold for **both** a dangling and an existing absolute
target, so the routed F2 remark (dangling-in-root symlink) does not weaken the
result on my probe.

**G3 expectgate**, genuine tools, tampered expect.txt:

- `h02-malformed-claim` tampered → `failed=expect_tamper:h02-malformed-claim,trees`, otherwise `selftest=ok scan=ok drift=ok entry=ok rows=ok pins=ok tree=ok claims=13`.
- `h01-semantically-empty` tampered → `failed=expect_tamper:h01-semantically-empty,trees` (the flag is not hardcoded to h02).
- untampered genuine tree → no `expect_tamper` reason at all.

**Do-nothing controls** re-derived from the lane, both byte-equal to the
committed receipts:

- `count-c3.py ddfb12fb…` → `C3=unmet toolgate=bad containment=bad expectgate=bad cases=1 rev=ddfb12fb… failed=count_c1_absent,count_c2_absent,g1_new_skipped,g2_skipped,g3_skipped`,
  exit 1, byte-equal to `evidence/control-c3-do-nothing.txt`; 1 marker under
  its own `g1-old`.
- `count-c2.py ddfb12fb…` → `C2=unmet selftest=bad scan=ok drift=ok trees=bad entry=bad rows=bad pins=bad tree=ok claims=0 files=0 spans=0 … failed=entry,pins,rows,selftest,tool_absent,trees,trees_set`,
  exit 1, byte-equal to `evidence/control-c2-do-nothing.txt`.

**Selftests** (frozen instruments at tip): `C3_SELFTEST pass=3 fail=0`,
`C2_SELFTEST pass=8 fail=0`, `C1_SELFTEST pass=6 fail=0`, all exit 0.

**count-c3 end-to-end at both revisions**: `C3=met toolgate=ok containment=ok
expectgate=ok cases=6` at `ac496c7c` and at `0f8340cf`, exit 0 both. The frozen
`count-c2`/`count-c1`/`contract`/`trees-c2h-expects` bytes are byte-identical
between freeze and tip (`sha256` compared for all five), so the claim is stable
under the lane movement.

**count-c1 executes no repo-supplied tool**: its only non-git `subprocess.run`
is at `count-c1.py:130`, running a **revision-pinned** r59 counter fetched with
`git show 7b86704d…` (`:127`, `:124`), with `--scratch` and `TMPDIR` set. G1 is
structural there, as the contract says.

## Findings

1. **HIGH — old-counter escape is cwd-wide, not scratch-wide.** r59
   `count-c2.py:235` and `:258` invoke the blob with no `--scratch`; a blob that
   writes on relative paths escapes to the invoker's working directory. Proven
   by marker at the lane root and at the fleet root, and by arm-attributing
   traces (`TRACE-scan1`, `TRACE-scan5`). The frozen contract's phrasing
   (`contract.md:106-107`, "no marker anywhere under its scratch") only covers
   the selftest arm; the C3 claim as written is satisfied, but the boundary is
   not closed in the sense the attack class implies.
2. **HIGH — count-c3 G1 does not detect a scan-arm escape.** `count-c3.py:173`
   scans only `g1-new`; the old-arm control at `:186-198` scans only `g1-old`.
   A scan-arm-only blob (`poc-blind` `ce145ed2`) writes `EXEC-MARKER` to the
   invoker cwd and still scores `toolgate=True`. The C3 PoC also routes only
   through the selftest arm, which is the one arm that passes `--scratch`, so
   the control never exercises the escaping path.
3. **MEDIUM — `gated` matches `tool_sha` as a substring.** `count-c3.py:174`
   accepts `scan_tool_sha` as satisfying `tool_sha`; the two are distinct
   failure classes in the new counter (`count-c2.py:162-179`). Reproduced on
   `se-new.out` (`failed=drift,scan,scan_tool_sha` → `gated=True`).
4. **MEDIUM — count-c3's three published labels are not derived from `met`.**
   `:300-305` map to `*_skipped` only; the gate-specific failure tokens
   (`g1_new_executed:*`, `g1_new_no_tool_sha`, `g1_old_control_did_not_reproduce`,
   `g2_parent_escape`, `g2_escape_written`, `g2_symlink_escape`,
   `g3_no_tamper_flag`) are never appended as bare labels, so each such failure
   renders as `ok`. Verbatim replay in section E. (Confirms the wave's routed
   item 1 from an independent construction.)
5. **INFO — old counter reports but does not gate the EC-path sha.**
   `f5f65b5d` scores `C2=met` on the old counter with an evil EC tool installed;
   `tool_sha` at r59 `:203` is a reason string, and `:206`/`:210` run anyway.
   This is the exact attacker shape the C2 H-series was frozen to kill.
6. **INFO — the new counter's pin gate is exact.** Unpinned bytes are neither
   written nor executed (`ec-tool.py` / `scan-tool.py` absent from every dirty
   scratch), and appended-byte tampering (genuine EC tool + `EVIL_BLOB` appended,
   `790d1acc…`) is also refused with `tool_sha`, markers 0.

## Hygiene / blast radius

- Untracked `EXEC-MARKER` created by my probes at the lane root
  (13:16:28, 13:18:05) and at the fleet root (13:20:36): captured byte-exact
  into scratch, then deleted. No tracked file was ever touched; lane HEAD
  unmoved; `git status` at both roots shows no marker.
- No pacman, no tool installs, no commits, no push, no sibling/fleet writes, no
  subagent dispatch.
- Scratch cleaned of fixtures after the receipt bundle
  (`/fast/scratch/hyaku/mori-r60/Mo60Executor58` removed).

## Commands to reproduce the two headline results

```
D=$(sed 's/^D=//' <scratch>/fullpath.txt); REV=$(cat <scratch>/fullrev.txt)
# old (hole):
cd <scratch>; mkdir -p old-scratch && python3 r59-count-c2.py "$REV" --repo "$D" --scratch old-scratch
# new (gate):
mkdir -p new-scratch && python3 r60-count-c2.py "$REV" --repo "$D" --scratch new-scratch
# marker search, both roots:
find <counter-scratch> -name EXEC-MARKER; find "$PWD" -maxdepth 1 -name EXEC-MARKER
```
