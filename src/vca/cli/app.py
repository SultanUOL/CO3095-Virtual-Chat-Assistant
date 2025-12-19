"""
CLI layer for the Virtual Chat Assistant.
Handles input and output only.
"""

from vca.core.engine import ChatEngine


class CliApp:
    """Console application wrapper."""

    def __init__(self) -> None:
        self._engine = ChatEngine()

    def run(self) -> None:
        print("Virtual Chat Assistant")
        print("Type help for commands. Type exit to quit.")
        if self._engine.loaded_turns_count > 0:
            print(f"(Loaded {self._engine.loaded_turns_count} previous turn(s) from history.)")

        try:
            while True:
                user_text = input("You: ")
                cmd = user_text.strip().lower()

                if cmd in {"exit", "quit"}:
                    self._engine.clear_history(clear_file=True)
                    print("Assistant: Goodbye.")
                    break

                reply = self._engine.process_turn(user_text)
                print(f"Assistant: {reply}")

        except KeyboardInterrupt:
            print()
            print("Assistant: Goodbye.")
