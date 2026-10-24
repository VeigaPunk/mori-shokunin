All eight negative controls printed `C1=unmet`, exited 1, and reported only `unmet_conditions=sources`; none printed `C1=met`.

# C0 — fabricated-source controls

Seat: `MoriR33.CtlFabricatedSources`. This is a critic's sandbox receipt, not a claim admission, independent semantic judgment, integration, or score change.

## Axes and strongest counterexamples

- **Depth / false provenance:** (a) all five Gate rows and copies pass, with located quotes and mutually consistent edited-byte hashes; every measurement-time fetch fails the hash match. Self-consistency does not establish upstream provenance.
- **Calibration / duplicate authority and identity:** (b) renaming an existing URL is rejected; (c) every Gate, copy and fetch passes, but counting one URL as two new ids is rejected by `distinct_sources=no`.
- **Freshness / byte stability:** (d) an unedited, commit-pinned GitHub HTML page is rejected because its response bytes change. A commit identity does not imply a byte-stable HTML representation.
- **Operability / bounded reproducibility:** (e–g) independently exercise quote length, quote containment, mined status and HTTPS, without table or receipt-shape failures.

All eight states contain ten distinct, unfenced decision-table rows, readings of at least eight words, source metadata, four qualifying skill lines, the exact frozen R-J in both dispatch and receipt, the matching entry hash, and all ten receipt rows marked supported with located spans. Those receipts are explicitly synthetic shape fixtures; no judge or additional UFO runtime was invoked. Every table row cites all fixture ids. In (b–g), five good new sources remain alongside the invalid source, so an early source rejection cannot accidentally invalidate receipt spans or quote overlap. The counter confirms `supported=10 supported_new=10 spans_bad=[]` and `rows_without_quote_overlap=0` for every control. These controls isolate source rejection, not R-J honesty or semantic sufficiency.

## Frozen inputs and containment

- Frozen base: `27969134d51ea15982db4f36c77e2decd2a22b07`; entering tip: `7d382043016e8854e3be2ee523a095b409c3d8a1`.
- Counter: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py`.
- Counter SHA-256: `7361f3e31f4a88afc7a50a907d9c2d5b66ca98306a633760ecc40ca53fa3d942`; builder compared its bytes with the frozen commit before creating controls.
- Contract read: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/contract.md`; SHA-256 `6edaf25fb830522d029479f88901e72497161c249afa8ddb58d73459766d273a`.
- Sole clone: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo`. Each control is a separate committed branch directly from the frozen base; no lane or fleet git writes occurred.
- `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were unset for clone/config/build/scoring. Exact counter commands below ran with that clean environment.
- Commands were timeout-bounded. Eight counter calls ran concurrently once each; the scorer reaped all children and its cleanup completed. No background service was started.
- Installs/updates: none. Available `python3`, `curl`, `git`, and `timeout` sufficed. No pacman transaction occurred.
- Fetch setup encountered one HTTP 404 for the candidate queue-sysfs document. Only that failed source slot was replaced with the successfully fetched kernel source file; it was not used in any scored control.

## Retained scripts and receipts

| Absolute script path | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/fetch_sources.py` | `894af4af30c0f2a23a18c2315b9e9b4d637707d1b29a7fc197c51e48f3e941bf` |
| `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/build_controls.py` | `ab4330ea6e3a4d3384b131de956629d65c192e1259472b5f5906ba3e9777ffd7` |
| `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/score_controls.py` | `84274c05905abe68f36f34585c5302eaf7c2c910b5b1ae3e5856931c83274a82` |

Machine-readable complete results: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/results.json`.
Fixture descriptions and source hashes: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/controls.json`.
Fetch command/hash receipts: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/fetch-receipts.json`.
Sandbox git command receipts: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/build-commands.json`.
Individual complete stdout, stderr and JSON receipts are retained in `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/receipts` under the control names below. All counter stderr was empty.

## (a) Five consistent but fabricated copies

Control: fetched five genuinely novel Linux v6.12 URLs, appended a distinct synthetic line to each fetched copy without removing any quote, and put each edited copy's SHA-256 in its admit Gate row. SOURCES rows are mined and use the same URLs. Exactly five new ids are cited.

Sandbox clone: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo`.
Commit: `9ef886b5a9bb1292ffbcd6525c457f963ac0e55e`.

