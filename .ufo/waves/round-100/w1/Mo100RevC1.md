# Mo100RevC1 — C1 code review (seat-terminal `dead_auth`), round 100 wave w1

Role: reviewer. Scope: `git diff d1bd1b3 5e2bcf2 -- tools/mori-seat-terminal.py tools/mori-round17-seat-regressions.py SKILL.md`.
Method: both revisions archived via `git archive` into scratch; all runs below executed on the **archived landing tree**
(never the live checkout); read-only git only. Scratch removed after this report was written.

## Diff shape (evidence ground truth)

- `tools/mori-seat-terminal.py` (+155/−…): docstring class list (:12) and escape claim (:41); PERMITTED-INPUT-SET note
  "quota/rate/auth tokens" (:37); `CLASSES` gains `"dead_auth"` between `dead_quota` and `dead_error_other` (:122);
  `AUTH_STATUSES = frozenset((401, 403))` (:154), `AUTH_TOKENS` = permission_denied, PERMISSION_DENIED, unauthenticated,
  UNAUTHENTICATED, authentication_error, permission_error (:155-163); LIMITS sentence (:234-240); `_error_metadata`
  gains `auth_token` flag + 6th endswith family (:592, :638-643); projection view threads `auth_token` (:708, :743);
  `_classify` inserts `_auth_evidence` at exactly the two former `return "dead_error_other"` sites (:827-828, :834-835);
  `_auth_evidence` = status ∈ {401,403} or token (:839-840). Four new selftest arms `auth-*` (:1595-1700). **No window
  mechanics changed**: trim stays `if len(window) > 96: del window[:-64]` (:648-649), i.e. 97-byte carry, 64 retained.
- `tools/mori-round17-seat-regressions.py` (+3/−2): `CLASSES` (:194-204) and the `_STUB_TOOL` embedded copy (:2201-2204)
  both gain `dead_auth` in the same position. No fixture `expected.json` changed.
- `SKILL.md` (+2/−2): registry rows :173 (seat terminal probe) and :174 (r17 seat gate).

## Findings

- **F1 — Info (coverage, not a defect).** The four new selftest arms (tool :1595-1700) cover 401-status→`dead_auth`,
  spelling-without-status→`dead_auth`, 403+quota-text→`dead_quota` (precedence), and space-form "permission denied" at
  status 500→`dead_error_other`. No arm exercises bare 403→`dead_auth` without quota text, nor the
  UNAUTHENTICATED / authentication_error / permission_error spellings, nor 403-beside-rate-token. All of those are
  exercised by the battery (count-c1.py families A1/A2/N2, lines 64-85) which passes 50/50 on two seeds, so this is a
  selftest-thinness note only; SKILL.md:173 claims only "`auth-*` arms included", which is true.
- **F2 — Info (cosmetic).** SKILL.md:173 lists dead classes `dead_quota · dead_rate_limit · dead_auth · dead_error_other`
  while both CLASSES tuples order `dead_rate_limit` before `dead_quota` (tool :118-126; gate :194-204). Harmless:
  `validate_totals` compares `set(value) != CLASS_SET` (gate :1358-1367), order-insensitive.
- **F3 — Info (pre-existing, unchanged by this diff).** `_error_metadata`'s `(type=` digit buffer (:609-616) grows until
  the closing `)`; the 12-digit bound lives in the projector validation layer, so the buffer is bounded only by
  `--max-tail-bytes` (≤ 512 KiB default), and `_RETRIES_RE` rescans the ≤97-byte window per byte until first match.
  Present at entering; no C1 impact; recorded so it is not attributed to this landing.

No High/Medium findings. No caller outside `tools/mori-round17-seat-regressions.py` and SKILL.md references
`mori-seat-terminal` (grep over tools/ + SKILL.md), so the class-set change has no other callsite to migrate.

## Task checks

1. **Precedence, both paths** — PASS. Z.AI-with-code branch (:819-829): mapped codes → quota_token → rate_token → auth;
   Z.AI-without-code / non-zai branch (:830-838): quota_token → 429-or-rate_token → auth. `dead_auth` is returned only at
   the two exact sites that previously returned `dead_error_other`; mapped-code Z.AI seats and quota/rate/evidence seats
   are unreachable for auth (code inspected; battery Z1/N1/N2 and N4 confirm).
2. **Token window across chunk boundaries and JSON escapes** — PASS. `_iter_decoded` (:565-602) yields decoded bytes for
   valid simple escapes and `\uXXXX ≤ 0x7F`, yields 0xFF otherwise (breaks token continuity — matches docstring :41).
   Checks run after each append *before* the 97→64 trim (:628-649); longest token `authentication_error` = 20 B < 64 B
   retained, so no straddle loss is possible by construction. Empirically: battery family A3 rewrites one token char to
   `\u00XX` in the transcript bytes (count-c1.py:76-78, :140-143) and lands `dead_auth` 2/2 cases per run.
