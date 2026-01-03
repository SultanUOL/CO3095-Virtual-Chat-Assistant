# Missing Deliverables Analysis - CO3095 Group Assignment

**Analysis Date:** Based on current project state  
**Excluded from Analysis:** Video, Written Report, Cover Sheet, GitHub Board Setup

---

## 🔍 IN-DEPTH ANALYSIS OF MISSING DELIVERABLES

### ❌ CRITICAL MISSING ITEMS

#### 1. Visual Diagrams and Charts

**Status:** ⚠️ **DATA EXISTS, BUT VISUAL CHARTS/DIAGRAMS ARE MISSING**

##### 1.1 Burndown Charts (3 charts required)
**Current State:**
- ✅ Data tables exist: `docs/burndown_charts/sprint1_burndown_data.md`, `sprint2_burndown_data.md`, `sprint3_burndown_data.md`
- ❌ **Visual charts/images are NOT created**
- ✅ Instructions for creating charts are provided in the data files

**Required:**
- **Sprint 1 Burndown Chart** (visual image/diagram)
- **Sprint 2 Burndown Chart** (visual image/diagram)
- **Sprint 3 Burndown Chart** (visual image/diagram)

**Action Required:**
- Create visual burndown charts (line graphs) using Excel, Google Sheets, or diagramming tool
- Charts should show Planned Remaining (dashed line) vs Actual Remaining (solid line)
- Export as PNG/JPEG images
- Include in report and video demonstration
- Charts can be created from data in `docs/burndown_charts/` folder

---

##### 1.2 PERT Network Diagram
**Current State:**
- ✅ Calculations exist: `docs/pert_calculations.md`
- ✅ ASCII diagram exists in the document
- ❌ **Visual PERT network diagram/image is NOT created**

**Required:**
- Visual PERT network diagram showing:
  - All activities (nodes)
  - Dependencies (arrows/edges)
  - Critical path (highlighted)
  - Activity durations
  - Earliest/latest start/finish times
  - Slack/float values

**Action Required:**
- Create visual PERT network diagram using:
  - Diagramming tool (Draw.io, Lucidchart, MS Visio)
  - Or PowerPoint/Google Slides
  - Or specialized PERT diagram software
- Export as PNG/JPEG image
- Include in report and video demonstration
- Reference: `docs/pert_calculations.md` for data and structure

---

##### 1.3 EVM Charts (Earned Value Management)
**Current State:**
- ✅ Calculations exist: `docs/evm_calculations.md`
- ✅ Data tables exist for creating charts
- ❌ **Visual EVM charts/images are NOT created**

**Required:**
- EVM chart showing:
  - Planned Value (PV) line
  - Earned Value (EV) line
  - Actual Cost (AC) line
  - Cumulative values over time

**Action Required:**
- Create visual EVM chart (line graph) using Excel or Google Sheets
- Export as PNG/JPEG image
- Include in report and video demonstration
- Reference: `docs/evm_calculations.md` for data

---

##### 1.4 Velocity Chart
**Current State:**
- ✅ Data exists: `docs/velocity_tracking.md`
- ✅ Data table with velocity metrics
- ❌ **Visual velocity chart/image is NOT created**

**Required:**
- Velocity chart showing:
  - Planned velocity vs Completed velocity per sprint
  - Sprint 1, Sprint 2, Sprint 3 comparison

**Action Required:**
- Create visual velocity chart (bar/column chart) using Excel or Google Sheets
- Export as PNG/JPEG image
- Include in report
- Reference: `docs/velocity_tracking.md` for data

---

#### 2. Planning Poker Evidence

**Current State:**
- ✅ Story points assigned: `docs/planning_poker_story_points.md`
- ✅ Session information documented (tool used, participants, dates)
- ❌ **Visual evidence/screenshots are NOT included**

**Required:**
- Screenshots or evidence of Planning Poker session:
  - Screenshot of Planning Poker tool (point.poker or similar)
  - Screenshot showing story point assignments
  - Evidence of team discussion/voting process
  - Or photos of physical Planning Poker session

**Action Required:**
- If session was digital: Take screenshots during/after session
- If session was physical: Take photos of cards/voting
- Include screenshots/photos in report
- Document evidence in `docs/planning_poker_story_points.md` or create separate evidence folder

---

#### 3. Research Component Documentation

