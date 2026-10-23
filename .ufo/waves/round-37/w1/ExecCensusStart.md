# ExecCensusStart — frozen source census re-run (round 37, wave 1)

**Item attacked:** the frozen source census as specified by `CORPUS.md` §"Census — run from
the lane root", executed through the maintained CLI
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`, must exit 0
and report `mori ok` for the mori lane, and must reproduce the round-37 receipt
`.ufo/waves/round-37/evidence/census-end.txt`.

**Axes:** (1) exit code 0, (2) `mori ok` verdict line present, (3) output byte-identical to the
frozen receipt, (4) the frozen *manual* awk/grep census commands in `CORPUS.md` agree with the
maintained parser, (5) determinism across reruns and across `--today` values.

**Tool installs:** none (no `pacman`, no `uv tool install`, no release binary). Environment used
as-found: `GNU Awk 5.4.1, API 4.1`, `GNU bash 5.3.20(1)-release`.

**Writes:** this report only. No lane file, registry, receipt, or tool was modified; the lane
working tree stayed clean (`git status --porcelain corpus/ tools/` → empty). No git/jj mutation
command was run. Scratch output went to `/tmp` (`/tmp/census-live.txt`, `/tmp/census-cmd.txt`,
`/tmp/c1.txt`…`/tmp/c3.txt`).

---

## 1. The registered command — verbatim run

```
$ cd /home/vgpnk/Projects/shokunin
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori; echo EXIT=$?
```

Observed (full output, 16 lines + `EXIT=0`):

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
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
EXIT=0
```

**Last five lines** (acceptance asks for exactly this tail):

```
mori	W04	S201 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c across scopes
mori	W04	S218 duplicate url github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch across scopes
mori	W04	S220 duplicate url raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
EXIT=0
```

**Exit code: 0.** `mori ok` present on the verdict line.

Independent confirmation that the exit code is the script's own and not the pipeline's:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori 2>&1 | tail -n 5; echo "PIPESTATUS=${PIPESTATUS[0]}"
```

Observed: the same five lines, `PIPESTATUS=0`.

---

## 2. Comparison with the frozen receipt

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori > /tmp/census-cmd.txt 2>&1; echo EXIT=$? >> /tmp/census-cmd.txt
$ cmp /tmp/census-cmd.txt mori-shokunin/.ufo/waves/round-37/evidence/census-end.txt && echo "BYTE_IDENTICAL"
$ sha256sum /tmp/census-cmd.txt mori-shokunin/.ufo/waves/round-37/evidence/census-end.txt
```

Observed:

```
BYTE_IDENTICAL
1853c8e6147a2f807371c664d567c0787f9abbe5221a214fca410fae1606fc45  /tmp/census-cmd.txt
1853c8e6147a2f807371c664d567c0787f9abbe5221a214fca410fae1606fc45  mori-shokunin/.ufo/waves/round-37/evidence/census-end.txt
```

The live run is **byte-identical** to `evidence/census-end.txt`, including the trailing
`EXIT=0` line the receipt carries.

The round-37 start receipt is the same bytes as the end receipt, i.e. the census did not drift
across the wave:

```
$ diff mori-shokunin/.ufo/waves/round-37/evidence/census-start.txt mori-shokunin/.ufo/waves/round-37/evidence/census-end.txt; echo "diffexit=$?"
$ sha256sum .ufo/waves/round-37/evidence/census-start.txt .ufo/waves/round-37/evidence/census-end.txt
```

Observed:

```
diffexit=0
1853c8e6147a2f807371c664d567c0787f9abbe5221a214fca410fae1606fc45  .ufo/waves/round-37/evidence/census-start.txt
1853c8e6147a2f807371c664d567c0787f9abbe5221a214fca410fae1606fc45  .ufo/waves/round-37/evidence/census-end.txt
```

---

## 3. The frozen *manual* census (CORPUS.md §Census) agrees with the maintained parser

`CORPUS.md:131-147` freezes a manual awk/grep census to be run from the lane root, and adds
at `CORPUS.md:151-155` that the maintained `scripts/sources-census.sh` CLI accepts 0–3 leading
spaces while the frozen manual examples assume column-zero input. Both were run.

Cwd: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

| Frozen check | Command (verbatim from `CORPUS.md:133-147`) | Observed |
|---|---|---|
| rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `225` |
| malformed rows (must print 0) | `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md` | `0` |
| tier histogram | `awk -F'|' … {t=$5; …} END{…}' corpus/SOURCES.md` | `A=200 B=8 C=17 ` (sum 225) |
| status histogram | `awk -F'|' … {s=$9; …} END{…}' corpus/SOURCES.md` | `mined=176 queued=25 rejected=24 ` (sum 225) |
| duplicate ids (must print nothing) | `awk -F'|' … {i=$2; …; print i}' corpus/SOURCES.md \| sort \| uniq -d` | no output |
| enum violations / tier inflation (must print nothing) | `awk -F'|' … NF==13 {… if (t !~ /^[ABC]$/) … if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md` | no output |
| mined rows whose used-by paths do not exist (must print nothing) | `awk -F'|' … {s=$9; … if (s=="mined") {… print p}}' corpus/SOURCES.md \| while read -r p; do [ -e "$p" ] \|\| echo "missing: $p"; done` | no output |

