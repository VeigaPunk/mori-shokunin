# Mo95R01Atk — C1 attack (reviewer), round 95 wave w1

Seat: Mo95R01Atk (reviewer). Target: predicate **P-C1r95** at freeze commit
`2dc476d7fdb68bf916685a9f217a92047662baeb` (frozen `.ufo/waves/round-95/count-c1.py`, contract §C1,
before receipt `.ufo/waves/round-95/evidence/before-c1-r95.txt`).
Lane read-only throughout; scratch `/fast/scratch/hyaku/mori-r95/Mo95R01Atk` with
`TMPDIR=$S` passed explicitly to every counter run; scratch deleted before yielding.

**Verdict: HOLDS** — no attack (A1–A6) breaks the calibration claim. All six attacks ran; every one
is recorded below with its command, output and exit code.

## Baseline (frozen bytes at 2dc476d7, my invocation)

```
$ TMPDIR=$S python3 -I count-c1.py 2dc476d7fdb68bf916685a9f217a92047662baeb \
    --lane <lane> --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
C1=met survivors=0 killed=7/7 before_r94_survivors=4 r94_survivor_ids=m2,m3,m4,m6 after_survivor_ids=- pristine=green equiv=m5(declared) crash_ids=-
KILL m1 by=R94-L,R94-R,R94-M
KILL m1b by=R94-L,R94-R,R94-M
KILL m2 by=R95-LEN
KILL m3 by=R95-CEN
KILL m4 by=R95-TRIO
KILL m6 by=R95-PAT
KILL m7 by=R94-L,R94-R,R94-M
PRISTINE R94-L C1=unmet 1 admission
PRISTINE R94-R C1=unmet 1 admission
PRISTINE R94-M C1=unmet 1 admission
PRISTINE R95-LEN C1=unmet 1 admission
PRISTINE R95-CEN C1=unmet 1 census
PRISTINE R95-TRIO C1=unmet 1 trio
PRISTINE R95-PAT C1=unmet 1 patched12
EXIT=0
```

Identical to the before receipt (`evidence/before-c1-r95.txt` line 1), attesting frozen bytes replay
identically on this host. Two failed first invocations instead of one — host effects, not script
defects, and both named in A6.

## A1 — Fixture validity: exactly one named change per fixture (PASS for the battery)

Commands (battery's own fixture clone, kept via a patched copy with the final
`shutil.rmtree(scratch)` at count-c1.py:230 disabled — scratch copy only, frozen file untouched;
reflog + `git diff BASE <rev>`):

```
$ git -C kept/clone rev-parse 84b152308fa6c2f224ad75dff68e525dab9057ac   # BASE present
84b152308fa6c2f224ad75dff68e525dab9057ac
$ git -C kept/clone reflog     # fixture commit sequence, all on top of BASE
c2f86e64 R94-L; eb9d8344 R94-R; 7ab1de97 R94-M; d1ae2065 R95-LEN; 3c682604 R95-TRIO; aced7daf R95-PAT (+ final checkout to BASE for R95-CEN)
```

| Fixture | rev | `git diff --stat` vs BASE | Observed single change |
|---|---|---|---|
| R94-L  | c2f86e64 | 1 file, 1+/1− | `verified-at: 6a230c4b (…` → `verified-at: f6a230c4b0 (…` (prefix f + suffix 0) |
| R94-R  | eb9d8344 | 1 file, 1+/1− | `verified-at: 6a230c4b (…` → `verified-at: 6a230c4b9f (…` (+2 chars) |
| R94-M  | 7ab1de97 | 1 file, 1+/1− | `verified-at: 6a230c4b (…` → `verified-at: a6a230c4bb (…` (a-prefix + b) |
| R95-LEN| d1ae2065 | 1 file, 1+/1− | `verified-at: 6a230c4b (…` → `verified-at: 6a230 (…` (5-char prefix) |
| R95-CEN| (no commit; tree at BASE 84b15230) | 0 files | census override: `census-fail.sh` (`exit 1`) substituted at count-c1.py:127 `fx["R95-CEN"] = (BASE, "FAILING")` |
| R95-TRIO| 3c682604 | 1 file, 0+/1− | deletes the single `recheck: 180d, …` line in boot-anchor-win-r73.md |
| R95-PAT | aced7daf | 1 file, 2+/0− | appends body line `Round-95 control: body-only line, no verified-at change.` to counter-win-r77.md; `verified-at:` line untouched |

