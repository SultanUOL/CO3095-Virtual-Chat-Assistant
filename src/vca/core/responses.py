"""
Response generation based on intent and conversation state.
Backbone only.
"""


class ResponseGenerator:
    """Generates assistant replies."""
    _ECHO_LIMIT = 200

    def generate(self, intent: str, raw_text: str) -> str:
        if intent is None:
            safe_intent = "unknown"
        else:
            safe_intent = str(intent)

        if raw_text is None:
            text = ""
        else:
            text = str(raw_text)

        stripped = text.strip()

        if safe_intent == "empty":
            return "Type a message and I will respond. You can also type help."

        if safe_intent == "help":
            return "Commands: help, history, exit. Otherwise type any message to get a basic reply."

        if safe_intent == "history":
            return "History is not available yet in User Story 1."

        if safe_intent == "exit":
            return "Goodbye."

        preview = stripped
        if len(preview) > self._ECHO_LIMIT:
            preview = preview[: self._ECHO_LIMIT] + "..."

        if preview == "":
            return "I did not catch that. Type a message or type help."

        return f"You said: {preview}"
