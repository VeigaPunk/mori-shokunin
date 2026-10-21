Verdict: PARTIAL. Per-dispatch-file counts HOLD (0 differences). Lane-level revenger settlement is BROKEN (three attacks survive: §4.1, §4.2, §4.4).

# LiveRevenger: C2 falsification on lane `revenger-shokunin` (round 20)

Times are UTC; local is -03:00.

## 0. Summary

- **Per-dispatch-file counts: HOLDS.** The lane has one `ufo-swarm-wave-dispatch-v1` file. The live scan, the wave-1 GT (`build/GtLaneRevenger.md`) and the committed fleet scan (`evidence/c2-live-fleet.json`) agree on every field that both sides record: 1 wave, 32 members, 0 present, 32 missing, 0 misrooted, 0 empty, 0 unparsed, 0 unsafe, 8 ignored JSON, 0 unreadable JSON, state `unsettled`, exit 1. Zero numeric differences. No lane change since any snapshot (§3).
- **Lane-level settlement: BROKEN.**
  1. **Exit 0 with no visible dispatch.** A lane with no discoverable dispatch JSON exits 0. A readable-but-not-searchable dispatch directory silently drops its JSON. Scratch copies reproduce both (§4.1).
  2. **The lane's live dispatch is invisible.** `kaika-r1/dispatch.md` (2026-10-19, 10 members, one batched call) is a markdown receipt. Its 10 declared writes all exist with real content. Neither the tool nor the GT counts it (§4.2).
  3. **The 32 counted seats were never dispatched**, yet the tool reports them as an `unsettled` wave with 32 missing reports (§4.4).
- Tool installs or updates: none. Subagents: none. Lane files edited: none.

## 1. What was run (all read-only on the lane)

| Step | Command or check | Result |
|---|---|---|
| Assigned scan | `python3 tools/mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/revenger-shokunin --fleet-root /home/vgpnk/Projects/shokunin --out .ufo/waves/round-20/falsify/LiveRevenger/scan.json` | rc **1**; scan.json 3616 B, sha256 `045303d9…8971` |
| Determinism | same command to `/tmp/LiveRevenger-rerun.json` | rc **1**; `cmp` identical; same sha256 |
| Tool under test | `tools/mori-wave-settlement.py` | 689 lines; sha256 `e5c06dad…8a48`; mtime 2026-10-21T11:04:26.834Z |
| Dispatch file | `.ufo/waves/fleet-round-1-interactive/rendered-undispatched.json` | sha256 `ec7a98e1…2917d9f`, equals `sha256sum` of raw bytes; `dispatch_sha256` in scan.json equal |
| Report paths | 32 names at `revenger-shokunin/.ufo/waves/fleet-round-1-interactive/reviews/<n>.md` and at `shokunin/.ufo/waves/fleet-round-1-interactive/reviews/<n>.md` (`os.path.lexists`) | none present in either root; the `reviews/` directory is absent in both |
| Independent recomputation | own lstat chain under the frozen rules, compared with scan.json per member | 32/32 `missing`, identical to live |
| Scratch mutations | copies of the lane's `.ufo/waves` under `falsify/LiveRevenger/mut/` and `mut2/`, each scan using an empty fleet root (§5) | as tabled |
| Frozen oracle | `frozen/c2-expected.json` | read for case `ids` only (14 ids; no zero-wave or unreadable-entry case) |

Not run: `--selftest`, `tools/mori-census.sh`, lane selftests, a fleet-wide search for misrouted copies (GT §6 already covers this; not repeated).

## 2. Per-dispatch-file comparison

File: `.ufo/waves/fleet-round-1-interactive/rendered-undispatched.json` (the only dispatch-schema JSON on the lane).

