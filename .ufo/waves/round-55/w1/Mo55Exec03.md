# Mo55Exec03 — sources-census end check (round 55, wave w1)

role: executor (leaf) · lane mori-shokunin · reportDir `.ufo/waves/round-55/w1`
scope: re-run the sources-census end check and inspect registry row ids / used-by paths. Read-only; no source edits, no git/jj mutation, no production writes.

## Measurement point

| item | value |
|---|---|
| lane repo | `/home/vgpnk/Projects/shokunin/mori-shokunin` |
| lane HEAD at run | `b8a70adf93ebd9d1e4e95bef8627a220f2fa816b` ("round-55: publish w1 ready marker") |
| data revision named by L1 | `b8b7064c2b54c8b6b22c288232a96c43fae1af47` |
| `corpus/SOURCES.md` blob @ `b8b7064c` | `ef37c1533e6f9dc9edc2cec4fc2be77173ae3b5e` |
| `corpus/SOURCES.md` blob @ HEAD | `ef37c1533e6f9dc9edc2cec4fc2be77173ae3b5e` |
| `corpus/SOURCES.md` worktree blob | `ef37c1533e6f9dc9edc2cec4fc2be77173ae3b5e` |
| census tool | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (35466 B, sha256 `3fb7261569f46423…`) |
| disk guard before/after | `/fast/scratch/hyaku` 26% used, 594.5 G free — no ENOSPC condition |

The registry bytes the census reads are identical at the data revision, at HEAD and in the working tree, so the end check binds to the L1-named data commit even though two knowledge files carry uncommitted sibling edits (`corpus/knowledge/disk-runway-enospc-r55.md` +1/−1, `corpus/lessons/round-55.md`). Census `validate` parses only registry row fields and used-by existence, so those content edits cannot change its verdict.

## Command and exit

```
cd /fast/scratch/hyaku/mori-r55/Mo55Exec03
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
```

- exit status: **0** (fresh run, `2026-10-27`)
- stderr: empty (0 bytes)
- stdout: 24 lines, tab-separated, trailing newline present

## Exact stdout (verbatim, tabs preserved)

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
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	W04	S228 duplicate url docs.python.org/3/library/os.path.html across scopes
mori	W04	S349 duplicate url www.openeuler.org/whitepaper/openEuler%2024.03%20LTS%20%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf across scopes
mori	W04	S351 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S470 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
mori	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori	W04	S492 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```
then `exit=0`.

## Comparison with the frozen receipts

- `sha256(.ufo/waves/round-55/evidence/census-start.txt)` = `611391325d4d0d20…`, 2580 B, trailing newline.
- `sha256(.ufo/waves/round-55/evidence/census-end.txt)` = `611391325d4d0d20…`, 2580 B, trailing newline — **the start and end receipts are byte-identical**.
- Fresh run + literal `exit=0` line: byte-identical to `evidence/census-start.txt` (`diff` empty).
- Fresh run + literal `exit=0` line: byte-identical to `evidence/census-end.txt` (`diff` empty).
- Round-54 defect D1 (transcribed census receipt with spaces and a `%E7%99%BD%E6%96%87%E6%9C%AC` truncation) does **not** reproduce here: round-55 end receipt is mechanical tab-separated output, byte-equal to my re-run, and carries the full `%E7%99%BD%E7%9A%AE%E4%B9%A6` S349 escape.

Identical start and end output is the expected result: no `corpus/SOURCES.md` change landed between the census-start capture and now (blob `ef37c153` throughout), so the warning set is the same 23 W04 lines and the single `ok` line.

## Row ids and used-by paths (independent parse)

Independent re-derivation from `corpus/SOURCES.md` (plain Python, not the census tool):

| check | result |
|---|---|
| registry row-shaped lines | 316 |
| field count per row | 316/316 rows NF=11 (contract NF=13 incl. empty edge cells) |
| duplicate ids | none |
| used-by entries (comma groups expanded) | 361 checked, 0 missing on disk, 0 empty groups |
| used-by = `—` | 48 rows (all `status=queued|rejected`-style, no E11 exposure) |
| `census` mode totals | `rows 316 · tier.A 285 · tier.B 14 · tier.C 17 · status.mined 265 · status.queued 24 · status.rejected 27 · invalid 0 · missing 0`, exit 0 |

### W04 rows (23 lines, 18 distinct URLs)

Every W04 message names an S-id that exists in the registry, and each named URL genuinely occurs under ≥2 distinct scopes (18 distinct URLs; the 5 repeats are URLs shared by 3+ rows). Sample: S035 scopes `systemd message identifiers for coredumps, kernel OOM and systemd-oomd kills` / `structured process-termination and unit-result message identifiers`; S073 scopes `lexical versus resolved path containment and the symlink caveat` / `symlink caveat of lexical containment only (narrowed from S069)`. The W04 lines are warning-code only; per the tool contract they never change lane status, and exit stayed 0.

### Round-55 source rows

- C1 sources: `S502` (tier A, mined; used-by r53 recheck, memory-failure-kills-r54, kernel-v7.3-recheck-r55), `S516` (tier A, mined; used-by r54 + r55 recheck), `S526`–`S534` (tier A, mined; used-by `corpus/knowledge/kernel-v7.3-recheck-r55.md`).
- C2 sources: `S535`–`S543` (tier A, mined; used-by `corpus/knowledge/disk-runway-enospc-r55.md`) — 9 rows, matching C2's "9 sources".
- All 20 rows are `status=mined`, tier A, non-dash used-by, and their used-by targets exist.
- `corpus/knowledge/kernel-v7.3-recheck-r55.md` references 11 S-ids (`S502 S516 S526 S527 S528 S529 S530 S531 S532 S533 S534`); `corpus/knowledge/disk-runway-enospc-r55.md` references 9 (`S535`–`S543`). All 20 referenced S-ids resolve to registry rows; none absent.
- Anchor copies with `sha256 <prefix>` and `copy corpus/evidence/…` for all 44 `S5xx` rows: file present and sha256 prefix matches in 44/44 cases (0 absent, 0 mismatch).

## Verdict

End census: **exit 0**, warning-only (23 × W04), no `E` codes, no missing registry, no dangling used-by. The contract requirement "End census must exit 0" is satisfied at the working tree whose registry blob equals the L1-named data commit `b8b7064c`.

## Findings

| severity | finding | evidence |
|---|---|---|
| none (pass) | end census exits 0 with 23 W04 warnings and `mori ok`; output reproduces byte-for-byte | this report, "Exact stdout"; `.ufo/waves/round-55/evidence/census-end.txt` (sha256 `611391325d4d0d20…`) |
| none (pass) | start/end receipts byte-identical and mechanically captured; round-54 D1 does not recur | `evidence/census-start.txt` vs `evidence/census-end.txt`, both 2580 B / `611391325d4d0d20…` |
| none (pass) | 316 rows, NF=11 everywhere, no duplicate ids, 361/361 used-by paths resolve | this report, "Row ids and used-by paths" |
| note (informational) | census measured the working tree at HEAD `b8a70adf`, not literally commit `b8b7064c`; equivalence holds because `corpus/SOURCES.md` blob is `ef37c153` at both | this report, "Measurement point" |
| note (informational) | two files carry uncommitted sibling edits (`disk-runway-enospc-r55.md`, `round-55.md`); they do not affect validate, which reads registry rows and path existence only | `git status --porcelain` at run |
