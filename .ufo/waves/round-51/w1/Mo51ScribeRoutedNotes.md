# Mo51ScribeRoutedNotes — round-50 routed defects (§5) and the 35 attempt-1 seats

Seat: scribe, leaf (no subagent). Assignment: draft, as a fenced block, the lesson section
`## Round-50 routed defects (spot-check §5) — dispositions` for
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-51.md`, from the round-50 spot-check §5 items 1-6
and the round-51 contract's `carriers` block, with carriers 1 → C1, 2 → round shape (one v2 wave `w1` after data,
as frozen), 3 → NOT done (successor calibration counter, K4 beyond SHONEN; routed to round 52 with the reason),
4 → the P-C2 entailment arm, 5 → deviations named in `LOG.md`, 6 → the operator's fleet-commit author date; and to
give a final disposition for the 35 attempt-1 seats with no report ("outcome unknown, not dead"), saying what is
knowable from `.ufo/waves/round-50/w1/` and `w1-dispatch.json`.

Posture: read-only. No lane file was edited, staged, committed or checked out; no mutating git or jj command ran
(`git log/show/ls-tree/rev-parse/grep/diff` only, all with explicit revisions); no fleet-root tracked file touched;
no subagent; no kernel log MESSAGE text read (the kill/oom path was not touched at all); no cgroup, sysctl, swap or
watermark read or changed; no OOM triggered; no `systemctl`/`journalctl --vacuum`. The one lane tool I ran,
`tools/mori-wave-settlement.py scan`, is documented read-only and writes only its stdout (I redirected it into my
own scratch). Nothing installed or upgraded (host-wide pacman pause respected; nothing was needed). Scratch:
`/fast/scratch/hyaku/mori-r51/Mo51ScribeRoutedNotes/` (`mkdir -p`, `TMPDIR` exported into it, removed at the end —
see §7). Every quoted byte below is re-derivable from committed bytes plus two host logs read (`.ufo/watchdog.log`
and `.ufo/state/inline-dispatcher.log`, both in the fleet root, neither written).

Per the seat rules I do not edit the lesson, `LOG.md`, `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `corpus/`,
`tools/` or `considerthese/`: the section is drafted fenced in §2 and the L1 integrates it.

## 1. Sources read (absolute paths)

