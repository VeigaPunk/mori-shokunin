# Mo94K02Crit — round 94 w1 critic (frontier step, mistake, planner disagreement, fixture)

Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`, freeze `6b65e7c1`, base `84b15230`. Lane not edited. Scratch removed by trap and by hand at exit. Installs: none.

## Verdicts

| Item | Verdict | One-line reason |
|---|---|---|
| 1. P5 / S624 | **P5 rests on S624: yes. Teaches line: admit with a correction** | `startswith` is the operation the counter uses; the scribe's teaches line adds a `start`-parameter digression and must say "prefix test on the first token", not imply provenance. |
| 2. D3 marker mistake | **Lane defect: yes (durability). `captured-by: none` is NOT honest. Proposed `.gitignore` fix: can pass its own check while making the defect worse; reject as written.** | Markers are normally committed (33 tracked `ready`/`dispatched` files in history); the fix hides them, and does not cover `w1.ready`. |
| 3. D1 planner | **Stays OPEN (operator-owned). The shape line is a disclosure, not a closure.** | Policy supports "validator does not count planner as a swarm role"; nothing in the artifacts binds the L1 to the topology planner slot; "No residual call" is wrong. |
| 4. Fixture | **Not a result cherry-pick; a coverage gap. Second file to replay: `rotation-schedule-r74.md`** (plus `drift-pin-r10.md`). | Single-file battery, always verified-at on line 1; I replayed two more TWELVE files and got identical verdicts, but the battery cannot show line-position or window-edge robustness. |

## 1. Sourced claim (P5, S624)

Command (scratch; not the lane):
```
curl -fsSL --max-time 60 -o stdtypes.html https://docs.python.org/3/library/stdtypes.html; echo curl_rc=$?
sha256sum stdtypes.html; wc -c stdtypes.html
```
Observed:
```
curl_rc=0
2397d83204d8901b852e5dcb72cb1b5cbf311e9db1f15116089b85ab21d22b68  stdtypes.html
815447 stdtypes.html
```
Matches contract P5 (sha256 and 815447 bytes). Anchor `id="str.startswith"` present. Tag-stripped text (my extraction): `str.startswith(prefix[, start[, end]]) Return True if string starts with the prefix, otherwise return False. prefix can also be a tuple of prefixes to look for. With optional start, test string beginning at that position.`
The recorded quote in the contract / scribe draft has a space before the comma ("prefix , otherwise"); that is an extraction artifact of replacing tags with spaces. A row must state the normalisation or quote the visible text.

The counter applies the operation as written: `.ufo/waves/round-94/count-c1v2.py:103` reads `return len(tok) >= 7 and ac.startswith(tok)`, where `tok` is the first whitespace token of the `verified-at:` value. Direction is correct: the token must be a leading part of the admission `%h`. So P5 rests on S624 for the operation.

What S624 does NOT say: anything about tokens, 7-character minimum, `verified-at:`, or whether the admission commit is the correct provenance. Those are the lane's rule, not the page's.

Scribe draft (`w1/Mo94Sc01Lesson.md` line 12, present at check time) teaches: "`str.startswith(prefix)` is prefix equality at the string's beginning (the page adds: 'test string beginning at that position', for optional `start`), so an admission check that compares the first token with `startswith` does not accept a hash that merely occurs inside a longer token".
- Core claim: supported. Embedded-hash rejection is shown by the controls, not by S624 alone; the sentence states it as a consequence, which is fine.
- Overreach/padding: the `start` parameter is not used by the counter; drop it. "Prefix equality" is a gloss; say "prefix test". Add the limit: the test establishes only that the token is a leading part of the admission `%h`, not that the admission commit introduced the current content (contract named limit).

Proposed S624 teaches line (replaces the scribe's):
> `str.startswith(p)` is True when the string begins with `p`. The round-94 counter applies it to the first whitespace token of `verified-at:` (at least 7 characters) against the admission `%h`, so a hash occurring inside a longer token is rejected. It does not show that the admission commit introduced the file's current content.

Quote to record (visible text, normalised): `Return True if string starts with the prefix, otherwise return False.` (anchor `id="str.startswith"`, docs.python.org/3/library/stdtypes.html; post-redirect builtins path per scribe note).

## 2. Mistake: D3 untracked orchestrator markers

Commands (lane, read-only):
```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files | grep -c "ready"        -> 67
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files | grep -c "ready.dispatched"  -> 33 (earlier count: 33 via ls-files | grep -c ready.dispatched)
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files | grep "ready" | head   -> .ufo/waves/round-47/w1.ready, .ufo/waves/round-47/w1.ready.dispatched, ...
git -C /home/vgpnk/Projects/shokunin/mori-shokunin check-ignore -v .ufo/waves/round-94/w1.ready.dispatched; echo rc=$?   -> rc=1
```
Current porcelain: `?? .ufo/waves/round-92/w1.ready.dispatched`, `?? .ufo/waves/round-93/w1.ready`, `?? .ufo/waves/round-93/w1.ready.dispatched`, `?? .ufo/waves/round-94/w1.ready`, `?? .ufo/waves/round-94/w1.ready.dispatched` (five paths; the round-94 pair is new since the red-before receipt).

**Lane defect?** Yes, in durability terms. The lane's own history commits its markers (33 tracked `*.ready.dispatched` and matching `w1.ready` files from earlier rounds). Rounds 92-94 left them untracked, while `jj-lane.sh state` counts `^??` lines as `untracked=` (`scripts/hyaku/jj-lane.sh:181`) and the contract accepted "clean except three markers". The orchestrator writes these files into the lane tree, so the origin is shared; the non-durability is the lane's.

**Captured-by none honest?** No. The defect was captured by the round-93 non-author spot-check, `corpus/lessons/round-93-verifier-spotcheck.md` §1 (porcelain row) and §6 D3, with a route "operator/orchestrator to commit or move them". The honest entry is: `captured-by: round-93 spot-check D3 (non-author); gate: none`. Scribe draft also says `none`; fix both.

**Can the `.gitignore` fix fail?** It passes its own check and fails the protocol. Fixture run (scratch repo, committed one tracked marker, then the rule):
```
before rule:  ?? .ufo/waves/round-92/   ?? .ufo/waves/round-93w.ready
after rule:   ?? .gitignore  ?? .ufo/waves/round-92/  ?? .ufo/waves/round-93w.ready
check-ignore -v .ufo/waves/round-92/w1.ready.dispatched -> .gitignore:1:*.ready.dispatched  rc=0
check-ignore -v .ufo/waves/round-92/w1.ready           -> rc=1
git add -A; git ls-files -> .gitignore, .ufo/waves/round-47/w1.ready.dispatched (tracked before), .ufo/waves/round-92/w1.ready, .ufo/waves/round-93w.ready
untracked count after add: 0
```
Consequences for the lane:
- The ignored marker `w1.ready.dispatched` is silently excluded from `git add`: the defect the spot-check named (non-durable markers) is made invisible, not fixed. The red/green check measures suppression, not durability, so "green" is the wrong pass.
- `w1.ready` (round-93 and round-94) is not matched: the lane keeps 2 untracked paths, so `untracked=0` is unreachable with this rule.
- The rule does not touch the 33 already-tracked markers, so the history now has tracked and hidden markers for the same kind of file.
- The patch is not in the tree (`w1/patches/` absent at check time); this verdict is on the contract's stated rule.

Correct treatment (route, not patch here): commit the markers with the round's integration commit (the protocol the spot-check cites and the 33-file precedent), or route the move to the orchestrator. The gate should be durability: after the commit, `git ls-files --error-unmatch` on each marker path exits 0 and `status --porcelain` shows no `??` for `.ufo/waves/`. Red-before/green-after must use that predicate, not `check-ignore`.

## 3. Planner disagreement (round-93 D1)

Evidence read:
- `scripts/hyaku/ufo-wave-policy-v2.json` `nativeProfiles."omp-native-v1"`: `"planner": {"role":"planner","depth":1,"count":1}` is a topology slot; `proposalRoles` lists scout, reviewer, critic, connector, sentinel, executor, mutation-tester, revenger, simplifier, scribe (no planner). Supports "planner is not a swarm role".
- `scripts/hyaku/lane-addendum.md:254-257` (orchestrator ruling 2026-10-19): "the validator rejects `planner` … You, the L1, hold the canonical §3 planner seat … Record that mapping in the report".
- Validator not run (NOT RUN: validator not invoked by this seat).

Verdict: the contract's shape line answers the mechanical question (the policy lists planner as a topology slot, not a swarm role) and discloses the mapping, which the addendum asks for. It does not close D1:
1. Nothing in the policy or the spec binds the L1 to the topology planner slot (`count:1`); "the L1 holds it" is the lane's self-assignment [INFERENCE], and the L1 wrote the contract and its own seat count.
2. The round-93 route for D1 was "operator (validator) and lane (disclose)". The lane half is done by the shape line; the operator half (validator behaviour, binding L1 to the planner slot) is not evidenced in round 94.
3. "No residual call" in the contract is wrong for D1; "residual: D1 operator-side, open" is accurate.

Keep D1 open and routed to the operator. Round-94 report must name the mapping (per addendum) and the open operator half.

## 4. Fixture choice (controls-r94.py)

`controls-r94.py:29` `FIXTURE_FILE = "corpus/knowledge/counter-win-r77.md"`; `FIXTURES` (lines 33-37) are three embeddings of its single admission hash. Facts from the base:
- `counter-win-r77.md`: verified-at on line 1, the earliest position.
- `drift-pin-r10.md`: verified-at on line 2. `rotation-schedule-r74.md`: verified-at on line 12, the last line the counter's `head_lines(n=12)` window reads.

Replay (my own driver, scratch clone only, same recipe as `controls-r94.py` lines 105-130; the frozen controls were not changed or run as the battery):
```
== drift-pin-r10.md ac=5be89432 verified-at_count=1 verified-at_line=2
CTRL drift-pin-r10.md left   v1: C1=met   ... adm_ok=19 adm_fail=0 ...  rev=b09126a16748
CTRL drift-pin-r10.md left   v2: C1=unmet ... adm_ok=18 adm_fail=1 ... checks_failed=admission
CTRL drift-pin-r10.md right  v1: C1=met ;  v2: C1=unmet checks_failed=admission
CTRL drift-pin-r10.md middle v1: C1=met ;  v2: C1=unmet checks_failed=admission
CTRL drift-pin-r10.md live v2: C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=84b152308fa6
== rotation-schedule-r74.md ac=dc50c80b verified-at_count=1 verified-at_line=12
CTRL rotation-schedule-r74.md left   v1: C1=met ;  v2: C1=unmet checks_failed=admission
CTRL rotation-schedule-r74.md right  v1: C1=met ;  v2: C1=unmet checks_failed=admission
CTRL rotation-schedule-r74.md middle v1: C1=met ;  v2: C1=unmet checks_failed=admission
CTRL rotation-schedule-r74.md live v2: C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=84b152308fa6
== counter-win-r77.md ac=6a230c4b verified-at_count=1 verified-at_line=1
CTRL counter-win-r77.md left/right/middle: v1 C1=met, v2 C1=unmet checks_failed=admission (all three)
CTRL counter-win-r77.md live v2: C1=met ... adm_ok=19 ...
```
Result: v1 false-passes 9/9 across three files; v2 rejects 9/9; live v2 met. The verdicts are not cherry-picked by file. The weakness is coverage: the frozen battery is one file, always at line 1, so it cannot distinguish a token rule from a line-position artifact, and it never exercises the 12-line head edge.

Required second replay file: **`corpus/knowledge/rotation-schedule-r74.md`** (TWELVE member, verified-at at the window edge, line 12). Also run `drift-pin-r10.md` (line 2, multi-line value). Record both as a named control-battery gap for the lesson; do not edit the frozen controls.

## Commands and cleanup
- NOT RUN: `ufo` validator; `.gitignore` patch (absent from `w1/patches/`); frozen `controls-r94.py` battery (not re-run here; receipt `evidence/controls-r94.txt`).
- No sysctl, service, pacman or PATH changes; no lane or fleet file written. Scratch removed.
