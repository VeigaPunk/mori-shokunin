# SurvivorReplay — round-25 wave 1: replay of the six round-24 pressure survivors

Seat: `MoriR25.SurvivorReplay` (leaf mutation tester; no subagents dispatched).
Date: 2026-10-22. Sandbox: `/fast/scratch/hyaku/mori-r25/wt-survivors`
(`git clone --no-hardlinks` of the lane; branch `r25-wt-survivors`; own `.git` directory —
`git rev-parse --absolute-git-dir` = `/fast/scratch/hyaku/mori-r25/wt-survivors/.git`, distinct
from the lane's `/home/vgpnk/Projects/shokunin/mori-shokunin/.git`).

**Lane bounds.** The only file this seat wrote in the lane is this report
(`.ufo/waves/round-25/w1/SurvivorReplay.md`). No `git add`/`commit`/`stash`/`checkout`/`switch`/
`reset`/`pull`/`push` ran in `/home/vgpnk/Projects/shokunin/mori-shokunin`; no mutating `jj`
command ran at the fleet root. All mutation happened in the sandbox clone; the frozen
`tools/fixtures/mori-pressure/cases.json` was never edited (blob
`aeb80ea080436cb344df8dba7ec19eeecc639e347ae87a14bc6835631f28ca94` before and after).

---

## 1. The six survivors, identified

From `.ufo/waves/round-24/w2/` (lane, read-only):

| # | Mutant | Round-24 report | Mutation site at the tip |
|---|---|---|---|
| 1 | threshold edge (`>=` → `>`) | `MutPsiThresholdEdge.md` | `tools/mori-pressure.py:302` `if avg10 >= warn_avg10 and …` |
| 2 | matcher ignoring `findings_include` | `MutPsiMatcher.md` | `tools/mori-pressure.py:498` `if not any(f.get("id") == fid and f.get("resource") == resource …):` |
| 3 | grammar: extra trailing field accepted | `MutPsiGrammar.md` mutant A | `tools/mori-pressure.py:123` `LINE_RE` `total=([0-9]+)$` |
| 4 | grammar: duplicate kinds accepted | `MutPsiGrammar.md` mutant B | `tools/mori-pressure.py:180-182` the `if kind in kinds:` guard |
| 5 | grammar: negative total accepted | `MutPsiGrammar.md` mutant C | `tools/mori-pressure.py:123` `LINE_RE` `total=([0-9]+)$` → `(-?[0-9]+)` |
| 6 | PARTIAL outranking HIGH | `MutPsiVerdictOrder.md` | `tools/mori-pressure.py:345-348` the `elif findings:` / `elif any(s != STATE_OK …)` order |

`MutPsiGrammar.md` §"Mutants (each applied alone to the clone, smallest single-point change)"
gives exactly three grammar shapes (A extra fields, B duplicate kinds, C negative total), so
the six are: threshold edge, matcher, three grammar shapes, PARTIAL-over-HIGH.

## 2. Baseline at the tip

Tip `7634be75c74891b5cd2815d0bd5374f89abd7087` ("round-25: declare claims and contract; freeze
the 21 C2 runway cases before any tool"). Tool bytes
`tools/mori-pressure.py` sha256 `2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7`.

Two detectors exist at this tip:

- **D-frozen** — `python3 -I -B tools/mori-pressure.py --selftest` → the 12 frozen cases
  `P01–P12` plus the matcher negative controls.
- **D-supp** — `python3 -I -B tools/mori-pressure.py --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json`
  → the co-evolved file `S01–S07` (7 cases at the tip).

Baseline, both green before any mutation:

```
$ python3 -I -B tools/mori-pressure.py --selftest
MORI_PRESSURE_SELFTEST: PASS 12/12
MATCHER: rejected 48/48 corrupted expectations
exit=0

$ python3 -I -B tools/mori-pressure.py --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json
MORI_PRESSURE_SELFTEST: PASS 7/7
MATCHER: rejected 28/28 corrupted expectations
exit=0
```

**Structural fact, load-bearing for the rest of this report.** `_cases_path()`
(`tools/mori-pressure.py:404-413`) resolves only `fixtures/mori-pressure/cases.json`. The
supplementary file is **opt-in** and is reached only through `--cases`. No committed script,
CI file or tool in the lane runs `--cases` (grep for `supplementary-cases` over `*.sh`, `*.py`,
`*.yml`, `*.yaml`, `*.toml` outside `.ufo/` returns nothing; `tools/mori-census.sh` does not
mention `mori-pressure`). So the supplementary suite is a *separate* corpus, not part of the
declared after-value `MORI_PRESSURE_SELFTEST: PASS 12/12`, and nothing in the lane executes it
automatically.

## 3. Replay of the six — one at a time, pristine → mutated → restored

Each mutant was applied alone in the sandbox, both detectors were run, then the file was
restored with `git checkout -- tools/mori-pressure.py` (clone-local) and the restored sha256 was
compared byte-for-byte against the pristine hash.

| # | Mutant | Mutated sha256 | D-frozen | D-supp | Verdict | Failing line |
|---|---|---|---|---|---|---|
| 1 | threshold edge `>=`→`>` | `ba2f725ca8c350b18812db8bcbe261c017cc598158904dbccd43fa9bac44bd42` | PASS 12/12 | **FAIL 6/7** | **KILLED** | `S01: exit 0 != 1; verdict PRESSURE_OK != PRESSURE_HIGH; finding PRESSURE_HIGH on memory missing` |
| 2 | matcher ignores `findings_include` | `031d0c4b673e060f9157067b97216bf6e8df7410a655bbf360a10c9931cceb9d` | **FAIL 12/12** | **FAIL 7/7** | **KILLED** | `MATCHER: accepted 12 of 48 corrupted expectations: P01/finding, … P12/finding` / `MATCHER: accepted 7 of 28 corrupted expectations: S01/finding, … S07/finding` |
| 3 | grammar extra fields | `db3d384afb98172875c905d90d8593992e709ffd9a4910057839e56bcdbe8dbc` | PASS 12/12 | **FAIL 6/7** | **KILLED** | `S02: verdict PRESSURE_OK != PRESSURE_PARTIAL; io.state is 'ok', expected 'malformed'` |
| 4 | grammar duplicate kinds | `85676cb0cd768795ab139e90281484b6b1f44f2c783547375a4dec859e96cbfa` | PASS 12/12 | **FAIL 6/7** | **KILLED** | `S03: verdict PRESSURE_OK != PRESSURE_PARTIAL; memory.state is 'ok', expected 'malformed'` |
| 5 | grammar negative total | `afab17a81acda57bd43724f5b7e4cd3c7eadc5b928c4df8ea19ac663394ccd21` | PASS 12/12 | **FAIL 6/7** | **KILLED** | `S04: verdict PRESSURE_OK != PRESSURE_PARTIAL; cpu.state is 'ok', expected 'malformed'` |
| 6 | PARTIAL outranking HIGH | `4276fef4fea24be13113fcccb9fad2b6853c3828ef15c77846eb7d7f0283d4d0` | PASS 12/12 | **FAIL 5/7** | **KILLED** | `S05: exit 0 != 1; verdict PRESSURE_PARTIAL != PRESSURE_HIGH` and `S07: exit 0 != 1; verdict PRESSURE_PARTIAL != PRESSURE_HIGH` |

**All six are killed at the tip.** No mutant survived; no baseline failure was observed, so every
red is a genuine kill and no result is inconclusive. The killers are the tip's own artifacts:
`S01` (threshold edge), `S02`/`S03`/`S04` (the three grammar shapes), `S05`+`S07` (verdict
precedence), and the matcher negative controls (mutant 2 — the tip's `_corrupted_expectations`
adds a bogus `["PRESSURE_HIGH", "absent-resource"]` pair to each passing case, which the weakened
matcher accepts).

Restoration evidence, identical for all six: after `git checkout -- tools/mori-pressure.py` the
file hash was `2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7` — byte-identical
to the pristine baseline — and both detectors returned to PASS. The harness asserts this equality
on every run and aborts on mismatch.

### Coverage note the L1 needs

Mutants 1 and 3–6 still pass the **frozen 12 alone** (`PASS 12/12`); only mutant 2 is caught by
the frozen corpus, and only through the matcher controls. The frozen 12 therefore remain blind to
the threshold edge and the three grammar shapes and to the verdict precedence. Since
`supplementary-cases.json` is opt-in and no committed runner invokes it, **the six survivors are
killed only by a corpus that the lane does not execute on its own.** This is a coverage finding,
not a contract change: the round-24 lesson (`corpus/lessons/round-24.md:75-81`) already describes
the supplementary file as the response to these survivors, so the behaviour is intended; what is
missing is that nothing runs it.

## 4. Still-surviving mutants in the same six families

Since the six named mutants are already killed, I probed the *same six families* for neighbouring
mutations that survive **both** detectors at the tip. Nine survived; each is a real behaviour
change of the tool, not a no-op (each was re-verified to change the parse/verdict output).

| Label | Mutation (single point at the tip) | Survived |
|---|---|---|
| trailing whitespace accepted | `line = raw.rstrip("\r")` → `raw.strip()` (`:174`) | both |
| leading whitespace accepted | `line = raw.rstrip("\r")` → `raw.lstrip(" ")` (`:174`) | both |
| fractional total accepted | `LINE_RE` `total=([0-9]+)$` → `total=([0-9]+(?:\.[0-9]+)?)$` (`:123`) | both |
| empty total accepted | `LINE_RE` `total=([0-9]+)$` → `total=([0-9]*)$` (`:123`) | both |
| unknown kind accepted | `LINE_RE` `^(some\|full)` → `^(some\|full\|stall)` (`:122`) | both |
| `--warn-avg10` ignored | `avg10 >= warn_avg10` → `avg10 >= 10.0` (`:302`) | both |
| required kind not enforced | `missing = [k for k in REQUIRED_KINDS[name] …]` → `missing = []` (`:189`) | D-frozen only |
| regressed counter not partial | `elif any(s != STATE_OK …)` → `any(s not in (STATE_OK, STATE_REGRESSED) …)` (`:347`) | D-supp only |
| system cpu full thresholded | `THRESHOLD_KINDS["cpu"] = ("some",)` → `("some", "full")` (`:78`) | D-supp only |

(Three of the nine — required kind, regressed counter, cpu-full threshold — were caught by the
other detector, but each is blind in one of the two corpora; all nine are blind to a lane that runs
only one corpus, which is the state of the lane today.)

## 5. New supplementary cases S08–S16 that kill them

Added to `tools/fixtures/mori-pressure/supplementary-cases.json` **in the sandbox**. The frozen
`cases.json` was not touched. The file was written so that `json.dumps(doc, indent=1)` reproduces
the bytes exactly (verified byte-identical round trip), preserving the existing format.

| Case | Shape | Kills |
|---|---|---|
| S08 | trailing space after `total` → io `malformed` | trailing whitespace accepted |
| S09 | leading space before the kind → memory `malformed` | leading whitespace accepted |
| S10 | fractional `total=654321.5` → io `malformed` | fractional total accepted |
| S11 | empty `total=` → memory `malformed` | empty total accepted |
| S12 | a `stall` line → io `malformed` | unknown kind accepted |
| S13 | `--warn-avg10 5.0`, memory some `avg10=7.00` → `PRESSURE_HIGH`, exit 1 | `--warn-avg10` ignored |
| S14 | io carries only `some` → io `malformed` | required kind not enforced |
| S15 | interval run, cpu some total 200000 → 100000, no finding → `PRESSURE_PARTIAL`, exit 0 | regressed counter not partial |
| S16 | cpu `full avg10=40.00` → `PRESSURE_OK`, exit 0 | system cpu full thresholded |

### Proof each new case kills its mutant

Each mutant was applied alone to `tools/mori-pressure.py` in the sandbox and the supplementary
suite was run; the named case must go red.

```
=== S08 trailing whitespace accepted -> KILLED by S08
    mutated sha256 c4f3cb69d91ca7ca6d5a04c9b874035b6450d45af72da8e27cbfa9e9cf5f4532
    MORI_PRESSURE_SELFTEST: FAIL 14/16
    S08: verdict PRESSURE_OK != PRESSURE_PARTIAL; io.state is 'ok', expected 'malformed'; …
    S09: verdict PRESSURE_OK != PRESSURE_PARTIAL; memory.state is 'ok', expected 'malformed'; …
    restored sha256 2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7 (== pristine: True)

=== S09 leading whitespace accepted -> KILLED by S09
    mutated sha256 b54c166f886ab726f6b4592dd1ceb10bca9c1f08a2418a413e0175ee7a5688d8
    MORI_PRESSURE_SELFTEST: FAIL 15/16
    S09: verdict PRESSURE_OK != PRESSURE_PARTIAL; memory.state is 'ok', expected 'malformed'; …
    restored sha256 2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7 (== pristine: True)

=== S10 fractional total accepted -> KILLED by S10
    mutated sha256 8bbf1cc311c4f2916e8b744b29b4e55e629d70d71f08b8c70742b75b57f1b037
    MORI_PRESSURE_SELFTEST: FAIL 15/16
    S10: interval validation failed: invalid literal for int() with base 10: '654321.5'
    restored sha256 2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7 (== pristine: True)

=== S11 empty total accepted -> KILLED by S11
    mutated sha256 e286ce291ab4adc9f26b22e8345da90932210e9c48c613ffb466a9692e0707ce
    MORI_PRESSURE_SELFTEST: FAIL 15/16
    S11: interval validation failed: invalid literal for int() with base 10: ''
    restored sha256 2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7 (== pristine: True)

=== S12 unknown kind accepted -> KILLED by S12
    mutated sha256 624228864ee910101e0396e05105164e05e4258fecf623d613988bd662431a78
    MORI_PRESSURE_SELFTEST: FAIL 15/16
    S12: verdict PRESSURE_OK != PRESSURE_PARTIAL; io.state is 'ok', expected 'malformed'; …
    restored sha256 2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7 (== pristine: True)

=== S13 --warn-avg10 ignored -> KILLED by S13
    mutated sha256 932af4eb672dcfc8340bba5281acc5c75f354f739a590d7ef916ae055ac24e07
    MORI_PRESSURE_SELFTEST: FAIL 15/16
    S13: exit 0 != 1; verdict PRESSURE_OK != PRESSURE_HIGH; finding PRESSURE_HIGH on memory missing
    restored sha256 2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7 (== pristine: True)

=== S14 required kind not enforced -> KILLED by S14
    mutated sha256 06062dde4be79ff030516cf43eb8bba6062906d6423dbdcf82b8c11a50597048
    MORI_PRESSURE_SELFTEST: FAIL 15/16
    S14: verdict PRESSURE_OK != PRESSURE_PARTIAL; io.state is 'ok', expected 'malformed'; …
    restored sha256 2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7 (== pristine: True)

=== S15 regressed counter not partial -> KILLED by S15
    mutated sha256 bcd3cac5af41513ceee37e01d4b73fa95e6efd07fea1e45c850e746690940d0b
    MORI_PRESSURE_SELFTEST: FAIL 15/16
    S15: verdict PRESSURE_OK != PRESSURE_PARTIAL
    restored sha256 2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7 (== pristine: True)

=== S16 system cpu full used for threshold -> KILLED by S16
    mutated sha256 41da3f55d0cd1ac1eb2255df81144fbad36fe4f7e102ff757361bb8672ac1552
    MORI_PRESSURE_SELFTEST: FAIL 15/16
    S16: exit 1 != 0; verdict PRESSURE_HIGH != PRESSURE_OK
    restored sha256 2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7 (== pristine: True)

=== unmutated frozen: rc=0 | MORI_PRESSURE_SELFTEST: PASS 12/12 | MATCHER: rejected 48/48 corrupted expectations
=== unmutated supplementary: rc=0 | MORI_PRESSURE_SELFTEST: PASS 16/16 | MATCHER: rejected 64/64 corrupted expectations

checks failed: 0
```

S10 and S11 fail through the matcher's `interval validation failed:` branch because the loosened
regex makes `int(match.group(5))` raise — a crash in the parse path, i.e. a genuine tool
behaviour change, not a fixture artefact. S08 also kills S09's mutant and vice versa (the
whitespace mutants are each other's witnesses), which is why S08's run shows S09 red too.

### The unmutated tool still passes

After all nine mutants were reverted (hash back to `2c815f84…` every time):

```
$ python3 -I -B tools/mori-pressure.py --selftest
MORI_PRESSURE_SELFTEST: PASS 12/12
MATCHER: rejected 48/48 corrupted expectations
exit=0

$ python3 -I -B tools/mori-pressure.py --selftest --cases tools/fixtures/mori-pressure/supplementary-cases.json
MORI_PRESSURE_SELFTEST: PASS 16/16
MATCHER: rejected 64/64 corrupted expectations
exit=0
```

The declared 12-case after-value is unchanged: the frozen corpus still prints `PASS 12/12` and its
blob is byte-identical (`aeb80ea080436cb344df8dba7ec19eeecc639e347ae87a14bc6835631f28ca94`).

## 6. Sandbox commit

```
$ git -C /fast/scratch/hyaku/mori-r25/wt-survivors add tools/fixtures/mori-pressure/supplementary-cases.json
$ git -C /fast/scratch/hyaku/mori-r25/wt-survivors commit -m "round-25 wave 1 (SurvivorReplay): nine supplementary pressure cases S08-S16 killing still-surviving round-24 mutants …"
$ git -C /fast/scratch/hyaku/mori-r25/wt-survivors log --oneline -3
e559c8e round-25 wave 1 (SurvivorReplay): nine supplementary pressure cases S08-S16 killing still-surviving round-24 mutants
7634be7 round-25: declare claims and contract; freeze the 21 C2 runway cases before any tool
28b79d3 round-24 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git -C /fast/scratch/hyaku/mori-r25/wt-survivors show --stat --oneline HEAD
e559c8e round-25 wave 1 (SurvivorReplay): nine supplementary pressure cases S08-S16 killing still-surviving round-24 mutants
 .../mori-pressure/supplementary-cases.json         | 268 ++++++++++++++++++++-
 1 file changed, 267 insertions(+), 1 deletion(-)
$ git -C /fast/scratch/hyaku/mori-r25/wt-survivors show --name-only --format="" HEAD
tools/fixtures/mori-pressure/supplementary-cases.json
$ git -C /fast/scratch/hyaku/mori-r25/wt-survivors status --porcelain
(empty)
```

The commit touches exactly one file. `tools/mori-pressure.py` and the frozen
`tools/fixtures/mori-pressure/cases.json` are byte-identical to the tip
(`2c815f84c6d7a51a040d95b62eac1d035dba5bcf32a5d942414ff33e3b2d29b7` and
`aeb80ea080436cb344df8dba7ec19eeecc639e347ae87a14bc6835631f28ca94` at `HEAD`).

### The diff

```diff
--- a/tools/fixtures/mori-pressure/supplementary-cases.json
+++ b/tools/fixtures/mori-pressure/supplementary-cases.json
@@ -1,6 +1,6 @@
  {
   "schema": "mori-pressure-cases-v1",
-  "note": "Supplementary cases written by the L1 after wave-2 mutation testing (survivors: threshold edge, grammar looseness, verdict precedence, EPERM). Co-evolved with the tool, not frozen before it; they do not change the declared 12-case after-value.",
+  "note": "Supplementary cases written by the L1 after wave-2 mutation testing (survivors: threshold edge, grammar looseness, verdict precedence, EPERM), then extended in round-25 wave 1 by the SurvivorReplay seat (S08-S16: grammar whitespace/fractional-total/empty-total/unknown-kind/required-kind shapes, the --warn-avg10 value, a regressed counter with no finding, and system cpu full never thresholded). Co-evolved with the tool, not frozen before it; they do not change the declared 12-case after-value.",
   "cases": [
@@ -219,6 +219,272 @@
+  },
+  {
+   "id": "S08",
+   "topic": "grammar: a trailing space after total is not the PSI grammar, so io is malformed",
+   "args": [],
+   "snapshots": [
+    {
+     "files": {
+      "cpu": "some avg10=1.23 avg60=0.45 avg300=0.12 total=98765\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
+      "memory": "some avg10=2.34 avg60=1.56 avg300=0.78 total=456789\nfull avg10=1.11 avg60=0.66 avg300=0.22 total=334455\n",
+      "io": "some avg10=3.21 avg60=2.43 avg300=1.09 total=654321 \nfull avg10=0.98 avg60=0.87 avg300=0.54 total=223344\n",
+      "irq": "full avg10=0.31 avg60=0.29 avg300=0.27 total=111222\n"
+     },
+     "errors": {}
+    }
+   ],
+   "expect": {
+    "exit": 0,
+    "verdict": "PRESSURE_PARTIAL",
+    "resources": {
+     "io": {
+      "state": "malformed",
+      "some": null,
+      "full": null
+     }
+    },
+    "findings_include": []
+   }
+  },
+  {
+   "id": "S09",
+   "topic": "grammar: a leading space before the kind is not the PSI grammar, so memory is malformed",
+   "args": [],
+   "snapshots": [
+    {
+     "files": {
+      "cpu": "some avg10=1.23 avg60=0.45 avg300=0.12 total=98765\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
+      "memory": " some avg10=2.34 avg60=1.56 avg300=0.78 total=456789\nfull avg10=1.11 avg60=0.66 avg300=0.22 total=334455\n",
+      "io": "some avg10=3.21 avg60=2.43 avg300=1.09 total=654321\nfull avg10=0.98 avg60=0.87 avg300=0.54 total=223344\n",
+      "irq": "full avg10=0.31 avg60=0.29 avg300=0.27 total=111222\n"
+     },
+     "errors": {}
+    }
+   ],
+   "expect": {
+    "exit": 0,
+    "verdict": "PRESSURE_PARTIAL",
+    "resources": {
+     "memory": {
+      "state": "malformed",
+      "some": null,
+      "full": null
+     }
+    },
+    "findings_include": []
+   }
+  },
+  {
+   "id": "S10",
+   "topic": "grammar: a fractional total is not a non-negative integer counter, so io is malformed",
+   "args": [],
+   "snapshots": [
+    {
+     "files": {
+      "cpu": "some avg10=1.23 avg60=0.45 avg300=0.12 total=98765\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
+      "memory": "some avg10=2.34 avg60=1.56 avg300=0.78 total=456789\nfull avg10=1.11 avg60=0.66 avg300=0.22 total=334455\n",
+      "io": "some avg10=3.21 avg60=2.43 avg300=1.09 total=654321.5\nfull avg10=0.98 avg60=0.87 avg300=0.54 total=223344\n",
+      "irq": "full avg10=0.31 avg60=0.29 avg300=0.27 total=111222\n"
+     },
+     "errors": {}
+    }
+   ],
+   "expect": {
+    "exit": 0,
+    "verdict": "PRESSURE_PARTIAL",
+    "resources": {
+     "io": {
+      "state": "malformed",
+      "some": null,
+      "full": null
+     }
+    },
+    "findings_include": []
+   }
+  },
+  {
+   "id": "S11",
+   "topic": "grammar: an empty total is not a non-negative integer counter, so memory is malformed",
+   "args": [],
+   "snapshots": [
+    {
+     "files": {
+      "cpu": "some avg10=1.23 avg60=0.45 avg300=0.12 total=98765\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
+      "memory": "some avg10=2.34 avg60=1.56 avg300=0.78 total=\nfull avg10=1.11 avg60=0.66 avg300=0.22 total=334455\n",
+      "io": "some avg10=3.21 avg60=2.43 avg300=1.09 total=654321\nfull avg10=0.98 avg60=0.87 avg300=0.54 total=223344\n",
+      "irq": "full avg10=0.31 avg60=0.29 avg300=0.27 total=111222\n"
+     },
+     "errors": {}
+    }
+   ],
+   "expect": {
+    "exit": 0,
+    "verdict": "PRESSURE_PARTIAL",
+    "resources": {
+     "memory": {
+      "state": "malformed",
+      "some": null,
+      "full": null
+     }
+    },
+    "findings_include": []
+   }
+  },
+  {
+   "id": "S12",
+   "topic": "grammar: only some and full are kinds, so a stall line makes io malformed",
+   "args": [],
+   "snapshots": [
+    {
+     "files": {
+      "cpu": "some avg10=1.23 avg60=0.45 avg300=0.12 total=98765\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
+      "memory": "some avg10=2.34 avg60=1.56 avg300=0.78 total=456789\nfull avg10=1.11 avg60=0.66 avg300=0.22 total=334455\n",
+      "io": "some avg10=3.21 avg60=2.43 avg300=1.09 total=654321\nfull avg10=0.98 avg60=0.87 avg300=0.54 total=223344\nstall avg10=1.00 avg60=1.00 avg300=1.00 total=1\n",
+      "irq": "full avg10=0.31 avg60=0.29 avg300=0.27 total=111222\n"
+     },
+     "errors": {}
+    }
+   ],
+   "expect": {
+    "exit": 0,
+    "verdict": "PRESSURE_PARTIAL",
+    "resources": {
+     "io": {
+      "state": "malformed",
+      "some": null,
+      "full": null
+     }
+    },
+    "findings_include": []
+   }
+  },
+  {
+   "id": "S13",
+   "topic": "threshold: --warn-avg10 5.0 is honoured, so memory some avg10 7.00 is PRESSURE_HIGH",
+   "args": [
+    "--warn-avg10",
+    "5.0"
+   ],
+   "snapshots": [
+    {
+     "files": {
+      "cpu": "some avg10=1.23 avg60=0.45 avg300=0.12 total=98765\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
+      "memory": "some avg10=7.00 avg60=3.50 avg300=1.75 total=456789\nfull avg10=1.11 avg60=0.66 avg300=0.22 total=334455\n",
+      "io": "some avg10=3.21 avg60=2.43 avg300=1.09 total=654321\nfull avg10=0.98 avg60=0.87 avg300=0.54 total=223344\n",
+      "irq": "full avg10=0.31 avg60=0.29 avg300=0.27 total=111222\n"
+     },
+     "errors": {}
+    }
+   ],
+   "expect": {
+    "exit": 1,
+    "verdict": "PRESSURE_HIGH",
+    "resources": {
+     "memory": {
+      "state": "ok"
+     }
+    },
+    "findings_include": [
+     [
+      "PRESSURE_HIGH",
+      "memory"
+     ]
+    ]
+   }
+  },
+  {
+   "id": "S14",
+   "topic": "grammar: a file missing its required kind is malformed, so io (some only) is malformed",
+   "args": [],
+   "snapshots": [
+    {
+     "files": {
+      "cpu": "some avg10=1.23 avg60=0.45 avg300=0.12 total=98765\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
+      "memory": "some avg10=2.34 avg60=1.56 avg300=0.78 total=456789\nfull avg10=1.11 avg60=0.66 avg300=0.22 total=334455\n",
+      "io": "some avg10=3.21 avg60=2.43 avg300=1.09 total=654321\n",
+      "irq": "full avg10=0.31 avg60=0.29 avg300=0.27 total=111222\n"
+     },
+     "errors": {}
+    }
+   ],
+   "expect": {
+    "exit": 0,
+    "verdict": "PRESSURE_PARTIAL",
+    "resources": {
+     "io": {
+      "state": "malformed",
+      "some": null,
+      "full": null
+     }
+    },
+    "findings_include": []
+   }
+  },
+  {
+   "id": "S15",
+   "topic": "verdict precedence: a regressed counter with no threshold finding is PRESSURE_PARTIAL, exit 0",
+   "args": [
+    "--interval",
+    "1"
+   ],
+   "snapshots": [
+    {
+     "files": {
+      "cpu": "some avg10=1.23 avg60=0.45 avg300=0.12 total=200000\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
+      "memory": "some avg10=2.34 avg60=1.56 avg300=0.78 total=456789\nfull avg10=1.11 avg60=0.66 avg300=0.22 total=334455\n",
+      "io": "some avg10=3.21 avg60=2.43 avg300=1.09 total=654321\nfull avg10=0.98 avg60=0.87 avg300=0.54 total=223344\n",
+      "irq": "full avg10=0.31 avg60=0.29 avg300=0.27 total=111222\n"
+     },
+     "errors": {}
+    },
+    {
+     "files": {
+      "cpu": "some avg10=1.23 avg60=0.45 avg300=0.12 total=100000\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n",
+      "memory": "some avg10=2.34 avg60=1.56 avg300=0.78 total=456789\nfull avg10=1.11 avg60=0.66 avg300=0.22 total=334455\n",
+      "io": "some avg10=3.21 avg60=2.43 avg300=1.09 total=654321\nfull avg10=0.98 avg60=0.87 avg300=0.54 total=223344\n",
+      "irq": "full avg10=0.31 avg60=0.29 avg300=0.27 total=111222\n"
+     },
+     "errors": {}
+    }
+   ],
+   "expect": {
+    "exit": 0,
+    "verdict": "PRESSURE_PARTIAL",
+    "resources": {
+     "cpu": {
+      "state": "counter_regressed"
+     }
+    },
+    "findings_include": []
+   }
+  },
+  {
+   "id": "S16",
+   "topic": "threshold: system cpu full is never used for a threshold, so cpu full avg10 40.00 stays PRESSURE_OK",
+   "args": [],
+   "snapshots": [
+    {
+     "files": {
+      "cpu": "some avg10=1.23 avg60=0.45 avg300=0.12 total=98765\nfull avg10=40.00 avg60=40.00 avg300=40.00 total=0\n",
+      "memory": "some avg10=2.34 avg60=1.56 avg300=0.78 total=456789\nfull avg10=1.11 avg60=0.66 avg300=0.22 total=334455\n",
+      "io": "some avg10=3.21 avg60=2.43 avg300=1.09 total=654321\nfull avg10=0.98 avg60=0.87 avg300=0.54 total=223344\n",
+      "irq": "full avg10=0.31 avg60=0.29 avg300=0.27 total=111222\n"
+     },
+     "errors": {}
+    }
+   ],
+   "expect": {
+    "exit": 0,
+    "verdict": "PRESSURE_OK",
+    "resources": {
+     "cpu": {
+      "state": "ok"
+     }
+    },
+    "findings_include": []
+   }
+  }
  ]
 }
```

Full diff also retrievable from the sandbox:
`git -C /fast/scratch/hyaku/mori-r25/wt-survivors show e559c8e -- tools/fixtures/mori-pressure/supplementary-cases.json`.

## 7. What the L1 needs to decide (not decided here)

1. **Nothing runs the supplementary corpus.** `_cases_path()` (`tools/mori-pressure.py:404-413`)
   resolves only `cases.json`; `supplementary-cases.json` is reachable only through `--cases`, and
   no committed script invokes it. Five of the six round-24 survivors are killed *only* by the
   supplementary corpus. Until some lane command runs `--cases …supplementary-cases.json`, the
   tool's coverage of the round-24 survivors rests on a corpus the lane never executes. This is a
   coverage finding; wiring a runner is the L1's call, not this seat's.
2. **The count claims elsewhere in the lane need the new number if this commit is landed.**
   `corpus/lessons/round-24.md:79-80` says the supplementary file is "S01–S06" with "`PASS 6/6`".
   Defect D3 was routed to seat `MoriR25.D3LessonCorrection`, and its correction line has since
   landed at `corpus/lessons/round-24.md:100`, reading "`PASS 7/7`" against the file at
   `4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e` (= 7 cases). `SCORECARD.md:1521` also says
   `PASS 7/7`. Landing S08–S16 changes the file's case count from 7 to 16 and the supplementary
   run from `PASS 7/7` to `PASS 16/16`, so the landed D3 correction line and `SCORECARD.md:1521`
   would need re-deriving against the new revision. My sandbox commit is **not** landed in the
   lane; the L1 owns that decision and the accompanying count corrections.
3. **D3's count predicate is revision-pinned, so it survives the change.** `contract.md:21`
   computes `n` from the file at `4f05dd5a…` (7 cases). Landing S08–S16 does not change `n` at
   that pinned revision, so the D3 predicate keeps its stated value; only the narrative count in
   the lesson's correction line and in the SCORECARD becomes stale. Flagged for the L1 and the
   D3 seat, not changed here.
4. **The lane tip moved during this seat's run** (from `7634be75…` to `cb51e846…` as sibling
   wave-1 work landed). This seat's replay and all committed bytes are against the dispatched
   base `7634be75c74891b5cd2815d0bd5374f89abd7087`. The structural findings above were re-checked
   against the new tip `cb51e846fd7acef10bfb75e83411c1045b296ef0` and still hold: `_cases_path()`
   is unchanged at `tools/mori-pressure.py:404-413` and still resolves only `cases.json`, and no
   committed script under `tools/` or `scripts/` invokes `--cases …supplementary-cases.json` for
   the pressure tool (the only `supplementary-cases` hit under `tools/` is a docstring mention
   inside `tools/mori-job-runway.py:60`, which is the C2 runway tool, not a runner).

## 8. Tooling

- Read `/home/vgpnk/.omp/agent/RULES.md` before acting. **No tool was installed or updated this
  session** — no pacman transaction (none was run; all pacman transactions are paused host-wide
  per the contract bounds), no `uv tool install`, no `npm -g`, no `cargo install`, no official
  binary download. Nothing in the task needed a new tool.
- Environment: system `python3` 3.14.8 (pre-existing), `git` 2.56.0 (pre-existing). Every
  detector run used `python3 -I -B` as the contract requires.
- Probes: two throwaway harnesses under `/fast/scratch/hyaku/mori-r25/probe-survivors/`
  (`probe.py`, `killcheck.py`) — outside the repo, so they are not in the commit. The only
  in-repo artefact this seat produced is `tools/fixtures/mori-pressure/supplementary-cases.json`
  (sandbox commit `e559c8e`).
- A `tools/__pycache__/` directory appeared in the sandbox during probing (importlib loading the
  tool module); it was removed before the commit, so `git status --porcelain` is empty. The
  lane repo was never touched.
- No `/proc`, `/sys`, cgroup, PSI or service interaction; no host writes outside the sandbox and
  this report.

Report: `.ufo/waves/round-25/w1/SurvivorReplay.md`
