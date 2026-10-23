# RevAppendDebt — wave 2, round 36 (falsify + verify)

Item attacked: **Append-only debt closure count** (QUALITY 102 debt; gate registered by QUALITY
104). Seat: `mori-r36-w2-RevAppendDebt-23`. Lane read-only; scratch under
`/fast/scratch/hyaku/mori-r36/mori-r36-w2-RevAppendDebt-23/`. No tools installed (no installs to
record).

Target: the gate's `ids` list at the landed tip `bf0df77fee4b6ef54a90aea09335c7617f125151` must be
exactly the 18 carried-debt ids (15 pre-round-34 ids + S069 + r35-era S182/S193 pair, per QUALITY
104's count), and each of the 18 must have exactly one superseding row at the tip whose `teaches`
opens `supersedes S<id> —`. FAIL on count mismatch.

## Evidence

### 1. One command over committed bytes — the registered gate (QUALITY 104's check)

Command (cwd = lane repo):

```
python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097f7ab2b471b4593ed2019c980b1368c68
```

Observed output (exit 0):

```
changed S041 superseded_by=S206
changed S044 superseded_by=S207
changed S051 superseded_by=S208
changed S062 superseded_by=S209
changed S064 superseded_by=S210
changed S069 superseded_by=S073
changed S179 superseded_by=S211
changed S180 superseded_by=S212
changed S181 superseded_by=S213
changed S182 superseded_by=S201
changed S183 superseded_by=S214
changed S184 superseded_by=S215
changed S185 superseded_by=S216
changed S186 superseded_by=S217
changed S188 superseded_by=S218
changed S189 superseded_by=S219
changed S190 superseded_by=S220
changed S193 superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
```

### 2. Count and set checks (asserted programmatically)

- `violations=18`, `len(ids)=18`, no duplicates.
- Gate ids set == expected set exactly: `{S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,
  S183,S184,S185,S186,S188,S189,S190,S193}` — 15 pre-round-34 ids
  (S041,S044,S051,S062,S064,S179,S180,S181,S183,S184,S185,S186,S188,S189,S190) + S069 + S182 + S193.
  No extra id, no missing id.
- `deleted=[]`, `round_changed=[]`, exit 0.

### 3. Per-id superseding-row uniqueness at the tip (independent parse of committed bytes)

Tip blob `bf0df77:corpus/SOURCES.md` (sha256
`e40f9cb2eed2bac873f24bf8bf6e45d9c12db488375afc09f29cbd25a2f9d7b1`) parsed by header position; 220
registry rows, 34 rows whose `teaches` opens `supersedes S###`. For each of the 18 gate ids:

| id | superseder rows at tip | teaches opens `supersedes S<id> —` |
|---|---|---|
| S041 | S206 (1) | yes |
| S044 | S207 (1) | yes |
| S051 | S208 (1) | yes |
| S062 | S209 (1) | yes |
| S064 | S210 (1) | yes |
| S069 | S073 (1) | yes |
| S179 | S211 (1) | yes |
| S180 | S212 (1) | yes |
| S181 | S213 (1) | yes |
| S182 | S201 (1) | yes |
| S183 | S214 (1) | yes |
| S184 | S215 (1) | yes |
| S185 | S216 (1) | yes |
| S186 | S217 (1) | yes |
| S188 | S218 (1) | yes |
| S189 | S219 (1) | yes |
| S190 | S220 (1) | yes |
| S193 | S202 (1) | yes |

Exactly one superseding row per id; every superseder `teaches` cell opens `supersedes S<id> —`
(with the em dash immediately after the id; zero format deviations). Superseder rows match the
gate's `superseded_by=` disposition for all 18 ids.

### 4. No other id in the gate's ids list

The summary `ids=[...]` contains exactly the 18 ids above and nothing else (set equality proven,
no duplicates). Informational: 16 further superseder targets exist at tip (S067,S070,S071,S083,
S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140) — these are older corrections whose
targets are not in the gate's `ids` (their rows were not edited in place), consistent with the gate's
definition and not part of this debt's count.

## Findings

None. QUALITY 102's carried debt is closed with the expected count: 18 ids, each discharged by exactly
one superseding row at the tip whose `teaches` opens `supersedes S<id> —`, no extra ids, no
deletions, no round_changed ids.

## VERDICT: PASS

(no defect found; FAIL would require a count mismatch, an id without exactly one superseding row, or
an extra id in the gate's list — none observed.)
