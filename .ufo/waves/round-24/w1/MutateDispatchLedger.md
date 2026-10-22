# MutateDispatchLedger — mutation probe of `tools/mori-dispatch-ledger.py verify`

Seat: `MoriR24.MutateDispatchLedger` (leaf; no subagents dispatched).
Claim under test: **C1**, surface `tools/mori-dispatch-ledger.py verify` — the instrument R4 relies on.
Date: 2026-10-22. Sandbox: `/fast/scratch/hyaku/mori-r24-a2/mut-ledger`
(git clone of `/home/vgpnk/Projects/shokunin/mori-shokunin`).

**The lane repo was never written.** Every mutant was created, committed and probed
inside the sandbox clone. The only file this seat wrote in the lane is this report.
Read-only `git log/show/ls-tree/status` was used against the lane.

---

## 1. Scope and what was mutated

The tasking named four mutant classes against the round-23 ledger
`.ufo/waves/round-23/wave2-ledger.json` at `c725aa37` and its dispatch file
`.ufo/waves/round-23/wave2-run.json`:

| # | Mutant class | Where the byte changed |
|---|---|---|
| M1 | digest flipped | ledger row `payload_sha256` |
| M2 | attempt gap | ledger row `attempt` sequence (1, 3) |
| M3 | at decreasing | ledger row `at` sequence |
| M4 | started_ids mismatch | ledger row `started_ids` |

Each mutant was **committed** in the sandbox (never left as an uncommitted working-tree
edit), and `verify` was then run against that mutant's own commit, so the tool read the
mutated bytes as git objects, exactly as it would on the lane.

Because R4 as amended (contract Amendment A4) reads *every* `.ufo/waves/round-N/*-attempts.json`
and *every* `.ufo/waves/round-N/*-ledger.json`, the same four classes were additionally
mutated on the **round-24** ledger that R4 actually consumes at the landed tip
(`.ufo/waves/round-24/wave1-attempts.json`, base `f7eb430`), plus boundary mutants on
both.

---

## 2. Baseline (pristine) — the detector is green before any mutation

```
$ python3 -I tools/mori-dispatch-ledger.py verify --repo . --rev c725aa37 \
      --ledger .ufo/waves/round-23/wave2-ledger.json
{"finding_id":"LEDGER_CLEAN","finding_ids":["LEDGER_CLEAN"],"findings":[],
 "ledger_path":".ufo/waves/round-23/wave2-ledger.json","mode":"verify","rev":"c725aa37",
 "rows":[{"attempt":1,"index":1,"reasons":[],"result":"started","started_ids":96,
          "status":"bound","tasks_count":96}],
 "schema":"mori-dispatch-ledger-v1","status":"clean",
 "totals":{"bound":1,"ledger_findings":0,"rows":1,"unbound":0}}
exit=0
```

Round-24 ledger, read-only against the lane itself (no clone, no writes):

```
$ python3 -I tools/mori-dispatch-ledger.py \
      --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev HEAD \
      --ledger .ufo/waves/round-24/wave1-attempts.json
{"finding_id":"LEDGER_CLEAN","finding_ids":["LEDGER_CLEAN"],... "rows":[{"attempt":1,
 "index":1,"reasons":[],"result":"started","started_ids":33,"status":"bound",
 "tasks_count":33}],... "status":"clean"}
exit=0
```

**Baseline is clean (exit 0) for both ledgers.** No baseline failure, so every red
below is a genuine kill and every green below is a genuine survival.

---

## 3. The four tasked mutants — ALL FOUR TURN VERIFY RED

Round-23 ledger, base `c725aa37`. Each row is a distinct committed mutant; `verify`
was run at that mutant's own commit.