| what | where |
|---|---|
| frozen contract (entering tip `aa3af1ec…`, freeze `4677910e…`, data `87e0c37…`) | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/contract.md` (147 lines) |
| round-50 closure, §5 routed defects at `:171-188` | `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-50-verifier-spotcheck.md` |
| round-50 lesson, routed-defect precedent at `:199-240`, round shape at `:250-260` | `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-50.md` (308 lines) |
| round-50 wave 1 payload, registry, report dir | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/{w1-dispatch.json,w1-spec.json,w1.ready,w1.ready.dispatched,w1/}` |
| round-50 wave 2 payload (counterpart names) | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/{a2w1-dispatch.json,a2w1-results.json}` |
| round-51 receipts | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/evidence/{c1-at-data.txt,c2-at-data.txt,control-c1-do-nothing.txt,control-c1-{scratch-only,witness}.txt,control-c2-do-nothing.txt,freeze-sha256.txt}` |
| round-51 wave payload + registry | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/{w1-dispatch.json,w1.ready.dispatched,w1/swarm-registry.json}` |
| counters | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-51/{count-c1.py,count-c2.py}` |
| landed data bytes | `git show 87e0c374537557754bf71dd68036ded3ddc6699c:tools/mori-pin-check.py`, `:…:.ufo/waves/round-40/conform.py`; working-tree `tools/mori-pin-check.py`, `tools/mori-wave-settlement.py` |
| entering bytes for the before-half | `git show aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd:tools/mori-pin-check.py`, `:…:.ufo/waves/round-40/conform.py` |
| fleet dispatcher records (read only) | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`, `/home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log`, `/home/vgpnk/Projects/shokunin/.scratch/goal-20261026-hyaku-run8.md` |
| fleet-owned commit script (read only) | `/home/vgpnk/Projects/shokunin/scripts/hyaku/fleet-commit.sh:84-85` |

## 2. Draft for `corpus/lessons/round-51.md` (fenced; L1 integrates)

````markdown
## Round-50 routed defects (spot-check §5) — dispositions

The round-50 closure routed six defects (`corpus/lessons/round-50-verifier-spotcheck.md:171-188`). Item by item:
what this round did, where the bytes are, and what stays open.

1. **`.scratch` producers → C1** (`round-50-verifier-spotcheck.md:173-175`). This is exactly this round's C1
   surface, and its predicate is the counter's docstring. At `87e0c374537557754bf71dd68036ded3ddc6699c` the counter
   prints `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0` exit 0
   (`evidence/c1-at-data.txt`), against `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1
   classified=bad selftest=pass=114,fail=0` exit 1 at the entering tip (`evidence/control-c1-do-nothing.txt`, whose
   residue line is `kill_residue_first: !! .scratch/pin-check-uphozg94/tree/.gitignore`). Both producers the
   closure named are changed:
   - `tools/mori-pin-check.py` — entering `:884` read `scratch_parent = os.path.join(repo, ".scratch")`; v5 makes
     the `--rev` export a `git clone -q --shared --no-checkout` plus `checkout -q --detach` under `--scratch DIR`,
     defaulting to the TMPDIR temp dir and "never `<repo>/.scratch`" (`tools/mori-pin-check.py:880-886,901,136-142`),
     and gives every mismatch line `class=env` or `class=stale` with the summary ending `env=N stale=N`, `env=2`
     `stale=2` over the frozen five-row fixture (`:136-142`).
   - `.ufo/waves/round-40/conform.py` — entering `:69-70` hardcoded `LANE = "/home/vgpnk/Projects/shokunin/
     mori-shokunin"` and `SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-40", "scratch")`; at the data
     commit `LANE` is four `dirname`s of `__file__` and `SCRATCH_ROOT = tempfile.gettempdir()`.
   What the claim does not cover, named before data: arm A kills at one moment only (3 s after the first write) and
   proves nothing about a kill at another moment; arm B hides one path (the lane) and does not prove portability to
   another host, user or kernel; arm C's fixture is five rows and its rule is "no tally line ⇒ env", so a tool that
   prints a tally and then fails environmentally is classed `stale`; and `--root` mode still writes
   `<root>/.scratch` (`tools/mori-pin-check.py:542`), so a closure that re-executes with `--root` against the lane
   refills it. The producer is closed on the `--rev` and `conform.py` paths the closure named, not on every path;
   the `--root` residue stays a named limit of the claim.

2. **Round shape → one v2 wave after the data, as frozen** (`round-50-verifier-spotcheck.md:176-178`). Measured
   against the contract (`contract.md:121-122,127-133`): wave `w1`, `counts={"spawn":68,…,"total":68}`, against the
   v2 policy band `waveMinLanes 64` / `waveMaxLanes 128`; registry created 19:42:41 and the wave stamped
   dispatched 19:48:42, both after the data commit `87e0c37…` (author 19:37:01, committer 19:37:45); one wave and no
   second; 68 is under the closure's 100-seat ceiling and under the contract's 128 cap; attack share is 29/68 = 43 %
   (reviewer 14, critic 12, mutation-tester 3) against the 25 % floor. The contract states two seat bands that part
   company above 100 (`:121-122` "w1 (64–100 seats)" versus `:129` "band 64–128"); 68 is inside both, and the
   disagreement can only bite on a residual call, where `LOG.md` must say which ceiling was used.

   **The 35 attempt-1 seats: outcome unknown, not dead.** The round-50 lesson already says "unknown (not dead, not
   complete)"; this round closes it with what the record actually holds. Knowable:
   - the wave ramped rather than spawning at once. `.ufo/state/inline-dispatcher.log:1569-1603` shows 21 spawned at
     05:50:20 and three seats deferred by the host job cap before the wave completed —
     `Mo50CritC2Counter` (05:52:27-05:54:27), `Mo50CritStagedClaims` (05:55:28-05:56:28) and
     `Mo50ConnConsiderthese` (05:57:49) — reaching `spawned mori 50 w1 40` at 05:58:49. So the
     `w1.ready.dispatched` stamp (05:58:49) is when the wave finished spawning, not when it started: the first
     landed report, `Mo50ScoutCoverageFR1.md`, was written 05:51:24, 7m25s earlier. `corpus/lessons/round-50.md:196`
     and `:252` read "dispatched … at 2026-10-26T05:58:49"; that is the stamp, and the wave ramped.
   - five reports exist, mtimes 05:51:24-06:08:03, all committed by the orchestrator salvage `9b8562a3`
     (`git log --diff-filter=A` per file → one commit).
   - the same log's live count for the wave falls 39/40 (05:59:19) → 38/40 (06:05:05) → 37/40 (06:09:06) and holds at
     37/40 through its last tick 06:22:15; it records no tick until 08:29:36, where the restarted dispatcher
     `adopted` the wave file and recorded no further spawn for it.
   - the L1 died in the host crash: `.ufo/watchdog.log:1518` `lane-dead-no-report mori round=50 … attempt 1 L1 died in
     the orchestrator host crash 2026-10-26 ~08:50 -03`, and `.scratch/goal-20261026-hyaku-run8.md:85` says the omp
     exit "ended every live agent: L1s SoujiR32, TabiR31, TameshiR48 and MoriR50, plus their seats".
   - settlement is filesystem shape only. `tools/mori-wave-settlement.py scan --lane-root <lane>` on the committed
     tree: `.ufo/waves/round-50/w1-dispatch.json members 40 … present 5, missing 35, stub 0, misrooted 0, unsafe 0,
     unparsed 0`; the tool's docstring says outright "A missing report is not a dead seat; this tool reports
     filesystem shape only" (`tools/mori-wave-settlement.py:18`).
   - no per-seat identity was recorded: `w1/swarm-registry.json` has `agentId: null` for all 40 members, and no
     `.ufo/waves/round-50/w1-results.json` exists; `a2w1-results.json` is attempt 2's, 64 seats and 64 results,
     written 10:50:12 — after the critic that reported it missing at 09:56, so that critic sentence was true when
     written and is stale now.
   - no per-seat remnant survives: all five landed reports name scratch under
     `/fast/scratch/hyaku/mori-r50/<seat>/`, and that root is gone today (`ls /fast/scratch/hyaku | grep mori` →
     `mori-r51` only). Attempt-2 seats removed their own scratch by design (`a2w1/Mo50bConnSalvage.md:11`), so
     absence today is not evidence that the root was never used.
   Not knowable, and not to be asserted: whether a named seat started, took a turn, wrote and lost a draft, or
   finished with nothing to show. The record keeps counts, not names; "unknown" is the finding, and "dead" would be
   an invention.
   The work itself was mostly re-attempted: 25 of the 35 items carry the same item name in `a2w1`, 8 more were
   re-tasked under a different name for the same intent (three quote inventories → six `RevRows*` reviewers;
   `ScribeRowCgroup`, `ScribeAxesCells`, `ScribeShonen` → the landed data plus `RevRowsCgroup*`, `RevAxesCells`,
   `RevShonen`; `ExecHostPaths` → `SentHostPaths`/`ExecMisrootSweep`; `ConnConsiderthese` → the considerthese lines
   in `ScribeLessonGate`/`RevPromptConformance`), and 2 were never re-attempted and left nothing:
   `Mo50ExecSelfassessTool` (a candidate standing C1 tool) and `Mo50ExecCensusMirror` (the scratch
   mirror-validation harness) — no `mori-selfassess-check.py` and no `mirror-validate.sh` anywhere in the tree at
   `87e0c37…`. Those two are dropped, not deferred, and the round-51 record says so.

3. **Successor C1 counter and K4 beyond SHONEN → not done this round; routed to round 52**
   (`round-50-verifier-spotcheck.md:179-181`). The contract routes it in as many words: "3 successor calibration
   counter and K4 beyond SHONEN → not claimed this round (stays routed to round 52, named in `LOG.md`)"
   (`contract.md:122-123`). The reason is the freeze rule itself — "A predicate, counter, floor or kill rule changed
   after any seat has scored is not the claim's rule" (`contract.md:6-7`) — and the round's two claims are
   operability (C1) and depth (C2); a successor calibration counter would be a calibration-axis instrument, and
   this round's C1 instrument reads no `SCORECARD.md`, no `## Axes` row, no Score cell and no `QUALITY.md`/`LOG.md`
   pin (`grep -c 'SCORECARD\|Axes' .ufo/waves/round-51/count-c1.py` → 0), so nothing here re-tests the five
   survivors the closure named or closes K4 outside `SHONEN.md` (round 50 closed K4 for `SHONEN.md` only,
   `corpus/lessons/round-50.md:230-235`). Both stay open; this sentence is the deviation `LOG.md` must carry under
   item 5.

