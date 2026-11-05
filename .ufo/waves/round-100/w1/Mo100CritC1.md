# Mo100CritC1 — critic on C1 (coverage, dead_auth)

Scope: attack C1 only. Entering `d1bd1b339b894de0249b0f60702dff9962da88d9`, landing `5e2bcf2c487e377b51287c587144bdde5b233f8f`. Trees extracted with `git archive | tar -x` into scratch (read-only git). Counter: frozen `.ufo/waves/round-100/count-c1.py`. No tools installed (none needed; python3 stdlib only). Nothing in the lane or fleet was written.

## 1. Reproduction of the counter (landing vs entering)

```
c1-enter-100:  C1=unmet cases_ok=23/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,Z1-zai-unmapped-auth selftest=ok r17gate=ok registry=unmet sourced=unmet checks_failed=battery,registry,sourced seed=100 tool_rc=1
c1-enter-7:    C1=unmet cases_ok=23/50 ... checks_failed=battery,registry,sourced seed=7
c1-enter-4242: C1=unmet cases_ok=23/50 ... checks_failed=battery,registry,sourced seed=4242
c1-land-100:   C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=100 tool_rc=1
c1-land-7:     C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=7 tool_rc=1
c1-land-4242:  C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=4242 tool_rc=1
c1-land-big (seed 1234567891): C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=1234567891 tool_rc=1
```
The entering line at seed 100 matches the contract's `before` receipt exactly (`23/50`, `checks_failed=battery,registry,sourced`).

Landing diff (entering → landing, tool only): `_classify` gains `_auth_evidence(view)` checked only after the Z.AI branch, quota token, 429/rate token, and immediately before the `dead_error_other` return. `_error_metadata` gains an `auth_token` flag matched on a 97/64-byte carry window over the full decoded span. No other class branch changes. Arithmetic of the ordering is correct: auth can only convert what would otherwise be `dead_error_other`.

## 2. Attempts to score C1=met without implementing the status-and-spelling rule

Forgeries live in scratch (`forge/forge.py`, one tree per variant; every other file of the landing tree symlinked). They read the same transcripts and emit the seats schema.

| Attempt | Construction | seed 100 | seed 7 | seed 4242 | seed 1234567891 | Result |
|---|---|---|---|---|---|---|
| F1 template lookup | Fixed templates copied from the counter (regex, tail-stripped, exact fullmatch); no match → `dead_error_other` | 42/50 | 42/50 | 42/50 | not run | unmet: A4, A5 composed families fail |
| F2 auth-first, no precedence | status 401/403 or any spelling → `dead_auth` before quota/rate | 41/50 | 41/50 | 41/50 | not run | unmet: N1, N2, Z1-zai-quota, Z1-zai-rate fail |
| F3 keyword forger | any `permission|denied|auth|forbidden|unauthori` word → `dead_auth`; quota/rate first | 43/50 | 41/50 | 40/50 | not run | unmet: N3 (`permission denied writing cache`), N5 composed words, Z1 fail |
| F4 seed search | Imports the frozen counter's `battery()`, searches seeds 1..20000 for the one whose bodies match the files, emits its expected classes | 50/50 | 50/50 | 50/50 | 11/50 | battery met on small seeds; unmet at 1234567891 |
| F5 F4 + delegation | F4 plus: non-counter invocations (selftest, round-17 gate sandbox, i.e. files not named `C\d{3}`) delegate to the landing tool | **C1=met** | **C1=met** | **C1=met** | 11/50 → unmet | a full `C1=met` line without implementing the rule, for seeds ≤20000 |

Exact counter lines (seed 100 shown; seeds 7/4242 identical in shape):

```
F1 seed 100: C1=unmet cases_ok=42/50 families_failed=A4-auth-status-composed,A5-auth-spelling-composed selftest=ok r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,r17gate seed=100 tool_rc=0
F2 seed 100: C1=unmet cases_ok=41/50 families_failed=N1-quota-wins,N2-rate-wins,Z1-zai-quota-code,Z1-zai-rate-code selftest=ok r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,r17gate seed=100 tool_rc=0
F3 seed 100: C1=unmet cases_ok=43/50 families_failed=N3-other-stays,N5-other-composed,Z1-zai-quota-code,Z1-zai-rate-code selftest=ok r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,r17gate seed=100 tool_rc=0
F3 seed 4242: C1=unmet cases_ok=40/50 families_failed=N3-other-stays,N5-other-composed,Z1-zai-quota-code,Z1-zai-rate-code selftest=ok r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,r17gate seed=4242 tool_rc=0
F4 seed 100: C1=unmet cases_ok=50/50 families_failed=- selftest=ok r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=r17gate seed=100 tool_rc=0
F4 seed 4242: C1=unmet cases_ok=50/50 families_failed=- selftest=ok r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=r17gate seed=4242 tool_rc=0
F4 seed 1234567891: C1=unmet cases_ok=11/50 families_failed=A1-auth-status,A2-auth-spelling,A3-auth-escaped,A4-auth-status-composed,A5-auth-spelling-composed,N1-quota-wins,N2-rate-wins,N4-aborted,N4-completed,N4-unsettled,Z1-zai-quota-code,Z1-zai-rate-code,Z1-zai-unmapped-auth selftest=ok r17gate=rc1 registry=met sourced=met(S637,S638) checks_failed=battery,r17gate seed=1234567891 tool_rc=0
F5 seed 100: C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=100 tool_rc=0
F5 seed 7: C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=7 tool_rc=0
F5 seed 4242: C1=met cases_ok=50/50 families_failed=- selftest=ok r17gate=ok registry=met sourced=met(S637,S638) checks_failed=- seed=4242 tool_rc=0
F5 seed 1234567891: C1=unmet cases_ok=11/50 families_failed=A1-auth-status,...(abridged; same battery families as F4) checks_failed=battery,r17gate seed=1234567891 tool_rc=0
```

