# KakeSuccessors: C2 "missing" semantics, kake round-22/w2 → round-23/w1

PARTIAL. `corpus/knowledge/wave-settlement-r20.md` §4 names the right limit but states the kake instance wrongly. The tool does not link successor reports, and the 21 kake round-22/w2 seats still read `missing` (scan re-run: unchanged). The sentence "kake r22/w2 seats re-run as r23/w1" overstates it. Only 18 of the 21 seats have a round-23/w1 carry-over, the carry-overs are re-scoped tasks rather than re-runs, 5 predecessors are "never ran" per task text, and the mapping is hand-derived from task text but filed under "Limits (measured)". All 18 mappings verify from the task texts. Three seats have no successor in any of the five kake dispatch files. The frozen "missing" rule itself holds: it is a declared-path check, and it reads these 21 correctly.

Scope: read-only. No lane production file, no git/jj, no subagents, `mori-census.sh` not run.

## 1. Verdict on wave-settlement-r20.md §4 (lines 59–60)

Quoted: "Successor reports are not linked: kake r22/w2 seats re-run as r23/w1 still read `missing` (`build/GtLaneKake.md`); tabi r12/r13 wrote 63 same-stem `.txt` files beside missing `.md` paths."

| Part of the sentence | Verdict | Evidence |
|---|---|---|
| Successor reports are not linked | HOLDS | The tool has no successor or carry logic (grep for successor/carr/re-run/Carried: no matches). Membership is decided only by the declared `Report:` path: trailer match `tools/mori-wave-settlement.py:208-209`, status `_member_status` `:221-234` (lane root, then fleet root for `misrooted`). |
| "still read `missing`" | HOLDS | Scan §4.4: round-22/w2 `missing` = the same 21 names; state `partial` 43/64. |
| "kake r22/w2 seats re-run as r23/w1" | OVERSTATED | 18 of the 21 missing seats have a round-23/w1 successor. `ReopenGoogleTroubleshoot`, `ReopenPythonURL`, `ReopenRFC6596` have none. |
| "re-run" | IMPRECISE | Successors are re-scoped tasks, not identical re-runs. Milestone changes `falsify-canonical-capability` → `r23-build` in 18/18; Judged-on changes in 9/18; body text differs in 18/18. Five predecessors read "(never ran)". Run state is not verified. |
| Under "## 4. Limits (measured)" | OVERSTATED | Only the `missing` result is measured. The successor link is task-text evidence (`build/GtLaneKake.md` §5 says "run state is not verified"). |
| tabi r12/r13 clause | NOT CHECKED | Outside this item. |

Suggested replacement for lines 59–60 (the owner L1 makes the edit):

> - Successor reports are not linked. The settlement reads only each member's declared `Report:` path, so kake round-22/w2 stays `partial` (43/64) with 21 `missing` seats. Round-23/w1 task text carries 18 of those seats forward ("Carried from round-22 dead wave-2 seat …"): 17 under the same name, and `Attack23` as `Attack23WrongHost`. Their reports exist at the round-23/w1 paths. The successors are re-scoped tasks (milestone `r23-build`), not identical re-runs; five predecessors are described as "never ran". `ReopenGoogleTroubleshoot`, `ReopenPythonURL` and `ReopenRFC6596` have no successor. The mapping is hand-derived from task text (`build/GtLaneKake.md` §5), not produced by the tool. [tabi clause unchanged; not verified here.]

What "missing" means here: the frozen contract (`.ufo/waves/round-20/contract.md:74-81`) defines `missing` as "no file at the declared path under the lane root, and no misrooted copy", and says a missing report is NOT a dead seat. Under that rule the 21 are correctly `missing`. The error is only in reading r23/w1 as covering r22/w2.

## 2. The 18 successor mappings (verified from task texts)

Basis. "explicit": the round-23/w1 text names the predecessor. "name+URL": the carry text names no seat, but the successor has the same name and the same URL as the predecessor (exact string match).

