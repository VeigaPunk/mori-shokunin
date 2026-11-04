# Mo79R01Review — C1 adversarial review, round 79 w1

## Findings (severity ordered)

**Low — R01-1: setup diagnostics breach the stdout-only contract.** At reviewed
`tools/mori-control-receipt.py` sha256
`b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`,
`check_receipts` writes read failures to its `err` stream (lines 121–124), which
`main` supplies as `sys.stderr` (203). Usage and empty-directory failures also use
stderr (186–199). Reproductions `empty`, `missing`, `directory_as_file`, `usage`,
and `invalid_utf8` below all return the proper rc 2, but stdout is empty and stderr
nonempty. Contract C1 explicitly requires stdout only; a stdout-only collector
loses these setup diagnostics. Recommendation only: make the diagnostic channel
conform and retain rc 2. No source was edited. This overlaps the sentinel finding;
do not count it twice.

No required binding/claim-recognition attack landed. The frozen C1 behavior
checks succeeded at working-tree bytes, not at an admitted committed revision.

## What I did (numbered)

1. Read the frozen C1 spec, SCORECARD axes and r78 closure, QUALITY 159/161–163,
and SKILL instrument registry. Axes: operability (C1), calibration (honest evidence),
freshness (this run at the named bytes); no scalar move or admission recommended.
The initial tool read returned path-not-found while its owner was building it;
I waited for availability, then read all 351 candidate source lines.
2. Tried `read xd://lsp`: result `No such tool: xd://lsp` (mounted device list
contained no lsp). Therefore semantic references/definition/diagnostics were
unavailable, not empty proofs. Used literal fallback `grep` for
`mori-control-receipt` across absolute lane `tools` and `.ufo/waves/round-79`
paths; it located the frozen `count-c1.py` caller, contract and dispatch text.
Read `count-c1.py` lines 125–160: canonical caller extracts the committed blob,
runs that blob with `python -I`, archives each evidence directory at the same
revision, and requires selftest >=10/0, named r78 witness rc1 and r79 unbound0
rc0. I did not run that counter or claim the working-tree run proves commitment.
3. Created an isolated temporary harness at
`/fast/scratch/hyaku/mori-r79/Mo79R01Review/attack.py`; it wrote only own scratch
fixtures, launched an eight-worker batch of commands below, and captured each
process's rc/stdout/stderr independently. Invocation:
`python3 -I /fast/scratch/hyaku/mori-r79/Mo79R01Review/attack.py`
from that same absolute scratch directory. Every target run used the one
canonical `/usr/bin/python3 -I` command and absolute candidate path. Hashes printed
before/after the batch were identical to the sha above. No rerouting, saturation,
or resume-continuity behavior exists in this tool's interface; no claims about
those unrelated runtime contracts are made.
4. Re-ran selftest and both live directories, then all named hostile fixtures and
extra read-error/claim-isolation arms. Exact commands and outputs follow. Receipt
fixtures are preserved below as Python bytes literals (including BOM/CRLF).
5. Removed all own scratch via an EXIT trap; cleanup output:
```
cleanup_scope=/fast/scratch/hyaku/mori-r79/Mo79R01Review
scratch_removed=yes
```
No git mutation, install/update, network call, host/unit/session change, or tool
edit was performed by this seat. Only this report is retained in the lane.

## Attack outcomes

- `indented`, `direct_under`: command binds, rc0; indentation is stripped.
- `comment`, `comment_cmd`: comments never bind, rc1, key x reported.
- `trailing_comment`, `decimal`, `exponent`: no integer claim, rc0 claims0.
- `negative`: x=-1 counts, rc1 claims1.
- `two_sections`: only #unbound reported, key b; bound section does not leak.
- `section_isolation`: command-only prior section cannot bind next section.
- `crlf`: accepted, sections2 claims1 bound1, rc0, no crash.
- `bom`: accepted UTF-8 BOM as literal U+FEFF; first heading becomes head content,
  yielding sections1 rather than sections2; following command and x=0 bind, rc0.
  `bom_claim`: BOM-prefixed first x=-1 is not a claim, rc0 claims0. Encoding/BOM
  normalization is not frozen, so these are disclosed limitations, not defects
  against the exact stripped-line regex. No traceback occurred.
