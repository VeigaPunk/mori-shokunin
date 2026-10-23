# Sources & frontier; Trend verdicts

Item attacked: the round-37 SOURCES census, frontier evidence, and learning-trend verdicts, using only the entering commit `842a32074b5c7972e9728f3f629d83eb92f127c2` and scored tip `e57c58b57c025364e79d130fbdf764d2674d83d6`.

## Sources & frontier

### Committed-row census

The following read-only command reads both `corpus/SOURCES.md` versions from Git objects, counts registry rows, groups the added rows by tier/kind/status, and compares each prior row in full:

```sh
python3 -c '
import collections, re, subprocess
repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
revs = ("842a32074b5c7972e9728f3f629d83eb92f127c2", "e57c58b57c025364e79d130fbdf764d2674d83d6")
def rows(rev):
    text = subprocess.check_output(["git", "-C", repo, "show", rev + ":corpus/SOURCES.md"], text=True)
    out = {}
    for line in text.splitlines():
        if re.match(r"^\|\s*S\d{3}\s*\|", line):
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            out[cells[0]] = cells
    return out
old, new = [rows(rev) for rev in revs]
added = sorted(set(new) - set(old))
common = set(old) & set(new)
changed = sorted(row_id for row_id in common if old[row_id] != new[row_id])
immutable = sorted(row_id for row_id in common if [v for i, v in enumerate(old[row_id]) if i not in (7, 9, 10)] != [v for i, v in enumerate(new[row_id]) if i not in (7, 9, 10)])
print("before=%d after=%d added=%d ids=%s" % (len(old), len(new), len(added), ",".join(added)))
print("tier=%s kind=%s status=%s" % (dict(sorted(collections.Counter(new[i][3] for i in added).items())), dict(sorted(collections.Counter(new[i][2] for i in added).items())), dict(sorted(collections.Counter(new[i][7] for i in added).items()))))
print("existing_rows_changed=%s immutable_fields_changed=%s" % (changed, immutable))
'
rc=$?; printf 'EXIT_CODE=%s\n' "$rc"; exit 0
```

Observed output:

```text
before=220 after=225 added=5 ids=S221,S222,S223,S224,S225
tier={'A': 4, 'B': 1} kind={'docs': 3, 'spec': 2} status={'mined': 5}
existing_rows_changed=[] immutable_fields_changed=[]
EXIT_CODE=0
```

Thus the five additions are S221 (A/spec/mined), S222 (B/docs/mined), S223 (A/docs/mined), S224 (A/docs/mined), and S225 (A/spec/mined). No pre-existing row changed, including the mutable status/recheck/used-by cells. Row pointers: `corpus/SOURCES.md:227-231`.

Round-specific append-only check:

```sh
python3 tools/mori-sources-appendonly.py e57c58b57c025364e79d130fbdf764d2674d83d6 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --round-base 842a32074b5c7972e9728f3f629d83eb92f127c2
```

Observed summary: `appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]`; exit code **0**. These are historical supersession/identity findings, not edits in this round; `round_changed=[]` and the full-row comparison above show no old row changed between the specified commits.

### Frontier advancement and evidence limits

`corpus/README.md:46` adds the coverage-map row for `knowledge/source-drift-hardening-r37.md`. The new note cites S221–S225 and describes the 4 MiB bounded read and post-redirect public-destination check, with the named `huge_cap` and `redirect_private_refused` arms and their intended mutation kills (`corpus/knowledge/source-drift-hardening-r37.md:1-12,25-58`). `git diff --name-status 842a32074b5c7972e9728f3f629d83eb92f127c2 e57c58b57c025364e79d130fbdf764d2674d83d6 -- corpus/knowledge` returned only `A corpus/knowledge/source-drift-hardening-r37.md`.

The scored tip has evidence gaps that constrain what can be claimed:

- `git ls-tree -r --name-only e57c58b57c025364e79d130fbdf764d2674d83d6 -- corpus/evidence/sources-r37` listed `S221.src`, `S222.src`, `S223.src`, and `S224.src` only. `S225.src` is absent from the scored tip, despite S225 at `corpus/SOURCES.md:231` and the note's S225 citation at `corpus/knowledge/source-drift-hardening-r37.md:3-7`.
- The committed live receipt records `MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162` and `EXIT=1` (`.ufo/waves/round-37/evidence/drift-live-r37.txt:221-222`). The documented command is `python3 tools/mori-source-drift.py --root .` (`corpus/knowledge/source-drift-hardening-r37.md:62-65`). Its receipt contains S001–S220 only, so it does not evidence a live sweep of the final 225-row registry or the five new rows.
- `git ls-tree -r --name-only e57c58b57c025364e79d130fbdf764d2674d83d6 -- .ufo/waves/round-37` contains no `evidence/c1-after.txt` or `evidence/c2-after.txt`, although the knowledge note points to `c2-after.txt` for the mutation results (`corpus/knowledge/source-drift-hardening-r37.md:53-58`). Those execution results are not verified by the scored-tip bytes.
- `git cat-file -e e57c58b57c025364e79d130fbdf764d2674d83d6:corpus/lessons/round-37.md` failed: `fatal: path 'corpus/lessons/round-37.md' exists on disk, but not in 'e57c58b57c025364e79d130fbdf764d2674d83d6'` (exit 128). The lesson visible in the current checkout is not evidence at the scored tip and was not used here.

## Trend verdicts

- **Expansion — improved.** The tip adds a new source-linked knowledge entry on hardening the source-drift fetch path, mapped in `corpus/README.md:46`; its scoped new ground and source rows are recorded at `corpus/knowledge/source-drift-hardening-r37.md:1-12,25-58`. This is new mapped knowledge, not credit for the five-row count alone. The missing S225 copy and the 220-row live receipt remain limits on verification, not claims of complete source coverage. Rule: `LEARNING.md:31-35`.
- **Quality — unchanged.** The committed knowledge diff contains only the new entry; no pre-existing knowledge entry was re-verified, deepened, or superseded in the `842a320..e57c58b` range. Evidence: the `git diff --name-status ... -- corpus/knowledge` command above. Rule: `LEARNING.md:34`.
- **Discernment — unchanged.** The scored tip has no round-37 lesson or recorded outside admit-and-reject spot-check; the missing lesson lookup is recorded above. `LEARNING.md:40-48` requires a non-author sample of at least one admit and one reject, so no agreement or learning from disagreement is evidenced at e57. The source decisions are not self-certified as outside discernment.

## Scope and handoff

Only this report file is written: `.ufo/waves/round-37/w1/ScribeReport.md`. The lane's product code, corpus, evidence, and VCS state were not modified; no tools were installed. C1/C2 counters were not rerun. The findings above distinguish the committed scored tip from later checkout bytes and do not upgrade absent receipts or files into execution evidence.

VERDICT: FAIL — the scored tip lacks the cited S225 source copy and does not bind the final five-row state to its live sweep/after-receipts; see `corpus/SOURCES.md:231`, `corpus/knowledge/source-drift-hardening-r37.md:3-7,53-65`, and `.ufo/waves/round-37/evidence/drift-live-r37.txt:221-222`.