| Field | Live scan (`scan.json`) | Wave-1 GT (`GtLaneRevenger.md`) | Committed fleet (`c2-live-fleet.json`, `lanes[lane=="revenger-shokunin"]`, :404–408) | Result |
|---|---|---|---|---|
| dispatch files | 1 | 1 (§1, §2) | 1 (`dispatch_filename_flags` :11–14) | same |
| wave id | `revenger-r1-interactive-audit` | same (§2) | not recorded | same |
| members | 32 | 32 (§2); 32-row table (§4) equal to live row for row: name, agent, order | 32 | same |
| agents | reviewer 17, critic 12, sentinel 1, scribe 1, connector 1 | same (§4) | not recorded | same |
| present | 0 | 0 | 0 | same |
| missing | 32 | 32 | 32 | same |
| empty | 0 | 0 | 0 | same |
| misrooted | 0 | 0 | 0 | same |
| unparsed / unsafe | 0 / 0 | 0 / 0 | 0 / 0 | same |
| stub | 0 | no stub category; 0 files exist (`present` 0 in §3) | field absent | not comparable (0 by inspection) |
| state | `unsettled` | `unsettled` (§2, §3) | `exit` 1 only, no state field | same on exit |
| exit | 1 | "would exit 1" (§3, flagged as hand-applied) | 1 | same |
| ignored JSON | 8 | 8 (§3) | field absent | same / not comparable |
| unreadable JSON | 0 | 0 | 0 | same |
| waves | 1 | 1 | 1 | same |
| name hint | `undispatched-name:undispatched` | "filename suggests never dispatched: yes" (§2) | flagged in `dispatch_filename_flags` | same |
| dispatch sha256 | `ec7a98e1…2917d9f` | not recorded | not recorded | n/a (verified against `sha256sum`) |

Also verified against GT §1: all nine `.ufo/waves` JSON sizes equal the GT table (35955, 12826, 3259, 2981, 1022, 13941, 1681, 1670, 38123). GT's "27 entries" counts the `.ufo/waves` root; my walk gives 26 below the root (2 subdirectories plus 24 files), plus the root. GT §2 claims (counts 32/0/32, `resumeSends: []` at line 611, schema at line 2, 32/32 trailers equal to the template) are all confirmed. GT §5 citations (`wave-plan-run.json:6`, `routing-contract.json:2,3,4,7,8,9`) are confirmed line for line. GT found no error in its numbers. Its gap is scope: §7.2 records `kaika-r1/` as "0 members" without opening `kaika-r1/dispatch.md`.

## 3. Differences explained

- **Numeric differences: none.** Every field both sides record matches (table above). Nothing needs a live-change or tool-error explanation.
- **Fields the committed scan does not carry:** `stub`, `state`, `ignored_json`, `name_hint`, `dispatch_sha256`, `duplicate_*`. The committed revenger entry has only `empty, exit, lane, members, misrooted, missing, present, unparsed, unreadable_json, unsafe, waves`. The wrapper schema is `mori-r20-c2-fleet-live-v1` (c2-live-fleet.json:193 `lanes` array). This is a coverage gap in the committed artifact, not a disagreement.
- **Live lane change since the snapshot: none.** Timeline from `stat`/`os.lstat`:

| Artifact | mtime (UTC) | Meaning |
|---|---|---|
| `build/GtLaneRevenger.md` | 2026-10-21T10:34:39.380Z | GT last write; snapshot is at or before this |
| `evidence/c2-live-fleet.json` | 2026-10-21T10:46:53.060Z | committed fleet scan |
| `tools/mori-wave-settlement.py` | 2026-10-21T11:04:26.834Z | tool last changed; after both of the above |
| `falsify/LiveRevenger/scan.json` (first run) | 2026-10-21T11:00:36.375Z | ran on the pre-11:04:26 tool bytes |
| `/tmp/LiveRevenger-rerun.json` | 2026-10-21T11:06:57.829Z | ran on the 11:04:26 tool; byte-identical output |
| `revenger/.ufo/waves/fleet-round-1-interactive/rendered-undispatched.json` | 2026-10-15T05:07:52.794Z | dispatch JSON, bytes unchanged (35955 B) |
| `revenger/.ufo/waves/fleet-round-1-interactive/` (dir) | 2026-10-15T05:09:41.346Z | latest JSON write on the lane |
| `revenger/.ufo/waves/kaika-r1/` (15 files) | 2026-10-19T22:35:51.423Z (spread 0.289 ms) | bulk materialisation (§4.3) |
| `revenger/.ufo/waves/` (dir), lane root | 2026-10-19T22:35:51.423Z | same instant as kaika-r1 |
| `revenger/.ufo/` (dir) | 2026-10-15T05:13:42.105Z | unchanged |

  GT lists the `kaika-r1` files, so the GT snapshot is at or after 2026-10-19T22:35:51Z. Nothing in the lane is newer than that. Any snapshot between that instant and now has no lane change to explain. [INFERENCE: mtimes are honest; a timestamp-preserving copy would hide an edit.]
