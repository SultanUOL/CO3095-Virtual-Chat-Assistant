"""vca.domain.constants

Application-wide constants for conversation management and storage.

These constants define limits and configuration values used throughout the
application, including history retention policies, context window sizes, and
storage durability settings.
"""

HISTORY_MAX_TURNS = 500

CONTEXT_WINDOW_TURNS = 3
HISTORY_FSYNC_EVERY_WRITES = 10
HISTORY_LOAD_LIMIT_TURNS = HISTORY_MAX_TURNS
