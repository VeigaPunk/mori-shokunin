# Mo100ConnSibling — sibling-overlap and consumer scan (mori r100, wave w1, attempt 1)

Role: connector, read-only. No file outside this report or my scratch was created or modified; no git/jj
mutation; no subagents; no sudo/pacman. Scratch `/fast/scratch/hyaku/mori-r100/Mo100ConnSibling` removed at end.
Evidence base: current round cache (frozen contract + receipts read) and the live trees at fleet root
`/home/vgpnk/Projects/shokunin` (mori lane tip = landing `5e2bcf2c487e377b51287c587144bdde5b233f8f`, lane log:
`9579cff6c` freeze → `5e2bcf2cc` landing; `git -C ... log --oneline -8`).

## Method and scope traps (matters for reproduction)

- The fleet root `.gitignore` contains `*-shokunin/` (read: `/home/vgpnk/Projects/shokunin/.gitignore:1`), so a
  fleet-root grep with ignore rules silently skips every lane repo. The early fleet-wide `**/*.py` greps therefore
  returned false "No matches". Correct method: grep each lane from its own root (nested repo), plus one fleet-root
  grep for the non-lane surfaces (`scripts/`, `.ufo/` excluding `.ufo/state`, `tools/`, `templates/`, `counters/`).
- `.ufo/state` excluded everywhere per task; fleet `.ufo/waves` checked separately (zero hits for all four tokens).
- No tool installs were needed; none performed (nothing to record under the 2026-10-19 tooling authorization).

## 1. Consumers of `mori-seat-terminal` output / class names, and the exact key-set check

Search tokens: `mori-seat-terminal`, `dead_error_other`, `dead_rate_limit`, `mori-seat-terminal-v1`
(`mori-seat-terminal-v1` occurs only as a substring of `mori-seat-terminal` sites plus the schema constants
`SCHEMA = "mori-seat-terminal-v1"` — no independent consumer).

### The one exact key-set check in the fleet

`tools/mori-round17-seat-regressions.py` (the registered r17 fixture gate), `validate_totals`:

```python
if set(value) != CLASS_SET:
    return None, "totals_keys"          # :1361-1362
```

`CLASS_SET` derives from two `CLASSES` tuples in the same file — :194-203 (manifest side, now with `"dead_auth"`
at :199) and :2200-2204 (tool-output side, now `"dead_auth"` at :2203). This is the only place in all 21 lane
repos + fleet scripts where adding a `totals` key can break a consumer. Landing diff on the gate is exactly
`tools/mori-round17-seat-regressions.py | 3 +-` (full stat read from `git diff --stat d1bd1b33… 5e2bcf2cc…`,
artifact of this session); the fixture data `.ufo/waves/round-17/fixtures/seat/expected.json` is unchanged in the
landing and its per-case `totals` blocks are tolerated through the gate's zero-fill
(`expected_totals = {name: 0 for name in CLASSES}`, :1361, observed in the same read) — the contract's disclosed
"gate at the entering revision rejects the new tool (`totals_keys`); the landing updates that gate's class set in
the same commit" (`contract.md:36-38`) is exactly what the bytes show. The 66/66 re-run is C1's measured
`r17gate` family, not re-run by this seat (see Unrun).

Per-hit verdicts (all others: NO break — they read named fields, pin historical bytes, or are prose/evidence):

