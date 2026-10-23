measured 2026-10-23T12:05:50Z

# SupS064 — S064 append-only repair draft

Axes: source fidelity; immutable-row compliance; provenance.

VERDICT: supported

## Finding and provenance

Round-35 routed S064 as a real-content immutable-cell edit: its first-published commit is `367927c5`; scope gained a `lane rule` label and teaches was re-attributed and re-punctuated (`.ufo/waves/round-35/w2/ScoutAppendDebt.md:29`). The round-35 finding records that this was logged in round 33 (`ScoutAppendDebt.md:29`).

- `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 367927c5:corpus/SOURCES.md` returned the first-published S064 row: scope excluded remote publication/source authenticity/input-tree equality without a lane-rule label; teaches combined commit resolution with the subsequent byte-binding rule.
- `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:corpus/SOURCES.md` returned the tip row. Its scope and teaches explicitly mark the non-source attribution as a lane rule. Tip status is `mined`, recheck is `on-release`, and used-by includes `corpus/lessons/round-19.md`.
- `timeout 120s git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 6bd57097:corpus/lessons/round-19.md && printf 'PATH_PRESENT at 6bd57097\\n'` → `PATH_PRESENT at 6bd57097` (exit 0).

## Reopened source and decision

Reopened the tip source URL directly: `https://git-scm.com/docs/git-rev-parse`. Command: `timeout 100s curl -L --max-time 90s -sS -o /fast/scratch/hyaku/mori-r36/SupS064/S064.src -w 'HTTP_STATUS=%{http_code}\\n' https://git-scm.com/docs/git-rev-parse` → `HTTP_STATUS=200`. `timeout 120s sha256sum /fast/scratch/hyaku/mori-r36/SupS064/S064.src` → `64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421`; `wc -c` → `122463` bytes.

Located quotes from the saved response (quotes are contiguous, at most 25 words, and retain HTML source line locations):

- OPTIONS `--verify`: `Verify that exactly one parameter is provided` — `S064.src:2720`.
- OPTIONS `--end-of-options`: `wise to use --end-of-options so that the name argument is not mistaken for another option` — `S064.src:2736-2737`.
- OPTIONS commit peeling: `names an existing object that is a commit-ish (i.e. a commit, or an annotated tag that points at a commit)` — `S064.src:2729-2730`.
- EXAMPLES commit object name from REV: `Print the commit object name from the revision in the $REV shell variable` — `S064.src:3763`.
- Page version/date: `git-rev-parse last updated in 2.56.0` — `S064.src:1330`; `2026-09-28` — `S064.src:1363`.

The source supports selector verification, commit peeling and the example output. The scope exclusions and the later rule to retain an object ID and bind loaded bytes are clearly labeled `lane rule` in the tip row; the source does not purport to establish publication, authenticity or byte-to-tree binding. The reopened bytes do not falsify the tip cells. No claim is made that Git documentation independently proves those lane rules.

## Drafts for L1

DRAFT corpus/SOURCES.md
```text
| S2NN | git-rev-parse(1) — https://git-scm.com/docs/git-rev-parse | docs | A | C2 resolving an explicit selector to an existing commit object; lane rule: not remote publication, source authenticity or input-tree equality | OPTIONS --verify, --end-of-options and commit type peeling; EXAMPLES commit object name from REV; page last updated 2.56.0, 2026-09-28; opened 2026-10-23 | supersedes S064 — Resolve a selector with --verify --end-of-options and commit peeling; lane rule: do it once, retain the full object id, then separately bind the actual loaded register/correction bytes to blobs at that commit; a hash printer alone does not prove the latter. | mined | 2026-10-23 | on-release | corpus/lessons/round-19.md |
```

DRAFT corpus/lessons/round-36.md Gate line
```text
| S2NN | https://git-scm.com/docs/git-rev-parse | 2026-10-23 | sha256 64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421; supported. OPTIONS --verify: Verify that exactly one parameter is provided (S064.src:2720); --end-of-options: wise to use --end-of-options so that the name argument is not mistaken for another option (S064.src:2736-2737); commit peeling: names an existing object that is a commit-ish (i.e. a commit, or an annotated tag that points at a commit) (S064.src:2729-2730); EXAMPLES: Print the commit object name from the revision in the $REV shell variable (S064.src:3763); page updated: git-rev-parse last updated in 2.56.0 (S064.src:1330), 2026-09-28 (S064.src:1363). |
```

## Surfaces and limits

- Lane write: this report only, `.ufo/waves/round-36/w1/SupS064.md`. Scratch source: `/fast/scratch/hyaku/mori-r36/SupS064/S064.src`, SHA-256 above. No product file, registry, Git index, or other lane file was changed.
- Checks performed: source URL reopened (HTTP 200), quote/locator review against saved bytes, and used-by path existence at the named tip. No build, tests, append-only checker, or broader registry review was run.
- No tool was installed or updated.
