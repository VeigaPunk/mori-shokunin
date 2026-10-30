# Mo61ScribeQuality — QUALITY.md criterion drafts (mori round 61, wave w1)

seat: `Mo61ScribeQuality` · lane: `mori-shokunin` · role: scribe · mode: **read-only
(detection/report only)** · date: 2026-10-30
Contract: `.ufo/waves/round-61/contract.md` (freeze `7370a731abcafc4c803111de7c22cd6264d63be1`,
entering `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`).

## Behavior

Read the round-61 contract, the three fresh-start closures (`corpus/lessons/round-58-verifier-spotcheck.md`,
`round-59-verifier-spotcheck.md`, `round-60-verifier-spotcheck.md`), the r60 lane lesson
(`corpus/lessons/round-60.md`), the six committed r61 evidence receipts, and the frozen r61
counters. Ran the frozen r61 C3 counter read-only at two revisions and a **scratch-only mutant
battery** against scratch copies of that counter (the lane repo was never modified). Drafted two
QUALITY.md criteria (blocks below); no production file, registry, counter, contract or VCS state
was touched.

Axes (godspeed): **cheap parallel iteration** — every reading above was issued as one batch of
concurrent reads; **frontier walk** — the criterion drafts were derived from what the round's own
instruments still expose (F1/F4 → Draft A, F2 → Draft B) and from the receipt gap the round's
evidence still shows (F3 → optional Draft C), not from a pre-chosen template.

Paths used below: `L=/home/vgpnk/Projects/shokunin/mori-shokunin`;
`S=/fast/scratch/hyaku/mori-r61/Mo61ScribeQuality` (seat scratch, created, used, removed).

## Gates executed (read-only, frozen counters)

All commands ran with `TMPDIR` inside the seat scratch; the lane repo was read via `git show` /
`git cat-file` / `git ls-tree` / `git status --porcelain` only. No mutating git/jj command was run
against the lane or any fleet repo; the only commits created were inside the throwaway fixture the
frozen counter itself builds under the seat scratch (`git -C <scratch>/st-live … commit`).

| # | command | result |
|---|---|---|
| G1 | `python3 $L/.ufo/waves/round-61/count-c3.py 7370a731abcafc4c803111de7c22cd6264d63be1 --repo $L --scratch $S` | `C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=ok cases=5 failed=none rev=7370a731abcafc4c803111de7c22cd6264d63be1` — **rc=0** |
| G2 | same, entering rev `325f7e639916fcbc77fa2ec7475951a1b86bb1cb` | `C3=unmet r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r61 counters absent or sha pin mismatch at rev rev=325f7e63…` — **rc=1**; the verdict line is byte-identical to the committed control receipt `.ufo/waves/round-61/evidence/control-c3-do-nothing.txt` (which additionally carries `rc=1`) |
| G3 | `git show ac496c7c:.ufo/waves/round-60/count-c3.py \| sha256sum` | `fabde06c9d0a94a8487e5de45be3e413f6084816fb0507a71fd335bad5153514` = the counter's own `R60_SHA` pin (`count-c3.py:40`) |
| G4 | `sha256sum .ufo/waves/round-61/count-c{1,2}.py` | `a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00` / `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8` = `PIN_C1`/`PIN_C2` (`count-c3.py:41-42`) |

G1–G2 are evidence-verification only; no gate was scored by this seat and no receipt was written
into the lane's `evidence/` directory.

## Findings

### F1 — the r61 C3 repair binds the verdict **head** correctly, but its self-check cannot certify the **token** binding, and the published `TOKEN_MAP` is never read by the print path (MEDIUM-HIGH, instrument robustness)

The r61 counter repairs the r60 defect-2 shape in two halves. The head half is repaired:
`met` is now the conjunction of all measured booleans (`count-c3.py:187-188`,
`c1_ok = all(b.values()); met = c1_ok`). The token half is bound on the shipped bytes (the print
expression reads the measured boolean) but the binding is **not certified by the counter itself**,
and the published map is decorative:

* the print site derives the boolean key by string concatenation and never reads the published map —
  `count-c3.py:194`: `toks = " ".join(f"{t}={'ok' if b[t + '_ok'] else 'FAIL'}" for t in TOKENS)`;
* `TOKEN_MAP` (`count-c3.py:166-172`) is referenced only in the docstring (`:6`, `:16`), in the
  `REASON` string (`:52`) and in the self-check arm's **key-set** regex (`:113-117`). Its **values**
  are never read by the print path and never checked against the booleans the arms assign;
* the token-binding check inside `arm_r61repair` (`:119-123`) requires an assignment site
  `b["<token>_ok"], _ = …` to exist — it does not require the print expression to read it.

Measured on scratch copies (the repo copy is untouched; `sha256sum` of the repo copy unchanged at
`6e1fcd3e29b1496bd41a9adab85ce5a980b8c3c05b033f2fc67b5c664f1e6630`). Driver: import the copy,
feed `run_arms` a tampered r60 blob (`met = (c2_ok` → `met = (c1_ok and c2_ok`, so the
`r60hole` arm measures **False**), then call the module's own `fmt`:

```
=== count-c3.py (pristine) ===
  arms       : {'r60hole_ok': False, 'r61repair_ok': True, 'blobrefusal_ok': True, 'expectpin_ok': True, 'livepins_ok': True} met: False
  repair_arm : (True, '')
  LINE       : C3=unmet r60hole=FAIL r61repair=ok blobrefusal=ok expectpin=ok livepins=ok cases=5 failed=r60 bytes lost or hole absent (red-before unfaithful) rev=7370a731…
=== m1_no_c1ok.py  (met line drops the c1_ok conjunct) ===
  arms       : {… 'r61repair_ok': False …} met: False
  repair_arm : (False, 'c1_conjunct_missing')
  LINE       : C3=unmet r60hole=FAIL r61repair=FAIL … failed=r60 bytes lost or hole absent (red-before unfaithful);self source lost the c1_ok conjunct or TOKEN_MAP …
=== m2_literal_token.py  (print expression prints the token from a literal) ===
  arms       : {'r60hole_ok': False, 'r61repair_ok': True, 'blobrefusal_ok': True, 'expectpin_ok': True, 'livepins_ok': True} met: False
  repair_arm : (True, '')
  LINE       : C3=unmet r60hole='ok' r61repair='ok' blobrefusal='ok' expectpin='ok' livepins='ok' cases=5 failed=r60 bytes lost or hole absent (red-before unfaithful) rev=7370a731…
=== m3_tokenmap_remap.py  (TOKEN_MAP value remapped "r60hole" → "livepins_ok") ===
  repair_arm : (True, '')
  LINE       : C3=unmet r60hole=FAIL … (unchanged: the print path never reads TOKEN_MAP)
```

Readings:

* **M1 kills** — the arm detects the dropped conjunct (`c1_conjunct_missing`), so the arm is not
  vacuous on the *composition* half of the repair;
* **M2 survives** — with the token printed from a literal, `arm_r61repair` still returns
  `(True, '')` and the counter prints `r60hole='ok'` beside
  `failed=r60 bytes lost or hole absent`. That is the **r60 defect-2 shape reproduced inside the
  repaired r61 counter** — in the mutant, not in the committed bytes: a token that reads "ok" while
  the boolean it names measured False;
* **M3 survives** — the map's values are unchecked, and because the print path re-derives the key,
  a wrong map changes nothing on the line and nothing in the arm.

The frozen kill rule (`contract.md:107-110`) lists "an unbound token" as a failure, but the only
unbound-token detector in the counter is the assignment-site regex, so the class the kill rule
names is not reachable by the shipped arm. **Reported, not fixed** — the counter is frozen and
amendments are barred.

