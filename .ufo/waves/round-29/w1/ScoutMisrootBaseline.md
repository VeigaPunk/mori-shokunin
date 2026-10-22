# ScoutMisrootBaseline — round-29 wave-1 misroot baseline (before wave writes)

Seat: MoriR29.ScoutMisrootBaseline (leaf, read-only). Snapshot window 2026-10-22T19:55:43Z–20:00:18Z.
Lane HEAD `8a45cefe84af0557b457308e4e0f679ca490f9e9`; fleet HEAD `63729047644f839fe4c8cc97abd0d8bf741a5787`.
All mtimes below are stated twice: `stat` local (-0300) and UTC. Hashes are `sha256[:16]`.
Nothing was edited outside this file; the oom-killers tool was never opened or run; no tools installed.

Commands used (read-only): `git status --porcelain [-uall]`, `git ls-files -s`, `git diff [--cached] --numstat`,
`git log -- <path>`, `git ls-tree HEAD -- <path>`, `git rev-parse`, `stat`, `sha256sum`, `find`, `grep`.
After the first call I added `--no-optional-locks` (see disclosure §5).

## 1. Fleet root — untracked files (`git -C /home/vgpnk/Projects/shokunin status --porcelain -uall`, 5 entries)

| path | bytes | sha256[:16] | mtime (UTC) | classification |
|---|---|---|---|---|
| `AGENTS.md` | 5921 | `382f28ab4e2846a9` | 2026-10-22T18:12:23Z | fleet-root protocol doc; NOT mori/round-29 |
| `live_s228.html` | 5196 | `918d496cf0c3e6af` | 2026-10-22T15:45:20Z | bot-challenge page; source-id name (S228) |
| `nama.html` | 68855 | `bee96464d0fe77f7` | 2026-10-22T17:24:25Z | upstream 404 page; NOT mori/round-29 |
| `tf_bavelas.html` | 5583 | `9f07c0d0e4afa6ea` | 2026-10-22T15:45:19Z | upstream bot interstitial; NOT mori/round-29 |
| `scripts/hyaku/__pycache__/wave-live.cpython-314.pyc` | 10708 | `a0b914e3bb3a8679` | 2026-10-22T17:06:56Z | CPython 3.14 bytecode of tracked fleet script |

Evidence per row:

1. `AGENTS.md` first lines: "# AGENTS.md / Fleet root for the **shokunin** (職人) protocol …" (`AGENTS.md:1-2`). Content
   hits: `grep -ci` for `mori` = 0, for `round 29`/`round-29` = 0, for `earlyoom`/`systemd` = 0. Provenance: `git log
   -- AGENTS.md` prints nothing and `git ls-tree HEAD -- AGENTS.md` prints nothing → no history, no tree entry, so this
   is a new uncommitted fleet-root file, not a resurrected tracked one. Its hash `382f28ab…` differs from the lane's
   `mori-shokunin/AGENTS.md` (`f64e332c…`); all 17 nested `*/AGENTS.md` files have distinct hashes (`sha256sum
   */AGENTS.md | cut -c1-16 | sort | uniq -c` → 17 distinct), so it is not a copy of any lane's file. Author
   unattributed [INFERENCE: fleet-level/operator doc].
2. `live_s228.html` first lines: `<!DOCTYPE html>` then `<script id="anubis_version" type="application/json">"v1.26.2"`
   (`:4`). That marker is a bot challenge, not a source. The page also carries a harvested client-address field
   (`X-Real-Ip` inside `anubis_challenge`, `:6`) — value withheld under the privacy bound. The name carries source id
   S228, and `git grep -n S228` over the lane's tracked files returns nothing, so S228 is not yet a landed source row.
   Verdict: fetched bytes of a challenge wall, titled by source id — unusable as evidence and must never be passed.
3. `nama.html` first lines: `<title>Page not found - National Archaeological Museum</title>` (`:6`), body from
   `namuseum.gr` (e.g. `:251`, `:424`). The two case-insensitive `mori` hits are substrings of `Memories 1940` and
   `istoria-toy-moyseioy` URLs, not lane content. Verdict: accidental bytes of a 404 page; no mori/round-29 marker.
