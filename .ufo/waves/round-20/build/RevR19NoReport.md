# RevR19NoReport: why mori round-19 wave 1 retained 16 of 64 reports

Seat: RevR19NoReport (leaf reviewer). Method: file evidence only (wave JSON, `build/`, lessons, fleet MANIFEST, fleet scripts and reports, watchdog log, `.ufo/state` names). No session transcripts, no `~/.omp`, no git or jj commands, no subagents, no builds or tests. Installs or updates: none (Python stdlib and coreutils only). Times are UTC unless marked local (UTC-03:00). Paths are lane-relative (`mori-shokunin/`) unless shown in full. `[INFERENCE]` marks anything not directly observed.

## Verdicts

| # | Hypothesis | Verdict | Confidence | Basis |
|---|---|---|---|---|
| H1 | Misrooted under `/home/vgpnk/Projects/shokunin` | **Refuted** | High for successful misroots. Failed misroot writes leave no file, so they cannot be tested. | No `.ufo/waves/round-19/` at fleet root; 0 of 64 trailer paths exist there; no mori report written under fleet root in the wave window. |
| H2 | Wrong report dir | **Refuted** | High | 64 of 64 trailers are canonical; `build/` holds exactly the 16 delivered reports; no file for any of the 48 missing names exists elsewhere in the lane, its worktrees, the fleet, or other lanes. |
| H3 | Prompt never asked for a file | **Refuted** | High | 64 of 64 task bodies end in the same `Report:` trailer; dispatched bytes equal the attempt record; the same request in wave 2 yielded 48 of 70 reports. |
| H4 | Seat failed before writing | **Supported** (mechanism). Terminal class is recorded for 9 of the 48 (8 provider failures, 1 cancellation). For the other 39 only route-level attribution is available. | High that these seats ended without writing. Moderate for provider-throttling attribution `[INFERENCE]`. | 48 started seats left no file and were neither resumed nor replaced. The lesson records many with no final body. Delivery splits sharply by fleet route. |

## 1. Ground truth

- Dispatch: one batched task call, 64 tasks. Payload 118,996 bytes, sha256 `884b848c…e2263`. `wave1-attempts.json` `attempts[0]`: `state` started, `tasks_count` 64, `started_ids` 64.
- Settlement (`wave1-settlement.json`): `reports_present` 16 (lines 6–23); `known_provider_failed` 8 (24–33); `known_cancelled` 1 (34–36); `no_report_terminal_cause_unestablished` 39 (37–77). Sum 64. `replacements` 0 (line 83).
- Run (`wave1-run.json`): `counts` spawn 64, resume 0; `resumeSends` `[]`. Policy ramp is 5 spawns per 700 ms (`policy`), which implies all 64 launched within about 9 s `[INFERENCE from policy, not observed]`.
- Timeline (UTC): registry created 08:05:28 (`build/swarm-registry.json:4`). Payload written and dispatched 08:18:37. First delivered report 08:19:14 (DraftLesson). Last delivered report 08:26:14 (Content24). No report file written after 08:26:14. Last write I can see in any seat's private worktree: 08:45:44 (RegressionHarnessSparse owned file; authorship by that executor `[INFERENCE]`, no report). Wave 2 dispatched 08:49:29. Wave 1 settlement file written 09:05:29.
- Slot grant: wave 1 `live=176 pending=0 cap=240` (`wave1-attempts.json` `slot`). Wave 2 `live=47 pending=0 cap=240` (`wave2-attempts.json` `slot_grant`).

Delivered / total by role, with the documented fleet route from `scripts/hyaku/lane-addendum.md:73–79`:

| Role (documented route) | Wave 1 | Wave 2 |
|---|---|---|
| reviewer (m_zfl, zai) | 5/44 | 26/39 |
| scout (m_flash) | 5/8 | 19/26 |
| connector (m_flash) | 0/3 | 0/1 |
| executor (m_luna, Codex-hosted) | 2/3 | none |
| sentinel (m_luna) | none | 1/1 |
| critic (m_swe) | 3/3 | 2/3 |
| scribe (m_haiku) | 1/3 | none |
| **total** | **16/64** | **48/70** |

- Wave 1 missing 48: reviewers 39 (4 provider, 1 cancelled, 34 unknown); scouts 3 (1 provider, 2 unknown); connectors 3 (1 provider, 2 unknown); scribes 2 (provider); executor 1 (unknown).
- Wave 2 missing 22: all 22 classed as provider failures (13 reviewers, 7 scouts, 1 connector, 1 critic). The wave 2 settlement has no unknown class.
- Impact: the 36 Content reviewer bodies name 194 distinct blob paths (the frozen population). The 5 delivered Content reports cover exactly 26 of them; `content-reviews-before.json` has 26 rows matching their path lists. About 168 population paths lost delivered content review.

