# Mo54ExecMisrootSweep — misroot pre-sweep (read-only)

Seat: `Mo54ExecMisrootSweep`, round-54 wave `w1`, mori-shokunin lane. Executed 2026-10-27, 01:41–01:56 -03:00 on the
host running kernel 7.2.11 (MACHINE_ID omitted by rule). Scope: (A) enumerate untracked files at the fleet root and
under `/home/vgpnk/Projects/shokunin/.ufo` that could belong to mori round 54; (B) verify the D3 relocation receipt
against the data tip `78295c764093ff1f6cee08d7246679900bde7265`. No mutation of the fleet repo, the lane repo, the
lane's jj state or any git index; no file deleted; no host write; no pacman; no tool installed.

Scratch: `/fast/scratch/hyaku/mori-r54/Mo54ExecMisrootSweep/` (`TMPDIR` set there); removed at the end. Only
`git`-read verbs used (`status`, `show`, `cat-file`, `ls-tree`, `log`, `diff`, `rev-parse`, `check-ignore`,
`ls-files`).

## A. Untracked enumeration

Commands and their literal readings:

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain        # rc=0, stderr empty
?? e
?? o

$ git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all | wc -l
2
$ git -C /home/vgpnk/Projects/shokunin status --porcelain --ignored=matching --untracked-files=normal | grep -c '^ M'
0
$ git -C /home/vgpnk/Projects/shokunin check-ignore -v e o        # rc=1 (neither is ignored)
$ ls -1 /home/vgpnk/Projects/shokunin/.ufo/waves                  # no round-54 entry
$ ls -la /home/vgpnk/Projects/shokunin/.ufo/waves/round-54
ls: cannot access '.ufo/waves/round-54': No such file or directory
```

- Fleet root carries **no untracked directory tree** with round-54 content: the fleet-root `.ufo/waves` has no
  `round-54` and `git status --untracked-files=all` returns exactly two paths, both files.
- No tracked fleet-root file is modified (`^ M` count 0), so the fleet-root tracked tree was not touched during w1.
- `mori-shokunin/` is a **separate repository** (`git -C mori-shokunin rev-parse --show-toplevel` →
  `/home/vgpnk/Projects/shokunin/mori-shokunin`); the fleet root ignores it by the `.gitignore` pattern
  `*-shokunin/`, which is why none of the lane's writes appear above.
- Lane-repo untracked set (read-only, for the misroot class that round 28 produced — files at the *lane root*):
  51 untracked entries, **0 outside `.ufo/waves/round-54/`**:

```
$ git -C $LANE status --porcelain --untracked-files=all | grep '^??' | awk '{print $2}' \
    | grep -vc '^\.ufo/waves/round-54/'
0
$ git -C $LANE status --porcelain --untracked-files=all | grep -c '^??'
51
```

So the answer to the assignment's question — untracked files that could belong to mori round 54 — is **none at the
fleet root and none under the fleet-root `.ufo`**. The two fleet-root paths that do exist are foreign (below), and
the lane's untracked files are all inside its own wave directory, which is where they belong.

### Foreign untracked strays at the fleet root (reported, not touched)

| path | size | sha256 | birth (stat %w) |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/e` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-27 01:42:32.663910379 -0300 |
| `/home/vgpnk/Projects/shokunin/o` | 115 | `f846b4ff9ef8e545666709775def4999fbaf3118efc9601359309182eca46abe` | 2026-10-27 01:42:32.663910379 -0300 |

Both are mode 644 regular files with the *same* birth timestamp and were written within the same millisecond-second
window (`e` mtime .708910301, `o` mtime .712910294): one command with two shell redirections executed with the fleet
root as cwd. `e` is empty; `o` holds, verbatim (`cat -A`, `$` = newline):

```
keysym: eacute (0x00e9)$
$
=== Direct access ===$
$
KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS$
```

Content attribution (no mori token): `grep -l -i -E 'mori|round.?54|Mo54' e o` → no match, rc 1. Both files are
`xkbcli how-to-type` output — the header line is a literal of the xkbcli sub-binary:

```
$ grep -a -c '=== Direct access ===' /usr/lib/xkbcommon/xkbcli-how-to-type
1                                    # rc=0
$ xkbcli how-to-type                 # rc=0, usage on stderr names that same sub-binary
ERROR: missing positional parameter
Usage: /usr/lib/xkbcommon/xkbcli-how-to-type [--help] [--verbose] [--keysym] ...
```

