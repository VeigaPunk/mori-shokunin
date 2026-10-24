# CritC2Axis — round 36 wave 2, attempt 2

Attacks: C2's operability fit, blind-truth separation, historical provenance, and resistance to do-nothing/denial controls. Reviewed landed revision `bf0df77fee4b6ef54a90aea09335c7617f125151`; real-arm witness revision `6bd57097`, base `f10a320d`.

Axes: **operability** (runnable, correctly failing gate), **coverage** (deletion history edge classes), **calibration** (receipt scope versus claimed assurance). C1 freshness admission is not inferred here. This is a scoped critique, not a canonical admission judgment.

## Decisive counterexample: deleting and restoring the registry is forgotten

**Fixable defect; static finding, not a runtime reproduction.**

Counterexample history: A holds a valid registry containing S001; B removes `corpus/SOURCES.md`; C restores A's exact registry bytes. Set `--round-base A` and inspect C. The contract requires `round_changed=[S001]`: the row was deleted in a commit within A..C, even though the endpoint contains it unchanged (`.ufo/waves/round-36/contract.md:69-77`). Endpoint `ids` and `deleted` should both remain empty.

Evidence:

- `tools/mori-sources-appendonly.py:205-209` records a missing historical path as `None`.
- `tools/mori-sources-appendonly.py:223-225` skips that state, instead of recording the disappearance of the preceding ids. Consequently `prev_ids` and `last_seen` survive B unchanged (`:226-236`).
- The restored identical S001 contributes no immutable difference; the range union therefore misses B (`:246-255`). The CLI returns clean for an empty `round_changed` (`:493-495`).
- **[INFERENCE from those branches]** this history yields `appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]`, exit 0, although the required round verdict is exit 1 with `round_changed=[S001]`.
- The real-arm oracle repeats the omission: missing path becomes `None` at `count-c2.py:532-540`, then is skipped at `:551-553`, before deletion accounting at `:561-564`. Agreement between tool and oracle cannot expose this shared defect.
- The blind generator always writes a registry file (`count-c2.py:361-369`); its delete operation removes a row from a retained table (`:339-343,430-479`). It never exercises whole-path absence. The tool's committed fixtures likewise cover row deletion, not path deletion/restoration (`tools/mori-sources-appendonly.py:348-380`).

Impact: **operability** and **coverage**; **calibration** if the receipt is described as complete deleted-row protection. This does not show an observed failure of the frozen random distribution, or an observed negative control meeting P-C2. It shows a legitimate history outside that distribution on which the advertised gate gives a false clean result.

Smallest safe correction: represent an absent historical path as an empty row state for deletion accounting, retaining first/last-held values as needed for restoration comparisons. Add a delete-file/restore-identical fixture with independent expected `round_changed` and exit assertions. Correct the oracle's same omission as well; do not silently edit the frozen counter or relabel its old receipt as evidence of a corrected counter. No remediation was performed by this seat.

## 1. Operability fit: runnable craft, not merely bookkeeping

The axis objection itself does **not** succeed. The canonical definition is runnable artifacts whose checklist produces the stated outcome (`skills/shokunin/protocol/AXES.md:13`). This tool computes a verdict over actual Git history (`tools/mori-sources-appendonly.py:190-267`) and returns clean/failed/error (`:485-495`). `SKILL.md:864-867,875` registers an actionable pre-landing gate and makes supersession a disposition, not forgiveness. That is domain observability work, not merely adding a table row or printing a configured value.

The landed receipt demonstrates the narrower capability. Reader command actually used:

```text
functions.read(path="mori-shokunin/.ufo/waves/round-36/evidence/c2-after.txt:1-100")
```

Observed receipt excerpt (not rerun by this seat):

```text
blind arm: 24/24 sandbox histories matched the hidden truth (1.6s; coverage: deletions=22 changed-back=17 superseded=10)
real arm: pass (0.2s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=15440749816798970567
```

