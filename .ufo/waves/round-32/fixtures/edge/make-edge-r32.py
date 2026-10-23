#!/usr/bin/env python3
"""Generate fixtures/edge-r32.json: minimal briefs pinning edge cases of tools/mori-blind-check.sh.

Each case carries: the brief bytes, the rule-text clause (quoted from
.ufo/waves/round-31/rule-text.md), the expected report derived from that clause, and — where the
clause admits a competing reading — that reading with its own expected report.

The `expected` column is written BEFORE the tool is run (this file only encodes the rule-text
reading); run-edge-r32.py --update fills the `actual` column and computes `agree`/`agree_alt`.
"""
import base64, hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'fixtures', 'edge-r32.json')

RULE_TEXT = '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/rule-text.md'
TOOL = '/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-blind-check.sh'

WAVE_ROOT = '.ufo/waves/round-32/fx'
REGEX = r'^CaseE[0-9]+[a-z]?\.md$'

ALLOW_RULE = '.ufo/waves/round-31/rule-text.md'
ALLOW_SUB = '/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/allowed/*'

C1 = ('1. A block opens at a Markdown heading (any level) whose text contains `files opened` or '
     '`opened files` (case-insensitive), or at a line whose trimmed text starts with `Files opened:` '
     'or `Opened files:` (case-insensitive).')
C2 = ('2. Entries are the following lines that start (after optional indentation) with `- `, `* `, `+ `, '
     '`N. ` or `N) `, or with `|` (a table row); a table\'s separator row (only `|`, `-`, `:` and spaces) '
     'and the row directly above it are not entries. Blank lines inside the block are skipped.')
C3 = '3. The block closes at the first heading or at the first other non-blank line.'
C4 = ('4. An entry\'s candidates are its tokens, stripped of wrapping backticks, quotes and brackets, trailing '
     '`,;.` and a `:L` / `:L-M` suffix, that contain `://`, `/` or `.` or equal `LOG.md`, `SCORECARD.md`, '
     '`SKILL.md` or `PROVINCE.md`. An entry with no candidate, or with a candidate no allow line matches, is one '
     '`writer-forbidden-opened-path` hit at its own line.')
C5 = '5. A brief with no entry in any block is one `writer-missing-files-opened-list` hit at line 1.'


def tree_path(case_id):
    return f'{WAVE_ROOT}/{case_id.lower()}/Case{case_id}.md'


