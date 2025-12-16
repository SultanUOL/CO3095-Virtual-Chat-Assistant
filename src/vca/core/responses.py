"""
Response generation based on intent and conversation state.
Backbone only.
"""


class ResponseGenerator:
    """Generates assistant replies."""

    def generate(self, intent: str, raw_text: str) -> str:
        """
        Return a response string for the given intent.

        Sprint 1 will implement response rules and safe fallbacks.
        """
        raise NotImplementedError("Sprint 1 will implement generate.")