Source: `evidence/c2-after.txt:3-9`. This supports tested operability, not universal correctness or saturation. The defect above is repairable; it is not an unavoidable axis tradeoff and does not turn C2 into a freshness claim.

## 2. Hidden truth: memory-only labels, but no filesystem isolation

Code-path findings:

- The blind expected values are derived from in-memory operation snapshots (`count-c2.py:367,485,594`) and held by the parent during the tool invocation (`:601-620`). The sandbox writes Git histories, which are legitimate inputs, not a separate expected-summary file (`:368-371`).
- `tool_dir` contains the revision-extracted tool, not per-run truth (`:670-686`). Failed expected summaries are printed only after the entire blind arm returns (`:693-702`). The real oracle is computed after the real tool invocation (`:629-631`). I found no counter path writing the current blind truth to a temporary answer file before the corresponding invocation.
- However, `run_tool` is only `timeout` plus Python with `cwd="/"` (`:493-495`). Its subprocess setup starts a new process group, not a filesystem/user sandbox (`:70-83`), and `clean_env` merely removes Git redirection variables (`:62-67`). Changing cwd does not prevent access to the lane's absolute paths.
- **[INFERENCE]** a substitute can read C0 programs, committed reference programs, and ordinary same-user-readable temporary files. J8 contains a complete history walk before its denial projection (`c0/controls/J8.py:65-66,81-101`); `evidence/refs/ref-c2.py:86-162` contains the positive reference implementation. Thus the invocation does not establish implementation independence or exclude delegation to reference code.

Important distinction: accessible **reference algorithms** are not a disk copy of the current random **answer**. A wrapper delegating to a working implementation performs work transitively; I do not mislabel that as an observed do-nothing control meeting P-C2. No such wrapper was authored or executed here, and no actual cheating is alleged in the landed tool.

Smallest safe correction to assurance wording: say “expected values stay in parent memory,” not “the candidate is isolated from references.” If reference independence is required, use an explicit read-only input allowlist that excludes counters, C0/ref code and parent receipts, then freeze and score that changed harness separately. Merely relocating temporary directories or using neutral commit messages is not isolation.

## 3. Real arm binds a historical S069 rewrite

Command actually executed:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin --no-pager log -p --format=fuller -G '^\| S069 \|' 6bd57097 -- corpus/SOURCES.md
```

Observed: the history includes creation commit `8f8c58ee4d923131cfa61a669777ec481d5eca1d` and rewrite commit `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`. Their S069 teaches-cell excerpts are:

```text
8f8c58e addition: String-only containment cannot see symlinks: reject absolute and .. lexically before any filesystem call, and test symlinks separately.
62db24c before:  String-only containment cannot see symlinks: reject absolute and .. lexically before any filesystem call, and test symlinks separately.
62db24c after:   String-only containment cannot see symlinks: lane rule: reject absolute and .. lexically before any filesystem call, and test symlinks separately.
```

These are excerpted cells, not substituted full patch lines. The immutable `teaches` cell really changed in ancestry; the oracle's S069 entry is not invented from the round's narrative.

Second command actually executed:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin --no-pager log -p --unified=0 --format='%H %s' -G 'supersedes S069' 6bd57097 -- corpus/SOURCES.md
```

Observed commit `71abd41f9337412dc366ce605915c5e49edc94f2` adds S073, whose teaches cell opens:

```text
supersedes S069 — string-only containment (relative_to with walk_up) assumes no symlinks; resolve() first if needed.
```

Thus S069 being both changed and superseded in the receipt has independent history evidence. Supersession did not remove it from `ids`, as required. The real arm reads the supplied repository directly and walks the pinned historical revision (`count-c2.py:527-585,624-632`), rather than trusting current SOURCES text.

## 4. Do-nothing and denial receipts: both rejected under v2

Reader commands actually used:

```text
functions.read(path="mori-shokunin/.ufo/waves/round-36/evidence/c0-rescore-v2.txt:1-92")
functions.read(path="mori-shokunin/.ufo/waves/round-36/evidence/c0-rescore-v2.txt:681-770")
```

