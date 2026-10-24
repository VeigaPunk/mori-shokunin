# C1 adjacency falsification — attacked tip `e2bfbd6f8dccc51fc06455efc41f720301112dd4`

## Verdict and axis

**Adjacency remains harmed at this tip.** I would not admit an axis-level verdict of “adjacency improved.” The narrower statement that the frozen R1–R9 count improved may be reported separately, with its measured revision and gate evidence; it does not establish that committed private-context retention has been repaired end-to-end. The draft itself distinguishes the frozen-class metric from a partial whole-round sweep (`.ufo/waves/round-18/draft-verdicts.md:8,21-23`; attacked-blob SHA-256 `c83dc17160b108cec68526dcf817ff78ffabf8859c3f39b6ab11936101c22ff6`). I did not run the gate or independently verify that count.

**Impacted axis:** adjacency (C1). No evidence here changes calibration, operability, or other axes.

## Strongest counterexamples

1. **Known admitted findings are still pending at the attacked revision.** The exact-tip triage retains admitted session-record/per-seat-retry and operator/host-configuration findings as pending minimization (`.ufo/waves/round-18/out-of-metric-triage.md:25-26`; SHA-256 `b136c957cb8c45848b67cffde34287393925755b9f24836bc620f6e8ec60ae9a`). This is not a speculative regex miss: the frozen policy explicitly makes the regex classes a recall floor, so a clean R1–R9 count cannot prove absence of out-of-metric private context (`.ufo/waves/round-18/frozen/c1-policy.json:27-29`). The exact-tip triage labels these admitted findings as debt, so current adjacency harm is already established without deciding the SW1 boundary.

2. **The SW1 blanket rejection is not justified by wave membership alone.** At the attacked tip, triage rejects SW1 “other-seat tool/report results” because they are same-round lane work (`out-of-metric-triage.md:31`). The minimization rule committed at the same tip says other-session tool output or transcript excerpts/paraphrases are not retainable as such (`corpus/knowledge/evidence-minimization-r18.md:25-30`), while its separate same-wave exception is at `:37-40` (whole-file SHA-256 `4595ad4408c81769512213e96f9afbcfff30c4f40894d634356b15b47e393033`). The round-17 closure identifies other-session tool/document/history material as adjacency harm at `corpus/lessons/round-17-verifier-spotcheck.md:239,315` (whole-file SHA-256 `98f8f1c631fcb565af69d884330177ebe01bfb31f21218028157d2acc40698dd`). The closure does not state a same-wave exemption. Thus “same wave” cannot safely decide whether the *content* is an excerpt or paraphrase of private, other-session output.

   The wave-1 evidence supplies a concrete challenge to that categorical rule: `build/SweepR17Build2.md` classifies 48 lines across five round-17 reports as SW1 other-seat tool/report results (report at e2 SHA-256 `d632427d6858cacbb13e5667ea66081279d6639b85535f31562c57f09912a998`). These are the sweep’s source locations and source-blob hashes; no source text is reproduced:

   | Source path:line(s) | Class/count | Source SHA-256 |
   |---|---:|---|
   | `.ufo/waves/round-17/build/FrontierLinkage.md:7,15-22,28-31,35` | SW1; 14 lines | `1a7ed8983c1ac5cf003f49cea7227488244e526cea6462ea467c2b98709a919a` |
   | `.ufo/waves/round-17/build/HelperFailureWindows.md:9,34-39,177-178,195,248,264-265` | SW1; 13 lines | `4af9ca0b10f75e98c14dfd6cbc01c160945add3f56ab293ed0908496767eb4c4` |
   | `.ufo/waves/round-17/build/JjGate.md:244-247` | SW1; 4 lines | `76a05de8dc1c248f28cee37e65e3069922c5551657f2f8fe4c9b27d1c7e5c1e1` |
   | `.ufo/waves/round-17/build/KnowledgeJjBranch.md:33-35,56-60,101-103,115,119,123,127,143` | SW1; 16 lines | `4d0b6b66c6126c85fb311303b209d9275c21f52e2ca6fed4b887387569e5e396` |
   | `.ufo/waves/round-17/build/KnowledgeSeatTerminal.md:82` | SW1; 1 line | `4a49e621b867c49ce6b06c1572b36b9c02d6fffc87ae1355bd54f9e98e2c0c1a` |

   The sweep describes these as copied or paraphrased result material, not merely seat names. A path-limited `git diff-tree` from frozen base `d005cdde0e009dea6c0cc29b37163de536528658` to attacked tip listed none of those five source files (rc 0); their cited source blobs therefore remain at e2. This does not prove every SW1 line is private, but it falsifies a rule that rejects the entire family solely because it was produced by a sibling in the wave. The minimization table’s content-based boundary and the closure’s wording require an item-level check.

