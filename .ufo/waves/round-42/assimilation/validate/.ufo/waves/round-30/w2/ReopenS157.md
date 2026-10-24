# ReopenS157 — A1 residual F3, S157 (unit.c admit chain)

**Verdict: agree.** The S157 admit chain is intact: fresh fetch hash equals the excerpt header and the Gate admit line, all 17 excerpt rows are byte-identical to upstream v262 line n, both located quotes reconstruct verbatim and their `(N words)` labels equal `wc -w`, and the SOURCES `teaches` sentence is supported by the quoted block (one clause via excerpt line 2766, inside the row anchor but outside the two admit quote spans — noted, not a defect).

## 1. Fresh fetch

Command and output (`/fast/scratch/hyaku/mori-r30-w2/ReopenS157/`):

```
date -u +%Y-%m-%dT%H:%M:%SZ            -> 2026-10-22T22:02:42Z
curl -sS -o unit.c -w '%{http_code} %{url_effective} %{size_download}' \
  https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c
  -> http_status=200  url_effective=https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c  size=263849
sha256sum unit.c -> 47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7  unit.c
wc -l unit.c -> 7294
```

- Access time recorded **before** the request: 2026-10-22T22:02:42Z; HTTP **200**; 263 849 B; 7 294 lines.
- No bot challenge encountered (plain curl on a public URL).

## 2. Hash comparison

| carried by | value |
|---|---|
| fresh fetch (this seat) | `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7` |
| excerpt header, `corpus/evidence/sources-r30/S157.txt:3` | `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7` |
| Gate admit line, `corpus/lessons/round-30.md:116` | `47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7` |

Programmatic string compare: `excerpt sha == lesson sha: True`, `excerpt sha == fresh sha: True`. Access-time strings also agree (`accessed: 2026-10-22T21:12:02Z` in the excerpt; `| 2026-10-22T21:12:02Z |` in the admit line) — the earlier author access recorded there is consistent with the identical bytes.

## 3. Excerpt line-by-line diff

Every `<n><TAB><text>` row of `corpus/evidence/sources-r30/S157.txt` (rows 2763–2779, 17 rows, contiguous, matching the `lines: 2763-2779` header) was compared to line n of the fetched bytes:

```
excerpt quote lines: 17
mismatches: 0
```

Observed block in the fetched bytes (lines 2763–2779):

```
2763 (blank)
2764         /* Update timestamps for state changes */
2765         if (!MANAGER_IS_RELOADING(m)) {
2766                 dual_timestamp_now(&u->state_change_timestamp);
2767 (blank)
2768                 if (UNIT_IS_INACTIVE_OR_FAILED(os) && !UNIT_IS_INACTIVE_OR_FAILED(ns))
2769                         u->inactive_exit_timestamp = u->state_change_timestamp;
2770                 else if (!UNIT_IS_INACTIVE_OR_FAILED(os) && UNIT_IS_INACTIVE_OR_FAILED(ns))
2771                         u->inactive_enter_timestamp = u->state_change_timestamp;
2772 (blank)
2773                 if (!UNIT_IS_ACTIVE_OR_RELOADING(os) && UNIT_IS_ACTIVE_OR_RELOADING(ns))
2774                         u->active_enter_timestamp = u->state_change_timestamp;
2775                 else if (UNIT_IS_ACTIVE_OR_RELOADING(os) && !UNIT_IS_ACTIVE_OR_RELOADING(ns))
2776                         u->active_exit_timestamp = u->state_change_timestamp;
2777         }
2778 (blank)
2779         /* Keep track of failed units */
```

Indentation, blank rows and the surrounding inactive-stamp lines are reproduced exactly; no off-by-one and no reflow.

## 4. Admit Gate line quotes (round-30.md:116)

Both located quotes were rebuilt from fetched lines (`strip`, join with one space, collapse whitespace) and from the excerpt rows alone, then compared to the quoted text and to `wc -w`:

| located quote | rebuilt == quote | label | `wc -w` | label ok |
|---|---|---|---|---|
| `unit.c:2773-2774` | True (also True from excerpt rows alone) | 7 words | 7 | yes |
| `unit.c:2775-2776` | True (also True from excerpt rows alone) | 8 words | 8 | yes |

`wc -w` run literally on the reassembled quote files prints `7` and `8`. The `else if` form at 2775-2776 and the `if` form at 2773-2774 are quoted in the order they occur, so the pair is a faithful contiguous rendering of the branch.

## 5. SOURCES `teaches` support (corpus/SOURCES.md:163)

Teaches sentence: "Entering the active state overwrites the active-enter stamp with the transition's own clock reading, while leaving that state writes only the active-exit stamp, so a stop retains the old value and a restart replaces it."

Clause-by-clause against the quoted block:

- "Entering the active state overwrites the active-enter stamp" — supported: guard `!UNIT_IS_ACTIVE_OR_RELOADING(os) && UNIT_IS_ACTIVE_OR_RELOADING(ns)` then `u->active_enter_timestamp = u->state_change_timestamp;` fetched :2773-2774.
- "with the transition's own clock reading" — supported by fetched :2766 `dual_timestamp_now(&u->state_change_timestamp);`, refreshed earlier in the same `!MANAGER_IS_RELOADING` block, then copied at :2774. Fetched :2766 is inside the row anchor `src/core/unit.c:2763-2777` and inside the committed excerpt, but is **not** inside either admit quote span (:2773-2774, :2775-2776) — the admit line relies on the anchor/excerpt for this clause. Noted; the clause is evidenced by committed bytes, so not a defect.
- "while leaving that state writes only the active-exit stamp" — supported: the `else if (UNIT_IS_ACTIVE_OR_RELOADING(os) && !UNIT_IS_ACTIVE_OR_RELOADING(ns))` branch writes only `u->active_exit_timestamp` at fetched :2775-2776.
- "so a stop retains the old value" — supported within `unit.c`: `grep -n 'active_enter_timestamp\|active_exit_timestamp' unit.c` shows the only two writes are :2774 and :2776; the other hits are reads (`dual_timestamp_is_set` at :1971, :2066, :2451-2452) and inactive-stamp writes (:2769, :2771). No clearing on the way out. Cross-file absence (e.g. any other translation unit writing the field) was not checked this seat. [INFERENCE, low risk: the field is `struct Unit` private and the property getter only reads it.]
- "and a restart replaces it" — supported: a restart is stop then start, and starting re-enters the active-or-reloading set, re-running :2773-2774.

Row anchor tag check: `SOURCES.md:163` claims "tag v262 = commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492". GitHub API `git/ref/tags/v262` → ref sha `1f7dffaf714cc4488159c498b7a17cf34c5a96d5` (annotated tag object); `git/tags/1f7dffaf…` target sha → `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`. Claim holds.

## 6. Scope notes

- S157's remaining Gate rows are reject rows citing other URLs (`time-util.h` ×2, `service.c`, `org.freedesktop.systemd1.xml`, `bus-get-properties.c`, `bus-util.h`, `dbus-util.h`, `unit.h`, `libsystemd/.../bus-util.h`); the assignment scoped me to the unit.c admit line, so those URLs were not re-fetched. Their unit.c-adjacent assertions ("write site is unit.c:2774") match fetched :2774.
- Consumer check only: `corpus/knowledge/earlyoom-invocation-scope-r30.md:33` states the same :2773-2776 behavior, consistent with the fetched block. Entry-level support is not this seat's judgement.

## 7. Tooling and privacy

- No installs or updates this seat. Used only preinstalled `curl`, `python3`, `sha256sum`, `wc`, `grep`. No pacman/uv/npx needed.
- No host settings values, ids, unit names, journal text, or `/etc/default/earlyoom` values copied; only public upstream systemd bytes and lane corpus text.
- Read-only git not needed; all comparisons ran on the curl output under `/fast/scratch/hyaku/mori-r30-w2/ReopenS157/`. Nothing written in the lane except this report.