Observed v2 receipt excerpts, not fresh control runs:

```text
J1:
blind arm: 1/24 sandbox histories matched the hidden truth (2.3s; coverage: deletions=22 changed-back=16 superseded=9)
real arm: FAIL (0.3s)
  tool:   appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  tool exit=0
C2=unmet
seed=14043932168276761486
EXIT=1

J8:
blind arm: 0/24 sandbox histories matched the hidden truth (3.4s; coverage: deletions=22 changed-back=14 superseded=10)
  repo00 FAIL: lists differ
      want: appendonly_violations=2 ids=[S026] deleted=[S098] superseded=[S026] round_changed=[S026,S098]
      got:  appendonly_violations=8 ids=[S012,S021,S067,S083,S106,S145,S292] deleted=[S098] superseded=[] round_changed=[S012,S021,S067,S083,S106,S145,S292]
real arm: FAIL (0.5s)
  diff: violations: want=18 got=186
  tool exit=1
C2=unmet
seed=16410989564024834250
EXIT=1
```

Pointers: J1 `evidence/c0-rescore-v2.txt:2-8,75-85`; J8 `:681-687,757-767`. J8's source genuinely complements the present ids and round-changed ids while leaving deletion detection intact (`c0/controls/J8.py:65-66,99-119`). It is a denial control, not a setup failure. Its old individual C0 report used the v1 counter (`c0/CtlJ8.md:4`); the v2 aggregate above is the relevant receipt.

An always-empty program cannot match all blind histories once the counter enforces deletion coverage (`count-c2.py:703-706`), and it cannot match the real arm's required nonempty `ids` (`:632`). J8's exact-list disagreement is independently visible. No observed do-nothing or denial control meeting frozen P-C2 was found. A finite passing receipt is still not a completeness proof.

## Byte binding and execution boundaries

Commands actually executed from `/home/vgpnk/Projects/shokunin`:

```sh
sha256sum mori-shokunin/.ufo/waves/round-36/count-c2.py mori-shokunin/.ufo/waves/round-36/c0/controls/J8.py mori-shokunin/.ufo/waves/round-36/evidence/c0-rescore-v2.txt
```

Observed:

```text
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  mori-shokunin/.ufo/waves/round-36/count-c2.py
3332b68e76bf52f7ddd37fd818cc37991399de9e0e888162c3076e389a92476b  mori-shokunin/.ufo/waves/round-36/c0/controls/J8.py
160e85dfc8dfe587ee84ab88a779f11ac730011f8fbf46ab55c1d47cb979c733  mori-shokunin/.ufo/waves/round-36/evidence/c0-rescore-v2.txt
```

Counter hash matches `evidence/freeze-v2.txt:4` and J8's v2 receipt header (`evidence/c0-rescore-v2.txt:681`).

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show bf0df77fee4b6ef54a90aea09335c7617f125151:tools/mori-sources-appendonly.py | sha256sum
```

Observed:

```text
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  -
```

```sh
sha256sum mori-shokunin/tools/mori-sources-appendonly.py mori-shokunin/.ufo/waves/round-36/evidence/refs/ref-c2.py
```

Observed:

```text
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  mori-shokunin/tools/mori-sources-appendonly.py
08874f8f5bdf98d7580644bbeba4c0d2896f033d4b927859d3e72ccd953ca8ca  mori-shokunin/.ufo/waves/round-36/evidence/refs/ref-c2.py
```

Therefore the cited tool branches are the landed bytes, not an unbound working-tree replacement. The reference hash also matches the positive REF2 receipt (`evidence/c0-rescore-v2.txt:1161-1171`); that is provenance context, not evidence that a negative control met.

No counter, self-test, novel substitute, judge or alternate orchestration runtime was executed by this critic. No tools were installed or updated. Only this report file was written; no remediation or repository mutation was performed.

VERDICT: FAIL
