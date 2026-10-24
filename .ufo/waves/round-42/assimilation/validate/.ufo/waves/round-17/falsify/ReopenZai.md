# ReopenZai — fresh falsification of source row S043 and the lessons quote

Seat: MoriR17.ReopenZai-4 (wave 2, leaf; no subagent dispatch). Lane root:
`/home/vgpnk/Projects/shokunin/mori-shokunin`, branch `master`, measured tip
`273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` (as pinned). Access date 2026-10-20
(reopen at 16:48 -03:00 / 19:48 GMT). This seat attacks evidence only; it does not judge
admission, edit the registry, or run any tool selftest/gate.

Installs/updates: none. Writes: this report only. VCS mutation: none. No `/tmp`, no
background jobs, no journal query, no transcript read.

## 1. Live reopen of the cited page

Two independent surfaces were fetched, plus the docs index:

| Surface | Command | Observed |
|---|---|---|
| Canonical page | `curl -fsSI https://docs.z.ai/api-reference/api-code` | `HTTP/2 200`, `content-type: text/html; charset=utf-8`, `date: Tue, 20 Oct 2026 19:48:35 GMT`, rc0 |
| Canonical HTML body | `curl -fsSL https://docs.z.ai/api-reference/api-code \| grep -c 'Rate limit reached for requests'` | `2` (server-rendered; the quote is in the delivered HTML, not only in a JS payload), rc0 |
| Markdown alternate | `read https://docs.z.ai/api-reference/api-code` (reader reported `alternate-markdown`) and `curl -fsSI https://docs.z.ai/api-reference/api-code.md` | `HTTP/2 200`, `content-type: text/markdown; charset=utf-8`, rc0 |
| Size/identity | `curl -fsSL …api-code.md \| wc -c`; `… \| grep -c ''`; `… \| sha256sum` | `5208` bytes, `82` lines, `sha256 863aaf0d8a7b3309e71056a5ea786a2c889d985fb65a607459a12771291446f5` |
| Docs index | `curl -fsSL https://docs.z.ai/llms.txt \| grep -n 'api-reference/api-code'` | `31:- [Errors](https://docs.z.ai/api-reference/api-code.md)` |

Freshness witness: `.ufo/waves/round-17/build/SrcZaiErrorCodes.md:14-15` recorded the opening
as `status=200`, **5208 bytes**. My reopen returns the same 5208 bytes / 82 lines, byte-identical
tabulation, so the cited bytes did not change between the source seat's opening (receipt
mtime 15:54:27 -03:00) and this re-open. That covers the opening→reopen interval only; it is
not a permanent pin.

Exact anchors on the served markdown (line numbers verified against the live bytes, not
reconstructed):

```
16:| 1113 | 429 | Insufficient balance or no resource package. Please recharge. |
31:| 1302 | 429 | Rate limit reached for requests |
33:| 1308 | 429 | Usage limit reached for `{number}` `{unit}`. Your limit will reset at `{next_flush_time}` |
```

`# Errors` is line 5; the table header is line 9. The page is a general error-code table
(`Error Codes | HTTP Status Code | Error messege`), not a 429-only page.

## 2. Row fields under test (`corpus/SOURCES.md:49`)

| Field | Row text (abridged) | Observed on page | Verdict |
|---|---|---|---|
| source | `Z.AI API error codes — https://docs.z.ai/api-reference/api-code` | Canonical URL resolves 200 to the vendor's own Mintlify docs; markdown alternate is the same deployment (`x-mintlify-client-version`, Vercel headers) | **Match.** First-party vendor documentation for its own error contract. |
| scope | `Z.AI HTTP 429 business-code distinctions` | Page defines an outer HTTP status plus inner business code (`## Errors`, :7-8) and maps each business code to an HTTP status; all three cited rows are 429 | **Match, correctly narrowed.** The page is broader than 429; the scope names only the subset actually used. |
| anchor | `Error table, api-code.md lines 16/31/33, codes 1113/1302/1308; opened 2026-10-20` | Live bytes: 16=1113/429, 31=1302/429, 33=1308/429 | **Match exactly.** Line numbers are resolvable only against the `.md` alternate, which the anchor names; the rendered HTML has no such lines. |
| teaches | `Code 1302 means request rate limit; 1113 and 1308 usage/balance causes also use HTTP 429, so status alone cannot distinguish rate limit from quota.` | 1302 message is "Rate limit reached for requests" (:31); 1113 "Insufficient balance or no resource package" (:16); 1308 "Usage limit reached for …" (:33); 1305/:32, 1309/:34, 1310/:35, 1311/:36, 1313-1315, 1316-1321 all carry 429 | **Match.** Every clause is directly supported, and the "status alone" conclusion follows from the table itself. |
| tier | `A` | Official vendor docs, same kind/tier precedent as S044/S046 (`docs | A`, `corpus/SOURCES.md:50,52`) | **Match.** Tier assignment is consistent with lane convention. |
| status / opened / recheck / used-by | `mined | 2026-10-20 | on-release | corpus/knowledge/seat-terminal-status-r17.md` | Row exists at :49; entry exists; see §4 | **Consistent** (see §4). |

