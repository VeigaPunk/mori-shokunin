# Mo61SimplC3 — advisory simplification review of `.ufo/waves/round-61/count-c3.py`

Seat: Mo61SimplC3 (simplifier, advisory only). Frozen bytes: **not edited**.
Lane: mori-shokunin. Target file:
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c3.py`
(sha256 `6e1fcd3e29b1496bd41a9adab85ce5a980b8c3c05b033f2fc67b5c664f1e6630`, 289 lines,
read end to end). No VCS mutation, no fleet/sibling writes, no fixture outside scratch.

## Summary (one paragraph)

Read end to end, the r61 C3 counter is functionally correct at the freeze revision —
`C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=ok cases=5 rev=7370a731…`
(rc=0) and `C3_SELFTEST pass=8 fail=0` (rc=0) — but it carries **five distinct pieces of
dead or decorative code and three duplicate authorities** that a later round could delete
without touching any frozen contract: (1) `sh(..., binary=)`'s decode branch is unreachable
because both call sites pass `binary=True` (`:65`); (2) `materialize_pinned(run=True)`'s
execution branch is unreachable from the counter's own call sites — the only `run=True` call
passes an unpinned blob and is refused, and the pinned call uses `run=False` (`:128`, `:136`) —
so `EXEC_LOG` (`:58`) is write-only in practice and the "zero child executions recorded"
property holds by construction rather than by measurement (child census: 2 `git` children, 0
`python` children); (3) `arm_r61repair`'s second regex alternative `^\s*{t}_ok = ` (`:121`)
never matches the frozen bytes for any of the five tokens, so the disjunct is dead and, were
it live, would be a loose test (any line starting `<t>_ok =` would count as "bound" without
feeding `b[]`); (4) the module-level `TOKEN_MAP` (`:166`) is **never read at runtime** — its
only use is as a regex target inside `arm_r61repair` (`:113`) — so the "published TOKEN_MAP"
the contract names is a third spelling of the same five names already held by `TOKENS` (`:44`)
and by the `t + "_ok"` key construction (`:186`, `:194`), i.e. a pure duplicate authority;
(5) `EXPECTS`/`EXPECT_PIN` (`:46-48`) are decorative: `EXPECTS` is *derived* from `TOKENS`
(`{t: "ok" for t in TOKENS}`), `EXPECT_PIN` is computed *from `EXPECTS` at import* (`:47`),
and `arm_expectpin` (`:142-152`) recomputes that identical digest and compares it to itself —
so the comparison is `x != x`, no measured token value is ever compared against the expected
value, and an on-disk tamper of `EXPECTS` is **accepted** (proved below). Two further
needless-complexity items are the module-global `PIN_C1`/`PIN_C2` swap in `run_arms`
(`:176-190`, not exception-safe, parameterizes one arm) and the selftest's `src.name.replace(src.name, …)`
no-op (`:217`). The docstring's **arm list matches the code exactly** (five arms, same names,
same order as `TOKENS`), but two arm *descriptions* overstate what the code checks
(details in §3).

## 1. Dead code / unused arms (exact evidence)

| # | Site | Finding | Evidence |
|---|------|---------|----------|
| D1 | `count-c3.py:61-65` | `sh(repo, *args, binary=False)`: the `binary=False` branch `r.stdout.decode("utf-8","replace")` is unreachable — **both** call sites pass `binary=True` (`:69` in `cat`, `:281` in `main`). | `grep -n 'sh(' count-c3.py` → only `:61` (def), `:69`, `:281`; both `binary=True`. Probe: `sh_binary_false_calls` → only the `def` line. |
| D2 | `count-c3.py:72-84`, `:128`, `:136` | `materialize_pinned(..., run=True)`'s `subprocess.run([sys.executable, "-c", blob…])` branch is **never reached**: the sole `run=True` call (`:128`) passes a blob whose sha is not `"0"*64` → returns `("unpinned")` before the `if run:`; the pinned call (`:134-136`) passes `run=False`. | Probe: `materialize_unpinned` → `{"payload_is_none": true, "reason": "unpinned"}`; a full `run_arms` run left `exec_log_len: 0`; child-process census over a full run → exactly 2 children, both `git -C …/st-live` (the `livepins` arm), **no** `python -c` child. |
| D3 | `count-c3.py:58`, `:80`, `:131` | `EXEC_LOG` is written **only** inside the unreachable D2 branch (`:80`), so the guard `if EXEC_LOG:` (`:131`) is vacuous and the contract's "zero child executions recorded" is asserted, not measured. | Same probe as D2 (`exec_log_len: 0`). |
| D4 | `count-c3.py:120-122` | `arm_r61repair`'s second disjunct `re.search(rf"^\s*{t}_ok = ", text, re.M)` never matches the frozen source for any token — dead alternative (the first disjunct `b["<t>_ok"], _ = ` matches all five). | Probe `arm_r61repair_alternatives`: for all 5 tokens `first_alt_b_ok_form: true`, `second_alt_ok_assign: false`. |
| D5 | `count-c3.py:166-172` | The `TOKEN_MAP` **dict** is never read at runtime; only its *source text* is parsed (`:113`). The real binding is `b["<t>_ok"]` keys built in `run_arms` (`:186-190`) and re-derived as `t + "_ok"` in `fmt` (`:194`). | Probe replaced `m.TOKEN_MAP` with a recording dict subclass → `token_map_runtime_reads: []` over a full `run_arms` call. |

## 2. Duplicate authorities (three spellings of the same five names)

- `TOKENS` (`:44`) — the list.
- `TOKEN_MAP` (`:166`) — a dict whose every value is exactly `t + "_ok"` (probe: `TOKEN_MAP==t+_ok: true`), never consulted (D5).
- `b["<t>_ok"]` string literals + `t + "_ok"` concatenation (`:186`, `:194`).
- `EXPECTS` (`:46`) is a fourth, fully derived projection of `TOKENS` (probe: `EXPECTS==TOKENS projection: true`).

`REASON` (`:50-56`) is *not* a duplicate — its keys equal `TOKENS` but its values are unique prose, and it is consumed once at `:195`.

## 3. Docstring arm list vs. code — verdict

**Arm list matches.** Docstring "Arms" block (`:8-24`) lists `r60hole`, `r61repair`,
`blobrefusal`, `expectpin`, `livepins` — identical names and order to `TOKENS` (`:44`),
`TOKEN_MAP` keys (`:166`), `run_arms`' five invocations (`:186-190`), `fmt`'s printed tokens
(`:194`), and the `REASON` keys (`:50`). `cases=5` (`:284`) equals the arm count.

**Two arm descriptions overstate the code:**

- **r60hole (`:9-13`)** — docstring: "zero `failed.append("` sites". The code (`:96-104`)
  checks only that there is no `failed.append("<gate-token>")` for the three names
  `toolgate`/`containment`/`expectgate`. The pinned r60 bytes contain **19** other
  `failed.append(...)` sites, so the literal docstring claim is false against the very bytes
  the arm parses. (`grep -c 'failed\.append' r60_count-c3.py` → `19`;
  `grep -c 'failed\.append("toolgate")\|failed\.append("containment")\|failed\.append("expectgate")'` → `0`.)
  The code's real check is a *pair*: no append site for the token **and** the token is tested
  against `failed` (r60:296-306 shows the three tokens printed from the print expression).
- **livepins (`:22-23`)** — docstring: "the r61 count-c1.py / count-c2.py **materialize** at
  `<rev>`". Nothing is materialized: `cat()` (`:68-69`) is a one-line wrapper over
  `git show` and the bytes are compared by sha in memory (`:156-163`). A wording-only drift.
- **Top docstring (`:5-8`)** — "every printed token is one measured boolean under the published
  TOKEN_MAP" and "the frozen expect table is sha-pinned": both describe mechanisms the code
  does not use (D5, D6 below).

## 4. Findings for the L1 (falsification-grade, advisory — no fix applied)

**F1 — `expectpin` is a tautology; an on-disk tampered expect table is accepted.**
`EXPECT_PIN` (`:47`) is derived from `EXPECTS` at import, and `arm_expectpin` (`:142-152`)
recomputes the same digest and compares it to itself. Proof (scratch copy of the counter with
`EXPECTS = {t: "FAIL" for t in TOKENS}` substituted — production bytes untouched):
`arm_expectpin()` still returns `True`, while `EXPECT_PIN` changes from
`3a62b4f49066783de0fcd94dbc2e583c42e53dfb3e4ffc48ec3e7901c952e95e` to a different value and
`EXPECTS` equals the tampered table. The only tamper the arm detects is an in-memory
`dict(EXPECTS)` copy — that proves sha256 sensitivity, not a frozen pin. Against the
contract's kill rule ("an accepted tampered expect table") and the C3 target (c) "its frozen
expect table is sha-pinned and a tampered table is refused", the *on-disk* table is not
sha-pinned to any external constant, and no measured token value is ever compared against
`EXPECTS`. Reported, not fixed (frozen bytes; amendments barred).

**F2 — the `met` conjunct is name-based, not structural.**
`run_arms` computes `c1_ok = all(b.values())` then `met = c1_ok` (`:187-188`); the
`c1_ok` name is a ceremonial alias whose only function is to satisfy `arm_r61repair`'s
substring test `"c1_ok" in m.group(1)` (`:110-111`, regex first match:
`"    met = c1_ok"`, group `"c1_ok"` — probe `met_regex_first_match`). Symmetrically,
`arm_r60hole`'s red-before detection is the substring test `"c1" in m.group(1)` (`:93-94`)
against r60's `met = (c2_ok and toolgate and old_hole and containment and expectgate)`
(r60:255). Both arms are therefore satisfiable by a **rename** rather than by a change in the
measured conjunction. Substantively the count-c1 pin *is* covered, transitively via
`livepins_ok` (which checks `PIN_C1` = sha256 of `count-c1.py`), and the live pins in fact
match the committed files exactly (`sha256sum count-c1.py` = `a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00` = `PIN_C1`;
`count-c2.py` = `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8` = `PIN_C2`),
so this is a criterion-strength observation, not a live-pin failure.

**F3 — the selftest ignores `--repo` and depends on `cwd`.**
`selftest()` reads the fixtures from `os.getcwd()` (`:216`, `:230`) while the live path uses
`--repo` (`:271`, `:283`). Running `--selftest` from any other directory dies with
`FileNotFoundError: … '/fast/scratch/hyaku/mori-r61/Mo61SimplC3/.ufo/waves/round-61/count-c1.py'`
(traceback captured, rc=1); from the lane root it passes 8/8. `main` parses `--repo` and
discards it in selftest mode (`:276-278`).

## 5. Needless complexity (no behavior change implied)

- **C1 — global mutation to parameterize one arm.** `run_arms` declares
  `global PIN_C1, PIN_C2` (`:176`), swaps them from the `pins` argument (`:178-179`) and
  restores them after the arms (`:189`). `arm_livepins` reads the module globals (`:157-158`).
  Passing `pins` as an argument to `arm_livepins` would remove the `global` statement, the
  save/restore pair, and the non-exception-safe window (an exception inside an arm leaves
  the pins swapped for the rest of the process).
- **C2 — no-op string expression.** `:217` `(d / src.name.replace(src.name, R61_C1 if src.name.endswith("c1.py") else R61_C2)).write_bytes(src.read_bytes())`
  replaces the whole name with the target path; `for rel in (R61_C1, R61_C2): (d / rel).write_bytes((Path(os.getcwd()) / rel).read_bytes())`
  is the same behavior without the self-replace.
- **C3 — constant passed as a parameter.** `fmt(b, met, rev, cases)` (`:193`) has exactly one
  call site, `fmt(b, met, a.rev, cases=5)` (`:284`); `cases` is the arm count and would
  silently drift from the arm list if an arm were added.
- **C4 — redundant `met`.** `met` is `all(b.values())` (`:187`) and `fmt` recomputes the same
  conjunction to build its `failed` list (`:195`); `met` could be derived at its single consumer.
- **C5 — `cat()` is a one-line wrapper** over `sh()` used once (`:68-69`, `:158`).
- **C6 — brittleness of the two selftest mutations.** The self-mutant depends on the exact
  byte string `b"c1_ok = all(b.values())\n    met = c1_ok"` (`:246`) and the r60 mutant on the
  exact string `b"met = (c2_ok"` (`:238`); both are present in the pinned bytes today
  (r60:255 = `    met = (c2_ok and toolgate …)`), but a reformat turns either mutation into a
  no-op that silently degrades the selftest case to "expect failure, get success" → red.

## 6. Preserved contract (what a simplifier must not break)

- The five-token met line shape and `cases=5` (`fmt`, `:193-198`).
- `PIN_C1`/`PIN_C2` = sha256 of the committed `count-c1.py`/`count-c2.py` (both verified equal
  to the on-disk files; see F2) and `R60_SHA` = sha256 of r60's `count-c3.py` at
  `ac496c7c…` (verified: `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514`).
- Refusal-before-execution ordering in `materialize_pinned` (pin check precedes any
  `subprocess.run`) — the property the contract's arm (b) rests on; the *reachability* of the
  execution branch (D2) is the only thing at issue, not the ordering.
- The r60 red-before semantics: the arm must *fail* if the r60 hole is absent.

## 7. Verification receipt (commands actually run, read-only)

```
$ sha256sum .ufo/waves/round-61/count-c3.py
6e1fcd3e29b1496bd41a9adab85ce5a980b8c3c05b033f2fc67b5c664f1e6630  (289 lines)
$ python3 .ufo/waves/round-61/count-c3.py 7370a731abcafc4c803111de7c22cd6264d63be1 \
      --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch $TMPDIR
C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=ok cases=5 rev=7370a731abcafc4c803111de7c22cd6264d63be1
rc=0
$ python3 .ufo/waves/round-61/count-c3.py --selftest --scratch $TMPDIR      # cwd = lane root
C3_SELFTEST pass=8 fail=0                                            rc=0
$ python3 …/count-c3.py --selftest --scratch $TMPDIR                     # cwd = scratch → rc=1
FileNotFoundError: …/.ufo/waves/round-61/count-c1.py                    (F3)
$ git -C …/mori-shokunin show ac496c7c…:.ufo/waves/round-60/count-c3.py | sha256sum
fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514   (== R60_SHA)
$ grep -c 'failed\.append' <r60 bytes>      → 19
$ grep -c 'failed\.append("toolgate")\|failed\.append("containment")\|failed\.append("expectgate")' <r60 bytes> → 0
```

Instrumented probe (scratch-only `probe.py`: imports the frozen module by path, monkeypatches
`subprocess.run` and `TOKEN_MAP`, and loads a *tampered scratch copy* for F1) — outputs quoted
inline above; no production file was modified.

**Environment:** disk-guard `status` green before and after (root `/fast/scratch/hyaku` 56 % used,
357.1 G free). Scratch `/fast/scratch/hyaku/mori-r61/Mo61SimplC3/` (probe, r60 extract, fixture
`st-live/`, tampered scratch copy) — cleaned before yield. No tools installed or upgraded for
this seat (none needed). No commits, no `git`/`jj` mutation outside the counter's own
scratch fixture (`git -C <scratch>/st-live …`, inside scratch). No `task` dispatch, no
`agent://all` broadcast.

## 8. Tradeoff

Deleting D1–D5 and C1–C5 would remove ~35 lines of the 289-line counter without touching the
met line, the pins, the refusal ordering or the selftest's 8 cases — but it would change the
counter's *bytes*, and this round's contract freezes them (amendments barred), so nothing was
applied. F1 in particular is a property weakness rather than dead weight: tightening
`EXPECT_PIN` to an external constant would change behavior (a tampered `EXPECTS` would then
fail the arm), which is an L1 decision, not a simplifier's edit.