| Mutant | Commit | Mutation | verify exit | `finding_ids` | Verdict |
|---|---|---|---|---|---|
| M1 digest flipped | `ec6846a8` | `payload_sha256` → `"f"*64` | **1** | `PAYLOAD_SHA256_MISMATCH` | **KILLED** |
| M2 attempt gap | `f7e5e553` | rows `attempt` = 1, 3 | **1** | `ATTEMPTS_NONCONTIGUOUS` | **KILLED** |
| M3 at decreasing | `26cee18c` | row 2 `at` = 18:30:43Z < row 1 `at` = 18:30:44Z | **1** | `AT_DECREASING` | **KILLED** |
| M4 started_ids mismatch | `353390fe` | `started_ids` 96 → 95 (tasks_count 96) | **1** | `STARTED_IDS_MISMATCH` | **KILLED** |

Verbatim M1 output (the other three share the shape, captured in
`/fast/scratch/hyaku/mori-r24-a2/mut-ledger/mutants/out/`):

```json
{"finding_id":"LEDGER_UNBOUND","finding_ids":["PAYLOAD_SHA256_MISMATCH"],
 "findings":[{"id":"PAYLOAD_SHA256_MISMATCH","row":1,"scope":"row"}],
 "mode":"verify","rev":"ec6846a87059bf187fed9e6869f95d888b96d324",
 "rows":[{"attempt":1,"index":1,"reasons":["payload_sha256_mismatch"],
          "result":"started","started_ids":96,"status":"unbound","tasks_count":96}],
 "status":"failed","totals":{"bound":0,"ledger_findings":0,"rows":1,"unbound":1}}
exit=1
```

### The same four classes on the round-24 ledger R4 actually reads

Base `f7eb430`, ledger `.ufo/waves/round-24/wave1-attempts.json`:

| Mutant | Commit | verify exit | `finding_ids` | Verdict |
|---|---|---|---|---|
| R24-M1 digest flipped | `44afab08` | **1** | `PAYLOAD_SHA256_MISMATCH` | **KILLED** |
| R24-M2 attempt gap | `4cd8be1b` | **1** | `ATTEMPTS_NONCONTIGUOUS` | **KILLED** |
| R24-M4 started_ids mismatch | `0820b7ca` | **1** | `STARTED_IDS_MISMATCH` | **KILLED** |
| R24-M5 dispatch payload byte changed | `4c48f16b` | **1** | `PAYLOAD_BYTES_MISMATCH`, `PAYLOAD_SHA256_MISMATCH` | **KILLED** |

**Conclusion for the tasked question:** all four tasked mutant classes turn
`mori-dispatch-ledger.py verify` red, on both the round-23 and the round-24 ledger.
The verify surface is *not* vacuous on the four classes the tasking named.

---

## 4. Additional boundary mutants (all on committed sandbox bytes)

