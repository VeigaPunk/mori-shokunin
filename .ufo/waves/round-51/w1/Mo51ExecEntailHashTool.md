# Mo51ExecEntailHashTool — C2 entailment plumbing checked before votes land (mori round 51, wave w1)

Seat: Mo51ExecEntailHashTool (executor, leaf — no subagents). Item: check the C2 entailment plumbing before votes
land. Data commit scored: `87e0c374537557754bf71dd68036ded3ddc6699c`. Lane HEAD observed after the run:
`b504cb1701568a0038aab9d98ec13d28eff801da` (the wave spec/dispatch commit; it carries no `w1/` report, so the
counter still reads unmet there — line in §2). Scratch:
`/fast/scratch/hyaku/mori-r51/Mo51ExecEntailHashTool/` (`mkdir -p`, `TMPDIR` pointed inside it, removed at the end).
No writes to the lane except this report; no git/jj mutation in the lane or the fleet root.

Axes for this item: (a) do the recorded row hashes equal an independent recomputation, (b) does a correctly voted
report actually turn P-C2 met, (c) do the three vote states the contract names (entailed / overclaim / L1-authored)
do what the predicate says they do, (d) what does the frozen counter silently accept.

## 1. Row hashes recomputed with an independent script

I wrote my own parser/hasher from the predicate sentence only (no import of `count-c2.py`; source quoted below,
scratch copy deleted with the scratch dir):

```python
# hashrows.py — <h> = first 12 hex of sha256 of the row's claim cell, whitespace collapsed, ends stripped
import hashlib, re, subprocess, sys
def cells(line):
    s = line.strip(); p = re.split(r"(?<!\\)\|", s)
    return [x.strip() for x in (p[1:-1] if s.endswith("|") else p[1:])]
def rows(text):
    header, out, fence = None, [], False
    for line in text.split("\n"):
        if line.lstrip()[:3] in ("```", "~~~"): fence = not fence; continue
        if fence or not line.lstrip().startswith("|"):
            if header is not None and out: break
            continue
        cs = cells(line)
        if header is None:
            if [c.lower() for c in cs] == ["claim", "source", "quote"]: header = cs
            continue
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cs): continue
        out.append(cs)
    return out
repo, rev = sys.argv[1], sys.argv[2]
text = subprocess.run(["git", "-C", repo, "show", "%s:corpus/knowledge/memavailable-estimate-r51.md" % rev],
                      stdout=subprocess.PIPE).stdout.decode("utf-8", "surrogateescape")
for n, cs in enumerate(rows(text), 1):
    h = hashlib.sha256(re.sub(r"\s+", " ", cs[0]).strip().encode("utf-8")).hexdigest()[:12]
    print("row=%d hash=%s claim=%s" % (n, h, cs[0]))
```

Commands and outputs (all from scratch; `$S` = the scratch dir):

```
$ python3 "$S/hashrows.py" mori-shokunin 87e0c374537557754bf71dd68036ded3ddc6699c > "$S/mine.txt"
rows=21                       # stderr
exit=0
$ python3 mori-shokunin/.ufo/waves/round-51/count-c2.py --hashes 87e0c374537557754bf71dd68036ded3ddc6699c > "$S/counter-hashes.txt"
exit=0
$ diff -u .ufo/waves/round-51/evidence/c2-hashes-at-data.txt "$S/mine.txt"          -> (no output) exit=0
$ diff -u .ufo/waves/round-51/evidence/c2-hashes-at-data.txt "$S/counter-hashes.txt" -> (no output) exit=0
$ diff -u "$S/mine.txt" "$S/counter-hashes.txt"                                     -> (no output) exit=0
```

So the evidence file, the frozen counter's `--hashes`, and my recomputation agree byte for byte on all 21 rows:

```
row=1 hash=2d0daa4192f1
row=2 hash=eba2b78b47f3
row=3 hash=ad57d1b66582
row=4 hash=72cdbee44353
row=5 hash=a9cf30c5ed71
row=6 hash=5d06a2ae70cf
row=7 hash=6c8b6efc9731
row=8 hash=6b8f33ed528e
row=9 hash=1b9c863ec2c2
row=10 hash=cbcd91de05ac
row=11 hash=58ba82f481b8
row=12 hash=ec0f6c97eeba
row=13 hash=40b46a312e03
row=14 hash=a06f1037d952
row=15 hash=102feb3debfa
row=16 hash=357c747c23d2
row=17 hash=d6001a798ea7
row=18 hash=8f6d04247472
row=19 hash=a07e4bd7a5ec
row=20 hash=4d162ecf1409
row=21 hash=50f54829ae20
```

The claim text a seat reads from disk is the claim text the counter hashes: the worktree matches the data commit for
both files, so a seat hashing the working-tree entry gets these hashes too.

```
$ git -C mori-shokunin diff --stat 87e0c374537557754bf71dd68036ded3ddc6699c -- \
    corpus/knowledge/memavailable-estimate-r51.md corpus/SOURCES.md