- **Tool change since the snapshot: explained, no effect on revenger.** The tool file changed at 11:04:26Z, after the committed scan (10:46:53Z) and after the GT (10:34:39Z). My first scan (11:00:36Z) ran on the earlier bytes; the rerun (11:06:57Z) ran on the current bytes. The outputs for revenger are byte-identical (sha256 `045303d9…8971`). [INFERENCE: the committed fleet file was produced by a tool version before 11:04:26Z; it records no tool sha, so this is not proven. Numbers for other lanes in that file were not re-verified.]

## 4. Attacks and results

### 4.1 Exit 0 with no visible dispatch (BROKEN)

Evidence: scratch S1, S9, S10, S11 (§5). Code:

- `scan_lane` `tools/mori-wave-settlement.py:317–318`: no waves root gives `paths = []`.
- `scan_lane` `:366`: `rc = 0 if all(wave["state"] in ("settled","no-spawn") for wave in waves) else 1`. `all([])` is `True`, so zero waves exit 0.
- `_wave_root` `:86–87` (ENOENT returns None) and `:90–91` (symlink or non-directory returns None).
- `_dispatch_files` `:111–114`: an `OSError` other than ENOENT on a `*.json` entry is skipped with `continue`. It is counted as neither `ignored_json` nor `unreadable_json`. A readable but non-searchable directory (mode 0644) triggers this: scratch S9 gives rc 0, `waves` 0, `ignored_json` 0 (was 8).

Contract: `contract.md:64–67` requires every regular `*.json` under `.ufo/waves/` to be discovered, or counted as `ignored_json` or `unreadable_json`. `contract.md:87–88` exits 0 when "every discovered wave" settled, which is vacuous when none is discovered. The frozen oracle's 14 ids (read: `all-present`, `one-missing`, `none-present`, `empty-report`, `misrooted`, `malformed-dispatch`, `no-trailer`, `traversal`, `absolute-path`, `symlink-report`, `other-schema-ignored`, `no-spawn`, `content-not-emitted`, `deterministic`) include no zero-wave or unreadable-entry case. The refinement cases (`:39–51`) each yield one wave, except r4 which yields two. So no test covers this.

Revenger consequence: removing the file whose name reads "undispatched" gives rc 0, `waves` 0, `states` `{}`, while the live 10-member receipt stays invisible. [INFERENCE: this is the cleanup the name invites.] S9 is a tool error against the contract's own discovery wording, not only vacuity.

### 4.2 The live 10-member dispatch is invisible (BROKEN, coverage)

Evidence (`kaika-r1/dispatch.md`, 30 lines):

- `:3–4`: "Dispatched 2026-10-19 by L1 `W2RoundRevenger` in ONE batched native `task` call: 10 members."
- `:9–20`: table of 10 members with sole-write paths.
- `:25–30`: a routing note saying the earlier fleet round-1 blocker (`MISSING_BINDING`) "was a property of the prior dispatch contract". The file has no closure or failure note.

On disk (existence and size checked, headers read, contents not reviewed):

| Declared sole write | Size (B) | Header |
|---|---|---|
| planner.md | 18443 | "# Revenger — kaika continuation pl…" |
| connector.md | 14254 | "# Sibling Overlap and Connection Sca…" |
| exec-lang-ledger.md | 5975 | "# exec-lang-ledger — verify_icon_l…" |
| exec-multi-ledger.md | 5179 | "# exec-multi-ledger — C1 fix: corp…" |
| e3-sources.md | 7768 | "# e3 sources — ExecForensicKnowled…" |
| e4-sources.md | 4944 | "# e4-sources — proposed corpus/SOU…" |
| scribe-pointer-audit.md | 16034 | "# Scribe pointer audit — revenger…" |
| scout-freshness.md | 3067 | "# Scout freshness sweep — RevScout…" |
| reviewer-oracle.md | 14603 | "# Reviewer oracle — C1 saved-ledge…" |
| critic-claims.md | 10970 | "# Claim-set critique — C1–C3" |

All six declared corpus writes exist (`corpus/verify_icon_languages.py` 9721 B, `corpus/verify_multi_icon_states.py` 9815 B, and four `corpus/knowledge/*.md` at 10640–14755 B). Four further `-post` files are not in the receipt: `critic-post.md` (5558 B), `mutation-post.md` (2746 B), `mutation-post-l2.md` (8152 B), `reviewer-post.md` (10753 B).