Reading: F1–F3 (template, keyword, precedence) are each caught by the battery. F4 and F5 show the battery is only as strong as its seed range: a forger that searches the counter's generator passes any printed seed it can enumerate. The counter's default seed is `SystemRandom` over 1..2^31, so the search fails in expectation, and the 1234567891 run fails. This is a disclosed-class weakness (the counter reads its own generator from a path outside the tree); it is not a flaw in the landing rule. Attempt F5 needed a file-name check (`C\d{3}`) to route the round-17 gate; that is a forger's special-casing, not a counter defect.

Held-out evidence is in §3; it is the stronger attack.

## 3. Held-out terminal-error records (own construction, not from the counter or selftest)

26 synthetic session files (`{"type":"session","version":3}` header + one assistant `stopReason:"error"` message, `completedAt` = 1793000000000−3600000 unless noted). Run with `--now-ms 1793000000000 --max-files 1000` on both trees (default 900 s settle). Expectation is my reading of the frozen predicate P1 plus the claim's stated intent. ✔ = landing agrees with expectation.

Records (errorStatus / errorMessage / provider):

| id | errorStatus | errorMessage (abridged) | provider | expected | entering | landing | |
|---|---|---|---|---|---|---|---|
| H01 | 401 | `401 Invalid API key provided for this workspace` | anthropic | dead_auth | dead_error_other | dead_auth | ✔ |
| H02 | 403 | `403 Quota exceeded for quota metric 'Requests'` | anthropic | dead_quota | dead_quota | dead_quota | ✔ |
| H03 | 403 | `403 Quota exceeded for project 'acme-prod'` | anthropic | dead_quota | dead_error_other | **dead_auth** | ✘ |
| H04 | 403 | `403 QUOTA_EXCEEDED: project over its daily limit` | anthropic | dead_quota | dead_error_other | **dead_auth** | ✘ |
| H05 | 403 | `403 rate limit exceeded for organization` | anthropic | dead_rate_limit | dead_rate_limit | dead_rate_limit | ✔ |
| H06 | 403 | `403 plan blocked (type=1308)` | zai | dead_quota | dead_quota | dead_quota | ✔ |
| H07 | 403 | `403 slow down (type=1302)` | zai | dead_rate_limit | dead_rate_limit | dead_rate_limit | ✔ |
| H08 | 401 | `401 forbidden (type=1450)` | zai | dead_auth | dead_error_other | dead_auth | ✔ |
| H09 | 500 | `500 internal error: permission denied writing cache` | openai | dead_error_other | dead_error_other | dead_error_other | ✔ |
| H10 | — | `rpc error: code = PermissionDenied desc = model not entitled for this key` | devin | dead_auth | dead_error_other | **dead_error_other** | ✘ |
| H11 | — | `rpc error: code = Unauthenticated desc = token expired` | devin | dead_auth | dead_error_other | **dead_error_other** | ✘ |
| H12 | — | `{"code":"permission_denied","message":"no entitlement"}` | anthropic | dead_auth | dead_error_other | dead_auth | ✔ |
| H13 | — | `stream error permission\u005fdenied: no entitlement` (escape in transcript bytes) | anthropic | dead_auth | dead_error_other | dead_auth | ✔ |
| H14 | — | filler ×25 (>200 B) + ` unauthenticated` | anthropic | dead_auth | dead_error_other | dead_auth | ✔ |
| H15 | 403 | `403 ` + filler ×25 + ` quota exceeded` | anthropic | dead_quota | dead_quota | dead_quota | ✔ |
| H16 | 500 | `500 ` + filler ×25 + ` permission denied` | anthropic | dead_error_other | dead_error_other | dead_error_other | ✔ |
| H17 | 500 | `500 upstream authentication_error: key disabled` | anthropic | dead_auth | dead_error_other | dead_auth | ✔ |
| H18 | 429 | `PERMISSION_DENIED but RATE_LIMITED` | anthropic | dead_rate_limit | dead_rate_limit | dead_rate_limit | ✔ |
| H19 | — | `upstream returned 401 Unauthorized` (text only, no status field) | anthropic | dead_error_other | dead_error_other | dead_error_other | ✔ (boundary) |
| H20 | `"401"` (string) | `401 Unauthorized` | anthropic | dead_error_other | dead_error_other | dead_error_other | ✔ (boundary) |
| H21 | 403 | `403 Forbidden` (completedAt 10 s ago) | anthropic | error_unsettled | error_unsettled | error_unsettled | ✔ |
| H22 | 403 | `403 \u0071uota exceeded` (escaped lowercase q) | anthropic | dead_quota | dead_quota | dead_quota | ✔ |
| H23 | — | `réseau permission_denied gate` (raw UTF-8 before token) | anthropic | dead_auth | dead_error_other | dead_auth | ✔ |
| H24 | — | `permission_denied: code 1113 out of quota` | zai | dead_quota | dead_quota | dead_quota | ✔ |
| H25 | 401 | filler ×25 (>200 B) + ` usage limit reached` | anthropic | dead_quota | dead_quota | dead_quota | ✔ |
| H26 | — | `Retry budget exhausted after 3 retries: Devin stream error unauthenticated` | devin | dead_auth | dead_error_other | dead_auth | ✔ |

