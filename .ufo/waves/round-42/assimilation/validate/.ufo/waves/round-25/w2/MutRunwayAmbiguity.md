# Mutation probe — C2 `tools/mori-job-runway.py`, ambiguity handling

Seat: `MoriR25.MutRunwayAmbiguity` (wave 2, lane `/home/vgpnk/Projects/shokunin/mori-shokunin`).
Target of the attack: claim **C2** (harness background-job runway capability), specifically the
**ambiguity handling** of rules 2, 3 and 4 (`_binary_sites` and `_effective`).

## Verdict: **weakened** (coverage gap on the ambiguity axis — the landed tool is not defective)

The landed bytes are correct as written: every mutant below was a change I made in a private
clone and then reverted. The claim is weakened in the sense that matters for C2's after-value:
**the frozen 21 cases do not certify the ambiguity abstention**, and neither do the 18
supplementary cases. 8 of my 12 mutants were killed; **4 survived both committed suites**, and one
survivor (M11) produces exactly the failure mode amendment A2 exists to prevent — a hard number
where the contract says abstain.

Real omp behaviour on this host makes none of the four survivors reachable today
(one clamp site, one default site in the installed binary), so no live claim is falsified. The
gap is in the detector, not in the tool.

## Setup, baseline, restoration

* Private clone: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r25/w2-MutRunwayAmbiguity`
  (clone HEAD `e5e1b7bc1c8dd3dc838585f5ebacfd1bc39e1098`). The lane was never written to except
  this report file.
* Bytes under test (clone file == lane file, identical sha256 and git blob):
  * `tools/mori-job-runway.py` — sha256 `5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`,
    git blob `239dd8ebe630400a2739151260e482ad83dea459` (also `git rev-parse HEAD:tools/mori-job-runway.py` in the lane).
  * `tools/fixtures/mori-job-runway/cases.json` — sha256 `7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4`,
    git blob `48df844a22d74a57204f55a62e54760c7038c60f` (matches the contract pin `48df844a`).
  * `tools/fixtures/mori-job-runway/supplementary-cases.json` — sha256 `8d09756d10a9f501b0fa69599e096ce6ef5f3cd9debda89b5de2bc094679ffd6`.
* Mutated point in every case: `tools/mori-job-runway.py:408-412` (`_binary_sites`, the
  `len(set(numbers)) != 1` branch) and `tools/mori-job-runway.py:445-452` (`_effective`).
* One mutant at a time; each applied with a single-line `edit`, run, then reverted with
  `git checkout -- tools/mori-job-runway.py` inside the clone and re-verified by sha256.

Baseline (pristine) runs in the clone:

```
$ python3 -I -B tools/mori-job-runway.py --selftest
MORI_JOB_RUNWAY_SELFTEST: PASS 21/21                       exit=0
$ python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json
MORI_JOB_RUNWAY_SELFTEST: PASS 18/18                       exit=0
```

Final state after all twelve mutants: `sha256sum` back to
`5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`, `git status --short` empty,
pristine re-run `PASS 21/21` and `PASS 18/18`.

Detectors used: **D1** = `--selftest` (frozen 21), **D2** = `--selftest --cases
tools/fixtures/mori-job-runway/supplementary-cases.json` (18), **D3** = the scratch killer file
`/tmp/ambiguity-killer-cases.json` (4 cases KA/KB/KC/KD, written by me, not committed) used only
to name the input that kills a survivor. D3 passes 4/4 on the pristine tool, so its expectations
are contract-correct.

Live reference run (pristine, this host): `configured set 200` (the operator's OMP settings file,
`async:` / `  maxJobs: 200`), `clamp found 100 sites 1`, `setting_default found 100 sites 1`,
`effective 100`, `verdict RUNWAY_CLAMPED`, exit 1. Byte search of `~/.local/bin/omp`
(256,702,432 bytes) with the tool's own two patterns: exactly **one** clamp site (`100`) and
exactly **one** `async.maxJobs` default site (`100`).

## Result table

| # | Mutant | D1 frozen 21 | D2 supplementary 18 | D3 killer (scratch) | Live run |
|---|---|---|---|---|---|
| M1 | ambiguous → **first** match (both patterns) | **killed** — J10, J21 | survived | – | identical to baseline |
| M2 | ambiguous → **max** match (both patterns) | **killed** — J10, J21 | survived | – | identical to baseline |
| M3 | **ignore `setting_default` ambiguity** → first match | **killed** — J21 | survived | – | identical to baseline |
| M4 | ignore `clamp` ambiguity → max match | **killed** — J10 | survived | – | identical to baseline |
| M5 | ambiguous keeps a leaked value (`"ambiguous", numbers[0], …`) | **killed** — J10, J21 | survived | – | identical to baseline |
| M6 | ambiguity judged from the **first two** sites only | **survived** | **survived** | killed — KA, KC | identical to baseline |
| M7 | ambiguity judged from the **last two** sites only | **survived** | **survived** | killed — KB | identical to baseline |
| M8 | ambiguous state reports `sites: 0` | **survived** | **survived** | killed — KA, KB, KC | identical to baseline |
| M9 | `setting_default` ambiguity read as `absent` | **killed** — J21 | survived | killed — KC | identical to baseline |
| M10 | `clamp` ambiguity read as `absent` | **killed** — J10 | survived | killed — KA, KB | identical to baseline |
| M11 | ambiguous default **ignored in `_effective`** → base falls back to the clamp value | **survived** | **survived** | killed — KD | identical to baseline |
| M12 | ambiguous clamp not treated as absent in `_effective` (`clamp_value` stays `None`) | **killed** — J10 (traceback, exit 1) | survived | killed — KA, KB | identical to baseline |

"identical to baseline" = the live JSON (`clamp found 100 sites 1`, `setting_default found 100 sites 1`,
`effective 100`, `RUNWAY_CLAMPED`, exit 1) was byte-identical to the pristine live run. This is
expected: the installed binary carries exactly one site of each pattern, so every ambiguity branch
is dead on this host.

## Mutant detail (verbatim detector output)

### M1 — ambiguous → first match (both patterns) — KILLED

```diff
     if len(set(numbers)) != 1:
