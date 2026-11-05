# Round 100 — lesson (mori, L1 MoriR100, attempt 1)

Entering `d1bd1b339b894de0249b0f60702dff9962da88d9` (r99 admitted). Frozen contract `.ufo/waves/round-100/contract.md`
at freeze `9579cff6cfab2f06b1918e54aec4a5553b705a9c`, with every control (do-nothing, blanket, status-only,
spelling-only, precedence-flipped and template-lookup forgeries, three part-removed trees, positives; six C2 forgeries)
executed and committed first: `.ufo/waves/round-100/evidence/controls-r100.txt` (`CONTROLS_DONE unexpected=0`, 17 rows
`AS_EXPECTED`, first run). Landing `5e2bcf2c487e377b51287c587144bdde5b233f8f`.

## Claims (frozen)

- **C1 coverage** — the seat terminal census (`tools/mori-seat-terminal.py`) names credential and entitlement deaths
  `dead_auth` (HTTP 401/403 or an auth spelling, read after Z.AI codes, quota and rate evidence); the round-17 fixture
  gate carries the class. Before `C1=unmet cases_ok=23/50 ... checks_failed=battery,registry,sourced`; landing
  `C1=met cases_ok=50/50 ... checks_failed=-` (seed 100 and an unseeded run).
- **C2 calibration** — stated quote word counts in `corpus/SOURCES.md` match their quotes or carry an appended named
  correction. Before `C2=unmet stated=58 mismatches=7 uncorrected=7`; landing `C2=met stated=60 ... uncorrected=0
  spurious=0 altered=0 census=ok`. **Withdrawn after landing** (Mistake 5): the landing's appended corrections edit
  the immutable anchor cell (CORPUS rule 2), and six of the seven mismatches were already superseded in round 72.
  The edits were reverted and the correction landed the rule-2 way (S640–S644); the frozen counter, which does not
  read supersession, reads the final tip `unmet` again.

## Gate

New rows written this round (CORPUS rule 1), opened 2026-11-05 by the L1, pinned at `corpus/evidence/sources-r100/`:

| row | URL | access (UTC) | located quote (≤25 words, counted by command) | decision |
|---|---|---|---|---|
| S637 | https://connectrpc.com/docs/protocol/ | 2026-11-05T23:00:13Z, HTTP 200, 148033 B, sha256 `55d644c6…2578` | "use unauthenticated if the user can’t be identified or presents invalid credentials." (raw lines 646-647, 12 words) | admit, mined, tier A |
| S638 | https://grpc.github.io/grpc/core/md_doc_statuscodes.html | 2026-11-05T23:00:13Z, HTTP 200, 18133 B, sha256 `95459b76…e3c4` | "PERMISSION_DENIED must not be used for rejections caused by exhausting some resource" (raw line 88, 12 words) | admit, mined, tier A |
| S639 | https://www.rfc-editor.org/rfc/rfc9110.txt (scope §15.5.2/§15.5.4; S221 holds the URL for §15.4) | 2026-11-05T23:00:13Z, HTTP 200, 502941 B, sha256 `21c1cdce…232a` (pin `S221-rfc9110-r100.txt`) | "the request has not been applied because it lacks valid authentication credentials for the target resource." (lines 7550-7552, 16 words) | admit, mined, tier A (W04 cross-scope, by design) |
| S640 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | 2026-11-05T23:40:19Z, HTTP 200, 357953 B, sha256 `0889867a…1acd`, byte-identical to the S634 pin | "it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment." (raw lines 303-304, 18 words) | admit, correction row: `supersedes S634 —` 17-to-18 |
| S641 | https://docs.aws.amazon.com/waf/latest/developerguide/waf-tokens-immunity-times.html | 2026-11-05T23:42:08Z, HTTP 200, 16179 B, sha256 `5e5b941e…c865` | "This section explains how challenge and CAPTCHA timestamps expire." (line 54, 9 words) | admit, correction row: `supersedes S581 —` |
| S642 | https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-gettickcount64 | 2026-11-05T23:42:08Z, HTTP 200, 52661 B, sha256 `580f1935…277f` | "Retrieves the number of milliseconds that have elapsed since the system was started." (line 829, 13 words) | admit, correction row: `supersedes S582 —` |
| S643 | same URL and fetch as S642 | same | same quote, 13 words | admit, correction row: `supersedes S583 —` |
| S644 | https://learn.microsoft.com/en-us/windows/win32/api/realtimeapiset/nf-realtimeapiset-queryunbiasedinterrupttime | 2026-11-05T23:42:08Z, HTTP 200, 54774 B, sha256 `d0bcbba9…9136` | "If the function fails because it is called with a null parameter, the return value is zero." (line 827, 17 words; S584's 26-word quote is over the cap) | admit, correction row: `supersedes S584 —` |