4. **C2 entailment → the entailment arm of P-C2** (`round-50-verifier-spotcheck.md:182-183`). Implemented inside the
   frozen predicate: for every row of `corpus/knowledge/memavailable-estimate-r51.md`, the wave report files at R
   under `.ufo/waves/round-51/w1/` whose names do not start `MoriR51` must carry at least one vote line of the form
   `ENTAIL <h> entailed` and no dissent line `ENTAIL <h> overclaim`, where `<h>` is the first 12 hex of the sha256 of
   the row's claim cell with whitespace collapsed and ends stripped (`count-c2.py:14-18`, reader at `:117-130`, hash
   at `:113-114`). The votes are in flight as this is written: at the data commit the entry reads
   `claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0
   dissent=0` with `failed=entailment`, exit 1 (`evidence/c2-at-data.txt`) — located quotes with no recorded
   judgment do not meet P-C2. The wave pairs every row with two seats of different roles: seven reviewers
   `Mo51RevEntail01…19` (rows 1-3 each, 21/21) and four critics `Mo51CritEntail01…17` (rows 1-6, 7-11, 12-16, 17-21,
   21/21), a design seat `Mo51CritEntailArm`, and a hash-recomputation seat `Mo51ExecEntailHashTool`. The counter
   accepts one vote and no dissent, so "at least two seats of different roles" (`contract.md:131`) is a round-shape
   rule the predicate does not check — that gap is a named limit of P-C2, not something the L1 may close by editing
   a frozen counter. An `overclaim` blocks the row until the L1 replaces the claim text with text a
   non-L1 seat voted `entailed`; the old hash then matches no row and no vote line is ever deleted from a report.

