# CtlNormaliser — round 32 C0 control: normaliser and quote matching

Seat: MoriR32A2.CtlNormaliser (critic). Counter: the frozen `.ufo/waves/round-32/count-c1.py` (sha256
`cfa0b988a51fc59720382016c0608408c022b9aaedc19f92c24453493d1a84fe`, computed in-session), never edited.
Tools installed or updated: none. pdftotext 26.08.0, curl 8.23.0 and Python 3.14.8 were already on the host.

## 1. Control and the work it skips

This is a mixed probe control of 20 rows. It skips the claimed recheck work: no row is a real recheck, and the
verdicts are not judged. Each row probes one behaviour of `normalise`/`fold`/`quotes_of`
(count-c1.py:80-109) on real population pages:
- 4 rows are fabricated or unsupported quotes, built to test for false accepts.
- 5 rows are honest quotes copied as rendered text, built to test for false rejects.
- 11 rows test escapes, shape, typography, entities and duplicate URLs.

R4 is satisfied by sandbox scaffolding (`ctl-dispatch.json` with seat `CtlJudgeScaffold`, plus a receipt naming the
section sha). This keeps the quote checks isolated. It is not a judgment, and it is the trust limit already
stated in contract.md:63-65.

## 2. Construction

```
mkdir -p /fast/scratch/hyaku/mori-r32/CtlNormaliser
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r32/CtlNormaliser/lane
git -C .../lane checkout -q 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4
# each population URL fetched once: curl -sSL --fail -m 60 (the counter's own flags), ~2026-10-23T01:17Z
# .src copies = those fetched bytes unchanged (except S046: copy = the quote text only)
# corpus/lessons/round-32.md: ## Recheck, header `id | url | accessed | sha256 | quotes | verdict`,
#   20 rows, accessed 2026-10-23T01:00:00Z, verdict current
python3 count-c1.py --section-sha corpus/lessons/round-32.md   # -> 69fa9af4...24cd
# judge/JudgeRecheck.md: judge-role reviewer, judge-seat CtlJudgeScaffold, judged-sha256 as above, 20 agree lines
git -c user.name=ctl -c user.email=ctl@sandbox commit -m 'CONTROL CtlNormaliser: ...'
```

| id | probe | quote cell (abridged) | outcome |
|---|---|---|---|
| S002 | negation cut out of a word | "protected reclaimable memory available, OOM killer is invoked." (page: "un**protected**") | PASS = false accept |
| S051 | the same cut, PDF | "necessary collection and use of SSNs." (page: "eliminate the un**necessary** collection") | PASS = false accept |
| S041 | anchor boilerplate counted as topical | "Category: Standards Track" | PASS = false accept |
| S046 | copy is the quote only | `.src` = 1 line of quote text | PASS = false accept (provenance) |
| S012 | rendered text, `</code>,` | "…method, io.systemd.oom.ReportManagedOOMCGroups, intended…" | FAIL = false reject |
| S128 | rendered text, `</i>.` | "Its value is scaled linearly with oom_score_adj." | FAIL = false reject |
| S015 | rendered text, `</strong></span>.` | "These are additional fields added automatically by systemd-journald." | FAIL = false reject |
| S069 | rendered text, `</code>.` | "When walk_up is false (the default), the path must start with other." | FAIL = false reject |
| S137 | JSON message with `\n` decoded to a space | "kill: option for triggering kernel oom killer As mentioned in issue" | FAIL = false reject |
| S149 / S037 / S073 | the same passages in normalised form (`oom_score_adj .`, `systemd-journald .`, `os.walk() ,`) | duplicate URLs of S128/S015/S069 | PASS (honest) |
| S014 | inner quotes escaped `\"` | `"Members of the groups \" systemd-journal \", \" adm \", and"` | PASS (honest) |
| S001 | pipe escaped `\|` | `"… The following format is used: <some\|full> <stall amount in us>"` | PASS (honest) |
| S052 | entity in the cell | `"… it&rsquo;s crucial to be mindful of sensitive data handling."` | PASS (honest) |
| S007 | em dash typed in the quote; the normalised page has `-` | "systemd-oomd.service, systemd-oomd — A userspace out-of-memory (OOM) killer" | PASS (honest) |
| S076 | plain prose (duplicate URL of S067) | "The purpose of characterization testing is to document … system had." | PASS (honest) |
| S071 | typographic delimiters “…” | 0 quotes found | FAIL (quote_shape) |
| S074 | 4 honest quotes | — | FAIL (quote_shape, by design) |
| S067 | 2-word quote "Characterization Testing" | — | FAIL (quote_shape, by design) |

