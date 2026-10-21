# SourcesRecheck — round 20 (seat MoriR20.SourcesRecheck)

STATUS: complete. Read-only: no edits to corpus/SOURCES.md, the census, baselines, MANIFEST, or lane git/jj state. No subagents. No tools installed or updated.

Basis: today 2026-10-21 (UTC). Registry: `corpus/SOURCES.md` (65 rows, S001–S065). Inputs: `.ufo/waves/round-20/contract.md`, `frozen/c2-expected.json`, `evidence/c1-drift-entering.json`.

## 1. Validator run (once)

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` (no `--today`, so the default UTC date 2026-10-21 applies)

```
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
rc=0
```

- rc=0 means no E01–E12 finding. Both W04 lines are warnings: S035↔S013 (same catalog file at the same commit, different scope) and S037↔S015 (same man page, different scope).
- Read-only cross-checks with the same script: `overdue --today 2026-10-21 mori` gives rc=0, zero `overdue` lines and 65 `cadence` lines. `census mori` gives rows 65; tier A 55 / B 3 / C 7; status mined 34 / queued 23 / rejected 8. An independent Python parse matches these counts, and all 65 rows have 11 cells.

## 2. Rows due by 2026-10-21

### 2a. Numeric cadence: 21 rows, none due. No 30d rows exist.

Due = opened + N days, which is the validator's rule. The earliest due date is 2027-01-17.

| due | rows (recheck, opened) |
|---|---|
| 2027-01-17 | S012, S034 (mined); S018, S024, S025 (queued) — 90d, opened 10-19 |
| 2027-01-19 | S049 (mined); S055 (rejected) — 90d, opened 10-21 |
| 2027-04-17 | S021, S028 (queued); S030 (rejected) — 180d, opened 10-19 |
| 2027-04-19 | S063 (rejected) — 180d, opened 10-21 |
| 2027-10-19 | S029 (queued) — 365d, opened 10-19 |
| 2027-10-20 | S041 (mined); S042 (queued) — 365d, opened 10-20 |
| 2027-10-21 | S050, S051, S056, S062 (mined); S054, S057, S061 (rejected) — 365d, opened 10-21 |

### 2b. On-release: 44 rows, none triggered after opening. Four are superseded at opening.

A row is triggered when its upstream channel publishes something after the row's opened date. I checked each channel against its primary release feed with GET requests only.

| channel (rows) | newest item found | vs. opened | verdict |
|---|---|---|---|
| Linux mainline (S001–S006, S033) | v7.3, tag commit c03c1a14507dfaf8b856c2608f9ac216021fc222, published 2026-10-18 (kernel.org releases.json; GitHub tag object) | before 10-19 | not triggered. S004, S005, S006 and S033 pin c03c1a14, which is the v7.3 tag commit (the registry calls it "Linux master commit"). S003 pins v7.2, which is **superseded at open**. |
| Linux 7.2 stable branch | 7.2.12, 2026-10-21 (kernel.org) | after | not triggered by content. S003 pins the immutable v7.2 tag. |
| systemd (S007–S009, S011, S013–S015, S032, S035–S040) | v262 on 2026-09-22; v262.1 on 2026-10-16; stable 261.4, 260.6, 259.10, 258.12 on 2026-10-17 (GitHub API; releases.atom) | before | not triggered. S011 pins v261, which is **superseded at open**. |
| systemd.io PRESSURE (S010) | living page, no versioned release channel found | — | cannot trigger [INFERENCE: no release channel] |
| bpftrace (S017, S019, S020) | v0.27.0, 2026-09-10 (releases.atom) | before | not triggered |
| earlyoom (S016) | v1.9.0, 2025-09-16 | before | not triggered |
| OTel semantic conventions (S022) | v1.44.0, 2026-08-04 | before | not triggered |
| OTel specification (S023) | Release 1.61.0, 2026-09-14 (releases.atom) | before | not triggered |
| OTel collector-contrib (S026) | v0.163.0, 2026-10-14 | before | not triggered |
| OTel living pages (S052, S053) | living pages, no versioned release channel found | — | cannot trigger [INFERENCE] |
| man-pages (S027, S031) | 6.19, 2026-08-25 (mirrors.kernel.org index) | before | not triggered. Both rows were accessed 2026-09-09, after 6.19. |
| jj (S044, S045) | v0.46.0, 2026-10-07; v0.45.1, 2026-09-03 (releases.atom) | before 10-20 | S045 cross-checks jj 0.45.1, which is **superseded at open**. S044 not triggered; its detached-HEAD and colocation wording was not checked against 0.46.0 notes, which added colocated workspaces. |
| git (S046, S047, S058, S059, S064) | latest source release 2.56.0, 2026-09-28 (git-scm.com) | before | not triggered |
| pacman (S048) | latest tag v7.1.0, 2025-11-01 (GitLab tags) | before | not triggered |
| Z.AI API codes (S043) | living API page, no versioned release channel found | — | cannot trigger [INFERENCE] |
| SLSA provenance (S060) | page banner: "Version 1.2 is the current version" (accessed 2026-10-21) | row pins v1.0 | **superseded at open** |
| CPython hashlib docs (S065, rejected) | not checked | — | unverified |

Superseded at open means the pinned version was already replaced before the row was opened, so the row is due now even though no release fell after its opened date:

- **S003** (kernel v7.2; v7.3 published 2026-10-18, row opened 10-19). Recheck at v7.3 / c03c1a14.
- **S011** (systemd v261; v262 published 2026-09-22, and v262.1 on 2026-10-16). Recheck at the 262 line.
- **S045** (jj 0.45.1 cross-check; v0.46.0 published 2026-10-07). Re-run the metaedit help against 0.46.0.
- **S060** (SLSA Provenance v1.0; the banner names v1.2 current). Recheck against v1.2.

On-release rows whose channel cannot fire because the source is a living page: **S010, S043, S052, S053** (S053 is queued). I recommend a date cadence for these; this is an L1 decision and I did not apply it.

## 3. Queued rows (23) that C1 or C2 could mine

Basis: each row's `teaches` text as written in the registry. This seat did **not** re-open the queued sources, so any mining still needs a located quote from the opened page. Fit grades are strong, medium, weak or none. Line numbers refer to `corpus/SOURCES.md`.

### C1 — drift baseline (the 8 unclassified tokens in c1-drift-entering.json)

Tokens: `+FINDING:COREDUMP_NOTICE_JOURNAL_USER`, `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER`, `-FINDING:WATCHDOG_STALE`, `+FINDING:UNIT_FAILURE_OUT_OF_SCOPE`, `+io_avg_unavailable`, `+path`, `+age_s`, `+round`. C1 assigns the classes. This list only says which rows could ground each reason.

| row | fit | registry teaches (quoted) | token(s) it could ground |
|---|---|---|---|
| S032 (line 38) | strong | "COREDUMP_SIGNAL supplies a numeric signal field so crash classification need not infer signal from message wording." | COREDUMP_NOTICE_JOURNAL_USER; SEGFAULT_SIGNAL11_JOURNAL_USER |
| S033 (line 39) | strong | "Field 7 counts sectors written; cumulative counters need boot and device-reset context before deriving a rate." | io_avg_unavailable |
| S006 (line 12) | medium | "Generated signals carry target and sender context; delivery is separate and may differ after a signal is generated." | SEGFAULT_SIGNAL11 (generation versus delivery) |
| S027 (line 33) | medium (also weak for C2) | "A held pidfd reports termination through polling and avoids PID reuse ambiguity, but it is a persistent handle rather than a one-shot snapshot." | -WATCHDOG_STALE (a one-shot process-state snapshot) |
| S009 (line 15) | weak | "oomctl dump reports the current contexts held by oomd without equating that state with a kill count." | none directly |
| S005 (line 11) | weak | "The victim-mark tracepoint exposes PID, comm, UID, memory fields and oom_score_adj as a distinct event schema." | none of the 8 directly (kill-class fields) |

UNIT_FAILURE_OUT_OF_SCOPE is already grounded by mined S035, S036 and S038, so no queued row is needed. The census-schema tokens (+path, +age_s, +round) need no external row because they are census-internal diffs.

### C2 — wave settlement (frozen oracle: 14 cases; the vocabulary must avoid dead, failed and killed)

| row | fit | registry teaches (quoted) | use |
|---|---|---|---|
| S022 (line 28) | strong | "The vocabulary separates a CI-system error such as a killed worker from a command failure and enumerates the run results." | settled, partial and unsettled vocabulary; the no_vocab rule |
| S028 (line 34) | strong | "An Unknown probe result requires no action and further checks, keeping missing evidence distinct from failure." | "a missing report is NOT a dead seat" framing |
| S053 (line 59) | weak | "Attributes outside an allow-list are deleted before value checks; blocked-value regexes mask allowed attributes. Allow-list is a deletion mechanism, not an anonymization claim." | allow-list output schema. The canary case is already covered by mined S049–S052. |
| S023 (line 29) | weak | "JSONL provides a file-oriented export option, but ordering and monotonically increasing timestamps are not guaranteed." | why the determinism case needs an explicit sort key |
| S042 (line 48) | weak | "Retry-After indicates how long a user agent ought to wait before a follow-up request; this section is not proof of a client retry implementation." | re-dispatch cue only; not settlement |
| S029 (line 35) | weak, B-tier | "The chapter motivates saturation measurements while discouraging learned thresholds and causal overclaims." | framing only |

Gap: the C2 path cases (traversal, absolute-path, symlink-report) and the misrooted case have no registry row. Two frontier scribes have proposed candidates, and both use the number **S066**. The candidates are `build/SrcPathContainment.md` (pathlib, lexical versus resolved containment; lines 31–34) and `build/SrcPythonLstat.md` (os.lstat, final-component symlink; lines 24–27). Neither is in SOURCES.md, and the L1 must renumber one of them at admission.

No C1 or C2 fit this round (queued): S008, S010, S017, S018, S019, S020, S021, S024, S025, S026, S048.

## 4. Malformed or inconsistent rows

Structural (validator E01–E12): none. All 65 rows have 11 cells. IDs are unique and well formed. Kind, tier and status are within the enums. Recheck values are valid. No `opened` date is in the future. Community is never tier A. The used-by check covers 59 listed paths, all of which exist. Status and used-by are coherent. S034 is the only row without a URL; it is own-work with a local path, which is by design.

Semantic (the validator does not catch these):

1. **S059 is malformed (line 65).** Its `teaches` cell is the bare placeholder "rejected", and the rejection rationale sits in `anchor`. The validator's W02 test (`length(teaches)<8`, sources-census.sh:671) passes it, because "rejected" is exactly 8 characters. The registry keeps admitted cells immutable (Search log, bounded searches 9–10), so the fix belongs in an append-only correction, not an edit.
2. **S057 (line 63):** the `scope` cell begins "REJECTED: confirmatory versus exploratory labelling…", so a rejection summary sits in the scope column while `teaches` holds the full rejection.
3. **S065 (line 71):** the `scope` cell is "Rejected as sole support for the C2 measured-revision provenance claim…", which is the same pattern.
4. **S034 (line 40) is a stale own-work receipt.** It pins census SHA-256 3da5b098…, which is `tools/mori-census.sh` at commit 1f07f1d (round-12, 22:41:08Z on 2026-10-19). The receipt run is 22:38:11Z, about three minutes earlier; it was probably taken from the working tree before the commit landed [INFERENCE]. The census has since changed in six commits (18d7d55, 8d22d18, 26f6589, 273aa74, 2be8294, fe9fa90). The current SHA is 87b8d680…, which matches the C1 contract. The 90d recheck is not due until 2027-01-17, but S034 is not a current census baseline.
5. **S027 (line 33) and S031 (line 37):** the anchors say "fetched 2026-09-09", which is earlier than `opened` 2026-10-19. This is not a validator error. The release baseline still holds, because man-pages 6.19 is the newest release.
6. **S004, S005, S006 and S033** label c03c1a14 as "Linux master commit (2026-10-18)". That commit is the v7.3 tag commit. The label is imprecise, and the pin itself is current.
7. **S059 and S065 cadence:** these rejected rows carry `on-release`, but their flip conditions are not release-driven. This is minor.
8. **Known and documented:** S014 and S015 line anchors do not reproduce on the rendered systemd 262 page (Search log Correction, 2026-10-20). Several systemd rows cite `…/man/latest/…` URLs with line anchors (S007–S009, S014, S015, S032, S037, S039, S040). "latest" moves with each release, so those anchors are unstable.
9. **Validator gaps** (reported only; the fleet script was not edited): the W02 threshold admits an 8-character placeholder; there is no column-shape rule; no rule flags a version superseded at open; and no rule flags an on-release cadence whose channel is a living page.

## 5. Not verified

- Queued source contents were not re-opened (see §3).
- The CPython channel for S065 was not checked. S023 was checked only at the spec release-feed level.
- Anchor line numbers in other rows were not re-rendered.
- Git history was read only for the 12 most recent commits that touch `tools/mori-census.sh`.

## 6. Commands and reads (all read-only)

- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` (once); `overdue --today 2026-10-21 mori`; `census mori`.
- `sha256sum tools/mori-census.sh`; `git rev-parse --is-inside-work-tree`; `git log -n 12 --format=… -- tools/mori-census.sh`; `git show <rev>:tools/mori-census.sh | sha256sum` for each listed commit.
- Grep of `corpus/evidence/roster-r12-20261019T220912Z-live.log` for the SHA pins.
- Reads: SOURCES.md, contract.md, frozen/c2-expected.json, evidence/c1-drift-entering.json, build/SrcPathContainment.md, build/SrcPythonLstat.md.
- Web and API GETs: kernel.org `finger_banner` and `releases.json`; api.github.com releases for systemd, bpftrace, earlyoom, jj, semantic-conventions, collector-contrib and otel-cli; `repos/torvalds/linux/git/refs/tags/v7.3` with its tag object; `systemd/releases/tags/v262`; `releases.atom` for systemd, bpftrace, jj and opentelemetry-specification; mirrors.edge.kernel.org (git index); mirrors.kernel.org (man-pages index); git-scm.com; slsa.dev/spec/v1.0/provenance; gitlab.archlinux.org (pacman tags).

## 7. Handoff (L1 decisions; nothing applied)

1. Recheck now: S003, S011, S045 and S060 (superseded at open). Also re-check S044 against the jj 0.46.0 notes.
2. Correct S059 (teaches placeholder), and S057 and S065 (scope cells), through an append-only correction.
3. Resolve the S066 collision before admitting a path-safety source. The C2 traversal, absolute-path and symlink-report cases need one.
4. C1: mine S032 and S033 (strong), then S006 and S027 (medium).
5. C2: mine S022 and S028 (strong). S053 and S023 are optional (weak).
6. Living-page on-release rows (S010, S043, S052, S053): replace with a date cadence at the next registry edit.
7. S034: cite only as a historical receipt. The current census baseline is the 87b8d680… revision.
8. Validator (fleet script, not edited): raise the W02 threshold, add a column-shape check, add a superseded-at-open check.