-        return "ambiguous", None, len(numbers)
+        return "found", numbers[0], len(numbers)
```

D1: `MORI_JOB_RUNWAY_SELFTEST: FAIL 19/21`, exit 2

```
CASE J10: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_CLAMPED'; exit: expected 2, got 1; clamp.state: expected 'ambiguous', got 'found'; clamp.value: expected None, got 100; effective: expected None, got 100
CASE J21: setting_default.state: expected 'ambiguous', got 'found'; setting_default.value: expected None, got 100
```

D2: `PASS 18/18` (exit 0). The supplementary file has no ambiguous case at all.

### M2 — ambiguous → max match (both patterns) — KILLED

```diff
     if len(set(numbers)) != 1:
-        return "ambiguous", None, len(numbers)
+        return "found", max(numbers), len(numbers)
```

D1: `FAIL 19/21`, exit 2 — same two failing cases J10 and J21 as M1 (J10's sites are 100 and 64,
so `max` and `first` coincide at 100; the kill comes from the state field, not the value).
D2: `PASS 18/18`.

### M3 — ignore `setting_default` ambiguity (take the first match) — KILLED

```diff
     if len(set(numbers)) != 1:
-        return "ambiguous", None, len(numbers)
+        if pattern is DEFAULT_RE:
+            return "found", numbers[0], len(numbers)
+        return "ambiguous", None, len(numbers)
```

D1: `FAIL 20/21`, exit 2 — `CASE J21: setting_default.state: expected 'ambiguous', got 'found'; setting_default.value: expected None, got 100`.
Note J21's `effective`/`verdict` are unchanged (configured is `set`, so the default is not consulted);
the kill comes only from the `setting_default` state/value fields. D2: `PASS 18/18`.

### M4 — ignore `clamp` ambiguity (take the max match) — KILLED

```diff
     if len(set(numbers)) != 1:
