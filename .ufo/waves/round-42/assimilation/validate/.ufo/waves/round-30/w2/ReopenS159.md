# Seat MoriR30.ReopenS159 — contract A1 residual (F3) for S159

Verdict: **agree** — the F3 residual passes for S159 at lane tip `713be29`: re-fetched sha256 matches the excerpt header, the Gate cell and the SOURCES anchor; every excerpt line equals the fetched line of the same number; both admit quotes are verbatim and their `(N words)` labels equal `wc -w`. One soft over-reach in the SOURCES `teaches` cell is recorded under "teaches support" — it is not an F3 mismatch.

Item attacked: A1 "Residual, uncounted (F3)" (`.ufo/waves/round-30/contract.md:153-154`), for S159 only.

## 1. Re-fetch receipt (S159 patch)

- Command: `curl -sS -D headers.txt -o edd3d943.patch -w 'HTTP %{http_code}\n' 'https://github.com/rfjakob/earlyoom/commit/edd3d9438dc564da7b694e5c96c9b3bc63bef2ac.patch'`
- Output: `HTTP 200`
- Access time of my fetch: `2026-10-22T22:02:41Z` (`date -u` immediately after the request; response header `date: Thu, 22 Oct 2026 22:02:41 GMT`).
- Size/lines: `content-length: 1180`; `wc -c -l` → `39 1180` (39 lines, 1180 bytes).
- `sha256sum edd3d943.patch` → `dc5a771c9ed178751c0473c9ada89152e70b9da13a048b0af30df6bbb1f2a9a1`.
- This is a single-commit mbox: `:1` `From edd3d9438dc564da7b694e5c96c9b3bc63bef2ac …`, `:3` `Date: Sun, 1 Mar 2020 11:00:34 +0100`, `:4` `Subject: [PATCH] earlyoom.service: set Restart=always`.

Comparison against the three published digests:

| location | value | match |
|---|---|---|
| `corpus/evidence/sources-r30/S159.txt:3` (`sha256:`) | `dc5a771c9ed178751c0473c9ada89152e70b9da13a048b0af30df6bbb1f2a9a1` | yes |
| `corpus/lessons/round-30.md:135` (Gate sha256 cell) | same 64-hex | yes |
| `corpus/SOURCES.md:165` (anchor cell) | `patch 1,180 B sha256 dc5a771c…` | yes (size and digest) |

Excerpt header `accessed` (`S159.txt:4`) is `2026-10-22T21:13:43Z`, identical to the Gate cell's access stamp (`round-30.md:135`), and later than the contract commit time `2026-10-22T21:08:28Z` required by A1 4a (`contract.md:138-139`). I cannot re-derive the author's access clock from bytes; only its consistency is checkable, and it is consistent.

## 2. Excerpt line diff (every excerpt line vs fetched line n)

Method: split the fetched bytes on `\n`; parse every body line matching `^(\d+)\t(.*)$`; compare each text byte-for-byte to fetched line n. This is stricter than A2's whitespace-collapse rule (`contract.md:201-203`) — no collapse was applied.

- Excerpt body: 27 entries, numbered 6 through 36.
- Absent numbers inside 6-36: 12, 18, 20, 23. In the fetched bytes these are `''`, `' '`, `' '`, `' '` — one blank line and three diff context lines holding a single space. A2 permits sparse excerpts (`contract.md:201`), and no non-blank line was dropped: 31 lines in range minus these 4 = 27.
- Content mismatches: **0**. All 27 texts are identical, including whitespace-sensitive ones (e.g. line 25 is `' \t$(CC) $(LDFLAGS) $(CFLAGS) -o $@ $(wildcard *.c)'` in both).
- Lines of both quoted ranges are present: 6, 7, 34, 35, 36.

## 3. Admit Gate quotes: verbatim and word labels

Lesson line `corpus/lessons/round-30.md:135` sits under `## Gate` (`:104`) and before the next `## ` heading (`:156`), so it is a Gate line.

q1 — `` `edd3d943.patch:6-7` (13 words): "Have systemd restart us should we get killed or crash for some reason." ``
q2 — `` `edd3d943.patch:34-36` (21 words): "+# earlyoom never exits on it's own, so have systemd +# restart it should it get killed for some reason. +Restart=always" ``

