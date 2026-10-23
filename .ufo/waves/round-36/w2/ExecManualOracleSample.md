# ExecManualOracleSample — independent manual sample of the C1 real arm (round 36, wave 2, attempt 2)

Seat: `mori-r36-w2-ExecManualOracleSample-13` (executor; leaf). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`, read-only for this seat. Landed tip measured:
`bf0df77fee4b6ef54a90aea09335c7617f125151` (`git rev-parse HEAD` → same). At my first check
`git status --porcelain -- corpus tools` was empty; during my run concurrent seats began editing
`corpus/README.md`, `corpus/knowledge/source-drift-r36.md` and `.ufo/waves/round-36/contract.md`
in the worktree — none of those edits are mine, and I did not touch them. The files I measured
(`corpus/SOURCES.md`, `corpus/evidence/sources-r3*/`, `tools/mori-source-drift.py`) are byte-identical
between the tip and the worktree (`git show bf0df77:corpus/SOURCES.md | sha256sum` ==
`sha256sum corpus/SOURCES.md` → `e40f9cb2…`; the tool blob → `578667ca…` both ways), so the
measurement below is of the tip's bytes. Scratch: `/fast/scratch/hyaku/mori-r36/ExecManualOracleSample/`.
No tool installed or upgraded (nothing needed). No lane file edited except this report; no
git/jj mutating command run.

**What my item attacks:** the *per-row* honesty of the C1 real arm as reported by
`tools/mori-source-drift.py` on the lane's own bytes. I do not trust the tool's own verdict path:
I re-fetched each sampled row URL with `curl` (a different HTTP client, different UA, separate
process), hashed the body myself, located the committed copy myself under the tool's own
`find_copy` rule, applied the contract's classification rules by hand
(`contract.md:36-47`), and only then compared my line with the tool's line.

---

## 1. The sampled rows, the URLs the tool itself parses, and the copy each rule selects

I re-implemented the tool's registry parse and `find_copy` (highest `sources-r<N>`) rather than
reading URLs out of the Markdown by eye:

```
$ python3 -c "
import re
ROW_RE=re.compile(r'^\| S\d{3} ')
URL_RE=re.compile(r'https?://[^\s|]+')
p='/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md'
t=open(p,encoding='utf-8',errors='replace').read()
want={'S205','S206','S212','S156','S160','S176'}
for line in t.splitlines():
    if not ROW_RE.match(line): continue
    cells=[c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells)<2: continue
    m=URL_RE.search(cells[1])
    u=m.group(0).rstrip('.,;)') if m else None
    if cells[0] in want: print(cells[0], repr(u))
