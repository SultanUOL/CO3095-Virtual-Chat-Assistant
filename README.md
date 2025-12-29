# CO3095-Virtual-Chat-Assistant
Backend Python Virtual Chat Assistant for CO3095 Software Measurement and Quality Assurance, focusing on Agile Scrum development, software quality metrics, and comprehensive black box and white box testing.

# CO3095 Virtual Chat Assistant

## Requirements
Python 3.11
PyCharm

## How to run
1. Open this folder in PyCharm
2. Ensure the interpreter is set to the project venv
3. Mark `src/` as Sources Root
4. Run: `src/vca/main.py`

## Quick start
When the app starts, you will see:

Type help for commands and examples. Type exit to quit. Type restart to start a new session.

Common commands
help shows the list of commands and examples
restart starts a new in memory session
exit quits the application

You can also use prefixed commands like /help, /restart, and /exit.

History and logs
Conversation history is stored in data/history.jsonl.
Interaction analytics are stored in data/interaction_log.jsonl.

## Project structure
- src/vca/cli: CLI entry and loop
- src/vca/core: engine, intents, responses
- src/vca/storage: history persistence

## Logs and persisted files
Conversation history is stored in data/history.jsonl. System errors and exceptions are written to data/system_errors.log with a timestamp and error type. Stack traces are suppressed in the CLI output.

Interaction analytics are stored in data/interaction_log.jsonl.
Each line is a JSON object containing timestamp_utc, input_length, intent, and fallback_used.
User message content is not stored in the interaction log.