- `empty`: no .txt (only ignored.md), documented setup rc2, no traceback. Correct
  exit behavior, but lands R01-1 diagnostic-channel defect.
- `invalid_utf8`: clean decode-error rc2, no traceback; also lands R01-1.
- `strip_cmd`, `cmd_attribute`: verb-led and embedded cmd= forms bind, rc0.
- `missing`, `directory_as_file`, `usage`: clean rc2; also land R01-1.
- Selftest: 18 pass/0 fail rc0. r78: rc1, files15 sections37 claims40 unbound11;
  controls-r78 has seven unbound sections and the required correction key.
  r79: rc0, files3 sections15 claims41 unbound0.

## Commands, fixture bytes and captured outputs

All outputs are the original captured process streams, not inferred equivalents.
An empty stream is printed as `(empty)`; the stored bytes literals make fixtures
reconstructible after scratch removal. The live directories were the working-tree
contents at this run, not frozen snapshots; the file inventories appear in stdout.

### selftest

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --selftest
```
rc: 0

stdout:
```text
case 01 bound section ($ cmd above count)      pass
case 02 unbound section (count, no command)    pass
case 03 comment line neither command nor claim pass
case 04 inline cmd= line binds the section     pass
case 05 split across two ## headings           pass
case 06 non-integer key=value not a claim      pass
case 07 negative integer claim                 pass
case 08 empty file                             pass
case 09 missing path rc 2                      pass
case 10 receipt with no claims rc 0            pass
case 11 verb-led first token binds             pass
case 12 indented comment/claim handled         pass
case 13 claim key character class              pass
case 14 bare cmd= without space does not bind  pass
case 15 summary aggregates across files        pass
case 16 dir collection filters and sorts       pass
case 17 unreadable file rc 2                   pass
case 18 unbound line carries heading text      pass
CONTROL_RECEIPT_SELFTEST pass=18 fail=0
```

stderr:
```text
(empty)
```

### live78

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
```
rc: 1

stdout:
```text
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/census-end-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/census-start-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt sections=9 claims=10 bound=0 unbound=7
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#1. the counter instrument absent from the entering tree claims=1 keys=cat_file_rc
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#2. the tool in no ref, ever (log --all / rev-list --all --objects) claims=2 keys=log_all_lines,revlist_objects_named
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#3. the canonical capabilities row absent at entering claims=2 keys=counter_win_mentions_in_SCORECARD,canonical_capability_headings_at_entering
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#4. the D77-3 correction absent at entering claims=1 keys=correction_marker_in_LOG_at_entering
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#5. S593 absent at entering claims=2 keys=S593_rows_in_SOURCES_at_entering,SOURCES_rows_at_entering
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#7. the family table at entering (tolerant form, r77 lesson rule) claims=1 keys=family_rows_at_entering
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#3b. precise row-form control (the 1 mention at entering is the Round-77 section C2 prose at SCORECARD.md:3892, not a capabilities-table row) claims=1 keys=row_form_counter_win_rows_at_entering
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/counter-win-live-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/counter-win-selftest-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/foreign-sweep-r78.txt sections=1 claims=0 bound=0 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/freshstart-spotchecks-r78.txt sections=4 claims=1 bound=0 unbound=1
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/freshstart-spotchecks-r78.txt#1. the frozen r61 counter at the r61 data tip claims=1 keys=counter_rc
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/frozen-audit-r78.txt sections=1 claims=0 bound=0 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/pin-family-r78-final.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/pin-family-r78-s593-isolated.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/pin-family-r78.txt sections=2 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/post-landing-verify-r78.txt sections=5 claims=0 bound=0 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/s593-anchor-check-r78.txt sections=3 claims=2 bound=1 unbound=1
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/s593-anchor-check-r78.txt#B. able-to-fail arm (mislocation: wrong line + mutated count) claims=1 keys=abletofail_rc
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/selftests-battery-r78.txt sections=1 claims=12 bound=0 unbound=1
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/selftests-battery-r78.txt#(head) claims=12 keys=rc,rc,rc,rc,rc,rc,rc,rc,rc,rc,rc,rc
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/source-s593-r78.txt sections=5 claims=8 bound=0 unbound=1
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/source-s593-r78.txt#1. duplicate sweep INTO this receipt BEFORE the fetch (the r69 lesson rule) claims=8 keys=hits_cimwin32prov,hits_wmisdk,hits_perfos_memory,hits_GlobalMemoryStatusEx,hits_PerfOS,hits_CommitLimit,S593_rows,SOURCES_rows_before
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
```

