# Mo61Reviewer08 — selftest scrutiny

Axes: arm coverage, case-name fidelity, contract fidelity, evidence reproducibility. Review only; no counter/contract amendments proposed.

## Findings (severity order)

### High — C1's `superseded-ok` positively certifies a contract-invalid registry

Contract `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/contract.md:34-40` requires exactly one **non-superseded** row. C1:145-148 creates two superseded rows, and C1:156 expects this fixture to meet. C1:96-103 filters both out, then falls back to `hits[0]` when `live` is empty. The frozen receipt confirms `case superseded-ok: ok=True want=True pass failed=[]` (E1:5). This is not merely missing coverage: a green selftest protects the opposite of the frozen invariant. There is no zero-live-row rejection case or one-live-plus-superseded case.

### Medium — C1 `unres` never reaches the unresolved-entry arm; duplicate-live arm also untested

C1:157 requests `tools/nothere.py`, but supplies only GOOD, whose entry is `tools/g.py` (C1:139). Consequently `missing` fires at C1:92-95 and continues before path resolution (C1:113-116). E1:6 proves the actual failure is `missing:tools/nothere.py`, not `unres`. No listed case supplies a matching row for a nonexistent committed file. No case supplies two non-superseded matching rows, so C1:99-102 is also uncovered. All cases assert only the final boolean (C1:185-189), allowing the wrong failure arm to count as a pass.

### Medium — C3 `r60-tamper-detected` tests the hash guard, not the claimed semantic hole check

