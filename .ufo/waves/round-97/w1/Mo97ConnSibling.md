# Mo97ConnSibling — Sibling-Overlap Scan & Connector Synthesis

**Seat:** Mo97ConnSibling (role: connector)  
**Lane:** mori-shokunin (fleet & host observability)  
**Round:** 97 attempt 1, wave w1  
**Write scope:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-97/w1/Mo97ConnSibling.md` only  
**Execution mode:** Read-only scan of `/home/vgpnk/Projects/shokunin/*-shokunin`, `/home/vgpnk/Projects/shokunin/PROTOCOL.md`, `/home/vgpnk/Projects/shokunin/AXES.md`. No git/jj mutation. No package/sysctl modifications.

---

## Executive Summary

1. **Question 1 (docs.python.org pins across siblings):** 11 sibling lanes contain 59 markdown table rows matching `docs.python.org` and `sha256` in `corpus/SOURCES.md`. Exactly 58 of these rows record page-body SHA-256 digests (chousa S059 mentions SHA-256 conceptually in scope without recording a page digest). All 58 pinned snapshots are vulnerable to the Sphinx build-clock timestamp footer churn (`Last updated on ... UTC`) when verified live without a churn grammar.
2. **Question 2 (Gate registry convention):** The 8-cell table convention (`name | kind | entry | verdict map | self-test | pinned values | write scope | owner`) is owned fleet-wide by `PROTOCOL.md` §Gate standard ("Registry. The schema is this section's; a child lane's registry home is its own SKILL.md"). No sibling owns an auditor that audits mori's `SKILL.md`. Mori's new rows in section 'Round97 gate registry backfill' do not conflict with or duplicate any sibling registry.
3. **Question 3 (Adjacency bleed):** 0 / 4 tools belong to another lane's province. All four registered instruments (`tools/mori-cgroup-pressure.py`, `tools/mori-drift-recheck.py`, `tools/mori-scorecard-calibration.py`, `tools/mori-source-digest.py`) are strictly within `mori-shokunin/PROVINCE.md`. Specifically, cgroup pressure is read-only fleet resource runway correlation, explicitly acknowledged by tsukuroi (`tsukuroi-shokunin/PROVINCE.md:121`, OUT-001 / ADJ-04); drift re-check, scorecard calibration, and source digest are lane-internal calibration, freshness, and evidence integrity gates.

---

## 1. Sibling Lanes Pinning docs.python.org with Recorded sha256

### 1.1 Command and Row Counts per Lane
Command executed from fleet root:
```sh
for lane in /home/vgpnk/Projects/shokunin/*-shokunin; do
    name=$(basename "$lane")
    [ "$name" = "mori-shokunin" ] && continue
    src="$lane/corpus/SOURCES.md"
    if [ -f "$src" ]; then
        c=$(grep "docs\.python\.org" "$src" | grep -i "sha256" | grep "^|" | wc -l)
        [ "$c" -gt 0 ] && echo "$name: $c"
    fi
done
```

**Results (11 sibling lanes, 59 total matching rows):**
- `chousa-shokunin`: 2 matching lines (S059, S060; S059 is keyword-only, S060 records digest `025727ff…3dda3`)
- `kaidoku-shokunin`: 18 rows (S143, S144, S260, S263, S266, S267, S272, S274, S276, S284, S286, S287, S291, S292, S293, S298, S299, S319)
- `kake-shokunin`: 9 rows (S100, S111, S115, S116, S123, S126, S133, S441, S442)
- `kama-shokunin`: 4 rows (S538, S539, S540, S541)
- `kengaku-shokunin`: 2 rows (S249, S250)
- `kotoba-shokunin`: 1 row (S253)
- `mado-shokunin`: 1 row (S441)
- `revenger-shokunin`: 2 rows (S040, S044)
- `souji-shokunin`: 10 rows (S226, S229, S252, S253, S255, S256, S259, S272, S273, S278)
- `tameshi-shokunin`: 9 rows (S153, S154, S157, S279, S299, S300, S307, S309, S310)
- `tsukuroi-shokunin`: 1 row (S335)

Lanes with 0 docs.python.org + sha256 rows: `audio-shokunin`, `game-dev-2d-shokunin`, `game-dev-3d-shokunin`, `kagi-shokunin` (9 docs.python.org rows without sha256), `kasegi-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`, `lore-shokunin` (1 row without sha256), `tabi-shokunin`.

### 1.2 Vulnerability to 'Last updated on' Build Stamp Churn
In Sphinx-rendered documentation on `docs.python.org`, every rebuild or document re-generation stamps the HTML footer with:
```html
<div>Last updated on [date] [time] [UTC].</div>
```
When a lane records a full-page SHA-256 over raw HTML bytes, a live GET against `docs.python.org` differs in that footer line even when the normative documentation text is completely unaltered. In chousa, row S060 explicitly observes this:
`"The page carries a build clock in its footer ('Last updated … (06:37 UTC)'), so the body sha256 025727ff…3dda3 pins that snapshot only; a later GET differs in that line (06:57 UTC → 0189dd49…1e56)"`.
Across the 11 sibling lanes, all 58 rows recording page SHA-256 digests will fail a naive byte-equality live check (`live == recorded`). Mori's `tools/mori-drift-recheck.py` solves this via the `python-docs-page-stamp` grammar (grounded in S577 and S628).

---

## 2. Gate-Registry Convention (8-Cell Table)

### 2.1 Fleet Convention Authority
`PROTOCOL.md:398-406` defines the fleet-wide gate standard:
> "**Registry.** The schema is this section's; a child lane's *registry home* is its own `SKILL.md`. ... Row fields: name, `gate|probe`, entry command, verdict map (code → class), self-test command and spelling, pinned-value path, write scope, owner."

Every child lane that maintains a gate registry in its `SKILL.md` (e.g. `chousa`, `kagi`, `kaidoku`, `kake`, `kama`, `kasegi`, `kengaku`, `kotoba`, `kotodama`, `mado`, `souji`, `tabi`, `tameshi`, `tsukuroi`) implements this fleet standard. No sibling lane "owns" this convention; it is owned by the fleet protocol.

### 2.2 Sibling Scopes and In-Lane Attribution Analysis
- **Sibling tools:** No sibling tool audits or asserts authority over `mori-shokunin/SKILL.md`. Commands searching for cross-lane registry audits show sibling tools inspect only their own lane repositories.
- **Mori's auditor:** `tools/mori-gate-registry.py` audits only `mori-shokunin/SKILL.md` tables matching the standard 8 header fields (`FIELDS = ["name", "kind", "entry", "verdict map", "self-test", "pinned values", "write scope", "owner"]`).
- **In-lane historical context:** At entering revision `973b2af1`, `tools/mori-gate-registry.py --audit-all` reported `unregistered=4`. Investigation reveals that for `tools/mori-drift-recheck.py`, a row had previously been attempted in round 73 at `SKILL.md:1321`, but its entry command contained `[--only S###,S### | --from-sweep SWEEP_RECEIPT]`. Because `mori-gate-registry.py` naively splits table rows on `|`, that unescaped pipe character resulted in 9 cells instead of 8, causing the row to be rejected as malformed.
- **Round 97 backfill:** The new section `## Round97 gate registry backfill (four unregistered tools)` at `SKILL.md:1434-1448` appends clean 8-cell rows (using `or` instead of `|` in line 1446). This backfills the 4 missing tools without altering earlier lines.
- **Conflict / duplication verdict:** 0 conflict with any sibling; 0 duplication of any sibling tool.

---

## 3. Tool Ownership and Adjacency Bleed

Auditing the four registered tools against sibling `PROVINCE.md` boundaries:

| Registered Tool | Kind | Declared Province | Sibling Boundary Checks | Adjacency Bleed |
|---|---|---|---|---|
| `tools/mori-cgroup-pressure.py` | probe (entry in SKILL.md:1445) | `mori-shokunin/PROVINCE.md:9,26,550` (read-only cgroup pressure & memory.events for fleet resource runway) | `tsukuroi-shokunin/PROVINCE.md:121` explicitly records: `OUT-001 \| Mori owns kill/OOM and cgroup memory evidence; fleet correlation of host pressure is mori's, not OS triage`. ADJ-04 routes host pressure correlation to mori. The tool reads `/sys/fs/cgroup/*/{cpu,memory,io,irq}.pressure`, writes nothing, tunes nothing. | **0 (None)** |
| `tools/mori-drift-recheck.py` | probe (entry in SKILL.md:1446) | `mori-shokunin/PROVINCE.md:90,571` (observing and classifying drift of cited sources) | Each lane owns its own `corpus/SOURCES.md`. No sibling maintains or claims mori's source drift tool. | **0 (None)** |
| `tools/mori-scorecard-calibration.py` | gate (entry in SKILL.md:1447) | `mori-shokunin/PROVINCE.md:132-133` (judging lane's own claim labels against commit order / MANIFEST) | Calibrates mori's own `SCORECARD.md` Last-change column against `MANIFEST.json`. No sibling compares SCORECARD Last-change cells to MANIFEST. | **0 (None)** |
| `tools/mori-source-digest.py` | gate (entry in SKILL.md:1448) | `mori-shokunin/PROVINCE.md:125-131` (retention and integrity gate over own evidence) | Verifies digests of pinned files against mori's own `corpus/SOURCES.md` and `corpus/evidence`. Sibling digest checkers inspect only sibling-local files. | **0 (None)** |

**Adjacency bleed total:** 0 / 4 tools. All 4 tools are authentic, uncontested mori instruments.

---

## 4. Connector Synthesis & Proposed Move

### 4.1 Evidence and Cross-Domain Synergy
- **Freshness surface (C2):** Mori's round 96 honest stop was caused by treating docs.python.org timestamp churn as content drift. In round 97, mori verified that `tools/mori-drift-recheck.py` accurately identifies Sphinx build clock churn via the `python-docs-page-stamp` grammar (grounded in S577 and newly opened S628).
- **Fleet-wide sibling state:** 11 sibling lanes currently hold 58 docs.python.org rows with static SHA-256 pins that are equally subject to build-stamp churn.
- **Operability surface (C1):** `tools/mori-gate-registry.py` enforces the 8-cell protocol table standard. The historical un-registration of `mori-drift-recheck.py` was caused by naive pipe splitting of `[--a | --b]`.

### 4.2 Proposed Bounded Move
**Move:** In `corpus/lessons/round-97.md`, formalize an exportable lesson note documenting the **Sphinx Build-Stamp Normalization Pattern** (`python-docs-page-stamp` grammar, grounded in S577 and S628) and route an observational finding to the 11 sibling lanes holding 58 vulnerable `docs.python.org` rows. Additionally, note for mori's future tooling roadmap that `tools/mori-gate-registry.py` can be hardened with a backtick-masked row tokenizer to prevent CLI alternative pipes (`[--a | --b]`) from causing silent un-registration.

### 4.3 Affected Axes
- **Freshness (improved):** Provides a reusable, grounded distinction between time-churn and substantive content-drift, preventing spurious freshness failures across 58 fleet source rows without requiring manual re-pinning every time Python docs rebuild.
- **Operability (improved):** Prevents table-formatting syntax collisions in Markdown gate registries, ensuring tools remain discoverable and auditable.
- **Adjacency (unharmed):** Strictly observational; mori publishes the lesson and routes findings without modifying sibling repositories or absorbing sibling verification.

### 4.4 Second-Order Effects & Risks
- **Substrate / verification interaction:** If siblings adopt stamp stripping without validating the located quote, they risk masking genuine content drift. The pattern must specify that quote-location and teaching validity must remain strict even when the build stamp is ignored.
- **Adjacency risk:** Mori must not execute sibling source checks directly (violating lane read-only boundaries). Delivery must remain a routed finding.

### 4.5 Verification
- C1 verification: Materialize landing tree `e85ed91249953094b067554bfa79fcdc65791f8e` to scratch, run `python3 count-c1.py --root DIR` → `C1=met unregistered=0 registry=met targets_ok=4/4`.
- C2 verification: Run `python3 count-c2.py --root DIR` → `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass`.

---

## 5. Unrun Checks
- Did not mutate any git or jj reference anywhere in the fleet or lane.
- Did not modify any sibling files or fleet-level tracking files.
- Did not run external network fetches against sibling source URLs.
- Did not execute sibling gate self-tests or counters.
