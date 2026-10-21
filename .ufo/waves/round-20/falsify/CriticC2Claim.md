PARTIAL — the finite C2 capability is real and the co-evolved cases are transparently separated; do not treat the 14→0 delta as 14 production defects or the live comparison as fully provenance-bound proof of dispatch settlement.

## Counterexample

The strongest counterexample is semantic scope: the tool discovers every JSON file with `schema == ufo-swarm-wave-dispatch-v1`, then reports presence at its task trailers. It does not establish that each such file corresponds to an actual invocation. R3 `name_hint` is a warning, not an exclusion. The knowledge note records two name-hinted payloads that were never dispatched (mado `dispatch-preview.json`, revenger `rendered-undispatched.json`), while twelve other name-hinted payloads were executed. Thus a “settled”/“unsettled” result is a filesystem observation about dispatch-shaped JSON, not proof of launched seats, valid report contents, or accepted results. This is an explicit limit, not a defect against the frozen contract's narrower discovery rule.

## Evidence

- **Not a free lunch, but not 14 separate historical bugs:** frozen C2 defines 14 cases and explicitly calls entering absence a missing capability, “not 14 historical production defects” (`.ufo/waves/round-20/contract.md:90-93`; case inventory `.ufo/waves/round-20/frozen/c2-expected.json:6-20`). Before evidence reports `capability_absent=14, matched=0`; after evidence reports `capability_absent=0, matched=14, mismatched=0` (`.ufo/waves/round-20/evidence/c2-before.json:1-6`; `.../c2-after.json:1-6`). The oracle builds isolated fixtures, invokes the tool as a subprocess, and compares against the frozen cases (`.ufo/waves/round-20/build/OracleHarness/c2-oracle.py:336-416`); it does not import the production implementation. This validates one new capability against 14 finite requirements. The before count is the same absent-tool fact repeated for each case, not 14 independently observed production failures.
- **Refinements are separated honestly:** the lesson labels them “after dispatch; frozen bytes unchanged” and lists R1-R5 plus missing-`taskCall`, seven refinement selftests (`corpus/lessons/round-20.md:31-35`). The tool keeps these in `REFINEMENT_CASES` (`tools/mori-wave-settlement.py:37-48`); selftest appends that list to the frozen cases at runtime (`tools/mori-wave-settlement.py:600-640`). The external oracle loads only `frozen/c2-expected.json` (`.ufo/waves/round-20/build/OracleHarness/c2-oracle.py:393-416`). Therefore the 14/14 result does not silently count the seven refinements. Those refinements are disclosed, but are selftest coverage, not part of the independent 14-case oracle result.
- **Live W1 result:** querying `.ufo/waves/round-20/evidence/c2-live-mori.json:1` for wave `mori-r19-attempt2-build` returned dispatch `.ufo/waves/round-19/wave1-run.json`, 64 members, 16 present, 48 missing, state `partial`; the knowledge note records the scan at 10:46:42Z (`corpus/knowledge/wave-settlement-r20.md:71-74`). A separate manual ground-truth note says it extracted 64 tasks from `wave1-run.json`, used `stat` without the settlement tool, and found 16 present/48 missing (`.ufo/waves/round-20/build/GtMoriR19W1.md:4-10,16-25`); its present and missing sets match the recorded settlement (`.../GtMoriR19W1.md:96-109`). This is useful independent-method corroboration of the current tree, though the note gives no named reviewer or observation timestamp tying it to the 10:46:42Z scan.
- **Who counted it first is not established by the settlement JSON:** `.ufo/waves/round-19/wave1-settlement.json:1-23` records 64 returned IDs and the 16-name list, but contains no count-author field. Read-only history command and result:

  ```text
  git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --follow --reverse --format='%H%n%an <%ae>%n%aI%n%s' -- .ufo/waves/round-19/wave1-settlement.json; rc=$?; printf 'history_exit=%d\n' "$rc"
  ```

  ```text
  a4f79dd4dd8fedb6ab062bf53a0f4bebaa6cf42e
  mori-shokunin <mori@shokunin.local>
  2026-10-21T06:18:08-03:00
  round-19: settle falsification and bind final bounded measurements
  history_exit=0
  ```

  The manifest identifies `CloseMori19` as a non-author integrator, but its listed independent C2 rechecks concern the prior finite-case counts, not the W1 report count (`/home/vgpnk/Projects/shokunin/MANIFEST.json:10149-10151`); it repeats W1 totals in the closure note (`.../MANIFEST.json:10171`). The first W1 settlement commit therefore has the lane Git identity, not count-specific independent provenance. [INFERENCE] The commit identity alone cannot establish which seat/person derived the original 16; the later `GtMoriR19W1` method is separate evidence, but its generic Git author and missing observation time do not prove independent authorship or same-snapshot comparison.
- **Known limit is disclosed:** schema-based discovery and the distinction between report presence and actual dispatch are stated in `corpus/knowledge/wave-settlement-r20.md:54-62`; the implementation's name hint does not gate wave state (`tools/mori-wave-settlement.py:289-299,304-333`).

## Impacted axes

- **Coverage:** genuine positive movement for one narrow capability—per-member report-path presence for discovered dispatch-schema files, exercised against 14 frozen cases and a live W1 tree.
- **Calibration / admission confidence:** limit the live “independent” claim to a matching separate manual recount; the historical 16/64 receipt itself is not count-author-attributed or snapshot-bound.
- No evidence here supports changing operability, depth, freshness, or adjacency.

## Smallest safe correction

No change to the frozen cases or tool is required for the contracted observation-only behavior. Admit this as **one capability acquired, 14 frozen acceptance cases matched**—not 14 defects fixed—and keep the seven co-evolved selftests separate. Describe the scope as report-presence scanning of dispatch-shaped JSON, not verification of actual dispatch, successful completion, or result acceptance. If the live result is to be called independently verified, attach a named non-author recount receipt bound to the same dispatch digest and observation snapshot; otherwise say it agrees with a later manual recount. Tool installs/updates: none.
