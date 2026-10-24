# w1/SimpC1 — dead-weight audit of `.ufo/waves/round-37/count-c1.py`

Seat: mori round 37, wave 1, simplifier (C1 side). Read-only on the lane; plan only, no edits.
Target: deletable weight in the C1 counter that does not change P-C1.

## Axes

1. **Dead weight** (lines provably removable).
2. **P-C1 preservation** (predicate text and enforcement identical).
3. **Freeze-pin integrity** (the counter is byte-pinned; application cost).
4. **Evidence-format stability** (receipt-embedded output text).

## Anchor and method

- Audited bytes = the **pinned** counter: freeze-r37.txt pins blob `7518fef8f54afff69ee38a99f2acbf518006f5ad`, sha256 `86699627c7627cc3eea3ba9ea952079d081db390f9ba2be1e1d4d685dd98cdae`; working tree matched the pin at audit start (measured `sha256sum`).
- **lsp device unavailable in this session** (`read xd://lsp` → `No such tool: xd://lsp. Mounted devices: ast_edit, debug.`). Recorded per protocol; literal fallback used, never presented as semantic proof:
  - whole-module AST name resolution (sound here: `getattr|__import__|import_module|exec(|eval(` → **zero matches** in v1 and v2);
  - repo-wide grep for importers of `count[-_]c1`: all matches are historical round-17/26 receipts; nothing imports the round-37 script (hyphenated filename is not importable), and the plan leaves the CLI surface (`rev`, `--repo/--tool/--negatives/--seed`, exit 0/1/2) untouched.
- **Behavioral A/B on a scratch copy** (allowed scope `/fast/scratch/hyaku/mori-r37/SimpC1/`): applied all eight deletions to a copy, ran original and mutant on the scored tip:

  ```
  python3 <counter> e57c58b57c025364e79d130fbdf764d2674d83d6 --seed 7
  ```

  Both exit 0, `C1=met`: blind 24/24 (coverage deletions=22 changed-back=15 superseded=10), real pass, challenge pass, negatives `memo-n1`/`const`/`summary-only` rejected with byte-identical reasons. The **only** output difference is the `tool: /tmp/mori-c1-tool-<nonce>` mkdtemp line. Control: two runs of the *unmodified* original differ by exactly that same single line — the residual is the counter's own mandated nondeterminism (r36 debt g), not the mutation.

## Ranked deletion plan (line numbers: pinned v1 blob; v2 working tree in parentheses)

| # | Deletion | Lines (v1 pin) | Proof of deadness | P-C1 preservation |
|---|----------|----------------|-------------------|-------------------|
| 1 | **Dead return value `flags`** from `build_sandbox` | 417 (docstring), 525–527, unpacks 671 and 767 (v2: 418, 526–528, 672, 815) | `flags` has zero readers anywhere: 4 Name refs are one store, one return, two unpacks; no `flags[`/`flags.get`/`['flags']` in the module. Coverage gate reads `truth["changed_back"]`, not flags | No rng consumption change; A/B identical |
| 2 | **Vestigial `scratch` parameter of `real_arm`** | 724; callers 798, 911 (v2: 725, ~799, ~972) | Body never reads it (AST: `scratch` absent from `real_arm` body names). The v2 comment at 725–727 documents why: v1 cloned into scratch, v2 "read-only git only; no clone". Both call sites pass dead values (`scratch`, `None`) | Parameter carried no behavior; A/B identical |
| 3 | **One-caller wrapper `blind_arm`** | 720–721; sole caller 895 (v2: 721–722, ~896) | `return check_blind(tool, draw_blind(root, rng))`, called once; inline the composition | Same composition, same rng order; A/B identical |
| 4 | **Unreachable disjunct `cells is None`** in `op_delete` | 380 (v2: 381) | `cells = target if target is not None else self.rng.choice(self.rows)`: target=None ⇒ a row from `self.rows`; rows ≥ 3 at every delete (the same guard returns when `len ≤ 2`; initial draw ≥ 6 rows; nothing else removes rows) ⇒ `cells` is never `None` | Removes an unreachable branch; A/B identical |
| 5 | **Dead attribute `self.index`** | 310 (v2: 311) | Sole occurrence is the store; every other index use is the local parameter (e.g. path building at 313) | A/B identical |
| 6 | **Never-overridden `cwd` parameter of `run_tool`** | 532, 535 (v2: 533, 536) | All three callers (check_blind, real_arm, challenge_arm) pass 2 args; the `"/"` value is load-bearing, keep it as a literal at the `run(...)` call | A/B identical |
| 7 | **Never-overridden `timeout` parameter of `git`** | 118–119 (v2: 119–120) | No `git(...)` callsite passes `timeout=` anywhere in the module (the one regex hit is the def itself); always 120 — inline the literal | A/B identical |
| 8 | **Never-exercised default `title=SANDBOX_TITLE` on `render`** | 292 (v2: 293) | Only callsite is `Sandbox.commit`: `render(self.rows, self.title)`; the live default lives on `Sandbox.__init__` | A/B identical (second mutant run, exit 0, `C1=met`) |