| Hit | Surface | Verdict on `totals` gaining `dead_auth` |
|---|---|---|
| mori `tools/mori-seat-terminal.py` | landed tool; `CLASSES` :118-126 with `dead_auth` :122; `totals = _zero_totals()` :1130; precedence quota→rate→auth at :819-836 both zai and non-zai branches | producer; self-consistent |
| mori `tools/mori-round17-seat-regressions.py` | gate, the exact key-set check above | WOULD break mismatched pairs; landing updates it in the same commit (3-line diff) — disclosed in contract :36-38 and knowledge Limits :53-54 |
| mori `.ufo/waves/round-100/count-c1.py` | battery wants `dead_auth` (A1-A5, Z1 cases, :93-133); runs tool :166; registry check REQUIRES `dead_auth` in the SKILL row :211-212 | consumer that requires the new key, not broken by it |
| mori `.ufo/waves/round-100/controls-r100.py` :94-112, `candidate/apply-c1.py` :77-81 | construct the change (copies candidate tools, asserts one-match SKILL edits) | change constructors; consistent |
| mori `.ufo/waves/round-100/probe-live-errors.py` :52-60 | counts-only probe of r99 classes vs auth evidence; prints `r99_dead_error_other 190 of_which_auth_evidence 187` (receipt `evidence/live-errors-prefreeze.txt:11`) | no output-schema dependency |
| mori `.ufo/waves/round-17/{FINAL-PINNED_INPUTS.json,PINNED_INPUTS.json,build/*,evidence/*}`, round-100 `w1-spec.json`/`w1-dispatch.json`/`w1-validator.out` | sha pins of historical frozen copies; build prose; seat specs | pins of record (historical bytes), not live-tree re-verification; prose |
| mori `LOG.md`, `SCORECARD.md`, `SKILL.md` (registry rows, updated by apply-c1 `SKILL_SEAT_NEW` :46-53) | decision records; the registry row is consumed only by count-c1's registry family, which requires `dead_auth` | prose / requires-new-key |
| fleet `.ufo/reports/round-17/mori.md:14` | fleet-level round report prose | prose |
| fleet `scripts/**` (incl. `scripts/hyaku/*`), fleet `.ufo/waves/**` (state excluded) | combined-token grep: zero hits | no consumer |
| kaidoku `.ufo/waves/round-95/w1/ConnectorOverlap/overlap.md:49` | prose table: mori tools cited as O_NOFOLLOW precedents | prose |
| mado `.ufo/waves/round-23/w2/reports/CritProvinceBleed.md:102,262`; `round-47/w1/ConnSiblings.md:64`; `round-48/w1/ConnSiblings.md:18` (+report dup) | prose overlap/homonym notes | prose |
| tameshi `.ufo/evidence/round-18..21/*` (hash ledgers, e.g. `coldread/ledger.json:7204`, `measure-final.json:297`) | sha256 pins of `.ufo/waves/round-17/evidence/mutations/MutQuota/mutant-mori-seat-terminal.py` and `frozen/mori-seat-terminal-initial.py` — historical copies, not the live tool | pins of record; tameshi `tools/` swept separately: zero hits |
| souji `census/round-43/w1/R43connector01.md:52`, `R43connectorA.md:42-51`, `scan-receipts.json:9` | O_NOFOLLOW precedent prose + embedded grep stdout of an old HEAD | evidence of record |
| kumitate `.ufo/waves/round-41/falsify/ConnSiblingOverlap.md:3,9-11` | RAN the tool ad hoc on a live dir and read top-level fields (`files_scanned=68 completed=40 incomplete=18 aborted=3 unavailable=7`) | field-name reader, no totals key-set → unaffected; `verify/ConnSiblingA2.md:12`, `ReviewLedgerRoundReports.md:6-7` prose |
| kama `.ufo/waves/round-42/w1/out/R42B16/sibling_tools_sha256_list.txt:238` | path inventory for hashing | not an output consumer |
| kengaku `.ufo/waves/round-77/w1/ConnectorR77.md:42`; `round-78/w1/ConnectorR78.md:3174,3180,3219,3243` | comparison-table prose citing old tool line numbers; scan artifact rows marked "unrelated" | prose |
| tsukuroi `.ufo/waves/round-19/l1-capture/siblings/mori/*/PROVINCE.md:104`, `round-31/w1/ConnSiblingOverlap.md:33`, `round-32/w1/ScoutMoriHead/*`, `round-50/w1/R50*/*:104` | pinned PROVINCE captures (historical bytes) and selftest-env prose | captures of record / prose |
| chousa `.ufo/waves/round-62/w1/ConnSiblingOverlap.md:31` | prose precedent row | prose |
| tabi `.ufo/waves/round-23/w1/ConnSibling.md:13` | "not overlap despite the name" prose | prose |
| kake, kagi, kasegi, kotoba, kotodama, lore, revenger, game-dev-2d, game-dev-3d, audio, `kumitate-shokinin/` (stray typo dir) | whole-lane greps: zero hits | no consumer |

Complete code-surface enumeration: mori `tools/` (75 tracked files, `git ls-files tools/`; only the 2 files above
hit), tameshi `tools/` (zero), fleet `scripts/` + fleet `.ufo/` (one prose hit). Whole-lane greps for the >20-file
display windows (mori 667 files, tameshi 136) were sampled, not page-enumerated; every sampled hit is
prose/evidence/hash-ledger, and the executable-consumer class is fully enumerated by the code-surface sweeps
(declared under Unrun).

## 2. Sibling lanes that classify provider/seat death causes vs mori's landed precedence (quota → rate → auth)

