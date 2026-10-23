# mori round 36 — wave 2 — RevNgC2: reverse-engineer and attack `count-c2.py`

Seat: revenger, leaf member (no subagents). Date 2026-10-23. Lane tip under test
`bf0df77fee4b6ef54a90aea09335c7617f125151` (receipt rev), round base `f10a320d`.
Attacked surface: `.ufo/waves/round-36/count-c2.py` (the frozen C2 counter) and the soundness of
the measurement behind `evidence/c2-after.txt` (C2=met). What my item attacks: (1) truth/op-log
isolation between counter and `--tool`, (2) the harness-key surface (paths, env, argv) and the v2
real-arm re-design's claim to defeat it, (3) the frozen control J11's v2 verdict, (4) real-arm
memoization spoofability (novel bypass).

Bounds kept: lane repo read-only (no git/jj mutations, no lane file edited); exactly one file
written (this report); all scratch under `/fast/scratch/hyaku/mori-r36/RevNgC2/`. No tool
installs were needed (python3 + git only; nothing added to the toolchain).

## 0. Identity and freeze integrity of the attacked bytes

| check | command | observed |
|---|---|---|
| counter sha256 | `sha256sum .ufo/waves/round-36/count-c2.py` | `c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34` — equals the freeze-v2 pin (`evidence/freeze-v2.txt`) |
| counter blob pin | `git hash-object .ufo/waves/round-36/count-c2.py` | `d8c41d96616eb7caed5ad12cf4e8a2b93c2237dc` — equals the freeze-v3 blob pin (`evidence/freeze-v3.txt`) |
| control bytes | `sha256sum .ufo/waves/round-36/c0/controls/J11.py` | `ede4cfdcf9d5f2d4aae5bc35fbe7996914069fb6f2da0e6355aa55560f13a3b5` — equals the pin recorded at `evidence/c0-rescore-v2.txt:176` |
| scored tool bytes | `git diff bf0df77fee4b… -- tools/mori-sources-appendonly.py` | empty — the working-tree C2 tool is byte-identical to the receipted rev |

Observation (bookkeeping, not a counter defect): current `contract.md` hash-object is
`f505594b…`, not the `f68a06c2…` pinned inside `evidence/freeze-v3.txt` minutes earlier. The blob
is reachable; `git diff f68a06c2… -- .ufo/waves/round-36/contract.md` shows exactly one change:
the r32–r35 history-correction paragraph that freeze-v3 itself describes as "recorded outside the
frozen predicate bytes". P-C2 appears exactly once in both versions with identical bytes
(current file :24); counter bytes verified unchanged by two independent pin formats. Freeze of
the counters holds.

## 1. Is the sandbox op log or truth ever written where the `--tool` program can read it?

