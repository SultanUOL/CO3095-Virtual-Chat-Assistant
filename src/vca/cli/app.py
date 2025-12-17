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

        try:
            while True:
                user_text = input("You: ")
                reply = self._engine.process_turn(user_text)
                print(f"Assistant: {reply}")

                if self._engine.classify_intent(user_text) == "exit":
                    break
        except KeyboardInterrupt:
            print()
            print("Assistant: Goodbye.")