5. **Contract deviations named in the record** (`round-50-verifier-spotcheck.md:184-185`). Rule for this round: a
   deviation from `contract.md` is named in `LOG.md` and in this lesson, in the same breath as the item it deviates
   from — not only in the lesson, which is the defect round 50 hit. The deviation the contract already commits to is
   item 3 above (a routed defect not worked). The carrier for the rest is `LOG.md`'s `## Round 51` entry; at
   drafting, `LOG.md` has no `## Round 51` heading (`grep -c '^## Round 51' LOG.md` → 0; its last entry is
   `## Round 50` at `:2732`), and the entry is being drafted by `Mo51ScribeLogScorecard`. Two candidate deviations
   the entry must state if they stand at filing: item 3 above, and the contract's own two seat bands (item 2) if a
   residual call takes the round past 100 seats.

6. **Fleet-owned author date → the operator's** (`round-50-verifier-spotcheck.md:186-188`). The mechanism is
   unchanged and is fleet code: `scripts/hyaku/fleet-commit.sh:84-85` stamps the author before committing —
   "`jj commit <paths>` keeps @'s author: stamp it first so author == committer", `jj metaedit --update-author` —
   and the stamp is the working-copy change's creation time, so a filing commit can be authored before the lane tip
   it cites. Round 50 shows both sides in one round: the first filing `4a20abb1` is authored 10:15:47 against a tip
   committed 10:54:21 (the defect), and the second filing `e9833c0f` is authored 10:54:42, after the tip. The lane
   cannot fix this, and this round claims nothing about it: the report records both values (its own author date and
   the cited lane tip's committer date) as the surface, the way round 50 did. Routed to the operator, unchanged.

Status of the six: 1 → the C1 claim; 2 → done as frozen, with the 35 attempt-1 seats closed as "outcome unknown,
not dead"; 3 → not done, routed to round 52 and named; 4 → the C2 claim's entailment arm; 5 → the rule plus this
entry's copy; 6 → operator's, unchanged.
````

## 3. Verification of every number and quote in the draft

Read, not rerun: `c1-at-data.txt` and `c2-at-data.txt` are the committed receipts for the data commit, so I did not
re-execute either counter to decorate this report. Working-tree reads are the entering tree at the time of writing
(no dependant file changed since `87e0c37…`: `git status --porcelain -- tools .ufo/waves/round-40/conform.py
corpus/lessons/round-51.md` → empty; `corpus/lessons/round-51.md` does not exist yet).

| draft claim | command | observed |
|---|---|---|
| C1 met at data, and the 4-arm line | `tail -3 .ufo/waves/round-51/evidence/c1-at-data.txt` | `classified: PIN_CHECK=unmet … env=2 stale=2` / `kill_residue_first: -` / `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=119,fail=0 rev=87e0c37… failed=-` / `exit=0` |
| C1 unmet before, with a residue path | `tail -4 .ufo/waves/round-51/evidence/control-c1-do-nothing.txt` | `C1=unmet kill_residue=12547 relocated=unmet reloc_mismatch=1 classified=bad selftest=pass=114,fail=0 rev=aa3af1ec… failed=kill_residue,relocated,classified` / `exit=1`; residue line `kill_residue_first: !! .scratch/pin-check-uphozg94/tree/.gitignore` |
| pin-check entering `:884` writes `<repo>/.scratch` | `git show aa3af1ec:tools/mori-pin-check.py \| sed -n '878,892p'` | `scratch_parent = os.path.join(repo, ".scratch")` then `mkdtemp(prefix="pin-check-", dir=scratch_parent)` |
| v5 export is a shared clone in `--scratch`, default TMPDIR | `git show 87e0c37:tools/mori-pin-check.py \| sed -n '880,940p'`; `sed -n '135,143p;542p;901p' tools/mori-pin-check.py` | `git clone -q --shared --no-checkout … checkout -q --detach`; `--scratch` help "v5: never `<repo>/.scratch`"; `tmp_parent = os.path.join(root, ".scratch")` (the `--root` residue); docstring v5 note at `:135-143` |
| conform.py entering hardcodes the lane, scratch inside it | `git show aa3af1ec:.ufo/waves/round-40/conform.py \| sed -n '60,75p'` | `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`, `SCRATCH_ROOT = os.path.join(LANE, ".ufo", "waves", "round-40", "scratch")` at `:69-70` |
| conform.py at data derives the lane and uses TMPDIR | `git show 87e0c37:.ufo/waves/round-40/conform.py \| sed -n '55,85p'` | `LANE = os.path.dirname(×4 of __file__)`, `SCRATCH_ROOT = tempfile.gettempdir()` with the round-51 comment |
| round-51 wave is 68 spawns, band 64–128 | `python3 -c 'import json;d=json.load(open(".ufo/waves/round-51/w1-dispatch.json"));print(d["counts"],d["policy"])'` | `{"spawn":68,"resume":0,"total":68}`; `waveMinLanes 64`, `waveMaxLanes 128`, `hardCeiling 256` |
| ROLE SPLIT / attack share | same registry: `collections.Counter(role)` | executor 18, reviewer 14, critic 12, scribe 9, sentinel 4, mutation-tester 3, connector 3, scout 2, simplifier 2, revenger 1 → (14+12+3)/68 = 42.6 % |
| wave is after the data commit | `head -1 .ufo/waves/round-51/w1.ready.dispatched`; `git log -1 --format='%aI %cI' 87e0c37`; `tail -1 w1/swarm-registry.json` createdAt | stamp `2026-10-26T19:48:42`; data `19:37:01` / `19:37:45`; registry `2026-10-26T22:42:41.150Z` (= 19:42:41 -03) |
| freeze precedes the wave | `git show --stat --format='%h %aI' 4677910e` | `4677910e 2026-10-26T11:09:49-03:00`, 22 files, counters + controls + copies + receipts |
| contract states two bands (64–100 vs 64–128) | `.ufo/waves/round-51/contract.md:121-122,129` (read) | `w1 (64–100 seats) … total <= 128` / `band 64–128` |
| 40 attempt-1 spawns, 5 reports, 35 missing | `python3 -c '…w1-dispatch.json counts'`; `ls .ufo/waves/round-50/w1/*.md`; `python3 tools/mori-wave-settlement.py scan --lane-root <lane>` | `{"spawn":40,…,"total":40}`; five `.md` files; `…w1-dispatch.json members 40 … "present":5,"missing":35,"stub":0,"misrooted":0,"unsafe":0,"unparsed":0` |
| report mtimes and the add commit | `stat -c '%y %n' .ufo/waves/round-50/w1/*.md`; `git log --diff-filter=A --format='%h %aI' -- <file>` | 05:51:24 (ScoutCoverageFR1), 06:01:23 (RowOomKill), 06:02:48 (EntryB), 06:06:31 (RowMemcontrol), 06:08:03 (EntryA); each added by `9b8562a3` |
| the ramp, the three cap deferrals, 40/40 at 05:58:49 | `grep -n 'round-50/w1.ready\|mori/w1' .ufo/state/inline-dispatcher.log` | 21 spawned @05:50:20 → 25 @05:50:57 → 26 @05:51:27…05:54:27 → 29 @05:55:28 → 38 @05:57:49 → `1603: spawned mori 50 w1 40` @05:58:49; `spawn-cap … Mo50CritC2Counter` (05:52:27, 05:53:27, 05:54:27), `Mo50CritStagedClaims` (05:55:28, 05:56:28), `Mo50ConnConsiderthese` (05:57:49) |
| live counts and their stop | same log, `mori/w1: live` transitions | 39/40 @05:59:19, 38/40 @06:05:05, 37/40 @06:09:06 … 37/40 @06:22:15 (last tick); next record 08:29:36 `adopted …/round-50/w1.ready` |
| no re-spawn of w1 after the crash | `grep -n 'spawned mori 50' <.ufo/state/inline-dispatcher.log>` | only `:1603` (w1, 05:58:49) and `:1786` (a2w1, 09:50:39) |
| registry agent ids null, no results file | `python3 -c '…swarm-registry.json members'`; `ls .ufo/waves/round-50/*.json`; `python3 -c '…a2w1-results.json'` | 40 members, `agentId non-null 0`; `a2w1-dispatch/a2w1-results/a2w1-spec/w1-dispatch/w1-spec` — no `w1-results.json`; `a2w1-results.json` has `seats=64`, `results=64` |
| the attempt-2 seat's own claim about the results files | `grep -n 'a2w1-results.json' .ufo/waves/round-50/a2w1/Mo50bCritRoundShape.md`; `stat -c %y .ufo/waves/round-50/a2w1-results.json`; `git log -1 --format='%h aI=%aI cI=%cI' -- …/a2w1-results.json` | `:65` "Neither `w1-results.json` nor `a2w1-results.json` exists"; true at the seat's 09:56 read, false from the file's mtime `10:50:12`; add-commit `bae8656e aI=09:31:37 cI=10:52:00` |
| scratch root gone; reports name it | `ls -d /fast/scratch/hyaku/*/`; `grep -o '/fast/scratch[^ )`"]*' .ufo/waves/round-50/w1/*.md` | roots: `mori-r51`, `tameshi-r50`, … no `mori-r50`; reports name `/fast/scratch/hyaku/mori-r50/Mo50ScribeEntryA` etc. |
| attempt-2 seats removed their own scratch | `sed -n '1,15p' .ufo/waves/round-50/a2w1/Mo50bConnSalvage.md` | "Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bConnSalvage/` (removed at the end…)" |
| 25 / 8 / 2 split of the 35 | `python3` set difference of `Mo50*` vs `Mo50b*` suffixes over the two dispatch payloads | 25 exact-name counterparts; 10 not: 8 with same-intent different-name seats (3 quote inventories → `RevRowsCgroupA/B`, `RevRowsMemcgA/B`, `RevRowsOomA/B`; `ScribeRowCgroup`; `ScribeAxesCells` → `RevAxesCells`; `ScribeShonen` → `RevShonen`; `ExecHostPaths` → `SentHostPaths`+`ExecMisrootSweep`; `ConnConsiderthese`); 2 with none (`ExecSelfassessTool`, `ExecCensusMirror`) |
| the two dropped tools do not exist | `git ls-tree -r --name-only 87e0c37 \| grep -iE 'mirror-validate\|selfassess'`; `ls tools/ \| grep -iE 'selfassess\|mirror'` | only `.ufo/waves/round-46/w1/CritSelfAssessment.md` and `.ufo/waves/round-50/assimilation/a2/mirror-validate.txt` (attempt-2 L1 output, header says "L1 MoriR50a2"), no harness |
| C2 at data: 21 rows, located, `failed=entailment` | `cat .ufo/waves/round-51/evidence/c2-at-data.txt` | `C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c37… failed=entailment` / `exit=1` |
| — before | `head -3 .ufo/waves/round-51/evidence/control-c2-do-nothing.txt` | `C2=unmet claims=0 … failed=entry_absent,pins` / `exit=1` |
| the arm's reader, hash, dir, prefix | `.ufo/waves/round-51/count-c2.py:14-18,113-130` (read) | docstring arm sentence; `claim_hash = sha256(ws-collapsed, strip)[:12]`; `ENTAIL_DIR = ".ufo/waves/round-51/w1/"`; `if name.startswith(L1_PREFIX) or not name.endswith(".md"): continue` |
| entailment seat pairing (2 votes/row, different roles) | `python3` over `w1-dispatch.json` task text | Rev01 1-3, Rev04 4-6, … Rev19 19-21; Crit01 1-6, Crit07 7-11, Crit12 12-16, Crit17 17-21 |
| round-51 C1 reads no Axes/Score/K4 surface | `grep -c 'SCORECARD\|Axes' .ufo/waves/round-51/count-c1.py` | `0` |
| `LOG.md` has no round-51 entry | `grep -c '^## Round 51' LOG.md`; `grep -n '^## Round 50' LOG.md` | `0`; `2732:## Round 50 (…)` |
| fleet-commit mechanism | `grep -n 'metaedit --update-author' scripts/hyaku/fleet-commit.sh` | `84:  # \`jj commit <paths>\` keeps @'s author: stamp it first so author == committer.` / `85:  jw metaedit --update-author …` |
| round-50 filings' author vs committer | `git log --format='%H ad=%aI cd=%cI' -2 -- .ufo/reports/round-50/mori.md` (fleet repo) | `4a20abb1 ad=10:15:47 cd=10:54:42`; `e9833c0f ad=10:54:42 cd=10:54:59` |
| spot-check anchors | `grep -n '^## 5\|^1\. \*\*`' corpus/lessons/round-50-verifier-spotcheck.md` | §5 at `:171`; items at `:173,176,179,182,184,186` |

## 4. The 35 attempt-1 seats — what is knowable, laid out

Population: 40 dispatched names in `.ufo/waves/round-50/w1-dispatch.json` `taskCall.tasks`, 5 with a report on disk
(`Mo50ScoutCoverageFR1`, `Mo50ScribeEntryA`, `Mo50ScribeEntryB`, `Mo50ScribeRowMemcontrol`, `Mo50ScribeRowOomKill`),
35 without.

| class of fact | source | holds |
|---|---|---|
| dispatch count | `.ufo/waves/round-50/w1.ready` (`{"…","wave":"w1","dispatch":…}`), `w1.ready.dispatched` (`2026-10-26T05:58:49`), dispatcher `:1603` `spawned mori 50 w1 40` | 40 items authored and spawned |
| ramp and deferrals | dispatcher `:1569-1603` | 21 spawned by 05:50:20; deferrals name `Mo50CritC2Counter`, `Mo50CritStagedClaims`, `Mo50ConnConsiderthese`; 40/40 at 05:58:49 |
| per-seat outcome | `w1/swarm-registry.json` (40 `agentId: null`), absence of `w1-results.json`, settlement scan (`present 5 missing 35`) | **not recorded for any seat**, reported or not |
| per-seat activity | dispatcher live counts 39→38→37/40 (05:59:19-06:22:15) | counts only, no names; at least three runs ended by 06:09:06, which ones is not recorded |
| death of the wave's parent | `.ufo/watchdog.log:1518`, `.scratch/goal-20261026-hyaku-run8.md:85` | the L1 and "their seats" ended at the ~08:50 omp exit |
| per-seat artifacts | `ls -d /fast/scratch/hyaku/*/` | no `mori-r50` root survives; the reports name their scratch under it |
| successor work | `a2w1-dispatch.json` name/intent match | 25 same-name, 8 same-intent other-name, 2 none |

Disposition, in the words the lesson should use: **outcome unknown, not dead**. The strongest supportable negative is
"no report on disk"; the record contains no per-seat identity, no result code and no surviving scratch, so a seat
that finished with nothing, a seat that never took a turn, and a seat killed mid-write are indistinguishable. Any
sentence that says these seats "failed", "died" or "were idle" is unsupported.

## 5. Conflicts with material already committed

1. `corpus/lessons/round-50.md:196` and `:252` date the wave "at 2026-10-26T05:58:49". That is the
   `w1.ready.dispatched` stamp and the dispatcher's `spawned … 40` line, i.e. the end of the ramp; the wave file was
   ready at 05:49 and 21 seats had spawned by 05:50:20, and a landed report predates the stamp by 7m25s. Verified
   against `.ufo/state/inline-dispatcher.log:1569-1603`, `stat -c %y` of the five reports and
   `inline-dispatcher.log:1603`.
   The round-51 lesson should say "stamped dispatched" or give the ramp, not "dispatched at 05:58:49".
2. `a2w1/Mo50bCritRoundShape.md:65` says "Neither `w1-results.json` nor `a2w1-results.json` exists (`ls` → No such
   file or directory, both)." True at that seat's 09:56 read; false from 10:50:12, when
   `.ufo/waves/round-50/a2w1-results.json` was written (64 seats, 64 results; sha256 `1f630cb7…`, identical to the
   committed bytes). The round-51 lesson must not repeat it. (The file is deliberately not edited; this is the
   correction.) The file's own history also shows the item-6 skew inside the lane: its add-commit `bae8656e` has
   author date `09:31:37` and committer date `10:52:00`, while the file was written `10:50:12` — so no lesson may
   date a2w1's integration from that commit's author date.