3. **No message text emitted** — PASS. Emitted seat record (:1044-1058) carries only derived fields (seat, key, kind,
   prefix, class, provider, model, error_status, retry_exhausted, retries, error_code, terminal_ms, reason);
   `auth_token` is a boolean used only in classification (:657, :708, :743, :840) and is not in the emitted row; the
   gate's `SEAT_KEYS` unknown-key check would reject any new emitted key — 66/66 pass with it.
4. **Docstring / LIMITS / help / SKILL.md rows accurate** — PASS. Class list (:12) and escape claim (:41) match the
   implementation; LIMITS (:234-240) states 401/403-or-spelling after quota and rate and disclaims credential
   attribution; `--help` output contains `dead_auth`; SKILL.md:173 "53 arms at round 100, `auth-*` arms included" —
   measured `arms=53, passed=53` with 4 `auth-*` arms; SKILL.md:174 "gate refuses a tool without it (`totals_keys`)" —
   reproduced: the **entering** gate run against the **landing** tool exits 1 with `GATE mismatch: 5/66` and 61 cases
   reasoned `totals_keys` (run-manifest reasons counter: `totals_keys ×61`).
5. **Selftest arms assert what they claim** — PASS. Each arm's expected seats/class matches its name and the contract
   rule (see F1); selftest green 53/53 on the landing archive.
6. **Behavior change for non-`dead_error_other` seats** — NONE. Insertion sites only (check 1); battery N4 pins
   unsettled/completed/aborted seats with auth evidence to their old classes; Z1 pins zai 1308/1302 to quota/rate even
   beside 403/401; the 66 round-17 fixtures (all classes) pass unchanged on the landing tool with the landing gate.

## Executed verification (exact outputs)

```
$ cd $S/land && TMPDIR=$S python3 tools/mori-seat-terminal.py --selftest ; echo rc=$?
rc=0
{"arms":53,"finding_id":"SELFTEST_OK","passed":53,"schema":"mori-seat-terminal-selftest-v1","tool_sha256":"a7ff6fb67a4c2378171c676adc2dd948baa7074421a56a6ba2282dbe402169e7"}

$ cd $S/land && TMPDIR=$S python3 tools/mori-round17-seat-regressions.py --tool tools/mori-seat-terminal.py \
    --fixtures .ufo/waves/round-17/fixtures/seat --output $S/gate-land ; echo rc=$?
rc=0
GATE ok: 66/66 cases matched

$ cd $S/land && TMPDIR=$S python3 tools/mori-round17-seat-regressions.py --selftest ; echo rc=$?
rc=0
SELFTEST ok: green_rc0_and_manifest,capability_absent_rc1,mismatch_rc1,forbidden_key_rc1,...  (truncated; rc 0)

$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-100/count-c1.py --root $S/land --work $S/work-land
C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=983172561 tool_rc=1   (rc=0)

$ python3 .../count-c1.py --root $S/land --work $S/work-seed7 --seed 7
C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=7 tool_rc=1   (rc=0)

$ python3 .../count-c1.py --root $S/enter --work $S/work-ent   (rc=1)
C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=unmet sourced=unmet checks_failed=battery,registry,sourced seed=66459713 tool_rc=1
  (12 misses, all want=dead_auth got=dead_error_other — C003,C036,C006,C018,C009,C008,C050,C038,C017,C040,C002,C001)

$ cd $S/enter && TMPDIR=$S python3 tools/mori-round17-seat-regressions.py --tool $S/land/tools/mori-seat-terminal.py \
    --fixtures .ufo/waves/round-17/fixtures/seat --output $S/gate-enter-vs-land ; echo rc=$?
rc=1
GATE mismatch: 5/66 cases matched   (run-manifest: totals_keys ×61, want.totals.*=None artifacts of the same missing key)
```

The entering battery result matches the frozen before receipt (`evidence/before-c1.txt`: `C1=unmet cases_ok=23/50 …
checks_failed=battery,registry,sourced`), and the landing results match the frozen target (`cases_ok=50/50 …
checks_failed=-`), on the printed seed and on seed 7 (kill rule spot-check).

## Not run

- Re-execution of `controls-r100.py` (frozen receipt `CONTROLS_DONE unexpected=0` cited as committed; K7/P1 rows used
  above are from that receipt, not re-derived by me).
- Content audit of `corpus/knowledge/seat-auth-deaths-r100.md` pins/pings beyond the counter's `sourced=met(S637,S638)`
  conjunction — owned by the sourced-check seats.
- Fuzzing beyond the shipped battery/selftest/gate harnesses.

VERDICT C1 holds: precedence, window/escape matching, emission projection, docs/registry accuracy, selftest-arm honesty
and class-stability for non-`dead_error_other` seats all verified on the archived landing tree; battery 50/50 on seeds
983172561 and 7, gate 66/66, selftest 53/53, entering-gate rejection via `totals_keys` reproduced; findings are
Info-level only.
