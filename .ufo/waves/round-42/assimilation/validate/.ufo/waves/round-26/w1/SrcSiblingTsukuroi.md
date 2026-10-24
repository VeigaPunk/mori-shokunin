# SrcSiblingTsukuroi — tsukuroi's round-25 memory-pressure entry as a mori SOURCES row

Seat: `MoriR26.SrcSiblingTsukuroi` (scribe, leaf member). Wave: mori round 26 / wave 1.
Claim served: **C1 (freshness of the FR10 userspace-OOM-killer entry)**; **C2 (userspace OOM
killer read capability)** is *not* served by this source (see §5).
Deliverable: one ready-to-paste `corpus/SOURCES.md` row for the sibling lane's entry, with tier,
status, Gate line and the facts the round can rest on.

**No lane file was edited by this seat except this report.** `corpus/SOURCES.md` is untouched:
`git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain corpus/SOURCES.md` prints
nothing (measured at tip `5e5e86f`). No `jj` command was run at the fleet root; no lane commit,
push, or unit/package/journal change was made. The sibling repo was read with `git show` /
`git rev-parse` / `git branch -r --contains` only, and its public files were fetched with `curl`.

---

## 1. Commands run and their outcomes (exact, read-only)

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 157ee255:corpus/knowledge/memory-pressure-r25.md
  → 392 lines, 27,828 bytes; sha256 ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin branch -r --contains 157ee255
  → "origin/HEAD -> origin/master" and "origin/master"   (rc=0; 157ee255 IS on the pushed branch)
git -C ... merge-base --is-ancestor 157ee255 origin/master   → rc=0 (ancestor=yes)
git -C ... rev-parse 157ee255:corpus/knowledge/memory-pressure-r25.md
  → be3065ae512f3fefec115a23c0e8fee2cbca9fc4
git -C ... rev-parse origin/master:corpus/knowledge/memory-pressure-r25.md
  → be3065ae512f3fefec115a23c0e8fee2cbca9fc4   (unchanged at the pushed tip)
curl -sS https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md
  → http=200 size=27828; sha256 ecafdcdd…cd25  == local blob bytes (cmp identical)
curl -sS …/157ee255/.ufo/waves/round-25/capture/capture-earlyoom.txt
  → http=200 size=1037; sha256 7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309
curl -sS …/157ee255/.ufo/waves/round-25/capture/capture.txt
  → http=200 size=5607; sha256 e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136