(no output) exit=0
```

Live counter on the data commit (unchanged from `evidence/c2-at-data.txt`):

```
$ python3 mori-shokunin/.ufo/waves/round-51/count-c2.py 87e0c374537557754bf71dd68036ded3ddc6699c
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374537557754bf71dd68036ded3ddc6699c failed=entailment
exit=1
$ python3 mori-shokunin/.ufo/waves/round-51/count-c2.py HEAD --repo mori-shokunin      # HEAD=b504cb17
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=b504cb1701568a0038aab9d98ec13d28eff801da failed=entailment
exit=1
```

## 2. Fixture clone: a correctly voted report does turn P-C2 met

One `git clone --shared` from the lane into scratch (no full mirror), branch checked out at the data commit; every
commit below is in the clone only, under `-c user.name=Mo51ExecEntailHashTool -c user.email=mo51@example.invalid`.

```
$ git -C mori-shokunin rev-parse 87e0c374...^{commit}          -> 87e0c374537557754bf71dd68036ded3ddc6699c
$ git clone --shared --no-hardlinks mori-shokunin "$S/clone"   -> done, exit=0
$ git -C "$S/clone" rev-parse --show-toplevel                  -> $S/clone   (equals the fixture dir)
$ git -C "$S/clone" checkout -q -b fixture 87e0c374...
$ python3 .../count-c2.py 87e0c374... --repo "$S/clone"        # in-clone baseline, no votes
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=87e0c374... failed=entailment
exit=1
```

**F1 — `.ufo/waves/round-51/w1/Mo51Fake.md` with one `entailed` line per row** (hashes from §1; the vote lines in
this report are prefixed with `>` so they cannot be read as votes):

> ENTAIL 2d0daa4192f1 entailed — row 1
> ENTAIL eba2b78b47f3 entailed — row 2
> ENTAIL ad57d1b66582 entailed — row 3
> ENTAIL 72cdbee44353 entailed — row 4
> ENTAIL a9cf30c5ed71 entailed — row 5
> ENTAIL 5d06a2ae70cf entailed — row 6
> ENTAIL 6c8b6efc9731 entailed — row 7
> ENTAIL 6b8f33ed528e entailed — row 8
> ENTAIL 1b9c863ec2c2 entailed — row 9
> ENTAIL cbcd91de05ac entailed — row 10
> ENTAIL 58ba82f481b8 entailed — row 11
> ENTAIL ec0f6c97eeba entailed — row 12
> ENTAIL 40b46a312e03 entailed — row 13
> ENTAIL a06f1037d952 entailed — row 14
> ENTAIL 102feb3debfa entailed — row 15
> ENTAIL 357c747c23d2 entailed — row 16
> ENTAIL d6001a798ea7 entailed — row 17
> ENTAIL 8f6d04247472 entailed — row 18
> ENTAIL a07e4bd7a5ec entailed — row 19
> ENTAIL 4d162ecf1409 entailed — row 20
> ENTAIL 50f54829ae20 entailed — row 21

```
$ git commit -q -m "fixture F1: one entailed vote per row"     -> exit=0
2fd93255a2cf9db9cf583bc5171c5efed8fe3b27
 .ufo/waves/round-51/w1/Mo51Fake.md | 23 +++++++++++++++++++++++