The argument `eacute (0x00e9)` is the keysym/codepoint a probe queried. Which seat wrote them is **UNVERIFIED**:
`grep -rl -E 'how-to-type|xkbcli'` over the fleet-root `.ufo/waves` tree returned nothing, and the same grep over
`$LANE/.ufo/waves/round-54` returned nothing, so no report in either tree names this probe; the producer is either a
live seat of another lane whose report is not yet written, or a seat that never recorded the write. No
`Mo54`/mori/round-54 report path appears in either file. They are left in place (host guard: never touch other
lanes' files; only the orchestrator may remove them).

### Empty directories (invisible to `git status`, informational)

| path | entries | mtime | note |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/ok/` | 0 | 2026-10-25 16:43 | predates round 54; not tracked (empty dirs are unrepresentable in git) |
| `/home/vgpnk/Projects/shokunin/.ufo-scratch/RevengerAuditorHistory/` | 0 | 2026-10-25 07:41 | same; `.ufo-scratch` has 0 tracked files |

Neither is round 54's, and neither is the round-38 `--repo/` case (below). Not touched.

## B. D3 relocation verified at the data tip

For each line of `evidence/d3-relocation.txt` I compared the blob at the old path at the entering tip
`39dcf4d7e410d362781a47e8365ca23b5c807598` with the blob at the new path at `78295c76…`, checked the old path's
absence at `78295c76…`, compared the new-path blob with the working-tree file, and read git's own rename detection
over `39d..782`. Every column passes; every sha matches the receipt's own sha.

| old path (lane root @39dcf4d7) | new path (@78295c76) | sha256 old = new = receipt | old absent @782 | `git diff --name-status` | disk == git |
|---|---|---|---|---|---|
| `base.c` | `.ufo/waves/round-28/misroot-lane-root/base.c` | `cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6` | yes | `R100` | yes |
| `main.c` | `.ufo/waves/round-28/misroot-lane-root/main.c` | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | yes | `R100` | yes |
| `meminfo.c` | `.ufo/waves/round-28/misroot-lane-root/meminfo.c` | `526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb` | yes | `R100` | yes |
| `oom_kill.c` | `.ufo/waves/round-28/misroot-lane-root/oom_kill.c` | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | yes | `R100` | yes |
| `sd-main.c` | `.ufo/waves/round-28/misroot-lane-root/sd-main.c` | `5ecdca43a8e0ed088758b228b54c72df311c0b9dc3855721ed02c5b169d3aae3` | yes | `R100` | yes |
| `user@.service.in` | `.ufo/waves/round-28/misroot-lane-root/user@.service.in` | `72c2f40dcfced1d85bcc17583715966fc8a552b68af44404c213de2ea320504c` | yes | `R100` | yes |
| `MANPAGE.md` | `.ufo/waves/round-28/misroot-lane-root/MANPAGE.md` | `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda` | yes | `R100` | yes |
| `0` | `.ufo/waves/round-38/misroot-lane-root/0` | `b24122a0f0245c0aa6961fa234fb40adc4527bcd8e61c3c1e247ec8ba1c3a078` | yes | `R100` | yes |

Literal readings behind the table:

```
$ git -C $LANE show 39dcf4d7:base.c | sha256sum
cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6  -
$ git -C $LANE show 78295c76:.ufo/waves/round-28/misroot-lane-root/base.c | sha256sum
cef1a2cf3f34f683e69d623c4df563d5c0dc6bd71dcb3d42f40dadb0084915c6  -
$ git -C $LANE cat-file -e 78295c76:base.c ; echo $?
128                                   # absent at the data tip
$ git -C $LANE diff --name-status 39dcf4d7 78295c76 -- base.c main.c meminfo.c oom_kill.c sd-main.c \
    'user@.service.in' MANPAGE.md 0 .ufo/waves/round-28/misroot-lane-root .ufo/waves/round-38/misroot-lane-root
R100	MANPAGE.md	.ufo/waves/round-28/misroot-lane-root/MANPAGE.md
R100	base.c	.ufo/waves/round-28/misroot-lane-root/base.c
R100	main.c	.ufo/waves/round-28/misroot-lane-root/main.c
R100	meminfo.c	.ufo/waves/round-28/misroot-lane-root/meminfo.c
R100	oom_kill.c	.ufo/waves/round-28/misroot-lane-root/oom_kill.c
R100	sd-main.c	.ufo/waves/round-28/misroot-lane-root/sd-main.c
R100	user@.service.in	.ufo/waves/round-28/misroot-lane-root/user@.service.in
R100	0	.ufo/waves/round-38/misroot-lane-root/0
```

Additional readings:

- **Introducing commit.** `git log --diff-filter=A -1 78295c76 -- <each new path>` returns `1116c092` for all
  eight, i.e. the round-54 *data* commit, matching the receipt's authorship time 2026-10-27T01:33:08-03:00 and the
  contract's routing (D3 lands with the data, not with the freeze `6830f3af`).
- **Lane root is clean of the stray class.** Top-level `ls-tree` at `39dcf4d7` lists the eight stray names plus the
  ordinary tree; at `78295c76` those eight names are gone and **no new top-level entry appeared** (`.gitignore`,
  `.scratch`, `.ufo`, `AGENTS.md`, `LOG.md`, `MINT.md`, `PROVINCE.md`, `README.md`, `SCORECARD.md`, `SHONEN.md`,
  `SKILL.md`, `considerthese`, `corpus`, `tools`). The lane working tree has none of the eight names at the lane
  root either (`test -e` → absent for all eight), and each new-location file's disk bytes equal the `78295c76` blob.
- **`--repo/`.** `git ls-tree -r --name-only | grep -c '^--repo/'` = 0 at `39dcf4d7` **and** 0 at `78295c76`
  (it was never tracked, as the receipt states); `ls -ld $LANE/--repo` → `No such file or directory` (rc 2). Git
  cannot record an empty directory, so its removal is provable only from the disk absence plus the never-tracked
  counts — which is exactly what the receipt line claims.
- **Freeze commit present.** `git -C $LANE cat-file -t 6830f3af…` → `commit`.
- **Anchoring.** The lane HEAD advanced while this seat was reading (from `78295c76` to `2d0347a3`, "round-54: wave
  w1 spec (74 seats, v2 validated: 24 voters, 39 attack seats), dispatch payload, at-data receipts"). The
  verification above is anchored at `78295c76` as instructed; I re-checked the eight old paths at `2d0347a3` —
  `cat-file -e HEAD:<old>` fails for all eight, so the relocation is still in force at the newer tip.
- **LOG entry.** `grep -n -i -E 'round.54|misroot|D3' $LANE/LOG.md` shows the newest hit at the round-53 section
  (line 2882 region, `Planned (round 54)`); no round-54 misroot/relocation entry exists yet, and `LOG.md` is absent
  from the lane's modified list (`PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`,
  `corpus/SOURCES.md`, `corpus/knowledge/kernel-v7.3-recheck-r54.md`). The contract asks D3 to land "with a LOG
  entry"; that is still owed by the L1 at integration — not a defect in the relocation itself.

## C. Limits of this sweep

- Read-only throughout. The two foreign strays and the two empty directories are left in place for the L1; deleting
  them is outside a leaf seat's remit and outside this seat's path allowance.
- Producer identity for `e`/`o` is content- and string-derived only; no report in the fleet `.ufo/waves` tree or in
  the lane's round-54 tree names that probe (both greps empty), so which live seat redirected into the fleet root is
  UNVERIFIED.
- `git status` cannot see empty directories; the two empty dirs above come from `ls -A` entry counts, not from git.
- The D3 result is blob equality between the contract's entering tip and the data tip plus working-tree equality; it
  does not re-derive that the `39dcf4d7` blobs are the *original* round-28/round-38 strays beyond that tip being the
  contract's baseline. The receipt's `cmp=ok` per line and its sha values are confirmed independently.
- I ran neither counter, so nothing here scores C1 or C2; the ledger's and the entry's own content was not judged.
- No host state was read for this seat beyond `stat`/`ls` on the two strays and the xkbcli binaries; the host-read
  items of the wave belong to other seats.

## Findings

1. **MED — fleet-root untracked strays `e` and `o` produced during w1 by an unidentified live seat.**
   `/home/vgpnk/Projects/shokunin/e` (0 bytes, `e3b0c442…b855`) and `/home/vgpnk/Projects/shokunin/o`
   (115 bytes, `f846b4ff…6abe`), both born 2026-10-27 01:42:32.663910379, content is `xkbcli how-to-type` output for
   `eacute (0x00e9)` (`grep -a -c '=== Direct access ===' /usr/lib/xkbcommon/xkbcli-how-to-type` → 1). Neither
   names mori, round 54, `Mo54` or a lane path, so they are **not mori round-54 data**; they are fleet-root
   pollution of exactly the class this sweep exists to catch, caused by a command whose cwd was the fleet root
   instead of a seat scratch dir. Route to the orchestrator for removal/attribution; not touched here.
2. **LOW — origin of the strays is unrecorded.** No file under the fleet-root `.ufo/waves` tree or the lane's
   `.ufo/waves/round-54` mentions `how-to-type` or `xkbcli` (both greps empty), so the seat that wrote `e`/`o` filed
   no evidence of it. Producer identity UNVERIFIED.
3. **LOW — `/home/vgpnk/Projects/shokunin/ok/` is an empty untracked directory** (0 entries, mtime 2026-10-25
   16:43). Invisible to `git status`; predates round 54; not the round-38 `--repo/` case.
4. **LOW — `/home/vgpnk/Projects/shokunin/.ufo-scratch/RevengerAuditorHistory/` is an empty directory**
   (0 entries, mtime 2026-10-25 07:41) under an untracked-and-empty parent. Invisible to `git status`; not round 54's.
5. **LOW — no lane LOG entry for the D3 relocation yet** (`LOG.md` unmodified at `2d0347a3`; newest
   `round 54`/`misroot` grep hit is the round-53 section). The contract requires the relocation "with a LOG entry";
   owed at L1 integration. Concerns `mori-shokunin/LOG.md`.
6. **PASS (no finding) — D3 relocation verified 8/8.** All eight old paths absent at `78295c76` and at `2d0347a3`,
   all eight new paths byte-identical to the old blobs and to the receipt's sha256, all eight detected as `R100`,
   the lane root gained nothing, and `--repo/` is absent on disk and was never tracked. Concerns
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/evidence/d3-relocation.txt`.