```

The two capture digests are the ones the sibling entry itself records (`memory-pressure-r25.md:1-2`),
so the sibling's receipts **reproduce byte-for-byte from the public remote at the pinned commit**.

Access date for all three fetches: **2026-10-22**. Scratch copies live only under
`/fast/scratch/hyaku/mori-r26/srcsiblingtsukuroi/`.

---

## 2. The drafted row (existing 11-column shape, id left as `S???`)

Header shape read from `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:5-6`
(`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`).
Shape precedent for a *sibling-lane* row read from the fleet's existing ones:
`tsukuroi-shokunin/corpus/SOURCES.md:131` (S125) and `:133` (S127), and
`kake-shokunin/corpus/SOURCES.md:64` (S056) — all `kind = docs`, `tier = B`, scoped as
"not a primary source for any … fact". Mori's own registry currently has **no** sibling-lane row
(`grep -c "Sibling lane" mori-shokunin/corpus/SOURCES.md` → 0), so this would be its first.

Ready to paste (one row, 11 columns, no `|` inside any cell):

```markdown
| S??? | Sibling lane tsukuroi, Memory pressure and systemd-oomd — round 25 entry — https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md (tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md at commit 157ee255, git blob be3065ae512f3fefec115a23c0e8fee2cbca9fc4) | docs | B | The sibling lane's own dated host diagnosis of this host's userspace OOM killers — systemd-oomd inactive and disabled, earlyoom active and enabled, and the `auto` default reading — cited as adjacent evidence and never absorbed as mori's own OS or unit ownership; not a primary source for any systemd, earlyoom or kernel fact, not mori's own host capture, and not a host-wide unit census | commit 157ee255 (on pushed origin/master), git blob be3065ae512f3fefec115a23c0e8fee2cbca9fc4, entry bytes sha256 ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25 (27,828 B), section MP4 (lines 196-232), "How to read this entry" > "Userspace killers" (lines 40-42), "What this entry does not claim" (lines 363-367) and the wave-2 corrections block (line 387); receipts .ufo/waves/round-25/capture/capture.txt sha256 e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136 (lines 73, 76, 79, 112-113, 121-122, 130-131, 139-140) and .ufo/waves/round-25/capture/capture-earlyoom.txt sha256 7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309 (lines 6, 9, 12, 16, 22-31) | A sibling lane's dated, digest-pinned capture can show this host's earlyoom active and enabled while systemd-oomd is inactive and disabled, and can show that systemd-oomd's `auto` default is not monitoring, without mori owning unit, package or OS state — mori cites the diagnosis and keeps the ownership | mined | 2026-10-22 | 90d | corpus/knowledge/userspace-oom-killers-r26.md |
```

### 2.1 Cell-by-cell reasoning for the L1

| cell | value | reason |
|---|---|---|
| id | `S???` | left open by the assignment. Measured maximum in the live registry is `S113` (113 rows, `git show HEAD:corpus/SOURCES.md` sha256 `ed64303a5c8884488b5e4644b314431e9ecf8b4e2a46945aa15b4ab463164f79`), so `S114` is the next free id — but ten other wave-1 source seats are drafting rows, so **the L1 alone assigns ids**; this seat does not claim one. |
| source | title — public raw URL at the pinned commit, plus the repo path, commit and git blob | CORPUS.md allows "canonical URL or DOI (a repo path or command for `own-work`)". The sibling-lane precedent (S125/S127/S056) names the repo path; this row adds the canonical URL because the Gate requires a URL with a fetched-bytes digest. The URL is commit-pinned, therefore immutable and re-fetchable. |
| kind | `docs` | matches every existing sibling-lane row in the fleet (tsukuroi S125/S127, kake S056). `own-work` would be wrong: the artifact is the **sibling** lane's work, not mori's re-runnable output. |
| tier | `B` | scoped to the cell's own subject: the sibling's dated host diagnosis is a strong secondary for mori's adjacency question and is **not** primary for any systemd/earlyoom/kernel fact. Tier is scoped to `scope` (CORPUS.md), so B here does not demote the primary rows other seats open this round. |
| scope | the sibling's diagnosis of the two userspace killers, the `auto` reading, adjacency-not-absorption, and four explicit exclusions | prevents the row from being widened into mori's own host state, into a host-wide unit census (the sibling read four units only), or into a systemd semantic authority (the sibling sources that to its own S121/S122/S123). |
| anchor | commit + git blob + entry sha256 + section/line numbers + both capture receipts with their own digests and line numbers | every element is a measured location or digest; CORPUS.md rule 1 requires the location that grounds `teaches`. |
| teaches | one grounded learner benefit: a dated, digest-pinned sibling capture can show earlyoom active/enabled while oomd is inactive/disabled, and mori can cite that diagnosis without owning OS/unit state | phrased as a reading benefit, not as a new domain fact. It is the sentence the r26 entry's adjacency note needs. |
| status / used-by | `mined`, `corpus/knowledge/userspace-oom-killers-r26.md` | see §2.2 — the E11 landing-order condition. |
| opened | `2026-10-22` | the date this seat fetched and quoted the bytes. |
| recheck | `90d` | the row carries a **dated host diagnosis**; it goes stale like mori's own dated receipt row S034 (also `90d`). (The sibling-row precedent S125/S127/S056 uses `on-release` for a pinned commit; `90d` is chosen here because the content is host state, not a pinned API.) Flip to `on-release` if the L1 prefers the sibling-row convention. |
| used-by | `corpus/knowledge/userspace-oom-killers-r26.md` | the contract's C1 superseding entry. That file does **not** exist yet on disk (measured: `ls corpus/knowledge/` lists no `userspace-oom-killers-r26.md`), which is why §2.2 matters. |

### 2.2 Status and flip conditions (measured, not assumed)

- **`mined` requires the citing path to exist.** CORPUS.md's census prints `missing: <path>` for a
  `mined` row whose `used-by` path is absent (`used-by` existence check, CORPUS.md:145-148), which
  the round-16 source census recorded as validator error **E11**.
- **Landing-order condition:** land this row `mined` **in the same commit** as
  `corpus/knowledge/userspace-oom-killers-r26.md` (the seat that drafts it is
  `MoriR26.DraftEntryR26`), or in any commit after it. If the row would land while that entry is
  still absent, the row must land `queued` with `used-by = —` and be flipped to
  `mined` / `corpus/knowledge/userspace-oom-killers-r26.md` when the entry lands (CORPUS.md rule 2:
  only `status`, `recheck` and `used-by` change in place, old→new logged in the round lesson).
- **Flip to `rejected` if** the r26 entry does not cite this row at all, or if the sibling's
  host-state facts are superseded on the host (earlyoom stopped/disabled, oomd enabled) — the row
  would then be a stale adjacency note rather than a cited source. A rejected row must read
  `REJECTED: <reason>; flip: <what would change the verdict>` (CORPUS.md rule for `teaches`).
- **Alternative the L1 may prefer (honest, and cheaper):** do not add this row at all. Mori's
  precedent for sibling material is an **inline path citation inside the knowledge entry**, not a
  registry row: `corpus/knowledge/userspace-oom-killers-r12.md` cites
  `tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md:344–346,353–367` in prose, and
  `corpus/knowledge/kill-classes-by-message-id-r12.md:8` and
  `corpus/knowledge/kernel-oom-line-attribution-r12.md:8` do the same. The row's added value is
  precisely that it makes the sibling citation **auditable** (URL, byte digest, section lines,
  three located quotes) instead of a bare path — that is the reason to spend a row on it.

### 2.3 Draft `## Gate` block for `corpus/lessons/round-26.md`

