# Video Demonstration Script Guide
## CO3095 Virtual Chat Assistant - Group Project

This document outlines what each team member should talk about and demonstrate in the video submission.

---



## Video Overview

**Duration:** Approximately 20-30 minutes  
**Format:** Screen recording with narration  
**Structure:** Organized by sections, with each team member presenting their assigned areas

---

### 2. Written Report (PDF)
**Requirement:** Comprehensive written report with all required sections

**Status:** ❌ **NOT CREATED**

**Note:** Documentation exists in `docs/` folder, but needs to be compiled into a formal report format (PDF)

**Required Sections:**
- Introduction
- Project Overview
- Agile/Scrum Methodology
  - Planning Poker evidence (use `docs/planning_poker_story_points.md`)
  - Sprint organization (use `docs/sprint_plan.md`)
  - PERT analysis (use `docs/pert_calculations.md`)
  - COCOMO I & II (use `docs/cocomo_i_calculations.md`, `docs/cocomo_ii_calculations.md`)
  - Burndown charts (use `docs/burndown_charts/`)
  - Velocity tracking (use `docs/velocity_tracking.md`)
  - EVM (use `docs/evm_calculations.md`)
- Testing and Test Coverage
  - Black-box testing (reference `docs/test_organization.md`)
  - White-box testing (reference `docs/test_organization.md`)
  - Test coverage measurements (use `docs/test_coverage_analysis.md` - 80% coverage)
  - Research component: Symbolic Execution & Concolic Testing (reference `tests/jo213/test/docs/research_symbolic_execution_and_concolic_testing.md`)
- Development Tools
  - GitHub usage
  - Project board
- Complexity Metrics
  - Cyclomatic complexity analysis (use `docs/cyclomatic_complexity_analysis.md`)
- Conclusion

**Action Required:**
- Compile all documentation from `docs/` folder into report format
- Include all required sections listed above
- Format as academic report
- Export as PDF
- Submit separately (not in repository)

---


## Video Structure & Team Member Assignments

### Part 1: Introduction & Setup (5 minutes)
**Presenter: Wafiq Gborigi (wg73) - Scrum Master**
*Contributions: Conversation flow engine, general query handling, logging functionality (35 SP)*

#### Section 1.1: Project Introduction (1 minute)
- Introduce the Virtual Chat Assistant project
- Explain the project scope and goals
- Mention the 3-sprint Agile Scrum approach
- Provide overview of team structure (4 members)
- Mention your role as Scrum Master (coordinating ceremonies, maintaining Scrum board)

