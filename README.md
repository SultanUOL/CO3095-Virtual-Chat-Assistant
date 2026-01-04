# CO3095-Virtual-Chat-Assistant
Backend Python Virtual Chat Assistant for CO3095 Software Measurement and Quality Assurance, focusing on Agile Scrum development, software quality metrics, and comprehensive black box and white box testing.

# CO3095 Virtual Chat Assistant

## Setup Instructions for Charles Wilson Laboratory

This section provides detailed instructions for uncompressing, importing, setting up, and running the project in the Charles Wilson laboratory environment.

### Step 1: Uncompress the Project

1. Locate the submitted `.zip` file on the computer
2. Right-click on the `.zip` file and select "Extract All..." (Windows) or double-click to extract (macOS)
3. Choose a destination folder (e.g., Desktop or Documents)
4. Extract the files. The extracted folder should be named `CO3095-Virtual-Chat-Assistant`

### Step 2: Import into PyCharm

1. **Open PyCharm** (Professional or Community Edition)

2. **Open the Project:**
   - Click `File` → `Open...`
   - Navigate to the extracted `CO3095-Virtual-Chat-Assistant` folder
   - Select the folder and click `OK`

3. **Configure Project Interpreter:**
   - Go to `File` → `Settings` (Windows/Linux) or `PyCharm` → `Preferences` (macOS)
   - Navigate to `Project: CO3095-Virtual-Chat-Assistant` → `Python Interpreter`
   - Click the gear icon ⚙️ → `Add...`
   - Select `Virtualenv Environment` → `New environment`
   - Location: `.venv` (within the project folder)
   - Base interpreter: Select Python 3.11 (should be available in the lab)
   - Click `OK` to create the virtual environment

4. **Mark Sources Root:**
   - Right-click on the `src/` folder in the Project Explorer
   - Select `Mark Directory as` → `Sources Root`

### Step 3: Install Dependencies and Setup

1. **Open Terminal in PyCharm:**
   - Click `Terminal` tab at the bottom of PyCharm, or
   - Go to `Tools` → `Terminal`

2. **Verify Virtual Environment is Active:**
   - You should see `(.venv)` in the terminal prompt
   - If not, activate it:
     - **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
     - **macOS/Linux:** `source .venv/bin/activate`

3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - `pytest>=7.0.0` (for running tests)
   - `pytest-cov>=4.0.0` (for test coverage reports)

4. **Verify Installation:**
   ```bash
   python --version  # Should show Python 3.11.x
   pytest --version  # Should show pytest version
   ```

### Step 4: Run the Application

**Method 1: Using PyCharm Run Configuration**
1. Right-click on `src/vca/main.py`
2. Select `Run 'main'`

**Method 2: Using Terminal**
```bash
python src/vca/main.py
```

The application will start and display:
```
Type `help` for commands and examples. Type `exit` to quit. Type `restart` to start a new session.
```

### Step 5: Run All Test Cases

**Important:** All test commands must be run from the **project root directory**.

1. **Navigate to Project Root (if not already there):**
   ```bash
   cd /path/to/CO3095-Virtual-Chat-Assistant
   # Or simply ensure you're in the project root directory
   ```

2. **Run All Tests (319 tests):**
   ```bash
   python -m pytest tests/ -v
   ```

3. **Run Tests with Coverage Report:**
   ```bash
   python -m pytest --cov=src --cov-report=term --cov-report=html tests/
   ```
   
   To view the HTML coverage report:
   - Open `htmlcov/index.html` in a web browser

4. **Run Tests by Category:**
   
   **All Black-Box Tests:**
   ```bash
   python -m pytest tests/sa1068/test/blackbox/ tests/ma1059/test/blackbox/ tests/jo213/test/blackbox/ tests/wg73/test/blackbox/ -v
   ```
   
   **All White-Box Tests:**
   ```bash
   python -m pytest tests/sa1068/test/whitebox/ tests/ma1059/test/whitebox/ tests/jo213/test/whitebox/ tests/wg73/test/whitebox/ -v
   ```
   
   **Research Component (Symbolic & Concolic):**
   ```bash
   python -m pytest tests/jo213/test/whitebox/symbolic/ tests/jo213/test/whitebox/concolic/ -v
   ```

**For detailed test execution instructions, see [`HOW_TO_RUN_TESTS.md`](HOW_TO_RUN_TESTS.md)**

---

## Requirements
Python 3.11  
Windows PowerShell or PyCharm terminal  
PyCharm recommended  
pytest>=7.0.0  
pytest-cov>=4.0.0

## Application Usage

Once the application is running, you will see:

```
Type `help` for commands and examples. Type `exit` to quit. Type `restart` to start a new session.
```

### Common Commands
- `help` - Shows the list of commands and examples
- `restart` - Starts a new in-memory session
- `exit` - Quits the application

You can also use prefixed commands like `/help`, `/restart`, and `/exit`.

## History and logs
Conversation history is stored in `data/history.jsonl`.  
Interaction analytics are stored in `data/interaction_log.jsonl`.

## Project structure
- `src/vca/cli`: CLI entry and command loop  
- `src/vca/core`: engine, intents, responses, settings, logging  
- `src/vca/domain`: domain constants and runtime path configuration  
- `src/vca/storage`: file-based persistence layers  

## Logs and persisted files
Conversation history is stored in `data/history.jsonl`.

System errors and exceptions are written to `logs/system_errors.log` with a timestamp and error type. Stack traces are suppressed in the CLI output.

Interaction analytics are stored in `data/interaction_log.jsonl`.

Each line is a JSON object containing `timestamp_utc`, `input_length`, `intent`, and `fallback_used`.  
User message content is not stored in the interaction log.

## Testing
To run the full automated test suite:

`python -m pytest`

**⚠️ Important:** All test commands must be run from the **project root directory**. 

**📖 For detailed instructions on running tests, see [`HOW_TO_RUN_TESTS.md`](HOW_TO_RUN_TESTS.md)**

The test suite includes:
- **319 total tests** (all passing)
- Black-box tests: Specification-based and Random-based
- White-box tests: Statement, Branch, Path coverage
- Research component: Symbolic Execution and Concolic Testing (as per assignment requirements, these techniques should be applied to all code functions developed by each team member)

**Note on Research Component:** According to the assignment brief, symbolic execution and concolic testing are research components that should be applied to all code functions developed by each team member, following the naming convention `your_studentid.test.whitebox.symbolic` and `your_studentid.test.whitebox.concolic`. Currently, these tests are implemented in `tests/jo213/test/whitebox/symbolic/` and `tests/jo213/test/whitebox/concolic/` covering 23 functions across the codebase.

For test coverage analysis, see `docs/test_coverage_analysis.md` (80% overall coverage).