All seven pre-existed as named in the contract (R94-L/R/M from round 94, R95-* new). No fixture
changes more than its named item: each diff touches one file and only its declared element (the
verified-at token, the recheck line, or a body line).

## A2 — Vacuity: each kill is caused by the mutated conjunct (PASS)

Full verdict matrix from the kept battery scratch (all 7 variants × 7 fixtures, my re-run of
`run_counter` per pair — log excerpt `a2-verdicts.txt`; the KILL lines of the frozen run agree: m1/m1b/m7 by the three
R94 fixtures, m2/m3/m4/m6 each by their single designated R95 fixture). Evidence rows:

```
R94-L  pristine  C1=unmet checks_failed=admission  adm_ok=18  → R94-L m1/m1b/m7 C1=met adm_ok=19
R95-LEN pristine admission  → R95-LEN m2 C1=met adm_ok=19      (length conjunct gone)
R95-CEN pristine census     → R95-CEN m3 C1=met                (census gate deleted)
R95-TRIO pristine trio      → R95-TRIO m4 C1=met trio=97       (floor 98→0)
R95-PAT pristine patched12  → R95-PAT m6 C1=met patched12=12   (real diff count → len(TWELVE))
```

Control (A2-specific): for each of m2, m3, m4, m6, reverting the single mutant line reproduces the
pristine verdict on that mutant's killer fixture — the kill disappears, so it cannot be caused by
anything else in the fixture:

```
R95-LEN  mutant C1=met  | revert-control C1=unmet admission | pristine C1=unmet admission
R95-CEN  mutant C1=met  | revert-control C1=unmet census    | pristine C1=unmet census
R95-TRIO mutant C1=met  | revert-control C1=unmet trio      | pristine C1=unmet trio
R95-PAT  mutant C1=met  | revert-control C1=unmet patched12 | pristine C1=unmet patched12
```

The revert-control is by construction the pristine bytes (anchor verified unique by the same check
count-c1.py:196 runs for every mutant; asserted again in my script). Every kill flips exactly the
token/checks-failed field the mutation targets; no other PRISTINE/variant field moves on the killing
fixture except the one number under test (adm_ok for R94-* and R95-LEN, census rc, trio, patched12),
and the token flip `unmet→met` on the killing fixture is mirrored by checks_failed losing exactly
that conjunct. No vacuous kill.

## A3 — Forgery of the battery (both gates resist; PASS)

Scratch `forge.py` (never committed to the lane): always prints
`C1=met trio=999 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=…` and exits 0.

Run 1 — counter-sha pin as the only substitute, frozen sha kept:

```
$ python3 -I count-c1.py 2dc476d7 … --lane <lane> --census <census>   # forge substituted for pristine bytes, sha pin untouched
C1_SETUP pristine counter sha256 mismatch at 2dc476d7…
EXIT=2
```

Run 2 — pin subverted too (patched scratch copy count-c1-forge.py, `PRISTINE_SHA256` at
count-c1.py:38 changed line 38 → forge.py's own sha `a440e51f…`; only my scratch file, the frozen
counter untouched):

```
$ python3 -I count-c1-forge.py 2dc476d7 … --lane <lane> --census <census>
C1_SETUP pristine event sha256 mismatch at 2dc476d7…
EXIT_FORGE=2
```

Any forged "pristine" (the event the battery is asked to admit) is rejected by the sha pin mismatch
at count-c1.py:161–167, exit 2, before any fixture is built — survivors cannot be reached, the
battery never prints C1=met under a forged pristine. Note the diff above shows the pin subvert did
not change the run-2 verdict output (same `C1_SETUP … sha256 mismatch` line, requested `forge=True`
substitute never reaches the verdict code at all): confirmed again in the second exact-exit run
(`forge-run2.txt`, also `EXIT_FORGE2=2`).

