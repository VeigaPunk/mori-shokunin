# Mo60MutationTester32 — count-c2.py arm mutants, one wave-1 probe

Scope: mutate four behavior-bearing points of the frozen C2 counter in scratch
copies only, run the same bounded detectors on pristine / mutant bytes, and
report killed / survived / inconclusive with restoration evidence.

Lane `mori-shokunin` read-only. Freeze revision
`ac496c7cde8cad965079858accae3bedfe4a73f2`; entering revision
`ddfb12fb0838b4307c445194a844f0c4b1950195`; lane tip during the probe
`b3c256138f00c704d5aa56eb0332d74506502ef2` (C1 data landed at `398d3225`,
`b3c25613` after the freeze — every re-derivation below is pinned to a named
revision and read through `git show` / `git archive`, never the working tree).

Frozen bytes and pins verified before any probe:

```
sha256(.ufo/waves/round-60/count-c2.py) = 8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976  == PIN_C2 (count-c3.py:52)
sha256(.ufo/waves/round-60/count-c1.py) = 795c1f3193a76406a40561ac60fedb3eee75fc38df2b2efb3fc5295d617ddbae
sha256(tools/mori-entry-claims-check.py) = cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69
```

Baseline (pristine counter, lane repo, read-only, `--scratch` under
`/fast/scratch/hyaku/mori-r60/Mo60MutationTester32`):

```
$ python3 .ufo/waves/round-60/count-c2.py ac496c7c... --repo . --scratch .../base-freeze
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=ac496c7c...
exit=0
$ python3 .ufo/waves/round-60/count-c2.py b3c25613... --repo . --scratch .../base-tip
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=b3c25613...
exit=0
```

Disk guard green at start (`/fast/scratch/hyaku` 26% used, 600.0G free).

## Mutants (scratch copies, minimal byte spans)

Produced by `driver.py` with an exact-substring patcher that aborts unless the
anchor matches exactly once. Diffs are `diff -u pristine mutant`.

| id | mutation (counter lines at 8c4814f5…) | pristine sha → mutant sha |
|----|---------------------------------------|---------------------------|
| M1 `m1-drop-r54-control` | `:270` `drift_ok = attributed and ctrl` → `drift_ok = attributed` (renamed r54 control dropped) | `8c4814f5…df976` → `579cd353587cc20084c395f32e09dd0ac799c970c6b6fa0cef4f554e72aa8d65` |
| M2 `m2-any-nonzero-drift-exit` | `:249-252` five-line `attributed = (ran and … verdict==SETTLEMENT_SCAN_FAIL and any(DRIFT_REASON …))` → `attributed = (ran and p.returncode != 0)` | `8c4814f5…df976` → `0b1149d041709c2514a8a89d32b733d1543d98fc4d3e027010917fd4072c0bfd` |
| M3 `m3-skip-expect-equality` | `:363-366` committed-`expect.txt`-vs-frozen-table block deleted | `8c4814f5…df976` → `718def4282d71ecef9f4ae5622d004bcd625c4bb31aedd1e6858977dd961fbc7` |
| M4 `m4-skip-spans-eq-claims` | `:332` `and st.get("spans",0) == st.get("claims",0)` conjunct removed from `entry_ok` | `8c4814f5…df976` → `3dacba60f6dac38db10e76b975e26ccb7bcaa5a7c66d393a170b64537a4088dc` |

## Detector fixture