C3:238-243 says it inserts a `c1` conjunct and tests detection. But any such byte change fails C3:88-89 (`r60_bytes_pin`) before C3:91-102 inspects the met expression or gate tokens. The mutation anchor matches the actual r60 met line at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-60/count-c3.py:255`. The case asserts only a false arm/false aggregate, never its reason. E3:2's passing result therefore establishes rejection, not traversal of `r60_hole_absent`. Baseline `r60hole-real-bytes` covers only the accept path; no case reaches the semantic negative branches behind the pin guard.

### Medium — C2's good selftest cannot pass the default pointer floor; receipt omits invocation

C2:207-208 repeats the same six distinct pointers 22 times; C2:57-65 deduplicates them. There are six good ledger rows (C2:255-260). Default floor is 40 (C2:38,291), and selftest forwards it unchanged (C2:276,297). Thus the default `--selftest` good case necessarily gets `pointer_floor:6<40` and fails its expected True assertion. E2:1 instead records good=True with no failures, but E2 contains no command or floor setting. [INFERENCE] That receipt used a floor no greater than six, or different execution context/bytes; it does not document which. No dedicated case exercises the pointer-floor rejection while preserving the other invariants. This does not establish failure of a live default-floor ledger; it limits what the green receipt proves.

### Low — Several negative cases are confounded, so green totals do not isolate their named checks

* C2 `orphan`: E2:4 includes `rows_orphan`, `quote_words`, and `rows_ne_pointers`; the added quote has four words (C2:265) and the row count is seven. Removing the orphan-set check alone would still leave this case green.
* C2 `row-missing`: E2:3 includes both `rows_missing` and `rows_ne_pointers`; either alone suffices for its boolean assertion.
* C2 `tampered-copy`: E2:9 includes `copy_pin`, two `loc_bad` failures, and `sources_floor`. It reaches those arms, but does not isolate any one of them.
* C3 `wrong-pins-detected`: both pins are wrong (C3:253-256); `arm_livepins` returns on C1 first (C3:157-162), so no case negatively tests C2's pin independently.

## Complete case-to-arm map

Aliases below are absolute file paths, not shell-relative paths:

* C1 = `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c1.py`
* C2 = `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c2.py`
* C3 = `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c3.py`
* E1 = `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/evidence/selftest-c1.txt`
* E2 = `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/evidence/selftest-c2.txt`
* E3 = `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/evidence/selftest-c3.txt`

### C1: all six cases (list C1:150-158; results E1:1-8)

| Case | Actual arm/evidence |
|---|---|
| good | Conformant single live row, committed entry; positive measure path, C1:90-119; E1:1. |
| missing | `missing` at C1:92-95 for tools/absent.py; E1:2. |
| thin | Empty owner enters generic `thin` at C1:104-108; E1:3. Does not increment `noowner`. |
| noselftest | `noselftest` at C1:109-112; E1:4. |
| superseded-ok | Zero-live fallback at C1:103, then accepted; E1:5. Contract mismatch above. |
| unres | Actually `missing` at C1:92-95; E1:6. Name mismatch above. |

No case: skill absent (77-79), manifest decode error (81-86), empty manifest (88-89), duplicate live rows (99-102), matching row with unresolved entry (113-116), main manifest-not-found handling (208-216), malformed/wrong-width table or absent header handling (40-59). Empty-owner rejection is covered by `thin`; `noowner` has no increment site anywhere in this counter and remains zero, so the receipt does not validate that diagnostic as an independent arm.

### C2: all ten cases (list C2:261-272; results E2:1-12)

| Case | Actual arm/evidence |
|---|---|
| good | All three statuses: same at a:5-7/a:9/c:12/d:20, moved b:9→b:10, changed a:30→b:30 (255-260); four-source positive path (165-182); E2:1. Pointer deduplication is positive-tested, not 40-pointer coverage. |
| quote-missing | Correct quote exists elsewhere but not its same-range window; `quote_missing` (159-164); E2:2. |
| row-missing | `rows_missing` (127-131) plus count mismatch (185-186); E2:3. |
| orphan | `rows_orphan` (132-133), low word count (137-139), count mismatch (185-186); E2:4. |
| small-span | Six one-byte-identical words pass word count, fail distinct-byte floor (140-142); E2:5. |
| dup-quote | Duplicate quote (143-145); E2:6. |
| not-mined | Registry rows fail status condition (176-182); E2:7. |
| usedby-miss | Registry rows fail used-by substring (176-182); E2:8. |
| tampered-copy | Copy hash failure (114-116), missing accepted copy triggers loc_bad (150-152), only three cited copies triggers sources_floor (165-167); E2:9. |
| no-prov | Missing provenance trio (106-107); E2:10. |

No case: source entry absent (94-97), ledger absent (101-104), copy absent (110-113), duplicate anchor (125-126), >25-word quote (137-139; lower bound does have orphan coverage), out-of-bounds location (156-158), registry absent (168-170), standalone missing registry row, dedicated pointer-floor rejection (183-184). No negative moved/changed location case, no fewer-than-four otherwise-valid-source fixture, and no malformed location case (notably moved/changed `-` passes ROW but `span_of('-')` returns None before tuple unpacking at 148-149; static uncovered error path, not executed here). `loc_bad` and `sources_floor` do have cases via tampered-copy, but are not isolated. All acceptance assertions are boolean-only (276-280).

### C3: all eight cases (C3:233-265; results E3:1-10)

| Case | Actual arm/evidence |
|---|---|
| all-arms-good | Positive conjunction of all five arm booleans (175-190), pins recomputed from fixture counter bytes (233-235); E3:1. |
| r60-tamper-detected | r60 hash mismatch (88-89), not semantic c1 test; E3:2. |
| self-mutant-detected | Self bytes lack c1_ok in met; `c1_conjunct_missing` (110-112; mutation 245-251); E3:3. |
| wrong-pins-detected | First live counter pin mismatch (157-162; 253-256); E3:4. |
| blobrefusal | Unpinned run=True refusal, empty EXEC_LOG, pinned run=False materialization (126-139); E3:5. No successful child execution attempted. |
| expectpin | Current in-memory table matches its initialized hash; locally changed copy has different digest (142-153); E3:6. |
| r60hole-real-bytes | Positive r60 pinned-byte/text recognition (87-103); E3:7. |
| r61repair-real-bytes | Positive self-source recognition (106-123); E3:8. |

No independent negative case: missing r60/self bytes; r60 missing met, semantic hole absent, emitted append site, untested token (91-102); self missing/malformed TOKEN_MAP, wrong keys, or unbound token (113-122); preexisting EXEC_LOG/non-refusal/pinned refusal failure branches (129-138); altered active EXPECTS causing expect_pin_mismatch (145-146); absent live counter (159-160); second-counter-only hash mismatch (161-162). `arm_expectpin` itself compares a tampered copy's hash, but no selftest substitutes a tampered active table or a failing arm to exercise aggregate rejection/FAIL formatting for expectpin. Likewise no blobrefusal-false aggregate case. No assertions inspect `fmt` token/failed output (193-198). The all-good case overrides live pins with fresh fixture hashes, so it does not independently test the hardcoded PIN_C1/PIN_C2 values.

## Evidence and limits

Commands actually issued:

* `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 325f7e639916fcbc77fa2ec7475951a1b86bb1cb 7370a731abcafc4c803111de7c22cd6264d63be1 -- .ufo/waves/round-61/count-c1.py .ufo/waves/round-61/count-c2.py .ufo/waves/round-61/count-c3.py` — three added files, 819 insertions, zero deletions. Counter sources and receipts inspected through read tools at the absolute paths above. Text search located r60 met line; it is not semantic-reference proof.
* `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` — printed scratch free 370.9G/use 54%, /tmp free 97.5G; command timed out after 30 seconds while listing consumers. No heavy work followed; no ENOSPC observed.
* Own scratch directory `/fast/scratch/hyaku/mori-r61/Mo61Reviewer08` created, TMPDIR scoped there, then empty directory removed. No fixture, counter, selftest, or mutation execution; no tools installed; no VCS writes.

LSP: read of `xd://lsp` returned `No such tool`; no mounted server/status/reference/definition/diagnostics route was available. Findings are source/receipt control-flow review, not semantic LSP proof. Frozen receipts are cited as existing recorded output, not fresh test results. No production file, registry, contract, or counter changed.

Residual risk: no runtime branch trace or mutation run was performed; uncovered branches are statically derived from the complete case lists and their fixture builders. Green totals (C1 6/6, C2 10/10, C3 8/8) are not exhaustive arm coverage or saturation evidence. Canonical runtime/resume/rerouting behavior is not exercised by these counter-only case lists and no claim about it is made. Report is a review recommendation, not an admission or closure decision.

Self-evaluation: accuracy 4/5 (static reasoning plus existing receipts, no fresh trace); completeness 4/5 (all 24 cases mapped, no dynamic coverage); clarity 4/5 (absolute alias legend needed for compact pointers); actionability 4/5 (specific frozen findings, amendments intentionally barred); conciseness 4/5 (full requested arm ledger requires detail). Overall 4.0/5. Highest-value verification gaps are a reason-aware arm trace and documenting the C2 selftest floor; neither was performed or changed here.