Discovery excludes all of this: `_dispatch_files` `:120` accepts `.json` only, and `scan_lane` `:333` requires the dispatch schema. GT §7.2 says "0 members" without opening `dispatch.md`. [INFERENCE: a receipt-aware existence check would report 10 of 10 declared writes present. No tool computes that, and receipts carry no trailers to test.]

### 4.3 Provenance caveat (INFERENCE)

All 15 `kaika-r1` files share one instant: 2026-10-19T22:35:51.423Z, spread 0.289 ms (`connector.md` at .423602366, the rest at .423890958). The `.ufo/waves` directory and the lane root carry the same instant. Ten members running for minutes would not produce writes within 0.3 ms of each other. This looks like a bulk copy, restore, or harness flush. The mtimes cannot attribute these files to member execution, and C2 cannot either.

### 4.4 Never-dispatched rendering counted as unsettled (BROKEN, semantic)

Evidence that the 32 seats were never dispatched:

- `fleet-round-1-interactive/wave-plan-run.json:6`: `"dispatch_started": false`.
- `routing-contract.json:2–4`: verdict `could-not-evaluate`, finding `required_role_alias_binding_missing`, exit_code 2.
- `routing-contract.json:7–9`: `planned_lanes` 32, `dispatched_lanes` 0, `registry_persisted` false.
- `routing-assessment-run.json:11–12`: exit_code 2, stdout `MISSING_BINDING role=reviewer …`.
- `rendered-undispatched.json:611`: `"resumeSends": []`.
- `kaika-r1/dispatch.md:25–30`: the blocker "was a property of the prior dispatch contract" [INFERENCE: `rendered-undispatched.json` is superseded by kaika-r1].

Tool: `_summarize_wave` `:279–288` labels a wave with 0 present as `unsettled`. `:292` and `:301` add a name hint, `undispatched-name:undispatched`, which is informational only. S8 (renaming the file) changes nothing except `dispatch_path` and `name_hint`. Contract `:79` defines `unsettled` as "0 present, ≥1 member". There is no never-dispatched state. So fleet `missing` totals include 32 seats that were never asked to report (committed revenger entry `missing: 32`). GT §7.1 flagged this. I confirm it is a meaning error, not a count difference between tool and GT.

### 4.5 Duplicate dispatch copies double-count (BROKEN for totals; not present on revenger today)

