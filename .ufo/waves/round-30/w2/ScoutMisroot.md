# ScoutMisroot — fleet-root misroot sweep, mori round 30

**Verdict: agree** — nothing with MoriR30 seat content is misrooted at the fleet root
`/home/vgpnk/Projects/shokunin`, and the three named directories do not exist there at all.
**Defect found elsewhere at that root:** six untracked strays plus two staged build artifacts,
including a misrouted tool-output file literally named `write` (staged) and a Cloudflare
bot-challenge page persisted as `bm.json`. None is mori round-30 content.

Attacks: the assumption that seat writes for mori round 30 stay inside the lane repo, and the
completeness of the fleet-root dirty set.

## 1. Required list — dirty paths whose *content* names "mori round 30" or a MoriR30 seat

Snapshot 2026-10-22T19:05:40-03:00, fleet root. Two rows.

| status | path | size (B) | sha256 |
|---|---|---|---|
| M | `.ufo/watchdog.log` | 63201 | `bebfead5ac658801e324af13b83c06b314a5959c6ff090d3f202155b7f6e1895` |
| M | `.ufo/state/mori.report-baseline` | 68 | `0cbee464cca4087c71b84a9448808ccdc120259d59e721c428c6af3036291bd9` |

Matching content:
- `.ufo/watchdog.log:766` → `2026-10-22T18:01:21-03:00 launch mori round=30 pgid=45266 driver=hyaku-inline attempt=1`.
  Same file also carries `launch kake round=30` (`:261` of the diff, `complete` at `:262`-adjacent
  hunk) and `launch tsukuroi round=30` — driver bookkeeping, not seat output.