| id | Fetched upstream SHA-256 | Committed copy / Gate SHA-256 |
|---|---|---|
| S180 | `f76d7ea58954ae30cc7877bd48c71c9c3265726caebca54aafbc5d6fa5086923` | `cd7fffea035e093d339c3c6035528cdf7fb82d6d29ee32c7cddb37d5853a2756` |
| S181 | `4c35b795a518ceefea985f11e53b51f71d58fc99bf5a0920ca3738f13c90cb2e` | `d606a60f369fea4c3860f86e57d8f189d89fe15c3719df5a9c240a0495855ec7` |
| S182 | `d46bc91367b5f7b4de98d28499d2d1d3efe6ca1f66707b72a245f57550911ea8` | `236fb5f3ec3ebf437cf8fd814bd857fdbfb42c1ded7d375295fe3daf67d8abdc` |
| S183 | `563f1982dda26f1be93676a2327b6033fbb8b8d0895b7c48c255b7e50a476f9a` | `39818cbf89f9b9c2dce00e0004e6d9d547424e9529ad945fea8f8af8ec0d432e` |
| S184 | `f6539e348a71099eb158edb9620a7e60bcaf1106de1345608b0239ae1954bb70` | `72ea2485c198311f80f7bc9ac45991d28dd287b815dd7d2edb89d4c6eab48290` |

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 9ef886b5a9bb1292ffbcd6525c457f963ac0e55e --repo /fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
```

Full stdout, including every per-id line:

```text
rev=9ef886b5a9bb1292ffbcd6525c457f963ac0e55e repo=/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
entry=present entry_sha256=1423bfb7e2329de19958ce907191368bf37692aaf9e4d5f3a4d681795fdc7565 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=5 (S180,S181,S182,S183,S184)
S180 gate=ok quotes=4 copy=ok fetch=bad url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=4 copy=ok fetch=bad url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=1 copy=ok fetch=bad url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/blk-mq.rst
S183 gate=ok quotes=1 copy=ok fetch=bad url=https://raw.githubusercontent.com/torvalds/linux/v6.12/block/genhd.c
S184 gate=ok quotes=1 copy=ok fetch=bad url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/device-mapper/statistics.rst
gates_ok=5/5 copies_ok=5/5 fetch_ok=0/5 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=sources
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**; `C1=met`: **no**. Smallest safe correction: restore the unedited upstream bytes and their hashes; never bless an edited copy as upstream evidence.

## (b) New id re-registering an entering-tip URL

Control: S185 uses the exact URL already registered as S090/S143 at the entering tip, `https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst`. Its copy is the successfully fetched upstream response, with a located in-range quote. Five other novel sources remain valid.

Sandbox clone: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo`.
Commit: `322c2b968b49c5a5712376cf7dcfa7be43f9ab84`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 322c2b968b49c5a5712376cf7dcfa7be43f9ab84 --repo /fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
```

Full stdout:

```text
rev=322c2b968b49c5a5712376cf7dcfa7be43f9ab84 repo=/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
entry=present entry_sha256=c0e62195c11d97ae49758d1b1905528c08da34cc3e583d7ddfc76a31319c3fa5 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/blk-mq.rst
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/block/genhd.c
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/device-mapper/statistics.rst
S185 gate=bad url_registered_at_entering_tip
gates_ok=5/6 copies_ok=5/6 fetch_ok=5/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=sources
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**; `C1=met`: **no**. Smallest safe correction: do not create a new identity for an existing URL; cite its existing id without counting it toward the new-source requirement, and use genuinely new sources for that requirement.

## (c) Two new ids with one URL

Control: S180 and S185 both carry `https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst`, exact upstream copies and their correct identical hash. This intentionally violates both URL uniqueness and the consequent distinct-hash requirement, without any fetch or copy failure.

Sandbox clone: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo`.
Commit: `4da702a3f2e63f0809bf2a5f126a4cfb6959fcb4`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 4da702a3f2e63f0809bf2a5f126a4cfb6959fcb4 --repo /fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
```

Full stdout:

```text
rev=4da702a3f2e63f0809bf2a5f126a4cfb6959fcb4 repo=/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
entry=present entry_sha256=c0e62195c11d97ae49758d1b1905528c08da34cc3e583d7ddfc76a31319c3fa5 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/blk-mq.rst
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/block/genhd.c
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/device-mapper/statistics.rst
S185 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
gates_ok=6/6 copies_ok=6/6 fetch_ok=6/6 distinct_sources=no
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=sources
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**; `C1=met`: **no**. Smallest safe correction: keep one id per URL and remove the duplicate identity/citations, retaining enough genuinely distinct new sources. Changing only an id or digest cannot create another authority.