Net: −26/+18 vs the pinned bytes (960 → 953 lines, 7 net; 8 net with #8). Diff retained at `/fast/scratch/hyaku/mori-r37/SimpC1/` with both run transcripts (`origA/B-seed7.txt`, `mut-seed7.txt`, `mut2-seed7.txt`).

## Considered and rejected (argument-checked)

- **Merge `truth_from_states` with `oracle`** (~60 duplicated walk lines). The duplication is the design: blind truth comes from the op log, real truth from an independent git walk. One shared walk would let a single bug corroborate itself across arms — weakening exactly the discrimination P-C1 measures. Keep.
- **Tool exit-code equality checks** (v1 691, 708–711, 774, 786–788). Not in P-C1's text — but these are *additive strictness* on a real interface dimension (the honest tool exits 1 on round_changed, visible in receipts as `tool exit=1`). Deleting a check weakens the gate; not weight.
- **`malformed` counter** in `parse_id_lines`/`same_id_lines`. Enforces P-C1's "exactly the truth's per-id lines" against near-miss `changed`/`deleted`-looking lines. Keep.
- **`_scratch_parent`, `display_path`, SIGTERM→SIGKILL grace, `clean_env` GIT_\* pops.** Each implements a named contract requirement (r36 debts g and e, debt f, environment-attack hardening). Keep.
- **Defensive branches**: `immutable_indices` None-fallback, `superseders` `(colmap or {})`, `op_edit_immutable` empty-candidates fallback, `if not full` in `main`. Each is reachable in principle (registry without a header, all rows protected, degenerate git output) and each preserves the exit-2-setup-error vs exit-1-unmet distinction the contract defines. Keep.
- **Three-arm compare duplication** (`check_blind`/`real_arm`/`challenge_arm` each re-implement timeout→no-summary→lists→per-id). The largest duplication, but the three shapes differ on purpose: `real_arm` reports *all* diffs plus the ≥1-id oracle requirement, `check_blind` accumulates per-repo reasons, `challenge_arm` returns first-fail. Merging flattens receipt-embedded evidence text (axis 4). **Note:** the in-flight v2 amendment adds a *fourth* copy (`real_draw_arm`) in the same class — same rejection argument applies, now with more force.

## Mid-audit drift (observed, not acted on)

While this audit ran, the working-tree counter moved: 960 → 1020 lines, sha256 `866996…` → `20a6c2f3…` — the v2 "amendment A1" (`w1/RevC1Challenge`): new `draw_real_rev`/`real_draw_arm` drawn-rev arm, real lane SOURCES title, widened PREDICATE. My A/B proof base was copied before the drift and the diff contained only my edit lines, so the behavioral proof is against the pinned v1 bytes. All eight candidates were re-verified dead on the v2 bytes (line numbers above); the plan applies to both versions. The v1-vestige `scratch` param (#2) persists into v2.

## Stop axis

freeze-r37.txt pins the counter **by bytes** (blob + sha256), and the contract states a post-freeze change "is a new counter version, not an edit." Every proposal here is predicate-shape-preserving and was proven behaviorally identical on a fixed seed, so a re-freeze would be mechanical — but applying any of this invalidates the current pin while a v2 amendment is already in flight, and that re-freeze decision belongs to L1, not this seat. Beyond the eight, the next deletion would harm either a discrimination check (exit codes, malformed, coverage) or the pin axis. Stopping here.

No tools installed or upgraded. Scratch artifacts: `/fast/scratch/hyaku/mori-r37/SimpC1/`. Lane untouched except this report; challenge-scratch left clean by the counter runs (verified empty).

VERDICT: PASS