**Scope of this finding (for the L1's scoring, so it is not over-read).** The *shipped* counter is
not holey on this axis: at `:194` the print expression reads the measured boolean `b[t + '_ok']`,
so on the committed bytes every printed token is that arm's measured value (G1/G2 above show the
head and the tokens agreeing). What is missing is the **detector's coverage** — the counter cannot
certify its own token binding, because the arm checks an assignment site rather than the print
site, and the published map's values are neither read nor checked. That is a robustness gap to
route to round 62 and the ground for Draft A; it is **not** a met-flip on the committed bytes and
does not, by itself, defeat the C3 kill rule.

### F2 — the counter's own `--selftest` is not re-runnable against the scratch it is given (MEDIUM, operability)

```
$ python3 $L/.ufo/waves/round-61/count-c3.py --selftest --scratch $S     # 1st run
C3_SELFTEST pass=8 fail=0
rc=0
$ python3 $L/.ufo/waves/round-61/count-c3.py --selftest --scratch $S     # 2nd run, same --scratch
subprocess.CalledProcessError: Command '['git', '-C', '<S>/st-live', '-c', 'user.name=t', '-c',
'user.email=t@t', 'commit', '-qm', 'x']' returned non-zero exit status 1
rc=1        # no "C3_SELFTEST pass=" line was printed at all
```

Cause (`count-c3.py:219-224`): the fixture dir `<scratch>/st-live` is created, `git init -q`'d and
committed; on a second run the copied bytes are identical, `git commit` exits non-zero
("nothing to commit") and `check=True` raises. The run therefore ends in a traceback with **no
tally and no verdict line**, and its exit code (1) is indistinguishable from a genuine selftest
failure. A receipt taken from the second run carries no verdict (this is the r59-routed-4 shape
again, in a different place).

### F3 — the r61 evidence set has no after-state (claim-verdict) receipt yet (LOW→MEDIUM, observation at measurement time)

```
$ ls .ufo/waves/round-61/evidence/
control-c1-do-nothing.txt  control-c2-do-nothing.txt  control-c3-do-nothing.txt
selftest-c1.txt  selftest-c2.txt  selftest-c3.txt
$ grep -c 'C[123]=met' .ufo/waves/round-61/evidence/*.txt
…/control-c1-do-nothing.txt:0   …/control-c2-do-nothing.txt:0   …/control-c3-do-nothing.txt:0
…/selftest-c1.txt:0             …/selftest-c2.txt:0             …/selftest-c3.txt:0
```

