# Mo58Reviewer04 — C1 do-nothing probe (round 58, wave w1)

Date: 2026-10-27. Scope: run the frozen C1 counter at the entering revision, identify the
cheapest no-work state that could meet its target, and return an adversarial finding or an
explicit no-counterexample result. Read-only on the lane; no production, SCORECARD, LOG,
registry, or VCS writes; no subagents; no tool installs (system `python3`/`git` only).
Scratch: `/fast/scratch/hyaku/mori-r58/Mo58Reviewer04/` (TMPDIR set there; removed before
yield). Disk guard status before work: green (`/fast/scratch/hyaku` 33% use, 545.1G free).

## Baseline integrity (freeze hygiene)

- Working tree vs freeze `fe8801120a67c1a6b8899d7d0423839caa09e7d0`, sha256:
  - `contract.md`  `3aeff1d1…2e5223` IDENTICAL
  - `count-c1.py`  `6ecdb627…f84e4b` IDENTICAL
  - `count-c2.py`  `aab888ad…010d3` IDENTICAL
  No post-freeze byte change; C1 kill rule not triggered by drift.
- `git cat-file -e b783d0b8…:.ufo/waves/round-58/count-c1.py` → `fatal: … exists on disk,
  but not in 'b783d0b8…'`, exit 128 (before-control: counter absent at entering revision).
- Lane HEAD at probe time: `4272736cfc5147586e1543413772f80daf44b04b`.

## Seat deliverable — frozen counter at the entering revision

Exact command (run from the lane working tree; counter bytes sha-verified equal to freeze):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
TMPDIR=/fast/scratch/hyaku/mori-r58/Mo58Reviewer04/tmp \
  python3 .ufo/waves/round-58/count-c1.py b783d0b892637ce8d20f188cad20e4d8913ca635
```

Output, exit:

```
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=b783d0b892637ce8d20f188cad20e4d8913ca635
exit=0
```

Same command at the freeze revision `fe88011…` → `C1=met rows=2 pointers=ok manifest=ok
binding=ok failed=none rev=fe8801120a67c1a6b8899d7d0423839caa09e7d0`, exit 0.
`--selftest` → `C1_SELFTEST pass=4 fail=0`, exit 0.

Why it is met at the entering revision (all read at `b783d0b8…`):
- Active register: `## Capabilities` at `SCORECARD.md:1951`, binding sentence at `:1953`;
  both key rows at `:1989-1990`; superseded stub table at `:596-600` lacks the sentence and
  the `| key | capability |` header, so selection is correct.
- All four pointer targets resolve at that rev: `tools/mori-vote-bind.py`,
  `tools/mori-driver-liveness.py`, `.ufo/waves/round-56/evidence/c2-at-landed.txt`,
  `.ufo/waves/round-56/evidence/c1-at-landed.txt` (`git cat-file -e` → exit 0 each).
- Fleet `MANIFEST.json` `rounds[832].capabilities_added[0]` contains "vote binding", `[1]`
  contains "driver-liveness".

**Cheapest no-work state meeting the target:** `S* = (tree of b783d0b8…) ∪ {the counter
file at the freeze bytes}`. Every measured conjunct (binding, rows, pointers, manifest) is
already true at the entering revision — verified above — and `rev=R` in the target is
satisfied by `R = b783d0b8…` itself. S* differs from the entering revision by exactly one
added file; no SCORECARD edit, no evidence file, no MANIFEST change, no corpus change is
needed. At round 58 the counter re-verifies round-57 work (the rows landed pre-round;
`SCORECARD.md:2915` records them as the r57 C1 outcome); its only r58-discriminative
content is the existence of the counter file. This is consistent with the contract's
before-control (which tests only counter absence), so it is a calibration-power
observation, not a §9 invalidation — but it is what "do nothing" buys: the target is
reachable with zero verification work beyond landing the file.

## Findings by severity

**F1 — HIGH (contract-vs-counter mismatch, needs L1 ruling; no seat edit per kill rule).**
The frozen target output `C1=met rows=2 pointers=ok manifest=ok binding=ok selftest=ok
rev=R` is unsatisfiable as a literal: no code path in the frozen bytes emits the token
`selftest=ok`. `measure()` prints `… binding=ok failed=none rev=…` (empirically RUN1/RUN2
above); the only other output is `C1_SELFTEST pass=N fail=M` from `--selftest`, which also
lacks the token. If the round verifier exact-matches the frozen line, C1 can never score
met; if it token-matches, `selftest=ok` is a dead token and the unlisted `failed=none`
must be tolerated. Both the target sentence and the counter bytes are kill-frozen, so this
is resolvable only by L1 ruling (interpretation or documented verifier grammar).

