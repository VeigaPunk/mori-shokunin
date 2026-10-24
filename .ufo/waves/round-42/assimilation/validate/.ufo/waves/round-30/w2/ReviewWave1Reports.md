# ReviewWave1Reports — wave-1 report inventory (mori round 30, attempt 1, wave 2)

Verdict: **agree on coverage (35/35 committed, 0 missing, 0 uncommitted) — defect found on write scope**:
2 reports declare writes outside their report/scratch path (`CriticC2Design`, `ReviewC1Reachability`);
one of the two contradicts its own "Read-only" prompt, the other was instructed to use `/tmp` by its prompt.

Seat: `MoriR30.ReviewWave1Reports` (leaf, no subagents, no background jobs).
Measured tip read: `ad0f04745ced2194e58c22a0d6b38131bee3e230` (`git rev-parse ad0f047` → same).
All facts below are read-only `git ls-tree` / `git diff` / `git status` / `grep` against the lane; no lane
write except this report. No tool installed or updated (nothing needed).

## 1. Spec set vs committed set

- Spec item count: `git show ad0f047:.ufo/waves/round-30/wave1-spec.json | jq -r '[.items[].name] | sort | .[]' | wc -l`
  → `35` (`.ufo/waves/round-30/wave1-spec.json`, `reportDir: .ufo/waves/round-30/w1`).
- Committed at the measured tip: `git -C <lane> ls-tree --name-only ad0f04745ced2194e58c22a0d6b38131bee3e230 .ufo/waves/round-30/w1/`
  → 35 `.md` entries (the command in the ticket printed all 35; names below).
- Set difference both directions is empty (`comm -23` and `comm -13` over the jq name list and the
  `ls-tree` basenames printed nothing). So **no spec seat lacks a report, and no committed report lacks a spec seat**.
- File name = seat name for all 35; the registry at HEAD agrees: `git show HEAD:.ufo/waves/round-30/w1/swarm-registry.json`
  has `members` length `35` and the same 35 names (`jq -r '.members|length'` → 35), `wave: mori-r30-w1`.
- No zero-byte or stub report: `git ls-tree -r -l ad0f047 .ufo/waves/round-30/w1/ | awk '$4==0'` → 0 lines;
  smallest blob is `RetentionBase.md` at 4854 bytes (37-line `FixToolResidual.md` is 5397 bytes and carries
  the unified diff it promises, `FixToolResidual.md:1-14`).

## 2. Missing / uncommitted

- Missing: **none** (section 1).
- Uncommitted: **none**. `git status --porcelain -- .ufo/waves/round-30/w1/` → empty;
  `git diff --stat HEAD -- .ufo/waves/round-30/w1/` → empty; `git ls-files --others --exclude-standard .ufo/waves/round-30/w1/` → empty.
- Tip-vs-HEAD caveat for a later checker: `git diff --stat ad0f047..HEAD -- .ufo/waves/round-30/w1/` shows
  one added file, `swarm-registry.json` (+219), committed at `713be29`; `ls-tree HEAD` therefore lists 36
  entries. Only 35 are reports — the 36th is the registry artefact. Counting `ls-tree HEAD` as "36 seats"
  would overcount by one.
- Working tree `swarm-registry.json` is mode `600` and tracked at HEAD; it is not an uncommitted report.

## 3. Reports that say they wrote outside their scratch/report path

### 3.1 `CriticC2Design` — self-declared `/tmp` write, against a "Read-only" prompt (defect, low severity)

- `CriticC2Design.md:8`: "One scratch file of seat briefs was written to `/tmp` and deleted; nothing else was
  written outside this report."
- Its spec prompt is `.ufo/waves/round-30/wave1-spec.json` item `CriticC2Design`, which ends
  "Read-only; do not open the tool." (quoted from `git show ad0f047:...wave1-spec.json`). The wave-1 context
  bound is stricter still: write only the report, and scratch only under `/fast/scratch/hyaku/mori-r30/<seat>/`.
- No scratch dir exists for this seat: `ls /fast/scratch/hyaku/mori-r30/` lists `CriticC1Design` but not
  `CriticC2Design`, so the `/tmp` file was written outside both permitted locations.
- What I can observe: the file's content is not quoted anywhere in the report; no leftover remains that I can
  name (the report names no file path, so I cannot probe it). Whether a writer ever saw it is **unknown**
  [INFERENCE: no committed evidence either way; writers were confined to `rule-text.md` plus upstream URLs
  by their prompts, `wave1-spec.json` items `CaseR30a`-`CaseR30d`].
- Not a lane write: the report states "nothing else was written outside this report", and `git status` at
  `ad0f047` is consistent with that.

### 3.2 `ReviewC1Reachability` — `/tmp` scratch, but the prompt told it to (bound/spec tension, not a rogue write)

- `ReviewC1Reachability.md:11-12`: "four `--inputs` spot-runs with the tool and each inputs object copied to /tmp".
- `ReviewC1Reachability.md:159`: "`--inputs` spot-runs (tool copied to /tmp, inputs written to /tmp)".
- `ReviewC1Reachability.md:214`: "Scratch: `/tmp/mok-spot-mdc87z6k` and `/tmp/mok-spot2-*` held the copied
  tool and inputs objects and were removed after the runs. The only lane write is this report."