## (d) Byte-unstable GitHub HTML commit page

Control: S185 uses unedited response bytes from `https://github.com/torvalds/linux/commit/adc218676eef25575469234709c2d87185ca223a`, with a located quote and the exact response hash in its Gate. Two successful initial requests already differed:

- `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/inputs/unstable_commit.src`: 254608 bytes, SHA-256 `14baad2accddf428ebe5b3ad6fa6343789cb717ca240570f08f46659f6250d40`.
- `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/inputs/unstable_repeat.src`: 254609 bytes, SHA-256 `4f144b5cdbe668fb5d749d181b1a50063f64650ab9213fd08039a7533c84e635`.

Each initial request used `timeout 70 curl -sSL --fail -m 60 https://github.com/torvalds/linux/commit/adc218676eef25575469234709c2d87185ca223a`, exit 0, empty stderr. No request-token values are reproduced here.

Sandbox clone: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo`.
Commit: `6789333c1cc2c7c50e9914ed9924db7168bbb40d`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 6789333c1cc2c7c50e9914ed9924db7168bbb40d --repo /fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
```

Full stdout:

```text
rev=6789333c1cc2c7c50e9914ed9924db7168bbb40d repo=/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
entry=present entry_sha256=c0e62195c11d97ae49758d1b1905528c08da34cc3e583d7ddfc76a31319c3fa5 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/blk-mq.rst
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/block/genhd.c
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/device-mapper/statistics.rst
S185 gate=ok quotes=1 copy=ok fetch=bad url=https://github.com/torvalds/linux/commit/adc218676eef25575469234709c2d87185ca223a
gates_ok=6/6 copies_ok=6/6 fetch_ok=5/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=sources
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**; `C1=met`: **no**. Smallest safe correction: use a byte-stable pinned raw file or patch representation and its actual fetched hash. Do not normalize away HTML differences or weaken the frozen byte-equality requirement.

## (e1) Located 26-word Gate quote

Control: S185 has distinct, exact upstream dm-io bytes and one located quote, correctly labeled 26 words:

> Dm-io provides synchronous and asynchronous I/O services. There are three types of I/O services available, and each type has a sync and an async version. The

Sandbox clone: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo`.
Commit: `fc1920c1b549caf6346b973bcb000ad705020628`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py fc1920c1b549caf6346b973bcb000ad705020628 --repo /fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
```

Full stdout:

```text
rev=fc1920c1b549caf6346b973bcb000ad705020628 repo=/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
entry=present entry_sha256=c0e62195c11d97ae49758d1b1905528c08da34cc3e583d7ddfc76a31319c3fa5 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/blk-mq.rst
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/block/genhd.c
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/device-mapper/statistics.rst
S185 gate=bad gate_fields
gates_ok=5/6 copies_ok=5/6 fetch_ok=5/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=sources
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**; `C1=met`: **no**. Smallest safe correction: replace this with a located 3–25-word quotation, preserving its meaning and accurate count; a different count label alone is not a correction.

## (e2) Well-formed quote absent from the copy

Control: S185 has the exact upstream dm-io copy/hash but a syntactically located, 12-word Gate quote absent from that copy:

> This invented sentence is not present in the committed upstream source copy.

Sandbox clone: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo`.
Commit: `61a5e0bc5ada6ab3aca55d0d36a87315cbf08db6`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 61a5e0bc5ada6ab3aca55d0d36a87315cbf08db6 --repo /fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
```

