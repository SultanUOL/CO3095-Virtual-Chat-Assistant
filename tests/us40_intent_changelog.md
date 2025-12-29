# tests/us40_intent_changelog.md

US40 finalises intent handling by consolidating the tuned rules and ensuring the engine routes every supported intent through a concrete handler without falling back to the generic error response.

The main changes across US37 to US39 were tightening matching to avoid partial substring triggers, introducing a single source of truth for synonym and phrase rules, and enforcing deterministic priority where exit overrides help and help overrides normal conversation intents. Ambiguous and low confidence cases follow a consistent clarification policy so the system asks the user instead of guessing.

US40 adds a final set of engine level tests that exercise each supported intent with at least two representative inputs, plus a small guard test that confirms priority behaviour remains stable after tuning.