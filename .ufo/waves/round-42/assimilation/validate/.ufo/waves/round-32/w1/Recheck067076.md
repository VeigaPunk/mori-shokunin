# C1 recheck — S067, S076 (feathers characterization testing)

Seat `MoriR32A2.Recheck067076`, wave 1. Both ids share one URL. Verdict for both: **current**, no drift, no redirect.

## 1. Fetch facts

Command (one shell line, first try succeeded, exit 0):
`curl -sSL --fail -m 60 https://michaelfeathers.silvrback.com/characterization-testing -o /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck067076/S067.src`
then `date -u +%FT%TZ` in the same command. curl reported `HTTP=200 URL=https://michaelfeathers.silvrback.com/characterization-testing SIZE=36970`
— `%{url_effective}` equals the population url, so **no redirect**.

| id | url | accessed | bytes | sha256 | scratch copy |
|---|---|---|---|---|---|
| S067 copy | https://michaelfeathers.silvrback.com/characterization-testing | 2026-10-23T01:31:23Z | 36970 | 5d706e27809602eeeb566fd8baf0a569d7f42adc985f9d4f13a18b4dae70de16 | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck067076/S067.src |
| S076 copy | https://michaelfeathers.silvrback.com/characterization-testing | 2026-10-23T01:31:23Z | 36970 | 5d706e27809602eeeb566fd8baf0a569d7f42adc985f9d4f13a18b4dae70de16 | /fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck067076/S076.src |

Both `.src` files are the full fetched page (36970 bytes, one copy per id, identical bytes as the rules allow).
Normalised text (`seat-check.py text S067.src`) is 6589 chars; dumps kept at `S067.text` / `S067.wrap.txt`.
Integrator action (outside this seat's write bounds): copy the two `.src` files unchanged to
`corpus/evidence/recheck-r32/S067.src` and `corpus/evidence/recheck-r32/S076.src`; the committed sha must be
`5d706e27…de16`, **not** the round-20 copy's raw sha (that copy differs only in CSRF tokens, §5).

## 2. Ready-to-paste rows

```
| S067 | https://michaelfeathers.silvrback.com/characterization-testing | 2026-10-23T01:31:23Z | 5d706e27809602eeeb566fd8baf0a569d7f42adc985f9d4f13a18b4dae70de16 | "The purpose of characterization testing is to document your system's actual behavior, not check for the behavior you wish your system had."; "We can see them as descriptions of what we have rather than statements of correctness." | current |
| S076 | https://michaelfeathers.silvrback.com/characterization-testing | 2026-10-23T01:31:23Z | 5d706e27809602eeeb566fd8baf0a569d7f42adc985f9d4f13a18b4dae70de16 | "The purpose of characterization testing is to document your system's actual behavior, not check for the behavior you wish your system had."; "This is particularly useful when we want to refactor or rewrite. We can run our tests and find out immediately whether we've changed behavior." | current |
```

Both lines were re-parsed with the frozen counter's own `cells()` / `quotes_of()`: 6 cells each, accessed matches
`\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ`, sha is 64 hex, 2 quotes each, every quote inside the normalised copy.

## 3. Quote → teaches cell

Anchor check (both rows): the HTML paragraph that begins "It's a trick question" runs from `<p>` at byte 22167 to
`</p>` at byte 22870 of `S067.src`; its last sentence is exactly quote 1 (`corpus/SOURCES.md:73,82` locate the
passage the same way; `corpus/lessons/round-20.md:46,52` record the same sentence from the round-20 open).

**S067** — teaches: "A behavioral baseline documents actual behavior, not desired behavior: a re-pinned census
baseline certifies sameness since the pin, never health."
- Q1 "The purpose of characterization testing is to document your system's actual behavior, not check for the
  behavior you wish your system had." bears directly on the first clause: the essay distinguishes documenting actual
  behavior from checking wished-for behavior; it is the paragraph-final sentence the anchor names.
- Q2 "We can see them as descriptions of what we have rather than statements of correctness." bears on the second
  clause: the page frames such tests as descriptions of what a system *has* (sameness) rather than statements of
  correctness (health). The page never mentions a census or a re-pin; per `corpus/lessons/round-20.md:52` and S076 the
  census-baseline instantiation is the lane's own application, so `current` is claimed only for the source claim the
  page still makes, and the row's application clause is not attributed to the page.
- Verdict `current`: the live page still carries both sentences verbatim.

**S076** — teaches: "supersedes S067 — a characterization test documents actual behavior, not desired behavior.
Reading a re-pinned census baseline as sameness-since-pin rather than health is the lane's own application, not
taught here."
- Q1 (same sentence) bears on "documents actual behavior, not desired behavior"; it is the anchor sentence.
- Q2 "This is particularly useful when we want to refactor or rewrite. We can run our tests and find out immediately
  whether we've changed behavior." bears on the same cell from the change-detection side: the test's job is to show
  whether behavior changed, which is exactly the sameness-since-pin reading the row says is the lane's application;
  the page contains no census/baseline language, so "not taught here" holds.
- Verdict `current`: the page still teaches the actual-not-desired claim and still does not teach the census
  application.

## 4. seat-check output (verbatim)

```
--- S067 ---
sha256=5d706e27809602eeeb566fd8baf0a569d7f42adc985f9d4f13a18b4dae70de16
quotes=2 words=[22, 15] in_copy=[True, True]
shared_tokens=['actual', 'behavior', 'characterization', 'testing'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
EXIT67=0
--- S076 ---
sha256=5d706e27809602eeeb566fd8baf0a569d7f42adc985f9d4f13a18b4dae70de16
quotes=2 words=[22, 24] in_copy=[True, True]
shared_tokens=['actual', 'behavior', 'characterization', 'testing'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
EXIT76=0
```

(`live_quotes_ok=True` means the counter's own live re-fetch also contains every quote.)

## 5. Drift details

No drift, so no `Round32` corrections are drafted; the used-by files (`corpus/knowledge/drift-repin-r20.md`,
`corpus/lessons/round-20.md`, `SKILL.md`) need no change this round.

Evidence the page text is unmoved since 2026-10-21: `.ufo/waves/round-20/falsify/ReopenS072/s067.html` (36970 bytes,
raw sha256 `628bb3ea…69adb`) differs from today's copy in **three raw lines only**, all per-request
CSRF/authenticity tokens in `<meta name="csrf-token">` and the two search forms (`diff -u` = 29 lines, `raw.diff`
kept in scratch). Normalised text is byte-identical: both copies hash to
`9d07a69614bf62eb8f838e8362dbd83afa78073b7d24eb49375c2a785529873d` under `seat-check.py text`. That is why the raw
shas differ while the article is unchanged.

## 6. Notes

- No installation or update was needed this run; nothing installed.
- Bounds observed: wrote only this report and `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck067076/`; no git/jj
  writes in the lane or fleet repo; every command timeboxed; no background jobs left running; no messages sent.
- Remaining unknowns: none material. The one open judgement (already settled in the corpus) is that S067's second
  clause is the lane's application rather than the essay's teaching — `corpus/lessons/round-20.md:52` records that
  supersession, and S076 carries the corrected reading, so S067 stays `current` on the text the page actually has.
