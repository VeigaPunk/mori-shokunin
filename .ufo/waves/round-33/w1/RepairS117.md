# Round-32 routed repair: S117

Axes: strict R-R support; reproducible source provenance; narrow correction; lane containment.

## Finding

**S117 is not current under R-R on its population page alone.** The frozen base row puts the tags API first in its source cell (`timeout 10s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show -L123,123:corpus/SOURCES.md 7d382043`; output: commit `7d382043016e8854e3be2ee523a095b409c3d8a1`, `corpus/SOURCES.md` line 123). The round-32 spot-check says this population page is the tags JSON and reports zero `mem avail` hits there; it finds each listed factual clause absent from that page (`corpus/lessons/round-32-verifier-spotcheck.md:89`). Code pages below support some narrower release-local assertions, but they do not make the existing row current on the tags page under R-R.

## Provenance and gates

The URL check used `functions.grep` on `corpus/SOURCES.md` with pattern `https://raw.githubusercontent.com/rfjakob/earlyoom/v1\.9\.0/(main\.c|kill\.c|msg\.h|README\.md)|https://raw.githubusercontent.com/rfjakob/earlyoom/v1\.(8|7)/(main\.c|kill\.c)`; matches were lines 120, 123–125. The frozen S117 row at line 123 includes the tag-pinned URLs, so they are **not new sources**. Scratch preparation was `timeout 10s mkdir -p /fast/scratch/hyaku/mori-r33/RepairS117` (no output). The initial and second fetch of every URL below had matching SHA-256 values. Each fetch pair was run under `timeout 120s` with `date -u +%FT%TZ`, `sha256sum`, and `cmp -s`; both recorded fetch times were `2026-10-23T02:40:26Z`.

Exact fetch invocation pattern (each table row substitutes its URL and first filename; second output is `<filename>.second.src`):

```sh
timeout 120s bash -c 'set -e; date -u +%FT%TZ; curl -sSL --fail -m 60 URL -o FILE; sha256sum FILE; date -u +%FT%TZ; curl -sSL --fail -m 60 URL -o FILE.second.src; sha256sum FILE.second.src; cmp -s FILE FILE.second.src && printf "byte-identical\n"'
```