Row changes logged old→new: none at the final tip. In between, the landing `5e2bcf2c` changed S221 `used-by`
(`corpus/knowledge/source-drift-hardening-r37.md` → `…, corpus/knowledge/seat-auth-deaths-r100.md`) and the anchor
cells of S581, S582, S583, S584, S634 (the C2 correction text); repair `878708b3` restored all six rows byte-for-byte
(`git diff d1bd1b33 <final> -- corpus/SOURCES.md` adds rows only). S221 was the wrong ground: its scope is §15.4
(`w1/Mo100ScoutSrc.md` finding 1), so the 401/403 citation moved to the new row S639.

Rejected this round: re-pointing S221 at §15.5 by `used-by` alone (done at landing, reverted: a row teaches its own
scope). A second rejection: Connect's HTTP-to-code table as the rule for 429 (it maps 429 to `unavailable`); the lane
keeps 429 as rate evidence, because the seats' providers spell rate limits in the text and the census separates deaths
by what clears them, not by Connect's retry code. A third: an appended in-row correction as the C2 fix (Mistake 5).

Assimilation: none this round (the `merge/mori/` package holds no provider-error or quote-count theme).
considerthese: `considerthese/2026-11-05.md` proposals 1–5 read; none taken (proposal 5's survivor trend is served
by the w1 mutation seat).

## Frontier step — census

Round start (`.ufo/waves/round-100/evidence/census-before.txt`): `mori ok`, `exit=0`, 44 `W04`, rows 408
(`git show d1bd1b33:corpus/SOURCES.md | grep -cE '^ {0,3}\| *S[0-9]{3,}'`).

## Mistakes (CORPUS: class · evidence · captured-by · fix)

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| 1 | number-drift (stated counts) | rows S581–S584 (written r70/r71) state quote word counts that differ from their quotes; S584's failed-call quote is 26 words against the 25-word cap; S586/S587 (r72) corrected S581/S583 by supersession and S585 re-stated S584's counts, but S634 (r99) says 17 for 18 with no successor (`evidence/before-c2.txt`) | none until the r99 closure's hand count (D1) | QUALITY 213; S640 supersedes S634 (and S641–S644, Mistake 5). Shown able to fail: `count-c2.py` on the entering tree, `uncorrected=7` |
| 2 | number-drift (own draft) | the round-100 draft rows S637/S638 said "11 words" for two 12-word quotes (`candidate/apply-c1.py` before the freeze) | the L1 computing the counts before freezing | counted by command (QUALITY 213); the C2 counter now reads new rows too (`stated=60` at landing). Shown able to fail: an 11 in either row makes `count-c2.py` print `uncorrected=1` |
| 3 | breaking-class-set | the round-17 fixture gate rejects any tool whose `totals` key set differs (`validate_totals` → `totals_keys`); adding a class without the gate turns a registered gate red | control K7 (`r17gate=rc1`) before the freeze | QUALITY 214; the class lands with the gate. Shown able to fail: K7 |
| 4 | misfiled-death-cause | on 2026-11-04/05 the census would file 187 of 190 `dead_error_other` seats under the unknown bucket while they were 401/403/permission_denied refusals (`evidence/live-errors-prefreeze.txt`); the orchestrator diagnosed the provider outage by hand from transcripts (prompt Amendments 8–26) | none: the class set had no auth bucket | C1. Shown able to fail: `before-c1.txt` (A1–A5 and Z1 families fail) |
| 5 | rule-breach-by-advice (calibration) | the C2 landing appended corrections inside the immutable anchor cells of S581–S584 and S634, following the r99 spot-check's "editable in place" note instead of CORPUS rule 2 ("A correction is a new row whose `teaches` opens `supersedes S0NN —`"); the frozen counter counted mismatches in rows already superseded in round 72, so its before value 7 overstated the uncorrected set (1, S634), and no supersession-aware do-nothing control was built (`w1/Mo100RevHarm.md`, `w1/Mo100RevC2.md`) | the lane's own append-only gate, run by a wave seat after landing: `round_changed=[S581,S582,S583,S584,S634]`, `stale_supersede=[S581,S582,S583,S584]`; not run by the L1 before the freeze though SKILL.md requires it before any SOURCES.md landing | reverted at `878708b3`; S640 supersedes S634; S641–S644 supersede S581–S584 so the stale-supersede finding clears (plain gate at the final tip: `appendonly_violations=50 round_changed=[] stale_supersede=[]`, as at entering); QUALITY 213 rewritten; C2 withdrawn. Shown able to fail: the gate on `5e2bcf2c` exits 1. Residual: `--round-base d1bd1b33` keeps listing the five ids (edit history) |
| 6 | wrong-scope citation | the landing cited S221 for RFC 9110 §15.5 by adding to its `used-by`, while S221's scope and teaching are §15.4 redirects (`w1/Mo100ScoutSrc.md` finding 1) | the scout seat's row-scope check | new row S639 with the §15.5 scope; S221 restored. Shown able to fail: S221's scope cell at `5e2bcf2c` names §15.4 |
| 7 | counter-plants-unlabelled-token | the C1 counter's random tails (`(request id r-%d)`, `[trace %d]`) produce numbers holding `429`/`402`, which the round-17 rule reads as rate/quota evidence; the planted label stays `dead_auth`, so the landing fails 49/50 on seeds 10, 11, 42 (`evidence/landing-c1-killrule.txt`) and on 17, 51, 52 (`w1/Mo100ExecReplay.md`). The pre-freeze controls ran one seed (100), which happened to be clean | the replay seat's extra seeds; nothing before the freeze | next counter: tails from a digit-free alphabet, or a label computed from the same token rule; controls run on several seeds before the freeze. Shown able to fail: `count-c1.py --seed 10` on the landing tree |