"
S156 'https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c'
S160 'https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c'
S176 'https://docs.python.org/3/library/unicodedata.html'
S205 'https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md'
S206 'https://www.rfc-editor.org/rfc/rfc6585'
S212 'https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst'
```

Copy selection under the `find_copy` rule (`corpus/evidence/sources-r<N>/<id>.<ext>`, highest `N`),
verified against the committed tree at the tip (`git ls-tree -r --name-only bf0df77 --
corpus/evidence/`):

```
$ ls -l corpus/evidence/sources-r*/S205.src corpus/evidence/sources-r*/S206.src corpus/evidence/sources-r*/S212.src corpus/evidence/sources-r*/S156.* corpus/evidence/sources-r*/S160.* corpus/evidence/sources-r*/S176.*
-rw-r--r-- 1 vgpnk vgpnk  11296 Oct 23 09:11 corpus/evidence/sources-r36/S205.src
-rw-r--r-- 1 vgpnk vgpnk 171482 Oct 23 09:11 corpus/evidence/sources-r36/S206.src
-rw-r--r-- 1 vgpnk vgpnk   4315 Oct 23 09:11 corpus/evidence/sources-r36/S212.src
-rw-r--r-- 1 vgpnk vgpnk   4249 Oct 22 18:53 corpus/evidence/sources-r30/S156.txt
-rw-r--r-- 1 vgpnk vgpnk   2389 Oct 22 18:53 corpus/evidence/sources-r30/S160.txt
-rw-r--r-- 1 vgpnk vgpnk  55620 Oct 22 22:37 corpus/evidence/sources-r32/S176.src
```

```
$ find corpus/evidence -name 'S176*' -o -name 'S156*' -o -name 'S160*' | sort
corpus/evidence/sources-r30/S156.txt
corpus/evidence/sources-r30/S160.txt
corpus/evidence/sources-r32/S176.src
```

**Correction to the task's own hint (not a lane defect):** the task text says "r33-era copy for
S176". Under the `find_copy` rule the S176 copy is `sources-r32/S176.src`; no `S176.*` file exists
in `sources-r33`, `r34`, `r35` or `r36`. The rule-based selection (highest `N` present) and the
"r32" answer are the same file, so the classification is unaffected. S156/S160 are `r30` copies as
the task said.

## 2. Independent fetch (curl), then sha256 of body vs sha256 of copy

```
$ cd /fast/scratch/hyaku/mori-r36/ExecManualOracleSample
$ for id in …; do curl -sS -L --max-time 40 -A "mori-source-drift/1.0" -w "http_code=%{http_code} size=%{size_download} url=%{url_effective}\n" -o $id.fetch "$u"; sha256sum $id.fetch; done
== S205 https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md
http_code=200 size=11296 url=https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md
88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8  S205.fetch
== S206 https://www.rfc-editor.org/rfc/rfc6585
http_code=200 size=171482 url=https://www.rfc-editor.org/info/rfc6585/
cc0123160b49d4abce57f51a1d56c02745afc61d29dd20c0e51fc42bb5f5d968  S206.fetch
== S212 https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst
http_code=200 size=4315 url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst
4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e  S212.fetch
== S156 https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c
http_code=200 size=17973 url=https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/bus-print-properties.c
b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a  S156.fetch
== S160 https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c
http_code=200 size=47020 url=https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c
285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab  S160.fetch
== S176 https://docs.python.org/3/library/unicodedata.html
http_code=200 size=55620 url=https://docs.python.org/3/library/unicodedata.html
a82233d1a4dedfe297b6fe9a2dc263ad48da3c8b7a2acc05b62e2c90abb1cf37  S176.fetch
```

Committed-copy digests:

```
$ sha256sum corpus/evidence/sources-r36/S205.src corpus/evidence/sources-r36/S206.src corpus/evidence/sources-r36/S212.src corpus/evidence/sources-r30/S156.txt corpus/evidence/sources-r30/S160.txt corpus/evidence/sources-r32/S176.src
88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8  corpus/evidence/sources-r36/S205.src
cc0123160b49d4abce57f51a1d56c02745afc61d29dd20c0e51fc42bb5f5d968  corpus/evidence/sources-r36/S206.src
4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e  corpus/evidence/sources-r36/S212.src
4c02999410622d782979d025a9a61314104873cba9c19e4857feba4bd0473b5e  corpus/evidence/sources-r30/S156.txt
d458d674a8e7bd4b0b377f72c3815bcab0f6118b2241927b4e5466a2446832a0  corpus/evidence/sources-r30/S160.txt
d3d261bcde4906ce9685d8e362a7bbb0dc4b254b1fc12f70ec46a9db65e77375  corpus/evidence/sources-r32/S176.src
```

Stability re-check (second, independent fetch of the same URLs):

```
S176.fetch2 a82233d1a4dedfe297b6fe9a2dc263ad48da3c8b7a2acc05b62e2c90abb1cf37   (http_code=200 size=55620)
S156.fetch2 b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a   (http_code=200 size=17973)
S205.fetch2 88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8   (http_code=200 size=11296)
S206.fetch2 cc0123160b49d4abce57f51a1d56c02745afc61d29dd20c0e51fc42bb5f5d968   (http_code=200 size=171482)
S212.fetch2 4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e   (http_code=200 size=4315)
```

Note S206: the URL redirects to `https://www.rfc-editor.org/info/rfc6585/`; both my curl (`-L`) and
the tool (which follows redirects) land on the same body and the same digest as the committed copy.

## 3. Hand classification per `contract.md:36-47`

Rules, applied by hand to the two byte strings: `fresh` = sha256(body) == sha256(copy);
`excerpt` = not fresh and `copy.strip()` non-empty and occurring contiguously in the body;
`drifted` = otherwise. (`copy` = the whole committed file, header bytes included — that is what
the tool reads.)