- `.ufo/state/mori.report-baseline:1` → `30 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
  Field 1 is the round number: `record_report_baseline()` writes `printf '%s %s\n' "$n" "$digest"`
  (`scripts/shokunin-watchdog.sh:120`, called from `scripts/hyaku/inline.sh:100` with the claimed
  round). Field 2 is the sha256 of the report, or the empty byte stream when the report is absent
  (`report_digest()`, `scripts/shokunin-watchdog.sh:108`). `e3b0c442…` is sha256 of empty input, so
  the baseline means "mori round 30 recorded, report not yet present at dispatch". HEAD held `22 …`
  for the same file.
  Content-identical to `.ufo/state/tsukuroi.report-baseline` (also `30 e3b0c442…`, same sha256
  `0cbee464…`) — equality of hashes here does not imply copy; both lanes dispatched round 30 with
  no report on disk yet.

Fleet-root files naming mori round 30 / `MoriR30` that are **tracked and unmodified** (therefore
outside the dirty list, recorded for completeness, hashes at the same snapshot):
- `.ufo/prompts/mori-round-30.md` — 26360 B, `f8ab58e7708520ba9b479144facda6303a7ac20be7e7c79686cbc57cf094fec6`;
  committed by `inline.sh dispatch` via `fleet-commit.sh` (`scripts/hyaku/inline.sh:88-100`).
- `.ufo/waves/hyaku/PHASE4.md:61` — names `L1 MoriR30` (`base 58b61681`, `evidence ad53f62`);
  20017 B, `11662cc7a39db95561a73861442580a36be846d46cd8a102f669a0267f06b11a`, `git diff HEAD` empty.

## 2. Named-directory clause

`git -C /home/vgpnk/Projects/shokunin status --porcelain` and direct checks:

| fleet-root path | result |
|---|---|
| `.ufo/waves/round-30/` | ABSENT (`ls: cannot access`) |
| `corpus/` | ABSENT |
| `tools/` | ABSENT |

The correct homes exist only inside the lane: `mori-shokunin/.ufo/waves/round-30`,
`mori-shokunin/corpus`, `mori-shokunin/tools` (all `EXISTS`, checked with `[ -d ]`). Nearest
fleet-root neighbour `.ufo/reports/round-30/` contains only `kake.md` (8952 B,
`1cf462b0a1301e7e1426e499f41f7bea6a211af9b928f0f161fdbff3be20d05b`, header "kake round 30 report")
and `kotodama.md` (2485 B, `dcfebb7dffe9cd2a251236219cc95920849729348223eee445b5f8a9ce579dd4`,
header "kotodama — round 30 report (2026-10-18)", committed `3806217`). Both are genuine
fleet-level reports for *other* lanes' round 30, tracked and clean — not misroots and not mori.

## 3. Full dirty inventory (23 rows, sizes and sha256)

`M`/`A` = tracked (working-tree modified / index-added), `??` = untracked. All `.report-baseline`
files are 68 B driver state; identical content across lanes yields identical hashes.

| st | size | sha256 | path |
|---|---|---|---|
| M | 68 | `268504bbfa635583de680ad67a18082e1780764e119424cbddf7731d072bb393` | `.ufo/state/chousa.report-baseline` (`28 …`) |
| M | 68 | `268504bbfa635583de680ad67a18082e1780764e119424cbddf7731d072bb393` | `.ufo/state/kagi.report-baseline` (`28 …`) |
| M | 68 | `6e33063cea53f75b7afbfcc8955f9929462acc240c9d21a770e5d4dab70daad2` | `.ufo/state/kaidoku.report-baseline` (`29 …`) |
| M | 68 | `ed9951ef052a6e0fa4703bc182b8aabc9f96877046c1e9bd9f09f80771115b88` | `.ufo/state/kake.report-baseline` (`35 …`) |
| M | 68 | `bbb0b5be288f5353b58b59c21b3b102abce9d11e17f7e61542ac585b7a4623de` | `.ufo/state/kama.report-baseline` (`25 …`) |
| M | 68 | `6e33063cea53f75b7afbfcc8955f9929462acc240c9d21a770e5d4dab70daad2` | `.ufo/state/kengaku.report-baseline` (`29 …`) |
| A | 68 | `c5fbb77148c6960d4c29ae46aa84eee71d0cead119f7e9a6999768cfc1fe5e11` | `.ufo/state/kotoba.report-baseline` (`54 …`) |
| A | 68 | `88d916c7f2118571887bf5601d72e9806ba1dd8549fd39401921bc4a0e603e81` | `.ufo/state/kotodama.report-baseline` (`56 …`) |
| M | 68 | `95e2d396bd2de06d5ac5c186cb528c615df74757e5acd13c7e83e767d714181a` | `.ufo/state/kumitate.report-baseline` (`43 …`) |
| M | 68 | `330bcaf9ab26161f387744a9124f83ed05fcb5fd683e83a6890ff707e570d1ee` | `.ufo/state/mado.report-baseline` (`23 …`) |
| M | 68 | `0cbee464cca4087c71b84a9448808ccdc120259d59e721c428c6af3036291bd9` | `.ufo/state/mori.report-baseline` (`30 …`) |
| A | 68 | `c616a0fa7ffb433ce13f952b5872067d5c7f0f229d29ec295ffb6a6acaa9c2db` | `.ufo/state/revenger.report-baseline` (`62 …`) |
| M | 68 | `268504bbfa635583de680ad67a18082e1780764e119424cbddf7731d072bb393` | `.ufo/state/tameshi.report-baseline` (`28 …`) |
| M | 68 | `0cbee464cca4087c71b84a9448808ccdc120259d59e721c428c6af3036291bd9` | `.ufo/state/tsukuroi.report-baseline` (`30 …`) |
| M | 63201 | `bebfead5ac658801e324af13b83c06b314a5959c6ff090d3f202155b7f6e1895` | `.ufo/watchdog.log` |
| A | 10738 | `3700bf9a7137c40b7e13010ce982fbed99deed7574b8e0ef8357dfcfcc404579` | `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` |
| A | 25 | `95443b228053f4522714b3ba9cdb56cbce2e2c43b43b073b56e2c70978e0bac0` | `write` |
| ?? | 5921 | `382f28ab4e2846a94e176f67b5ea93d6c6a347997778a10ddc4c78772886eb86` | `AGENTS.md` |
| ?? | 5563 | `0c3a365ad3530f02b88c8b453f901cc2178b05d8a97aa00d6f7066cdf09c7816` | `bm.json` |
| ?? | 5196 | `918d496cf0c3e6afda37d8badf7ad046dd9a08eba3767071cb5caebdf9e0a7de` | `live_s228.html` |
| ?? | 68855 | `bee96464d0fe77f7e7abb84b2ad905954e45bf8a133a80bb5626f418a047a06b` | `nama.html` |
| ?? | 10708 | `a0b914e3bb3a8679ff5249fcfebaf6492714b3b2b7dc67cbe605595c627e79db` | `scripts/hyaku/__pycache__/wave-live.cpython-314.pyc` |
| ?? | 5583 | `9f07c0d0e4afa6eaf3aaf6531b3dc355bf364319b5d6edf6dcfe61fdcd3011c3` | `tf_bavelas.html` |

Content checks on every untracked/added non-baseline row: `grep -c -i -E 'MoriR30|mori round 30|mori-r30|round-30'`
returns 0 for `AGENTS.md`, `bm.json`, `live_s228.html`, `nama.html`, `tf_bavelas.html`, `write`, and
both `.pyc` files (`grep -a`, CPython 3.14). `grep -rIl 'MoriR30'` over the fleet root excluding
`.git` and the lane repo returns exactly one file, the tracked `.ufo/waves/hyaku/PHASE4.md`.

## 4. Defects found (outside the mori round-30 claim)

1. **`write` is a misrouted tool-output file, and it is staged.** 25 B, content
   `agent://U100N079H334f935b` (a `write` call whose path argument became a filename; the target is
   another seat's agent id, not a MoriR30 seat). Status ` A` — a fleet commit with a broad pathspec
   would publish it.
