# ConnSiblingOverlap — S229 URL and static-fold teaching

Axes: URL identity (exact S229 string, omission fails the seat); document-cousin honesty (a same-page RST pin is not the admitted URL, and calling it one would harm census uniqueness); static-fold teaching (name-resolution for a timeout fold, not any "name resolution"); no-harm (do not retarget S229 onto a sibling quote that licenses a module-map fold).

No tools installed. No sibling repo was written. No production file was edited.

## Verdict

Exact URL **absent** from every sibling `corpus/SOURCES.md`. Static-fold teaching **absent** from every sibling knowledge entry.

Document cousin, not a duplicate: `mado-shokunin` already pins the CPython execution-model **RST** (tag v3.14.8) on three rows. Those rows do not teach a static timeout fold, and one of them teaches the global-then-builtins sentence that a module-map fold would hide behind.

## Census

Admitted URL (mori `corpus/SOURCES.md:235`, S229):

`https://docs.python.org/3/reference/executionmodel.html#naming-and-binding`

Lanes with `corpus/SOURCES.md` (20, mori excluded): audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, revenger, souji, tabi, tameshi, tsukuroi.

Typo trees checked and **not** registries: `kaidoku-sh2`, `mori-shokukin`, `tameshi-shokukin` have no `corpus/SOURCES.md`.

Direct read of the 20 sibling registries (`python3` count, command below): `exact=0` and `executionmodel.html=0` in every file. The only `executionmodel.rst` hits are mado, substring count 8 on 5 lines: registry rows S111 (`:123`), S120 (`:132`), S121 (`:133`) — each row carries the raw URL and a `Doc/reference/executionmodel.rst:` locator — plus screening notes at `:393` and `:395`.