| Sibling | Classifier | Agreement with mori quota→rate→auth |
|---|---|---|
| kumitate (documents the harness native admission surface) | `corpus/knowledge/native-admission-detail.md:110`: `FAILURE_RULES` "eight rows in contract order — usage_limit/quota/tokens_exceeded, rate_limit/429, model_unavailable/unavailable, authentication/401, permission/403, timeout/deadline, invalid_request/400, tool_failure — first match wins"; `failure-telemetry.md:90-92`: digit-guarded 429 rate_limit, 401 authentication, 403 permission_denied, 400 invalid_request; `cost-and-profile.md:87-92`: capacity={usage_limit, rate_limit, model_unavailable}, `is_authorization`={authentication, permission_denied}→`authorization_unavailable` immediately; `reconcile-and-cycle.md:27-29`: HALT={authentication, permission_denied, invalid_request} | AGREES on order: quota before rate before auth(s), same relative precedence mori landed. DIFFERS: native splits 401/403 into two classes and carries model_unavailable/timeout/invalid_request/tool_failure classes mori folds into `dead_error_other`; mori's `AUTH_TOKENS` (`permission_denied`, `unauthenticated`, …, tool :155+) are exactly the native class names — naming converges, granularity differs. Plane differs: native classifies at dispatch for retry policy; mori classifies aged terminal records post hoc. |
| fleet `scripts/hyaku/ufo-wave-policy-v2.json:145` (and v1) | "authentication/permission_denied report authorization_unavailable with no retry or hop; invalid_request unavailable; capacity classes keep chain advance" | Same matrix as kumitate's reading; semantically consistent with mori's operator rationale (auth refusal does not clear by waiting — knowledge entry :18-19) |
| kama | `tools/kama-probe.sh:496-498`: HTTP 401→`UNAUTHORIZED_SERVICE`/`http-401`, 403→`UNAUTHORIZED_SERVICE`/`http-403` | Same 401/403 statuses as `dead_auth`, service-liveness plane (not seats); no quota/rate precedence in that arm — no conflict demonstrated |
| kengaku | `plans/probe-battery-r19.md:273-286` P8 "auth-dead (401, distinct from quota-dead)"; `probe-battery-TEMPLATE.md:92-93,333` "a 429 is a provider-meter event, not a model failure"; "A 429/401 ends the probe" | Agrees with separating auth deaths from meter deaths; consistent with mori reading quota/rate evidence before auth |
| kake | `corpus/knowledge/crux-keyless-check.md:8`: CrUX 403 with `error.status=PERMISSION_DENIED` = "evidence about the caller's access, not evidence that the requested origin lacks CrUX data" | Same interpretation mori gives auth refusals (caller-credential scope); same spelling family mori now reads |
| souji | `corpus/lessons/round-44.md:173-174` + `round-44-verifier-spotcheck.md:52-53`: per-cause labels MiniMax Token Plan 429 (rate), Devin `permission_denied` (auth), Cursor `USAGE_PRICING_REQUIRED` (quota-ish); own record `census/round-44/records/seat-terminal-errors.json` | Ad-hoc prose labels, no class-set contract; consistent with mori's cause split |
| tsukuroi | `tools/check-r74-routed-r75.py:126-127,153-155`: one routed death-receipt check names the observed class "(RESOURCE_EXHAUSTED or 429)" | Capacity-only, scope-limited to one routed item; no auth arm, no conflict |
| mado | `corpus/knowledge/idle-lock-route-r17.md:28-29`: "The GitHub REST API returned HTTP 403 rate-limit" | Shows 403 is ambiguous in the wild (forbidden-entitlement vs rate-limit). mori's rate-before-auth handles the worded case; a wordless 403 rate-limit would land `dead_auth` under the status arm. Cross-lane risk for C1's 403 rule (below) |

Not classifiers despite token matches: kaidoku `tools/round-44/c2-counter.py:989-990` (`permission_denied` is its
own subprocess error string for local permission failures), souji `cert-protocol.md:705` ("unauthenticated"
about author identity), kengaku fixture data (401/402/429 as task ids/line numbers).

## 3. Sibling lessons recording the 2026-11-04/05 auth-death incident

- **kasegi `corpus/lessons/round-69.md:57-58`** — seven seats (SentinelGate-2, RevengerHosts, ScoutS103, ScopeF47,
  CriticC2, ExecHarness-3, ScribeRound-4) each ended on `[commandcode/deepseek/deepseek-v4.1-flash] 401 Invalid
  'Authorization' header or token. (type=authentication_error param=UNAUTHORIZED)`, no fallback walk, not replaced.
  Dating: fleet `scripts/hyaku/lane-addendum.md` amendment 13 records `CloseKasegiR69` among deaths at
  20:17-20:19 on 2026-11-04. This is the sibling lesson that already records the incident.