## 3. The ≤25-word quote in `corpus/lessons/round-17.md:49`

```
| S043 | https://docs.z.ai/api-reference/api-code | Error table, api-code.md:31, code 1302/HTTP429:
“Rate limit reached for requests”; :16/:33 also map 1113/1308 to429. |
```

- Located quote: **"Rate limit reached for requests"** — verbatim cell text of the
  `1302 | 429` row at served markdown line 31.
- Word count: **5** (`python3` split; ≤25 satisfied).
- Location claim `api-code.md:31` — verified on live bytes.
- Secondary claim `:16/:33` for 1113/1308 — both verified at those exact lines; both map to 429.
- URL and access date (2026-10-20) — verified by reopen today.

**Agree.** The quote is verbatim, correctly located, and under the word cap. The only deviation
is typography: `to429`/`HTTP429` lack a space, which is cosmetic and changes no meaning.

## 4. used-by / status link and the dependency test

Registry link: `S043 … | mined | 2026-10-20 | on-release | corpus/knowledge/seat-terminal-status-r17.md`
(`corpus/SOURCES.md:49`). The used-by target exists (`corpus/knowledge/seat-terminal-status-r17.md`,
sha256 `aaff53d118eba83224f5bf77452fce218b56191b361fe2e1d396901ca97f56d2`). `on-release` is the same
interval used by the adjacent living-docs rows S044-S048, so it is convention-consistent for a
vendor documentation page. `mined` matches the lessons claim (`corpus/lessons/round-17.md:56-57`).

Dependency test — delete S043 and ask what loses support:

1. `corpus/knowledge/seat-terminal-status-r17.md:20` decision-table row `older error, Z.AI type
   1113/1308 or quota token | dead_quota`, and `:21` `type 1302 or rate-limit/429 token |
   dead_rate_limit`.
2. `corpus/knowledge/seat-terminal-status-r17.md:26-28`: "S043 is operational, not decorative:
   Z.AI documents both rate-limit and usage/balance causes under HTTP 429. Business-code and
   quota tests precede the generic 429 test."
3. `tools/mori-seat-terminal.py:87-88` `QUOTA_CODES = frozenset(("1113","1308"))`,
   `RATE_CODES = frozenset(("1302",))`; `:262-272` code test before token/429 test.
4. Fixtures: `.ufo/waves/round-17/fixtures/seat/expected.json:1236-1306` cases
   `code_quota_1113_beats_429`, `code_quota_1308_beats_429`, `code_rate_1302_beats_quota_token`
   (packs pinned at :6-8); selftest arms `tools/mori-seat-terminal.py:1327-1379`.
5. Contract `Amendment A1` `:112` and `:123` (code-first rule, 1113/1308 quota, 1302 rate).

The dependence is **material, not decorative**, and I can show it from the classifier, not just
from citation edges. The token heuristic alone would misclassify two of the three mapped codes:

- 1113 message "Insufficient balance or no resource package" contains none of
  `QUOTA_TOKENS = ("quota","usage limit","402","credits")` (`:86`);
- 1308 message starts "Usage limit reached …" with a capital `U`; the token is the lowercase
  `"usage limit"`, so a case-sensitive `in` misses it;
- both carry `errorStatus == 429`, so without the S043-derived code sets both would fall through
  to `dead_rate_limit` at `:269-272`.

So removing S043 changes three fixture-asserted classes. Chronology also supports the lessons
causal sentence at `corpus/lessons/round-17.md:59`: `build/SrcZaiErrorCodes.md` 15:54:27 →
`build/CriticFrontier.md` 16:02:31 (proposes code-before-429) → `contract.md` A1 16:08:18 →
`tools/mori-seat-terminal.py` 16:13:42 (mtime evidence). "S043 caused the A1
business-code/quota-before-generic429 fix" is observed ordering plus content agreement;
[intent attribution is INFERENCE].

## 5. Residual findings and qualified disagreements (none falsifies the row or quote)

R1. **Token-identity inference is unmarked in the entry body.** `corpus/knowledge/seat-terminal-status-r17.md:20`
    says "Z.AI type 1113/1308" as fact, but the page documents a JSON body `error.code`
    (`## Error Shapes`), not OMP's transcript `(type=NNNN)` token. The opening receipt already
    classes that link `[INFERENCE]` (`build/SrcZaiErrorCodes.md:35`) and `build/FrontierLinkage.md:17`
    says the docs do not establish it. The row's own `teaches` avoids the overclaim, so the row
    is sound; the entry body does not carry the marker. Confidence high on the text gap;
    materiality is L1's call.