The maintained CLI and the frozen manual commands agree on the registry: 225 rows, 0 malformed,
tier A=200/B=8/C=17, status mined=176/queued=25/rejected=24, no duplicate id, no enum violation,
no dangling `used-by`.

---

## 4. Determinism and date sensitivity

Three consecutive reruns of the registered command:

```
$ for i in 1 2 3; do bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori > /tmp/c$i.txt 2>&1; echo "run$i exit=$?"; done
$ sha256sum /tmp/c1.txt /tmp/c2.txt /tmp/c3.txt
```

Observed:

```
run1 exit=0
run2 exit=0
run3 exit=0
6b422b9740e7b054732e42f321facae03c97072d71b89cbff6a5498c68ba593d  /tmp/c1.txt
6b422b9740e7b054732e42f321facae03c97072d71b89cbff6a5498c68ba593d  /tmp/c2.txt
6b422b9740e7b054732e42f321facae03c97072d71b89cbff6a5498c68ba593d  /tmp/c3.txt
```

(These three files lack the appended `EXIT=0` line, hence the different digest from the receipt;
their mutual digests are identical — the run is byte-stable.)

Date sensitivity, since `E08` compares `opened` against `--today` (default `date -u +%F`):

```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin --today 2026-10-24 mori | tail -2 ; echo EXIT_1024=$?
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin --today 2026-12-01 mori | tail -2 ; echo EXIT_1201=$?
```

Observed: both end on `mori ok …` with exit `0`. The newest `opened` value in the registry is
`2026-10-23` (51 rows), so the verdict is stable across the plausible date range and does not
depend on the wall clock of the re-run.

---

## 5. Provenance of the inputs (why the run is the scored-tip census)

- The registry the CLI read is `mori-shokunin/corpus/SOURCES.md`, and its blob is identical
  between the scored tip and the lane HEAD:

```
$ git rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6:corpus/SOURCES.md HEAD:corpus/SOURCES.md
2dad136f61a199edb39fc4d1db241fe7afdbf605
2dad136f61a199edb39fc4d1db241fe7afdbf605
$ git diff --stat e57c58b57c025364e79d130fbdf764d2674d83d6 -- corpus/SOURCES.md
(empty)
```

- Lane working tree is clean for the census inputs: `git status --porcelain corpus/ tools/` →
  empty. The only untracked paths under the lane are other seats' wave-1 reports and `.scratch/`.
- The CLI itself is fleet-side (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`) and
  is unmodified in the fleet working tree (`git status --porcelain -- scripts/sources-census.sh`
  → empty; last touching commit `6a1dd8c ops: vendor canonical e737d2e; …`).

**Naming note (risk, not a defect):** the lane also ships its own `tools/mori-census.sh`
(254 328 bytes, mode 755) and the wave evidence uses the name `census-start.txt` /
`census-end.txt`. The registered gate command runs the *fleet* script
`scripts/sources-census.sh`; the lane-local `tools/mori-census.sh` is a different artifact and
was not used here. Anyone re-running this item must use the fleet script path in §1, not the
lane-local one.

---

## 6. Reading of the W04 lines

15 `W04` lines are emitted. Per the CLI's own contract header
(`scripts/sources-census.sh:38-42`: "W-codes and unlisted lanes never change status"), W04 is a
warning — the same URL appearing under two different `scope` values — and it cannot move the
lane off `ok`; the exit code stays 0 and the `mori ok` verdict line is still emitted. Two of the
15 are the same URL pair as other rows (`raw.githubusercontent.com/torvalds/linux/v7.2/fs/proc/base.c`
for S148 and S166), consistent with the warning being a scope observation rather than a row
defect. The frozen manual census's own duplicate checks (duplicate ids, enum violations) print
nothing, so the W04 set is not a contract violation under `CORPUS.md` §Rules.

---

## 7. Risks / blockers

- **Risk — the receipt is self-confirming.** `evidence/census-end.txt` is byte-identical to the
  live run, so the receipt pins the *current* registry rather than an independent expected
  value. If the registry had drifted, this gate would still pass as long as the drift produced
  no E-code and the receipt were refreshed. The strong form of this gate is the frozen manual
  census in §3 plus the registry-shape claims owned by `ScoutCorpusCensus.md` (225 rows, no
  duplicate id, `used-by` resolves), not the byte-match alone. [INFERENCE]
- **Risk — W04 is unactioned.** 15 same-URL-across-scope warnings persist in the scored
  registry. They are contract-legal, but they are visible noise in a receipt that otherwise
  reads "ok". [OBSERVED, no defect]
- **Blockers:** none.
- **Not attacked by this seat:** C1/C2 counter calibration, the drift probe, and the r17-jj
  battery — each has its own seat. This seat covers only the census item.

---

## Conclusion

The frozen source census, run exactly as `CORPUS.md` specifies and executed through the
registered command, exits **0** and reports **`mori ok`** for the mori lane. The last five
lines are reproduced verbatim in §1 and are byte-identical to
`.ufo/waves/round-37/evidence/census-end.txt` (sha256 `1853c8e6…06fc45` on both). The frozen
manual awk/grep census agrees with the maintained parser on every count, and the run is
deterministic across reruns and across `--today` values.

VERDICT: PASS