- kasegi `corpus/lessons/round-61.md:98` (+ spotcheck :81) — three seats on Devin swe-2 `permission_denied: This
  model is no longer available for your account…` followed by commandcode 401 `type=authentication_error`; r61
  date not re-verified (earlier than r69).
- kaidoku `corpus/lessons/round-81.md:73` — four exact-ID seats on the same Devin `permission_denied` stream error
  (run-15 era).
- tameshi `corpus/lessons/round-83.md:103-104` — SC1/SC2/S1/CN1 `permission_denied` (Devin swe-2 unavailable);
  R1 rate-limit 1302 then cyber_policy on fallback.
- souji `corpus/lessons/round-44.md` — same Devin `permission_denied` death class on 2026-10-30 (predates the
  incident; same class, earlier window).
- Operator-side incident log (fleet, not a lane lesson): `scripts/hyaku/hyaku.env:114-133,150-153,185,688-694,718,726-730`
  and `scripts/hyaku/lane-addendum.md` amendments 8-27 — commandcode 401, amr 402, opencode-go 402, Kimi-fallback
  403 `subscription permission_error`, Devin `permission_denied`; amendment 21 pins the rotation rule (omp rotates
  credentials only for usage-limit-classified errors; a hard 401 skips rotation).

## Proposed move (one, bounded; nothing executed or edited)

Post-settlement knowledge precision for a future mori round (coverage axis; touches no frozen predicate):
add one Limits bullet to `corpus/knowledge/seat-auth-deaths-r100.md` citing mado's observed case
(`mado-shokunin/corpus/knowledge/idle-lock-route-r17.md:28`, GitHub REST 403 that is rate-limit) beside the
existing S637/S638 grounds: a provider 403 that means rate-limit is `dead_auth` unless rate wording is present in
the record, because the status arm reads before nothing — auth is last but 403 alone is status evidence. mado's
case supplies the missing second real-world instance that 403 ≠ entitlement always; the landed knowledge entry
already carries the spelling-list boundary (`dead_error_other` for wordless `401` text without `errorStatus`,
:49-50) but not the 403-rate-limit case. Evidence: mado r17 entry (2026-10-20, byte-pinned recheck line);
mori knowledge entry Limits :45-54. Affected axes: coverage precision of the sourced entry; calibration (C2)
untouched; no tool or class-set change, so the r17 gate key set and C1's frozen predicate are untouched.
Verification for whoever lands it: `source:`/`verified-at`/`recheck` trio intact; `sources-census.sh validate`
exit 0; count-c1 `sourced` family still met (entry keeps S637/S638 `source:` lines; the addition is a Limits
bullet, not a registry edit).

## Risks

- Entering-revision r17 gate rejects the landed tool (`totals_keys`) — by construction and disclosed
  (contract :36-38); only a tool/gate update split across commits would break. Landing is one commit; count-c1's
  `r17gate` family measures the pair.
- The 403-ambiguity above (mado case): wordless 403 rate-limits misfile as `dead_auth`. Disclosure exists for
  spellings, not for this status case — that is the proposed move.
- mori's `dead_auth` merges what the native classifier splits (401 vs 403): an operator reading `dead_auth`
  cannot tell re-login (401) from entitlement/plan (403) without opening the seat record; consistent with, but
  coarser than, the runtime's action matrix. No consumer breakage.

## Unrun checks (named)

- Page-enumeration beyond the 20-file display cap of the whole-lane greps: mori (667 files), tameshi (136), and
  the per-lane vocab windows (kengaku 141, kake 107, kama 106, kaidoku 159, souji 490, mado 69, kumitate 71,
  tsukuroi 75 files). Code surfaces (`*/tools/`, `*/scripts/`, fleet `scripts/`, fleet `.ufo/`) were fully swept.
- Gate re-run (`GATE ok 66/66`), counters, selftest, controls — measurement belongs to the executor/reviewer
  seats; this seat ran nothing.
- kasegi r61 lesson date (r69 = 2026-11-04 is corroborated by `scripts/hyaku/lane-addendum.md` amendment 13).
- Live transcripts were never read; no message text, usage or credentials copied (counts/prose from committed
  lane files only).