```
$ python3 - <<'EOF'
import hashlib, os
root='/home/vgpnk/Projects/shokunin/mori-shokunin'
ev=os.path.join(root,'corpus','evidence')
def find_copy(sid):                      # the tool's rule: highest sources-r<N>
    best=None
    for name in os.listdir(ev):
        if not name.startswith('sources-r'): continue
        n=int(name[len('sources-r'):]); d=os.path.join(ev,name)
        if not os.path.isdir(d): continue
        for e in sorted(os.listdir(d)):
            if e.startswith(sid+'.'):
                if best is None or n>best[0]: best=(n,os.path.join(d,e))
    return best
for sid in ['S156','S160','S176','S205','S206','S212']:
    n,p=find_copy(sid)
    copy=open(p,'rb').read(); body=open(sid+'.fetch','rb').read()
    hb=hashlib.sha256(body).hexdigest(); hc=hashlib.sha256(copy).hexdigest()
    if hb==hc: st='fresh'
    else:
        s=copy.strip()
        st='excerpt' if (s and s in body) else 'drifted'
    hdr=None
    for line in copy.split(b'\n')[:6]:
        if line.startswith(b'sha256: '): hdr=line.split(b': ',1)[1].decode()
    print(f"{sid}: copy=sources-r{n}/{os.path.basename(p)} fetch_sha={hb} copy_sha={hc} "
          f"fetch_bytes={len(body)} copy_bytes={len(copy)} copy_header_sha={hdr} "
          f"stripped_contiguous={bool(copy.strip() and copy.strip() in body)} -> {st}")
EOF
S156: copy=sources-r30/S156.txt fetch_sha=b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a copy_sha=4c02999410622d782979d025a9a61314104873cba9c19e4857feba4bd0473b5e fetch_bytes=17973 copy_bytes=4249 copy_header_sha=b56aa781be9c29b610156925030d3c4ab720c0ad73d57907d230ca3047302f2a stripped_contiguous=False -> drifted
S160: copy=sources-r30/S160.txt fetch_sha=285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab copy_sha=d458d674a8e7bd4b0b377f72c3815bcab0f6118b2241927b4e5466a2446832a0 fetch_bytes=47020 copy_bytes=2389 copy_header_sha=285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab stripped_contiguous=False -> drifted
S176: copy=sources-r32/S176.src fetch_sha=a82233d1a4dedfe297b6fe9a2dc263ad48da3c8b7a2acc05b62e2c90abb1cf37 copy_sha=d3d261bcde4906ce9685d8e362a7bbb0dc4b254b1fc12f70ec46a9db65e77375 fetch_bytes=55620 copy_bytes=55620 copy_header_sha=None stripped_contiguous=False -> drifted
S205: copy=sources-r36/S205.src fetch_sha=88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8 copy_sha=88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8 fetch_bytes=11296 copy_bytes=11296 copy_header_sha=None stripped_contiguous=True -> fresh
S206: copy=sources-r36/S206.src fetch_sha=cc0123160b49d4abce57f51a1d56c02745afc61d29dd20c0e51fc42bb5f5d968 copy_sha=cc0123160b49d4abce57f51a1d56c02745afc61d29dd20c0e51fc42bb5f5d968 fetch_bytes=171482 copy_bytes=171482 copy_header_sha=None stripped_contiguous=True -> fresh
S212: copy=sources-r36/S212.src fetch_sha=4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e copy_sha=4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e fetch_bytes=4315 copy_bytes=4315 copy_header_sha=None stripped_contiguous=True -> fresh
```

**Hand verdicts:** S156 `drifted`, S160 `drifted`, S176 `drifted`, S205 `fresh`, S206 `fresh`,
S212 `fresh`.