- The item prompt for `ReviewC1Reachability` in `wave1-spec.json` explicitly asks for spot-runs "from temp files
  under /tmp", so the seat followed its item brief; the wave-level "own scratch dir" bound and the item brief
  disagree. No `/fast/scratch/hyaku/mori-r30/ReviewC1Reachability` dir exists, which is consistent with it
  using `/tmp` instead.
- Cleanup claim is consistent with the host: `ls -ld /tmp/mok-spot* /tmp/mok-spot2-*` →
  "No such file or directory" for both patterns.

### 3.3 Mentions that are **not** seat writes (checked, no defect)

- `FixBlindGate.md:189-190`: its gate script does `SELFTEST_TMPROOT=$(mktemp -d "$tmp_root/blind-gate-selftest.XXXXXX")`
  under `${TMPDIR:-/tmp}`. That is the delivered script's runtime behaviour under `--selftest`, not a write by
  the seat; the seat's own artefacts are `FixBlindGate.md:3` — the script under its scratch dir and this report.
- `CriticHarmScreen.md:82` says "`<tip>` is the landed tip; run in the lane (read-only) or a sandbox clone", and
  `:89-95` is a fenced sh block that writes `/tmp/t.py` and `/tmp/c.json`. These are instructions for the L1 to
  reproduce the screen, not statements that this seat ran them; the report never claims to have done so.
- Sandbox git writes inside the seat's own scratch are permitted and declared: `TipReceiptsR1.md:27-36`
  (`git clone --no-hardlinks ... /fast/scratch/hyaku/mori-r30/TipReceiptsR1/repo`, then `cp` and `git add`
  inside that clone); `FixToolResidual.md:3` (tool edited only in its clone
  `/fast/scratch/hyaku/mori-r30/FixToolResidual/lane`).
- Confinement statements that match the committed tree (spot-read): `SrcUnitActiveEnter.md:4`,
  `SrcUnitTimestampSet.md:5-6`, `SrcJournaldSuppressed.md:5,143`, `SrcShowZeroStamp.md:5`,
  `SrcEarlyoomServiceRestart.md:143`, `SrcJournalctlBoot.md:5-6,162`, `DraftEntryC1.md:229-231`,
  `DraftQualityRows.md:4`, `DraftSkillRows.md:110`, `DraftCorrectionsR2R3.md:187-189`, `MineMistakes.md:4`,
  `ConnectorSiblings.md:110`, `ScoutSourcesDup.md:3`, `ScoutProvinceStale.md:236`, `ReviewJudgeRulings.md:20`,
  `DraftProvinceR7.md:5`, `ProbeC1Cases.md:7`, `RetentionBase.md:27` (invented fixture inside its own scratch clone).
- No report claims a write to `/home/vgpnk/Projects/shokunin`, a sibling lane, `~/.local/bin`, `local://`, or the
  lane's `corpus/`, `SKILL.md`, `SOURCES.md`, `QUALITY.md`, `LOG.md`, `SCORECARD.md` (grep over all 35 for
  write verbs next to those paths returned nothing).
- No report references the shared files sitting directly in `/fast/scratch/hyaku/mori-r30/`
  (`entry-draft.md`, `skill-round30.md`, `sources-rows.txt`, `src-blocks.txt`, `r29w1.txt`, `r30w1.txt`,
  `fleet-status-start.txt`, `c1-sandbox.sh`, `L1-tool.diff`, `L1-c1-sandbox/`); grep for those names in the 35
  reports returned nothing. They are unattributed to any seat report.
- No seat claims a tool install or update (grep for install/upgrade/pacman lines: all 35 say none), so the
  tooling directive has nothing to record from wave 1. This seat installs nothing.

## 4. Trailer hygiene (observation, not a defect against the prompts)

- Only 5 of 35 reports carry a `Report:` line, and each points at itself:
  `ConnectorSiblings.md:113`, `CriticHarmScreen.md:250`, `DraftSkillRows.md:126`, `ScoutCarriedDebt.md:117`,
  `SrcJournaldSuppressed.md:159`.
- The 4 prompts whose text matches `Report:` (`BuildCountC1`, `BuildCountC2`, `FixBlindGate`, `FixToolResidual`)
  use it as a field label ("Report: the script in a fenced block, ..."), not as a trailer instruction; no item
  prompt requires a trailer. So the missing trailer on the other 30 is not a spec violation, only a
  convention gap that a checker must not treat as a missing report.

## 5. Confidence and remaining unknowns

- Confidence: **high** on counts and set equality (two independent enumerations: spec JSON and `ls-tree`, plus the
  HEAD registry), and high on the two self-declared out-of-path writes (direct quotes at the cited lines).
- Unknown 1: whether `CriticC2Design`'s `/tmp` "seat briefs" file existed long enough, and with what content, to
  be openable by a blind writer. No committed byte records it; the report names no path.
- Unknown 2: whether any seat used `/tmp`, `mktemp` or another out-of-tree path without declaring it. Only
  declared writes can be inventoried from committed bytes; host scratch outside the lane is not fully auditable
  after the fact (this seat did not scan `/tmp` for other files, to stay inside its read scope).
- Unknown 3: the wave-level bound and the `ReviewC1Reachability` item brief disagree about `/tmp`; someone owning
  the wave context must say which wins for future waves. I did not pick one.