By contrast, the r60 tip (`6752eafd`) evidence directory carries the after-state receipts:
`c1-at-data.txt`, `c2-at-freeze.txt`, `c3-at-freeze.txt`, each with exactly one `C<n>=met` line.
The r59 closure routed exactly this ("No committed receipt for `C1=met`/`C2=met` at data revision
`7b86704d` — seats replayed the verdicts, but the counters' own post-data output was never
captured under `evidence/`"; `corpus/lessons/round-59-verifier-spotcheck.md:102-103`).
**Status: not present at the time of measurement** — the round is mid-flight and the data phase may
still land them; recorded so the L1 can check before filing, not as a permanent defect.

### F4 — the counter's selftest cannot see an unbound token either (corollary of F1)

`python3 $S/mut/m2_literal_token.py --selftest --scratch $S/fresh` → `C3_SELFTEST pass=8 fail=0`,
rc=0; same for the M3 map remap (`pass=8 fail=0`, rc=0). The selftest asserts on the boolean dict
(`b["r60hole_ok"]`), never on the printed line, so the token-binding defect is invisible to both
the self-check arm and the selftest battery.

### Closed by r61 (for the record)

* r60 routed defect 6 ("exit codes not receipted") is closed at r61: the r60 control receipts at
  `ac496c7c` carry `grep -c '^rc='` → 0/0/0/0; the r61 receipts carry `rc=1` (three controls) and
  `rc=0` (three selftests).
* r60 routed defect 2's *composition* half is closed at r61 (M1 kills); its *token-binding* half is
  not (F1).

## Draft QUALITY.md blocks (for L1 integration)

Numbering is provisional — `corpus/QUALITY.md` ends at 157 (`corpus/QUALITY.md:1605`, file 1619
lines); the L1 assigns the final numbers. Every block is drafted from this round's own evidence and
cites the lesson/round that produced it. None proposes a change to any frozen counter or to the
contract.

### Draft A → criterion 158

```
158. Every token a counting command prints on its verdict line is bound, in that
     same command, to a measured boolean, and the binding is read at the print
     site — a token→boolean map restated beside the print expression does not
     bind it. A published map binds only when (a) the print expression reads
     it, (b) every value in it names a boolean the arms actually assign, and
     (c) the command's own self-check fails on a print-site unbound mutant (a
     token printed from a literal, or from a key the map does not name) — not
     only on a mutant that drops a conjunct from the verdict line.
     ← `corpus/lessons/round-60.md:152-161` "Wave-found instrument defects" 1
     (r60 routed defect 2: `toolgate`/`containment`/`expectgate` were printed
     from failed-list literals that no append site emits — `grep -c
     'failed.append("toolgate")'` → 0/0/0 — while `met`
     (`.ufo/waves/round-60/count-c3.py:255` at `ac496c7c`) omitted the
     count-c1 pin conjunct, so an unmet line could read `containment=ok`
     beside `failed=g2_escape_written`);
     `corpus/lessons/round-60-verifier-spotcheck.md:168-171` (same defect,
     routed HIGH); the r61 repair `.ufo/waves/round-61/count-c3.py` —
     `TOKEN_MAP` :166-172, the arm's key-only check :113-117, the print site
     :194, `met` :187-188 — and the contract's pre-seat amendment 1
     (`.ufo/waves/round-61/contract.md:3-6`, "every printed token is one
     measured boolean under the published TOKEN_MAP").
     Shown able to fail: on a scratch copy of the r61 counter with the print
     expression mutated to a literal, `arm_r61repair` still returns
     `(True, '')` while the printed line reads
     `C3=unmet r60hole='ok' r61repair='ok' blobrefusal='ok' expectpin='ok'
     livepins='ok' cases=5 failed=r60 bytes lost or hole absent
     (red-before unfaithful)` — the r60 defect-2 shape reproduced inside the
     repaired counter — and the same copy still passes its own selftest
     (`C3_SELFTEST pass=8 fail=0`, rc=0); the same arm does return
     `(False, 'c1_conjunct_missing')` when the `met` line drops `c1_ok`, and
     a `TOKEN_MAP` value remap (`"r60hole" → "livepins_ok"`) is likewise
     accepted (`(True, '')`, `pass=8 fail=0`) because the print path never
     reads the map. Not covered: the token's semantics — whether the boolean
     it names measures the right thing; that stays judge work.
```

### Draft B → criterion 159

```
159. A counting command's self-test is re-runnable against the scratch it was
     given, and every run prints its tally. The self-test creates or refreshes
     its own fixture (or refuses with a named reason), does not assume an
     unused `--scratch`, and prints the `…_SELFTEST pass=… fail=…` line and
     the exit code on every invocation: a run that dies inside a fixture
     subprocess without a tally is a failed run, and its receipt carries no
     verdict.
     ← `corpus/lessons/round-58-verifier-spotcheck.md:87` (routed defect 4:
     "add explicit scratch-path CLI option before freezing new counters");
     `corpus/lessons/round-60.md:175-180` (hygiene row 5: a counter run
     without `--scratch` wrote into the lane root); r61 measurement: the
     frozen `.ufo/waves/round-61/count-c3.py --selftest` run twice against
     the same `--scratch` prints `C3_SELFTEST pass=8 fail=0` (rc=0) on the
     first run and then exits 1 with
     `subprocess.CalledProcessError: Command '['git', '-C', '<scratch>/st-live',
     …, 'commit', '-qm', 'x']' returned non-zero exit status 1` and **no**
     tally line on the second run — the same exit code as a genuine
     selftest failure. Not covered: a scratch the operator deletes between
     runs, and a counter that never took a `--scratch` option at all.