## 2. H1, misrooted under `/home/vgpnk/Projects/shokunin`: REFUTED

- `FLEET/.ufo/waves/round-19/` does not exist (checked with `os.path.isdir`). A misrooted round-19 report would have had to create it.
- For all 64 wave 1 trailers, the same relative path under the fleet root is absent (0/64). Wave 2: 0/70.
- Fleet-root writes in the window 08:18:30–08:49:00 (walk of `.ufo` and `scripts`, worktrees pruned): five files, none a round-19 report. `.ufo/reports/round-20/kaidoku.md` (08:23:58), `.ufo/waves/hyaku/PHASE2.md` (08:40:12), and `scripts/hyaku/wave-slot.sh`, `wave-live.py`, `wave-slot-selftest.sh` (08:23:01). The last three are fleet tooling edits, not seat output.
- Fleet-wide basename search for all 64 names (361,096 files walked; `.git`, `node_modules` and worktrees pruned): no hit under the fleet root outside the mori lane in the window. Same-name files in other lanes are those lanes' own content, all dated outside the window. Examples: kama `.ufo/waves/round-19/build/advice/DraftLesson.md` (2026-10-21 06:32Z, before dispatch) and tabi `.ufo/waves/round-20/w1/CriticScope.md` (2026-10-21 10:03Z, after the settlement).
- The fleet root carries no untracked misroot by the L1's own sweep: `evidence/misroot-sweep.json:3–9` (`git status --porcelain` empty; `own_candidates` 0). `.gitignore` lines 1–6 do not ignore `.ufo/waves/round-19/`, so untracked misroots would have shown. I did not run git; this is the L1's observation.
- The misroot guard was present. Both contexts say `Every Report: trailer path is relative to /home/vgpnk/Projects/shokunin/mori-shokunin — write it at …/mori-shokunin/<that path>` (`wave1-taskcall.json` `.context`; the same sentence is in `wave2-run.json` `taskCall.context`). The static context check passed with clauses `lane_report_resolution` and `no_fleet_root_writes` (`wave1-context.json` stdout: `CONTEXT_OK`, 12 clauses).
- Read side: all 36 Content bodies use repo-relative blob paths. All 194 resolve under the lane; none resolve under the fleet root. A fleet-root working directory would therefore have failed for every reviewer, yet 5 reviewers delivered. They must have used lane paths. So a root misread cannot explain delivered versus missing.
- Caveat: a relative write from the fleet root into a missing directory may fail and leave nothing. Files cannot rule out failed attempts. `lane-addendum.md:157–162` records earlier misroots in kama r11, tsukuroi r12, tabi r15 and mado r16, so the hazard is real fleet-wide. It left no trace here.

## 3. H2, wrong report dir: REFUTED

- Trailers: 64 of 64 are `.ufo/waves/round-19/build/<Name>.md`, one per body, as the last line. The spec `reportDir` (`wave1-spec.json`) and the registry `reportDir` (`build/swarm-registry.json:6`) match.
- `build/` contains 17 entries: the 16 delivered reports (1,307 to 6,733 bytes, none empty) and `swarm-registry.json`. The 16 names equal `reports_present`.
- Lane-wide basename search for the 48 missing names, worktrees pruned: zero hits outside `build/`. Round-19 path hits are exactly the 16.
- `.ufo/worktrees/round-19/` holds nine entries:
  - Three sparse git worktrees (ContentGateSparse, FreezeMetadataSparse, RegressionHarnessSparse) contain only `.git` and the owned tool file.
  - Six non-git full copies (ContentGate, ContentGateActual, FreezeMetadata, FreezeMetadataActual, RegressionHarness, RegressionHarnessActual) each hold 5,274 files outside nested worktrees. None has a `round-19/build/` directory. Their only report-name hit is the old `round-13/build/RegressionHarness.md`.
- Wave 2 used `.ufo/waves/round-19/falsify/` (70 of 70 trailers), and its 48 reports are there. The per-wave directory rule held in both waves.

## 4. H3, prompt never asked for a file: REFUTED

