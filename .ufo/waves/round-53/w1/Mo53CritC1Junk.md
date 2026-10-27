# Mo53CritC1Junk — C1 counter junk-path attack report

Seat: critic, attack class. Scope: cheapest edit sets that make `count-c1.py` print `C1=met` without an honest
v7.3 recheck. All fixtures built in one `git clone --shared` of the lane under
`/fast/scratch/hyaku/mori-r53/Mo53CritC1Junk/lane`, every commit authored by fixture identity
`Junk Fixture <junk@fixture.invalid>`, scored with `python3 .ufo/waves/round-53/count-c1.py <rev> --repo <clone>`.
Scratch removed after this report. Tooling: none installed (git 2.x, python3 already present).

Baseline (data commit itself, control `no-votes` reproduces):
`python3 count-c1.py 2a4213bf8da72f7cd78189baa5bb9be825dca1df --repo lane` → rc 1
`C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 … failed=votes`

## Attack classes

### A1 — forged voter files, votes copied wholesale — MET (cheapest met found: 2 files, 1 commit)

Two new files `.ufo/waves/round-53/w1/Mo53Fr01.md` and `Mo53Fr02.md`, byte-identical, each containing only the
line `# fixture` plus 46 lines of the form `RECHECK <h> <disp>` where `<disp>` is copied verbatim from the
ledger's own disposition column. One commit, fixture identity, nothing else changed.

```
$ git -C lane log -1 --format='%an <%ae> %h' v_forge
Junk Fixture <junk@fixture.invalid> c6e227d0
$ python3 count-c1.py c6e227d00d700b0bc20e39eebc3b66b3f1b66ca7 --repo lane   # rc 0
C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=46 dissent=0 rev=c6e227d00d700b0bc20e39eebc3b66b3f1b66ca7
```

Let-through: `final_votes` (count-c1.py L160–180) reads `VOTE_DIR + voter + ".md"` from the tree at the scored
rev and attributes the file to the seat by pathname alone. No author, committer, file-mode or content
provenance is checked: a voter file written by a non-voter seat — or by the ledger author in the same commit —
is indistinguishable. `ls-tree --name-only` membership (L164–166) is the only gate. "At least two of the
twelve RECHECK seats" reduces to "two pathnames". The same commit may carry the ledger AND its votes.

### A2 — QUOTE evasion: author self-votes stand after a one-character quote mutation — MET

`Mo53Fr01.md` contains a `QUOTE <h> :: <text>` line for every hash, followed by its own `RECHECK <h> holds`
for every hash — the exact self-vote pattern the guard exists to reject — except each quoted text is mutated
by one character (trailing `.` appended, or ` (sic)` suffixed). `Mo53Fr02.md` votes only.

```
rev=dbf123a9a707762380def27a995d758e63984e7c  rc 0
C1=met … holds=46 changed=0 voted=46 dissent=0
```

Positive control — same file with the row's quote text byte-exact — the guard does fire:

```
rev=d49579c71bf215b02cf15a0e3dd527ed08a96f5f  rc 1
C1=unmet … voted=0 failed=votes
```

Let-through: L249 `q not in proposed.get(w, {}).get(h, set())` is an exact-match disqualifier on
whitespace-collapsed text built at L179. Any non-whitespace mutation of the QUOTE text (one appended `.`)
un-disqualifies the author's vote; omitting QUOTE lines entirely does the same. "An author's vote is not
counted on a quote it proposed" is enforced only against authors who quote themselves verbatim.

### A3 — junk quote on an `absent` row: located in the file, unrelated to the claim — MET

Ledger row `d7a1dc88dcb3` (claim: *hugetlb mappings are charged strictly unless MAP_NORESERVE*) — status
`absent` — its quote cell replaced with `Always allow shrinking brk. */ if (brk <= mm->brk) { /* Search one
past newbrk`, a verbatim span of `mm/mmap.c.v7.3` from the `brk` syscall, unrelated to MAP_NORESERVE. Same
forged votes as A1.

```
rev=3f36795910f449862f0a973d8598d8714556bd74  rc 0
C1=met … voted=46 dissent=0
```

Let-through: L231–232 — `quote_ok` requires only `6 ≤ words ≤ 25`, `q in norm[path]`, and `q == q72` **only
when `derived == "held"`**. For an `absent` row the quote cell may be ANY 6–25-word substring of the file,
including whitespace-joined text spanning line/comment boundaries; nothing ties it to the claim's subject.
An "absent" row can thereby name the wrong passage, or prose assembled across a brace boundary, and pass.

### A4 — contradictory dispositions rubber-stamped: `held` rows declared `changed` — MET

All 44 `held` rows' disposition cells flipped `holds` → `changed` while the status cells stay honest `held`
(quotes still verbatim in the v7.3 copy); voter files echo `changed` on those hashes, `holds` on the two
absent rows.

```
rev=3155f72e3826075a7ad58023ade21f51073d2a5f  rc 0
C1=met scope=46 … held=44 absent=2 holds=2 changed=44 voted=46 dissent=0
```

Let-through: `disp` is checked only against `("holds", "changed")` (L244) and then against the votes
(L249–252); it is NEVER compared to `derived`. The counter's own evidence (quote verbatim present → `held`)
and the ledger's verdict (`changed`) may contradict on every row and the claim still passes, because
`status_ok` checks the status cell, not the disposition. Note the landed honest ledger already exercises the
converse: both `absent` rows carry disposition `holds` — permissible semantics (claim survives respelled
text), but proof the field is asserted, not verified.