## 4. The tool's own run, and the comparison

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 tools/mori-source-drift.py --root /home/vgpnk/Projects/shokunin/mori-shokunin > /fast/scratch/hyaku/mori-r36/ExecManualOracleSample/tool-run.txt 2>&1; echo "exit=$?"
exit=1
$ grep -E '^(S156|S157|S158|S159|S160|S176|S177|S205|S206|S210|S211|S212) |^MORI_SOURCE_DRIFT' tool-run.txt
S156 drifted
S157 drifted
S158 drifted
S159 drifted
S160 drifted
S176 drifted
S177 drifted
S205 fresh
S206 fresh
S210 drifted
S211 drifted
S212 fresh
MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
```

(The full 220-line output is in the scratch file; the exit code 1 is the tool's contract:
`drifted>0` → 1, `contract.md:47`.)

Determinism, second run of the same command:

```
$ python3 tools/mori-source-drift.py --root /home/vgpnk/Projects/shokunin/mori-shokunin > …/tool-run2.txt 2>&1; echo "exit2=$?"
exit2=1
$ diff …/tool-run.txt …/tool-run2.txt && echo IDENTICAL
IDENTICAL
ad8a7ed4c75f420dd3bc33514ec1f46025b00c66036db2d75f09eb594d17f5dd  …/tool-run.txt
ad8a7ed4c75f420dd3bc33514ec1f46025b00c66036db2d75f09eb594d17f5dd  …/tool-run2.txt
```

**Comparison — 6 of 6 agree:**

| row | my hand state | tool line | agree |
|---|---|---|---|
| S156 | drifted | `S156 drifted` | yes |
| S160 | drifted | `S160 drifted` | yes |
| S176 | drifted | `S176 drifted` | yes |
| S205 | fresh | `S205 fresh` | yes |
| S206 | fresh | `S206 fresh` | yes |
| S212 | fresh | `S212 fresh` | yes |

The tool's summary (`rows=220 fresh=49 drifted=9 no-copy=162`) matches the tip's data receipt
`.ufo/waves/round-36/evidence/c1-after.txt:3` (`oracle_fetched=58 oracle_fresh=49 oracle_drifted=9
oracle_excluded=0 mismatches=0`): 49 fresh + 9 drifted = 58 rows with a committed copy, and the
registry carries 220 rows.

**Why the three `drifted` rows are `drifted` (mechanism, each measured):**

- **S156, S160** — the committed copy is an *annotated excerpt*: a 5-field header
  (`id`, `url`, `sha256` = digest of the **full fetched document**, `accessed`, `lines`) followed by
  `N<TAB>text` quoted lines. Its header digest **equals the live body digest** exactly
  (S156 `b56aa781…` = live `b56aa781…`; S160 `285b3d0c…` = live `285b3d0c…`), so the *source has
  not changed*; the copy file is nonetheless not a contiguous substring of the body (header bytes
  plus line-number prefixes), hence `drifted`, not `excerpt`. Reader check:
  `head -c 400 corpus/evidence/sources-r30/S156.txt` → `id: S156 / url: … / sha256:
  b56aa781… / accessed: 2026-10-22T21:12:07Z / lines: 16-426` then `16\t#include "strv.h"`.
- **S176** — the copy is the whole page and the live page is the same size (55 620 B both), differing
  in exactly one line: `diff corpus/evidence/sources-r32/S176.src S176.fetch` →
  `721c721  <       Last updated on Oct 23, 2026 (00:01 UTC).  --- >       Last updated on Oct 23, 2026 (18:17 UTC).`
  A docs.python.org rebuild footer, not a changed source.

So for my six sampled rows the tool's labels are exactly right *as byte labels*, and the drifted
ones are representation differences, not source changes — the same conclusion the wave-1 sweep
reached (`w1/MineCopyFidelity.md`).

---

## 5. Defect found while measuring (independently reproduced): the landed corpus enumerates the
##    drifted set as **seven** rows; the tip's receipt and probe both give **nine**

My item's assigned comparison passed (6/6). But to know whether the *sampled* drifted rows were a
complete population, I hand-classified the three remaining drifted ids the tool printed
(S157, S158, S159, S177) and then the two the tool prints as drifted but no landed text mentions
(S210, S211):

```
$ python3 - <<'EOF'   # same hand rules, same find_copy rule, curl fetch
S157: copy=sources-r30/S157.txt fetch_sha=47e98d394462e05b copy_sha=bff6495cd91a9b8f hdr_sha=47e98d394462e05b -> drifted
S158: copy=sources-r30/S158.txt fetch_sha=428dc8308d5caf70 copy_sha=9e375293fea6d643 hdr_sha=428dc8308d5caf70 -> drifted
S159: copy=sources-r30/S159.txt fetch_sha=dc5a771c9ed17875 copy_sha=e6fe760c95ba3bb7 hdr_sha=dc5a771c9ed17875 -> drifted
S177: copy=sources-r32/S177.src fetch_sha=fe0d61d9e8cef672 copy_sha=650c53ac7695b816 hdr_sha=- -> drifted
S210: copy=sources-r36/S210.src fetch_sha=9b8f63b653029da4 copy_sha=64c603545b3f9799 hdr_sha=- -> drifted
S211: copy=sources-r36/S211.src fetch_sha=27a79ff9a136515f copy_sha=a4e104ec9d6da304 hdr_sha=- -> drifted
EOF
```

(S211's fetch digest differs from fetch to fetch — see the nonce finding below — so its printed
`fetch_sha` is one sample, not a stable value; the `drifted` verdict is stable.)