$ python3 .../count-c2.py 2fd93255a2cf9db9cf583bc5171c5efed8fe3b27 --repo "$S/clone"
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=2fd93255a2cf9db9cf583bc5171c5efed8fe3b27
exit=0
```

The predicate is satisfiable exactly as written: 21 `entailed` lines (one per row, hashes as in §1), nothing else
changed, reads met with `entailed=21 dissent=0`.

**F2 — same file plus one `overclaim` line on row 1**, committed:

```
$ git commit -q -m "fixture F2: one overclaim line on row 1"   -> exit=0
d77050d4b6f89deb8cc952658acbbc439bcb14ff
$ python3 .../count-c2.py d77050d4b6f89deb8cc952658acbbc439bcb14ff --repo "$S/clone"
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=20 dissent=1 rev=d77050d4b6f89deb8cc952658acbbc439bcb14ff failed=entailment
exit=1
```

One `overclaim` blocks the row even though the same file also voted it `entailed` (`count-c2.py:220-224`: overclaim
is checked first and wins). `entailed` drops to 20 and `failed=entailment` is carried.

**F3 — rename the report to `MoriR51x.md`, votes unchanged**, committed:

```
$ git mv .ufo/waves/round-51/w1/Mo51Fake.md .ufo/waves/round-51/w1/MoriR51x.md
$ git commit -q -m "fixture F3: rename report to MoriR51x.md"  -> exit=0
1de44768020a8755a4d881c37e127e146c5f296d
 .ufo/waves/round-51/w1/{Mo51Fake.md => MoriR51x.md} | 0
$ python3 .../count-c2.py 1de44768020a8755a4d881c37e127e146c5f296d --repo "$S/clone"
C2=unmet claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=1de44768020a8755a4d881c37e127e146c5f296d failed=entailment
exit=1
```

The L1 prefix is a name test, not authorship (`count-c2.py:124`): the whole file's votes vanish from the tally, and
the file's `overclaim` vanishes with them — a `MoriR51*` report cannot dissent, so an overclaim written in one is
inert in both directions.

## 3. The overclaim-resolution route the contract names, validated end to end

The contract says an `overclaim` is resolved only by replacing the claim text with text a non-L1 seat voted
`entailed`. I took the two replacement routes the live reports propose and replayed them in the clone: replace the
cell, keep the old overclaim line, add the replacement's `entailed` line.

**Row 6** (`corpus/knowledge/memavailable-estimate-r51.md:27`, source S493). Proposed in
`Mo51CritEntail01.md` with vote hash `0a908e8eb4f3`:

```
old: The estimate starts from the free page count minus totalreserve_pages, the pages the kernel holds back from userspace allocations.
     hash(old) = 5d06a2ae70cf
new: The estimate begins with the free page count minus totalreserve_pages, then adds file cache and reclaimable slab.
     hash(new) = 0a908e8eb4f3   (equals the entailed vote)   words=17  words-beyond-quote=15  occurrences in entry=1