4. `tf_bavelas.html` line 1: `<title>Just a moment...</title>` (Cloudflare interstitial). No `mori`, `round 29`,
   `earlyoom` or `systemd` hits. Verdict: bytes of a blocked fetch; no mori/round-29 marker. `git grep -i -e namuseum
   -e bavelas` over tracked files finds no URL attribution in the lane, so the intended target of that fetch is not
   recorded here.
5. `wave-live.cpython-314.pyc` is bytecode of tracked `scripts/hyaku/wave-live.py` (7163 B, 2026-10-21 23:04 -0300),
   i.e. a fleet-orchestrator import, not mori content. It is `??` while its sibling
   `append-closure.cpython-314.pyc` is intent-to-add (§2) — an inconsistent index state, not a round-29 write.

**All five predate round-29 wave 1.** Newest is `AGENTS.md` at 18:12:23Z; the wave-1 spec/dispatch were written at
19:54:46Z/19:55:02Z (`stat .ufo/waves/round-29/wave1-spec.json`, `wave1-dispatch.json`). So zero fleet-root untracked
paths carry a round-29 wave-1 timestamp at snapshot time. Four of them (`AGENTS.md`, `live_s228.html`, `nama.html`,
`tf_bavelas.html`) were already untracked in the previous round's sweep [INFERENCE from carried-state: I did not read
those reports; see §5 blindness note].

## 2. Fleet root — index placeholders (` A` column), NOT untracked and NOT staged content

`git status --porcelain` prints these with a leading space in the index column:
`.ufo/state/kotoba.report-baseline`, `.ufo/state/kotodama.report-baseline`, `.ufo/state/revenger.report-baseline`,
`scripts/hyaku/__pycache__/append-closure.cpython-314.pyc`, `write`.

They are **intent-to-add** entries, not additions: `git ls-files -s` shows the empty blob for all five
(`100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0 <path>`) and `git diff --cached --numstat` prints 0 lines, while
`git diff --numstat -- write` prints `1	0	write`. A path-only diff that treats ` A` as "staged new file" will
mis-classify these.

- `write` — 25 B, `95443b228053f452`, mtime 2026-10-21T22:52:50Z. Sole content is an `agent://<internal-agent-id>` URI
  (id withheld). Shape: a `write` call that lost its `path` and landed in the fleet cwd. Pre-existing by ~21 h; not a
  round-29 artifact.
- `.ufo/state/{kotoba,kotodama}.report-baseline` — mtimes 2026-10-22T19:46:17Z / 19:46:11Z; content is one line,
  `<line-count> <sha256>` (empty-report sentinel `53 e3b0c442…`). Orchestrator state, not mori round-29 prose.
  `revenger.report-baseline` mtime 2026-10-21T17:54:50Z, same shape.
- `append-closure.cpython-314.pyc` — 2026-10-22T08:01:42Z, bytecode of tracked `scripts/hyaku/append-closure.py`.

Also modified (not asked for, listed so the diff is complete): 11 ` M .ufo/state/*.report-baseline` entries and
` M .ufo/watchdog.log` — the fleet watchdog is live, so these move on their own.

## 3. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin` — untracked (19:56Z, re-checked 19:59Z, identical)

Whole-entry list from `git status --porcelain`:

```
 M corpus/lessons/round-28.md          # tracked, dirty (see below)
?? .scratch/
?? .ufo/waves/round-28/w2/MutCountC1Amended.md
?? .ufo/waves/round-28/w2/MutHeadingCheck.md
?? .ufo/waves/round-28/w2/MutTipReceiptCheck.md
?? .ufo/waves/round-28/wave1-run.err
?? .ufo/waves/round-29/w1/
?? .ufo/waves/round-29/wave1-dispatch.json
?? .ufo/waves/round-29/wave1-run.json
?? .ufo/waves/round-29/wave1-spec.json
```

Hashes (`sha256[:16]`), size, mtime UTC:

