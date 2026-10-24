# ExeC1Selftest — committed C1 selftest at the measured revision

## Result

`CONFORM_SELFTEST pass=14 fail=0`, exit status **0**, in a fresh disposable clone checked
out detached at the measured revision. All fourteen per-mutation lines were **PASS**; there
was no FAIL line. stderr was empty (0 bytes). Elapsed wall time **68 s** (shell-measured
`ELAPSED=68s`; job wall 69.46 s). The checker was not edited.

The same selftest was repeated in a second independent clone at the control-after revision
`aa161e998eb22282e3d96ed2710bb0b39e5163de`; both runs produced **byte-identical** output
(sha256 `096c8c833a34c4277018ca7ed4fec0fc7c019cf7496bb5728c5e95ae3a72c1d6`, 15 lines) and
exit 0.

## Revision binding (why this revision is measurable)

| revision | role | `.ufo/waves/round-41/conform.py` | `fixtures/c1/count-c8.py` |
|---|---|---|---|
| `7450722e5f3b4fc6df3d719386ed643af59630e3` | lane tip / primary measured rev | `e1f2e11e…475427` | `4e4d50eb…02f6da` |
| `aa161e998eb22282e3d96ed2710bb0b39e5163de` | `control-after.txt` revision | `e1f2e11e…475427` | `4e4d50eb…02f6da` |
| `62a207f7521fa2e2fcd2e8b0260f047ccfce8862` | contract entering tip | `e3b0c442…b855` = empty blob (file absent) | empty blob (file absent) |

- `conform.py` digest equals the `freeze-r41.txt` pin
  `e1f2e11e7556cb4522c36cf22b3666650561e8eba0a7a7e85dc8c22c65475427`; the counter equals
  the pin `4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da`.
- The checker first exists at `d72ac167` (`git log -- .ufo/waves/round-41/conform.py` shows
  only that commit), so `62a207f7` cannot host the committed selftest; the measured range is
  `d72ac167..7450722e`, over which the checker, counter, round-39 contract
  (`fc36841b…8ebcd3`) and witness fixture (`8ac9e82b…cb4af`) are byte-invariant.
- Interpreter: `/usr/bin/python3` — Python 3.14.8 (main, Oct 2 2026) [GCC 16.2.1].

## Exact commands and output

Sandbox creation (per revision), isolated from the lane working tree:

```text
SB=$(mktemp -d /tmp/mori-r41-exe-c1-tip-XXXXXX)        # primary:  /tmp/mori-r41-exe-c1-tip-4Uv8vh
git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin "$SB/repo"
git -C "$SB/repo" checkout -q --detach 7450722e5f3b4fc6df3d719386ed643af59630e3
git -C "$SB/repo" rev-parse HEAD
```

```text
7450722e5f3b4fc6df3d719386ed643af59630e3
PRE_STATUS=[]                          # clean detached checkout, no working-tree edits
```

Run (cwd = sandbox repo; `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_CONFIG_GLOBAL`
unset, `LC_ALL=C`):

```text
/usr/bin/python3 .ufo/waves/round-41/conform.py \
  7450722e5f3b4fc6df3d719386ed643af59630e3 \
  --repo /tmp/mori-r41-exe-c1-tip-4Uv8vh/repo \
  --contract /tmp/mori-r41-exe-c1-tip-4Uv8vh/repo/.ufo/waves/round-39/contract.md \
  --counter /tmp/mori-r41-exe-c1-tip-4Uv8vh/repo/.ufo/waves/round-41/fixtures/c1/count-c8.py \
  --selftest
```

Output (verbatim, all 15 lines; `EXIT=0 ELAPSED=68s`):

```text
PASS predicate          predicate token changed -> only predicate failed
PASS head_pin           pin label renamed -> only head_pin failed
PASS tool_resolve       relative resolution removed -> only tool_resolve failed
PASS bounded_reads      git helper run timeout removed -> only bounded_reads failed
PASS timeout_scope      timeout value replaced with None -> only timeout_scope failed
PASS timeout_scope_shadow function-local None shadow inserted -> only timeout_scope failed
PASS timeout_scope_walrus walrus timeout binding to None -> only timeout_scope failed
PASS timeout_scope_tupleunpack tuple-unpacked timeout binding to None -> only timeout_scope failed
PASS timeout_scope_deadloop dead-loop rebind must not outrank the source-ordered binding -> only timeout_scope failed
PASS drain_bind         communicate drains replaced by wait+read -> only drain_bind failed
PASS drain_bind_decoy   decoy used communicate beside a wait+read drain -> only drain_bind failed
PASS timeout_state      budget flag ignored -> only timeout_state failed
PASS scratch            scratch parent moved off-lane -> only scratch failed
PASS selftest_conjunct  communicate timeout keyword stripped -> only selftest_conjunct failed
CONFORM_SELFTEST pass=14 fail=0
```