**Current State:**
- ❌ **MISSING** - Research component documentation file does not exist
- ⚠️ **INCOMPLETE** - Symbolic and concolic testing should be applied to ALL code functions developed
- ❓ **UNCLEAR** - Current test organization references symbolic/concolic tests but directories may be missing
- Expected location: `tests/jo213/test/docs/research_symbolic_execution_and_concolic_testing.md` (does not exist)

**Required (Based on Assignment Requirements):**
- Research component document on Symbolic Execution and Concolic Testing
- Document MUST explain:
  - **What symbolic execution is** (research/explanation)
  - **What concolic testing is** (research/explanation)
  - **How symbolic execution was performed** (detailed explanation)
  - **How concolic testing was performed** (detailed explanation)
  - **Drawing the symbolic tree** (visual diagram showing symbolic execution tree)
  - **Computing the values** (showing value computations)
  - **Other important elements** related to both techniques
  - **Application to ALL code functions developed** (not just a few)
  - Which functions were tested using these techniques
  - Results and analysis

**Critical Requirements:**
- ⚠️ **Symbolic execution and concolic testing must be applied to ALL code functions developed**
- This is in ADDITION to all other taught testing techniques
- Must include visual symbolic tree diagrams
- Must show value computations
- Must be comprehensive and detailed

**Current Test Coverage:**
- Currently only 2-3 functions have symbolic/concolic tests:
  - `FileLock.try_acquire()` (symbolic)
  - `InputValidator.clean()` (symbolic and concolic)
- Many more functions need symbolic/concolic testing to meet "ALL functions" requirement

**Key Functions That Need Symbolic/Concolic Testing:**
Based on codebase analysis, major functions that should have symbolic/concolic tests include:
- `IntentClassifier.classify_result()` (CC=32, critical function)
- `ChatEngine.process_turn()` (CC=12, core engine)
- `ResponseGenerator.generate()` and related handlers
- `HistoryStore.load_turns()` (CC=21)
- `CLIApp.run_with_io()` (CC=25)
- And other developed functions

**Action Required:**
1. ✅ Create research component documentation file: `tests/jo213/test/docs/research_symbolic_execution_and_concolic_testing.md`
2. ✅ Verify/create symbolic and concolic test directories: `tests/jo213/test/whitebox/symbolic/` and `tests/jo213/test/whitebox/concolic/`
3. ⚠️ **CRITICAL:** Create symbolic/concolic tests for ALL developed functions (currently only 2-3 functions have tests - need many more)
4. Include symbolic tree diagrams in the documentation (visual diagrams required)
5. Include value computation examples (show actual computations)
6. Document should be comprehensive (typically 2-5 pages minimum)
7. Include in report and reference in video demonstration
8. Focus on high-complexity functions (CC ≥ 10) first, then expand to others

---

### ⚠️ POTENTIALLY MISSING ITEMS (Need Verification)

#### 4. Test Execution Results/Screenshots

**Current State:**
- ✅ Test files exist and are organized
- ✅ Tests can be run (163 tests)
- ❓ **Test execution screenshots/results documentation may be missing**

**Required:**
- Screenshots or documentation showing:
  - Test execution results (pytest output)
  - Test pass/fail status
  - Coverage reports (HTML screenshots)
  - Test execution by technique (black-box, white-box separately)

**Action Required:**
- Run tests and capture screenshots of:
  - Overall test execution (all tests)
  - Black-box test execution
  - White-box test execution
  - Coverage report screenshots
- Include screenshots in report
- Show in video demonstration (but video is excluded from this analysis)

---

#### 5. Source Code Documentation/Comments

**Current State:**
- ✅ Source code exists in `src/vca/`
- ❓ **Code comments and documentation may need verification**

**Required:**
- Code should be well-commented
- Functions should have docstrings
- Complex logic should have inline comments
- README.md should be comprehensive (already exists)

**Action Required:**
- Review source code for adequate comments
- Ensure all functions have docstrings
- Verify code is readable and well-documented

---

#### 6. Requirements/Dependencies File

**Current State:**
- ✅ `requirements.txt` exists
- ❓ **May need verification that it includes all dependencies**

**Required:**
- Complete `requirements.txt` with all Python dependencies
- Should include: pytest, pytest-cov, and any other dependencies

**Action Required:**
- Verify `requirements.txt` is complete
- Ensure all dependencies are listed
- Test that `pip install -r requirements.txt` works

---