| path | bytes | sha256[:16] | mtime (UTC) |
|---|---|---|---|
| `.ufo/waves/round-28/w2/MutCountC1Amended.md` | — | `dc118b9fa5974ce0` | 2026-10-22T19:21:22Z |
| `.ufo/waves/round-28/w2/MutHeadingCheck.md` | — | `700b6cd6a1410e1e` | 2026-10-22T19:22:28Z |
| `.ufo/waves/round-28/w2/MutTipReceiptCheck.md` | — | `2379b7961386c47e` | 2026-10-22T19:27:19Z |
| `.ufo/waves/round-28/wave1-run.err` | 0 | `e3b0c44298fc1c14` (empty) | 2026-10-22T17:58:33Z |
| `.ufo/waves/round-29/wave1-dispatch.json` | — | `04088fc891b68241` | 2026-10-22T19:55:02Z |
| `.ufo/waves/round-29/wave1-run.json` | — | `c04c367680c959bd` | 2026-10-22T19:54:46Z |
| `.ufo/waves/round-29/wave1-spec.json` | — | `f283198791b7256e` | 2026-10-22T19:54:46Z |
| `.scratch/` (directory) | 646 MB | dir digest `60f627fefde1d06a` | newest file 2026-10-21T15:30:50Z |

- `.scratch/` — 151 344 files, all under `.scratch/round22` (measure3 72 983, measure2 66 032, measure1 5 645, three
  `trial*-fixtures`), plus `.scratch/SrcGitCommit-git-rev-parse.html` (a saved `git-rev-parse` doc page, 2026-10-21).
  Newest file 2026-10-21T15:30:50Z → last round's scratch, not round-29. Directory digest computed as
  `find .scratch -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum`. Not gitignored (`git check-ignore`
  returns nothing for `.scratch/x`), so it shows as one untracked entry.
- `.ufo/waves/round-29/w1/` — live directory: 1 file at 19:54Z (`swarm-registry.json`, 4482 B, `9bb9060989cc775f`),
  7 files at 19:59Z as siblings landed (`SourceJournalMonotonic.md`, `AxisFreshness.md`, `AxisDepth.md`,
  `AxisCalibration.md`, `RetentionBase.md`, `BuildTipReceipts.md`). No hashes recorded for those six: they are being
  written, so only a name-level diff is meaningful. This report is the eighth.
- The three round-29 top-level JSONs (`wave1-spec`, `wave1-run`, `wave1-dispatch`) are lane orchestration outputs,
  written by the L1 harness 44 s before wave 1 began; they are mori round-29 artifacts by construction.
