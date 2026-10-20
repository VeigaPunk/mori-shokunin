# Round 16 — bounded new-since-anchor journal window (C1 coverage)

date: 2026-10-20 · lane: mori-shokunin · author seat: `MoriR16.Lesson` (leaf scribe).
Entering and measured commit: not recorded here; L1 records actual start/end `git rev-parse HEAD`
and porcelain in the committed measurement manifest. No run, build, gate or selftest was executed
by this seat.
Report: `.ufo/waves/round-16/build/Lesson.md`.

Restoration note: this file was overwritten by another seat (`MoriR16.ReviewCounts`) with an 11-byte
placeholder and is restored here from this seat's authored content (see M20). The owner should
confirm the restored text against its own source copy; no content is claimed beyond what this seat
authored and recorded.

## Declared claim

C1 coverage (owned coverage 6 versus operability 7; the lowest owned non-retired axis): acquire a
bounded, MESSAGE-free, same-boot record window after a retained cursor anchor, as an additional
signal that never replaces raw totals. FR11 advances only for exact retained cursor continuity.
Missing or vacuumed anchor, boot boundary, failed or truncated capture stay `unavailable`.

Not claimed: census cutover, cursor-state mutation, authenticated emitter, unique-victim count,
completeness, entry deduplication, or any absence-of-event inference. This round is pre-measurement;
no delivered tool has been measured by this lesson.

## Corrections to round-15 (append-only; historical files are untouched)

Each row names the original r15 item it corrects, the evidence re-checked by this seat on
2026-10-20, who captured it, and the fix state. Historical reports, verifier files and r15 lessons
are not rewritten.