S6: a byte-identical copy under another name gives `waves` 2, `members` 64, `missing` 64, `unique_dispatch_sha256` 1, and `duplicate_of` set on the second wave only. Code: `scan_lane` `:344–353` sums every wave into the totals. Only the sha count (`:355`) dedupes. [INFERENCE: the committed fleet list flags tabi copies under `.ufo/waves/round-20/final-clones/…`; if they carry the dispatch schema they would be counted the same way, which could inflate tabi's `members` 3932. Not verified.]

### 4.6 Unreadable subdirectory: rc 2 with a misattributed message (minor, fail-closed)

S7: `reviews/` chmod 000 gives rc 2 with stderr `mori-wave-settlement: lane root is unreadable`. The cause is `_dispatch_files.visit` `os.scandir` (`:99–103`), which raises `ScanError`. The message is printed at `main` `:672–673`. Fail-closed, so no silent miscount, but the message names the wrong object.

### 4.7 Behaviour that holds (HOLDS)

- S0: a byte copy of the lane's `.ufo/waves` gives a payload equal to scan.json except `lane_root`.
- S2: 32 non-empty reports give `settled`, rc 0.
- S3: 31 reports plus one `STATUS: started` marker gives `partial`, stub 1, rc 1 (`_member_status` `:229–231`).
- S4: 16 present, 16 missing gives `partial`, rc 1, and a missing list of 16.
- S5: 2 reports only under the fleet root gives misrooted 2, counted as not present, rc 1 (`:233–236`).
- S8: the name hint does not affect counts or state.
- Trailers: 32/32 members have exactly one matching line, the path equals the template, and it is the strict last line. The R1 "last matching line" rule is not exercised on this lane.
- Determinism: scan.json and the rerun are byte-identical across the tool change.

## 5. Scratch battery (copies only; the lane is untouched)

Scratch outputs: `falsify/LiveRevenger/mut/*.out.json`, `mut2/*.out.json`. Fleet root: an empty scratch directory.

| Run | Scenario | rc | waves | members | present | missing | stub | misrooted | states | ignored JSON | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S0 | byte copy of live `.ufo/waves` | 1 | 1 | 32 | 0 | 32 | 0 | 0 | unsettled | 8 | payload equal to scan.json minus `lane_root` |
| S1 | rendered JSON removed | **0** | **0** | 0 | 0 | 0 | 0 | 0 | `{}` | 8 | false clean (§4.1) |
| S2 | all 32 reports non-empty | 0 | 1 | 32 | 32 | 0 | 0 | 0 | settled | 8 | |
| S3 | 31 reports, 1 `STATUS: started` | 1 | 1 | 32 | 31 | 0 | 1 | 0 | partial | 8 | |
| S4 | 16 reports | 1 | 1 | 32 | 16 | 16 | 0 | 0 | partial | 8 | |
| S5 | 2 reports under fleet root only | 1 | 1 | 32 | 0 | 30 | 0 | 2 | unsettled | 8 | misrooted counted as not present |
| S6 | identical second dispatch copy | 1 | 2 | **64** | 0 | **64** | 0 | 0 | unsettled ×2 | 8 | double count (§4.5) |
| S7 | `reviews/` mode 000 | **2** | – | – | – | – | – | – | – | – | stderr "lane root is unreadable" (§4.6) |
| S8 | dispatch renamed to `rendered.json` | 1 | 1 | 32 | 0 | 32 | 0 | 0 | unsettled | 8 | only `dispatch_path`, `name_hint` change |
| S9 | `fleet-round-1-interactive/` mode 0644 | **0** | **0** | 0 | – | – | – | – | `{}` | **0** (was 8) | silent drop (§4.1) |
| S10 | `.ufo/waves` is a symlink | **0** | **0** | 0 | – | – | – | – | `{}` | 0 | false clean (§4.1) |
| S11 | no `.ufo/waves` | **0** | **0** | 0 | – | – | – | – | `{}` | 0 | false clean (§4.1) |

## 6. Residual risk and verification gaps

- [INFERENCE] The 10 declared `kaika-r1` outputs are the members' real reports. Only headers and sizes were checked. Contents were not reviewed, and receipts have no trailers.
- Snapshot times: GT and the committed scan carry no internal timestamp. I used file mtimes (GT at or before 10:34:39Z, committed scan at or before 10:46:53Z).
- The tool version behind the committed fleet scan is unknown (no sha recorded). Its numbers for other lanes were not re-verified.
- mtime evidence assumes no timestamp-preserving copies. The `kaika-r1` cluster shows a bulk write, so these mtimes show when files were materialised, not who wrote them.
- Mutation results come from copies. They test the tool on revenger-shaped data, not the live lane.
- Not run: `--selftest`, `tools/mori-census.sh`, lane selftests, and a wider search for misrouted copies outside the two roots.

## 7. Decisions for the integration owner (recommendations only; nothing implemented here)

1. Exit codes (§4.1): exit non-zero when `.ufo/waves` is missing, symlinked, or yields zero dispatch JSON while receipts or other waves exist. Count an unstat-able `*.json` as `unreadable_json` and fail on it, not skip it.
2. Coverage (§4.2): decide whether C2 must read markdown receipts such as `kaika-r1/dispatch.md`, whose declared-writes table is parseable, or whether the lane must emit dispatch JSON. Until one of these is decided, the lane-level claim stays BROKEN.
3. State (§4.4): add a never-dispatched state, or exclude waves with `dispatch_started: false`. Mark or retire `rendered-undispatched.json` only after the L1 decides.
4. Totals (§4.5): dedupe members by `dispatch_sha256` or report duplicates separately.
5. Message (§4.6): separate "unreadable `.ufo/waves` entry" from "lane root unreadable".
6. Re-run `evidence/c2-live-fleet.json` on the current tool before quoting numbers beyond revenger (§3).

## 8. Bounds and compliance

- Read-only on the lane and fleet. Mutations ran on copies under `falsify/LiveRevenger/`. Writes: this report, `falsify/LiveRevenger/scan.json`, `falsify/LiveRevenger/mut*/`, `/tmp/LiveRevenger-rerun.json`.
- No lane production file, committed baseline, MANIFEST, or git/jj state was modified. No git or jj command was run. `.jj/`, `.ufo/interactive-sessions/`, `.ufo/worktrees/` and ~/.omp transcripts were not read or listed.
- Frozen oracle: `ids` only. No subagents. No installs or updates. No `pacman` activity.
