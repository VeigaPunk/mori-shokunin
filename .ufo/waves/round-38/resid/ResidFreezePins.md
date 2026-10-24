# ResidFreezePins — round 38 residual review

## Scope and axes

Reviewed committed bytes at `b6993744171a05efc627b5e0664489c31aa5214e`, not the mutable lane worktree. Axes: freeze integrity; predicate identity; calibration/operability/depth claim correspondence; timing-evidence provenance. Detection and report only; no admission judgment or remediation.

The required command `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse mori` exited 128: `fatal: ambiguous argument 'mori': unknown revision or path not in the working tree.` Therefore the moving `mori` name could not be verified in this checkout. The explicitly assigned commit resolves to the full hash above and was checked out detached in an isolated scratch clone. This limits branch-name provenance, not the committed-byte checks below.

## Counterexample

No counterexample found to the requested hash, predicate, declaration-mapping, or 18-id equality invariants.

One ancillary, fixable citation defect: `SCORECARD.md:2185` attributes the timing observation to `evidence/gate-after.txt:21`. In the committed receipt, line 21 is the `appendonly_violations=...` summary; the `supersede_timing` line is **22**. The declaration's actual 18-id text is correct. This is a citation offset, not a counterexample to the C3 declaration or a reason to infer a canonical judgment.

## Evidence

### Freeze pins: 13 of 13 exact matches

Read `.ufo/waves/round-38/evidence/freeze-r38-v3.txt` from the assigned commit. Every non-comment line is a SHA-256 entry (lines 16–28). For each entry, independently fetched `git show b6993744171a05efc627b5e0664489c31aa5214e:<path>` and passed its bytes to `sha256sum`; all 13 outputs equal the manifest. An independent `hashlib.sha256` pass agreed. No malformed or unmatched hash lines.

All paths below are relative to `.ufo/waves/round-38/`; each actual hash equals its recorded hash.

| Manifest line | File | Actual SHA-256 |
|---|---|---|
| 16 | `contract.md` | `8cfeed27f0ce715089f18ff5cb20d18d211f2e31ed0f0aecf09105d79fb4eac9` |
| 17 | `count-c1.py` | `5aa51556946a3e5293ba069a12b9e816694ea406bd11f5cb22da5e5ba7c22ea3` |
| 18 | `count-c4.py` | `8332341c3901ef09e76bbd7f31e8c8e68b4e4ecc5d3002f2d20201c9e7093ba1` |
| 19 | `conform.py` | `580a0bf15a815b5a26aed908f67a3d74f29d714b19175cee6057fb694aaeb01e` |
| 20 | `fixtures/make-witness-sandbox.py` | `1128524c33511b9b133de02ae2feab1b34767ad689e43acf85cfd35bb2d70259` |
| 21 | `fixtures/memo-n1.py` | `c65220e9e6ac7de6912e8d852d2c6c9da72b5edbb95d5c6f6643433d257dce1d` |
| 22 | `fixtures/const.py` | `83e74c9ebdc035ab9a8af26f859effcaeb16c3ce7faceee9504de2359683b2cb` |
| 23 | `fixtures/summary-only.py` | `d88c9eb648df24548520716682f8b5b68702a46dafdd7a645b270d81ee80f9c9` |
| 24 | `fixtures/hang-after-flush.py` | `647410536bcc6b9ead5456af96056617b78b7945aaacc2c5d3635b1b017a87ca` |
| 25 | `fixtures/memo-sha.py` | `62cbe56ee2497d19dceea4d9abcb6072c8e26a3a5d2dcbf365337534732e391c` |
| 26 | `fixtures/witness-token-entry.md` | `ce4dac65d1dd0ee55f71de1ee5937d474fdfecf32ea599ea3a204395178194f2` |
| 27 | `fixtures/witness-dangling-row.md` | `bc62b0b3db38fbf6086eb5dbdff50a90e5901046ab012abb23e89d9c50357ff2` |
| 28 | `fixtures/witness-summary-only-live.txt` | `8ac9e82bae369a2e41f4a4377016c3e82d58c8c6de484722f1d85b0bbf7cb4af` |

### Predicate identity: independent byte comparison, not just conformance normalization

For each committed Python source, located its unique top-level `PREDICATE` assignment, evaluated only its literal string expression with `ast.literal_eval`, and compared its UTF-8 bytes against the unique corresponding contract blockquote after removing only the Markdown `> ` prefix. No whitespace normalization, Unicode normalization, or punctuation changes. All four equality comparisons were true; independent unified diffs were empty.

Also manually compared the displayed source literals with the untruncated contract lines: P-C1's final lane-tip clause and bare `head_at_measurement=<40-hex>.`, P-C4's em dashes and witness clauses, P-C5's backticked pin/scratch clauses, and P-C6's latest-superseder/descendant/stale clauses all match.