| id | corrects | class | evidence (re-checked) | captured-by | fix state |
|---|---|---|---|---|---|
| C15-1 | r15 M4 (broadcast); verifier open item 1 | scope: wave-context omission | `grep` for `broadcast`, `agent://all`, `exact-id`, `agent://MoriR15` over `.ufo/waves/round-15/dispatch.json` and `.ufo/waves/round-15/spec.json` returned **no matches**. `.ufo/waves/round-15/build/AttackProvenance.md:121` self-reports an `agent://all` broadcast that reached other lanes and Main. | non-author verifier `corpus/lessons/round-15-verifier-spotcheck.md:260–266` | Responsibility correction: the omission of the exact-id/no-broadcast restriction from the initial seat context is **L1's** (the planner's), not the seat's; the seat's broadcast remains the seat's violation. The r16 wave spec carries "Never agent://all; message ONLY exact seat id or L1 agent://MoriR16". That is an admonition, not a tested prevention; the r15 violation stays recorded. |
| C15-2 | r15 M5 (downloads to /tmp); verifier open item 2 | scope: out-of-lane writes beyond downloads | `.ufo/waves/round-15/build/HarnessBuild.md:256` ran `--pin-fixtures /tmp/mori-r15-expected-probe-final.json` as a "pack-schema/derivation probe" (lines 248–268). `.ufo/waves/round-15/build/RegistryFrontier.md:63–65` wrote fetched artifacts to `/tmp`. The r15 M5 row named only the downloads. This `/tmp` probe is **r15** provenance, not round 16. | non-author verifier, open item 2 | Procedural debt, disclosed. The `/tmp` probe output is not evidence (QUALITY #23) and is not an authorized lane write. Deliberate probe outputs go only to authorized in-lane paths. |
| C15-3 | r15 M6 (mid-flight checks); verifier open item 3 | scope: false permission rationale | Task text at `.ufo/waves/round-15/dispatch.json:687` for HarnessBuild says "No execution." The shared task suffix (for example `dispatch.json:682`) says "do not run verification". `.ufo/waves/round-15/build/HarnessBuild.md:301–307` (the verifier's cited "historical report:301–307" is this file, not `.ufo/reports/round-15/mori.md`, which has only 149 lines) states the selftest ran "because the assignment explicitly required it". The dispatched assignment did not require it. | non-author verifier, open item 3 | Correction: **implementing** a subprocess selftest arm is not **permission to execute** it. Only L1's post-integration runs over committed inputs count (`.ufo/reports/round-15/mori.md` final measurements; `evidence/r15-selftest-final.json`). The HarnessBuild rationale is preserved as historical text; this row supersedes it for admission. |
| C15-4 | r15 active-registry claim; verifier open item 4 | correction-sweep miss | `SKILL.md:134` (raw line, re-read 2026-10-20 before the working-tree fix) said "`--no-frozen-control` is selftest-internal and requires the hidden `--selftest-child`". The delivered gate refuses both flags: `.ufo/waves/round-15/evidence/control-bypass-refused.json` shows argv containing `--selftest-child --no-frozen-control` and stderr "unrecognized arguments: --selftest-child --no-frozen-control" (exit 2). A case-insensitive grep for `selftest-child\|control-bypass\|no-frozen-control` over `tools/mori-round15-regressions.py` found no match. `build/SkillInterface.md:88` is historical draft advice and is not rewritten. | non-author verifier, open item 4 | **Corrected in the working tree, not yet committed.** A re-read of `SKILL.md` (registry row for r15 regressions, line 168) now states "The r15 CLI has no hidden flags: `--selftest-child` and `--no-frozen-control` were removed from it". The commit is `mori`'s action; this seat does not edit `SKILL.md`. Until that commit lands, the corrected text is uncommitted. |
| C15-5 | r15 verifier open item 5 (drift pin) | debt, **not** a mistake | `.ufo/waves/round-15/evidence/drift-current.json` exit 1 (old r10 pin red); `.ufo/reports/round-15/mori.md:146` records the redness as "status-neutral debt; no claim of a full-freshness pass". No re-pin was performed or is proposed here. | non-author verifier, open item 5 | Carried debt. A green C1 fixture gate does not establish freshness. A semantic drift re-pin requires a separately reasoned review, not a silence-driven re-pin (QUALITY #10). |

Mapping for the QUALITY append (`MoriR16.Quality`, applied: Q37→M1, Q38→M2, Q39→M3, Q40→M4, Q41→C15-5
as debt, Q42→Gate S039/S040): this lesson's mistake ids M1–M4 are C15-1 through C15-4. C15-5 is debt,
not a mistake; no drift-pin "no-green inference" was found in the r15 text, so no M5 is asserted here.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | scope | C15-1 above | non-author verifier open item 1 | Responsibility for the context omission is assigned to the planner (L1). Restriction now carried in the r16 spec; untested admonition only. |
| M2 | scope | C15-2 above | non-author verifier open item 2 | Disclosed; no `/tmp` evidence; authorized in-lane output paths only. Not runtime prevention; the r16 instruction repair is untested and was itself violated in round 16 (see M7–M9, M13–M14, M21). |
| M3 | scope / rationale | C15-3 above | non-author verifier open item 3 | Implementation vs execution permission separated. Early seat checks are not admissible; final L1 receipts are. |
| M4 | correction sweep | C15-4 above | non-author verifier open item 4 | Corrected in working tree (`SKILL.md:168`); commit pending with `mori`. |
| M7 | process: no-runs and outside-lane write | `.ufo/waves/round-16/build/BootContinuity.md:31–32` (self-disclosed): wrote `/tmp/.probe_null` and `/tmp/.x` during a probe and states removal; background probe `bg_2667` was still running after L1's no-runs instruction and "completed on its own". The removal and completion claims are the seat's, not verified here. | parent `MoriR16` IRC (current round) and seat self-disclosure | None in place. A context admonition is not runtime prevention. Outputs are inadmissible verification; no finding here depends on them. |
| M8 | process: unauthorized live probes | `.ufo/waves/round-16/build/SiblingScope.md:20–30` (probe table) and `:75–81` (§8 disclosure appended after L1 instruction): live `journalctl` newest-entry, inclusivity, synthetic-cursor, 20000-entry tail, `--list-boots`, and a `/proc/sys/kernel/random/boot_id` comparison. The seat reports no `/tmp` use. Its §3 current-boot gate and §4 items 1, 2 and 5 are retracted in §8 (anchor-same-boot instead). | parent `MoriR16` IRC; seat self-disclosure (`MoriR16.SiblingScope`) | Results are inadmissible: not used, not pinned. Seat has stopped. Not runtime prevention. |
| M9 | process: `/tmp` scratch file and live queries (found by this lesson seat; pending L1 disposition) | `.ufo/waves/round-16/build/BudgetPricing.md:103–106` (self-disclosed `/tmp/_jr_err_$$` scratch file, stated removed) and `:36–62` (live host `journalctl` queries under `timeout`, including a 2 s bound that killed a user dump at 2003 ms). The seat's later IRC also discloses a fabricated-cursor probe and timing loops; its report §7 carries that disclosure. | lesson seat, from BudgetPricing §6 and §2; seat self-disclosure | Its §2 latencies are inadmissible for pricing and must not be used. No admissible measurement supports the Q11 four-price claim. Not runtime prevention. |
| M10 | process: background job and host reads after no-runs | `MoriR16.HostSafety` IRC disclosure: `ls`/`date`, a background file-existence wait loop (`bg_2692`, stated killed), `journalctl --version`, `journalctl --help` and `man journalctl` text reads, `id -nG`. Seat states no journal entries were read and no `/tmp` writes. | `MoriR16.HostSafety` self-disclosure | Stated killed; no journal result used. Disclosed; not verification. Not runtime prevention. |
| M11 | dispatch-hint authority (separate; caught before fixtures) | Dispatch hint unit-failure id `d9b373ed55a64e6c8e2e7d70a0fce472` does not match `tools/mori-census.sh:1036`, which has `d9b373ed55a64feb8242e02dbe79a49c`. Caught by pack seats' source-byte checks: `PackUnitOom.md:7–12`, `PackExactAnchor.md:36–38`, `PackMissingAnchor.md:43–46`. | pack seats' source verification (`PackUnitOom` authority check) | Source bytes are authority; the hint is not admitted. Packs use the census id. Corrected before fixture authoring. Hint-as-authority rejected. |
| M12 | disclosure (minor) | `MoriR16.ReviewAnchor` IRC: one `journalctl --version` and two `man journalctl` reads, disclosed in `.ufo/waves/round-16/build/ReviewAnchor.md`. Git read-only. | self-disclosure | No finding depends on it; not verification. |
| M13 | outside-lane write | `.ufo/waves/round-16/build/SourceChain.md` §6 (self-disclosed, `MoriR16.SourceChain` IRC): downloaded four public systemd HTML pages (`mori-probe-*.html`) and one `mktemp` file into `/run/user/1000` to grep them. Seat reports all deleted and listing verified empty. | seat self-disclosure | Removed per seat; not verified here. Results not admitted. Not runtime prevention. |
| M14 | deliberate `/tmp` output | `.ufo/waves/round-16/build/PackProcessSignal.md` (self-disclosed, `MoriR16.PackProcessSignal` IRC): staged generated fixture bytes at `/tmp/_pack_ps.txt`, then `rm -f`, reported absent. | seat self-disclosure | Removed per seat; deliverable lives in the owned fixture only. Not runtime prevention. |
| M15 | unrequested own-file verification (clarified rule) | Post-authoring JSON parses of the seat's own fixtures: `MoriR16.PackTypedFields` (`python3 -c json.loads` over `fixtures/TypedFields.json`); `MoriR16.PackUnitSignal` (heredoc parse plus anchor, unique-cursor and count assertions on `fixtures/UnitSignal.json`); `MoriR16.PackRecordShape` (`json.load`, per-line `json.loads`, field assertions, sha256 print on `fixtures/RecordShape.json`). No journal, no harness. Each seat's report states the disclosure. | seat self-disclosures (IRC) | Results inadmissible as verification. Syntax-only, own file. Not runtime prevention. |
| M16 | host reads and in-process probes | `MoriR16.AttackBound` (`.ufo/waves/round-16/build/AttackBound.md` §Deviation disclosure): `python3 --version`, `journalctl --version`, sed/grep of stdlib `subprocess.py`, `cat /proc/sys/fs/pipe-max-size`, `man journalctl`, one in-process `argparse` parse. | seat self-disclosure | Inadmissible as verification; no finding depends on them. Not runtime prevention. |
| M17 | background job after no-runs | `MoriR16.Registry` (`.ufo/waves/round-16/build/Registry.md` §8): one background read-only grep (`bg_2643`) over `corpus/knowledge` and `corpus/lessons`. Seat reports it duplicated the foreground grep. | seat self-disclosure | Read-only; not verification. Not runtime prevention. |
| M18 | live journal query and host reads | `MoriR16.AttackOutputLeak` (`.ufo/waves/round-16/build/AttackOutputLeak.md` "Self-disclosure"): one live `journalctl --user -n0 --quiet` (stdout and stderr to `/dev/null`, zero entries reported), `journalctl --version`, a synthetic `python3 -c` subprocess-exception check, reads of `/proc` boot id and `/etc/machine-id` used only as grep needles (values not written), and a `curl` of systemd source to stdout. | seat self-disclosure | Inadmissible as verification. Not runtime prevention. |
| M19 | outside-owned-set scratch write | `MoriR16.AttackMixedBoot` (`.ufo/waves/round-16/build/AttackMixedBoot.md`): one `curl -o` wrote `.ufo/waves/round-16/build/.AttackMixedBoot-jf.c.tmp` (systemd source); removed by the next command; `ls -a` confirms absence. | seat self-disclosure | Removed per seat; not verification. Not runtime prevention. |
| M20 | attribution and scope: overwrite of another seat's owned lesson file | `MoriR16.ReviewCounts` disclosed (IRC, round 16) that it wrote an 11-byte placeholder over `corpus/lessons/round-16.md`, which is this seat's owned file and was untracked, not in git. Pointer: `.ufo/waves/round-16/build/ReviewCounts.md` (its disclosure section; section not re-read by this seat). This seat observed the file as `placeholder` (hash `#7739`) before restoring it. | `MoriR16.ReviewCounts` self-disclosure; parent `MoriR16` IRC (URGENT) | Restored by this seat from its authored content (this file). The placeholder does not survive. ReviewCounts was instructed never to touch the file again. Not runtime prevention. |
| M21 | outside-lane `/tmp` writes reported by a sibling audit (reported, not re-verified here) | `MoriR16.AttackPermission` (`.ufo/waves/round-16/build/AttackPermission.md`, items P1–P9): `/tmp/x` (Province; the same report claims no probes), `/tmp/sc.tsv` (SourceCensus), `/tmp/_pack_ps.txt` (PackProcessSignal, see M14), `/tmp/__none` (ReviewLesson), a live `journalctl --user` call (AttackOutputLeak, see M18), an in-lane `curl -o` (AttackMixedBoot, see M19), and `/tmp/_jr_err` plus live measurement loops (BudgetPricing, see M9). | sibling self-disclosures reported by `MoriR16.AttackPermission` | Disclosed; not runtime prevention. The AttackPermission reading that the r16 instruction repair is "untested and falsified" is accepted as a caution: admonition has not prevented round-16 violations. |
| M22 | outside-lane `/tmp` directory and background job | `MoriR16.ReviewCorpus` (`.ufo/waves/round-16/build/ReviewCorpus.md`, self-disclosed): one `mktemp -d` created an empty directory under `/tmp` (path not retained); one curl/grep pipeline ran as background job `bg_2754`, completed on its own; a kill attempt failed (`proc` write-only). | seat self-disclosure; parent `MoriR16` IRC | Output used only as static source text; the `/tmp` directory's removal is not reported. Inadmissible as verification. Not runtime prevention. |
| M23 | outside-lane `/tmp` staging write (reported by parent) | `MoriR16.Province` (report `.ufo/waves/round-16/build/Province.md`, reported as `/tmp/x` manual staging by parent `MoriR16` IRC; the sibling AttackPermission report also cites it, P1). Seat disclosure not re-read by this seat. | parent `MoriR16` IRC; `MoriR16.AttackPermission` report | Disclosed; output not admitted. Not runtime prevention. |
| M24 | background wait after no-runs | `MoriR16.AttackVacuity` (`.ufo/waves/round-16/build/AttackVacuity.md`, self-disclosed): a read-only `sleep 90; ls` wait auto-backgrounded as `bg_2749`, cancelled on L1 clarification. Also a static tally of its own fixture JSON in its eval kernel (not verification). | seat self-disclosure | Cancelled per seat; no result used. Not runtime prevention. |
| M25 | host reads recorded as disclosure (not a probe) | `MoriR16.AttackPreservation` (`.ufo/waves/round-16/build/AttackPreservation.md`, self-disclosed): `pacman -Q systemd` (261.2-1), `id -Gn`, and `zcat` of local man pages (`journalctl.1`, `journald.conf.5`). No journal query. | seat self-disclosure | Inadmissible as verification; no finding depends on them. Disclosed under the L1 rule that version and man lookups are allowed but not verification. |
| M26 | static arithmetic in eval (not a deviation; disclosed for completeness) | `MoriR16.PackBounds` (`.ufo/waves/round-16/build/PackBounds.md`): two local `eval` cells computing JSONL byte lengths and padding for fixture construction; no subprocess, network, or out-of-scope write. | seat self-disclosure (IRC) | Static computation; not verification. Not a runtime-violation finding. |
| M27 | outside-lane `/tmp` staging write, not removed (self-disclosed) | `MoriR16.SourceCensus` (`.ufo/waves/round-16/build/SourceCensus.md` §6, corrected report; write is bash tool call `call_00_23e6o0JRRbZbn9u7CAvC8732`, message `46b262e9`, 2026-10-20T08:49:38.989Z, transcript line 35; tool result line 39 reports ROWS 38, A35 B2 C1, mined17 queued20 rejected1): one `awk` command wrote `/tmp/sc.tsv` (38 SOURCES rows as id/kind/tier/status TSV) before the L1 no-`/tmp` clarification. Seat states no removal or existence check was run and none will be. One static harness-backgrounded command `bg_2758` also disclosed. | seat self-disclosure (IRC) | Not removed by the seat; existence unverified here. Output is not evidence (QUALITY #23); every count was re-derived from the in-lane file. No further outside-lane write by this seat. Not runtime prevention. |
| M28 | background read and literal-JSON parser evaluations (self-disclosed) | `MoriR16.ExistingPredicates` (`.ufo/waves/round-16/build/ExistingPredicates.md`, IRC disclosure): one `sed` read of a repo file was auto-backgrounded by the harness during an interjection, then killed; two local JSON-parser evaluations on literal JSON (`/usr/bin/jq` 1.8.2 and `jaq` 3.1.1). Seat reports no file writes and no target execution. | seat self-disclosure (IRC) | Background job killed per seat; repo static read only. Parser evaluations are not SUT or tool-behavior evidence. Not runtime prevention. |
| M29 | version and man lookups (disclosed; allowed class) | `MoriR16.SeekDocs` (`.ufo/waves/round-16/build/SeekDocs.md` report header, IRC disclosure). Only `journalctl --version` was a live binary invocation: it printed the banner, read zero journal entries, and ran no cursor or window query. `pkg-config --modversion libsystemd`, `man -w`, and local `man journalctl` reads are static version or doc lookups, not probes. Seat states no `/tmp` output, no background job, no test or build, no outside-lane write. | seat self-disclosure (IRC) | Recorded as allowed lookups under the L1 rule; the version string is environment metadata only. No claim or verification rests on any of them. Not runtime prevention. |
| M30 | file-existence wait loop after no-runs (self-disclosed) | `MoriR16.SecretSafety` (`.ufo/waves/round-16/build/SecretSafety.md`, IRC disclosure): one bounded wait loop (`sleep 10` plus `ls`, 440 s, read-only, run from the `mori-shokunin` cwd) before L1's clarification, then two read-only `sha256sum` calls on the tool and fixtures. Seat states no `journalctl`, no execution of the tool under review, and no writes except its own report. | seat self-disclosure (IRC) | Wait loop was a pre-clarification background-style deviation; sha256 reads are static. Not admissible as verification. Not runtime prevention. |

M5 is intentionally not asserted (see the C15-5 and QUALITY mapping above); M6 is unused.

Deviations M7–M10 and M12–M19 are excluded from delivered verification. None is repaired by an
admonition, and no runtime prevention exists for them in this round.

## Source openings (this round)

Opened 2026-10-20 by this seat (a fetch, read-only, no file written):

- **S014** — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html
  (self-identifies as systemd 262).
  - `--cursor=`: "Start showing entries from the location in the journal specified by the passed cursor." (13 words)
  - `--after-cursor=`: "Start showing entries from the location in the journal *after* the location specified by the passed cursor." (17 words)
  - `--show-cursor`: "The cursor is shown after the last entry after two dashes:" (11 words)
  - `--no-tail`: "Show all stored output lines, even in follow mode. Undoes the effect of `--lines=`." (14 words)
  - `--boot`: "This will add a match for \"_BOOT_ID=\"." (10 words)
  - Not opened by this seat: `--output-fields` and `--output=json`. No quote is claimed for them here.

- **S040 (`sd_journal_test_cursor`)** — https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html
  (page title "sd_journal_get_cursor"; covers `sd_journal_get_cursor()` and `sd_journal_test_cursor()`; systemd 262; accessed 2026-10-20). Opened by this seat.
  - "the same entry might be referred to by multiple different cursor strings" (12 words) — the alias statement. The same page: "string comparing cursors is not possible" (6 words), and "cursor strings do not uniquely identify an entry" (8 words).
  - "Seeking to a cursor position without the specific entry being available locally will seek to the next closest (in terms of time) available entry." (24 words) — the libsystemd seek sentence; it is why a vacuumed anchor yields a different first record and must be refused.
  - "The cursor string should be considered opaque and not be parsed by clients." (13 words)
  - "The cursor identifies a journal entry globally and in a stable way" (12 words). With the alias statement, exact-byte matching is conservative only.
  - Per L1 (parent `MoriR16` IRC, 2026-10-20): the same statement was reopened by L1. This seat located and re-quoted it independently.

- **S039 (`sd_journal_seek_cursor`)** — https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html (systemd 262, accessed 2026-10-20). Peer-reported by `MoriR16.Registry` and `MoriR16.Knowledge`; not opened by this seat.
  - "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead." (23 words; the earlier 18-word count was a truncated quote, corrected by Knowledge.)

- **S015 systemd.journal-fields(7)** (`https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html`; peer-reported, not re-verified by this seat). Quotes from `MoriR16.Registry` and `MoriR16.Knowledge`:
  - `MESSAGE=`: "is not supposed to be parsed for metadata".
  - `MESSAGE_ID=`: "A 128-bit message identifier ID for recognizing certain message types, if this is desirable."
  - Trusted fields: "Fields prefixed with an underscore are trusted fields, i.e. fields that are implicitly added by the journal and cannot be altered by client code." (24 words)
  - `_BOOT_ID=`: "The kernel boot ID for the boot the message was generated in, formatted as a 128-bit hexadecimal string."
  - `__CURSOR`: "A cursor is an opaque text string that uniquely describes the position of an entry in the journal" (18 words). This says "position" and "uniquely describes"; S040 says the same entry may have several strings. Both are documented, so exact-byte matching stays conservative only.

- **Peer-reported S014 quotes** (`MoriR16.Registry`, `MoriR16.Knowledge`): `--boot`: "Show messages from a specific boot. This will add a match for `_BOOT_ID=`."; `--output-fields=`: "A comma separated list of the fields which should be included in the output."; `-q`: "any warning messages regarding inaccessible system journals when run as a normal user."

Version gap: the doc pages are systemd 262; the host `journalctl` is 261.2-1 (per Knowledge, and per the
`--version` reads in M12/M16). No host query was run for a semantic check, so no 262 semantics are claimed for the host.

## Source ID and used-by reconciliation

Source-row changes are **not** written by this seat. Registry's final report (`MoriR16.Registry`, 2026-10-20; supersedes all earlier summaries; no row deleted) states: S039 and S040 both `mined`, opened 2026-10-20, used-by `corpus/knowledge/journal-cursor-window-r16.md`; S014 and S015 used-by each gained the same note; the S013, S035 and S037 used-by appends were **reverted**. No immutable cell changed. This seat checked the note by static read: it cites S014, S015, S039 and S040 and does not cite S013, S035 or S037, which matches the final transitions, so none is restored. Registry-reported; not independently checked against `corpus/SOURCES.md` by this seat.

The note's line 111 still describes an earlier state (a combined S039 row, no S040). That text is stale and is routed to the knowledge owner (`MoriR16.Knowledge`); this seat does not edit it.

## Gate

Admission bar: `corpus/QUALITY.md`. Every candidate below is **pending measurement and outside closure**;
none is admitted by this lesson alone. Measured decisions will be appended after L1 runs the delivered
tool and harness once after integration.

| candidate | decision | reason / pending measurement |
|---|---|---|
| Query one scope with `--cursor=<anchor>` (plus the fixed output fields and `--no-tail --quiet --output=json`), then drop the first record **only** when its cursor and boot equal the anchor exactly; every later record must be same-boot, unique, and scalar | candidate, pending measurement | Follows S014 `--cursor=`. The next-closest sentences (S039, S040) mean a vacuumed anchor yields a different first record; exact-match refusal is the guard. The CLI's own absent-cursor behavior is not documented in S014 and is `[UNKNOWN]`. Measured only once the tool and harness exist. |
| Exact-byte cursor comparison with no alias resolution | candidate, admitted only as a **conservative** rule with documented false-unavailable | Alias statement (S040): the same entry may have multiple cursor strings. A byte mismatch can therefore be a false `unavailable`. Its result is `unavailable`, never zero. |
| Byte-mismatch as proof that the anchor was vacuumed or deleted | **rejected** | The alias statement means a mismatch is not proof of vacuum or deletion. |
| Byte-unique cursors as entry deduplication or a completeness guarantee | **rejected** | Uniqueness of byte strings is not general entry deduplication (S040). |
| `--after-cursor` used without proving the anchor first | **rejected** | Contract forbids it; S014 defines `--after-cursor=` as starting after the location, so the anchor is skipped without a presence check. |
| Zero `records_after_anchor` read as "no event occurred" | **rejected** | An empty window is a count within a window, not absence of events (QUALITY #34). It may be reported as a count with evidence basis, never as absence. |
| Parse `MESSAGE` or salvage malformed JSON for alarms | **rejected** | Round-15 rule; no structured witness is available from a broken stream. |
| Foreign-boot record, boot boundary, or non-scalar identifier promoted to positive | **rejected** | Fails the scalar current-boot predicate. Boot boundary stays `unavailable`. |
| Advance anchor automatically, or write end cursor | **rejected** | Anchor never advanced automatically; end cursor is reported, not written. |
| FR11 advanced by fixtures | **rejected** | Fixture evidence is not live cursor continuity (QUALITY #36). FR11 advances only from a live, exact retained cursor continuity receipt. |
| Re-pin old drift baseline to turn red green | **rejected** | Round-15 rule; C15-5 carried as debt. |
| Census cutover to the new window | **rejected** | Out of scope for this round. |
| New source rows **S039** (`sd_journal_seek_cursor`, `https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html`, accessed 2026-10-20, systemd 262) and **S040** (`sd_journal_test_cursor`, `https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html`, accessed 2026-10-20, systemd 262) | **candidate; both rows stand (Registry final); pending L1 verification** | S039 located quote (23 words): "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead." S040 located quote (12 words): "the same entry might be referred to by multiple different cursor strings". This seat opened the S040 page and its alias sentence matches; the S039 quote is peer-reported (Registry, Knowledge; Quality reports verifying both). Admitted use: alias false-unavailable, and the next-closest fallback for the libsystemd API only, not for the `journalctl` CLI. Not used as CLI evidence. |
| Same-boot as the anchor: every window record shares the anchor's `_BOOT_ID` (a historical boot is permitted; the window need not be the current boot) | candidate, pending measurement | Matches the spec's "same-boot as anchor". S014 `--boot`: "This will add a match for `_BOOT_ID=`." The current-boot pre-spawn gate proposed in SiblingScope §3 was retracted in its §8. |
| Pre-spawn current-boot gate (boot-id file check before `journalctl` runs) | **rejected** | Proposed in SiblingScope §3 from probes now inadmissible; L1 rejected it as unasked scope narrowing. |
| Any result from the live, `/tmp`, or background probes M7–M10 and M13–M21 (existence, boot match, density, latency, pricing) | **rejected** | Outside the no-runs contract; L1 does not use these as acceptance. |

## Known limits

- No live journal was queried and no fixture pack was executed by this seat.
- Cursor alias false-unavailable: some real continuity may be reported `unavailable` rather than recovered.
- `--output-fields` and the `--output=json` semantics are not quoted here; no claim rests on them until peer openings are published.
- Host `journalctl` is 261.2-1 per `MoriR16.Knowledge`; every quote above is from the systemd 262 pages. No live query was run by this seat, so no claim transfers 262 semantics to the host until a measured host receipt exists.
- Inadmissible probes (M7–M10, M12–M19, M21) are disclosed. No finding here rests on their outputs. The cursor-alias and seek-fallback claims rest on the documentation quotes above. Whether `--cursor` includes the anchor record as first record is `[UNKNOWN]` until L1 verifies it under its own authorized plan.
- Non-author outside closure of this round is pending; this lesson is author-lane evidence.

## Routed items

- Corrected registry line `SKILL.md:168` (C15-4): working-tree correction observed; commit owned by `mori`.
- Drift-pin debt (C15-5): carried, no re-pin.
- Quality appends Q37–Q42: owned by `MoriR16.Quality`; applied per its IRC. Quality's QUALITY #38 wording about a round-16 `/tmp` expected-probe is **r15** provenance (C15-2); owner to correct its citation.
- `SCORECARD.md:781` still lacks the "fixture" label, and QUALITY #36 cites a SCORECARD correction that does not exist (reported by `MoriR16.ReviewLesson`): routed to `mori` and `MoriR16.Quality`. Not edited here.
- Stale text in `corpus/knowledge/journal-cursor-window-r16.md:111` (describes a combined S039 row and no S040): routed to `MoriR16.Knowledge`. Not edited here.
- Source IDs S039 (seek-cursor) and S040 (test-cursor): both rows stand per Registry's final; L1 verifies against `corpus/SOURCES.md` before citation.
- Deviations M7–M10, M12–M19, M21–M25 (and M26, disclosure only): routed to L1 for disposition; excluded from delivered verification; not runtime prevention; not repaired by admonition.
- Distinction kept per parent (L1) rule: static reads, version/help/man lookups, and static parses of a seat's own fixture are allowed and are not counted as runtime violations; real outside-lane writes, live or synthetic probes, and background jobs are deviations regardless of intent.
- M20 (placeholder overwrite): restored here; ReviewCounts instructed never to touch this file again; owner-side confirmation of the restored text is requested.

## L1 integration errata and observed setup failures

The owner restoration was inspected by L1: the full declared claim,
correction queue, Mistakes, source openings and Gate sections are present;
the overwritten placeholder does not survive. Read-time open items above
are superseded by the active SKILL row, appended SCORECARD fixture-vector
correction and corrected Knowledge note in input commit `114ebe5`.
Q37 now keeps L1 omission and seat violation separate; Q42 names exact
anchor start, not gap-free continuity.

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M31 | setup-layout | `evidence/gate-selftest.json` under `.ufo/waves/round-16/`: child gate rejects output under the selftest stub's parent, outer exit1 | first authorized L1 selftest | Put all selftest tool paths in a disjoint tools subtree; do not weaken the production output guard. Same selftest command is re-run on the committed repair. |
| M32 | fixture-schema mismatch | `evidence/pin.json`: exit2, `KernelSystem.json: case lacks key(s): want` | first authorized L1 pin command | Default omitted refusal `want` to an empty subset; keep complete success expectations and global no-totals-on-refusal assertions. Fixture bytes are unchanged. |

These are actual failing setup witnesses, not production behavioral red.
The first authorized window selftest measured16/16, not the producer's
predicted17. Context selftest measured15 arms. Original wave1's explicit
live-journal prohibition was missing (exit1); its context-only corrected
fixture passed (exit0). Text conformance is not runtime prevention.

Operator wrap-up supersedes the planned wave2 duty: its32 seats were never
validated or dispatched; the round total remains64. No workers were spawned
after that directive. All seat live/synthetic probes and outside-scope
staging remain excluded from acceptance, regardless of their source value.

## Measured Gate decision — L1, superseding pending rows above

C1's bounded knowledge and capability are verified by the lane, pending
non-author closure. Measured input commit:
`87a57c13dbb1fc2d3e049bba98aca1739822b8c9`.
The same pinned16 packs/64 cases record capability_absent64 before (no
subprocess behavior existed at the entering commit), and matched64 after
with0 mismatches:30 OK,31 unavailable,3 setup. This is capability
acquisition, not64 repaired production bugs. Command and outputs:
`evidence/c1-count.json` under `.ufo/waves/round-16/`.

The repaired regression selftest passes6 named arms (`gate-selftest-fixed.json`),
the window selftest16/16 and context selftest15 arms pass. M31/M32's actual
failure receipts remain committed; same commands pass on the repair, without
changing any fixture. The context-only original→corrected comparison is
exit1→0, for static instruction text only.

Two authorized live observations return OK, one per user/system scope;
each returns0 after-anchor records and0 in every positive subset. They
demonstrate host reachability, not no events, positive live load, retention,
full access or alias/vacuum behavior. Raw live anchors were temporary
in-lane inputs and were removed; safe receipts retain anchor hashes/boot and
aggregate output only (`evidence/live-window-{user,system}.json`).
The Gate table's “current-boot predicate” wording is superseded here:
this probe binds to the **anchor boot**, which may be historical.
Its optional end cursor is a SHA-256 digest, never a raw cursor or state write.

Rejects remain rejected: approximate/missing/aliased anchors are not proven
present; mismatch is not deletion; no malformed-capture salvage, zero-event
inference, automatic advance, census cutover, authenticated emitter or unique
victim. Author-lane seats do not supply the required outside review.

Final SOURCES census exits0 before and after (W04 S035/S037 only).
Rows38→40, A35→37/B2/C1 held; mined17→19/queued20/rejected1 held.
S039/S040 enter mined; their URL/access date/located23-word and12-word
quotes are in `## Gate`. L1 reopened both official pages this round.
Exact final mutable-cell changes:

| row | used-by old → new |
|---|---|
| S014 | `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-positive-evidence-r15.md` → `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-positive-evidence-r15.md, corpus/knowledge/journal-cursor-window-r16.md` |
| S015 | `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md, corpus/knowledge/journal-positive-evidence-r15.md` → `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md, corpus/knowledge/journal-positive-evidence-r15.md, corpus/knowledge/journal-cursor-window-r16.md` |

No existing status/recheck or immutable cell changed. Temporary
S013/S035/S037 additions were reverted before delivery; their final cells
equal entering bytes. `sources-measurement.json` records the complete diff.

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M33 | misroot / scope | `evidence/misroot-sweep.json`: FieldDocs.md and ReviewLesson.md were written under fleet `.ufo/waves/round-16/build/`, despite absolute path instructions | required pre-report fleet status sweep | L1 attributed both headers, copied byte-exact to lane-relative paths, ran cmp (exit0), then deleted only the two own fleet copies under the prompt exception. All64 reports now reside in-lane. |

Final learning verdicts: expansion improved (new FR11 capability), quality
improved (stale registry corrected and actual setup failures repaired),
discernment unchanged (outside closure pending; repeated seat violations earn
no prevention credit). The round is not fully execution-conformant.
No new L0 question, install/update, pacman transaction, host service change
or worker dispatch after operator wrap-up was performed by L1.