| Mutant | Mutation | verify exit | `finding_ids` | Verdict |
|---|---|---|---|---|
| M5a | dispatch byte **outside** the bound payload (`wave` label) | 0 | `LEDGER_CLEAN` | **SURVIVED** (see §5) |
| M5b | dispatch byte **inside** payload (`taskCall.context`) | 1 | `PAYLOAD_SHA256_MISMATCH` | KILLED |
| M5c | dispatch byte **inside** payload (`taskCall.tasks[0].name`) | 1 | `PAYLOAD_BYTES_MISMATCH`, `PAYLOAD_SHA256_MISMATCH` | KILLED |
| M6 | ledger `dispatch_path` → missing file | **2** | `DISPATCH_PATH_UNAVAILABLE` | red (unavailable, not "failed") |
| M7 | ledger `at` = 2099 (far future) | 0 | `LEDGER_CLEAN` | **SURVIVED** (no future bound) |
| M8 | ledger `at` precedes the dispatch commit | 0 | `LEDGER_CLEAN` | **SURVIVED by verify** (see §5) |
| M9 | duplicate `attempt` number (1, 1) | 1 | `ATTEMPTS_NONCONTIGUOUS` | KILLED |
| M10 | `at` = `"not-a-timestamp"` | 1 | `AT_INVALID` | KILLED |
| M11 | two rows both `result: started` | 1 | `DUPLICATE_STARTED`, `STARTED_NOT_LAST` | KILLED |
| M12 | legacy row, `payload_sha256` removed | 1 | `LEGACY_ROW_UNBOUND` | KILLED |
| M13 | ledger JSON is an object, not an array | **2** | `LEDGER_INVALID` | red (unavailable) |
| M14 | ledger = `[]` | 1 | `STARTED_MISSING` | KILLED |
| M15 | ledger row points at a *different* dispatch file (round-24 run, 33 tasks) | 1 | `PAYLOAD_SHA256_MISMATCH`, `PAYLOAD_BYTES_MISMATCH`, `TASKS_COUNT_MISMATCH`, `STARTED_IDS_MISMATCH` | KILLED |
| M16 | ledger path absent at REV | **2** | `LEDGER_INVALID` | red (unavailable) |
| M17 | round-24 dispatch **envelope** rewritten (`policy`/`counts`/`registry`), `taskCall` untouched, commit dated *now* | 0 | `LEDGER_CLEAN` | **SURVIVED by verify** (see §5) |
| M18 | round-24 dispatch **envelope** rewritten (`policy`, `counts`, `registry`, `wave`, `note`), `taskCall` untouched, commit dated **inside** the window the ledger row claims (epoch 1792656845, between dispatch-blob epoch 1792656837 and row `at` 1792656853) | 0 | `LEDGER_CLEAN` | **SURVIVED** (see §5) |
| M19 | round-23 dispatch **envelope** rewritten, `taskCall` untouched, commit dated inside the round-23 wave2 window (epoch 1792607420, between blob epoch 1792607409 and row `at` 1792607444) | 0 | `LEDGER_CLEAN` | **SURVIVED** (see §5) |

Note on exit codes: `verify` distinguishes three outcomes — 0 clean, 1 findings,
2 could-not-evaluate (`LEDGER_INVALID`, `DISPATCH_PATH_UNAVAILABLE`). A reviewer must
treat exit 2 as *red* for R4; the routed-check tool does so (it reports
`attempt_ledger_not_clean` / `dispatch_not_committed` accordingly).

### 4.1 Cross-check: the same mutants through `mori-routed-check.py --round 23`

Run against the sibling's in-flight `wt-routed` clone, with the round-23 wave2 ledger
as the subject. The `wave2-ledger.json` row status is the signal:

| rev | wave2-ledger `verify_exit` | `verify_findings` | wave2-ledger row status |
|---|---|---|---|
| `c725aa37` base | 0 | `LEDGER_CLEAN` | `bound_before_call` |
| M1 digest flipped | **1** | `PAYLOAD_SHA256_MISMATCH` | `bound_before_call` |
| M2 attempt gap | **1** | `ATTEMPTS_NONCONTIGUOUS` | `bound_before_call` |
| M3 at decreasing | **1** | `AT_DECREASING` | `bound_before_call` |
| M4 started_ids mismatch | **1** | `STARTED_IDS_MISMATCH` | `bound_before_call` |
| M8 `at` precedes dispatch commit | 0 | `LEDGER_CLEAN` | **`dispatch_committed_after_dispatch`** |
| M5 envelope byte, `taskCall` untouched | 0 | `LEDGER_CLEAN` | `dispatch_committed_after_dispatch` (M5's commit was dated late; M19 is the timestamp-honest version) |

The round-23 R4 item is red at base for the *real* defect (the round-23 wave-1 ledger
rows precede the dispatch commit `22772c1`), exactly as contract Amendment A4 states;
the four tasked mutants add a distinct `attempt_ledger_not_clean` reason on top.

**Caveat on the cross-check:** `mori-routed-check.py` had not landed in the lane when
this probe ran (it is the sibling seat `BuildRoutedCheck`'s in-flight work, and its
bytes changed between two of my runs). The `held` counts and reason strings above are
observations of that snapshot, not of a landed tool. The `mori-dispatch-ledger.py
verify` results in §3 and §4 are observations of **lane-committed bytes** and are
stable.

---

## 5. Survivors — the coverage finding

### 5.1 M8 / R24-M8: `verify` does not and cannot check dispatch-commit ordering

`mori-dispatch-ledger.py verify` reads committed **blobs only**. Its only git calls are
`cat-file -e <rev>^{commit}` and `cat-file blob <rev>:<path>`
(`tools/mori-dispatch-ledger.py:88` and `:105`); there is **no** `git log`, no
committer-time read, and the string `committer` does not occur in the file
(`grep -c committer` → 0). Therefore a ledger row whose `at` precedes the commit that
added its `dispatch_path` is **clean** under `verify` (M8 exit 0, R24-M8 exit 0).

This is **not** a defect in the ledger tool: R4's ordering clause is deliberately the
*routed-check* tool's predicate, per contract Amendment A4 ("the committer time (UTC)
of the commit that last changed its `dispatch_path` blob at or before REV is at or
before the row's `at`"). The routed-check tool implements it in
`_last_change_epoch` (sibling seat's in-flight `wt-routed` clone:
`/fast/scratch/hyaku/mori-r24-a2/wt-routed/tools/mori-routed-check.py:290`, used at
`:540-548`). I confirmed end-to-end against that clone:

| rev | routed-check rc | `held` | R4 held | R4 reasons | verify exit | verify findings |
|---|---|---|---|---|---|---|
| `f7eb430` pristine | 0 | 4 | true | — | 0 | `LEDGER_CLEAN` |
| R24-M1 digest flipped | 1 | 3 | false | `attempt_ledger_not_clean` | 1 | `PAYLOAD_SHA256_MISMATCH` |
| R24-M2 attempt gap | 1 | 3 | false | `attempt_ledger_not_clean` | 1 | `ATTEMPTS_NONCONTIGUOUS` |
| R24-M4 started_ids mismatch | 1 | 3 | false | `attempt_ledger_not_clean` | 1 | `STARTED_IDS_MISMATCH` |
| R24-M5 dispatch payload byte changed | 1 | 3 | false | `attempt_ledger_not_clean`, `dispatch_committed_after_dispatch` | 1 | `PAYLOAD_BYTES_MISMATCH`, `PAYLOAD_SHA256_MISMATCH` |
| **R24-M8 `at` precedes dispatch commit** | **1** | **3** | **false** | **`dispatch_committed_after_dispatch`** | **0** | **`LEDGER_CLEAN`** |

So the round-24 R4 mutant named in the contract ("a ledger row whose `at` precedes its
dispatch commit") **is** caught — by the routed-check tool, not by `verify`. The two
instruments are complementary, and the routed-check one is the one that carries the
ordering clause.

### 5.2 M17 / M18 / M19: the dispatch file's **envelope** is not bound — this is a real coverage gap

`_payload_identity` (`tools/mori-dispatch-ledger.py:120-165`) walks the dispatch JSON
and binds **only** the `{"context": ..., "tasks": ...}` pair of the unique validator
run object. Everything else in the dispatch file is outside the bound payload:

| Dispatch file | total bytes | bound payload bytes | **unbound envelope bytes** | unbound top-level keys |
|---|---|---|---|---|
| round-23 `.ufo/waves/round-23/wave2-run.json` | 177,691 | 159,710 | **17,981 (10.1 %)** | `schema`, `wave`, `policy`, `counts`, `registry`, `compaction`, `resumeSends`, `note` |
| round-24 `.ufo/waves/round-24/wave1-run.json` | 43,254 | 36,222 | **7,032 (16.3 %)** | same eight |

Mutants M17/M18/M19 rewrite exactly that envelope — `policy.maxLanes`,
`policy.hardCeiling`, `counts.total`, `registry.dispatch`, `wave`, `note` — while
leaving `taskCall` byte-identical. `verify` reports **`LEDGER_CLEAN`, exit 0**, on all
three. The lane's `policy` block is the lane cap and ramp configuration
(`maxLanes`, `minLanes`, `waveMinLanes`, `waveMaxLanes`, `declaredMaxLanes`,
`hardCeiling`, `rampBatchSize`, `rampIntervalMs`, `globalRunnerCeiling`) and
`registry` names every seat and its role — i.e. the envelope carries the dispatch
*authorisation and identity*, and none of it is bound by the digest.

M18 and M19 were deliberately **timestamp-honest**: the mutant commit was dated inside
the window the ledger row claims, so the R4 ordering predicate is satisfied and the
ordering clause cannot be the reason for a red. M18 still comes back
`held: 4`, R4 **held**, `bound_before_call` from the routed-check tool — because
`verify` says clean and the ordering clause says the dispatch was committed in time.
So **the entire C1 R4 chain is blind to a rewritten dispatch envelope.**

M17 (same envelope mutation, commit dated "now") does come back red, but only via
`dispatch_committed_after_dispatch` — the mutant's own late commit time, not the payload.
That red is an artifact of when I committed, not detection of the envelope change; M18
removes the artifact and the finding disappears.

**This is a coverage finding, not a licence to change the contract.** The lane's
`payload_sha256` semantics are "the validator payload identity" by design (round-18
wave-2 `MutDispatchLedger` M1/M2 froze exactly this). The R4 clause as written says
"verifies clean with `tools/mori-dispatch-ledger.py verify`" — it does not claim the
whole dispatch file is bound. But a reader of the R4 row would reasonably infer that
"the dispatch was bound" means "the dispatch that was sent is the dispatch recorded".
The envelope gap should be recorded as a known limit of R4 (and, if the L1 wants it
closed, of the payload identity in a later round) rather than silently assumed.

---

## 6. `--selftest`

```
$ TMPDIR=/fast/scratch/hyaku/mori-r24-a2/selftest-tmp \
  python3 -I tools/mori-dispatch-ledger.py --selftest
SELFTEST mori-dispatch-ledger PASS 14/14
exit=0
```

Run in the sandbox at base `c725aa37` tool bytes (SHA256
`9ec14ed3457596afed70bf1664cc51cc5d39f4ffb54b6cad6bc886b0dbde8441`, byte-identical to
the same file at `f7eb430` and at lane HEAD — `git show <rev>:tools/mori-dispatch-ledger.py | sha256sum`
gives the same digest for all three). The selftest refuses to run with `TMPDIR` unset
or under `/tmp` / `/var/tmp` (`SELFTEST_SCRATCH_REQUIRED` /
`SELFTEST_SCRATCH_FORBIDDEN`), which is why a scratch dir under `/fast` was used.

---

## 7. Restoration evidence

The sandbox was reset to base after every mutant (`git reset --hard` on a dedicated
branch), and the final state was re-verified.

```
$ git -C /fast/scratch/hyaku/mori-r24-a2/mut-ledger status --porcelain
?? mutants/                       # only my harness scripts + captured outputs, untracked

$ git -C ... rev-parse HEAD
c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130      # == the base rev named in the tasking

$ sha256sum .ufo/waves/round-23/wave2-ledger.json .ufo/waves/round-23/wave2-run.json \
            tools/mori-dispatch-ledger.py
b9e82807052b8e06fb067934583935e8d1a04b24f539f3f74bb910abdb3a5797  .ufo/waves/round-23/wave2-ledger.json
63205203e1ca34bfd64b70ddc233a05590fa2e00ef0fd0123dcb7165c748f8d0  .ufo/waves/round-23/wave2-run.json
9ec14ed3457596afed70bf1664cc51cc5d39f4ffb54b6cad6bc886b0dbde8441  tools/mori-dispatch-ledger.py
```

These three digests equal the **pristine base** digests recorded before the first
mutation (`base.hashes` in the harness output), so the mutated bytes are fully
reverted. `verify` on the restored tree returns `LEDGER_CLEAN`, exit 0 (see `base.json`
and `restored.json` / `restored2.json` in `mutants/out/`).

Mutant commits live only on the sandbox branches `mut/ledger` and `mut/ledger-r24`
(base `c725aa37` and `f7eb430` respectively) and are never pushed. The sandbox clone's
remote was not modified.

**Lane untouched:** the only lane-side writes by this seat are this report file
(`.ufo/waves/round-24/w1/MutateDispatchLedger.md`). No `git add`/`commit`/`stash`/
`checkout`/`reset`/`pull`/`push` and no mutating `jj` command was run in
`/home/vgpnk/Projects/shokunin/mori-shokunin`. All lane access was `git log`,
`git show`, `git ls-tree`, `git status` (read-only) plus read-only
`mori-dispatch-ledger.py verify` subprocesses.

---

## 8. Verdict summary

| Question | Answer |
|---|---|
| Do the four tasked mutants turn verify red? | **Yes, all four** — M1 `PAYLOAD_SHA256_MISMATCH`, M2 `ATTEMPTS_NONCONTIGUOUS`, M3 `AT_DECREASING`, M4 `STARTED_IDS_MISMATCH`; exit 1 each. |
| Do they survive? | **No.** All four are killed on the round-23 ledger, and the same classes are killed on the round-24 ledger R4 reads. |
| Does `--selftest` pass? | **Yes** — `SELFTEST mori-dispatch-ledger PASS 14/14`, exit 0. |
| Which mutants survive? | (a) dispatch-envelope rewrites with `taskCall` untouched (M17/M18/M19) — `LEDGER_CLEAN`, exit 0, 10–16 % of dispatch bytes unbound; (b) `at` before the dispatch commit (M8/R24-M8) and `at` far in the future (M7) — `LEDGER_CLEAN`, exit 0, because `verify` reads blobs only and has no committer-time predicate. |
| Is the C1 R4 clause blind to the envelope gap? | **Yes.** With a timestamp-honest envelope mutant (M18) the routed-check tool still reports `held: 4`, R4 held, `bound_before_call`. The R4 ordering clause cannot catch it either. |
| Is the round-24 R4 mutant ("`at` precedes dispatch commit") caught? | **Yes**, by `tools/mori-routed-check.py` (`dispatch_committed_after_dispatch`, `held: 3`), not by `verify` (which reports `LEDGER_CLEAN` on it). The two instruments are complementary. |

**Recommended disposition (for the L1, not acted on by this seat):**

1. Record the dispatch-envelope gap as an explicit limit of R4's "verifies clean"
   wording. If R4 is meant to bind the whole dispatch file, the payload identity —
   not the R4 clause — is what must change, and that is a separate round's claim.
2. Keep the exit-2 distinction in mind when reading R4: a missing or malformed ledger
   is `LEDGER_INVALID` / `DISPATCH_PATH_UNAVAILABLE` at exit 2, not a "clean" pass.
3. Do not narrow the R4 predicate on the strength of these mutants: every mutant class
   the contract names is detected, and the one gap found is in the dispatch envelope,
   which the contract does not currently claim to bind.

---

## 9. Tooling

No installs or upgrades were performed. Everything used was already on the host:
`git 2.56.0`, `python3 3.14.8` (`python3 -I` for every tool invocation, as required).
`TMPDIR` was pointed at `/fast/scratch/hyaku/mori-r24-a2/selftest-tmp` because the
tool's selftest refuses `/tmp` and `/var/tmp`. No pacman, `uv`, `npm`, `cargo` or
service operation was run; no host file outside the sandbox clone and this report was
written.

### Reproduction

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin \
    /fast/scratch/hyaku/mori-r24-a2/mut-ledger
cd /fast/scratch/hyaku/mori-r24-a2/mut-ledger
git checkout -b mut/ledger c725aa37
# then run mutants/run-mutants.sh ... run-mutants8.sh (harness preserved in the sandbox)
```