| # | Successor (round-23/w1, agent) | Basis | Predecessor (round-22/w2, missing) | Successor report, bytes | Judged-on r22→r23 |
|---|---|---|---|---|---|
| 1 | ReopenGoogleCanonical (scout) | name+URL | ReopenGoogleCanonical | 6212 | operability→freshness |
| 2 | ReopenHTMLLink (scout) | name+URL | ReopenHTMLLink | 5699 | operability→freshness |
| 3 | ReopenHTMLBase (scout) | name+URL | ReopenHTMLBase | 4791 | operability→freshness |
| 4 | ReopenHTMLTemplate (scout) | name+URL | ReopenHTMLTemplate | 6259 | operability→freshness |
| 5 | ReopenPythonParser (scout) | name+URL | ReopenPythonParser | 5071 | operability→freshness |
| 6 | Attack23WrongHost (reviewer) | explicit | Attack23 (renamed successor) | 3504 | operability (same) |
| 7 | BoundaryManifestKeys (reviewer) | explicit | BoundaryManifestKeys | 6290 | operability (same) |
| 8 | BoundaryTraversal (reviewer) | explicit | BoundaryTraversal | 5393 | operability (same) |
| 9 | BoundaryURLAuthority (reviewer) | explicit | BoundaryURLAuthority | 5474 | operability (same) |
| 10 | BoundaryHeadRecovery (reviewer) | explicit | BoundaryHeadRecovery | 5384 | operability (same) |
| 11 | BoundaryInertContexts (reviewer) | explicit | BoundaryInertContexts | 3412 | operability (same) |
| 12 | BoundaryAttributes (reviewer) | explicit | BoundaryAttributes | 4900 | operability (same) |
| 13 | BoundaryReadOnly (reviewer) | explicit | BoundaryReadOnly | 5743 | operability (same) |
| 14 | BoundaryReplayIntegrity (reviewer) | explicit | BoundaryReplayIntegrity | 6240 | operability (same) |
| 15 | ConnectBrowser (connector) | explicit | ConnectBrowser | 7078 | operability→operability, freshness |
| 16 | ConnectSource (connector) | explicit | ConnectSource | 6405 | operability→operability, freshness |
| 17 | ConnectCapability (connector) | explicit | ConnectCapability | 7225 | operability→operability, freshness |
| 18 | ConnectProof (connector) | explicit | ConnectProof | 14827 | operability→operability, freshness |

Checks, all 18: the predecessor is in the tool's round-22/w2 `missing` list. The successor trailer is `.ufo/waves/round-23/w1/<Name>.md`. The file is a regular, non-symlink, non-stub file with size > 0. Agent type matches (5 scout, 9 reviewer, 4 connector). `duplicate_report_paths` = 0 for round-23/w1.

Content check (token overlap over the task bodies, a weak signal): the same-name predecessor ranks first of the 64 round-22/w2 tasks for 16 of 18. `ReopenPythonParser` ranks second, tied at 0.35 with `ReopenPythonURL`; the URL resolves it (html.parser vs urllib.parse). `ConnectCapability` ranks fourth; its link rests on the explicit name and the shared topic ("canonical capability"). `Attack23` → `Attack23WrongHost` is the same frozen case, `wrong_host`, now pinned to a commit. A name-only linker would miss it.

## 3. Missing seats with no successor

