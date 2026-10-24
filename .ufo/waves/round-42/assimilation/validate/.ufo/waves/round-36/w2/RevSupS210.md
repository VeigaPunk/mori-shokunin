measured 2026-10-23T18:52:09Z

# RevSupS210 — re-open S210 (git-rev-parse docs): row + copy

Seat: `mori-r36-w2-RevSupS210-23` (leaf; no subagents). Target: re-open S210 at
`corpus/SOURCES.md:216` (tip `bf0df77fee4b6ef54a90aea09335c7617f125151`, confirmed
`git -C mori-shokunin rev-parse HEAD` → `bf0df77fee4b6ef54a90aea09335c7617f125151`).
Attack axes: (1) teaches-cell language at the options anchor; (2) copy sha256-equality;
(3) lane-rule consistency with corpus usage (`lessons/round-19.md`).

Scratch: `/fast/scratch/hyaku/mori-r36/RevSupS210/`. No tools installed or upgraded
(host already had `curl` 8.23.0 / OpenSSL 3.6.5; used for the live fetch).

## 1. Teaches-cell language present at the options anchor — PASS

The teaches cell asserts `--verify --end-of-options and commit peeling` under OPTIONS.

Fresh fetch `https://git-scm.com/docs/git-rev-parse` (reader view), `## OPTIONS` →
`--verify` entry:

- `Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1 …` (OPTIONS, `--verify`)
- `you can add the `^{type}` peeling operator to the parameter. For example, `git rev-parse "$VAR^{commit}"` will make sure `$VAR` names an existing object that is a commit-ish (i.e. a commit, or an annotated tag that points at a commit)` (OPTIONS, `--verify`)
- `wise to use `--end-of-options` so that the name argument is not mistaken for another option` (OPTIONS, `--verify`)
- EXAMPLES: `Print the commit object name from the revision in the $REV shell variable:` `$ git rev-parse --verify --end-of-options $REV^{commit}`; `This will error out if $REV is empty or not a valid revision.`
- Page version: `git-rev-parse last updated in 2.56.0`; `2.56.0 … *2026-09-28*` — matches the row's anchor cell.

Stored copy `corpus/evidence/sources-r36/S210.src` carries the same language at the
OPTIONS anchor, verified by grep on the raw HTML:

- `<h2 id="_options"><a class="anchor" href="#_options"></a>OPTIONS</h2>` — S210.src:2615
- peeling operator + commit-ish language — S210.src:2727–2731
- `Note that if you are verifying a name from an untrusted source, it is wise to use --end-of-options so that the name argument is not mistaken for another option` — S210.src:2735–2737
- EXAMPLE `$ git rev-parse --verify --end-of-options $REV^{commit}` and `This will error out if $REV is empty or not a valid revision.` — S210.src:3766–3771

Both the live page and the committed copy assert the exact language the teaches cell
claims. No mismatch.

## 2. Copy sha256-equality — FAIL

Fetch and compare:

```
$ curl -sL --max-time 60 https://git-scm.com/docs/git-rev-parse -o fresh.html
$ wc -c fresh.html corpus/evidence/sources-r36/S210.src
122331 fresh.html
122463 corpus/evidence/sources-r36/S210.src
$ sha256sum fresh.html corpus/evidence/sources-r36/S210.src
9b8f63b653029da49bce87f6b292f099dc8f1b3667a85515c92f66a6f5eb2978  fresh.html
64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421  corpus/evidence/sources-r36/S210.src
$ cmp fresh.html corpus/evidence/sources-r36/S210.src
fresh.html corpus/evidence/sources-r36/S210.src differ: char 899, line 36
```

`diff -u` shows exactly two hunks (4 changed lines), both site-asset chrome:

- line 36: stylesheet link `href="/application.min.c863b1eca1217b6c0d4a322bad3dcbe8f057d08564bd9fb8dca5a00a04dc66e6.css" integrity="sha256-yGOx7KEhe2wNSjIrrT3L6PBX0IVkvZ&#43;43KWgCgTcZuY="` → `href="/application.min.ee050e6639aacc8d3f18c4718a1a579307a7b4f7e327a148fb17dba7398c7476.css"` (integrity attribute dropped)
- line 3818: script tag `application.min.2c50db482403f7c73cf1c3fdff10121a98d563baede24a87cbc8b056a298196a.js" integrity="sha256-LFDbSCQD98c88cP9/xASGpjVY7rt4kqHy8iwVqKYGWo="` → `application.min.eab2fadf7c740b753eac932d50ce3f1a8faccdef730adfe2b7d9c14c898960c9.js"` (integrity attribute dropped)

The man-page prose is byte-identical between copy and live (title, NAME, OPTIONS,
EXAMPLES all identical — the diff touches nothing else), so the taught content is
unaffected. But the copy is not sha256-equal to the current live page.

Corroboration — this is not a fetch artifact:

- The lane's own frozen counter classifies S210 as drifted at the tip: `.ufo/waves/round-36/evidence/drift-live-r36.txt:210` → `S210 drifted`; `evidence/c1-after.txt:3` → `oracle_drifted=9` (independent re-derivation by `w2/ExecDriftLive.md` and `w2/ExecReC1A.md`: drifted set = S156–S160, S176, S177, S210, S211; live sha `9b8f63b6…` matches my fresh fetch exactly).
- The copy itself carries no `sha256:` header, and no lesson Gate digest exists for S210 at the tip (`corpus/lessons/round-36.md` does not exist under `bf0df77`; the lessons dir ends at `round-35.md`). The only recorded digest for this URL is `corpus/lessons/round-32.md:43` (S064 row): `64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421` — equal to the current S210 copy, i.e. the copy reproduces the pre-asset-rebuild bytes, not today's live bytes.

By the lane's own mechanical criterion (`corpus/QUALITY.md:837-839`: compare full-document
sha256 with the one recorded when the row was opened; count as a source change when they
differ), S210 is a source change: `sha256(copy)=64c60354…` vs `sha256(live)=9b8f63b6…`.

## 3. Lane rule in teaches consistent with round-19 corpus usage — PASS

The teaches cell: `lane rule: do it once, retain the full object id, then separately bind
the actual loaded register/correction bytes to blobs at that commit; a hash printer alone
does not prove the latter.`

`corpus/lessons/round-19.md` (C2 refinement discovered by the first-wave critic) states
the same separation: `A bound invocation must compare exact loaded register/correction
bytes with blobs at its explicit measured commit; uncommitted, external or differing input
is could-not-evaluate.` The round-19 Gate for S064 likewise scopes the source:
`Type peeling and --end-of-options are in OPTIONS --verify; neither proves input bytes
match that tree.` S210's teaches language is consistent with that usage (resolve once,
bind bytes separately; hash printer alone is not a binding).

## VERDICT: FAIL

Defect: `corpus/evidence/sources-r36/S210.src` is not sha256-equal to the live page
(`sha256(S210.src)=64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421` vs
live `9b8f63b653029da49bce87f6b292f099dc8f1b3667a85515c92f66a6f5eb2978`; `cmp` differs at
char 899 line 36). The mismatch is confined to two site-asset-bundle lines (stylesheet/script
link digests and their `integrity=` attributes) — the taught prose is byte-identical and the
options-anchor content (check 1) holds — but the row's copy does not reproduce live bytes,
and the lane's own frozen counter already records S210 as drifted at the tip
(`.ufo/waves/round-36/evidence/drift-live-r36.txt:210`; `evidence/c1-after.txt:3`
oracle_drifted=9 includes S210). No recorded full-document digest exists at the tip for S210
(no copy header; no round-36 lesson Gate), so there is no pinned baseline against which the
drift was adjudicated as representation-only.

Checks: 1 PASS (options anchor, live + copy cited above), 2 FAIL (copy sha256-equality),
3 PASS (lane-rule consistency with `lessons/round-19.md`).

Tooling: no installs/upgrades performed.

Report: .ufo/waves/round-36/w2/RevSupS210.md