#### Section 1.2: How to Compile and Run the Code (2 minutes)
- Navigate to project directory
- Show project structure (`src/`, `tests/`, `docs/`)
- Demonstrate setting up virtual environment:
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # or .venv\Scripts\activate on Windows
  pip install -r requirements.txt
  ```
- Show how to run the application:
  ```bash
  python -m vca.main
  # or
  python src/vca/main.py
  ```
- Explain basic usage and command-line interface
- Mention your work on the conversation flow engine that orchestrates the system

#### Section 1.3: Software Features Demonstration (2 minutes)
- Demonstrate key features with focus on your contributions:
  - **Conversation flow engine** (your work: US5-US8, US21-US24, US37-US40)
  - **General query handling** (conversation context management)
  - Question handling ("what is Python?")
  - Command processing (`/help`, `/history`, `/exit`)
  - **Logging functionality** (your work)
  - History persistence
- Show a brief interactive session (2-3 turns)
- Highlight main capabilities, especially conversation flow and query handling

---

### Part 2: Project Planning & Management (8 minutes)
**Presenter: Ayomide Adebanjo (ma1059) - Documentation Lead**

#### Section 2.1: Planning Poker & Story Points (3 minutes)
- Explain Planning Poker methodology
- Show Planning Poker evidence (screenshots/photos from point.poker sessions)
- Present story points estimation:
  - Total: 140 story points across 3 sprints
  - Sprint 1: 39 SP, Sprint 2: 43 SP, Sprint 3: 58 SP
- Show story point distribution per team member
- Explain Fibonacci sequence usage (2, 3, 5, 8, 13)
- Reference: `docs/planning_poker_story_points.md`

#### Section 2.2: GitHub Project Board - Sprint Overview (3 minutes)
**For each sprint (1, 2, 3):**
- Navigate to GitHub Project Board
- Show user stories in the sprint:
  - **Sprint 1:** US1-US16 (39 SP)
  - **Sprint 2:** US17-US32 (43 SP)
  - **Sprint 3:** US33-US48 (58 SP)
- For each sprint, show:
  - User story numbers
  - Assigned team member (who is responsible)
  - Start date and end date for each user story
  - Story points assigned
  - Status (Completed/In Progress/To Do)
- Screenshot each sprint view clearly
- **Note:** Each user story has corresponding black-box tests (specification-based and random-based) that verify acceptance criteria. These tests are demonstrated through user story validation.

#### Section 2.3: GitHub Commit History (2 minutes)
- Navigate to GitHub repository
- Show commit history
- Demonstrate how commits are linked to user stories:
  - Commit messages contain user story references (e.g., `[US1]`, `US1:`, `fix US1`)
  - Filter commits by user story ID
- Show examples of commits for each sprint
- Explain commit message format and traceability
- Show branch structure if applicable (feature branches per story)

---

### Part 3: Core Features & Architecture (6 minutes)
**Presenter: Sultan Adekoya (sa1068) - Architecture Lead**
*Contributions: Greeting, help, exit commands, intent classification, CLI setup, initial project structure (37 SP)*

#### Section 3.1: Architecture Overview & Project Structure (2 minutes)
- Explain the modular, layered architecture you set up
- Show project structure you established:
  - `src/vca/` (core modules)
  - `src/vca/core/` (engine, intents, responses)
  - `src/vca/cli/` (command-line interface you implemented)
  - `src/vca/storage/` (persistence layer)
  - `src/vca/domain/` (domain models)
- Show initial project setup and structure decisions
- Explain architectural decisions and separation of concerns

#### Section 3.2: Command-Line Interface & Core Commands (2 minutes)
- Demonstrate the CLI you implemented (your work: CLI setup)
- Show the commands you implemented:
  - **`/help` command** (your work: US1, US17)
  - **`/exit` command** (your work: US3, US19)
  - **Greeting recognition** (your work: US2, US18)
- Show command parsing and routing logic
- Demonstrate how commands are processed through the CLI layer
- Mention your user stories: US1-US4 (Sprint 1), US17-US20 (Sprint 2), US33-US36 (Sprint 3)

#### Section 3.3: Intent Classification System (2 minutes)
- Explain the intent classification system you implemented
- Show `IntentClassifier` class and keyword matching logic
- Demonstrate intent detection:
  - Greeting intents ("hello", "hi", "greetings")
  - Question intents ("what is", "how does", "tell me about")
  - Command intents (help, exit, history)
  - Unknown intent handling
- Show how intent classification integrates with the engine
- Mention your contribution to specification-based testing and symbolic analysis
- Reference: `src/vca/core/intents.py` (your work: US4, US20, US34, US36)

---

### Part 4: Cost Estimation & Project Metrics (6 minutes)
**Presenter: Ayomide Adebanjo (ma1059) - Documentation Lead**
*Contributions: Input validation, response handling, conversation history, planning documentation (31 SP)*

#### Section 4.1: PERT Analysis & Critical Path (2 minutes)
- Explain PERT (Program Evaluation and Review Technique) methodology
- Show PERT Network Diagram (visual diagram)
  - Activities (nodes) with IDs
  - Dependencies (arrows/edges)
  - Critical path highlighted
  - Duration estimates (O, M, P)
- Present Critical Path Calculation:
  - Show forward pass calculation
  - Show backward pass calculation
  - Explain how critical path was identified (zero slack activities)
  - Show critical path duration: 21 days
  - Explain why critical path equals project duration
- Reference: `docs/pert_calculations.md`

#### Section 4.2: COCOMO I & II Cost Estimation (3 minutes)
- Explain COCOMO models (Basic Organic and Post-Architecture)
- **COCOMO I Calculation:**
  - Show formula: E = 2.4 × (KLOC)^1.05
  - Show calculation: E = 2.4 × (3.206)^1.05 = 8.16 person-months
  - Show schedule: T = 2.5 × (8.16)^0.38 = 5.55 months
  - Show staffing: 8.16 / 5.55 = 1.47 people
- **COCOMO II Calculation:**
  - Show scale factors (PREC, FLEX, RESL, TEAM, PMAT)
  - Show formula with scale factors
  - Show calculation: E = 5.39 person-months, T = 6.20 months
  - Show staffing: 0.87 people
- **Comparison with Actual:**
  - Actual: 3.0 PM, 0.75 months, 4 people
  - Explain differences (commercial vs academic project)
- Reference: `docs/cocomo_i_calculations.md`, `docs/cocomo_ii_calculations.md`

#### Section 4.3: Earned Value Management (EVM) (1 minute)
- Explain EVM methodology
- Show EVM Chart (visual line graph)
  - Planned Value (PV) curve
  - Earned Value (EV) curve
  - Actual Cost (AC) curve
  - Explain that all three curves overlap (perfect performance)
- Present key metrics:
  - CPI (Cost Performance Index) = 1.00 (on budget)
  - SPI (Schedule Performance Index) = 1.00 (on schedule)
  - EAC = 140 SP, VAC = 0 SP
- Explain what these metrics mean (100% completion, no overruns)
- Reference: `docs/evm_calculations.md`

---

### Part 5: Testing - White-Box Techniques (8 minutes)
**Presenter: John Onwuemezia (jo213) - Testing Lead**

#### Section 5.1: White-Box Testing Overview (1 minute)
- Explain white-box testing approach (internal structure, code coverage)
- Mention techniques: Statement Coverage, Branch Coverage, Path Coverage
- Mention research component: Symbolic Execution and Concolic Testing
- Show test organization structure:
  ```
  tests/
  ├── wg73/test/whitebox/
  ├── sa1068/test/whitebox/
  ├── jo213/test/whitebox/  (includes symbolic/concolic)
  └── ma1059/test/whitebox/
  ```

#### Section 5.2: Statement Coverage Tests (1.5 minutes)
- Explain statement coverage (ensuring all executable statements are executed)
- Show naming convention: `studentid.test.whitebox.statement_coverage`
- Run statement coverage tests:
  ```bash
  python -m pytest tests/wg73/test/whitebox/statement_coverage/ -v
  python -m pytest tests/sa1068/test/whitebox/statement_coverage/ -v
  python -m pytest tests/jo213/test/whitebox/statement_coverage/ -v
  python -m pytest tests/ma1059/test/whitebox/statement_coverage/ -v
  ```
- Show test results
- Explain coverage target (80% overall)

#### Section 5.3: Branch Coverage Tests (1.5 minutes)
- Explain branch coverage (all decision branches tested: if/else, loops)
- Show naming convention: `studentid.test.whitebox.branch_coverage`
- Run branch coverage tests:
  ```bash
  python -m pytest tests/wg73/test/whitebox/branch_coverage/ -v
  python -m pytest tests/sa1068/test/whitebox/branch_coverage/ -v
  python -m pytest tests/jo213/test/whitebox/branch_coverage/ -v
  python -m pytest tests/ma1059/test/whitebox/branch_coverage/ -v
  ```
- Show test results
- Explain how branch coverage exercises rare branches (error handlers, edge cases)

#### Section 5.4: Path Coverage Tests (1 minute)
- Explain path coverage (multiple execution paths through complex functions)
- Show naming convention: `studentid.test.whitebox.path_coverage`
- Run path coverage tests:
  ```bash
  python -m pytest tests/wg73/test/whitebox/path_coverage/ -v
  python -m pytest tests/sa1068/test/whitebox/path_coverage/ -v
  python -m pytest tests/jo213/test/whitebox/path_coverage/ -v
  python -m pytest tests/ma1059/test/whitebox/path_coverage/ -v
  ```
- Show test results
- Explain how path coverage tests complex functions with multiple paths

#### Section 5.5: Symbolic Execution (Research Component) (2 minutes)
- Explain symbolic execution methodology
  - Modelling inputs as symbolic variables
  - Deriving path conditions
  - Selecting concrete inputs for each path
- Show naming convention: `studentid.test.whitebox.symbolic`
- Show test organization: `tests/jo213/test/whitebox/symbolic/`
- List functions tested with symbolic execution (23 functions):
  - `InputValidator.clean()` (7 paths)
  - `FileLock.try_acquire()` (4 paths)
  - `IntentClassifier.classify_result()` (8 paths)
  - `ChatEngine.process_turn()` (7 paths)
  - `HistoryStore.load_turns()` (multiple paths)
  - `ResponseGenerator.generate()` (multiple paths)
  - `ConversationSession.recent_turns()` (multiple paths)
  - And 16 additional functions
- Show symbolic execution test files:
  ```bash
  python -m pytest tests/jo213/test/whitebox/symbolic/ -v
  ```
- Show test results (9 test files, all passing)
- Show visual symbolic tree diagrams (if available) for high-complexity functions
- Reference: `tests/jo213/test/docs/research_symbolic_execution_and_concolic_testing.md`

#### Section 5.6: Concolic Testing (Research Component) (1 minute)
- Explain concolic testing methodology
  - Combining concrete execution with symbolic tracking
  - Using real execution traces to identify uncovered branches
  - Using constraint solvers to generate inputs
- Show naming convention: `studentid.test.whitebox.concolic`
- Show test organization: `tests/jo213/test/whitebox/concolic/`
- Run concolic tests:
  ```bash
  python -m pytest tests/jo213/test/whitebox/concolic/ -v
  ```
- Show test results (8 test files, all passing)
- Explain how concolic testing added 110 new tests and found subtle bugs
- Mention issues found and fixed (missing default responses, file-handling errors)

---

### Part 6: Test Coverage Analysis (3 minutes)
**Presenter: John Onwuemezia (jo213) - Testing Lead**

#### Section 6.1: Overall Test Coverage (1.5 minutes)
- Explain test coverage measurement tool: **pytest-cov** (pytest-cov plugin)
- Run coverage analysis:
  ```bash
  python -m pytest --cov=src --cov-report=term --cov-report=html tests/
  ```
- Show overall coverage results:
  - **Overall Statement Coverage: 80%** (Excellent threshold: ≥70%)
  - Total Statements: 1,556
  - Statements Covered: 1,243
  - Statements Missed: 313
- Explain what 80% coverage means (meets excellent grade threshold)

#### Section 6.2: Module-by-Module Coverage (1.5 minutes)
- Open HTML coverage report: `htmlcov/index.html`
- Show module-by-module coverage breakdown:
  - `vca/core/intents.py`: 97% (Outstanding)
  - `vca/core/responses.py`: 89% (Excellent)
  - `vca/core/validator.py`: 91% (Excellent)
  - `vca/core/engine.py`: 80% (Excellent)
  - `vca/storage/history_store.py`: 81% (Excellent)
  - `vca/storage/interaction_log_store.py`: 97% (Outstanding)
- Explain that critical modules achieved 90-97% coverage
- Show coverage summary table
- Reference: `docs/test_coverage_analysis.md`

---

### Part 7: Response Handling & Validation (3 minutes)
**Presenter: Ayomide Adebanjo (ma1059) - Documentation Lead**
*Contributions: Input validation, response handling, conversation history persistence (31 SP)*

#### Section 7.1: Input Validation System (1.5 minutes)
- Explain the input validation system you implemented
- Show `InputValidator` class and validation logic (your work: US13, US29)
  - Non-empty input validation
  - Length limits and truncation
  - Safety checks and sanitization
- Demonstrate validation in action:
  - Empty input handling
  - Long input truncation
  - Special character handling
- Show how validation integrates with the conversation flow
- Reference: `src/vca/core/validator.py` (your work)

#### Section 7.2: Response Handling & History Persistence (1.5 minutes)
- Explain the response generation system you worked on
- Show `ResponseGenerator` class (your work: US14, US30, US31, US32)
  - Response selection based on intent
  - Context-aware responses
  - Fallback responses
- Demonstrate conversation history persistence (your work: US15, US45, US46, US47, US48)
- Show `HistoryStore` and how conversation turns are saved
- Show JSONL file format (`data/history.jsonl`)
- Demonstrate loading and saving conversation history
- Reference: `src/vca/core/responses.py`, `src/vca/storage/history_store.py` (your work)

---

### Part 7.5: Burndown Charts & Velocity (2 minutes)
**Presenter: Ayomide Adebanjo (ma1059) - Documentation Lead**
*As Documentation Lead, you compiled these planning documents*

#### Section 7.5.1: Burndown Charts (1 minute)
- Explain burndown charts (tracking remaining work over time)
- Show 3 burndown charts (Sprint 1, 2, 3):
  - Visual line graphs showing Planned vs Actual Remaining Story Points
  - Each sprint shows linear burn-down from total SP to zero
  - Actual remaining closely tracks planned remaining
  - All sprints completed on schedule (reached 0 SP by Day 7)
- Reference: `docs/burndown_charts/sprint1_burndown_data.md`, `sprint2_burndown_data.md`, `sprint3_burndown_data.md`

#### Section 7.5.2: Velocity Tracking (1 minute)
- Explain velocity (story points completed per sprint)
- Show velocity chart (bar/column chart):
  - Sprint 1: 39 SP (planned) vs 39 SP (completed) - 100%
  - Sprint 2: 43 SP (planned) vs 43 SP (completed) - 100%
  - Sprint 3: 58 SP (planned) vs 58 SP (completed) - 100%
  - Average Velocity: 47 SP per sprint
- Explain that 100% completion indicates accurate estimation and disciplined execution
- Reference: `docs/velocity_tracking.md`

---

### Part 8: Conclusion & Summary (2 minutes)
**Presenter: All Team Members (30 seconds each)**

#### Section 8.1: Individual Reflections
- **Wafiq (wg73):** Summarize Scrum Master role, coordination of ceremonies, conversation flow engine, general query handling, logging functionality (35 SP delivered). Learned: balancing technical contribution with coordination responsibilities, delegation, conflict-resolution skills.

- **Sultan (sa1068):** Summarize architecture lead role, setting up project structure, implementing greeting/help/exit commands, intent classification system, CLI setup (37 SP delivered). Learned: importance of early architectural decisions, close collaboration with testers.

- **John (jo213):** Summarize testing lead role, implementing advanced commands and error-handling features, designing symbolic and concolic test cases, configuring coverage measurement (37 SP delivered). Learned: deepened understanding of white-box testing techniques, ability to explain complex testing concepts clearly to the team.

- **Ayomide (ma1059):** Summarize documentation lead role, implementing input validation, response handling, conversation history persistence, compiling planning documentation (31 SP delivered). Learned: balancing programming tasks with documentation responsibilities, importance of precision and clarity in technical reporting.

#### Section 8.2: Project Summary
- **Wafiq (wg73):** Key achievements:
  - 48 user stories completed (140 SP total)
  - 100% sprint completion (all sprints on schedule)
  - 319 tests (all passing)
  - 80% test coverage (exceeds excellent threshold)
  - Perfect EVM performance (CPI=SPI=1.00)
- Thank viewers and conclude

---

## Video Production Checklist

### Before Recording
- [ ] All team members review this script
- [ ] Practice each section (especially command execution)
- [ ] Prepare all screenshots/diagrams in advance
- [ ] Ensure GitHub Project Board is set up and accessible
- [ ] Verify all tests pass before recording
- [ ] Prepare visual charts/diagrams (burndown, PERT, EVM, velocity)
- [ ] Have Planning Poker evidence ready (screenshots/photos)

### During Recording
- [ ] Use clear screen recording software (OBS, QuickTime, etc.)
- [ ] Speak clearly and at moderate pace
- [ ] Highlight important information (mouse movements, zoom in on key metrics)
- [ ] Pause briefly when showing test results (allow time to read)
- [ ] Ensure command outputs are visible and readable
- [ ] Show file paths and directory structure clearly

### After Recording
- [ ] Review entire video for accuracy
- [ ] Check audio quality (clear narration)
- [ ] Verify all required sections are included
- [ ] Ensure video is within time limits (20-30 minutes recommended)
- [ ] Add timestamps/chapters if possible
- [ ] Export in required format (MP4 recommended)

---

## Key Talking Points Summary

### Wafiq Gborigi (wg73) - Scrum Master
*Contributions: Conversation flow engine, general query handling, logging functionality (35 SP)*
- **Sections:** Introduction, Setup, Features Demo (Conversation Flow), Conclusion
- **Key Points:**
  - Project overview and team structure (Scrum Master role)
  - How to compile and run the code
  - Software features demonstration (focus on conversation flow engine, query handling)
  - Logging functionality
  - Total 35 SP delivered across 3 sprints (US5-US8, US21-US24, US37-US40)
  - Learned: balancing technical contribution with coordination, delegation, conflict-resolution

### Sultan Adekoya (sa1068) - Architecture Lead
*Contributions: Greeting, help, exit commands, intent classification, CLI setup, project structure (37 SP)*
- **Sections:** Architecture Overview, CLI & Core Commands, Intent Classification
- **Key Points:**
  - Architecture overview and project structure setup
  - Command-line interface implementation (`/help`, `/exit`, greeting commands)
  - Intent classification system (keyword matching, intent detection)
  - Total 37 SP delivered across 3 sprints (US1-US4, US17-US20, US33-US36)
  - Learned: early architectural decisions, close collaboration with testers

### John Onwuemezia (jo213) - Testing Lead
*Contributions: Advanced commands, error-handling, symbolic/concolic testing, coverage measurement (37 SP)*
- **Sections:** White-Box Testing, Symbolic/Concolic, Test Coverage
- **Key Points:**
  - White-box testing techniques (statement, branch, path coverage)
  - Symbolic execution (23 functions, 9 test files) - Research Component
  - Concolic testing (8 test files, 110 new tests) - Research Component
  - Test coverage analysis (80% overall, module breakdown)
  - Coverage measurement tool configuration
  - Total 37 SP delivered across 3 sprints (US9-US12, US25-US28, US41-US44)
  - Learned: white-box testing techniques, explaining complex concepts clearly

### Ayomide Adebanjo (ma1059) - Documentation Lead
*Contributions: Input validation, response handling, conversation history, planning documentation (31 SP)*
- **Sections:** Planning Poker, GitHub Board, Commit History, Validation & Responses, History, Burndown, Velocity, Cost Estimation
- **Key Points:**
  - Planning Poker methodology and story points (140 SP total)
  - GitHub Project Board (3 sprints, user stories, assignments, dates)
  - GitHub commit history (linked to user stories)
  - Input validation system implementation
  - Response handling and conversation history persistence
  - Burndown charts (3 sprints, all on schedule)
  - Velocity tracking (100% completion, 47 SP average)
  - Cost estimation (PERT, COCOMO I & II, EVM)
  - Total 31 SP delivered across 3 sprints (US13-US16, US29-US32, US45-US48)
  - Learned: balancing programming with documentation, precision and clarity in reporting

---

#---