## 3. Sandbox

Path `/fast/scratch/hyaku/mori-r32/CtlNormaliser/lane`, commit `a5dee63f9d70a0e88fb3f5f2cb558202ed1cfb23`
(parent 29f7d04, committed 2026-10-22T22:23:11-03:00, 23 files). Function-level reproducer:
`/fast/scratch/hyaku/mori-r32/CtlNormaliser/repro.py`. It imports the frozen counter read-only.

## 4. Counter output (live, verbatim)

`timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py a5dee63f9d70a0e88fb3f5f2cb558202ed1cfb23 --repo /fast/scratch/hyaku/mori-r32/CtlNormaliser/lane`
```
revision=a5dee63f9d70a0e88fb3f5f2cb558202ed1cfb23 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=20 header_ok=True section_sha256=69fa9af433002828 judge_ok=True judge_seat_ok=True judge_agree=20
rows_ok=12/34 verdicts={'current': 20}
row_failures=S012:quote_not_in_copy,live_quote S015:quote_not_in_copy,live_quote S031:rows=0 S039:rows=0 S040:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S047:rows=0 S049:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:quote_shape S068:rows=0 S069:quote_not_in_copy,live_quote S071:quote_shape,quote_off_topic S074:quote_shape S117:rows=0 S128:quote_not_in_copy,live_quote S137:quote_not_in_copy,live_quote
new_ok=0 new_failures=none
C1=unmet exit=1
exit=1
```
The earlier `--no-live` run of the same commit gave the same rows_ok=12/34. Its output was
`C1=diagnostic exit=1 (live check R3 skipped)`, and it does not count.

## 5. Verdict

The control is unmet as expected. C1 was never met: there are only 20 rows and no S175+ source. However, 4 of
the 12 passing rows are false accepts that would count toward rows_ok=34/34 if a seat used them. These are
S002, S051, S041 and S046. 5 honest rendered-text quotes are false rejects: S012, S015, S069, S128 and S137. The
escapes `\"` and `\|`, entities in the cell, NBSP, curly and em-dash folding, script-block exclusion and
duplicate-URL rows all behave correctly.

## 6. Counter weaknesses, with reproducers

**W1 — false accept: meaning can be flipped by cutting a word (impacted: freshness/C1 correctness).** The check
is `q in ntext` and `all(q in normalise(b) …)` (count-c1.py:248, :254, and :307 for the gate). That is a plain
substring test with no word boundary, so a quote may start mid-word.
- Sandbox: S002 and S051 pass live, so rows_ok includes both.
- repro.py prints `substring mid-word (unprotected) … -> PASS`.
- 16 distinct candidates (23 hits) exist on population pages (searched with `\b(un|non-?|in|im|ir|dis)` + stem, with ≥2
  topical tokens). For example, S012 "privileged users can terminate arbitrary processes" (the page says
  "unprivileged"), and S062 "compatible with this specification".

Smallest fix, pre-data: match on word boundaries, e.g. `re.search(r'(?<!\w)'+re.escape(q)+r'(?!\w)', text)` at
the three sites. Without that fix, the judge must check that every quote starts and ends on a whole word.

**W2 — false reject: tag-to-space turns rendered text into a different string (impacted: honest-data miss
risk).** `re.sub('<[^>]*>', ' ', …)` (count-c1.py:102) puts a space wherever a tag closes before
punctuation or mid-token. Examples of rendered text against what the counter compares:
- `pipe(2),` becomes `pipe(2) ,`
- `testing.` becomes `testing .`
- `/proc/<i>pid</i>/oom_score_adj` becomes `/proc/ pid /oom_score_adj`

Sandbox: S012, S015, S069 and S128 fail both copy and live. The normalised forms pass (S037, S073, S149).

My measurement (`/fast/scratch/hyaku/mori-r32/CtlNormaliser/rates.py`, re-run with identical numbers): rendered
text from html.parser with inline tags joined, compared against `normalise()` of the same bytes, on sentences of
3–25 words sharing ≥2 tokens with the row. The share of those topical sentences that the counter rejects:

| rows | rejected |
|---|---|
| S012 | 46% (17/37) |
| S128, S149 | 44% |
| S068 | 42% |
| S037 | 38% |
| S069 | 35% |
| S015 | 32% |
| S073 | 30% |
| S007, S062 | 25% |
| S058 | 21% |
| S001 | 20% |

Five quotes recorded verbatim in earlier anchors all pass live: S039, S040, S049, S051 ×2. Fix: no counter change
is needed.
Data seats must copy quotes from `normalise(<copy>)` output and dry-run `count-c1.py <rev> --no-live` before
handing in (see guidance).