```markdown
| S??? | Sibling lane tsukuroi, Memory pressure and systemd-oomd (round 25 entry) — https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md ; opened 2026-10-22; 27,828 B, sha256 ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25; commit 157ee255, git blob be3065ae512f3fefec115a23c0e8fee2cbca9fc4 | entry line 41 (verbatim, 12 words): "read-only capture shows `earlyoom.service` active and enabled on this host." / entry lines 200-202 joined with single spaces (18 words): "`auto` is the default and means systemd-oomd will not actively use that cgroup's data for monitoring and detection" / entry line 204 (verbatim, 9 words): "On this host systemd-oomd is inactive and disabled" | B/mined for the sibling lane's dated, digest-pinned host diagnosis only. The entry itself scopes its `auto` reading to the four captured units and its earlyoom note to a supplementary read-only capture marked "not a C2 counting input"; it is not evidence for any systemd semantic, any earlyoom message grammar, any action count, or any host-wide unit census, and mori cites it without absorbing OS or unit ownership. |
```

Quote verification (all three re-derived from the fetched bytes):

| quote | lines | check | words |
|---|---|---|---|
| "read-only capture shows `earlyoom.service` active and enabled on this host." | 41 | strict substring of line 41 | 12 |
| "`auto` is the default and means systemd-oomd will not actively use that cgroup's data for monitoring and detection" | 200-202 | strict substring of the space-joined span (the entry's own quote convention, `memory-pressure-r25.md:20-23`) | 18 |
| "On this host systemd-oomd is inactive and disabled" | 204 | strict substring of line 204 | 9 |

All three are ≤25 words and verbatim. No journal `MESSAGE` text, no uid, no command line, and no
`--avoid`/`--prefer` expression or `/etc/default/earlyoom` value is quoted anywhere in this report
or in the row (the sibling's supplementary capture contains none of those; its `ExecStart` line was
deliberately **not** copied).

---

## 3. The facts the round can rest on (each with its line number)

All entry line numbers are in `tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md` at commit
`157ee255` (392 lines, blob `be3065ae512f3fefec115a23c0e8fee2cbca9fc4`).

| id | fact | line(s) |
|---|---|---|
| F1 | The sibling's frozen round-25 capture **never read earlyoom**; the earlyoom state comes from a separate supplementary read-only capture. | 40-41 |
| F2 | The sibling's supplementary capture shows `earlyoom.service` **active** and **enabled** on this host. | 41 (receipt: `capture-earlyoom.txt` lines 6, 9) |
| F3 | Installed earlyoom package version `earlyoom 1.9.0-1`; unit `ActiveEnterTimestamp=Thu 2026-10-22 04:55:44 -03`. | receipt `capture-earlyoom.txt` lines 12, 16 |
| F4 | The sibling states explicitly that it does **not** claim that nothing watches memory before the kernel, and repeats that earlyoom is active and enabled (supplementary capture, "context only"). | 363-365 |
| F5 | `ManagedOOMMemoryPressure=` / `ManagedOOMSwap=` semantics: `auto` is the default and means systemd-oomd will not actively use that cgroup's data for monitoring and detection; an `auto` unit becomes a kill candidate only when an ancestor cgroup is set to `kill`. | 200-203 (semantic sourced by the sibling to its own S121) |
| F6 | On this host **systemd-oomd.service is inactive and disabled** (unit-level read). | 204 (receipt `capture.txt` line 73 `inactive`; lines 76 and 79 `disabled` for the service and the socket) |
| F7 | All **four captured units** (`user@1000.service`, `user-1000.slice`, `user.slice`, `-.slice`) carry `auto` on both properties; the ancestor chain up to the root slice is `auto` and nothing in it is monitored. | 205-207 (receipt `capture.txt` lines 112-113, 121-122, 130-131, 139-140) |
| F8 | The sibling's verdict is **scoped**, not verified: a unit outside those four was not read, so no host-wide statement is made. | 209-211 and 366-367 |
| F9 | `OOMRules=` is **empty** on the four read units (supplementary capture, context only). | line 387 (receipt `capture-earlyoom.txt` lines 22, 25, 28, 31) |
| F10 | The sibling does not attribute pressure to any workload, session or fleet wave; that correlation is mori's under `PROVINCE.md` row ADJ-04. | 368-369 |
| F11 | Host identity of the sibling's capture: kernel `7.2.11-arch1-1`, systemd `262 (262-1-arch)`, capture window `2026-10-22T10:06:23Z`–`10:06:33Z`. | line 2 (receipt `capture.txt` lines 3, 6, 9) |

---

## 4. Which facts are tsukuroi-owned host diagnosis that mori must cite and not absorb

mori's `PROVINCE.md:8-9` refuses "OS package, systemd unit, driver/firmware and boot state
(→ tsukuroi)"; `PROVINCE.md` Adjacent row `tsukuroi` records that host diagnosis as the sibling's.

| fact | owner | mori's treatment |
|---|---|---|
| F2, F3 — earlyoom active/enabled, package version, unit activation timestamp | **tsukuroi** (its read-only capture, `capture-earlyoom.txt`) | **Cite, do not absorb.** Mori's C1 statement rests on mori's own round-26 host capture (the `MoriR26.HostCapture` seat), not on this sibling receipt. The sibling row is corroboration and provenance only. |
| F6 — systemd-oomd inactive and disabled | **tsukuroi** (unit state) | **Cite, do not absorb.** Unit state is tsukuroi's; mori reports the absence of readable evidence and never owns the unit's state or its enablement. |
| F7, F9 — four captured units `auto`, `OOMRules=` empty | **tsukuroi** (per-unit configuration reading) | **Cite, do not absorb, and do not generalize.** The sibling read four units; mori must not restate this as a host-wide unit census, and must not repeat it as mori's own configuration finding. |
| F5 — `auto` is the default and is not monitored | **Not tsukuroi's to give mori.** The sibling itself sources this to its own S121 (`systemd v262 man/systemd.resource-control.xml`). | **Do not source from the sibling.** Mori must hold this semantic from the **primary** v262 rows other seats open this round (`MoriR26.SrcResourceControlV262`, `MoriR26.SrcOomdUtilV262`). This sibling row is at most a secondary pointer, never the authority for the semantic. |
| F8 — the scoped limit | shared discipline | Mori must carry the same limit in its own entry: four units read ⇒ no host-wide claim. |
| F10 — no pressure attribution to fleet/wave | mori's own scope | Mori may and must do this correlation itself (`PROVINCE.md` ADJ-04); nothing to absorb. |
| The sibling's **actions** (enable a unit, set `kill`, enable systemd-oomd) | **operator** (host mutation) | Out of scope for mori: detection and report only, never remediation. |

---

## 5. C2 grammar: this source contributes **nothing** to it

Measured on the fetched entry bytes (`python3` substring counts over the 27,828-byte file):

```
'sending SIGTERM'      0      'escalating to SIGKILL' 0      'low memory!' 0
'dryrun'               0      'earlyoom 1.9.0'        0      'v1.9.0'      0
'10.00'                0      '5.00'                 0      'kill failed' 0
```

The sibling entry contains **no earlyoom message grammar, no thresholds and no action counts**; it
states that its captures never read earlyoom's own output (line 40). C2's grammar (the contract's
`main.c` / `kill.c` message shapes at tag v1.9.0) must come from the primary earlyoom rows opened
by the other wave-1 source seats, never from this sibling row. The sibling contributes to C2 only
as **host context** (which killer is actually running), which the tool's own live reads supply.

---

## 6. Flags against the round-26 contract

**No contradiction on host state.** The sibling's capture and the contract agree on every point the
contract states (`contract.md`, Frontier area): earlyoom **1.9.0** (package `earlyoom 1.9.0-1`),
**active and enabled**, `ActiveEnterTimestamp=Thu 2026-10-22 04:55:44 -03` (identical to the
contract's "since 2026-10-22 04:55:44 -03"); `systemd-oomd.service` **inactive and disabled**;
host **systemd 262**. The sibling's frozen capture therefore **corroborates** C1 rather than
contradicting it.

**F-1 — the sibling's own MP4 sentence contains a clause the sibling withdrew.** Entry line 203
reads "systemd-oomd monitors only cgroups whose units carry `kill`", and the entry's wave-2
corrections (line 387) withdraw it as too strong for systemd v262: units with `OOMRules=` are also
monitored (its S121 lines 1633-1644; S123 lines 115-116), and the host conclusion stands only
because `OOMRules=` is empty on the four read units. **Consequence for mori:** the row's `teaches`
and the r26 entry must use the corrected form (`auto` is not monitored; `kill` on the unit or an
ancestor makes a candidate; `OOMRules=` units are also monitored in v262). Any mori text repeating
"only cgroups whose units carry `kill`" would import a withdrawn claim. This is why the Gate
quote for the `auto` semantic stops at line 202 and does not quote line 203.

**F-2 — internal tension in the sibling entry about `OOMRules=`.** Lines 366-367 say the
"`OOMRules=` channel of systemd v262 was not read by the capture", while line 387 and the
supplementary capture (lines 22, 25, 28, 31) show it **was** read — empty — for the four units.
The "not read" sentence describes the *frozen* capture only. Mori must not restate "OOMRules= was
not read" as a current host fact, and must not restate "OOMRules= is empty" as mori's own finding
(it is tsukuroi's supplementary read, context only).

**F-3 — scope: four units, not the host.** F7/F8 are scoped to `user@1000.service`,
`user-1000.slice`, `user.slice`, `-.slice`. C1 and C2 concern the two killer *services*, not unit
configuration; the r26 entry must not carry the four-unit result forward as a host-wide statement.

**F-4 — the sibling's `auto` semantic is not mori's authority.** See §4; mori holds it from the
primary v262 rows, so the round does not gain a second, weaker path to a systemd semantic.

**F-5 — the sibling's captures are explicitly not counting inputs.** `capture-earlyoom.txt` line 1
and the entry's line 1 both label the supplementary capture "context only and not a counting
input". Mori's C2 tool must read the live host itself; no mori count may be sourced from these
receipts.

**F-6 — no r26 entry exists yet.** `corpus/knowledge/userspace-oom-killers-r26.md` is absent from
the tree (measured). The contract's C1 after-state ("a superseding entry … exists whose `source:`
line cites at least one `corpus/SOURCES.md` row opened in round 26") is satisfied only when that
entry lands; this row is a candidate to be the cited round-26 row, and it can land `mined` only
with that entry (see §2.2). Other round-26 rows (earlyoom `main.c`/`kill.c`/README/manpage/
meminfo/unit, systemd v262 `resource-control`/`oomd-util`, journal JSON) are also candidates.

---

## 7. Gates, touched surfaces, out-of-scope

- **Gates run (exercised):** the sibling blob read, the pushed-branch containment check, the
  ancestor check, three public `curl` fetches with digests, the byte-identity comparison between
  the fetched entry and the local blob, the per-line quote re-derivation, the `grep` census of the
  registry for existing sibling rows, and the absence checks for `corpus/knowledge/userspace-oom-killers-r26.md`.
- **Gates not run (out of this seat's scope):** the round-26 C1 counting command, the tool's
  `--selftest`, the sources census/validator (the L1 runs them at landing), and any wave-2 review.
- **Touched surfaces:** exactly one file — `.ufo/waves/round-26/w1/SrcSiblingTsukuroi.md` (this
  report). No lane corpus file, no `corpus/SOURCES.md`, no lesson, no tool, no unit, no package,
  no journal, no sibling repo was modified. Scratch only under
  `/fast/scratch/hyaku/mori-r26/srcsiblingtsukuroi/`.
- **Out of scope / not done by this seat:** the r26 knowledge entry and its `source:` line
  (seat `MoriR26.DraftEntryR26`); the SOURCES id assignment (L1); the primary earlyoom and systemd
  v262 rows (other source seats); the tool and its cases (executor seats); the C1/C2 verification
  (L1).
- **Tools:** `curl 8.23.0`, `git 2.56.0`, `python3 3.14.8` — all already present on the host.
  **No tool was installed, upgraded or removed by this seat**, so there is nothing to record under
  the tooling directive; **no pacman transaction was attempted** (host-wide pacman transactions are
  paused).

**Report: `.ufo/waves/round-26/w1/SrcSiblingTsukuroi.md`**