3. **Other wave-1 findings corroborate the pending categories.** `build/SweepR17Build5.md:37` classifies 17 lines in `ReviewSeatBreachDetect.md` as M-SESSION-RECORD; `:47` classifies 37 lines in `SentinelJjSandbox.md` as M-OPERATOR-CONFIG (report at e2 SHA-256 `9bcabbf072862247fecff63f8343d7398ad07e71d83582267aefad95251cd0f5`; source hashes and line groups are recorded there). The attacked-tip triage separately lists these families among the admitted pending items at `out-of-metric-triage.md:25-26`. The sweep’s classifications are location/count/hash only; no private values are needed to establish the residual debt.

## Assessment of the L1 rule

The same-wave exception is a **fixable adjudication-rule defect**, not a safe basis for declaring all sibling results non-private. It is reasonable to retain a lane result when the content is independently established as non-private and contains no item in the minimization table’s “never” column. It is not safe to retain an excerpt or paraphrase of other-session tool output merely because a sibling authored or reported it in the same wave. The closure’s use of “other-session” does not itself prove every sibling report is private, but the SW1 sweep findings create a concrete overlap that the blanket rejection does not resolve.

## Smallest safe correction

- Keep “frozen R1–R9 metric improved” only as a metric-scoped statement; keep the C1 axis at **harmed** while any admitted out-of-metric finding remains pending.
- Replace the categorical SW1 rejection with a content test: retain only independently supported, non-private lane conclusions; redact/abstract any output excerpt or paraphrase that falls under the “never” categories, regardless of same-wave provenance. Record safe provenance as path/line, class, count, and a whole-file/long-line digest rather than copied content.
- Complete the admitted pending minimizations and cover the sweep gaps identified at `out-of-metric-triage.md:35` before changing the axis verdict. A clean R1–R9 count alone is insufficient.

## Evidence that would change this verdict

At one exact measured revision: (1) the admitted pending session-derived and host/config findings are removed or reduced to the allowed support-only form; (2) each SW1 item is either minimized or shown, with content-based evidence, to contain no other-session/private output; and (3) a fresh full-tree lexical plus manual sweep closes the identified coverage gaps with no remaining “never” items. This would support an adjacency improvement for the current committed tree, not erase any historical disclosure; the closure leaves exposure/history decisions with the authorized owner.

## Evidence and activity record

- Attacked revision lookup: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show -s --format=%H e2bfbd6f8dccc51fc06455efc41f720301112dd4` — rc 0; exact requested revision.
- Exact-tip blob digests: `git show e2bfbd6f8dccc51fc06455efc41f720301112dd4:.ufo/waves/round-18/draft-verdicts.md | sha256sum` — rc 0, `c83dc171…`; triage equivalent — rc 0, `b136c957…`; `build/SweepR17Build2.md` equivalent — rc 0, `d632427d…`; `corpus/knowledge/evidence-minimization-r18.md` equivalent — rc 0, `4595ad44…`; closure equivalent — rc 0, `98f8f1c6…`.
- Path-limited source check: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff-tree --no-commit-id --name-only -r d005cdde0e009dea6c0cc29b37163de536528658 e2bfbd6f8dccc51fc06455efc41f720301112dd4 -- .ufo/waves/round-17/build/{FrontierLinkage,HelperFailureWindows,JjGate,KnowledgeJjBranch,KnowledgeSeatTerminal}.md` — rc 0; no paths listed.
- Reads/searches were limited to the contract, frozen inputs, cited closure/minimization sections, draft, triage, and wave-1 `Sweep*.md` reports. Read/glob/grep devices do not expose numeric exit codes. No URLs accessed; no tool installed or updated; no tests, gate runs, VCS mutations, or other file writes performed.