**No — source level.** The counter's complete disk-write inventory (`grep -n 'open(\|makedirs\|mkdtemp\|\.write(\|rmtree\|NamedTemporary\|mkstemp' count-c2.py`):

- `count-c2.py:368-369` — `Sandbox.commit()` writes `corpus/SOURCES.md` into the sandbox repo. This is the history content itself, i.e. exactly the input the tool is supposed to read.
- `count-c2.py:380` — `os.makedirs(<sandbox>/corpus)`.
- `count-c2.py:670` — `tempfile.mkdtemp(prefix="mori-c2-")` under `$TMPDIR`; `count-c2.py:685-686` — writes the extracted tool into it (only on the scored, no-`--tool` path; holds the tool, never truth).
- `count-c2.py:690` — `os.makedirs(scratch)`; `count-c2.py:718,720` — `shutil.rmtree` cleanup.

Nothing else is written. The op log lives in `Sandbox.rows/states/first/protected` and the truth
in the `truth_from_states` dict — process memory only; `format_summary` is called solely at
compare/print time. Module docstring (:12-16): the truth "comes from the counter's own op log …
never from git and never from a file the tool can read" — verified true of the bytes.

**No — runtime level.** I ran the counter with an instrumented delegate tool
(`--tool /fast/scratch/hyaku/mori-r36/RevNgC2/instrument.py`, seed `1234567890123456789`): each
invocation logs its argv/cwd/env/parent-chain, inventories the repo it was handed, then scans the
run's scratch tree for any loose file containing `appendonly_violations=` (`.git/objects`
excluded — that is the legitimate history). Command and observed verdict (real arm failed for an
instrumentation-only reason, see disclosure below):

```
blind arm: 24/24 sandbox histories matched the hidden truth (40.1s; coverage: deletions=22 changed-back=18 superseded=7)
real arm: FAIL (120.7s) … tool exit=124      # my scanner's own cost, see disclosure
C2=unmet
```

The 24 blind-arm records (`surface-log.jsonl`) show, per invocation:
- non-git repo inventory = `corpus/SOURCES.md` + standard `.git` files only (HEAD, config, hooks samples, index, logs, objects, refs, COMMIT_EDITMSG, plus a rerere `MERGE_RR` side file the host git config creates — no truth content);
- truth-hit scan: **0 hits in 24/24 invocations** while the blind arm passed 24/24 — the truth existed in counter memory at that moment and nowhere on disk;
- `cwd` = `/` in every invocation (`run_tool`, `count-c2.py:493`); env byte-identical across all invocations (`clean_env`, :62-67, strips only the six `GIT_*` repo vars);
- parent chain: `timeout 120 <python> <tool> …` → `python3 .ufo/waves/round-36/count-c2.py bf0df77…`.

**Memory channel:** the only place truth exists outside git is the counter's heap. A child-tool
probe reading the counter ancestor's `/proc/<pid>/mem` heap regions got `PermissionError(13)`
(`kernel.yama.ptrace_scope = 1` on this host; the tool is a descendant, not an ancestor, so
attach is denied). The truth is not child-readable — but note this protection is host policy,
not counter design (residual note for r37 if the counter is ever run under yama 0).

**The one truth-adjacent datum the tool legitimately receives:** `--round-base <sha>` on argv
(blind `count-c2.py:601`, real :629) — part of the frozen C2 tool interface (contract.md §C2),
required to compute `round_changed`.

**Disclosure (instrumentation scope slip, read-only):** my scanner computed the scan root as
`dirname(--repo)`; on the real arm that is the fleet root `/home/vgpnk/Projects/shokunin`, and
the walk exceeded the tool's 120 s `timeout` (:493 wraps every arm), so the real-arm record was
lost and that invocation scored FAIL. No writes outside my scratch; the lost record is replaced
by source-level evidence above. Correct design would have bounded the scan to the sandbox root.

Minor counter quirk found while invoking it: `main()` validates `--tool` with
`os.path.isfile(tool)` (:674) relative to the counter's cwd, but the tool later executes with
child cwd `/` (:493). A relative `--tool` path passes the check then fails in every arm
(observed: `can't open file '//.ufo/waves/round-36/c0/controls/J11.py'`, 24× exit 2,
`C2=unmet`). Scored runs never pass `--tool`; C0 always used absolute paths
(`c0-rescore-v2.txt:178`). Cosmetic.

## 2. Harness keys (paths under /fast/scratch or /tmp, env, argv) — and does the v2 real arm defeat them?

Full arm-distinguishing surface, reconstructed from source + runtime records:

| key | blind arm | real arm | line | usable to memoize the real arm? |
|---|---|---|---|---|
| repo path | `<SCRATCH_ROOT>/c2-%08x/repoNN` (:42, :690) | lane repo abs path (:628-629) | detected by J11 (:70) | v2 **defeats scratch-path keys**: the real arm runs on the repository itself, no clone (:626-629 comment "no clone") |
| argv rev literal | `HEAD` (:601) | `6bd57097` (:629) | — | yes — rev string distinguishes arms |
| local git config `user.name` | `"mori counter"` planted in every sandbox (:382) | lane identity (`mori-shokunin`) | — | **yes — exploited below (N1)** |
| SOURCES.md title | `"# SOURCES - sandbox registry"` (:257) | lane title | — | yes (blind-side detector) |
| parent/grandparent cmdline | `timeout 120 …` → `count-c2.py …` (runtime-observed) | same | — | yes, but only detects; gains nothing in the blind arm |
| env | identical both arms (:62-67) | identical | — | no |
| cwd | `/` both arms (:493, calls :601/:629) | `/` | — | no |
| tool file location | same file both arms with `--tool`; on the scored path extracted once (:670-686) and reused | same | — | no |

**Answer:** the v2 re-design does what its comment (:625-628) claims only for *path* keys — J11
cannot see the real arm as "under /fast/scratch or /tmp" anymore (J11.py:70-72 fires EMPTY;
confirmed by re-run, §3). It does **not** eliminate arm detection: any of the surviving keys
lets a tool behave differently per arm. Detection alone is harmless in the blind arm (truth is
random, in memory, unreachable — §1), so the only exploitable direction is **real-arm
memoization**: a tool that computes honestly on the 24 random sandboxes and prints a precomputed
constant on the fixed real input. The precomputed constant is publicly available — the receipt
`evidence/c2-after.txt` itself prints the oracle line, and `REAL_REV`/`REAL_BASE` are frozen
constants (:44-45). Demonstrated in §4.

## 3. Control J11 re-run under v2 — confirmed unmet

Command (absolute `--tool` path; seed = the receipt seed for replayability):

```
python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 \
  --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J11.py \
  --seed 15440749816798970567
```

Observed (full output kept at `scratch/j11-v2-abs.out`):

```
blind arm: 24/24 sandbox histories matched the hidden truth (1.9s; coverage: deletions=22 changed-back=17 superseded=10)
real arm: FAIL (0.2s)
  tool:   appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=[…18…] got=[] ; superseded: want=[…] got=[] ; round_changed: want=[…] got=[] ; violations: want=18 got=0
  tool exit=0
C2=unmet
seed=15440749816798970567
exit=1
```

Mechanism: J11's gate (`J11.py:69-72`) prints the empty summary for any repo not under
`/fast/scratch` or `/tmp`; under v2 the real arm is the lane repo, so the gate fires exactly
there, while the blind arm (under the scratch root) gets the real rules and passes 24/24. This
reproduces `evidence/c0-rescore-v2.txt:176-190` byte-for-byte in structure (same four diffs,
same exit semantics), on the receipt seed. J11 is genuinely unmet under v2; the path-key control
does not pass.

## 4. Novel bypass attempt: real-arm memoization keyed on the sandbox git identity

**N1** (`scratch/n1-memo.py`): gate on `git config --local user.name == "mori counter"` — the
identity `build_sandbox` plants in every sandbox repo (`count-c2.py:382`) and the lane repo does
not have. Blind arm → delegate to the honest lane tool `tools/mori-sources-appendonly.py`
(read-only run of the lane's own tool, permitted). Real arm → print a precomputed constant,
never reading any history. The constant is my **independently recomputed** oracle output
(`scratch/oracle-r36.py`, written from the contract's definitions only, no counter code reused):
`appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]`
— which exactly equals the oracle line in `evidence/c2-after.txt`, confirming the receipt's
real-arm expectation is truthful (18 ≥ 1 id, predicate satisfied).

Command: `python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b… --tool …/n1-memo.py --seed 9876543210987654321`

```
blind arm: 24/24 sandbox histories matched the hidden truth (2.1s; coverage: deletions=22 changed-back=17 superseded=8)
real arm: pass (0.2s)
  tool:   appendonly_violations=18 ids=[S041,…,S193] …  (identical to oracle)
  oracle: appendonly_violations=18 ids=[S041,…,S193] …
C2=met
seed=9876543210987654321
exit=0
```

**The counter's response: `C2=met`, exit 0, for a tool that never computed the real-arm
answer.** The blind arm's 24/24 pass with the gate active proves the identity marker is present
in all 24 sandboxes and that the honest delegation passed; the real-arm pass proves the constant
is indistinguishable from computation to `real_arm` (:624-633), which checks output lists only.

**Isolation (N2, `scratch/n2-const.py`):** the same constant printed unconditionally, seed
`1111111111111111111` → `blind arm: 0/24` (24× "lists differ"), real arm pass, `C2=unmet`,
exit 1. So the blind arm is the only discriminating arm; against a memoizing tool the real arm
adds zero discrimination.

**Severity (bounded):** this does **not** invalidate `evidence/c2-after.txt` — that receipt
scored the honest lane tool extracted from rev `bf0df77` via `git show` (:680-686), whose bytes
are unchanged since the tip (§0) and whose real-arm line I reproduced independently. What N1
falsifies is the *discrimination claim* of the real arm: a `C2=met` verdict does not imply the
real-arm answer was computed rather than recalled. The limit is inherent to the frozen design —
the contract itself declares the real arm "a real-input arm on the lane's own bytes with a known
witness", and the witness is published in the receipt — and cannot be closed without a predicate
change (e.g. scoring an unannounced rev), which is outside this seat's authority. Frozen-control
family coverage: all 25 C0 controls unmet under v2 (`c0-rescore-v2.txt`); N1 is outside that
frozen table and is a post-data finding, recorded here for the r37 debt list rather than as a
receipt-breaking defect. The load-bearing evidence of C2 — 24 random in-memory-truth blind
histories — survives every attack I could construct: constants fail (N2), leaks do not exist
(§1), memory is unreachable (§1), and only honest computation passes the blind arm.

## Summary of residuals (detection/report only, per mori province)

1. Real-arm memoization spoofability via surviving arm-detection keys (demonstrated, `C2=met`;
   receipt unaffected) — candidate r37 counter note, requires predicate change to close.
2. Truth-in-memory protection rests on host yama policy (ptrace_scope=1), not on the counter.
3. `--tool` relative-path inconsistency (:674 isfile vs :493 cwd `/`) — cosmetic, controls only.
4. `evidence/freeze-v3.txt`'s `contract.md` blob pin was stale within minutes of writing (the
   disclosed history-correction prose landed after the pin); counter pins unaffected (§0).
5. Blind sandbox `MERGE_RR` side files are created by the host git config's rerere; no truth
   content, no effect on scoring (observed in repo inventories).

## VERDICT

VERDICT: PASS — no defect found in the frozen `count-c2.py` w.r.t. its predicate P-C2 or its
freeze: truth/op-log never written where the tool reads (source + 24/24 runtime scans), J11
re-confirmed unmet under v2 on the receipt seed, path-key defeat by the v2 real arm confirmed,
and the landed receipt's real-arm oracle independently reproduced. The novel bypass (N1,
`C2=met` from a memoizing tool) is recorded as a bounded residual of the declared
known-witness design, not a defect in the counter's measured claim.
