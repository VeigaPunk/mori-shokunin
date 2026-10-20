# Round 17 lane overlap audit

## Axes

- **C1 coverage (axis 6):** read-only, field-limited classification of each OMP seat transcript's last observed terminal state, with per-prefix and per-provider/model tallies (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:9-15,39-56`).
- **C2 operability (axis 7):** branch-anchored Mori census probes plus `HEAD_BRANCH_MISMATCH` and `LANE_AUTHOR_MISMATCH` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:16-22,80-94`).

## Findings from the four PROVINCE.md / SKILL.md pairs

### C1: transcript overlap is adjacent, not duplicate terminal-status coverage

- Souji has two transcript-facing tools, but neither classifies a seat's final state. `souji-seat-audit` checks conduct/disclosure classes (`V-SURFACE`, `V-LIVE-CENSUS`, `V-WRITE-SCOPE`, `V-EXEC`, etc.); its “status-aware” clause selects severity from a recorded write result (`⇒ ok`/`⇒ error`), not the OMP seat's terminal message. `r17-transcript-manifest` checks transcript inventory and byte digests. These are separate outputs and evidence purposes from C1's terminal classes and bounded field projection (`/home/vgpnk/Projects/shokunin/souji-shokunin/SKILL.md:166-167`; C1 contract `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:39-56`).
- Mado's post-hoc tripwire scans seat transcripts for assistant tool-call commands and reports host-mutation/package-query/live-probe findings; its frozen mode replays digest-pinned incident lines. It does not classify `stopReason`/terminal role, quota or rate-limit deaths, or provider/model terminal tallies (`/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md:527-540,563,566-567`). Its “after every wave” timing is superficially similar to settlement, but the measured claim is seat conduct, not wave completion/death.
- No corresponding seat-terminal, seat-death, or transcript-settlement mechanism was found in the reviewed Tameshi or Kaidoku PROVINCE/SKILL pair; their matching SKILL material below concerns revision pins, not OMP transcript state. Tameshi also explicitly keeps sibling product gates adjacent/report-only (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md:14-20,44-48`).

**Conclusion:** no existing lane surface duplicates C1. Do not broaden C1 into a command/conduct audit or reuse incident transcript content as fixtures: its contract deliberately considers only `type == "message"` records and explicitly forbids emitting message content/error text (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:35-56`), while Souji and Mado answer different questions.

### C2: branch-tip patterns overlap, but do not duplicate the census behavior

- Tameshi's pin comparison selects `<branch>` using the shared `detect_branch` rule and reads `refs/heads/<branch>^{commit}` / its blob, never jj working-copy `HEAD`. This is a direct precedent for C2's branch-resolution substrate, but its output is pin-byte `current/stale/drift` and harness `held/moved`, not Mori census row 6 report closure or row 9 authorship (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md:1027-1035,1843-1844`; C2 contract `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:82-90`).
- Kaidoku has the closest behavioral analogue: its jj revision-pin rules report that an unbookmarked jj commit can leave `HEAD` off `main` while `git show HEAD:<path>` still succeeds; its `revpin` refuses a literal `--rev HEAD` unless HEAD equals `refs/heads/main` (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md:569-579,587-589`). This overlaps C2's anti-HEAD hazard, but is not a drop-in duplicate: Kaidoku tests strict equality to `main`, while C2 resolves the lane branch dynamically and emits `HEAD_BRANCH_MISMATCH` only when `HEAD` is **not an ancestor** of `refs/heads/<branch>` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:82-87`).
- Souji's jj rules also distinguish branch queries from keep-only/unbookmarked commits and exclude `refs/jj/*` from durable receipt roots (`/home/vgpnk/Projects/shokunin/souji-shokunin/SKILL.md:108-111`; `/home/vgpnk/Projects/shokunin/souji-shokunin/PROVINCE.md:25-30,101-118`). That is receipt/pruning safety, not a census duplicate. Mado's `mado-landed-check` follows live `origin` `refs/heads/master` ancestry for landing records, not a local jj-colocated lane census (`/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md:574`).

## One bounded move

**Add one adversarial off-branch-HEAD case to the existing C2 jj regression gate, modeled on Kaidoku's observed `git show HEAD:<path>` false reassurance.** In a colocated sandbox, leave the selected `refs/heads/<branch>` tip at commit B and set detached `HEAD` to a non-ancestor off-branch commit U that contains a report path absent from B. Confirm `git show HEAD:<path>` succeeds in the fixture, then assert the census does not close/grade that report from U, uses the branch tip for row 6, and emits `HEAD_BRANCH_MISMATCH` with the contracted lane/head/tip detail. Keep the fixture in the existing sandbox gate; no production scope or C1 changes. This is a targeted verification improvement for **C2 operability**; **C1 coverage is unchanged**.

## Contradictions and risks

- Do not copy Kaidoku's `HEAD != branch tip` rule literally: ordinary detached-at-tip HEAD is expected in jj, and a HEAD that is behind the branch can still be an ancestor. The C2 trigger is specifically failed ancestry; the proposed U must be off-branch/non-ancestor to avoid a false failure (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:82-87`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md:577-579`).
- C2's drift finding is not permission to reinterpret Souji's receipt roots: `refs/jj/keep/*` is explicitly not a durable receipt root and keep-only work can be invisible to branch queries. Keep those cleanup/receipt semantics separate (`/home/vgpnk/Projects/shokunin/souji-shokunin/SKILL.md:108-111`).
- The off-branch fixture should only falsify row 6's HEAD-based path check; preserve the existing A/B/C grading and separately specified row 9 author scan unchanged (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:84-90`).

## Verification

- **Not run:** this was a static connector audit; no executable checks or shell commands were run, no files were read from OMP session directories, and no tools were installed.
- Main integration verification should run the contracted `tools/mori-round17-jj-regressions.py --census PATH --output DIR` against both entering and delivered census bytes; include the new off-branch-HEAD assertion in the gate's case count and confirm the entering implementation is red for that case and the delivered implementation is green (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:91-94`).
- Report evidence is limited to local source text cited above; no URLs consulted.