CASES = [
    {
        'id': 'E01',
        'title': 'setext heading (Files opened / ---) opens the files-opened block',
        'allow_lines': [ALLOW_RULE],
        'brief': 'Files opened\n------------\n- .ufo/waves/round-31/rule-text.md\n',
        'primary': {
            'basis': 'markdown-semantics',
            'clauses': [C1, C2, C4],
            'reading': ('Clause 1 opens a block at "a Markdown heading (any level)". A setext heading is a Markdown '
                        'heading (level 1 with `===`, level 2 with `---`); its text is the line above the '
                        'underline, here `Files opened`, which contains `files opened`. So the block opens at line '
                        '1, the `- ` line is an entry (clause 2) and its candidate '
                        '`.ufo/waves/round-31/rule-text.md` matches an allow line (clause 4): no hit.'),
            'hits': [],
            'exit': 0,
        },
        'alt': {
            'basis': 'atx-only',
            'description': ('Block opener must be an ATX `#` heading at column 0, so the setext heading opens '
                            'nothing and the brief has no entry in any block (clause 5).'),
            'hits': [[1, 'writer-missing-files-opened-list']],
            'exit': 1,
        },
    },
    {
        'id': 'E02',
        'title': 'indented `#` heading (2 spaces) opens the files-opened block',
        'allow_lines': [ALLOW_RULE],
        'brief': '  ## Files opened\n  - .ufo/waves/round-31/rule-text.md\n',
        'primary': {
            'basis': 'markdown-semantics',
            'clauses': [C1, C2, C4],
            'reading': ('Clause 1 says "a Markdown heading (any level)" with no column-0 qualifier. In CommonMark an '
                        'ATX heading may be indented by up to three spaces and is still a heading, so the heading '
                        'text `Files opened` contains `files opened` and the block opens. Clause 2 allows optional '
                        'indentation before the `- ` marker, so the second line is an entry; clause 4: its candidate '
                        'matches an allow line. No hit.'),
            'hits': [],
            'exit': 0,
        },
        'alt': {
            'basis': 'atx-column-0-only',
            'description': ('Only `#` headings at column 0 open a block, so the 2-space indented heading is not seen '
                            'and the brief has no entry (clause 5).'),
            'hits': [[1, 'writer-missing-files-opened-list']],
            'exit': 1,
        },
    },
    {
        'id': 'E02b',
        'kind': 'control',
        'title': 'CONTROL: `#` heading indented 4 spaces is an indented code block, not a heading',
        'allow_lines': [ALLOW_RULE],
        'brief': '    ## Files opened\n    - .ufo/waves/round-31/rule-text.md\n',
        'primary': {
            'basis': 'markdown-semantics',
            'clauses': [C1, C2, C5],
            'reading': ('Four spaces of indentation makes the line an indented code block in CommonMark, so it is '
                        'not a heading under any reading and clause 1 opens no block. The brief has no entry in any '
                        'block, so clause 5 gives one `writer-missing-files-opened-list` hit at line 1. Both the '
                        'markdown reading and the column-0 reading agree here: this control shows the tool reacts '
                        'to indentation depth, not to indentation as such.'),
            'hits': [[1, 'writer-missing-files-opened-list']],
            'exit': 1,
        },
        'alt': None,
    },
    {
        'id': 'E03',
        'title': 'CRLF line endings do not change the path token',
        'allow_lines': [ALLOW_RULE],
        'brief': '## Files opened\r\n- .ufo/waves/round-31/rule-text.md\r\n',
        'primary': {
            'basis': 'line-terminator-semantics',
            'clauses': [C1, C2, C4],
            'reading': ('No clause of the rule mentions line terminators, and CRLF is a line terminator, so the brief '
                        'reads as `## Files opened` / `- .ufo/waves/round-31/rule-text.md`. The heading contains '
                        '`files opened` (clause 1), the `- ` line is an entry (clause 2) and its candidate token is '
                        '`.ufo/waves/round-31/rule-text.md`, which matches an allow line (clause 4). No hit.'),
            'hits': [],
            'exit': 0,
        },
        'alt': {
            'basis': 'byte-literal',
            'description': ('The carriage return stays inside the path token, so the candidate no longer matches '
                            'the allow line and becomes forbidden.'),
            'hits': [[2, 'writer-forbidden-opened-path']],
            'exit': 1,
        },
    },
    {
        'id': 'E04',
        'title': 'tab directly after `-` is not a list marker',
        'allow_lines': [ALLOW_RULE],
        'brief': '## Files opened\n-\t/etc/passwd\n',
        'primary': {
            'basis': 'clause-literal',
            'clauses': [C1, C2, C3, C5],
            'reading': ('Clause 2 enumerates the entry markers as `- `, `* `, `+ `, `N. `, `N) ` and `|`: the dash is '
                        'followed by a space, so `-\\t/etc/passwd` is not an entry marker and the line is not an '
                        'entry. Clause 3 then closes the block at that first other non-blank line, so the brief has '
                        'no entry in any block and clause 5 gives one `writer-missing-files-opened-list` hit at line '
                        '1. The path on that line is never inspected as a candidate.'),
            'hits': [[1, 'writer-missing-files-opened-list']],
            'exit': 1,
        },
        'alt': {
            'basis': 'commonmark-list-item',
            'description': ('A tab is a valid list-item separator in CommonMark, so `-\\t/etc/passwd` is a list item '
                            'and its path is an entry candidate that no allow line matches.'),
            'hits': [[2, 'writer-forbidden-opened-path']],
            'exit': 1,
        },
        'note': ('Both readings exit 1 but with different rules; the literal reading is the one the clause text '
                 'supports, SKILL.md names the tab behaviour a known limit.'),
    },
    {
        'id': 'E05',
        'title': 'a `../` path passes an allow glob',
        'allow_lines': [ALLOW_RULE, ALLOW_SUB],
        'brief': ('## Files opened\n'
                  '- /fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/allowed/../../secret.txt\n'),
        'primary': {
            'basis': 'clause-literal',
            'clauses': [C1, C2, C4],
            'reading': ('Clause 4 says a candidate is forbidden when "no allow line matches" it, and the allow file '
                        'holds one bash glob per line. The candidate token is the whole '
                        '`/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/allowed/../../secret.txt`; the allow line '
                        '`/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/allowed/*` matches it (in bash pattern '
                        'matching `*` also spans `/`). No clause of the rule normalises `..`, so the entry is '
                        'allowed: no hit.'),
            'hits': [],
            'exit': 0,
        },
        'alt': {
            'basis': 'path-normalisation',
            'description': ('`..` segments are resolved before matching, so the candidate leaves the allowed '
                            'directory and matches no allow line.'),
            'hits': [[2, 'writer-forbidden-opened-path']],
            'exit': 1,
        },
        'note': ('Normalised, the candidate is /fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/secret.txt, one level '
                 'above the allowed/ subtree. SKILL.md names the un-normalised matching a known limit.'),
    },
    {
        'id': 'E06',
        'title': 'a `# files opened` line inside a code fence does not open a block',
        'allow_lines': [ALLOW_RULE],
        'brief': ('## Cases\n'
                  '\n'
                  '```text\n'
                  '# files opened\n'
                  '- /etc/passwd\n'
                  '```\n'
                  '\n'
                  '## Files opened\n'
                  '- .ufo/waves/round-31/rule-text.md\n'),
        'primary': {
            'basis': 'markdown-semantics',
            'clauses': [C1, C2, C4],
            'reading': ('Clause 1 opens a block at "a Markdown heading". Inside a fenced code block the line '
                        '`# files opened` is code content, not a heading, so it opens nothing; the fenced '
                        '`- /etc/passwd` line is code content too and is not an entry (clause 2). The real '
                        '`## Files opened` heading opens the block and its single entry matches an allow line '
                        '(clause 4). No hit.'),
            'hits': [],
            'exit': 0,
        },
        'alt': {
            'basis': 'fence-blind',
            'description': ('The fenced `# files opened` line is read as a heading, so it opens a block and the '
                            'fenced `- /etc/passwd` line becomes an entry with no matching allow line.'),
            'hits': [[5, 'writer-forbidden-opened-path']],
            'exit': 1,
        },
    },
    {
        'id': 'E06b',
        'kind': 'control',
        'title': 'CONTROL: the tool\'s json-fence protection does not cover the files-opened rule',
        'allow_lines': [ALLOW_RULE],
        'brief': ('## Cases\n'
                  '\n'
                  '```json\n'
                  '# files opened\n'
                  '- /etc/passwd\n'
                  '```\n'
                  '\n'
                  '## Files opened\n'
                  '- .ufo/waves/round-31/rule-text.md\n'),
        'primary': {
            'basis': 'tool-faithful',
            'clauses': [C1, C2, C4],
            'reading': ('A `json` fence inside a `## Cases` section is the shape the tool protects from the two '
                        'round-30 detectors, but that protection is scoped to the detectors: the files-opened parser '
                        'still reads the fenced `# files opened` line as a heading, so the fenced `- /etc/passwd` '
                        'line is an entry with no matching allow line and gives one '
                        '`writer-forbidden-opened-path` hit at line 5. This control separates "fence-blind" from '
                        '"json-fence-protected": only the former is what E06 measures.'),
            'hits': [[5, 'writer-forbidden-opened-path']],
            'exit': 1,
        },
        'alt': None,
        'note': 'The expected column here is the tool-faithful reading, so agree=yes here is expected by design.',
    },
    {
        'id': 'E07',
        'title': 'a heading with words between `files` and `opened` does not open a block',
        'allow_lines': [ALLOW_RULE],
        'brief': '## Files I opened\n- .ufo/waves/round-31/rule-text.md\n',
        'primary': {
            'basis': 'clause-literal',
            'clauses': [C1, C2, C4, C5],
            'reading': ('Clause 1 opens a block at a heading whose text "contains `files opened` or `opened files`". '
                        'The heading text `Files I opened` contains neither substring, so no block opens; the `- ` '
                        'line is therefore not inside a block and is not an entry. The brief has no entry in any '
                        'block, so clause 5 gives one `writer-missing-files-opened-list` hit at line 1.'),
            'hits': [[1, 'writer-missing-files-opened-list']],
            'exit': 1,
        },
        'alt': {
            'basis': 'loose-mention',
            'description': ('A heading that mentions files and opened opens the block, so the entry counts and the '
                            'brief is clean.'),
            'hits': [],
            'exit': 0,
        },
    },
    {
        'id': 'E08',
        'title': 'lead-in prose before the first entry closes the block',
        'allow_lines': [ALLOW_RULE],
        'brief': ('## Files opened\n'
                  'I read the rule text before listing the entries.\n'
                  '- .ufo/waves/round-31/rule-text.md\n'),
        'primary': {
            'basis': 'clause-literal',
            'clauses': [C1, C2, C3, C5],
            'reading': ('Clause 3: "The block closes at the first heading or at the first other non-blank line." The '
                        'prose line is the first other non-blank line, so the block closes there and the following '
                        '`- ` line is not an entry. The brief has no entry in any block, so clause 5 gives one '
                        '`writer-missing-files-opened-list` hit at line 1.'),
            'hits': [[1, 'writer-missing-files-opened-list']],
            'exit': 1,
        },
        'alt': {
            'basis': 'loose-lead-in',
            'description': ('Prose directly under the heading is a lead-in and the list still counts, so the brief is '
                            'clean.'),
            'hits': [],
            'exit': 0,
        },
    },
    {
        'id': 'E09',
        'title': 'a sub-heading inside the block closes the block',
        'allow_lines': [ALLOW_RULE],
        'brief': ('## Files opened\n'
                  '- .ufo/waves/round-31/rule-text.md\n'
                  '### Notes\n'
                  '- /etc/passwd\n'),
        'primary': {
            'basis': 'clause-literal',
            'clauses': [C1, C2, C3, C4],
            'reading': ('Clause 3 closes the block "at the first heading"; the rule states no depth rule, so the '
                        '`### Notes` heading closes the block and the `- /etc/passwd` line after it is not an entry '
                        '(clause 2 needs an open block). The only entry is the first `- ` line, whose candidate '
                        'matches an allow line (clause 4). No hit.'),
            'hits': [],
            'exit': 0,
        },
        'alt': {
            'basis': 'markdown-section',
            'description': ('A deeper heading does not end the enclosing Markdown section, so `- /etc/passwd` is '
                            'still an entry and its path is forbidden.'),
            'hits': [[4, 'writer-forbidden-opened-path']],
            'exit': 1,
        },
    },
    {
        'id': 'E09b',
        'kind': 'control',
        'title': 'CONTROL: a sub-heading with all entries below it leaves the brief with no entry',
        'allow_lines': [ALLOW_RULE],
        'brief': ('## Files opened\n'
                  '### Notes\n'
                  '- .ufo/waves/round-31/rule-text.md\n'),
        'primary': {
            'basis': 'clause-literal',
            'clauses': [C1, C2, C3, C5],
            'reading': ('Clause 3 closes the block at the first heading, so the `### Notes` heading closes the block '
                        'opened by `## Files opened`; the `- ` line below it is not inside any open block and is not '
                        'an entry. The brief has no entry in any block, so clause 5 gives one '
                        '`writer-missing-files-opened-list` hit at line 1. This is the shape the round-31 lesson '
                        'describes for the round-29 briefs (literal reading yields a missing-list hit).'),
            'hits': [[1, 'writer-missing-files-opened-list']],
            'exit': 1,
        },
        'alt': None,
    },
]