- Tracked-dirty `corpus/lessons/round-28.md`: sha256[:16] `189c96196ef1f937`, 17 335 B, mtime 2026-10-22T19:55:52Z,
  `git diff --stat` → `1 file changed, 8 insertions(+)`. The hunk is the hygiene-item-5 census correction ("Census at
  round end: ten W04 lines, not nine …") — a wave-1 seat landing it, not a misroot. The lane index was untouched
  (`.git/index` mtime 19:52:08Z).

## 4. One entry moved inside the snapshot window (do not mistake it for a round-29 write)

At 19:55:43Z the lane status read `?? .ufo/waves/round-28/w1/FixR1Runway.md`. At 19:55:52Z `stat` on that path returned
"No such file or directory", and at 19:56Z both plain and `core.untrackedCache=false` status no longer list it.
`.ufo/waves/round-28/w1` now has mtime 2026-10-22T19:55:48Z, i.e. the directory changed **five seconds after** the first
snapshot — so a concurrent seat removed or moved that round-28 wave-1 report between my two calls. `find` at depth 6
(lane) and depth 4 (fleet) finds no `FixR1*` file. Observed: gone at 19:55:48Z, no index change. [INFERENCE: disposed
under round-28 hygiene item 1; disposition receipt not visible to me.]

Consequence for the L1: a path-only after-diff will show this as a deletion; it is a round-28 w1 artifact removed during
wave 1, not a fleet-root misroot and not a round-29 write.

## 5. Answer to the assigned question

- Untracked paths at the fleet root that **name mori or round 29**: none. `AGENTS.md` names the shokunin fleet protocol
  and no lane; `live_s228.html` names a source id, not a lane.
- Untracked paths that are **upstream bytes a mori seat could have fetched**: three — `nama.html` (a 404 page from
  `namuseum.gr`), `tf_bavelas.html` (Cloudflare "Just a moment" interstitial), `live_s228.html` (Anubis challenge wall,
  named by source id S228). All three are failed-fetch artifacts: none may be used as a located quote, and the two
  challenge pages must never be passed (`live_s228.html:6` records a challenge payload).
- Untracked paths that are **fleet tooling residue**: `scripts/hyaku/__pycache__/wave-live.cpython-314.pyc` (+ the
  intent-to-add `append-closure` pyc), plus the intent-to-add `write` misroot from 2026-10-21.
- Snapshot verdict: the fleet root was **clean of round-29 writes** at 19:55:43Z–20:00:18Z. Newest fleet-root untracked
  mtime 18:12:23Z, 1 h 42 min before the wave-1 spec.

## 6. After-the-wave diff recipe (for the L1)

```sh
# fleet root: expect exactly these 5 untracked files, these hashes
git -C /home/vgpnk/Projects/shokunin --no-optional-locks status --porcelain -uall
sha256sum -b AGENTS.md live_s228.html nama.html tf_bavelas.html \
  scripts/hyaku/__pycache__/wave-live.cpython-314.pyc | cut -c1-16
# lane: compare entry list, then the stable hashes of §3; ignore round-29/w1/ growth and live .scratch/
git -C /home/vgpnk/Projects/shokunin/mori-shokunin --no-optional-locks status --porcelain
```

Baseline constant for the fleet root (16-hex prefixes): `382f28ab4e2846a9` AGENTS.md, `918d496cf0c3e6af` live_s228.html,
`bee96464d0fe77f7` nama.html, `9f07c0d0e4afa6ea` tf_bavelas.html, `a0b914e3bb3a8679` wave-live pyc.
Lane baseline constants: `dc118b9fa5974ce0`, `700b6cd6a1410e1e`, `2379b7961386c47e`, `e3b0c44298fc1c14` (empty),
`04088fc891b68241`, `c04c367680c959bd`, `f283198791b7256e`, `.scratch` digest `60f627fefde1d06a` (151 344 files).

## 7. Disclosures and unknowns

- **Index stat-refresh:** my first `git status --porcelain` on the fleet repo ran at 19:55:43Z and the fleet
  `.git/index` carries mtime 2026-10-22 16:55:43.397822631 -0300 = 19:55:43Z, i.e. that call most likely refreshed the
  index stat cache (git's optional lock). No index content changed — `git diff --cached --numstat` is 0 lines and the
  intent-to-add blobs are the empty blob. All later calls used `--no-optional-locks`. This is the only write my seat
  may have caused in the fleet repo, and it wrote no tracked or staged content.
- **Blindness boundary:** one unrestricted `git grep -i` for provenance terms (`namuseum|bavelas|archaeolog`) returned
  four matching lines from `.ufo/waves/round-27/w2/ScoutMisroot.md:71`, `.ufo/waves/round-28/w2/ReviewMisrootSweep.md:34`,
  and two fleet `.ufo/reports/round-{32,54}/*.md` files. I did not open any of those files and quote only their
  `path:line` metadata; no content from them shaped §1–§6 beyond confirming that `tf_bavelas.html` and the other
  fleet-root files were already untracked before this round. I did not open or run `tools/mori-oom-killers.py`.
- **Privacy:** no OMP settings value, session id, session path, uid, pid, unit name, journal message, or `/etc/default`
  value is recorded here. One fetched challenge page contains a client address; the value is withheld and only the key
  name is cited.
- Unknown: who authored `AGENTS.md` at the fleet root (no history, no attribution). Unknown: the exact target of the
  `tf_bavelas.html` and `nama.html` fetches (no URL recorded in any tracked file). Unknown: where `FixR1Runway.md`
  went (removed, not in either repo at depth 4–6).