Throwaway repo at `/fast/scratch/hyaku/mori-r60/Mo60MutationTester32/fx/lane`,
built from the lane subset the counter reads (135 entries, 3.8 MB: the two
tools, entry + registry, six ARTIFACT copies, five REAL_SCAN files, the r53
drift file, `trees-c2h/`), extracted with
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive ac496c7c… -- <subset>`
into an explicitly `git init`-ed dir whose `rev-parse --show-toplevel` is
asserted to be that dir; every later command is `git -C <that dir>`.
Base commit `f43e499c2859f958d187ddaa1ffe8e950aca82c0` reproduces the frozen
line byte-for-byte (modulo rev), so the fixture is a faithful stand-in.

Scenario commits (each a single-file change off base):

| scenario | rev | change |
|----------|-----|--------|
| s-base | `f43e499c…` | none |
| s-r54-corrupt | `a03e576c…` | `.ufo/waves/round-54/w1-results.json` ← `{"lane": "x"}` (breaks the r54 artifact used by both the scan arm and the `ctrl` control) |
| s-drift-wrong-reason | `b7ff9c78…` | `.ufo/waves/round-53/w1-results.json` ← `{"lane": "x"}` (scan FAIL without any `:extra_keys=` reason) |
| s-drift-not-json | `4c7f2fe1…` | r53 file ← `not json at all` (scan FAIL, reason `not_json`) |
| s-expect-tamper | `ab6030f1…` | `trees-c2h/h02-malformed-claim/expect.txt` ← `grammar\nTAMPERED-EXTRA\n` (G3 semantics) |
| s-entry-alias | `65670049…` | entry + one well-formed claim line `K15` re-quoting K1's exact bytes at the same `line:5` (H2 alias) |

Matrix = 6 scenarios × 5 counters (pristine + 4 mutants), 30 runs, each with
its own `--scratch` and `TMPDIR`; all runs exit 0/1 as tabulated.

## Kill table

`flip` = pristine and mutant outputs differ (verdict or arm token). Direction
in brackets. "committed" = whether a detector already committed in the lane
falsifies the mutant behaviorally (excluding the sha pin).

| mutant | detector fixture | pristine output | mutant output | flip | committed? | verdict |
|--------|------------------|-----------------|---------------|------|-----------|---------|
| M1 | s-r54-corrupt | `C2=unmet … scan=bad drift=bad … failed=drift,scan,tree,tree:…w1-results-r54.json` (exit 1) | `C2=unmet … scan=bad drift=ok …` — `drift` gone from `failed=` (exit 1) | **drift arm only** [bad→ok] | no (only tail-fixture) | **killed, weak** (arm-token; verdict never moves) |
| M2 | s-drift-wrong-reason | `C2=unmet … drift=bad … failed=drift` (exit 1) | `C2=met … drift=ok …` (exit 0) | drift arm **and** verdict [unmet→met] | no | **killed, strong** |
| M2 | s-drift-not-json | `C2=unmet … drift=bad … failed=drift` (exit 1) | `C2=met … drift=ok …` (exit 0) | drift arm **and** verdict | no | **killed, strong** (second detector) |
| M3 | s-expect-tamper | `C2=unmet … trees=bad … failed=expect_tamper:h02-malformed-claim,trees` (exit 1) | `C2=met … trees=ok …` (exit 0) | frozen tree h02 **and** verdict [unmet→met] | count-c3 G3 PoC (but gated by PIN_C2) | **killed, strong** |
| M4 | s-entry-alias | `C2=unmet … entry=bad … claims=14 spans=13 failed=entry` (exit 1) | identical line, exit 1 | none | no | **SURVIVED** (see finding) |
| all | s-base | `C2=met …` (exit 0) | identical `C2=met …` (exit 0) | none | — | silent on the frozen input (expected) |
| all | count-c3 structural gate | `count-c3 <rev> --repo <fixture with mutant count-c2>` | `C3=unmet … failed=count_c2_sha,g1_new_skipped,g1_old_skipped,g2_skipped,g3_skipped,r59_counter_absent` | yes | yes (count-c3.py:141-145) | **killed, structural** (sha pin) |

Rows not listed in the table (e.g. M1 on s-drift-*, M3 on s-drift-*, M4 on
every scenario) are byte-identical to pristine — the full 30-row matrix is in
the receipt below.

## Findings

1. **M4 survives: the `spans==claims` conjunct is unreachable-false.** The
   pinned tool's `ok` is `len(reasons)==0`
   (`tools/mori-entry-claims-check.py:239`), every claim whose copy is in
   `artifacts` contributes exactly one `(file,start,end)` key or a
   `distinct:dup_span` / `span:*` reason (`:146-171`), and `stats["spans"]` is
   simply `len(spans)` (`:170`). Therefore `ok==true ⟹ spans==claims`, so
   `entry_ok`'s `and st["spans"]==st["claims"]` can never differ from the
   tool's own verdict. Direct probe of the pinned tool on the alias input:

   ```
   [s-base]        exit=0 ok=True  stats={'claims':13,'files':6,'spans':13,'min_span':12} reasons=[]
   [s-entry-alias] exit=1 ok=False stats={'claims':14,'files':6,'spans':13,'min_span':12} reasons=['distinct:dup_span=K1=K15']
   ```

   The only input that separates `spans` from `claims` already forces
   `ok=false` and exit 1, which the mutant still rejects via
   `p.returncode==0 and out["ok"] is True`. No repo-reachable input flips this
   mutant; only count-c3's `PIN_C2` (`count-c3.py:52`, gate `:141-145`,
   `count_c2_sha`) falsifies it. Reported as a coverage finding, not a claim
   defect: the frozen predicate and the counter's output on every reachable
   input are unchanged.

2. **M1 cannot move the verdict.** `ctrl` re-scans `REAL_SCAN[0]`
   (`count-c2.py:254`) — the same bytes the scan arm already scans at `:195`.
   `ctrl==false ⟹ scan==bad`, so the dropped conjunct can only be observed on
   inputs where the scan arm is already failing; the flip is confined to the
   `drift=` token and `failed=` membership, and `C2=unmet` stays `C2=unmet`.
   Detected (weakly) by the r54-corrupt fixture; invisible to every committed
   receipt and to count-c2's own selftest.

3. **Committed detector coverage.** `count-c2.py --selftest` → `C2_SELFTEST
   pass=8 fail=0`; its eight checks are `frozen_trees`, `artifacts_map`,
   `real_scan`, `pins_hex` and four containment checks (`:426-443`). None
   exercises the drift-attribution, expect-equality or spans conjunct, so no
   committed test kills M1/M2/M3/M4 behaviorally; the only committed kill is
   the count-c3 sha pin, which is pre-emptive (it refuses to run the mutant at
   all), not a behavioral detection of the defect class.

4. Count-c3's G3 PoC does kill M3 at token level when the counter is allowed
   to run (`expect_tamper:h02-malformed-claim` present in pristine
   `failed=`, absent under M3), but that arm is skipped for any non-pinned
   count-c2 — confirmed by the pin probe for all four mutants.

## Receipts

Counters (pristine and mutants) and all fixtures live only under
`/fast/scratch/hyaku/mori-r60/Mo60MutationTester32` (`bin/`, `fx/`, `runs/`).

Full matrix (`driver.out`, 30 runs):

```
[s-base__c2-pristine]              exit=0 C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=f43e499c2859f958d187ddaa1ffe8e950aca82c0
[s-base__m1-drop-r54-control]      exit=0 C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13
[s-base__m2-any-nonzero-drift-exit] exit=0 C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13
[s-base__m3-skip-expect-equality]  exit=0 C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13
[s-base__m4-skip-spans-eq-claims]  exit=0 C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13
[s-drift-not-json__c2-pristine]    exit=1 C2=unmet ... drift=bad ... failed=drift
[s-drift-not-json__m1-...]         exit=1 C2=unmet ... drift=bad ... failed=drift
[s-drift-not-json__m2-...]         exit=0 C2=met ... drift=ok ...
[s-drift-not-json__m3-...]         exit=1 C2=unmet ... drift=bad ... failed=drift
[s-drift-not-json__m4-...]         exit=1 C2=unmet ... drift=bad ... failed=drift
[s-drift-wrong-reason__c2-pristine] exit=1 C2=unmet ... drift=bad ... failed=drift
[s-drift-wrong-reason__m1-...]     exit=1 C2=unmet ... drift=bad ... failed=drift
[s-drift-wrong-reason__m2-...]     exit=0 C2=met ... drift=ok ...
[s-drift-wrong-reason__m3-...]     exit=1 C2=unmet ... drift=bad ... failed=drift
[s-drift-wrong-reason__m4-...]     exit=1 C2=unmet ... drift=bad ... failed=drift
[s-entry-alias__c2-pristine]       exit=1 C2=unmet ... entry=bad ... claims=14 files=6 spans=13 failed=entry
[s-entry-alias__m1-...]            exit=1 (identical to pristine)
[s-entry-alias__m2-...]            exit=1 (identical to pristine)
[s-entry-alias__m3-...]            exit=1 (identical to pristine)
[s-entry-alias__m4-...]            exit=1 (identical to pristine)
[s-expect-tamper__c2-pristine]     exit=1 C2=unmet ... trees=bad ... failed=expect_tamper:h02-malformed-claim,trees
[s-expect-tamper__m1-...]          exit=1 C2=unmet ... trees=bad ... failed=expect_tamper:h02-malformed-claim,trees
[s-expect-tamper__m2-...]          exit=1 C2=unmet ... trees=bad ... failed=expect_tamper:h02-malformed-claim,trees
[s-expect-tamper__m3-...]          exit=0 C2=met ... trees=ok ...
[s-expect-tamper__m4-...]          exit=1 C2=unmet ... trees=bad ... failed=expect_tamper:h02-malformed-claim,trees
[s-r54-corrupt__c2-pristine]       exit=1 C2=unmet ... scan=bad drift=bad ... tree=bad ... failed=drift,scan,tree,tree:corpus/evidence/sources-r59/w1-results-r54.json
[s-r54-corrupt__m1-...]            exit=1 C2=unmet ... scan=bad drift=ok ... tree=bad ... failed=scan,tree,tree:corpus/evidence/sources-r59/w1-results-r54.json
[s-r54-corrupt__m2-...]            exit=1 C2=unmet ... scan=bad drift=bad ... (identical to pristine)
[s-r54-corrupt__m3-...]            exit=1 C2=unmet ... scan=bad drift=bad ... (identical to pristine)
[s-r54-corrupt__m4-...]            exit=1 C2=unmet ... scan=bad drift=bad ... (identical to pristine)
```

Pin probe (`pin-probe.out`, count-c3 against a fixture whose
`.ufo/waves/round-60/count-c2.py` is the mutant and `count-c1.py` is the
pinned c1):

```
[m1-drop-r54-control]       exit=1 C3=unmet toolgate=bad containment=bad expectgate=bad cases=0 rev=4b61246d... failed=count_c2_sha,g1_new_skipped,g1_old_skipped,g2_skipped,g3_skipped,r59_counter_absent
[m2-any-nonzero-drift-exit] exit=1 C3=unmet ... failed=count_c2_sha,...  rev=2a2fcbea...
[m3-skip-expect-equality]   exit=1 C3=unmet ... failed=count_c2_sha,...  rev=66cbb606...
[m4-skip-spans-eq-claims]   exit=1 C3=unmet ... failed=count_c2_sha,...  rev=b4901720...
```

Entry-arm probe (`entry-probe.out`, pinned tool run verbatim on materialized
roots): see finding 1.

Restoration:

```
before: sha256(.ufo/waves/round-60/count-c2.py) = 8c4814f5…df976   (writing tree, read-only use)
after : sha256(.ufo/waves/round-60/count-c2.py) = 8c4814f5…df976
after : sha256(.ufo/waves/round-60/trees-c2h/h02-malformed-claim/expect.txt) = 2be265b0eee38add45e54d3fdbf23363e427d735843e94552852f219e415ff26
after : git status --porcelain .ufo/waves/round-60/count-c2.py .ufo/waves/round-60/count-c3.py tools/  → (empty)
```

No lane production file, corpus registry, SCORECARD, LOG or VCS state was
modified; the four mutants and every fixture commit exist only in the scratch
tree, which is removed before yield. No commits, no VCS mutation, no fleet or
sibling writes.