3. `contract.md:121-122` says the wave is "`w1` (64–100 seats) … total <= 128"; `contract.md:129` says "band
   64–128". Both are in the frozen file. 68 seats sit inside both, so no reading of the claim is affected — but a
   residual call between 101 and 128 seats would satisfy one sentence and breach the other, and `LOG.md` must say
   which was applied (draft item 5).
4. The round-50 closure's item 2 asks to "keep within the 100-seat ceiling"; the round-51 contract restates the cap
   as 128 in its carriers line and 100 in the wave-shape line. Same tension as (3), recorded once.
5. `corpus/lessons/round-50.md:196` also cites the settlement line as `members=40 … present=5, missing=35`, which
   reproduces exactly today; the round-51 lesson may cite it as a re-derivable fact.

## 6. Out of scope / not checked

- I did not run `count-c1.py` or `count-c2.py` at any revision: both receipts are committed and re-running them is
  the executors' and the closure's work, not the scribe's.
- I did not open the five attempt-1 reports' content beyond counting sibling references and scratch paths; the
  salvage audit is `a2w1/Mo50bConnSalvage.md`.
- I did not check the bwrap arm, the mutation set, or the freeze-sha256 list against the working tree (C1's and the
  sentinel's items).
- I did not read any kernel log; no cgroup, sysctl or swap surface was touched.
- `considerthese/2026-10-26.md` (suggestion 1 → C1 arm C) was read only through the contract and the pin-check
  docstring, not as a file.
- The seven rounds' `LOG.md`/`SCORECARD.md` drafts belong to `Mo51ScribeLogScorecard`; I only state what its entry
  must carry (draft items 3 and 5).

## 7. Scratch

`/fast/scratch/hyaku/mori-r51/Mo51ScribeRoutedNotes/` was created with `mkdir -p`, `TMPDIR` was exported into
`…/tmp` for the one tool run (`mori-wave-settlement.py scan`), and the one file written there (`scan.json`) was
read for the two settlement lines and then removed with the whole scratch tree before this report was written.
Disk guard before the run: `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` →
`/fast/scratch/hyaku 26% 601.6G free` (no ENOSPC risk; nothing written outside scratch and this report).

## Findings

1. **MED — `corpus/lessons/round-50.md:196,252` date the attempt-1 wave from its spawn-completion stamp.**
   `.ufo/waves/round-50/w1.ready.dispatched` = `2026-10-26T05:58:49` and dispatcher `:1603` records
   `spawned mori 50 w1 40` at that second, but the log shows the wave ramping from ~05:49 (21 spawned at 05:50:20)
   and `Mo50ScoutCoverageFR1.md` has mtime 05:51:24 — 7m25s before the stamp. The round-51 lesson must not copy
   "dispatched at 05:58:49" as a start time.
2. **MED — the 35 attempt-1 seats cannot be given a per-seat outcome from any committed byte.** 40/40 registry
   entries have `agentId: null`, no `w1-results.json` exists, the settlement tool reports filesystem shape only
   (`tools/mori-wave-settlement.py:18`) and the `/fast/scratch/hyaku/mori-r50` root is gone. "Outcome unknown, not
   dead" is the strongest supportable statement; the draft states it and forbids "dead/failed/idle".
3. **MED — the `.scratch` producer is closed only on `--rev`, not on `--root`.** `tools/mori-pin-check.py:542`
   still sets `tmp_parent = os.path.join(root, ".scratch")`, so a closure or a seat that re-executes with `--root`
   against the lane refills the tree the round-50 closure asked to be freed. The contract names this before data
   ("`--root` mode still writes temp dirs under `<root>/.scratch` (unchanged; not claimed)"), so it is a limit, not
   a breach — but the round-51 lesson must carry it in item 1 rather than reading routed defect 1 as fully closed.
4. **MED — the P-C2 entailment arm accepts one vote, while the frozen round shape asks two seats of different
   roles.** `count-c2.py:117-130` counts a row entailed when any non-`MoriR51` `.md` file in
   `.ufo/waves/round-51/w1/` carries the row's hash as `entailed` and none carries `overclaim`. The wave pairs
   every row with a reviewer and a critic (7+4 seats, 21 rows each), but a wave that lost all critics would still
   meet the predicate. Named limit for the closure; the predicate is frozen and is not to be changed this round.
5. **LOW — `a2w1/Mo50bCritRoundShape.md:65` says `a2w1-results.json` does not exist.** True at that seat's 09:56
   read; the file was written 10:50:12 with 64 seats/64 results, so the sentence is stale. The round-51 lesson must
   not repeat it.
6. **LOW — a lane commit carries a change-creation author date 80 minutes before its content.**
   `bae8656e` (round-50 integration) is authored `09:31:37` and committed `10:52:00`, while
   `.ufo/waves/round-50/a2w1-results.json` inside it has mtime `10:50:12` and its content quotes a dispatcher tick
   at `09:55:56`. This is the in-lane analogue of routed defect 6: no lesson may date the a2w1 integration, or any
   file first added by it, from an author date.
7. **LOW — `contract.md:121-122` and `:129` disagree on the wave's upper band (64–100 vs 64–128).** 68 seats are
   inside both, so no measurement is affected; a residual call would have to name which ceiling it obeyed
   (`LOG.md`, draft item 5).
8. **LOW — two attempt-1 items were never re-attempted and left nothing:** `Mo50ExecSelfassessTool` (candidate
   standing C1 tool) and `Mo50ExecCensusMirror` (mirror-validation harness). Neither `mori-selfassess-check.py` nor
   `mirror-validate.sh` exists anywhere at `87e0c37…`. The D-b disposition should say "dropped", not "deferred", for
   these two.
9. **LOW — the `1 -> C1` carrier is broader than the two files the closure named.** The claim's arms A/B/C/D hold,
   but routed defect 1 also asked that "re-executions are hermetic (D-d)"; hermeticity is proven for one lane path
   hidden (arm B) and one kill moment (arm A), not for the lane's other host-path instruments. The relocation sweep
   item in the round shape is where the rest is checked; the lesson should not read C1 as sweeping them.