| Predicate | Source location | Contract location | UTF-8 bytes | SHA-256 of both equal strings |
|---|---|---|---|---|
| P-C1 | `.ufo/waves/round-38/count-c1.py:55-66` | `.ufo/waves/round-38/contract.md:114` | 844 | `62fe1a9e11b6c56dd2d181aaed2e851d3bf64c3c082366785ccad222878ac903` |
| P-C4 | `.ufo/waves/round-38/count-c4.py:54-64` | `.ufo/waves/round-38/contract.md:22` | 727 | `737a1977b9ec4e2b1391978f2ea06cfbc3fd41c25c007eec2b44c6f1417070bd` |
| P-C5 | `.ufo/waves/round-38/conform.py:47-56` | `.ufo/waves/round-38/contract.md:62` | 642 | `3f326ba1ce4277082798d1c83868e977e076a98f2a95bdef4195d8d8648a5620` |
| P-C6 | `tools/mori-sources-appendonly.py:76-84` | `.ufo/waves/round-38/contract.md:95` | 531 | `815071a023e8b83182814a5361621db80f91d35fb62842f155d9c82260dd56ce` |

### Requested conformance replay

Ran the committed checker, contract, and both committed counters from the scratch clone detached at the assigned revision. Before running, byte-compared those inputs and the summary fixture with `git show`; also checked the checker's hardcoded lane `hang-after-flush.py` fixture against its committed bytes. No source modifications.

Exact invocation, with the scratch clone path used during this review:

```sh
R=b6993744171a05efc627b5e0664489c31aa5214e
S=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/scratch/resid-freeze-pins-m3pz369g/committed
python3 "$S/.ufo/waves/round-38/conform.py" "$R" \
  --repo "$S" \
  --counter "$S/.ufo/waves/round-38/count-c1.py" \
  --counter "$S/.ufo/waves/round-38/count-c4.py" \
  --contract "$S/.ufo/waves/round-38/contract.md"
```

Observed exit **0** in 3.30 seconds. Output included:

```text
check predicate        PASS (exit=0 equal=True)
check head_pin         PASS (pin=b6993744171a05efc627b5e0664489c31aa5214e tip=b6993744171a05efc627b5e0664489c31aa5214e)
check tool_resolve     PASS
check bounded_reads    PASS
check timeout_state    PASS (exit=1 timeout_reason=True pass=False)
check scratch          PASS
CONFORM=met
```

The `tool_resolve`, `bounded_reads`, and `scratch` lines above omit their parenthesized details only; their observed statuses were PASS. Did not rerun `--selftest` or the C4/gate semantic suites; this seat's replay establishes the requested predicate check and the ordinary conformance run, not independent mutation adequacy.

### SCORECARD declaration: exactly the three contracted claims

The round-38 declaration has exactly three claim rows (`SCORECARD.md:2153-2155`), matching the contract rather than confusing claim numbers with predicate numbers:

| Claim | Axis | Instrument / predicate | Declaration observation |
|---|---|---|---|
| C1 | calibration | `count-c4.py` / P-C4 | fabricated binding accepted by r37 `C2`, rejected by `C4`; real binding `C4=met` |
| C2 | operability | `conform.py` / P-C5 | `CONFORM=unmet` → `CONFORM=met`, with the declared six-mutation selftest |
| C3 | depth | `tools/mori-sources-appendonly.py` / P-C6 | timed supersede output; stale S069 before its new disposition, none stale after |

The C3 after-cell's backticked timing string is byte-identical to the full timing line in committed `.ufo/waves/round-38/evidence/gate-after.txt:22`: 144 UTF-8 bytes, SHA-256 `813c765fdd7fa4b7a8f6cdd29ebe1c6a10bd4fa8d7b6fe88adb08c472acf0774`, exactly 18 distinct ids in the same order:

```text
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]
```

Provenance boundary: `gate-after.txt:1` records a gate run at `f725f3076972e6e70595b5ac8279be524a111ff8`. The comparison above is to that receipt as committed at `b6993744`; it is not represented as a fresh gate execution at `b6993744`.

## Impacted axes and smallest safe correction

No demonstrated impairment of the targeted freeze/identity or calibration/operability/depth mappings. The citation offset affects evidence navigability/provenance only: change the correction note's `gate-after.txt:21` reference to `:22`. Separately, supply or identify the intended moving `mori` reference if branch-name verification is required; do not infer it from the supplied hash. Neither correction was applied.

No tools installed or upgraded. The temporary review clone is disposable and removed after inspection; lane Git index/jj state, sources, instruments, and evidence were not modified.