2. **`bm.json` is a saved bot challenge, not JSON.** First bytes are
   `<title>Just a moment...</title>` / Cloudflare `challenge-platform` CSP markup. No mori text. It
   is untracked; persisting challenge HTML under a `.json` name also invites a tool to parse it as
   data. Nothing here passed the challenge — this is only a recorded page.
3. `live_s228.html`, `nama.html`, `tf_bavelas.html` — untracked fetch strays whose names suggest
   source research (`S228`); content contains neither `MoriR30` nor `round-30`. Provenance
   unattributed (see §6).
4. `scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` is staged (` A`) and
   `wave-live.cpython-314.pyc` is untracked — build artifacts inside a tracked source tree.
5. `AGENTS.md` at the fleet root is untracked (looks like intended repo documentation; no mori
   content).

## 5. Method (read-only)

`git -C /home/vgpnk/Projects/shokunin status --porcelain`; per-row `stat -c%s` + `sha256sum`;
`git diff HEAD -- .ufo/state .ufo/watchdog.log`; `git show HEAD:<path> | cut -c1-40` for the
before-values; `git ls-files --error-unmatch` for tracked status; `grep -rIl` content sweeps;
`grep -a` over the `.pyc`; `sed -n` reads of `scripts/shokunin-watchdog.sh` (`:108`, `:120`) and
`scripts/hyaku/inline.sh` (`:88-100`). No file was created, modified, moved or deleted outside this
report; no git/jj write occurred; no unit, process or service was touched.

## 6. Unknowns / limits

- `.ufo/watchdog.log` is **live**: the same sweep read it as 110 s apart and got sha256
  `abaa5d93…` then `bebfead5…` (63201 B at 19:03:39). Treat the hash as point-in-time and re-hash
  before any comparison; growth is driver appends, not a seat write.
- Content scanning was limited to dirty rows plus a `MoriR30` sweep; gitignored files were filtered
  by *name* only (`git status --ignored=matching` + grep for `round-30|mori|corpus|tools` returns
  only `!! mori-shokunin/`, the expected nested lane repo, and the mori baseline row). An ignored
  file whose *content* names MoriR30 would not appear here.
- Attribution of the four html/json strays to a specific seat is unproven: their content carries no
  agent id. `write` does carry one, and it is not a MoriR30 seat.
- The lane's own round-30 tree was checked for existence only; its contents belong to the lane
  seats, not this sweep.

## 7. Tooling

No tool installed or updated during this sweep (host pacman transactions are paused per bounds; none
was needed). Read-only git only; scratch use limited to command substitution.