- 64 of 64 wave 1 task bodies end with exactly one trailer, `Report: write your scoped findings to .ufo/waves/round-19/build/<Name>.md` (`wave1-run.json` `taskCall.tasks[].task`, last line).
- The dispatched payload is `wave1-taskcall.json` (sha256 `884b848c…e2263`, 118,996 bytes). This equals the attempt record's `payload_sha256` and `payload_bytes`. `wave1-run.json` `taskCall` is object-equal to that file.
- The context (3,787 characters, equal to `wave1-spec.json` `.context`) says `Report only your assigned new file`. The same wording appears in wave 2.
- Within wave 1 the request is identical across roles, yet delivery ranges from 0% to 100% by role. The prompt cannot separate delivered from missing seats.
- Observation, not causal: spec `items[].prompt` never contains the trailer. All 64 dispatched bodies equal prompt plus trailer suffix. The request exists only in the assembled payload.

## 5. H4, seat failed before writing: SUPPORTED (mechanism)

Established from files:

1. All 64 seats started (`started_ids` 64). Registry members carry agent IDs for all 64 (`build/swarm-registry.json`, `wave1-record.json`). The registry has no status field, so no terminal state was ever recorded there.
2. No file exists for the 48. The lesson says that at recovery there were no running mori worker jobs and that "many started seats had no final body" (`corpus/lessons/round-19.md:109–111`). Missing reports are missing evidence (`:111`).
3. No resume (`resumeSends` `[]`) and no replacement (`replacements` 0). The context says "never wake old failed identity or replace dead seats" (`wave1-taskcall.json` `.context`). A seat lost to a provider window therefore could not be recovered inside round policy.
4. Provider classes recorded by the L1 (`wave1-settlement.json:78–82`):
   - `rate_limit_error with reported retry-after-ms=5495000; no retry made` (about 91.6 minutes, no retry);
   - `turn_rate_limit_exceeded after5 retries`;
   - `HTTP429 vendor type1302 after5 retries`.
   The second and third are also in the wave 2 settlement. The mori closure report gives the same classes (`.ufo/reports/round-19/mori.md:64–66`). I could not verify them independently from transcripts. Neighbouring round-19 lane tsukuroi also recorded "6 dead by 429" of 72 seats (`.ufo/l0-questions.md:75`), so this failure class is not unique to mori.
5. The retry budget is 5. The context reads `Globalretry5; respect provider backoff` (both waves; the missing space is in the source). The settlement's "after5 retries" matches. The fleet config is `retry.maxRetries` 40 (`lane-addendum.md:115`). The wave therefore capped seats at 5 retries `[INFERENCE on reading]`.
6. Not all losses were at spawn. The RegressionHarnessSparse owned file has mtime 08:45:44, 27 minutes after dispatch and 19 minutes after the last delivered report. Attributing that write to the executor is `[INFERENCE]`; the L1 integrated later. That executor never delivered. Its file parses (`ast.parse` ok). If the write is its own, it was active then ended without its report.
7. Load at grant: 176 live seats in wave 1 versus 47 in wave 2. Other lanes launched in the pre-dispatch window (`.ufo/watchdog.log`: kaidoku r21 05:05:02, tsukuroi r20 05:13:11, souji r20 05:13:50, local). The watchdog has no mori line after 04:51:00 local, so it recorded neither wave.
8. The author's own wake failed earlier, at 04:40:20 local, on an Anthropic 429 with `retry-after-ms7844000` (about 2 h 11 min). That is another long retry window, far longer than a 5-retry budget (`.ufo/watchdog.log`, entry `lane-dead-no-report mori round=19`).

Route attribution `[INFERENCE]`:

- The documented route table is `lane-addendum.md:73–79`: reviewer to m_zfl (zai); executor and sentinel to m_luna (Codex-hosted); critic to m_swe; scribe to m_haiku; scout and connector to m_flash.
- The documented zai error is `429 Rate limit reached for requests (type=1302)` (`lane-addendum.md:101–103`), with a documented failover from zai 429 to gpt-6-luna (`:111–112`). The settlement's `HTTP429 vendor type1302` matches the zai code. Its `turn_rate_limit_exceeded` matches the Codex capacity wording in `.ufo/l0-questions.md:56`.
- Delivery fits route concentration. Reviewers (zai) delivered 5/44 in wave 1 and 26/39 in wave 2. Critics, executors and scouts delivered most seats in wave 1 (3/3, 2/3, 5/8).
- Task size does not explain it. The 8 Gate, Meta and Harness reviewers have short bodies (about 1.4 KB) and delivered 0/8. The 36 Content reviewers (about 2.1 KB) delivered 5/36. The five delivered Content reviewers are not systematically lighter than the missing ones (blob bytes overlap).
- Connectors are the anomaly. They delivered 0/4 across both waves, on the same documented route family as scouts, who delivered 24/34 across both waves. The captured chain per seat is not in any file, so this stays open.
- Limit: no file records a seat's answering model, cascade hop or terminal error. `lane-addendum.md:99–100` asks seats to record the answering model when a claim depends on it. The attribution of the 34 unknown reviewers to the zai route is therefore `[INFERENCE]`, though strongly suggested by the route pattern and the error text.