stderr:
```text
(empty)
```

### live79

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence/census-start-r79.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence/controls-r79.txt sections=7 claims=13 bound=6 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/evidence/source-rfc9111-r79.txt sections=7 claims=27 bound=5 unbound=0
CONTROL_RECEIPT_SUMMARY files=3 sections=15 claims=41 unbound=0
```

stderr:
```text
(empty)
```

### empty

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --dir /fast/scratch/hyaku/mori-r79/Mo79R01Review/empty
```
rc: 2

stdout:
```text
(empty)
```

stderr:
```text
mori-control-receipt.py: --dir: no .txt files under: /fast/scratch/hyaku/mori-r79/Mo79R01Review/empty
```

### missing

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/absent.txt
```
rc: 2

stdout:
```text
(empty)
```

stderr:
```text
mori-control-receipt.py: cannot read receipt: /fast/scratch/hyaku/mori-r79/Mo79R01Review/absent.txt: [Errno 2] No such file or directory: '/fast/scratch/hyaku/mori-r79/Mo79R01Review/absent.txt'
```

### directory_as_file

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/empty
```
rc: 2

stdout:
```text
(empty)
```

stderr:
```text
mori-control-receipt.py: cannot read receipt: /fast/scratch/hyaku/mori-r79/Mo79R01Review/empty: [Errno 21] Is a directory: '/fast/scratch/hyaku/mori-r79/Mo79R01Review/empty'
```

### usage

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py
```
rc: 2

stdout:
```text
(empty)
```

stderr:
```text

  mori-control-receipt.py RECEIPT [RECEIPT ...]   check the named receipts
  mori-control-receipt.py --dir DIR              check every *.txt directly
                                                 under DIR (sorted); may be
                                                 combined with receipt paths
                                                 (dir files first)
  mori-control-receipt.py --selftest             in-memory self-test, no files
  mori-control-receipt.py --help                 this usage

Output per file:
  CONTROL_RECEIPT <path> sections=S claims=C bound=B unbound=U
  unbound <path>#<section> claims=N keys=<k1,k2>     (one per unbound section)
Final line:
  CONTROL_RECEIPT_SUMMARY files=F sections=S claims=C unbound=U

Exit codes: 0 no section with claims is unbound; 1 some is; 2 setup (usage,
missing path, unreadable file).

Python 3 standard library only; `python -I` safe; stdout only — no file
writes, no network, no subprocess, no temp files.
mori-control-receipt.py: no receipt path and no --dir given
```

### help

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --help
```
rc: 0

stdout:
```text

  mori-control-receipt.py RECEIPT [RECEIPT ...]   check the named receipts
  mori-control-receipt.py --dir DIR              check every *.txt directly
                                                 under DIR (sorted); may be
                                                 combined with receipt paths
                                                 (dir files first)
  mori-control-receipt.py --selftest             in-memory self-test, no files
  mori-control-receipt.py --help                 this usage

Output per file:
  CONTROL_RECEIPT <path> sections=S claims=C bound=B unbound=U
  unbound <path>#<section> claims=N keys=<k1,k2>     (one per unbound section)
Final line:
  CONTROL_RECEIPT_SUMMARY files=F sections=S claims=C unbound=U

Exit codes: 0 no section with claims is unbound; 1 some is; 2 setup (usage,
missing path, unreadable file).

Python 3 standard library only; `python -I` safe; stdout only — no file
writes, no network, no subprocess, no temp files.
```