| Page URL | First/second saved copies under `/fast/scratch/hyaku/mori-r33/RepairS117/` | SHA-256 (both copies) | Result |
|---|---|---|---|
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | `main-v1.9.0.src`, `.second.src` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | byte-identical |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | `kill-v1.9.0.src`, `.second.src` | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | byte-identical |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h | `msg-v1.9.0.src`, `.second.src` | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` | byte-identical |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md | `README-v1.9.0.src`, `.second.src` | `23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd` | byte-identical |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/main.c | `main-v1.8.src`, `.second.src` | `9bdc8209af6f68403f1137a3e86e566a0ca137dc1ec5c46a1fdf099151b2834c` | byte-identical |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/kill.c | `kill-v1.8.src`, `.second.src` | `459af5589d6cc092303dcc1e27783557e8a91e2820565a08fc5094bc87054133` | byte-identical |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/main.c | `main-v1.7.src`, `.second.src` | `ceaa208361fa112857e30928a0e727711b9da6e86cebaa2f100bbd3d02113412` | byte-identical |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/kill.c | `kill-v1.7.src`, `.second.src` | `1453cd2a6a48de4bafef6032b40c421e433270fddd1bcc94e85a83d80ec65af8` | byte-identical |

The fetches saved the eight tag-pinned code/document URLs from the frozen row. No tags/releases JSON was fetched for this repair. No tools were installed or updated.

## Clause audit under R-R

Locators below are line numbers in the unchanged first-fetch files named in the artifact table. Quotes are exact excerpts. “Unsupported” means the cited page does not state the whole assertion; comparing separate pages or inferring from absence does not satisfy R-R.

| Atomic assertion from S117 | Page and quote | R-R | Correction disposition |
|---|---|---|---|
| The `mem avail` wording was introduced in v1.8. | v1.8 main.c, `main-v1.8.src:382-383`: `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT` | Unsupported as history: this page states its own print expression, not when the wording originated. | Replace with a v1.8-only output fact (draft row 1). |
| The same wording is unchanged in v1.9.0. | v1.9.0 main.c, `main-v1.9.0.src:414-415`: `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT` | Unsupported as a cross-release comparison: the page states its own expression, not that it is unchanged. | Replace with a v1.9.0-only output fact (draft row 2). |
| v1.8 main.c uses the `mem avail <=` threshold wording. | v1.8 main.c, `main-v1.8.src:382-383`: same quote above. | Supported, narrowly as a v1.8 source-code fact. | Draft row 1. |
| v1.9.0 main.c uses the `mem avail <=` threshold wording. | v1.9.0 main.c, `main-v1.9.0.src:414-415`: same quote above. | Supported, narrowly as a v1.9.0 source-code fact. | Draft row 2. |
| A v1.7 invocation prints `mem <=`. | v1.7 main.c, `main-v1.7.src:326-327`: `fprintf(stderr, "sending SIGTERM when mem <= " PRIPCT " and swap <= " PRIPCT` | Supported as the shown v1.7 source expression. | Draft row 3. |
| A v1.7 invocation never prints the contract's threshold line. | v1.7 main.c line 326 quote above. | Unsupported: the positive line shown does not state the negative/“never” assertion. | Drop the absence claim; retain only the directly quoted v1.7 expression. |
| The action prefix is stable across v1.7, v1.8, v1.9.0. | v1.7 kill.c `:377`: `sending %s to process`; v1.8 kill.c `:539`: same; v1.9.0 kill.c `:627`: same. | Unsupported under R-R as a stability claim; each page states only its own literal. | Use release-local rows 4–6; do not claim stability. |
| The escalation prefix is stable across the three tags. | v1.7 kill.c `:167`: `escalating to SIGKILL after %.1f seconds`; v1.8 kill.c `:230`: `escalating to SIGKILL after %.3f seconds`; v1.9.0 kill.c `:318`: same `.3f` quote. | Unsupported under R-R as a cross-page claim; the individual literals are directly evidenced, but no one page states stability. | Use release-local rows 4–6; do not claim stability. |
| Trailing action fields change across tags. | v1.7 kill.c `:377`: `badness %d, VmRSS %lld MiB`; v1.8 kill.c `:539`: `oom_score %d, VmRSS %lld MiB`; v1.9.0 kill.c `:627`: `oom_score %d, oom_score_adj %d, VmRSS %lld MiB`. | Unsupported as a comparative clause under R-R, despite the release-local quoted strings. | State each release's own format only in rows 4–6. |
| The version line, rather than the action line, identifies the grammar. | v1.9.0 main.c `main-v1.9.0.src:161`: `fprintf(stderr, "earlyoom " VERSION`; action prefix is quoted above. | Unsupported: the page shows a version-print expression and an action literal, not the conclusion that one identifies the grammar. | Drop the grammar-identification claim; optional direct replacement is draft row 7. |
| Percentages use a width-5 format field. | v1.9.0 msg.h, `msg-v1.9.0.src:9-10`: `// printf format for percentages` / `#define PRIPCT "%5.2lf%%"` | Supported as the v1.9.0 macro definition. | Draft row 8. |
| A single-digit threshold is space-padded. | v1.9.0 msg.h, `msg-v1.9.0.src:9-10`: same quote above. | Unsupported under R-R: the quote gives the format string but does not state the padding behavior. | Drop unless a named page explicitly states that behavior. |

## Draft correction rows (IDs left for L1)

Each proposed row below uses one cited code page as its population page and makes only a release-local assertion. The source ID is intentionally not invented.

| Draft | Single population page | Replacement teaches cell |
|---|---|---|
| 1 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/main.c | The v1.8 SIGTERM-threshold print expression uses `mem avail <=` (`main-v1.8.src:382-383`). |
| 2 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | The v1.9.0 SIGTERM-threshold print expression uses `mem avail <=` (`main-v1.9.0.src:414-415`). |
| 3 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/main.c | The v1.7 SIGTERM-threshold print expression uses `mem <=` (`main-v1.7.src:326-327`). |
| 4 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.7/kill.c | The v1.7 action literal starts `sending %s to process`, includes `badness %d, VmRSS %lld MiB`, and the escalation literal uses `%.1f seconds` (`kill-v1.7.src:167,377`). |
| 5 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.8/kill.c | The v1.8 action literal starts `sending %s to process`, includes `oom_score %d, VmRSS %lld MiB`, and the escalation literal uses `%.3f seconds` (`kill-v1.8.src:230,539`). |
| 6 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | The v1.9.0 action literal starts `sending %s to process`, includes `oom_score %d, oom_score_adj %d, VmRSS %lld MiB`, and the escalation literal uses `%.3f seconds` (`kill-v1.9.0.src:318,627`). |
| 7 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | The v1.9.0 source has the stderr print expression `fprintf(stderr, "earlyoom " VERSION` (`main-v1.9.0.src:161`). |
| 8 | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h | The v1.9.0 `PRIPCT` macro is defined as the printf format `"%5.2lf%%"` (`msg-v1.9.0.src:9-10`). |

**Correction paragraph:** Replace S117's combined tag-history and log-grammar teaching with release-local source rows like drafts 1–8, each naming only its population page. Keep the directly quoted `mem avail <=`, `mem <=`, per-release action/escalation literals, version-print expression, and width-5 macro facts. Remove the claims that the wording was introduced or unchanged, that v1.7 never emits another line, that prefixes/fields are stable or change across releases, that a version line identifies grammar, and that a single-digit threshold is space-padded; those are not stated by one cited page under R-R. Therefore the existing S117 row remains not current on its tags-JSON population page alone.

## Surfaces, gates, limits

- Lane write: only this requested report, `.ufo/waves/round-33/w1/RepairS117.md`; fetched bytes are in `/fast/scratch/hyaku/mori-r33/RepairS117/`.
- Read-only evidence: frozen `git show` at `7d382043`; source URL search; eight first/second fetch pairs and SHA comparisons; quote inspection at listed source-copy line locators.
- No edits to product/source/judge files; no Git/JJ writes; no judge/counter, build, or test run; no tools installed. No claim is made that any unrun check passed.
- Known limit: tags/releases JSON and the counter were not fetched/run in this repair; the population-page finding is cited from the round-32 spot-check (`corpus/lessons/round-32-verifier-spotcheck.md:89`), not re-measured here.

## Artifact paths

- Report: `.ufo/waves/round-33/w1/RepairS117.md`
- Evidence copies: `/fast/scratch/hyaku/mori-r33/RepairS117/{main-v1.9.0,kill-v1.9.0,msg-v1.9.0,README-v1.9.0,main-v1.8,kill-v1.8,main-v1.7,kill-v1.7}.src` and matching `.second.src` files.
