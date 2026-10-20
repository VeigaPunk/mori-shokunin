# MisrootR16Facts — MoriR17.MisrootR16Facts-5 (scout)

Read-only fact finding for the r16 misroot Mistakes row. All observations 2026-10-20, seat
`MoriR17.MisrootR16Facts-5`, at lane tip `24526ea` / fleet HEAD `206442a`. No edits, no VCS writes,
no executions beyond reads/hashes and read-only git plumbing.

## Verdict

1. **File confirmed.** `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson` =
   **847 bytes**, sha256 **`15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e`**, and
   it has **zero newline bytes**: the whole file is its first line (verbatim below).
2. **The r16 sweep did use a pathspec** — exactly the addendum's
   `git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/waves .ufo/reports`
   (two-element pathspec, fleet-root-relative), recorded in
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-16/evidence/misroot-sweep.json:2`,
   exit 0 (line 3). Because the pathspec is rooted at `.ufo/`, it cannot see a plain top-level file.
3. **The instructing text** is `scripts/hyaku/lane-addendum.md` §3 (write scope), introduced by
   commit **`8bda79b`** (2026-10-20T05:44:32-03:00), new lines **92–96**, blob
   `d3cbd4c6e1d637ccbee7b24b3778824cc00e137c`. The wave was launched 5 s later
   (`2026-10-20T05:44:37-03:00`), so that revision was the rendered instruction.

## 1. File facts (observed)

Target: `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson`

| Fact | Value | Command (rc) |
|---|---|---|
| size | 847 bytes | `stat -c '%s'` (rc 0) |
| sha256 | `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e` | `sha256sum` (rc 0) |
| md5 | `de92f967ad2b89885ab6ab7ee7e4d469` | `md5sum` (rc 0) |
| newline count | `0`; last byte `0x2e` (`.`) — no trailing newline | `wc -lc` → `0 847` (rc 0); `tail -c1 \| od -An -tx1` |
| mtime | `2026-10-20 05:52:24.199681143 -0300` | `stat -c '%y'` (rc 0) |
| tracked? | yes, fleet repo; added by `ac0a7fc` (2026-10-20T06:30:51-03:00, wrap-up "archived seat notes") | `git ls-files --error-unmatch` (rc 0); `git log --diff-filter=A` |
| HEAD bytes | working tree sha256 == `git cat-file -p HEAD:…` sha256 | both `15f9f82d…`; `git hash-object` = HEAD blob |

First line = entire file (847 chars, single paragraph, quoted verbatim as data):

> BootContinuity disclosure (inadmissible, not verification): (1) Live read-only journalctl probes
> ran on the host: a current-boot cursor fetch (rc 0, 2 records, cursor/boot fields only), an
> --cursor anchor query (rc 0, records not counted), a fabricated-cursor query (rc 1, empty
> stdout), and a --user -n 1 query (rc 0, 337 bytes). One of these ran as background job bg_2667,
> started before the no-runs instruction; it completed on its own; I did not re-run it. (2) Scratch
> files were written to /tmp (/tmp/.probe_null, /tmp/.x) during the probe and removed afterwards.
> Results from (1) are not used as evidence in BootContinuity.md beyond the disclosed observation
> that the fabricated cursor refuses with rc 1; cursor inclusivity on this host is unobserved.
> Findings rest on S014/S015/sd_journal_test_cursor static text only. No further execution.

Name/content mismatch (observed): the file is named `MoriR16.Lesson` but holds no lesson — it is a
BootContinuity disclosure addressed *to* the Lesson seat, i.e. a peer message written as a path.
Writer identity is not recorded in the file (see Unknowns).

## 2. Round-16 sweep evidence (observed)

File: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-16/evidence/misroot-sweep.json`
(1004 B, mtime `2026-10-20 06:14:43.654750824 -0300`).

- `line 2` `command`: `git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/waves .ufo/reports`
  — a real pathspec (`--` separator, two paths), resolved against the **fleet root**, so the match
  set is exactly `.ufo/waves/**` + `.ufo/reports/**`.