def main():
    cases = []
    for c in CASES:
        brief = c['brief'].encode('utf-8')
        p = tree_path(c['id'])
        prim = c['primary']
        alt = c['alt']
        case = {
            'id': c['id'],
            'kind': c.get('kind', 'edge-case'),
            'title': c['title'],
            'wave_dir': f'{WAVE_ROOT}/{c["id"].lower()}',
            'brief_name': f'Case{c["id"]}.md',
            'writer_regex': REGEX,
            'allow_lines': c['allow_lines'],
            'brief_text': c['brief'],
            'brief_base64': base64.b64encode(brief).decode(),
            'brief_sha256': hashlib.sha256(brief).hexdigest(),
            'brief_len': len(brief),
            'rule_text_reading': {
                'basis': prim['basis'],
                'clauses': prim['clauses'],
                'reading': prim['reading'],
            },
            'expected': {
                'hits': [f'{p}:{ln}:{rule}' for ln, rule in prim['hits']],
                'exit': prim['exit'],
                'scanned': 1,
            },
            'alt_reading': None,
            'actual': {'exit': None, 'stdout': [], 'hits': []},
            'agree': None,
            'agree_alt': None,
        }
        if alt:
            case['alt_reading'] = {
                'basis': alt['basis'],
                'description': alt['description'],
                'hits': [f'{p}:{ln}:{rule}' for ln, rule in alt['hits']],
                'exit': alt['exit'],
            }
        if 'note' in c:
            case['note'] = c['note']
        cases.append(case)

    doc = {
        'version': 1,
        'round': 32,
        'defect': 'routed defect 6 of corpus/lessons/round-31-verifier-spotcheck.md §8 (tool edge cases)',
        'tool': TOOL,
        'tool_sha256': hashlib.sha256(open(TOOL, 'rb').read()).hexdigest(),
        'rule_text': RULE_TEXT,
        'rule_text_sha256': hashlib.sha256(open(RULE_TEXT, 'rb').read()).hexdigest(),
        'runner': '/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/run-edge-r32.py',
        'generator': '/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/make-edge-r32.py',
        'sandbox': '/fast/scratch/hyaku/mori-r32/ExecEdgeFixtures/sandbox/repo',
        'how_to_reproduce': ('python3 run-edge-r32.py   -> rebuilds a fresh sandbox git repo under this seat\'s '
                             'scratch dir, reruns the lane tool over every case exactly as its usage says '
                             '(cwd = sandbox repo, lane-rev = sandbox commit) and compares the stored `actual` '
                             'column; --update rewrites that column.'),
        'expected_semantics': ('`expected` is the report required by the primary reading of the quoted rule-text '
                                'clauses (`rule_text_reading.basis` says which reading and why). `alt_reading` '
                                'records the competing reading where the clause is ambiguous, with the report that '
                                'reading requires. `agree` compares actual against `expected`; `agree_alt` compares '
                                'actual against `alt_reading` (null when there is none).'),
        'cases': cases,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as h:
        json.dump(doc, h, indent=1, ensure_ascii=False)
        h.write('\n')
    print('wrote', OUT, len(cases), 'cases')


if __name__ == '__main__':
    main()