Full stdout:

```text
rev=61a5e0bc5ada6ab3aca55d0d36a87315cbf08db6 repo=/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
entry=present entry_sha256=c0e62195c11d97ae49758d1b1905528c08da34cc3e583d7ddfc76a31319c3fa5 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/blk-mq.rst
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/block/genhd.c
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/device-mapper/statistics.rst
S185 gate=ok quotes=1 copy=bad fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/device-mapper/dm-io.rst
gates_ok=6/6 copies_ok=5/6 fetch_ok=6/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=sources
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**; `C1=met`: **no**. Smallest safe correction: use actual upstream text and its real locator; do not insert the invented quote into the committed source copy.

## (f) Cited id remains queued

Control: all ten rows cite S185, but its SOURCES status is `queued`. Its distinct URL, upstream bytes, Gate fields and located quote are otherwise valid.

Sandbox clone: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo`.
Commit: `cfd01559800dbafb6c505a7b75523cbc87f87064`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py cfd01559800dbafb6c505a7b75523cbc87f87064 --repo /fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
```

Full stdout:

```text
rev=cfd01559800dbafb6c505a7b75523cbc87f87064 repo=/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
entry=present entry_sha256=c0e62195c11d97ae49758d1b1905528c08da34cc3e583d7ddfc76a31319c3fa5 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/blk-mq.rst
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/block/genhd.c
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/device-mapper/statistics.rst
S185 gate=bad source_status_not_mined
gates_ok=5/6 copies_ok=5/6 fetch_ok=5/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=sources
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**; `C1=met`: **no**. Smallest safe correction: genuinely mine/review the source and log the queued→mined change before counting it as new support; otherwise remove the unsupported citation.

## (g) Non-HTTPS URL

Control: S185 Gate and SOURCES rows both use `http://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/device-mapper/dm-io.rst`. The committed copy is unchanged from the fetched HTTPS upstream bytes, with a valid quote/hash. The counter rejects the scheme before trying to fetch this URL.

Sandbox clone: `/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo`.
Commit: `92538d5b228e537d271ab0d32465e32e7c783fa8`.

Exact counter command:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py 92538d5b228e537d271ab0d32465e32e7c783fa8 --repo /fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
```

Full stdout:

```text
rev=92538d5b228e537d271ab0d32465e32e7c783fa8 repo=/fast/scratch/hyaku/mori-r33/CtlFabricatedSources/repo
entry=present entry_sha256=c0e62195c11d97ae49758d1b1905528c08da34cc3e583d7ddfc76a31319c3fa5 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=10 rows_ok=10 distinct_rows=10 short_readings=0
new_id_rows=10 new_ids=6 (S180,S181,S182,S183,S184,S185)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/iostats.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/stat.rst
S182 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/block/blk-mq.rst
S183 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/block/genhd.c
S184 gate=ok quotes=1 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v6.12/Documentation/admin-guide/device-mapper/statistics.rst
S185 gate=bad gate_fields
gates_ok=5/6 copies_ok=5/6 fetch_ok=5/6 distinct_sources=yes
rows_without_quote_overlap=0
dispatch_rule=yes receipt_rule=yes judged_sha=ok covered=yes supported=10 supported_new=10 spans_bad=[] unsupported=[]
skill_rows=4
unmet_conditions=sources
C1=unmet
```

Exit code: **1**. Printed `C1=unmet`: **yes**; `C1=met`: **no**. Smallest safe correction: use the actual HTTPS URL consistently and retain its exact fetched bytes/hash; an HTTP redirect is not an exemption from the stated Gate requirement.

## Review finding

No escape was observed on the assigned controls, and no frozen-counter change is warranted by these receipts. Each fixture defect is repairable at the source/representation layer; accepting fabricated bytes, duplicate identities, overlong or unlocated quotes, queued support, or non-HTTPS provenance instead would relax P-C1, not repair the fixture. The canonical authority must not admit such a trade. This review does not establish global counter soundness, byte stability of every URL over time, or authenticity of any real judge receipt. The contract's named synthetic-receipt residual remains unchanged.