- `line 3` `exit_code`: `0`.
- `observed_stdout`: `?? .ufo/waves/hyaku/` and `?? .ufo/waves/round-16/build/` (nothing else).
- `own_misroots`: `FieldDocs.md` (sha256 `e451a53a…`, `copied_byte_exact: true`, `cmp_exit_code: 0`,
  `fleet_copy_deleted: true`) and `ReviewLesson.md` (`e6eaf754…`, same flags).
- `foreign`: `"hyaku directory not opened or modified"`; `scope`: `"Only two attributed mori report
  files copied, cmp-verified and removed from fleet root under prompt exception"`.

Pathspec is why the root file was invisible: `MoriR16.Lesson` sits at the fleet repo root, which is
outside both pathspec elements. Its observed mtime (05:52:24) precedes the sweep (06:14:43), so it
existed while the sweep ran and still could not appear [mtime-preservation method unobserved; the
ordering conclusion is [INFERENCE] from the observed mtime].

Timeline (observed timestamps): write mtime **05:52:24** → sweep **06:14:43** → archive commit
**`ac0a7fc` 06:30:51** (16 min after the sweep, 38 min after the mtime).

## 3. Addendum text that instructed the pathspec (observed)

`/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md`, §3 "Write scope", added by commit
`8bda79b2a65cdf1b2cce78f9fb72f7bc47180bfd` (`8bda79b`, 2026-10-20T05:44:32-03:00, subject
`ops(hyaku): addendum — L1 misroot sweep before report (copy seat files from fleet root into lane,
cmp, delete fleet copy)`; `git show --stat` = 1 file, +5 lines). Blob at that commit
`d3cbd4c…`, file sha256 `721c231b3d1de943222d717dc77f7457557fb9b14b91a29a801a58e92116d4bd`.

New lines **92–96** of that revision, verbatim:

> **Misroot sweep before the report:** run `git -C {{FLEET_ROOT}} status --porcelain -- .ufo/waves
> .ufo/reports`. For every untracked file one of your seats wrote into the fleet root (check its
> content names your lane/round), copy it byte-exact into the same relative path under
> {{LANE_CWD}}, verify with `cmp`, then delete the fleet copy (the one fleet-root deletion you may
> make) and record the misroot under `## Mistakes`. Never touch files another lane's seats wrote.

Dispatch correlation: `…/round-16/dispatch-digest.json` records
`2026-10-20T05:44:37-03:00 launch mori round=16 … driver=hyaku-inline attempt=1` — 5 seconds after
the commit, so the dispatched prompt carried this revision [INFERENCE: rendering source is the
working tree; only the timestamps are observed].

The pathspec form was later removed by commit `4bb0943` (2026-10-20T10:13:55-03:00), which changed
the same bullet to `git -C {{FLEET_ROOT}} status --porcelain` (no pathspec — seat notes have landed
as plain files at the fleet root). The current file (clean at fleet HEAD `206442a`; last touched by
`c68af97`, blob `94047fb0…`, 197 lines) carries that wording at **lines 134–139**; the bullet is
otherwise unchanged.

Scope of the instruction: `templates/round-prompt.md` has **0** matches for `misroot`
(`grep -c -i misroot` → `0`, rc 1) and so does `scripts/hyaku/closure-prompt.md` (same, rc 1).
The pathspec instruction existed only in the addendum.

## 4. Existing in-tree records (observed, for de-duplication)

- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-16-verifier-spotcheck.md:202-208`
  already names the defect: the file is "a message written as a path", archived byte-for-byte, "It
  appears in neither the lesson Mistakes table nor `misroot-sweep.json`. The sweep used the
  addendum's pathspec `-- .ufo/waves .ufo/reports`, so L1 followed the instruction as written, but
  the write remains an outside-lane write. Append a Mistakes row naming it."
- `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/HANDOFF.md:142-145`: three late-found notes
  (`MoriR16.Lesson`, `SoujiR15`, `TameshiR15`) were "outside the `.ufo/` sweep pathspec" and are
  archived under `.ufo/waves/hyaku/misroots/`; "Future misroot sweeps should check
  `git -C <fleet> status --porcelain` with no pathspec."
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-16.md:244` = **M33**, which
  records only the *two recovered report files* (`FieldDocs.md`, `ReviewLesson.md`) and the
  pathspec sweep; it does **not** mention the root-level plain file. L1 report
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/mori.md:13` says the same and cites M33.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-16/build/Lesson.md:21-27` Mistakes
  table is M1–M26 with no row for any fleet-root write (M20 is the lesson-file overwrite).
