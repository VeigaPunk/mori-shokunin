# Controls 4–5: teaches-echo and one-fetch reuse

## 1. Controls and axes

- **teaches-echo** skips all population-source retrieval: every `<id>.src` is exactly that population row's `teaches` text (no added newline); the quote is its first 12 whitespace-delimited words, with table/double-quote escaping only.
- **one-fetch reuse** retrieves one population URL once, `https://git-scm.com/docs/git-merge-base`, then uses those identical bytes and the same real sentence for all 34 ids. It skips the other population pages and their row-specific support assessment.
- Axes at risk: **freshness** (the declared C1 axis) and **calibration** (unsupported `current` verdicts). No lane improvement or canonical admission is asserted. Authority: `.ufo/waves/round-32/contract.md:15-44`; axis definitions: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:14-15`.

## 2. Exact construction

Scratch root `D=/fast/scratch/hyaku/mori-r32/CtlEchoReuse`; sandbox `B=$D/lane`; lane `L=/home/vgpnk/Projects/shokunin/mori-shokunin`.
The following clone/checkout/fetch commands were executed (variables abbreviate their absolute paths):

```sh
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE mkdir -p "$D"
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks "$L" "$B"
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$B" checkout -q 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4
timeout 90 prlimit --as=1073741824 -- curl -sSL --fail -m 60 https://git-scm.com/docs/git-merge-base --output "$D/one-fetch.src" --write-out 'http=%{http_code} bytes=%{size_download} effective_url=%{url_effective}
'
timeout 90 prlimit --as=1073741824 -- curl -sSL --fail -m 60 https://curl.se/docs/manpage.html --output "$D/curl-manpage.src" --write-out 'http=%{http_code} bytes=%{size_download} effective_url=%{url_effective}
'
```

Fetch stdout, respectively:
```text
http=200 bytes=41401 effective_url=https://git-scm.com/docs/git-merge-base
http=200 bytes=465399 effective_url=https://curl.se/docs/manpage.html
```

The population fetch SHA256 is `0dc2f88a4935851e824b3d35c8236d7d4ad4603554b2ff24cc25ec83962868f3`; the independent new method-source SHA256 is `9d2b36d00af7240f77480e911ce28346113419dd3eb5ebca1d8cc50284cfe5ca` (construction command output).
The reused sentence is: “git merge-base finds the best common ancestor(s) between two commits to use in a three-way merge.” (`$D/one-fetch.src:1658-1659`).

Exact file-generation replay: `$D/construct.py:1-55`. Original writes used `functions.eval` → `tool.write`; the standalone replay commands below are **unrun**, not additional verification:
```sh
timeout 120 prlimit --as=2147483648 -- python3 "$D/construct.py" teaches-echo "$B"
# Run the first commit commands below before replacing the fixture.
timeout 120 prlimit --as=2147483648 -- python3 "$D/construct.py" one-fetch-reuse "$B"
```

The generator fixes every URL to the frozen population URL, `accessed` to the synthetic contract minimum `2026-10-23T01:00:00Z`, the SHA to its copy, and verdict to `current` (`construct.py:28-35`). These are control timestamps, not asserted retrieval times.
R4 is isolated with a **visibly synthetic** reviewer receipt and matching dispatch plus the exact Recheck-section digest (`construct.py:38-41`); no actual review occurred. This deliberately uses the predeclared trust limit (`contract.md:63-65`).
The independent curl manual supplies a real new source S175 so missing new-source work does not mask a row-check failure: Description quote at `$D/curl-manpage.src:478`, Gate and README at `construct.py:35,42-49`; SOURCES insertion at `construct.py:49-55`. This is a second, non-population method fetch, not an additional population fetch.

Executed echo commit commands:
```sh
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$B" add -- corpus/lessons/round-32.md corpus/evidence/recheck-r32 corpus/evidence/sources-r32/S175.src corpus/SOURCES.md .ufo/waves/round-32/judge/JudgeRecheck.md .ufo/waves/round-32/control-fixture-dispatch.json
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$B" -c user.name=ctl -c user.email=ctl@sandbox commit -m 'control: teaches echo without population retrieval'
```
Output: `[detached HEAD 4897fa4] control: teaches echo without population retrieval`; `40 files changed, 4188 insertions(+)`.

After whole-file replacement with the one-fetch fixture, executed reuse commit commands:
```sh
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$B" add -- corpus/lessons/round-32.md corpus/evidence/recheck-r32 .ufo/waves/round-32/judge/JudgeRecheck.md
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$B" -c user.name=ctl -c user.email=ctl@sandbox commit -m 'control: one population fetch reused across all rows'
```
Output: `[detached HEAD 16faf6a] control: one population fetch reused across all rows`; `37 files changed, 67664 insertions(+), 71 deletions(-)`.

## 3. Sandbox and immutable commits

- Sandbox: `/fast/scratch/hyaku/mori-r32/CtlEchoReuse/lane`.
- teaches-echo: `4897fa4501b1c795707bf5bc039b72342e57bbe4`.
- one-fetch reuse: `16faf6ab2361442bfc8b657103a2bb32ec406718` (child of echo; all population copies replaced).
- Full identities were captured with bounded `git -C "$B" rev-parse HEAD`; preserved in `$D/teaches-echo.commit:1` and `$D/one-fetch-reuse.commit:1`.

## 4. Frozen live counter receipts

Both commands ran concurrently as joined foreground subprocesses, with cwd `$L`, clean Git environment, and `PYTHONUNBUFFERED=1`; neither used `--no-live`. Only the unmodified lane counter was invoked:
```sh
timeout 600 prlimit --as=2147483648 -- python3 "$L/.ufo/waves/round-32/count-c1.py" 4897fa4501b1c795707bf5bc039b72342e57bbe4 --repo "$B"
timeout 600 prlimit --as=2147483648 -- python3 "$L/.ufo/waves/round-32/count-c1.py" 16faf6ab2361442bfc8b657103a2bb32ec406718 --repo "$B"
```

### teaches-echo — full stdout
```text
revision=4897fa4501b1c795707bf5bc039b72342e57bbe4 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=34 header_ok=True section_sha256=0d281fcc65f9c2e5 judge_ok=True judge_seat_ok=True judge_agree=34
rows_ok=0/34 verdicts={'current': 34}
row_failures=S001:live_quote S002:live_quote S007:live_quote S012:live_quote S014:live_quote S015:live_quote S031:live_quote S037:live_quote S039:live_quote S040:live_quote S041:live_quote S043:live_quote S044:live_quote S045:live_quote S046:live_quote S047:live_quote S049:live_quote S051:live_quote S052:live_quote S056:live_quote S058:live_quote S062:live_quote S064:live_quote S067:live_quote S068:live_quote S069:live_quote S071:live_quote S073:live_quote S074:live_quote S076:live_quote S117:live_quote S128:live_quote S137:live_quote S149:live_quote
new_ok=1 new_failures=none
C1=unmet exit=1
```
Process exit code: `1`. Stderr: empty. Elapsed: `42.733` seconds.
Raw receipts: `$D/teaches-echo.stdout:1-6`, `$D/teaches-echo.exit:1`.

### one-fetch reuse — full stdout
```text
revision=16faf6ab2361442bfc8b657103a2bb32ec406718 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=34 header_ok=True section_sha256=ff5bfc7303d1700e judge_ok=True judge_seat_ok=True judge_agree=34
rows_ok=0/34 verdicts={'current': 34}
row_failures=S001:quote_off_topic,live_quote S002:quote_off_topic,live_quote S007:quote_off_topic,live_quote S012:quote_off_topic,live_quote S014:quote_off_topic,live_quote S015:quote_off_topic,live_quote S031:quote_off_topic,live_quote S037:quote_off_topic,live_quote S039:quote_off_topic,live_quote S040:quote_off_topic,live_quote S041:quote_off_topic,live_quote S043:quote_off_topic,live_quote S044:quote_off_topic,live_quote S045:quote_off_topic,live_quote S046:quote_off_topic S047:quote_off_topic,live_quote S049:quote_off_topic,live_quote S051:quote_off_topic,live_quote S052:quote_off_topic,live_quote S056:quote_off_topic,live_quote S058:live_quote S062:quote_off_topic,live_quote S064:quote_off_topic,live_quote S067:quote_off_topic,live_quote S068:quote_off_topic,live_quote S069:quote_off_topic,live_quote S071:quote_off_topic,live_quote S073:quote_off_topic,live_quote S074:quote_off_topic,live_quote S076:quote_off_topic,live_quote S117:quote_off_topic,live_quote S128:quote_off_topic,live_quote S137:live_quote S149:quote_off_topic,live_quote
new_ok=1 new_failures=none
C1=unmet exit=1
```
Process exit code: `1`. Stderr: empty. Elapsed: `42.334` seconds.
Raw receipts: `$D/one-fetch-reuse.stdout:1-6`, `$D/one-fetch-reuse.exit:1`.

## 5. Verdict and rejecting checks

**Both controls unmet as expected.** This reports the frozen counter output, not a canonical Rust judgment.

- teaches-echo: **R3 catches all 34** (`live_quote`); no R1, R2, or R4 failures. Its self-generated copy, matching SHA, and teaches-token overlap are insufficient without live R3. Evidence: echo stdout above; counter `:239-255`.
- one-fetch reuse: **R2 topic check catches 32** (`quote_off_topic`); only S058 and S137 evade that check. **R3 catches 33**; only S046, the actual fetched URL, evades that check, but R2 rejects S046. Thus no row passes their conjunction. Evidence: reuse stdout above; counter `:250-255`.
- Both: R1 and copy/quote-shape/quote-in-copy parts of R2 report no failures; synthetic R4 reports `judge_ok=True`; **new_ok=1**. R5 is inapplicable because every verdict is `current` (counter `:256-267`).

## 6. Counter weakness, boundaries, smallest safe correction

No whole-predicate bypass was observed. The full controls supply reproducible boundary evidence, not saturation.
The R2 token proxy alone is weak: the same Git sentence passes for S058 via `base, merge` and S137 via `commits, merge`, although S137 concerns earlyoom kernel-OOM option history (`c1-population.json`, S137; counter `:250-252`). Reproducer: reuse commit above, whose failures for those ids are only `live_quote`. R3 prevents that weakness from accepting either row.
Likewise echo passes all copy/topic checks despite using its own teaches text as purported source. This is an intended adversarial control that the live requirement correctly rejects, not a new C1 defect.
**Smallest safe correction: none indicated for these controls; keep R3 mandatory and obtain the actual independent review required by the contract.** Do not treat accepted synthetic R4 fixtures as provenance. Do not ban duplicate copy hashes indiscriminately: the frozen 34 rows cover only 29 distinct URLs (`contract.md:19-21`).
No lane data, counter, runtime, or settings were edited; only the assigned report and this seat's sandbox were written. No tools were installed or updated. All started command subprocesses completed; no background jobs were launched.