Totals: entering agrees with expectation on 14/26 (it misses the auth records H01, H08, H10, H11, H12, H13, H14, H17, H23, H26 and the 403 records H03/H04 are also missed at entering). Landing agrees on 22/26. Landing disagrees on four records: H03, H04, H10, H11.

Landing answers I think are wrong, and why:

1. **H03, H04 — capitalised or uppercase quota with HTTP 403 becomes `dead_auth`.** The landing tool's quota vocabulary is case-sensitive (`quota`, `usage limit`, `402`, `credits`), so `Quota exceeded` and `QUOTA_EXCEEDED` are not quota evidence, and the 403 pushes them to `dead_auth`. The landing comment states the purpose of the precedence: "explicit quota/rate evidence wins … some providers answer quota exhaustion with 403". A 403 quota exhaustion reported in title case is a quota death labelled as a credential refusal, the exact category error the claim exists to prevent. This is a real defect of the precedence, though the frozen predicate's "quota evidence" is the tool's own token set, so the battery cannot see it. Remedy would need a case-insensitive quota match, which is a predicate change, not a fix inside this claim.
2. **H10, H11 — CamelCase gRPC-Go spellings stay `dead_error_other`.** The predicate enumerates only the six SCREAMING_SNAKE/snake spellings. Go's `codes.Code.String()` prints `PermissionDenied`/`Unauthenticated` and grpc-go's error text is `rpc error: code = <Code> desc = …` [INFERENCE from grpc-go's public API, not present in the pinned S638 page, which lists only the upper-snake names]. Fleet transcripts contain such lines (counts only, see §4). The claim's motivation names "Connect/gRPC/provider auth refusal", so this is a coverage gap against the stated motivation, not a predicate falsification.

Landing answers I agree with on the boundary records: H09 (plain-word 500 stays other), H16 (long plain-word stays other), H19/H20 (text-only and string-typed status stay other, consistent with reading the HTTP status field only).

## 4. Counts-only evidence (fleet transcripts, no message text printed)

Command: `find ~/.omp/agent/sessions/-Projects-shokunin -name '*.jsonl' -print0 | xargs -0 grep -h -c -F <pattern> | awk` (summed line counts).
- `code = PermissionDenied`: 15 lines
- `code = Unauthenticated`: 11 lines
- `code = PERMISSION_DENIED`: 2 lines
- `code = UNAUTHENTICATED`: 2 lines
- `PermissionDenied`: 157 lines; `Unauthenticated`: 107 lines

These are raw line counts, not proof that each sits in an `errorMessage` field; they show CamelCase spellings occur in the fleet's transcripts.

## 5. Tooling

No packages installed or upgraded. Used python3 (stdlib) and coreutils. Nothing installed in ~/.local/bin or PATH.

## 6. Unrun

- Seed search beyond 20000 and the default random seed (not run; F4/F5 expected unmet by construction).
- Counter run on seeds other than 100, 7, 4242, 1234567891 for the landing tree (not run).
- Transcript lines larger than the 512 KiB tail window (`DEFAULT_MAX_TAIL_BYTES`) (not run; pre-existing limit, out of claim scope).
- Mutation test with precedence reversed inside the landing tool itself (not run; F2 covers the precedence attack via a standalone classifier).

## 7. Verdict

C1 as frozen: the predicate P1 holds on the counter (landing 50/50 on four seeds, every other check met; entering reproduces the contract's 23/50). Both held-out defects (H03/H04 capitalised quota with 403; H10/H11 CamelCase gRPC-Go spellings) are outside what the frozen battery can see, and the first contradicts the claim's stated intent.

VERDICT C1 needs-amend: landing 50/50 on the counter at seeds 100, 7, 4242, 1234567891 and entering reproduces 23/50, but held-out records H03/H04 show 403 quota deaths in title/upper case reclassified dead_auth (quota token is case-sensitive, the precedence the claim relies on does not hold for them), and H10/H11 CamelCase gRPC-Go auth spellings stay dead_error_other against the stated gRPC motivation.
