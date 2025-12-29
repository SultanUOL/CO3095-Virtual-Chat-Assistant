US37 rule tuning notes

Observed issues

Some help style questions such as "what can you do" were classified as question because they matched the generic question prefix rule.

Changes made

Added an explicit help phrase rule for common capability and command queries.
When the help phrase rule matches, the question rules are skipped so the classifier is deterministic and confidence stays aligned with the help rule strength.

Expected impact

Help intent coverage increases for capability queries while existing priority behaviour for multi intent inputs remains unchanged.