The five excerpt rows (S156–S159 and S160) all carry a `sha256:` header equal to the live body's
digest (`hdr_sha == fetch_sha` in the output above for S157 `47e98d39…`, S158 `428dc830…`,
S159 `dc5a771c…`), and S177's copy differs from the live page in exactly one line
(`diff …/sources-r32/S177.src S177.fetch` → `370c370 <       Last updated on Oct 23, 2026 (00:01
UTC). --- >       Last updated on Oct 23, 2026 (18:17 UTC).`). So the *seven* rows the landed text
enumerates are indeed all representation differences — the landed text's characterisation of those
seven is correct; its **count** is what no longer holds.

All nine agree with the tool. But the landed text enumerates only seven:

- `corpus/knowledge/source-drift-r36.md:17` — "seven `drifted` rows were five annotated excerpts
  from round 30 (S156–S160: header lines and line-number prefixes; each header's full-document
  sha256 still equals the live body) and two docs.python.org pages whose only change is the build
  footer (S176, S177)".
- `corpus/QUALITY.md:841` (criterion 105, "Shown able to fail") — "all seven real drifted rows were
  representation differences (S156–S160 annotated excerpts whose header sha256 equals the live body;
  S176/S177 build footers)".
- `SKILL.md:860` — names only "annotated excerpts (round 30, S156–S160) and rebuilt doc pages
  (S176, S177)".

against the same tip's `evidence/c1-after.txt:3` (`oracle_drifted=9`) and the live run above
(`drifted=9`, ids `S156, S157, S158, S159, S160, S176, S177, S210, S211`).

A fourth site carries the same figure: `.ufo/waves/round-36/contract.md:118-119` ("5 of the 7
oracle-drifted real rows are such excerpts and 2 differ only in a docs.python.org rebuild footer").
That sentence is a **pre-data** statement (it records wave-1's `w1/CritAxisFit.md` argument, made
before the r36 copies existed), so it is not wrong where it was written — and it is frozen, so it is
not mine to change. It is listed here only because the *landed* documents above inherited the same
"seven" figure and present it as the probe's current behaviour, which is what a reader at this tip
will act on.

**When "seven" was true, and why it is stale now.** The wave-1 population was seven because the
round-36 copies S205–S220 (including S210 and S211) did not exist yet; they arrived in the data
commit `bf0df77` itself. The three landed documents describe the probe's output as a reader will
meet it *at the tip*, where the drifted set is nine. The gap is therefore a stale carry-over of a
pre-data measurement into post-data standing guidance, not a disagreement about the bytes.

Two consequences, both material to the standing guidance:

1. **The count is wrong at the tip.** "The seven drifted rows" reads as the complete set; at the tip
   it is nine. The "seven" is the wave-1 population, before the r36 copies S205–S220 existed, and it
   was carried into the landed text unchanged. A reader who runs the probe and sees `drifted=9` with
   S210 and S211 unnamed is reading guidance written for a population that no longer exists.
2. **Criterion 105's prescribed procedure cannot be executed for the two unnamed rows.**
   `corpus/QUALITY.md:837-839` requires, "for every real row a counter counts as drifted, compare
   the source's full-document sha256 with the one recorded when the row was opened (the copy header
   or the lesson Gate)". The r36 copies of S210/S211 carry **no `sha256:` header** (they are raw
   response bodies) and no lesson Gate digest exists for them, so the procedure has no recorded
   digest to compare against for 2 of the 9 rows the counter counts.

For completeness, I characterised those two rows myself (they are representation differences too,
but of kinds the landed text does not describe):

- **S210** (`https://git-scm.com/docs/git-rev-parse`): copy vs live differs in 4 diff lines only —
  the stylesheet/script asset filenames and the presence of `integrity="sha256-…"` attributes
  (`diff corpus/evidence/sources-r36/S210.src S210b.fetch`):
  `< link rel="stylesheet" href="/application.min.c863b1ec….css" integrity="sha256-yGOx7KEh…">` vs
  `> link rel="stylesheet" href="/application.min.ee050e66….css">` (and the matching `<script>`).
  The prose is identical (`<title>Git - git-rev-parse Documentation</title>` in both).
- **S211** (`https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/`): copy vs live differs in 4 diff
  lines only — `<meta name="ncbi_phid" content="…">` and the `csrfmiddlewaretoken` hidden input.
  That page is **not byte-reproducible at all**: three consecutive fetches of the same URL gave
  three different digests (`8f1fd5da…`, `0a325532…`, `f1f0460f…`) with a different CSRF token
  each time. So S211 can never be classified `fresh` again, whatever the site does — the probe's
  exit code 1 is structurally guaranteed while such a row is in the corpus.

