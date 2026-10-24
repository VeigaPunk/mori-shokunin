{
  "schema": "mori-content-reviews-v1",
  "reviewer": "MoriR19Recovery.Content24",
  "revision": "b3602869dadd4016675aeba8db2adf3fa1e1b531",
  "rows": [
    {
      "path": ".ufo/waves/round-16/build/PackAnchorValidation.md",
      "blob_sha256": "66f10d06de4e1609684b2d04e4e1b48ffc3425361128410aadc529624bad2105",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "Scoped fixture-analysis report uses public catalog identifiers and an explicitly fabricated control; no private, credential, authentication, or configuration values appear.",
      "findings": []
    },
    {
      "path": ".ufo/waves/round-16/build/SourceChain.md",
      "blob_sha256": "f3a95b093f747ca0365da2bde5a440361d1dae830c14bb3d6549687c81489220",
      "decision": "minimized",
      "content_basis": "content-reviewed",
      "reason": "The audit and source material are scoped technical content; a procedural disclosure includes an unnecessary user-scoped runtime location and temporary-file naming detail, but no credential, authentication, or home-configuration value.",
      "findings": [
        { "line": 63, "class": "host-runtime-path" }
      ]
    },
    {
      "path": ".ufo/waves/round-18/build/ReviewRegisterOracle.md",
      "blob_sha256": "10ac64218d4d1b61c02b5548cbb1ddd6a4ce283150053847e000cccb3317ee12",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "The report contains scoped chronology and correction analysis with repository references; no personal, session, credential, authentication, or configuration values appear.",
      "findings": []
    },
    {
      "path": ".ufo/waves/round-18/falsify/AttackTokDeadSeatCrossCheck.md",
      "blob_sha256": "a488868ba5d322b3f2205210b16326d4dc624177278d834e840f83a3f843ee0d",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "The report describes privacy risks in a separate target without reproducing the underlying session or per-seat values; remaining content is scoped surface and technical analysis.",
      "findings": []
    },
    {
      "path": ".ufo/waves/round-18/falsify/ReopenOwaspAsvs.md",
      "blob_sha256": "76f1ed727cd93e7236e46e52b3690367293e1b03dd67eee0dd019b6aef245e7e",
      "decision": "retain",
      "content_basis": "content-reviewed",
      "reason": "The source review contains public-source quotations, scoped citation judgments, and aggregate limitations; no actual private, credential, authentication, or configuration values appear.",
      "findings": []
    }
  ]
}