-        return "ambiguous", None, len(numbers)
+        if pattern is CLAMP_RE:
+            return "found", max(numbers), len(numbers)
+        return "ambiguous", None, len(numbers)
```

D1: `FAIL 20/21`, exit 2 — `CASE J10: verdict: expected 'RUNWAY_UNKNOWN', got 'RUNWAY_CLAMPED'; exit: expected 2, got 1; clamp.state: expected 'ambiguous', got 'found'; clamp.value: expected None, got 100; effective: expected None, got 100`.
D2: `PASS 18/18`.

### M5 — ambiguous state leaks a value — KILLED

```diff
     if len(set(numbers)) != 1:
-        return "ambiguous", None, len(numbers)
+        return "ambiguous", numbers[0], len(numbers)
```

D1: `FAIL 19/21`, exit 2 — `CASE J10: clamp.value: expected None, got 100` and
`CASE J21: setting_default.value: expected None, got 100` (state and verdict still correct).
D2: `PASS 18/18`.

### M6 — ambiguity judged from the first two sites only — **SURVIVED**

```diff
     if len(set(numbers)) != 1:
-        return "ambiguous", None, len(numbers)
+    if len(set(numbers[:2])) != 1:
+        return "ambiguous", None, len(numbers)
```

D1: `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` exit 0. D2: `PASS 18/18` exit 0. Live run identical to
baseline. **The whole frozen suite passes while the tool can now report a hard number for a binary
whose clamp sites disagree.**

Killer input (D3, case KA): a binary with three clamp sites whose first two agree and the third
differs — `Math.min(100, XPe.get(R))`, `Math.min(100, YPe.get(S))`, `Math.min(64, Abc.get(T))`.
Pristine: `clamp {ambiguous, null, sites 3}`, `effective null`, `RUNWAY_UNKNOWN`, exit 2.
Mutant: `clamp {found, 100, sites 3}`, `effective 100`, `RUNWAY_CLAMPED`, exit 1 — a false cap.
Case KC does the same for `setting_default` (three defaults 100, 100, 50).

### M7 — ambiguity judged from the last two sites only — **SURVIVED**

```diff
     if len(set(numbers)) != 1:
-        return "ambiguous", None, len(numbers)
+    if len(set(numbers[-2:])) != 1:
+        return "ambiguous", None, len(numbers)
```

D1: `PASS 21/21`. D2: `PASS 18/18`. Live run identical to baseline.

Killer input (D3, case KB): three clamp sites whose first differs and the last two agree —
`Math.min(64, XPe.get(R))`, `Math.min(100, YPe.get(S))`, `Math.min(100, Abc.get(T))`.
Pristine: `clamp {ambiguous, null, sites 3}`, `effective null`, `RUNWAY_UNKNOWN`, exit 2.
Mutant: `clamp {found, 64, sites 3}`, `effective 64`, `RUNWAY_CLAMPED`, exit 1 — worse than M6,
because the state is decided from the tail while the reported value is still `numbers[0]`: the
mutant reports "found" with a value that its own ambiguity test never looked at.

### M8 — ambiguous state reports `sites: 0` — **SURVIVED**

```diff
     if len(set(numbers)) != 1:
-        return "ambiguous", None, len(numbers)
+        return "ambiguous", None, 0
```

D1: `PASS 21/21`. D2: `PASS 18/18`. Live run identical to baseline.

Killer input (D3): any ambiguous case that pins `sites` (`"clamp": {"state": "ambiguous", "value": null, "sites": 3}`)
— KA, KB and KC all fail under the mutant (`clamp.sites: expected 3, got 0`). The verdict and the
effective value are untouched, so the only loss is the count of matching sites.

### M9 — `setting_default` ambiguity read as `absent` — KILLED

```diff
     if len(set(numbers)) != 1:
-        return "ambiguous", None, len(numbers)
+        if pattern is DEFAULT_RE:
+            return "absent", None, len(numbers)
+        return "ambiguous", None, len(numbers)
```

D1: `FAIL 20/21`, exit 2 — `CASE J21: setting_default.state: expected 'ambiguous', got 'absent'`.
D2: `PASS 18/18`. D3: killed by KC.

### M10 — `clamp` ambiguity read as `absent` — KILLED

```diff
     if len(set(numbers)) != 1:
-        return "ambiguous", None, len(numbers)
+        if pattern is CLAMP_RE:
+            return "absent", None, len(numbers)
+        return "ambiguous", None, len(numbers)
```

D1: `FAIL 20/21`, exit 2 — `CASE J10: clamp.state: expected 'ambiguous', got 'absent'`.
D2: `PASS 18/18`. D3: killed by KA and KB.

### M11 — ambiguous default ignored in `_effective` (base falls back to the clamp value) — **SURVIVED**

```diff
     elif configured_state_name == "absent" and default_state_name == "found":
-        base = default_value
+    elif configured_state_name == "absent" and default_state_name in ("found", "ambiguous"):
+        base = default_value if default_value is not None else clamp_value
```

D1: `PASS 21/21` exit 0. D2: `PASS 18/18` exit 0. Live run identical to baseline.

Killer input (D3, case KD): **no config file at all** (so `configured` is `absent`) and a binary
carrying two `async.maxJobs` defaults (100 and 50) plus one clamp site (100).
Pristine: `setting_default {ambiguous, null, sites 2}`, `effective null`, `RUNWAY_UNKNOWN`, exit 2.
Mutant: `effective 100`, `verdict RUNWAY_DEFAULT`, **exit 0** — the tool states a default cap the
binary does not determine. This is precisely the failure amendment A2 forbids ("`RUNWAY_UNKNOWN` is
never a false number"); the frozen suite does not notice it, because J21 (the only ambiguous-default
case) has `configured` = `set`, so `_effective` never consults the default there.

### M12 — ambiguous clamp not treated as absent in `_effective` — KILLED

```diff
-    if clamp_state_name != "found" or clamp_value is None:
+    if clamp_state_name == "absent":
         return None