Unplaced candidate: the erroneous parent stand-down after wave 1 started (`corpus/lessons/round-19.md:106–109`; `.ufo/reports/round-19/mori.md:72–73`; `LOG.md:1357`). No file gives its time, its recipients, or its effect on seats. `.ufo/l0-questions.md` has no stand-down row, and `.ufo/state/mori.out` is 22 bytes. It can be neither ruled in nor out.

## 6. Divergences and other findings

1. Retry budget. A 5-retry wave budget sits below the fleet's `retry.maxRetries` of 40. Documented historical zai retries came roughly 72 s apart (`lane-addendum.md:102–103`), so 5 retries covers about 6 minutes. This is `[INFERENCE]` on spacing. Wave 2 had the same budget and still delivered 48 of 70.
2. No recovery path. "Never wake old failed identity or replace dead seats" combined with resume 0 made a 429 loss permanent for the round. The settlement correctly calls the 48 missing evidence, not deaths, but the design converted throttling into permanent loss.
3. Missing per-seat metadata. The registry records kind, agent ID, role and item only. Route, answering model and terminal class are not recorded at spawn or settlement. The 39 unknowns cannot be resolved from the wave's own files.
4. Self-nesting worktree copies. The six full copies under `.ufo/worktrees/round-19/` recurse: `ContentGate/.ufo/worktrees/round-19/ContentGate/…` continued at least 40 levels. An `os.walk` of `.ufo/worktrees` reached 2,000,000 files in 2.2 s before I capped it, against about 6,400 lane files outside worktrees. The copied files carry mtimes 04:25Z to 06:28Z, before dispatch. This is a hazard for any unbounded recursive search of the lane. Wave 2 ran in the same tree and delivered 48 of 70, so it is not sufficient to explain wave 1. No file shows a wave 1 seat walking it. `[INFERENCE]` on hazard. The disposition says the creation attempts timed out at 60 s or 300 s (`worktree-disposition.json:18`).
5. Reviewer dependency. The 8 Gate, Meta and Harness reviewers were told to read in-progress writer files under the sparse worktrees and "do not wait" (for example the GateCoverage body). None delivered. Whether this mattered is not established.
6. Contract premise. `.ufo/waves/round-20/contract.md:51–54` says the 48 were "found only by hand at recovery and closure (MANIFEST round-19 closure notes)". The MANIFEST closure row (`rounds[398]`) gives the counts (W1 64/16/8/1/39; W2 70/48/22; 0 replacements) and says its reviewers executed jq counting commands. I searched every string field of that row for "hand", "found", "missing" and "recover", and found no "by hand" wording. That premise needs a source or a correction.
7. Lesson scope breaches (not causal). CriticTrends (a delivered wave 1 seat) and CriticNoHarm (wave 2) disclosed broad searches into retained session material (`corpus/lessons/round-19.md:187–190`). This does not explain the loss.

## 7. Limits

- Per-seat terminal causes for the 39 wave 1 unknowns are unobservable from files. Transcripts are off-limits by design.
- Route attribution rests on the documented route table and matching error strings. No file I read records the wave 1 answering model.
- A failed write into a non-existent fleet directory would leave no file. The fleet-root result refutes successful misroots only.
- Mtimes were read as write times. Copies may carry older mtimes. Times are UTC.

## 8. Implications (for the planner; nothing run)

- A C2 scan of wave 1, if run, should report `partial`, 16 present, 48 missing, 0 misrooted, 0 unsafe, 0 unparsed. The files predict this; I did not run the tool. It cannot assign a cause.
- Recording each seat's route, answering model and terminal class at spawn and settlement would turn the 39 unknowns into evidence.
- Decide whether a 5-retry budget and the no-replacement rule are intended for 429 windows. The data suggest they converted provider throttling into permanent loss.

## Tooling and bounds

- Installs or updates: none. Reads used Python stdlib and coreutils (`sha256sum`, `stat`, `os.walk`, JSON loads).
- No git or jj commands. No writes except this report (the STATUS line was overwritten). No messages to any peer. No subagents. No transcripts. No `~/.omp`. No `mori-census.sh`. No builds or tests.
