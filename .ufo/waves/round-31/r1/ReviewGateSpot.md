# ReviewGateSpot — round-31 Gate discernment spot-check

Seat: `MoriR31.ReviewGateSpot` (non-author reviewer).
Pinned: `a29f3e3f7f7259afb07df29c5ee8f68882712e96` (lane HEAD == tip; `git status --porcelain`
clean for `corpus/SOURCES.md` and `corpus/lessons/round-31.md`, so working tree = committed bytes).
Gate text: `corpus/lessons/round-31.md:45-69`. SOURCES rows: `corpus/SOURCES.md:167,170,172,174,176,178,180`.

## Method

- Re-fetched all 7 assigned URLs with `curl -fsSL` on 2026-10-22, compared `sha256sum` to the Gate cell.
- Whitespace-normalized each admitted quote (`" ".join(s.split())`) and substring-checked it against the
  whitespace-normalized stated line range of the fetched bytes; counted whitespace tokens vs. stated word count.
- Pulled each id's SOURCES row at tip; compared URL, `status`/`tier` cells, and assessed whether `teaches` is
  supported by the located quotes (anchor coverage also noted).
- Reject reasons tested against `git show a12c68ae:corpus/SOURCES.md` (pre-round registry) and
  `round-30.md:134` at tip.
- Cross-checked committed `corpus/evidence/sources-r31/S###.src` bytes against live fetches.

## Results

| id | decision | agree? | reason |
|---|---|---|---|
| S161 | admit, A, mined | yes | sha256 `c2024c38…` matches live fetch and committed `S161.src`. All 3 quotes verbatim at `pgrep.1:105-108` (21w), `:305` (10w), `:318-324` (19w); counts exact, ≤25. SOURCES:167 same URL, tier A, `status: mined`; anchor `103-108, 294-311, 318-324` covers all quote lines; teaches (name-by-default vs `-f` full cmdline, probe-error exits, self-exclusion) is directly supported by q1/q3. |
| S164 | admit, A, mined | yes | sha256 `44e4185b…` matches fetch + evidence. Both quotes verbatim at `exec.c:1096` (7w) and `:1257` (3w). SOURCES:170 same URL, `status: mined`, sha recorded; anchor names `strnlen:1096` and `kbasename:1257` explicitly; teaches (comm = basename of execve path, truncated to comm-buffer−1) is supported by both quotes. Consistent with Gate:50 — dropped sub-3-word `:1253` quote, kept `:1257` at exactly 3 words. |
| S166 | reject | yes | sha256 `cef1a2cf…` matches fetch. Reason verified at `a12c68ae`: `SOURCES.md:133` (S127) and `:154` (S148) both carry `raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c` and record the identical sha `cef1a2cf3f34f683…4915c6` — bytes, not just URL, already admitted. Round-30 precedent: `round-30.md:134` is the S158 row, which does reject a URL "already shown inside a SOURCES row" (S154) — cited accurately. SOURCES:172 self-consistently `status: rejected`. No `S166.src` committed — consistent with Gate:48 ("every admit row's bytes are committed"). |
| S168 | reject | yes | sha256 `e760f716…` matches fetch. `a12c68ae` `SOURCES.md:88` (S082) carries the exact `proc.rst` URL at v7.2 with recorded sha256 `e760f716f8278dee` — the stated prefix, byte-identical to the fresh fetch. SOURCES:174 `status: rejected`, reason restated correctly. No `S168.src` committed — consistent. |
| S170 | admit, A, mined | yes | sha256 `a9f3b83b…` matches fetch + evidence. All 3 quotes verbatim at `proc_pid_cmdline.5:13-14` (17w), `:16-17` (21w), `:33-37` (19w). SOURCES:176 same URL incl. `?h=man-pages-6.20`, `status: mined`; anchor covers `:13-14, :16-17, :33-40` ⊃ stated lines; teaches (self-reported writable cmdline, zombie 0-byte read can't distinguish dead watchdog) supported by q2+q3. |
| S172 | admit, A, mined | yes | sha256 `f2ac57cc…` matches fetch + evidence. All 3 quotes verbatim at `PR_SET_NAME.2const:26-29` (21w), `:34-35` (19w), `:53-57` (11w). SOURCES:178 same URL, `status: mined`; anchor `:26-29, :31-35, :53-57` covers stated lines; teaches (self-set ≤16-byte name, silent truncation, EFAULT-only, comm-not-identity) supported by q1/q2/q3. |
| S174 | admit, A, mined | yes (nit) | sha256 `509fd950…` matches fetch + evidence. All 3 quotes verbatim at `proc_locks.5:46-48` (Gate says 12w, actual 13 whitespace tokens — see nit), `:80` (9w), `:93` (9w). SOURCES:180 same URL, `status: mined`; anchor `:46-48, :79-80, :91-93` ⊃ stated lines; teaches (read-only PID-of-flock-holder identity anchor) supported. |

## Nits (cosmetic, no decision impact)

1. **S174 first quote labeled "(12 words)"** — whitespace-token count is 13
   (`.B` `FLOCK` `This` `is` `a` `BSD` `file` `lock` `created` `using` `.BR` `flock` `(2).` = 13).
   Either way ≤25 and verbatim; the word-count annotation is off by one under naive splitting.
2. Gate `accessed` timestamps all cluster at `2026-10-22T23:43:0xZ` — plausible for a single sweep; no issue.

## Reject-reason summary

Both rejects are true and byte-provable: S166's base.c bytes already live under S127/S148
(`a12c68ae` rows 133/154, same sha); S168's proc.rst bytes live under S082 (`a12c68ae:88`, same sha prefix
recorded). The round-30 precedent citation resolves to a genuine duplicate-URL reject row.

## Census validator

`$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`

```
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	W04	S147 duplicate url raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md across scopes
mori	W04	S148 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S149 duplicate url man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html across scopes
mori	W04	S150 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.exec.xml across scopes
mori	W04	S166 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c across scopes
mori	W04	S168 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Exit code: **0** (warnings only). Note the validator's own W04 warnings independently confirm the S166/S168
duplicate-URL facts — and flag S148, which is exactly why S166 was rejected. Validator ran against the working
tree, which equals tip bytes for `corpus/SOURCES.md` (porcelain clean).

## Verdict

**Agree with all 7 Gate decisions.** Every sha256 cell matches a fresh fetch (2026-10-22) and the committed
evidence file; every admitted quote is verbatim at its stated lines whitespace-normalized and ≤25 words; every
SOURCES row carries the same URL, `mined`/`rejected` status consistent with the Gate decision, a `teaches` cell
the quotes support, and anchors covering the quoted lines; both reject reasons are factually true at `a12c68ae`.
Only finding: one cosmetic word-count annotation off by one (S174, 12→13 tokens).