```

D1: the frozen selftest **crashes** — no PASS line, traceback
`TypeError: '<' not supported between instances of 'int' and 'NoneType'` at
`tools/mori-job-runway.py:455` (`max(1, min(clamp_value, base))`), exit 1 → killed by J10.
D2: `PASS 18/18` (no ambiguous clamp in the supplementary file, so the crash never fires there).

## Findings, severity, and the smallest fix

### F1 — high: the frozen suite does not detect "ignore the ambiguous default" (M11)

`tools/mori-job-runway.py:445-452` can be weakened so that an ambiguous `setting_default` is
ignored and the tool reports `effective 100` / `RUNWAY_DEFAULT` / exit 0, and **both committed
suites still print PASS**. The contract (rule 4) requires `effective` to be null unless the default
is `found`, and A2 states that an abstention is always the safe direction. The landed bytes are
correct; the detector is not.

* Smallest fix (cases, not the tool): add one case to `tools/fixtures/mori-job-runway/supplementary-cases.json`
  (the co-evolved file; the frozen 21 blob `48df844a` is pinned and must not change) with
  `config: null`, a binary carrying two `async.maxJobs` defaults (100 and 50) and one clamp site
  (100), and `expect` `{"verdict": "RUNWAY_UNKNOWN", "exit": 2, "effective": null,
  "setting_default": {"state": "ambiguous", "value": null, "sites": 2}}`. That is my case KD and it
  kills M11.

### F2 — medium: the frozen suite does not detect an ambiguity test that looks at a subset of the sites (M6, M7)

`len(set(numbers)) != 1` can become `len(set(numbers[:2])) != 1` or `len(set(numbers[-2:])) != 1`
and the whole frozen 21 still passes, while the tool can report a hard cap for a binary whose
clamp sites disagree. Rule 2 says "**every** match … all matches carry the same number".

* Smallest fix: two cases in the supplementary file — three clamp sites `100, 100, 64` and three
  clamp sites `64, 100, 100`, each expecting `clamp {ambiguous, null, sites 3}`, `effective null`,
  `RUNWAY_UNKNOWN`, exit 2 (my cases KA and KB). The same shape on the default side (three defaults
  `100, 100, 50`) covers the `setting_default` branch (my case KC).

### F3 — low: the `sites` value of an ambiguous state is pinned by no case (M8)

No case asserts `sites` in the ambiguous state, so a mutant that reports `sites: 0` (and hides how
many sites matched) passes everything. The contract letter only ties `sites` to the `found` state,
so this is an unpinned observable rather than a contract violation; the verdict and the effective
value are unaffected.

* Smallest fix: in the same two or three new supplementary cases, include `"sites": 3` inside the
  `clamp` / `setting_default` expectation, which kills M8 at no extra case cost.

### F4 — medium: the supplementary 18 cases add no detection power on the ambiguity axis

Every one of the 18 supplementary cases expects `clamp {found, …, sites 1}` and
`setting_default {found, 100}`; none of them is ambiguous. Consequently **every** mutant in this
report — M1 through M12, killed or survived — passes the supplementary suite (M12 crashes it only
because the frozen run crashed first, not because the supplementary cases exercised it). The
supplementary file as landed covers the A2 config-abstention forms only.

* Smallest fix: the three or four cases named in F1–F3, added to
  `tools/fixtures/mori-job-runway/supplementary-cases.json`.

## Does omp's real behaviour make the survivors matter?

Not today, and the gap is therefore a coverage finding rather than a falsified claim.

* The installed binary `/home/vgpnk/.local/bin/omp` (256,702,432 bytes) carries **one** clamp site
  (`maxRunningJobs: () => Math.min(100, XPe.get(R))`) and **one** `async.maxJobs` default site
  (`default: 100`) — measured with the tool's own two byte patterns. With one site per pattern the
  ambiguous branch cannot be entered, so M1–M12 leave the live answer untouched
  (`configured set 200` → `effective 100` → `RUNWAY_CLAMPED`, exit 1) on this host. Verified by
  running the live survey under every mutant: identical output in all twelve runs.
* The survivors become live as soon as the binary grows a second site of either pattern — for
  example a second job-manager construction site, or the `async.maxJobs` setting being registered
  twice (exactly what frozen case J21 models: two `async.maxJobs` definitions with defaults 100
  and 50). Then M6/M7 would report a hard number for a cap that is not determined, and M11 would
  report `RUNWAY_DEFAULT`/exit 0 with an effective value derived from the clamp rather than from
  an undetermined default.
* I did not run omp (lane bound), so I make no claim about which value omp would actually use in
  the multi-site case; the contract's requirement is to abstain, and the mutants that survive
  remove that abstention.

## What the claim needs

Nothing in the landed bytes needs to change: `tools/mori-job-runway.py` at blob `239dd8eb`
implements rules 2–4 as written, and every mutant I made was reverted (final sha256
`5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`, `git status` clean, pristine
re-run `PASS 21/21` and `PASS 18/18`). The after-value `PASS 21/21` should not be read as
certifying the ambiguity abstention; four mutants of the ambiguity axis pass it, one of them
producing a false number. Adding the cases named in F1–F3 to the supplementary file (which the
contract explicitly leaves out of the counted after-value) closes the gap without touching the
frozen 21.

## Reproduction

```
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r25/w2-MutRunwayAmbiguity
cd /fast/scratch/hyaku/mori-r25/w2-MutRunwayAmbiguity
python3 -I -B tools/mori-job-runway.py --selftest
python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json
# apply one mutant at tools/mori-job-runway.py:410-411 (or :449-450), then:
python3 -I -B tools/mori-job-runway.py --selftest
python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json
python3 -I -B tools/mori-job-runway.py --selftest --cases /tmp/ambiguity-killer-cases.json   # scratch, mine
git checkout -- tools/mori-job-runway.py && sha256sum tools/mori-job-runway.py
```

Tooling: no installs were needed (Python 3 standard library only, `git`, `sha256sum`); the lane
was not modified.