## Wave findings (w1, 12 seats, 0 dead)

- C1 replays: landing `50/50` on seeds 100, 7, 4242, 1234567891, 5, 6; `49/50` on seeds 10, 11, 17, 42, 51, 52
  (Mistake 7); entering `23/50` everywhere (`w1/Mo100ExecReplay.md`, `w1/Mo100CritC1.md`, `w1/Mo100MutC1.md`). Freeze
  integrity: frozen files unchanged between freeze and landing; landed tools byte-identical to the candidate.
- Live trial (`w1/Mo100ExecTrial.md`): four real session directories, 4741 transcripts, both tools: only transition
  `dead_error_other` → `dead_auth`, 22 seats, all on identical terminal records.
- Review (`w1/Mo100RevC1.md`): precedence, escape-aware window, projection and docs verified; info findings only.
- Held-out records (`w1/Mo100CritC1.md`): 22/26 right at landing (14/26 at entering). Wrong: H03/H04 capitalised
  quota with 403 → `dead_auth` (fixed after the landing, `6a1fc283`); H10/H11 CamelCase gRPC-Go spellings stay
  `dead_error_other` (a disclosed limit; routed). No counter forgery reached `met` without the rule.
- Mutation (`w1/Mo100MutC1.md`): 32 mutants of the round-100 surface; 26 killed (M09 on one of two seeds), 1
  equivalent (M18), 5 battery gaps G1–G5 (407 status, `not_authorized`, `unauthorized`, mixed case, no
  `errorMessage` member).
- Harm (`w1/Mo100RevHarm.md`): every registered self-test equal or additive on both trees; the r99 frozen counter
  byte-identical; one new red — the append-only gate on the C2 landing (Mistake 5), repaired.
- C2 (`w1/Mo100RevC2.md`, `w1/Mo100ExecCalib.md`, `w1/Mo100CritC2.md`): the seven mismatches re-derived by hand; the
  counter's grammar misses four stated counts (all correct today) and is blind to supersession and to nine
  forgery forms F1–F9; the withdrawal stands on Mistake 5 regardless.
- Consumers (`w1/Mo100ConnSibling.md`): the only exact key-set consumer of the seat census is the round-17 gate,
  updated in the same commit; no sibling lane's reader breaks.
- Sources (`w1/Mo100ScoutSrc.md`): S637, S638, RFC 9110 quotes located verbatim, live bytes equal the pins; S221
  scope finding → Mistake 6.

## Routed (next round)

1. Digit boundaries for the numeric quota/rate spellings, and a counter that cannot plant tokens it does not label
   (Mistake 7).
2. CamelCase gRPC-Go auth spellings, after a source is opened for the printed form.
3. A supersession-aware stated-count counter; its grammar gaps.
4. Battery gaps G1–G5; r99 D3/D4 carried; r97 R1–R3; 31 `prefix_only` digest rows; operator L0s.

## r99 spot-check routed defects

D1 → S640 (rule-2 correction; the in-place advice was not followed after Mistake 5). D2 → the round-100 counter
design (composed families A4/A5/N5 and the template-lookup control K5, which failed as expected); D3, D4 carried.