stderr:
```text
(empty)
```

### indented

Fixture bytes: `b'## section\n    $ cmd\nx=0\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/indented.txt
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/indented.txt sections=2 claims=1 bound=1 unbound=0
CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=1 unbound=0
```

stderr:
```text
(empty)
```

### comment

Fixture bytes: `b'## section\n# $ git status\nx=0\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/comment.txt
```
rc: 1

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/comment.txt sections=2 claims=1 bound=0 unbound=1
unbound /fast/scratch/hyaku/mori-r79/Mo79R01Review/comment.txt#section claims=1 keys=x
CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=1 unbound=1
```

stderr:
```text
(empty)
```

### trailing_comment

Fixture bytes: `b'## section\nx=0 # note\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/trailing_comment.txt
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/trailing_comment.txt sections=2 claims=0 bound=0 unbound=0
CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=0 unbound=0
```

stderr:
```text
(empty)
```

### negative

Fixture bytes: `b'## section\nx=-1\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/negative.txt
```
rc: 1

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/negative.txt sections=2 claims=1 bound=0 unbound=1
unbound /fast/scratch/hyaku/mori-r79/Mo79R01Review/negative.txt#section claims=1 keys=x
CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=1 unbound=1
```

stderr:
```text
(empty)
```

### decimal

Fixture bytes: `b'## section\nx=1.5\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/decimal.txt
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/decimal.txt sections=2 claims=0 bound=0 unbound=0
CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=0 unbound=0
```

stderr:
```text
(empty)
```

### exponent

Fixture bytes: `b'## section\nx=1e3\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/exponent.txt
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/exponent.txt sections=2 claims=0 bound=0 unbound=0
CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=0 unbound=0
```

stderr:
```text
(empty)
```

### two_sections

Fixture bytes: `b'## bound\n$ cmd\na=1\n## unbound\nb=2\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/two_sections.txt
```
rc: 1

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/two_sections.txt sections=3 claims=2 bound=1 unbound=1
unbound /fast/scratch/hyaku/mori-r79/Mo79R01Review/two_sections.txt#unbound claims=1 keys=b
CONTROL_RECEIPT_SUMMARY files=1 sections=3 claims=2 unbound=1
```

stderr:
```text
(empty)
```

### direct_under

Fixture bytes: `b'$ cmd\nkey=0\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/direct_under.txt
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/direct_under.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT_SUMMARY files=1 sections=1 claims=1 unbound=0
```

stderr:
```text
(empty)
```

### crlf

Fixture bytes: `b'## section\r\n$ cmd\r\nx=0\r\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/crlf.txt
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/crlf.txt sections=2 claims=1 bound=1 unbound=0
CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=1 unbound=0
```

stderr:
```text
(empty)
```

### bom

Fixture bytes: `b'\xef\xbb\xbf## section\n$ cmd\nx=0\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/bom.txt
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/bom.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT_SUMMARY files=1 sections=1 claims=1 unbound=0
```

stderr:
```text
(empty)
```

### bom_claim

Fixture bytes: `b'\xef\xbb\xbfx=-1\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/bom_claim.txt
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/bom_claim.txt sections=1 claims=0 bound=0 unbound=0
CONTROL_RECEIPT_SUMMARY files=1 sections=1 claims=0 unbound=0
```

stderr:
```text
(empty)
```

### comment_cmd

Fixture bytes: `b'## section\n# foo cmd=git\nx=1\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/comment_cmd.txt
```
rc: 1

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/comment_cmd.txt sections=2 claims=1 bound=0 unbound=1
unbound /fast/scratch/hyaku/mori-r79/Mo79R01Review/comment_cmd.txt#section claims=1 keys=x
CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=1 unbound=1
```

stderr:
```text
(empty)
```

### strip_cmd

Fixture bytes: `b'## section\n  git status\nx=0\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/strip_cmd.txt
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/strip_cmd.txt sections=2 claims=1 bound=1 unbound=0
CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=1 unbound=0
```

stderr:
```text
(empty)
```

### cmd_attribute