- Fleet root today: `MoriR16.Lesson`, `SoujiR15`, `TameshiR15` are all **ABSENT** (test -e each);
  the only copy is the archived one, tracked at `ac0a7fc`.

## 5. Draft Mistakes row (facts only, for L1's table)

| id | class | what | where | instruction in force | disposition |
|---|---|---|---|---|---|
| (next M-id) | misroot / message-as-path | A round-16 seat wrote an 847-byte, single-line BootContinuity disclosure as a plain file at the fleet repo root — a peer message written as a path; never copied into the lane by the seat, never listed in `misroot-sweep.json`. | `/home/vgpnk/Projects/shokunin/MoriR16.Lesson` (fleet root, outside lane and outside `.ufo/`); sha256 `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e`; mtime 2026-10-20 05:52:24-03 | lane-addendum §3 (commit `8bda79b`, lines 92–96): `git status --porcelain -- .ufo/waves .ufo/reports` — the prescribed pathspec cannot match top-level files, so the L1 sweep followed the text verbatim and still could not detect the file. Not a disobedience; an instruction-scope defect. | Detected only post-hoc: archived byte-for-byte (`cmp`-equal to HEAD blob) at `.ufo/waves/hyaku/misroots/MoriR16.Lesson` by commit `ac0a7fc` (06:30:51), 16 min after the sweep (06:14:43) and 38 min after the observed mtime. Fix so far is instruction text only (`4bb0943`: no pathspec); no runtime prevention exists. |

Notes L1 may want in the row/caption: the sweep receipt is internally honest (command = addendum
text, exit 0, stdout limited to `.ufo/` matches) so it is evidence of *scope*, not of a false
record; M33 covers only the two report files under `.ufo/waves/round-16/build/` and must not be
read as covering this file; the reader must also see that this was one of three root-level notes
archived together (`SoujiR15`, `TameshiR15`), per `HANDOFF.md:142-145`.

## Confidence

- File size/sha256/first line/tracked-at-`ac0a7fc`: **observed, high** (three independent commands,
  working tree == HEAD blob).
- Sweep used the addendum pathspec: **observed, high** (command string verbatim in the receipt;
  stdout consistent with the pathspec scope).
- Instructing text = `8bda79b` §3 lines 92–96: **observed, high** (diff and commit timestamp;
  dispatch 5 s later). [INFERENCE] only on prompt rendering from the working tree.
- Root file present *at sweep time*: **observed mtime + [INFERENCE]** on mtime preservation.
- Attribution of the write to a specific seat/round-16 process: **UNKNOWN**.

## Remaining unknowns

1. Which round-16 seat wrote `MoriR16.Lesson` — the content is BootContinuity-addressed, but the
   writer id is not recorded in the file, in `misroot-sweep.json`, or in `swarm-registry.json`
   (which lists `MoriR16.Lesson` only as a recipient agent id, line 154). Same question for the
   sibling notes `SoujiR15` / `TameshiR15` (archived together at `ac0a7fc`; per-file authorship
   unobserved).
2. Whether any other fleet-root file our seats wrote *before* `4bb0943` still exists untracked: not
   enumerated here (a no-pathspec `git status` at the fleet root was not run — my item names no
   such command; the three known names are absent, and fleet root is being written by live hyaku
   sessions).
3. Original write time vs archived mtime: `mv`/`cp -p` cannot be distinguished from the current
   tree; ordering (05:52:24 < 06:14:43) holds either way under the stated inference.

## Seat hygiene

No installs or upgrades (none needed; no tool/version/channel to record). No background jobs, no
`journalctl`, no `/tmp` writes, no pacman, no VCS mutation (`git log/show/cat-file/ls-files/
hash-object/rev-parse` reads only), no writes anywhere except this report. Peer files untouched.