Shared mado URL (not S229's URL):

`https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst`

Sibling knowledge trees: 938 markdown/text files across the same 20 lanes. Zero files contain `static fold`, `timeout fold`, or `executionmodel.html`.

## Overlap table

| Path | What it is | Verdict |
|---|---|---|
| 19 sibling `corpus/SOURCES.md` other than mado | No `executionmodel.html`, no `executionmodel.rst`, no `naming-and-binding` | **Absence.** |
| `mado-shokunin/corpus/SOURCES.md:123` S111 | Same document, raw RST @ v3.14.8, sha256 `11f99f83d785ac174dc02aaf26e03eb91813b38c213729c0017b5a3a70a2eb89`. Located quote is the global-statement paragraph: "The global namespace is searched first. If the names are not found there, the builtins namespace is searched next." (`executionmodel.rst:140-142`). Teaches E3 tripwire shadowing. | **Cousin, wrong sentence.** Not the admitted URL. Not a static fold. |
| `mado-shokunin/corpus/SOURCES.md:132` S120 | Same RST URL. Locator `:240-256` (annotation laziness). | **Cousin, different section.** |
| `mado-shokunin/corpus/SOURCES.md:133` S121 | Same RST URL. Locator `:89-114,322-329`. The range `:89-114` includes the S229 sentence, which sits at RST `:113-114` in `mado-shokunin/.ufo/waves/round-22/w1/sources/SourceClosure/cpython-3.14.8-Doc-reference-executionmodel.rst`. Teaches cell is factory enclosing scope and **runtime** free-variable lookup, not a static fold. | **Cousin. Range overlaps the sentence; the teaching does not.** |
| `mado-shokunin/corpus/knowledge/tripwire-precision-r20.md:41-44` | "Name binding follows Python (S111): the binding in effect at the call wins" for tripwire leads. | **Name resolution, not a static fold.** |
| `mado-shokunin/corpus/knowledge/tripwire-lifetime-recovery-r22.md:13-16` | Enclosing-frame / late-global rules for factory closures, cited to S121. | **Runtime lifetime, not a static fold.** |
| `mado-shokunin/corpus/knowledge/tripwire-binding-boundaries-r21.md:36` | S120 annotation laziness. | **Different section.** |
| `kaidoku-shokunin/corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md` and `2026-10-22-r28-evm-heldout-selector-naming.md` | EVM selector naming. | **False friend.** Not Python scoping. |
| `kaidoku-shokunin/corpus/knowledge/2026-10-13-r2-crash-inspect-probe.md:42` | ELF `NT_FILE` "module map". | **False friend.** Not a Python module-level name map. |

The S229 sentence is in both copies, at different anchors: mori HTML `corpus/evidence/sources-r40/S229.src:294-295`; mado RST `:113-114`. Mori's row cites `:254-256` (section span `:249-262`). Those three line numbers are not interchangeable. This seat did not re-derive the lesson's counting method.

## Proposed move

Do not retarget S229 onto mado's raw RST URL, and do not import S111's or S121's teaches cell as the warrant for the static fold.

S111's located sentence is global-namespace-then-builtins. Treating that as the fold's source would make a module-map constant fold look specified, which is the round-39 hole `corpus/knowledge/conform-scope-r40.md:9-20` exists to close (function-local `TIMEOUT = None` must shadow `TIMEOUT = 120`). S121's teaches cell says free names resolve at runtime; following that into the checker would refuse the static three-case fold rather than repair it.

Keep the admitted HTML URL and the §4.2.2 sentence ("When a name is used in a code block, it is resolved using the nearest enclosing scope") as the only warrant. Census W04 keys duplicate URL strings; the exact string is absent on siblings, so S229 adds no cross-lane duplicate of the admitted URL. Collapsing the cousin into "same URL" would be a false W04. Collapsing it into "no overlap" would hide the substitution hazard above.

C1 (operability) and C2 (append-only depth) are untouched. The frontier axis improves by the classification: S229 stays the opener for the static fold, and mado stays a tripwire source.

## Risks

- Point-in-time. A sibling can admit the HTML URL after this walk.
- A gitignore-respecting fleet grep is not evidence of absence (lane trees can be ignored; one such search returned no `executionmodel.html` hit and is not the census). The counts above are direct reads of the 20 `SOURCES.md` files and 938 knowledge files.
- Lessons outside `corpus/knowledge` were not the asked surface. The exact URL grep over each sibling `corpus/` tree (knowledge, lessons, evidence) also returned no matches.
- HTML `:294-295` versus the row's `:254-256` is an anchor mismatch inside mori. Quote-gate seats own it. It is recorded here only so nobody "fixes" it by copying mado's RST `:113-114`.

## Verification

Re-run from the fleet root. Expect `exact=0` on every sibling line and `rst` only under mado.

```
python3 - <<'PY'
import pathlib
url = "https://docs.python.org/3/reference/executionmodel.html#naming-and-binding"
root = pathlib.Path("/home/vgpnk/Projects/shokunin")
lanes = sorted(p for p in root.glob("*-shokunin") if p.name != "mori-shokunin")
print(f"sibling_lanes={len(lanes)}")
for lane in lanes:
    text = (lane / "corpus" / "SOURCES.md").read_text(errors="replace")
    n, html, rst = text.count(url), text.count("executionmodel.html"), text.count("executionmodel.rst")
    print(f"{'HIT' if n or html or rst else 'ABSENT'} {lane.name} exact={n} html={html} rst={rst}")
PY
```

Observed stdout (2026-10-24): `sibling_lanes=20`, nineteen `ABSENT … exact=0 html=0 rst=0`, and `HIT mado-shokunin exact=0 html=0 rst=8`.

Grep (gitignore off), exact URL across the 20 sibling `corpus/` trees: no matches.

Grep (gitignore off), `executionmodel|naming-and-binding|Naming and binding` on the 20 `SOURCES.md` files: only mado S111/S120/S121 and the two screening notes.

Grep (gitignore off), `static fold|static timeout|timeout fold|module-map|module map` on the 20 `corpus/knowledge` trees: only kaidoku ELF module-map prose, no static fold.