R2. **Classifier coverage is 3 of the page's 12+ 429 codes.** The page maps usage/balance/
    entitlement causes to 429 at 1113 (:16), 1305 (:32), 1308 (:33), 1309 (:34), 1310 (:35),
    1311 (:36), 1313-1315 (:37-39), and 1316-1321 (:40-45). The tool maps only 1113/1308→quota
    and 1302→rate. A `(type=1310)` ("Weekly/Monthly Limit Exhausted") or `(type=1316..1321)`
    ("Usage limit reached …", capital `U`) therefore classifies `dead_rate_limit` via the 429
    branch. `seat-terminal-status-r17.md:50` discloses heuristics "outside the explicitly mapped
    Z.AI codes", so this is a disclosed limit rather than a false row claim — but `:26` can be
    read as complete vendor discrimination. The row's `teaches` correctly limits itself to
    1113/1308, so the lesson quote is not implicated.

R3. **Anchor durability.** No page digest is pinned in SOURCES, the lesson, or the entry
    recheck line; `last-modified` on the `.md` response equals the per-response `date`
    (19:47:56 GMT), so it cannot witness content age. Today's byte-identical 5208/82 match is
    the only content witness for the opening→reopen interval. The anchor is line-based on a
    living page and will drift on any edit; `on-release` is the sole guard.

R4. Cosmetic only: `corpus/lessons/round-17.md:49` writes `HTTP429` and `to429` without spaces.

## 6. Verdict

**Agree with S043 and the lessons quote** on all six attacked facets (source, scope, anchor,
teaches, tier, quote): URL live and first-party; scope correctly narrowed; anchors 16/31/33
verified on the served bytes; every teaching clause directly supported; tier A consistent;
quote verbatim, 5 words, correct line. The used-by/status link is live and the knowledge entry
genuinely depends on the cited fact — the tool's code-before-429 branch and three fixture
cases change without it. No falsifying defect was found in this scope.

Exact attacked scope: the S043 row (`corpus/SOURCES.md:49`), its field values, the
`corpus/lessons/round-17.md:49` cell, the S043→`seat-terminal-status-r17.md` used-by edge, and
the A1 `:112/:123` code-precedence implementation in `tools/mori-seat-terminal.py`. Not attacked
here: classifier correctness beyond the S043 code paths, fixture adequacy, other source rows,
and any admission/score judgment.

## 7. Commands (all read-only, no writes)

| Command (cwd = lane root unless noted) | rc | Output used |
|---|---|---|
| `read https://docs.z.ai/api-reference/api-code` | 0 | Full rendered/markdown-alternate body; quote present |
| `curl -fsSI https://docs.z.ai/api-reference/api-code` | 0 | HTTP/2 200, text/html, date 19:48:35 GMT |
| `curl -fsSL …/api-code \| grep -c 'Rate limit reached for requests'` | 0 | `2` |
| `curl -fsSI https://docs.z.ai/api-reference/api-code.md` | 0 | HTTP/2 200, text/markdown, 82-line/5208-byte body |
| `curl -fsSL …/api-code.md \| grep -n -E '^\| (1113\|1302\|1308) \| 429 \|'` | 0 | lines `16:`, `31:`, `33:` |
| `curl -fsSL …/api-code.md \| wc -c` / `grep -c ''` / `sha256sum` | 0 | `5208` / `82` / `863aaf0d…91446f5` |
| `curl -fsSL https://docs.z.ai/llms.txt \| grep -n 'api-reference/api-code'` | 0 | `31:- [Errors](https://docs.z.ai/api-reference/api-code.md)` |
| `grep` (tool) `^\| S04[0-9] \|` on `corpus/SOURCES.md` | 0 | row S043 at :49 |
| `grep` (tool) `1302\|1113\|1308\|QUOTA_TOKENS…` on `tools/mori-seat-terminal.py` | 0 | `:86-88`, `:262-272`, selftest `:1327-1379` |
| `grep -n -E '1113\|1308\|1302' …/fixtures/seat/expected.json` | 0 | cases at `:1236-1306`, pins `:6-8` |
| `sha256sum tools/mori-seat-terminal.py` | 0 | `5819c3c0…adbdba` = PINNED_INPUTS value |
| `stat -c '%y %n'` on six lane files | 0 | chronology in §4 |
| `python3 -c` quote word count + lesson line dump | 0 | `words 5`; line 49 as quoted |

## 8. Remaining unknowns

- Whether the page content changed between the source seat's fetch (15:54) and mine is
  answered only by the byte-count match (5208) and identical cited lines; no per-fetch digest
  was recorded at 15:54, so change-and-revert inside that window is unobservable [UNKNOWN].
- Whether any real OMP transcript's `(type=NNNN)` is the same namespace as this vendor table
  is [INFERENCE]; this seat read no transcript and the page does not document that token form.
- Human intent behind L1's narrowing to 1113/1308 (R2) is not recorded in the contract; the
  contract names exactly those codes [UNKNOWN as motive, observed as text].
