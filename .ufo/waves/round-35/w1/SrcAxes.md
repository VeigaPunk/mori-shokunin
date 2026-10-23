measured 2026-10-23T08:51:49Z

# S199 frontier source finding

VERDICT: admit

## Behavior and findings

- `git ls-remote https://github.com/VeigaPunk/kimi-shokunin` reported `b47dfbe2cd185e33f9aa42a66a9e6c63c9591d5b` for both `HEAD` and `refs/heads/main`; fetched `skills/shokunin/protocol/AXES.md` from that pinned raw URL successfully. (Command: `timeout 120 git ls-remote https://github.com/VeigaPunk/kimi-shokunin`; output: `b47dfbe2cd185e33f9aa42a66a9e6c63c9591d5b HEAD`, same hash for `refs/heads/main`; URL below.)
- Saved fetched bytes to `/fast/scratch/hyaku/mori-r35/SrcAxes/AXES.src`; `sha256sum` output was `04ea5c9e89c91cef645536ab56863ebb014dce617e7083e54968092968a7d993`. (Command: `sha256sum /fast/scratch/hyaku/mori-r35/SrcAxes/AXES.src`.)
- Compared the fetched bytes with `/home/vgpnk/Projects/shokunin/AXES.md`; `cmp` reported `identical`. They do not differ. (Command: `cmp -s ...`; output: `identical`.)
- The source says SCORECARD carries capabilities separately and that rows enter through a round demonstrating the capability running; a passing demonstration is required to avoid pre-claiming. (`AXES.src:60-64`; pinned URL below.) Its calibration definition is honest gap/confidence/overreach self-assessment, with SCORECARD entries matching observed repository state. (`AXES.src:15`.)
- The lane registry ends at S198 before `## Paths`, so S199 is the next unused ID observed. (`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md:204-206`.) The registry requires 11 columns and defines tier, scope, anchor, teaches, status, opened, recheck and used-by. (`/home/vgpnk/Projects/shokunin/CORPUS.md:86-108`.)

## DRAFT SOURCES S199

```text
DRAFT SOURCES S199
| S199 | Shokunin Expertise Axes — https://raw.githubusercontent.com/VeigaPunk/kimi-shokunin/b47dfbe2cd185e33f9aa42a66a9e6c63c9591d5b/skills/shokunin/protocol/AXES.md | spec | A | which capability rows a lane's SCORECARD may hold, and what calibration measures | Capabilities:62-64; The six axes:15; commit b47dfbe2cd185e33f9aa42a66a9e6c63c9591d5b | A SCORECARD capabilities row needs a running round-report demonstration; calibration checks honest self-assessment against observed repo state. | mined | 2026-10-23 | on-release | SCORECARD.md |
```

## DRAFT Gate S199

```text
DRAFT Gate S199
URL: https://raw.githubusercontent.com/VeigaPunk/kimi-shokunin/b47dfbe2cd185e33f9aa42a66a9e6c63c9591d5b/skills/shokunin/protocol/AXES.md
Access date: 2026-10-23 (date command output: 2026-10-23T08:51:49Z)
Quote (23 words): Rows enter only through a round that demonstrates the capability running; a capability without a passing demonstration in the round report is pre-claiming — AXES.src:62-63
Quote (9 words): Self-assessment quality: gaps named honestly, confidence graded, overreach caught — AXES.src:15
SHA-256: 04ea5c9e89c91cef645536ab56863ebb014dce617e7083e54968092968a7d993 (sha256sum output for /fast/scratch/hyaku/mori-r35/SrcAxes/AXES.src)
```

The source-row gate calls for opening a source in the round and recording its URL, access date, and a located quote of at most 25 words grounding `teaches`. (`/home/vgpnk/Projects/shokunin/CORPUS.md:112-115`.) The two quotes above are contiguous and under 25 words each. `VERDICT: admit` because the pinned protocol source was opened, hashed, and matched to the local AXES file; its content directly supports the drafted scope. (Raw URL and commands above; `AXES.src:15,62-64`.)

## Gates, touched surfaces, and limits

- Touched surfaces: this report and `/fast/scratch/hyaku/mori-r35/SrcAxes/AXES.src` (download and digest above). No product/source registry files were edited.
- Gates exercised: remote ref listing, pinned raw fetch, SHA-256, and byte comparison; outputs are recorded above. No installation or update was performed.
- Out of scope: no broader SCORECARD/C1 audit, round-34 repair audit, tests, commits, or publication was performed.

## Artifact paths

- Report: `.ufo/waves/round-35/w1/SrcAxes.md`
- Fetched source: `/fast/scratch/hyaku/mori-r35/SrcAxes/AXES.src`