- `ReopenGoogleTroubleshoot` (…/canonicalization-troubleshooting), `ReopenPythonURL` (docs.python.org …/urllib.parse.html), `ReopenRFC6596` (rfc-editor rfc6596.html): no carry text in any of the five kake dispatch files, no task of the same name, and no task with the same URL. Each URL appears only in a present round-22/w1 seat (`GoogleTroubleshoot`, `PythonURL`, `RFC6596`). Three unlinked.
- Round-22/w1 missing (`Knowledge`, `LessonDraft`, `RegistryDraft`, `TrendDraft`): no carry text. Best token-overlap matches are 0.14–0.20 and none is a plausible successor. `ScribeLessonDraft` (round-23/w1) is not among the top three for `LessonDraft`.
- Round-23/w2 missing (39): no carry text. I did not check their URLs.
- [INFERENCE] No unlabelled successor exists for the 21 round-22/w2 seats. Apart from the 18 successors, no task in the five files ranks in the top three for any of the 21. Token overlap is weak (0.23–0.41 for the real pairs), so this rules out little.

## 4. Commands and outputs

1. `/usr/bin/jq -r '.taskCall.tasks[] | select(.task | contains("Carried from round-22")) | [.name, .agent, (.task | match("Carried from round-22[^\\n]{0,200}").string), (.task | split("\n") | last)] | @tsv' kake-shokunin/.ufo/waves/round-23/w1-dispatch.json` → exit 0, 18 rows (names and trailers as in §2).
2. `/usr/bin/jq -r '.taskCall.tasks[] | [.name, .agent, (.task | split("\n") | last)] | @tsv' kake-shokunin/.ufo/waves/round-22/w2-dispatch.json` → exit 0, 64 rows.
3. Python 3 stdlib, read-only (`json`, `os.lstat`, `re`) over the five kake dispatch files:
   - "Carried from round-22" count: r21 wave1-validation 0; r22/w1 0; r22/w2 0; r23/w1 18 (of which "never ran" 5); r23/w2 0.
   - Status: r22/w2 present 43, missing 21. r23/w1 present 69, missing 0. All 18 predecessors missing. All 18 successors regular, size > 0, not `STATUS: started`.
4. Settlement tool, read-only (writes only `--out`): `python3 mori-shokunin/tools/mori-wave-settlement.py scan --lane-root /home/vgpnk/Projects/shokunin/kake-shokunin --fleet-root /home/vgpnk/Projects/shokunin --out .ufo/waves/round-20/falsify/KakeSuccessors/kake-scan.json >/dev/null` → exit 1. Run 2026-10-21, before 11:06:00Z.
   - Totals: waves 5, members 325, present 261, missing 64, misrooted 0, stub 0, empty 0, unparsed 0, unsafe 0; ignored_json 172, unreadable_json 0.
   - States: settled 2 (round-21 wave1-validation; round-23/w1). Partial 3 (round-22/w1 60/64; round-22/w2 43/64; round-23/w2 25/64).
   - round-22/w2 `missing` list = the 21 names. Matches GtLaneKake §2, §3, §8 and wave-settlement-r20 §5 ("kake 261/325").
5. `_glob` of `kake-shokunin/.ufo/waves/round-22/w2/**` (named directory): 43 reports, `swarm-registry.json`, and `raw/` (`MutateMismatch.json`, `MutateTemplate.json`). No `.txt` or other variant of any of the 21 names.
6. `stat` on three successors: regular files, 6212 / 3504 / 14827 bytes.
7. `c2-oracle.py` grep (`successor|Carried|carried|carry|round-22|kake`): no matches. The harness has no carry or successor semantics either.

## 5. Limits and record

- Not checked: report content (not judged, per C2); run state of any seat (no transcripts or session logs opened, per bounds); the tabi clause; any fleet-wide search.
- Not run: `mori-census.sh`; the tool's `--selftest`.
- Installs or updates: none. No pacman. Used `/usr/bin/jq`, python3 stdlib, coreutils `stat`/`date`/`mkdir`.
- Writes: this report, and the scratch file `.ufo/waves/round-20/falsify/KakeSuccessors/kake-scan.json`.
- Decision left to L1: whether C2 should record carry-overs. Neither the frozen contract nor the tool has successor state. Under the frozen rule the 21 stay `missing`. I would keep the tool as is and record the 18 mappings as labelled, hand-derived evidence in the note.
