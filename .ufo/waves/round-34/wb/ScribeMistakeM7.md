measured 2026-10-23T07:45:23Z

## Mistake candidate

- **M7 — Attempt 2 produced round integration artifacts after its last lane commit, leaving their durability and provenance unresolved at handoff.** Class: integration durability (round close without a committed integration). Evidence: the requested `git log --format='%h %cI %s' f10a320d..fd2521351c6cef47384aef30afbe1e4db7e6912e` output ends at `fd25213 2026-10-23T02:37:39-03:00` (`round-34: wave A spec/dispatch`); the permitted `stat -c '%y %n' .../.ufo/waves/round-34/wa/*.md ...` output shows later report mtimes, e.g. `ReopenS191.md` at `02:38:58.816866920 -0300` and `SentinelPrivacy.md` at `02:41:40.021595745 -0300`. The scratch snapshot files are dated `03:43:35-03:00`; those are snapshot mtimes, not established source-edit times. **[INFERENCE]** These timestamps support the gap, but this sweep cannot independently prove the exact orchestrator-death time or that every named integration artifact remained uncommitted at that instant. Captured-by: attempt 3's required re-derivation of the attempt-2 draft (assignment context; not independently verified by this sweep). Fix: before closing a round, require a final integration commit whose committer time is later than every required seat-report mtime; a reviewer compares normalized UTC report `stat` times with the final commit's `%cI`, fails if any report is newer, and confirms the commit tree contains the reports. Shown able to fail: comparing `fd25213` (`02:37:39-03:00`) with `ReopenS191.md` (`02:38:58.816866920 -0300`) already fails the timestamp gate.

VERDICT: supported

## Evidence checked

- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%h %cI %s' f10a320d..fd2521351c6cef47384aef30afbe1e4db7e6912e` — returned five commits; newest listed was `fd25213` at `2026-10-23T02:37:39-03:00`.
- `stat -c '%y %n' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/wa/*.md /fast/scratch/hyaku/mori-r34/a3-L1/drafts/*` — returned later wave-A report mtimes and scratch snapshot mtimes cited above. Scratch content was not treated as evidence.
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/mori-shokunin` — `branch=master local=5216d78dd1bc4ce57356555b509c9135a9702088 remote=5216d78dd1bc4ce57356555b509c9135a9702088 ahead=0 behind=0 head=detached tracked=5 untracked=16`. This is current state, not a historical record of the attempt-2 handoff.
- Read `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:72-113` only for M1-M6 formatting; per assignment, it is untrusted scratch and not evidence.

## Scope and limits

- Only this report was written: `.ufo/waves/round-34/wb/ScribeMistakeM7.md`. The lesson, integration artifacts, judge, and Git/JJ state were not changed.
- No tools were installed and no checks beyond the listed read-only evidence sweep were run.
- Exact crash time, full artifact count, and historical uncommitted status were not independently established by the permitted evidence.