(`corpus/README.md` carries an *uncommitted* worktree edit from a concurrent seat that corrects the
count to 9 but still enumerates only seven ids and does not name S210/S211; that file is not mine
and is recorded as observation only.)

This corroborates the same enumeration defect reported independently by `w2/ExecDriftLive.md` §6
("the landed corpus text enumerates **seven** drifted rows; the round's own receipt and the live
probe both say **nine**") and the count observation in `w2/RevQuality105.md:113-114` and
`w2/RevC1Interface.md:33`; it is not a new discovery, but my measurement is independent (different
client, hand rules, hand copy resolution) and adds the two new mechanism findings above
(S210 asset-hash/SRI change; S211 per-request CSRF nonce → permanently unreproducible).

## 6. Does anything infer a freshness admission from C1?

I searched the round's landed artifacts for the overreach shape. `corpus/knowledge/source-drift-r36.md:15`
("`fresh` proves only byte identity with the committed copy, never that the row's `teaches` is
right"), `SKILL.md:859-861` ("Read `drifted` as 'the copy is not reproducible from today's body',
never as a changed source") and the contract's own declaration
(`.ufo/waves/round-36/contract.md:116-125`, C1 exploratory, P-C1 = byte behaviour only) all state
the boundary explicitly, and the data receipt `evidence/c1-after.txt` contains only counter output
plus the `C1=met` label with no prose verdict. **No freshness admission from C1 found in the landed
artifacts.** The defect in §5 is an enumeration/accuracy defect in the standing guidance, not a
freshness overreach.

## 7. Exercised evidence, and what was not exercised

- Exercised: `curl` fetches of 9 row URLs (6 sampled + S157/S158/S159/S177/S210/S211) with recorded
  status codes, byte sizes and digests; sha256 of 9 committed copies; the tool's registry parse and
  `find_copy` rule re-implemented by hand; the contract's classification rules applied by hand; the
  lane's own `python3 tools/mori-source-drift.py --root <lane>` run (exit 1, 220 lines, summary
  above) twice, byte-identical between runs; the tip's committed tree (`git ls-tree`,
  `git rev-parse HEAD`, `git status --porcelain -- corpus tools` → empty).
- Not exercised: the frozen counters `count-c1.py` / `count-c2.py` (other seats own those runs; the
  receipt was read as committed bytes and its printed quantities compared against my live probe),
  the blind arm, the selftest fixture, and any lane file other than the three read-only greps above.
- No tool installed or upgraded; nothing to record under the 2026-10-19 operator directive.
- The lane repo was not mutated by me: my only write is this report file. `git status --porcelain`
  also lists `corpus/README.md`, `corpus/knowledge/source-drift-r36.md`,
  `.ufo/waves/round-36/contract.md` and `.ufo/waves/round-36/dispatch-log.txt` as modified — those
  are concurrent seats' worktree edits that appeared during my run; I did not touch them. (The
  `knowledge/source-drift-r36.md` edit refines the `excerpt`/`no-copy`/exit-2 table rows and does
  **not** touch line 17, the "seven drifted rows" sentence this report flags: `grep -n seven
  corpus/knowledge/source-drift-r36.md` → line 17 only, in the current worktree as well.)

## 8. Item verdict

Assigned check: **6 of 6 hand classifications equal the tool's lines** (S156/S160/S176 `drifted`;
S205/S206/S212 `fresh`), each re-derived from an independent `curl` fetch, a hand-selected copy
under the tool's own `find_copy` rule, and the contract's rules; and the tool's summary matches the
tip's receipt (`fresh=49 drifted=9`, 58 rows with copies, 220 registry rows).

Defect found outside that check but inside the same artifact family, with path:line evidence:
`corpus/knowledge/source-drift-r36.md:17`, `corpus/QUALITY.md:841` and `SKILL.md:860` state **seven**
drifted rows while the tip's receipt and live probe give **nine** (the two unnamed ids are S210 and
S211), and criterion 105's prescribed digest comparison (`corpus/QUALITY.md:837-839`) has no
recorded full-document sha256 to use for those two rows.

VERDICT: FAIL

Failing item: the landed corpus enumerates the C1 real arm's drifted set as seven rows
(`corpus/knowledge/source-drift-r36.md:17`, `corpus/QUALITY.md:841`, `SKILL.md:860`) against the
measured nine (`evidence/c1-after.txt:3`; live `MORI_SOURCE_DRIFT … drifted=9`, ids S156, S157,
S158, S159, S160, S176, S177, S210, S211). The assigned per-row comparison for S156, S160, S176,
S205, S206, S212 passes 6/6.