- q1 joined from fetched lines 6-7 with one space: **exact string equality** with the quote (also exactly equal after collapse), and equal to excerpt lines 6-7 joined. `wc -w` on the quote file → `13 q1.txt`; label says 13.
- q2 joined from fetched lines 34-36: **exact equality**, and equal to excerpt lines 34-36 joined. `wc -w` → `21 q2.txt`; label says 21.
- Both are ≤ 25 words (A1 4b cap, `contract.md:142-145`), and each is > 3 words, so the counted-id quote rule holds.
- The source's own `it's` (line 34) is retained, not "corrected": verbatim is satisfied.

## 4. Does the SOURCES `teaches` cell hold? (`corpus/SOURCES.md:165`, 7th cell; header row `:5`)

Cell text: "The unit's own comment and the commit message state the purpose of `Restart=always` — systemd restarts a daemon that was killed or crashed — so an earlyoom exit of that kind is followed by a fresh process that reprints its startup version line (S119:161)."

- Supported by the Gate-quoted lines: "The unit's own comment … and the commit message state the purpose of `Restart=always`". Fetched `:34-35` is the comment ("earlyoom never exits on it's own, so have systemd / restart it should it get killed for some reason."), `:36` is `+Restart=always`, `:6-7` is the message ("Have systemd restart us should we get killed or crash for some reason."). Report of intent — supported.
- "systemd restarts a daemon that was killed or crashed": as a statement of behaviour this is systemd's `Restart=` semantics, which the row's own scope cell excludes ("not systemd's own `Restart=` wording (systemd.service(5), not opened this round)"). The quoted lines give the authors' request, not a guarantee. [INFERENCE] presented in the declarative — a soft over-reach, not an F3 mismatch.
- "so … reprints its startup version line (S119:161)": not in S159's quoted bytes. I checked the cited line directly: `curl … https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` → `HTTP 200 bytes 21053`, line 161 = `fprintf(stderr, "earlyoom " VERSION "\n");`. The citation resolves; the causal step still leans on the excluded systemd semantics.
- Wider-than-quote anchors: the scope cell's Makefile component (":21-22") is byte-exact in the excerpt (`-all: earlyoom earlyoom.1` / `+all: earlyoom earlyoom.1 earlyoom.service`) but is not quoted in Gate line 135; the "2020-03-01" component is fetched `:3` (`Date: Sun, 1 Mar 2020 11:00:34 +0100`, matching the anchor's `2020-03-01T11:00:34+01:00`) but lies inside neither the excerpt (starts at line 6) nor a Gate quote. A1 4b/4c requires only one ≥3-word quote, so this is not a contract breach — it is a note that the row anchors more than its Gate line quotes.

## 5. Cheap adjacent check (same S159 block, not required by the item)

Reject row `round-30.md:136` URL re-fetched: `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in` → `HTTP 200 bytes 1340`, 51 lines, sha256 `d4019b66d87539a006fc2d178d972dcf1b46e70343627b8bf66d1a08dcdda0bd`, line 17 = `Restart=always` — all three row values match. I did not re-fetch the anonymous api.github.com tree URL in `:137`; it is rate-limit dependent and outside the admit chain.

## 6. Provenance of the bytes judged

- Context names lane tip `ad0f0474`; the live lane HEAD is `713be29` (`git log -1 --format='%H %s'` → `713be294669272b8b29e9a8cd60c5313704a2ee1 round-30: wave-2 spec, validator run and dispatch payload …`). `git status --porcelain` lists only untracked `.scratch/` and `.ufo/waves/round-30/w2/`.
- `git show HEAD:<path> | sha256sum` equals the worktree for the three judged files: `S159.txt` `e6fe760c…`, `round-30.md` `ed1ac08c…`, `SOURCES.md` `a8f7fbb0…`.
- `git log --oneline ee61010..HEAD -- corpus/SOURCES.md corpus/lessons/round-30.md corpus/evidence/sources-r30/S159.txt` lists only `ad0f047` touching `SOURCES.md` with 2 insertions at the round-24 search section (~line 211, below the S159 row). The lesson and the excerpt are unchanged since `ee61010`, so the judged bytes are the same at `ee61010` and at tip.

## 7. Tools

No install/update. System `curl 8.23.0` only. Scratch: `/fast/scratch/hyaku/mori-r30-w2/MoriR30.ReopenS159/` (headers.txt, edd3d943.patch, main.c, service-v190.txt, q1.txt, q2.txt).

## 8. Remaining unknowns

- Whether systemd actually restarts a killed earlyoom: `systemd.service(5)` was not opened this round, and the S159 row says so itself.
- The `teaches` consequence clause's truth therefore is not established by S159's bytes; I verified only that its parenthetical citation (S119 `main.c:161`) is real and is a version line.