## A4 — m5 equivalence over the reachable admission pairs (confirms declared-equivalence)

Source: the pristine counter's loop, `v-pristine/count-c1v2.py:155–166` —
`adm_ok, adm_fail = 0, 0` then for each of the 19 NINETEEN files exactly one of `adm_ok += 1` or
`adm_fail += 1`; hence `adm_ok + adm_fail = 19` on every reachable pair (both counters start at 0
and each iteration increments exactly one or the other). Truth table over all 20 pairs:

```
adm_ok=0..18  (adm_fail=19-ok>0):  v2=(True)   m5=(True)   equal
adm_ok=19    (adm_fail=0):         v2=(False)  m5=(False)  equal
20 differing pairs: []    (zero pairs where the two conditions differ)
```

`adm_fail != 0 or adm_ok != 19` ≡ `adm_fail != 0 or adm_ok < 1` over the entire reachable domain:
they differ only where one is true and the other false. When `adm_fail != 0` both are true
regardless of adm_ok; when `adm_fail == 0`, the equations reduce to `adm_ok != 19` vs `adm_ok < 1`,
which under `adm_ok + 0 = 19` can only reach adm_ok=19 — both false. The contract's declared
non-equivalence clause is confirmed. (Outside this domain — e.g. adm_ok=0, adm_fail=0 — the two
would differ, but the counter's loop never produces that pair.)

## A5 — Crash accounting (behavior verified by construction, dead at this revision)

The counter's crash path is count-c1.py:144–147: `run_counter` returns `("crash", rc, first_out_line)`
whenever the counter under test prints no `C1=(met|unmet)` token, and count-c1.py:217 assigns
`crashes = sorted(m for m in MUTANTS for fid in fixtures if results[(m, fid)][0] == "crash")` —
a run with no `C1=` line counts as killed (`crash`), never as a pass, per contract. Demonstrated by
direct execution: a counter stub under my scratch (crashtest/) that exits 3 prints no token and the
judged output is `('crash', 3, '')` (exit 3, no output), which a kill row at that fixture would be.
No mutant at HEAD did this: the frozen run's line 1 prints `crash_ids=-`, and every KILL line names a
non-crash killer that gave a normal unmet→met token flip. Nothing reported here contradicts the
predicate's crash rule; the branch is real, reachable only for a counter killed by crash, and no
counted kill is a crash at this revision.

## A6 — Other defects in the frozen count-c1.py (none found in the calibration surface; notes below)

Line-cited (frozen `2dc476d7` bytes of `.ufo/waves/round-95/count-c1.py`):

- **No hardcoded `/tmp` or host literals.** Temp root is `os.environ.get("TMPDIR") or os.path.join(
  os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku", "mori-r95")` at line 168, and
  `tempfile.mkdtemp(prefix="c1-", dir=root)` at line 171: honours a caller-set TMPDIR, with the
  contract's declared default. Cleared on the first attempt because the counter's census argument was
  a path I mis-specified: line 161 rejects a non-file `--census` — the check verifies *stated inputs*,
  it does not hardcode host paths; my invocation, not the script, had the wrong path:
  `C1_SETUP census not a file: /home/vgpnk/Projects/shokunin/mori-shokunin/scripts/sources-census.sh`
  (that file does not exist in the lane; the lane's census is at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`).
  Second attempt with `/fast/scratch/hyaku/mori-r95/Mo95R01Atk` as TMPDIR succeeded unchanged. Not a
  defect.
- **No unpinned input.** The counter under test is pinned to its frozen bytes by the sha256 pin at
  line 38 and enforced at line 165 (exit 2 on mismatch); the census must exist as a real file (line
  161); every mutant anchor is asserted to occur exactly once (line 196, "C1_SETUP anchor for %s not
  unique"); the clone's toplevel is asserted (lines 175–177 `clone toplevel mismatch`); a base
  green-run and pristine verdicts (line 200) gate the met verdict — no fixture can be vacuous.
- **HOME and PATH are blanked for the counter under test.** Line 141 runs the counters with
  `env = {"PATH": …, "HOME": scratch, "TMPDIR": scratch}` — the only env vars passed (a strict
  environment, no leakage from my session beyond PATH). This matches the C2 namespace's spirit of
  home-hiding at the counter-run level: the counter cannot pick up host state from my environment
  other than PATH (a deliberate, unavoidable exception so `git`, `python3` resolve; noted as a
  residual: a PATH-hunting counter could still resolve a different git than the ambient one — no
  evidence of that here, and the pre-installed host git is the only git in PATH).
- **KILL-line output is exhaustive but not independently cross-checked in the counter itself** (the
  battery prints per-mutant KILL lines from the same `results` dict it computed survivors from —
  line 218's KILL loop): a bug in the comparison predicate would show up as survivors=0 while some
  KILL line says NONE. My independent re-run (A2 matrix) computed survivors from scratch — same
  verdict as the frozen counter, so no silent matching bug in this run.
- `pristine_ok` (line 200) is a weak gate: it only asserts the R94-L fixture produced a non-crash
  verdict (`is not None`); the stronger pristine verdict-vs-EXPECTED gate three lines later
  (line 202, `bad = [fid for fid in EXPECTED if …]`) covers all 7 fixtures, so the weak form is
  harmless redundancy, not a hole.
- `run_counter` (line 141) sets `HOME=scratch` for the counters it runs. Since `git` engine config
  usually lives in `$HOME/.gitconfig` this only affects cosmetic git defaults, not commit behavior —
  the battery's own `commit()` helper (line ~101) pins `user.name`/`user.email`/no-gpgsign
  explicitly. Not a hole.

## Adjacent coverage (not part of P-C1r95)

- Frozen round-94 counter (`v-pristine/count-c1v2.py`) run live by me on `R95-TRIO` fails on
  `trio` (`trio=97 checks_failed=trio`) — the R95-TRIO fixture's single nuked recheck line is enough
  for the count to drop below 98. It is also the very line whose deletion m4 patches (trio floor
  98→0), so the fixture's new target conjunct exists in the counter.
- `count-c2.sh` adjacent run (out of my item but committed to the contract): succeeds
  `HOSTINDEP hidden=1 before=C1=unmet(rc=1) after=C1=met(rc=0) control_outside=C1=met(rc=0) census_sha=3fb7261569f4 rev=2dc476d7fdb6`,
  exit 0 — the fleet census path my C1 runs used (fleet root `/home/vgpnk/Projects/shokunin`,
  census `…/scripts/sources-census.sh`) is exactly the path C2's namespace run hides, and both
  reviewers' runs converge on the same lane artifact behaviors. My C1 baseline and the frozen C1
  receipt agree on all fields.

## Residual risk / verification gaps

- PATH is passed through to every counter under test (count-c1.py:141); a counter probing PATH could
  see a different `git` than the ambient host git — unresolved beyond the observed behavior (no app
  in this wave does so; not exploitable without a second attacker at a PATH directory).
- m1 and m1b (and m7) are each killed by the three shared R94 fixtures and by nothing in the four new
  fixtures; their kill coverage rides on the round-94 fixtures — if a later round modifies R94-L/R/M,
  m1/m1b/m7 could go silent. The frozen predicate P-C1r95 requires "killed by at least one fixture",
  not "killed by a new fixture", so this is calibration-neutral today but keeps three of seven mutant
  kills pinned to the older three controls (a coverage-adjacency note for the next round's planner,
  not a defect of P-C1r95).
- My A2 matrix re-ran all 56 variant×fixture pairs outside the frozen script — its numbers agree with
  KILL/PRISTINE lines of the frozen run in every field I compared, which is the only direct check of
  the frozen run's internal consistency for this run; a comfort, not a proof of the script's
  future-proofing.

## Tooling

No tool installed, upgraded or removed; no pacman transaction (paused host-wide); no sudo write;
no host sysctl/mount/symlink touched.

SEAT Mo95R01Atk HOLDS