$ python3 .../count-c2.py c5074402c780cb482327b899638b233d6b9c0682 --repo "$S/clone"
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=c5074402c780cb482327b899638b233d6b9c0682
exit=0
```

The old overclaim line is still in the fixture report; after the replacement `5d06a2ae70cf` is no row's hash, so it is
ignored. `bad_rows=0` shows the new cell also passes the row rules (6+ words, unique, 3+ words beyond the quote).

**Rows 14 and 15** (`…:35`, `…:36`, source S494), proposed in `Mo51RevEntail13.md`:

```
row 14 old a06f1037d952 -> new 6c2327e19df1  (equals the entailed vote)  words=19  words-beyond-quote=14
row 15 old 102feb3debfa -> new 7e14f1771092  (equals the entailed vote)  words=20  words-beyond-quote=15
$ python3 .../count-c2.py 2cbe94fcde1d9f55f2aab1c16407a28edee829d9 --repo "$S/clone"
C2=met claims=21 located=21 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=21 dissent=0 rev=2cbe94fcde1d9f55f2aab1c16407a28edee829d9
exit=0
```

Plumbing conclusion: all three proposed replacement texts hash exactly to the hash their seat voted `entailed`, and
inserting them verbatim into the claim cell scores met with the old overclaims still present. The L1 must paste the
proposal text exactly (the hash is over the whitespace-collapsed cell): adding or dropping a word, a comma or a
parenthetical changes the hash and the existing `entailed` line stops matching. Whether those three texts are true
entailments is the voting seats' judgment, not mine; I checked text↔hash and the row rules only.

## 4. Edge behaviour of the frozen vote reader (observed, not fixed)

Each probe is a fixture commit off the data commit, scored with `--repo "$S/clone"`.

| probe | fixture | counter line | reading |
|---|---|---|---|
| P1 nested | all 21 votes in `.ufo/waves/round-51/w1/sub/Mo51Nested.md` | `C2=unmet … entailed=0 dissent=0 … failed=entailment` exit=1 | `git ls-tree --name-only <rev> .ufo/waves/round-51/w1/` returns the tree entry `sub`; a nested report is never opened, so **votes must sit directly in `w1/`** |
| P2 fenced | the same 21 votes inside a ` ```text ` fence in `Mo51Fenced.md` | `C2=met … entailed=21 dissent=0` exit=0 | the reader is fence-blind: **a vote-shaped line inside a fenced sample still votes** |
| P3 unknown hash | F1 file + `ENTAIL ffffffffffff overclaim` | `C2=met … entailed=21 dissent=0` exit=0 | a vote on a hash that is no row is ignored (keyed by hash only, no row/seat attribution) |
| P4 uppercase ext | the 21 votes in `Mo51Fake.MD` | `C2=unmet … entailed=0 dissent=0 … failed=entailment` exit=1 | `name.endswith(".md")` is case-sensitive; a `.MD` report casts no vote |

Commit ids for the probes: `08276a0d` (nested), `0b2f7f11` (fenced), `6fd67464` (unknown hash), `1102fa8a` (`.MD`).

Live hazard from P2, checked on the real worktree: every vote-shaped line currently in `w1/` comes from a seat whose
item is entailment (`Mo51CritEntail01`, `Mo51CritEntail07`, `Mo51CritEntail17`, `Mo51RevEntail13`, `Mo51RevEntail16`,
`Mo51RevEntail19`) — no accidental vote seen at the snapshot time. `Mo51CritEntail07.md:12-16` keeps its votes inside
a fence and they do count, which is fine for that seat but means a *sample* in any other report would vote too.
For the same reason every vote sample in this report carries a `>` prefix.

## 5. Live vote state at the snapshot (worktree, not yet committed)

Snapshot `2026-10-26T19:49:07-03:00`, 23 `.md` files in `w1/`, `w1/` still untracked
(`git status --porcelain` → `?? .ufo/waves/round-51/w1/`, `?? …/w1.ready`, `?? …/w1.ready.dispatched`). The counter
reads committed revisions only, so this state is invisible to it until the L1 commits the wave.

| row | hash | state | voted by |
|---|---|---|---|
| 1–5 | `2d0daa4192f1`,`eba2b78b47f3`,`ad57d1b66582`,`72cdbee44353`,`a9cf30c5ed71` | entailed ×1 each | Mo51CritEntail01 |
| 6 | `5d06a2ae70cf` | **overclaim ×1** | Mo51CritEntail01 (+ replacement `0a908e8eb4f3` entailed) |
| 7–11 | `6c8b6efc9731`,`6b8f33ed528e`,`1b9c863ec2c2`,`cbcd91de05ac`,`58ba82f481b8` | entailed ×1 each | Mo51CritEntail07 |
| 12 | `ec0f6c97eeba` | **no vote** | — |
| 13 | `40b46a312e03` | entailed ×1 | Mo51RevEntail13 |
| 14 | `a06f1037d952` | **overclaim ×1** | Mo51RevEntail13 (+ replacement `6c2327e19df1` entailed) |
| 15 | `102feb3debfa` | **overclaim ×1** | Mo51RevEntail13 (+ replacement `7e14f1771092` entailed) |
| 16 | `357c747c23d2` | entailed ×1 | Mo51RevEntail16 |
| 17–18 | `d6001a798ea7`,`8f6d04247472` | entailed ×2 | Mo51CritEntail17, Mo51RevEntail16 |
| 19–21 | `a07e4bd7a5ec`,`4d162ecf1409`,`50f54829ae20` | entailed ×2 | Mo51CritEntail17, Mo51RevEntail19 |