### A5 — dissent burial, two flavours — both MET

Fence burial: `Mo53Fr01.md` ends its unfenced votes with `RECHECK <h1> holds`, then opens a `~~~` fence and
places `RECHECK <h1> changed` inside it — a final-line dissent the counter never sees.

```
rev=7c3b596019d1a449b5daff6e84d037271c3a8f95  rc 0
C1=met … dissent=0
```

Zero-width-space burial: same dissent line prefixed with U+200B — `^\s*RECHECK` does not match (ZWSP is not
`\s`), so the line is invisible, no fence needed.

```
rev=9f9de03997b8af1fda0b8a478b4fac71cc52c53f  rc 0
C1=met … dissent=0
```

Let-through: fence toggle at L168–172 skips fenced lines entirely (a `RECHECK` inside a fence is never a
recorded "final line" — the kill rule's "no seat's final line with the other word" cannot see it), and
RECHECK_RE L80 `^\s*` anchors only ASCII-equivalent whitespace. Both let a seat keep an on-record dissent in
its file while the counter records unanimous agreement. (`dissent` counting at L250 only sees recorded
words.)

## Ranked summary

| class | rev | rc | met? | let-through line(s) |
|---|---|---|---|---|
| A1 forged voters / copied votes | c6e227d00d70 | 0 | met | L160–180 `final_votes`: pathname = seat; no authorship binding; ledger and votes in one commit |
| A2 QUOTE-evasion self-vote | dbf123a9a707 | 0 | met | L249 exact-match `q not in proposed`; L179 builds set verbatim |
| A2b exact-QUOTE guard (positive) | d49579c71bf2 | 1 | unmet | guard works when text matches exactly — contrast point |
| A3 unrelated quote, absent row | 3f36795910f4 | 0 | met | L231–232 `q == q72` waived for `absent`; substring anywhere in file |
| A4 held→changed contradiction | 3155f72e3826 | 0 | met | L244–252 `disp` never compared to `derived` |
| A5a fenced dissent burial | 7c3b596019d1 | 0 | met | L168–172 fence skip |
| A5b ZWSP-prefixed dissent | 9f9de03997b8 | 0 | met | L80 `^\s*RECHECK` misses U+200B prefix |

Cheapest full met = A1: two short files, one commit, zero honest recheck of any of the 46 rows — the data
commit's ledger stands unmodified and the vote arm, the only arm that was still failing at `voted=0`, is
satisfied by copy-paste. A2–A5 each compose on top in the same commit.

Assessment per my role: A1 is the deepest defect — the vote arm provides no independence signal at all
(any committer mints any seat's "final line"; votes can be generated mechanically from the ledger they
ratify, byte-identical across seats). A4 is a fixable-by-design verification gap: `disp` vs `derived` is a
two-line consistency check conceptually, but changing the counter is out of bounds this round — it is a
named limit and a routed item for round 54, not a claim-rule change. A3's `absent`-row quote freedom is
partially covered by the contract's named limit ("held proves the words still occur somewhere") but the
absent-side replacement-quote freedom is NOT explicitly named — worth naming. A2/A5 are evasion-of-guard
limits: the QUOTE guard and dissent check hold only against verbatim, unfenced, plainly-anchored text.

UNVERIFIED: whether the real voter seats' reports (being written by siblings this wave) will contain
QUOTE-proposal patterns or fence artifacts — my fixtures demonstrate counter behavior only. No claim that
the landed ledger's content is wrong: the A3/A4 edits were mine, in a clone.

## Findings

- HIGH — `.ufo/waves/round-53/count-c1.py` L160–180 (`final_votes`): vote authenticity is pathname-only. A
  voter file `Mo53Fr<NN>.md` committed by anyone counts as that seat's final line; identical copied votes
  across seats satisfy "at least two distinct voters"; the ledger commit may itself carry the votes. P-C1's
  vote arm proves only that two files exist, not that two seats judged. Route to round 54.
- HIGH — count-c1.py L244–252: `disposition` is never checked against the counter-derived `status`
  (L226). `held` rows can be declared `changed` — and the landed ledger's `absent` rows are declared
  `holds` — with votes echoing, and `C1=met` prints. The claim's verdict column is unconstrained text.
  Route to round 54 (consistency check or explicit naming); landed data is not wrong — the two `absent`
  `holds` rows mean "claim survives under the respelled quote".
- MED — count-c1.py L231–232: for `absent` rows the quote cell is any 6–25-word substring of the v7.3
  copy, unrelated to the claim, possibly spanning line boundaries via whitespace collapse. The contract's
  named limit covers `held`; the absent-side freedom is unnamed.
- MED — count-c1.py L249+L179: the self-vote guard is exact-match. A `QUOTE` line mutated by one character
  (or omitted) lets the quote's author vote on its own rows. Guard works only against verbatim self-quoting.
- LOW — count-c1.py L168–172, L80: fenced or zero-width-space-prefixed `RECHECK` lines are invisible to
  the counter, so a file can contain a real dissent while `dissent=0` prints. Affects the kill rule's
  "no RECHECK seat's final line with the other word" phrasing.