**F2 — MEDIUM (do-nothing significance).** As delivered above: the counter is met at the
entering revision; the cheapest meeting state adds only the counter file. The C1 claim's
calibrated content at r58 is "a file exists", nothing more. Not a counter breakage; the
contract's before-control is satisfied exactly as written.

**F3 — LOW (stub-refusal inert against the lane's real marker form).** `STUB_MARK` is the
ASCII `-- none yet --`; the real superseded stub (`SCORECARD.md:596-600` at the entering
rev) uses em-dashes `— none yet —`. Counts at `b783d0b8…`: ASCII form 0×, em-dash form 2×.
Probe arm `emdashed_stub_in_active_body` (active-register body carrying the binding
sentence, `| key | capability |` header, 10 key rows, both good rows, plus an em-dash
`— none yet —` line) → `C1=met … exit 0`: the "refuses any section whose body contains the
stub marker" defense does not bind to the convention the lane actually uses. Mitigated on
real bytes because the stub section lacks the sentence and the required header; a
false-green needs a crafted section with all of sentence+header+10 key rows+good rows+an
em-dash none-yet line. As written the refusal predicate is dead weight.

**F4 — LOW (manifest arm is revision-independent).** `measure()` loads
`$FLEET/MANIFEST.json` from the live fleet working tree, not from rev R. The counter's
output is not a pure function of R: a fleet-side edit can flip met↔unmet with zero lane
commits. Cosmetic sibling defect: both hints missing yields the doubled token
`failed=manifest,manifest`.

**F5 — INFO (pointer filter coverage).** Only backticked tokens beginning `.ufo/`,
`tools/`, `corpus/` are `git cat-file -e`-resolved (after a `"/" not in path and no
.py/.txt/.md suffix` prefilter). Evidence pointers named outside those prefixes in the two
rows are never verified. Code-read finding; my live probe did not isolate it (the probe
row retained a `.ufo/` pointer and failed pointers for that reason).

**F6 — INFO (head-zone brittleness).** The binding sentence must appear within the first
12 body lines of the section; probe with it later → `binding=bad` rc=1. Conservative
direction (false-negative, not false-green); the real register has the sentence 2 lines
after its heading.

## §9 do-nothing controls — explicit no-counterexample result

Independent probe arms (frozen bytes imported as a module, `LANE`/`FLEET` patched to
throwaway fixtures under scratch TMPDIR; harness receipt embedded here, not filed
separately):

| arm | rc | output (abridged) | contracted? |
|---|---|---|---|
| ctl_a_bad_pointer (rows name nonexistent evidence path) | 1 | `C1=unmet rows=2 pointers=bad … failed=pointers` | yes — contract MUST `C1=unmet … failed=pointers` |
| ctl_b_stub_only (only table is the stub) | 1 | `C1=unmet rows=0 … binding=bad failed=binding` | yes — contract MUST `binding=bad` |
| conformant_minimal | 0 | `C1=met rows=2 … failed=none` | sanity pass |
| sentence_past_head_zone | 1 | `binding=bad` | predicted (F6) |
| stub_marker_in_active_body (ASCII) | 1 | `binding=bad` | predicted |
| duplicate_key_rows (3 key rows) | 1 | `rows=3 … failed=rows` | predicted |
| emdashed_stub_in_active_body | 0 | `C1=met … failed=none` | **finding F3** |
| manifest_hints_wrong | 1 | `manifest=bad failed=manifest,manifest` | predicted (F4 token) |
| manifest_file_missing | 1 | `manifest=bad failed=manifest` | predicted |
| nonexistent_revision | 1 | `C1=unmet reason=revision failed=rev` | clean, no traceback |
| evidence_files_absent | 1 | `pointers=bad failed=pointers×4` | predicted |
| nonprefixed_pointer_unchecked | 1 | `pointers=bad` (via retained `.ufo/` path) | F5 not isolated live |

Verdict: **no §9 counterexample.** Both contracted do-nothing controls score unmet with
the required tokens and exit 1; the frozen selftest is `pass=4 fail=0`; of twelve
independent arms only the em-dash-stub arm scored met, which is the F3 fidelity gap rather
than a false-green of any contracted control. No junk state met the counter otherwise.

## Residual risk and verification gaps

- `_find_register` returns the FIRST sentence-bearing, stub-free, header-carrying section;
  a crafted earlier such section would win selection. Not treated as a defect: SCORECARD
  text is lane-owned claim data, not adversarial input.
- F5 was established by code inspection only; a live isolation (row whose sole pointer is
  non-prefixed, all other files present) was not run.
- C2 counter behavior is out of this seat's scope; only its byte-identity to the freeze
  revision was checked.
- The round verifier's actual output-matching grammar (exact vs token) was not observed;
  F1 states both readings.

Scratch `/fast/scratch/hyaku/mori-r58/Mo58Reviewer04/` removed after this report was
written; no other writes performed.
