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

## Project structure
- src/vca/cli: CLI entry and loop
- src/vca/core: engine, intents, responses
- src/vca/storage: history persistence

## Logs and persisted files
Conversation history is stored in data/history.txt.

Interaction analytics are stored in data/interaction_log.jsonl.
Each line is a JSON object containing timestamp_utc, input_length, intent, and fallback_used.
User message content is not stored in the interaction log.