Second sandbox at the control-after revision `aa161e99…` (same command shape, sandbox
`/tmp/mori-r41-exe-c1-after-7QIxXm`, same explicit `--contract`/`--counter` overrides):
`EXIT=0 ELAPSED=68s`, 14 PASS / 0 FAIL, stderr 0 bytes, and `diff -u` against the primary
output is empty. `grep -c '^PASS '` = 14, `grep -c '^FAIL '` = 0.

## What the output establishes

- Every mutation anchor was present in the counter bytes: the `FAIL … anchor absent` branch
  never fired, so all fourteen mutations were actually applied to copies of `count-c8.py`.
- Every arm flipped **exactly** its expected check (`failing == [want]`, with the five alias
  arms `timeout_scope_shadow|walrus|tupleunpack|deadloop` → `timeout_scope` and
  `drain_bind_decoy` → `drain_bind` resolved through `MUTATION_CHECK_ALIAS`). A mutation that
  flipped nothing, flipped a second check, or was unwired from `evaluate` would have printed
  `FAIL … failing=[…] (want [..])` and changed the tally.
- The three r40 survivor constructions are inside this table
  (`timeout_scope_walrus`, `timeout_scope_tupleunpack`, `timeout_scope_deadloop`), so their
  detection mechanism is exercised by the 14/0 result; the survivor fixtures themselves are
  other seats' scope.

## Isolation and no-harm evidence

- Fresh `git clone --shared --no-checkout` of the lane, then `checkout --detach <rev>`;
  `git rev-parse HEAD` equals the requested revision in both sandboxes, and
  `git status --porcelain` was empty **before and after** each run (`wc -l` = 0). The
  `--shared` alternates file points at the lane object store for read-only object access;
  no lane Git metadata, index, ref or jj state was written.
- The selftest materialises its mutation copies under `<repo>/.ufo/waves/round-41/scratch`
  (sandbox clone only) and removes them in its `finally`; `ls -A …/round-41/scratch` after
  the run listed **no entries** in either sandbox.
- Lane state unchanged by this seat: `git rev-parse HEAD` = `7450722e…`, `git status
  --porcelain` still only the three pre-existing untracked wave-run/w1 entries, lane
  `.ufo/waves/round-41/scratch` **absent**, and lane `conform.py` sha256 still
  `e1f2e11e…475427` (no checker edit).
- No package, tool, build, lint or formatter was run or installed; no file outside this
  report was written.

## Residual coupling (recorded, not a target of this seat)

- `conform.py:72` binds `HANG_FIXTURE = os.path.join(LANE, ".ufo/waves/round-39/fixtures/hang-after-flush.py")`
  to the absolute **lane** path. The `timeout_state` check therefore executes the
  lane-resident fixture from inside the sandbox. This is a read-only coupling: the lane file
  is byte-identical at all three measured revisions (`6474105…7a87ca`) and equals the
  measured checkout's blob, no lane write occurs, and the result is unchanged in both
  sandboxes. A future edit to that lane fixture would, however, alter a sandbox run.
- `conform.py:66-70` default `DEFAULT_COUNTERS`/`DEFAULT_CONTRACT` to `LANE`; both were
  overridden with explicit sandbox paths, so those defaults were not exercised.
- Reading of "measured revision": the contract's after receipts were taken at `aa161e99`,
  the lane tip is `7450722e`, and the difference is receipts/lesson/calibration only. Both
  were measured; the outputs are byte-identical, so the 14/0 target holds under either
  reading. The reported primary is the lane tip `7450722e`.

## Risks and blockers

- No blocker. The frozen target for this item (`14-arm selftest passes 14/0`) is met at a
  clean checkout whose live HEAD equals the measured revision.
- Residual risk is the absolute-lane `HANG_FIXTURE` read above and the `--shared` object
  alternates (a concurrent lane object prune could break a mid-run sandbox; it did not).
- Tooling record: none installed or updated.