Fixture bytes: `b'## section\nrun cmd=git\nx=0\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/cmd_attribute.txt
```
rc: 0

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/cmd_attribute.txt sections=2 claims=1 bound=1 unbound=0
CONTROL_RECEIPT_SUMMARY files=1 sections=2 claims=1 unbound=0
```

stderr:
```text
(empty)
```

### section_isolation

Fixture bytes: `b'## bound\n$ cmd\n## unbound\nx=0\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/section_isolation.txt
```
rc: 1

stdout:
```text
CONTROL_RECEIPT /fast/scratch/hyaku/mori-r79/Mo79R01Review/section_isolation.txt sections=3 claims=1 bound=0 unbound=1
unbound /fast/scratch/hyaku/mori-r79/Mo79R01Review/section_isolation.txt#unbound claims=1 keys=x
CONTROL_RECEIPT_SUMMARY files=1 sections=3 claims=1 unbound=1
```

stderr:
```text
(empty)
```

### invalid_utf8

Fixture bytes: `b'\xff\nx=0\n'`

```sh
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py /fast/scratch/hyaku/mori-r79/Mo79R01Review/invalid_utf8.txt
```
rc: 2

stdout:
```text
(empty)
```

stderr:
```text
mori-control-receipt.py: cannot read receipt: /fast/scratch/hyaku/mori-r79/Mo79R01Review/invalid_utf8.txt: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

## Residual risk / verification gaps

- Candidate was untracked awaiting L1 integration per owner notification; only the
  sha-pinned working-tree behavior was exercised. L1 must use the frozen canonical
  counter at the eventual landed revision; I do not judge/admit the claim.
- r79 evidence may gain receipts after this run; current rc0 covers exactly the
  three .txt paths printed above. Later receipt bytes are not implicitly covered.
- Directory enumeration (`os.listdir`, line 195) has no OSError handler. A permission
  or disappearance race could traceback [INFERENCE]; no race/permission fixture
  was run, so not reported as a reproduced defect.
- No LSP server/device; text caller search is literal, not semantic coverage.
  No subprocess/network/write tracing was performed by this reviewer (sentinel's
  separate audit owns that scope). Syntax-only binding cannot prove that a shown
  command actually computed the count; that is the frozen scope, not a new defect.

## Own defects and self-evaluation

Initial parallel reads attempted the tool before its build was complete. The
path-not-found output caught that; no absent-file run was misrepresented as a
candidate failure. The first captured batch display truncated long JSON lines;
I fetched the full original artifact before composing this report, rather than
rerunning or inventing the omitted output. Scratch cleanup was installed only at
cleanup time, not at initial creation (process-interruption leakage risk during
the run); the observed EXIT cleanup nevertheless removed the whole tree.

Accuracy 4/5 (working-tree evidence, not committed-blob proof); completeness 4/5
(all requested attacks run, no filesystem-race reproduction); clarity 4/5
(full streams lengthen report but preserve evidence); actionability 5/5 (one
specific channel defect, exact source locations and reproductions); conciseness
4/5 (live78 full output retained for audit). Mean 4.2/5. Improvements: L1 bind
verification to committed revision, keep runtime-directory scope explicit, install
the cleanup trap before future fixture creation. User agreement is not assumed.

## Post-review owner notification (not independently exercised)

After submission, Mo79E01ReceiptTool reported accepting R01-1 and superseding the
reviewed candidate with sha256
`531d6b524635cccc57ef54712ed990899dfae36f2544143f6a1bbbd66c55f887`.
The owner reports stdout-only setup diagnostics, a new channel-check selftest
case (19/0 rc0), r78 rc1 with the witness, and r79 rc0 unbound0 over four receipts.
Source of these statements: the owner's direct coordination message and
`.ufo/waves/round-79/w1/Mo79E01ReceiptTool.md` § Review fix; these are owner-reported
results, not commands run by this reviewer. All captured commands above remain
bound only to b3b2f9e2… . R01-1 is therefore historical for that candidate and
owner-reported fixed in 531d6b52…; no independent re-review or admission is claimed.