```

### Optional third draft (only if the L1 wants the receipt class carried)

```
160. A claim's after-state is receipted by the counting command itself: for
     each claim the round commits a receipt under
     `.ufo/waves/round-<N>/evidence/` holding that command's own stdout and
     exit code at the measured freeze/data revision, with the counter's
     verdict line as its first line. A do-nothing control receipt does not
     substitute for the after-state receipt, and a seat's replay of a verdict
     is not the receipt. Extends 76 from the self-test artifact to the
     claim-verdict artifact.
     ← `corpus/lessons/round-59-verifier-spotcheck.md:102-103` (routed defect
     4: no committed receipt for `C1=met`/`C2=met` at the data revision —
     seats replayed the verdicts, the counters' own output was never captured
     under `evidence/`); r60 practice at its tip
     (`6752eafd:.ufo/waves/round-60/evidence/{c1-at-data,c2-at-freeze,
     c3-at-freeze}.txt`, one `C<n>=met` line each); measured at r61:
     `grep -c 'C[123]=met' .ufo/waves/round-61/evidence/*.txt` → 0 in all six
     files present, against 1 in each of the three r60 after-state receipts.
     Not covered: a receipt whose bytes cannot be re-derived by re-running the
     frozen command at the named revision.
```

## Touched surfaces

* `.ufo/waves/round-61/w1/Mo61ScribeQuality.md` — **this report only**.
* Scratch (created, used, removed): `/fast/scratch/hyaku/mori-r61/Mo61ScribeQuality/` — mutant
  copies of `count-c3.py`, a mirror of the r61/r60 counter bytes used as the selftest working
  directory, and the driver script. All removed before yielding; every measured output quoted
  above is reproduced inline here.
* No file in `corpus/`, `tools/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `SHONEN.md`,
  the registry, the wave directory, or any sibling/fleet repo was created, edited or deleted.
* No git/jj mutation was executed anywhere: only `git cat-file`, `git show`, `git ls-tree`,
  `git status --porcelain` (read-only) against the lane repo, and `git init/add/commit` inside
  the throwaway fixtures the frozen counter itself creates under my scratch.

## Out of scope (deliberately not done)

* No fix, patch, amendment or remediation of the frozen r61 counter, the contract, the registry or
  the r61 evidence set — F1/F2/F3 are reported for the L1 to route to round 62, not applied here.
* No provider-death, OOM-kill, fleet-liveness or service-state inference; the lane's observability
  scope was not touched.
* No tools installed or upgraded (no pacman, no `uv tool`, no `npx`); the measurement used only
  the stock `python3` (3.14) and `git` already present on the host. Nothing to record under the
  operator's tooling authorization.
* `count-c1.py` and `count-c2.py` were not executed (the C1/C2 data phase is in flight; the
  receipts they produce are the L1's evidence, not this seat's).

## Artifact paths

* This seat's report: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/w1/Mo61ScribeQuality.md`
* Sources read (lane, read-only):
  `.ufo/waves/round-61/contract.md`, `.ufo/waves/round-61/count-c3.py`,
  `.ufo/waves/round-61/evidence/{control-c1,control-c2,control-c3}-do-nothing.txt`,
  `.ufo/waves/round-61/evidence/selftest-c{1,2,3}.txt`,
  `.ufo/waves/round-60/count-c3.py` (at `ac496c7c`),
  `corpus/lessons/round-58-verifier-spotcheck.md`, `corpus/lessons/round-59-verifier-spotcheck.md`,
  `corpus/lessons/round-60-verifier-spotcheck.md`, `corpus/lessons/round-60.md`, `corpus/QUALITY.md`.
* Scratch (temporary, deleted before yield): `/fast/scratch/hyaku/mori-r61/Mo61ScribeQuality/`
  (`mut/m1_no_c1ok.py`, `mut/m2_literal_token.py`, `mut/m3_tokenmap_remap.py`, `driver.py`,
  `mirror/`), `TMPDIR` pointed there for every counter invocation.
