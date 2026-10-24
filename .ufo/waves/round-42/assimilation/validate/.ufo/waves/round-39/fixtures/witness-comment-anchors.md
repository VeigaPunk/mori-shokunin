# fabricated entry with comment-parked anchors (negative witness)

A fabricator read tools/mori-source-drift.py and picked three plausible policy
phrases as `anchor:` lines. All three occur in the tool's bytes — but only inside
`#` comment lines, never at a code position, because the phrases document the
policy rather than implement it. The round-38 substring check accepted them
(comments included); the round-39 non-comment occurrence rule rejects them.

   anchor: bounded read: an untrusted source must not stream past the cap
   anchor: a redirect actually happened: the new authority must be public
   anchor: bodies larger than this cannot be classified; read is capped at
