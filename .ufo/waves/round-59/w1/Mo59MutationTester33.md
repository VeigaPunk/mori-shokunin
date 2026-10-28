# Mo59MutationTester33 — C1 selftest-fixture mutant (binding-expect / keys-fail)

**Seat task.** Mutate `tools/mori-register-check.py` selftest fixtures: a fixture whose
expect prefix is `binding` but the failure is `keys` — does the counter notice the
prefix-vs-reason mismatch?

**Verdict: KILLED** — the counter notices on two independent channels, and the
semantic (selftest) arm alone is sufficient. No surviving mutant.

## Method (bounded)

Sandbox: scratch clone `--no-local` of the lane under
`/fast/scratch/hyaku/mori-r59/Mo59MutationTester33/lane` (toplevel asserted;
`.git` 138M → clone 456M; disk-guard green, 592.6G free). Lane repo touched
read-only (`git show`/`ls-tree`, counter runs with `--scratch` under my seat dir).
The counter was never modified in place; a repinned *scratch copy* was used only
to attribute detection between the sha arm and the selftest arm.

Detector: `python3 .ufo/waves/round-59/count-c1.py <rev> --repo <clone> --fleet /home/vgpnk/Projects/shokunin --scratch <dir>`.

## Mutant (smallest behavior-bearing point)

`tools/mori-register-check.py:261`, selftest case `stub_only`:

```diff
-    case("stub_only", STUB, _manifest(), PTRS, False, "binding")
+    case("stub_only", STUB + "\n## Capabilities\n\nThis is the lane's current capabilities register.\n", _manifest(), PTRS, False, "binding")
```

The fixture still declares the register (`binding` arm satisfied: `n_decl == 1`)
but now has **no key table**, so `check()` emits only `keys:missing` reasons —
expect prefix `binding`, actual failure class `keys`. This is the exact assigned
probe. The `check()` engine itself is byte-identical; only the selftest fixture
data changed.

- pristine tool sha256: `38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8` (== frozen PIN)
- mutant tool sha256: `45a5f7b13f9860db22d1fef5b91059b52c14fd8e913bb825300e879f3bee8c5a`
- mutant rev (scratch clone): `1f6c8d732c35651eb80496fb402e1006f668229f`

## Runs (actual outputs)

| leg | command | output | rc |
|---|---|---|---|
| counter selftest | `count-c1.py --selftest` | `C1_SELFTEST pass=6 fail=0` | 0 |
| tool selftest (pristine) | `mori-register-check.py --selftest` | `REGCHECK_SELFTEST pass=12 fail=0` | 0 |
| baseline | `count-c1.py 8ff344ff…` (real lane) | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=8ff344ff…` | 0 |
| mutant tool selftest | mutant `--selftest` | `FAIL stub_only: ok=False reasons=['keys:missing=rounds[832].capabilities_added[0]', 'keys:missing=rounds[832].capabilities_added[1]']` + `REGCHECK_SELFTEST pass=11 fail=1` | 1 |
| mutant, frozen counter | `count-c1.py 1f6c8d73…` | `C1=unmet selftest=bad fixtures=ok real=ok pointers=ok rev=1f6c8d73… failed=tool_sha,selftest` | 1 |
| mutant, repinned scratch counter | PIN→mutant sha | `C1=unmet selftest=bad fixtures=ok real=ok pointers=ok rev=1f6c8d73… failed=selftest` | 1 |
| restored rev `c308304a` | `count-c1.py c308304a…` | `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=c308304a…` | 0 |
| restored tool selftest | reverted `--selftest` | `REGCHECK_SELFTEST pass=12 fail=0` | 0 |

## Attribution

1. **sha arm**: `failed=tool_sha` — any byte drift in the tool is caught by the
   frozen PIN (`count-c1.py:46`), trivially.
2. **selftest arm (semantic)**: with the tool sha repinned in a scratch copy of
   the counter, `failed=selftest` still fires. Mechanism: the tool's own
   `case()` predicate checks `any(r.startswith(want_reason))`
   (`mori-register-check.py:251-252`), so `binding`-expected vs `keys`-emitted
   flips the case to fail → output `pass=11 fail=1` ≠ frozen
   `EXPECT_SELFTEST` (`REGCHECK_SELFTEST pass=12 fail=0`) → counter marks
   `selftest=bad`. The prefix-vs-reason mismatch is therefore detected
   *semantically*, not merely by identity pinning.

## Restoration evidence

Mutant commit reverted in the scratch clone only (`c308304a`):
- `sha256sum tools/mori-register-check.py` → `38b733d8…472b8` (working tree)
- `git show HEAD:tools/mori-register-check.py` → `38b733d8…472b8` (committed bytes)
- `git status --porcelain` → 0 lines; detector re-run on restored bytes → `C1=met`, rc 0.
Lane repo: no writes made (mutations exist only in the scratch clone; lane HEAD
unchanged; pre-existing ` M corpus/SOURCES.md` + `?? w1/` are not mine).

## Coverage notes (bounded, no contract change implied)

- The counter has **no independent reason-audit channel** for the tool's internal
  selftest: it sees only the selftest output string and the tool sha. A mutant
  that broke `case()`'s reason check *and* forged `pass=12 fail=0` would slip the
  selftest arm but is still killed by `tool_sha` — under the frozen PIN, coverage
  holds end-to-end. The prefix semantics live entirely inside the pinned tool.
- `case()` accepts `any` covering reason with `startswith` prefix matching;
  extra unrelated reasons are tolerated. Irrelevant to this probe (emitted
  reasons were exclusively `keys:missing`), noted for completeness.
- `count-c1.py` fixture arm computes `got` (reason-token set, ~line 145) but
  never uses it; `matched` already enforces expect prefixes against `reasons`
  directly. Dead code, not a defect.

## Artifact hygiene

Scratch `/fast/scratch/hyaku/mori-r59/Mo59MutationTester33/` (incl. lane clone,
mutated+repinned copies, fixture materializations) removed after this report;
all receipts are embedded above. No production edits, no fleet writes, no lane
VCS mutation, no commits outside the throwaway clone.