17 rows carry `entailed`, 3 carry `overclaim`, 1 (`row 12`) carries nothing; 3 vote hashes match no row
(`0a908e8eb4f3`, `6c2327e19df1`, `7e14f1771092` — the three proposed replacements, and I verified each equals the
sha256 of its proposal text in §3). Rows 17–21 have two votes from different roles, which is the wave's policy; the
frozen predicate itself needs only one.

## 6. Tooling

No tool installed or upgraded; no `pacman` transaction (host-wide pause respected); no writes to `~/.local/bin`.
`/home/vgpnk/Projects/shokuknow` untouched. Disk checked before work:
`scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku 27% 587.8G free`, `/home 35% 585G free`, rc 0; no ENOSPC.
Scratch (`hashrows.py`, `mine.txt`, `counter-hashes.txt`, `votes-valid.txt`, one `--shared` clone with the seven
fixture/probe commits, `tmp/`) removed after the report was written.

## 7. UNVERIFIED

- Whether rows 12, 14, 15 get votes or the L1 accepts the three replacement texts — I did not re-read `w1/` after the
  snapshot and the wave is still writing.
- The L1's integration commit: the fixture proves the counter turns met on a committed vote set, not that the real
  integration commit contains one.
- Entailment quality of any claim, including the three replacement texts: hash and row-rule plumbing only.
- The five source URLs' current bytes: I read the committed copies, not the network (pin arm is the counter's).

## Findings

- **MED — `corpus/knowledge/memavailable-estimate-r51.md:27` (row 6, hash `5d06a2ae70cf`)**: an `overclaim` from
  Mo51CritEntail01 blocks the row, so C2 reads `failed=entailment` until the claim cell is replaced. The proposed
  text hashes exactly to the seat's `entailed` vote (`0a908e8eb4f3`) and a fixture substitution scores met
  (`c5074402`); the cell must be replaced verbatim, not reworded.
- **MED — `corpus/knowledge/memavailable-estimate-r51.md:35-36` (rows 14, 15, hashes `a06f1037d952`,
  `102feb3debfa`)**: both blocked by `overclaim` votes from Mo51RevEntail13; the two proposed replacement texts hash
  exactly to that seat's `entailed` votes (`6c2327e19df1`, `7e14f1771092`) and the substitution fixture scores met
  (`2cbe94fc`).
- **MED — `corpus/knowledge/memavailable-estimate-r51.md:33` (row 12, hash `ec0f6c97eeba`)**: no vote at the
  snapshot; one row without an `entailed` line leaves `entailed=20 != claims=21` and C2 unmet.
- **MED — `.ufo/waves/round-51/count-c2.py:117-130` (vote reader)**: fence-blind — a vote-shaped line inside a
  fenced code block in any `w1/*.md` casts a real vote, so a pasted sample can block a row with an unintended
  `overclaim`. Frozen; named limit; seats must prefix quoted samples.
- **LOW — `.ufo/waves/round-51/count-c2.py:124,259-263`**: the reader sees only files directly under `w1/` with a
  lowercase `.md` suffix — a report under `w1/<seat>/` or a `.MD` file silently contributes nothing (probes P1, P4).
- **LOW — `.ufo/waves/round-51/count-c2.py:124`**: L1 exclusion is a filename-prefix test only, so a report named
  `MoriR51*` can neither vote nor dissent, and any non-prefixed file — whoever writes it — can vote `entailed` on text
  its author never opened. The arm proves a committed judgment string, not a reviewer step (named limit in the
  counter docstring; unchanged).