**W3 — off-topic quotes pass the token test (impacted: calibration of R2).**
`tokens(teaches+anchor+scope)` (count-c1.py:250) counts provenance and section words from the anchor, such as
`standards track`, `opened`, `last updated`, `operation modes` and `kernel documentation`. So page furniture
passes: S041 "Category: Standards Track" passes live, with tokens {category, standards, track}. 13 of the 14 rows
searched had such a 4-word window, for example S046 "SYNOPSIS DESCRIPTION OPERATION MODES" and S064
"git-rev-parse last updated". Fix:
the judge rejects such quotes; on the counter side, build the reference from teaches + scope only (a tradeoff that
needs no data).

**W4 — the copy is never shown to be the fetched page (impacted: false provenance).** R2 only needs the quotes
inside `normalise(copy)`. A one-line `.src` holding only the quote passes copy_sha, the copy check and R3: S046
passes live. Fix: the judge opens each `.src`; on the counter side, require the copy's mode (pdf/html/raw) to
match the live bytes and the copy's normalised length to be comparable to the live page's.

**W5 — narrower false-reject traps** (all from repro.py; "found" is the counter's own test):
- Legacy entities without a semicolon are decoded inside the quote cell. `&notify` becomes `¬ify` and `&regs`
  becomes `®s`, so both fail. Write `&amp;notify`.
- A page with no `<html`/`<!doctype` in its first 4 KiB falls back to raw text (count-c1.py:98-99). Entity and
  inline-tag quotes then fail, and a quote found only inside a `<script>` passes the copy check. R3 still
  rejects it, because every live population page is detected as HTML: 25 HTML URLs, S051 PDF, S117/S137 JSON in raw
  mode, and S056 not fetched.
- U+200B (on S043, S046, S058 and S064) and U+2010 (on S049 and S062) occur on population pages and are not folded.
  U+00AD (synthetic only) is not folded either. Retyping fails; copying the characters works.
- PDF line-end hyphens: pdftotext -layout has 11 of them in S051. "technical and non-technical personnel" fails,
  and the normalised form "non- technical" passes.
- JSON (S117/S137) is raw. A quote across `\n` must contain a literal `\n`: the S137 commit message passes with
  `killer\n\nAs mentioned` and fails with a space. No cell form can match a JSON-escaped inner `\"`; all three
  forms tried fail.
- NFKC can change meaning: `10²` becomes `102`, so "of 102 seconds" passes (synthetic; no population HTML page
  carries superscripts).

**W6 — environment risks to the live count (not normaliser defects).**
- S056 (pnas.org) returns HTTP 403 to the counter's curl (`curl: (22) … 403`). A `current` row there can never
  pass R3.
- The api.github.com unauthenticated budget read `remaining 32 of 60` (`/rate_limit`, ~01:17Z). Each live run
  costs 1–3 calls per S117/S137 row, and 3 when a quote misses. An exhausted budget fails honest S117/S137 rows.
  It would also let an `unreachable` row pass, because R3 only needs 3 counter fetch failures and the content of
  `.fetch.txt` is never read.
- S041 and S062 redirect to `/info/rfcNNNN/`. That page still holds the RFC text, e.g. "The 429 status code
  indicates…" is found.

## Guidance for data seats (no counter change)

1. Choose each quote from the counter's own text:
   `python3 -c "import importlib.util as u;s=u.spec_from_file_location('c','.ufo/waves/round-32/count-c1.py');c=u.module_from_spec(s);s.loader.exec_module(c);print(c.normalise(open('corpus/evidence/recheck-r32/SNNN.src','rb').read()))"`.
   Copy a span verbatim, including spaces such as `oom_score_adj .`. Then run `count-c1.py <rev> --no-live`.
2. Use ASCII `"` delimiters, never “ ”. Escape an inner `"` as `\"` and a `|` as `\|`. Give 1–3 quotes of 3–25
   words, and start and end each on a whole word.
3. Avoid passages that cross JSON `\"`, PDF line-end hyphens or `&`+letters. Copy rather than retype U+200B and
   U+2010.
4. S056 can only honestly be `unreachable` if the seat's own `curl -sSL --fail` also fails. Save api.github.com
   calls for the final count.

Hygiene note: `.ufo/waves/round-32/__pycache__/count-c1.cpython-314.pyc` exists in the lane, with mtime
22:13:31 -03:00. It predates my first import (~22:16:50), so I did not create it and left it untouched. Apart from
this report, I wrote nothing in the lane.
