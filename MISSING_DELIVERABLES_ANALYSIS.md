# Missing Deliverables Analysis - CO3095 Group Assignment

**Analysis Date:** Based on current project state and assignment brief review  
**Excluded from Analysis:** Video, Written Report, Cover Sheet, GitHub Board Setup (as per user request)

---

## 🔍 REMAINING MISSING DELIVERABLES

### ❌ CRITICAL MISSING ITEMS

#### 1. Visual Diagrams and Charts

**Status:** ⚠️ **DATA EXISTS, BUT VISUAL CHARTS/DIAGRAMS ARE MISSING**

**Assignment Requirement:** Video demonstration must show burndown charts, PERT diagram, EVM charts, and velocity charts. These must be visual images/charts, not just data tables.

##### 1.1 Burndown Charts (3 charts required)
**Current State:**
- ✅ Data tables exist: `docs/burndown_charts/sprint1_burndown_data.md`, `sprint2_burndown_data.md`, `sprint3_burndown_data.md`
- ❌ **Visual charts/images are NOT created**

**Action Required:**
- Create visual burndown charts (line graphs) using Excel, Google Sheets, or diagramming tool
- Charts should show Planned Remaining (dashed line) vs Actual Remaining (solid line)
- Export as PNG/JPEG images
- Include in report and video demonstration
- **Required Charts:**
  - Sprint 1 Burndown Chart
  - Sprint 2 Burndown Chart
  - Sprint 3 Burndown Chart

---

##### 1.2 PERT Network Diagram
**Current State:**
- ✅ Calculations exist: `docs/pert_calculations.md`
- ✅ ASCII diagram exists in the document
- ✅ Critical path calculated and documented
- ❌ **Visual PERT network diagram/image is NOT created**

**Action Required:**
- Create visual PERT network diagram using diagramming tool (Draw.io, Lucidchart, MS Visio, PowerPoint, or Google Slides)
- Diagram must show:
  - All activities (nodes)
  - Dependencies (arrows/edges)
  - Critical path (highlighted in different color/thickness)
  - Activity durations
  - Earliest/latest start/finish times
  - Slack/float values
- Export as PNG/JPEG image
- Include in report and video demonstration
- Reference: `docs/pert_calculations.md` for data and structure

---

##### 1.3 EVM Charts (Earned Value Management)
**Current State:**
- ✅ Calculations exist: `docs/evm_calculations.md`
- ✅ Data tables exist for creating charts
- ✅ All EVM metrics calculated (PV, EV, AC, CPI, SPI, EAC, VAC, ETC)
- ❌ **Visual EVM charts/images are NOT created**

**Action Required:**
- Create visual EVM chart (line graph) using Excel or Google Sheets
- Chart must show:
  - Planned Value (PV) line
  - Earned Value (EV) line
  - Actual Cost (AC) line
  - Cumulative values over time (per sprint or per week)
- Export as PNG/JPEG image
- Include in report and video demonstration
- Reference: `docs/evm_calculations.md` for data

---

##### 1.4 Velocity Chart
**Current State:**
- ✅ Data exists: `docs/velocity_tracking.md`
- ✅ Data table with velocity metrics
- ✅ Planned vs Completed velocity calculated for all 3 sprints
- ❌ **Visual velocity chart/image is NOT created**

**Action Required:**
- Create visual velocity chart (bar/column chart) using Excel or Google Sheets
- Chart must show:
  - Planned velocity vs Completed velocity per sprint
  - Sprint 1, Sprint 2, Sprint 3 comparison
  - Visual comparison of planned vs actual
- Export as PNG/JPEG image
- Include in report
- Reference: `docs/velocity_tracking.md` for data

---

#### 2. Planning Poker Evidence

**Assignment Requirement:** Video demonstration must show "Present the estimated story points via planning poker with evidence."

**Current State:**
- ✅ Story points assigned: `docs/planning_poker_story_points.md`
- ✅ Session information documented (tool used: point.poker, participants, dates)
- ✅ All 48 user stories have story points assigned
- ❌ **Visual evidence/screenshots are NOT included**

**Action Required:**
- Take screenshots or photos of Planning Poker session:
  - Screenshot of Planning Poker tool (point.poker or similar) showing voting session
  - Screenshot showing story point assignments for user stories
  - Evidence of team discussion/voting process
  - Screenshot showing final story point assignments
  - Or photos of physical Planning Poker session (if conducted in person)
- Include screenshots/photos in report
- Show screenshots in video demonstration
- Document evidence in `docs/planning_poker_story_points.md` or create separate evidence folder

---

#### 3. Research Component Documentation - Visual Diagrams

**Assignment Requirement:** "You will need to explain how you perform symbolic execution and concolic testing, including drawing the symbolic tree, computing the values, other important elements related to these two techniques, etc in the report."

**Current State:**
- ✅ Research component documentation file EXISTS: `tests/jo213/test/docs/research_symbolic_execution_and_concolic_testing.md`
- ✅ ASCII symbolic trees exist in Section 3 (InputValidator, FileLock)
- ✅ All value computation examples complete (Section 4)
- ✅ Comprehensive function coverage documentation complete (Section 5)
- ✅ Symbolic/concolic tests exist for 23 functions (110 new tests, all passing)
- ✅ Path conditions documented
- ✅ Constraint solving examples documented
- ❌ **Visual symbolic tree diagrams (PNG/JPEG images) are NOT created**

**Action Required:**
- Create visual symbolic tree diagrams for tested functions (23 functions now tested)
- **Priority Functions (High Complexity - CC ≥ 10):**
  - `IntentClassifier.classify_result()` (CC=32) - **HIGHEST PRIORITY**
  - `HistoryStore.load_turns()` (CC=21) - **HIGH PRIORITY**
  - `CLIApp.run_with_io()` (CC=25) - if tested
  - `ResponseGenerator.extract_topic_from_last_user_message()` (CC=11)
  - `ChatEngine._parse_clarification_choice()` (CC=11)
  - `ChatEngine.process_turn()` (CC=12)
- **Other Functions:**
  - `InputValidator.clean()`
  - `FileLock.try_acquire()`
  - `ResponseGenerator.generate()`
  - `ResponseGenerator.route()`
  - `ResponseGenerator.handle_question()`
  - `ResponseGenerator.handle_greeting()`
  - `ResponseGenerator.handle_history()`
  - `ResponseGenerator.handle_unknown()`
  - `ChatEngine._stage_classify_intent()`
  - `ChatEngine._stage_maybe_ask_for_clarification()`
  - `ChatEngine._clarification_options_from_candidates()`
  - `ChatEngine.classify_intent()`
  - `ChatEngine.reset_session()`
  - `ChatEngine.clear_history()`
  - `HistoryStore.save_turn()`
  - `ConversationSession.recent_turns()`
  - `ConversationSession.set_pending_clarification()`
  - `parse_user_input()`
- Use diagramming tool (Draw.io, Lucidchart, or similar)
- Diagrams must show:
  - Symbolic paths explored
  - Branch points and constraints
  - Path coverage visualization
  - Decision nodes and leaf nodes
  - Constraint annotations
- Export as PNG/JPEG images and embed in documentation
- **Note:** ASCII trees exist but visual diagrams are needed for professional presentation in report and video
- **Recommendation:** Focus on high-complexity functions first (CC ≥ 10), then add others as needed
- **Minimum:** Create visual diagrams for at least the 5-6 highest complexity functions (CC ≥ 20)

---

### ⚠️ POTENTIALLY MISSING ITEMS (Need Verification)

#### 4. Test Execution Results/Screenshots

**Assignment Requirement:** Video demonstration must show "Show and run your Black-Box test cases" and "Show and run your White-Box test cases" with "All the test cases and the test results (whether it passed or failed)."

**Current State:**
- ✅ Test files exist and are organized
- ✅ Tests can be run (319 tests total: 163 original + 110 new symbolic/concolic + 46 existing symbolic/concolic)
- ✅ All tests passing (319/319)
- ✅ Test coverage measured: 80% overall coverage
- ✅ HTML coverage report exists: `htmlcov/index.html`
- ❓ **Test execution screenshots/results documentation may be missing**

**Action Required:**
- Run tests and capture screenshots of:
  - Overall test execution (all 319 tests) showing "X passed"
  - Black-box test execution (specification-based and random-based separately)
  - White-box test execution (statement, branch, path coverage separately)
  - Symbolic/concolic test execution (156 tests)
  - Coverage reports (HTML screenshots showing 80% coverage)
  - Terminal output showing test results
- Include screenshots in report
- Show screenshots in video demonstration
- Document which testing tools and techniques were used for each test category

---

#### 5. GitHub Commit History Evidence

**Assignment Requirement:** Video demonstration must show "Show the GitHub commit history of your project that is linked to the user stories."

**Current State:**
- ✅ GitHub usernames documented: `docs/sprint_plan.md` and `docs/test_organization.md`
- ✅ User stories assigned to team members: `docs/sprint_plan.md`
- ❓ **GitHub commit history screenshots may be missing**
- ❓ **Commit messages linking to user stories may need verification**

**Action Required:**
- Verify commit messages reference user stories (e.g., `[US1]`, `#1`, `US1:`, etc.)
- Take screenshots of GitHub commit history showing:
  - Commits linked to user stories
  - Commit messages referencing user story numbers
  - Branch structure (if branches were used for user stories)
  - Commit timeline showing development progress
- Include screenshots in report
- Show screenshots in video demonstration
- Ensure commit messages follow pattern: `[US#] Description` or `US#: Description`

---

#### 6. GitHub Project Board Screenshots

**Assignment Requirement:** Video demonstration must show "For each sprint, show the following details in your SCRUM (GitHub Project) board: The user stories in each sprint, Who is responsible for each user story, The start and end date of each user story."

**Current State:**
- ✅ Sprint plan exists: `docs/sprint_plan.md` with all user stories, assignments, and dates
- ❓ **GitHub Project board screenshots may be missing**

**Action Required:**
- Verify GitHub Project board exists and is accessible
- Take screenshots of GitHub Project board showing:
  - Sprint 1 board view with user stories (US1-US16)
  - Sprint 2 board view with user stories (US17-US32)
  - Sprint 3 board view with user stories (US33-US48)
  - Each screenshot should show:
    - User story numbers and descriptions
    - Assigned team member (who is responsible)
    - Start and end dates
    - Status (To Do, In Progress, Done)
- Include screenshots in report
- Show screenshots in video demonstration
- If GitHub Project board is not set up, create it before submission

---

#### 7. COCOMO and EVM Calculation Evidence

**Assignment Requirement:** Video demonstration must show "Present the cost computed via COCOMO, COCOMO II, EVM and their calculation."

**Current State:**
- ✅ COCOMO I calculations exist: `docs/cocomo_i_calculations.md`
- ✅ COCOMO II calculations exist: `docs/cocomo_ii_calculations.md`
- ✅ EVM calculations exist: `docs/evm_calculations.md`
- ✅ All formulas applied correctly
- ✅ All values calculated and documented
- ❓ **Screenshots or visual presentation of calculations may be missing**

**Action Required:**
- Create visual presentation of calculations:
  - Screenshot or formatted table showing COCOMO I calculation steps
  - Screenshot or formatted table showing COCOMO II calculation steps
  - Screenshot or formatted table showing EVM calculation steps
  - Show formulas and intermediate values
- Include in report
- Show in video demonstration
- Reference calculation documents: `docs/cocomo_i_calculations.md`, `docs/cocomo_ii_calculations.md`, `docs/evm_calculations.md`

---

#### 8. Critical Path Calculation Evidence

**Assignment Requirement:** Video demonstration must show "Show the critical path and its calculation."

**Current State:**
- ✅ PERT calculations exist: `docs/pert_calculations.md`
- ✅ Critical path identified and calculated
- ✅ All activity times calculated (optimistic, pessimistic, most likely, expected)
- ✅ Earliest/latest start/finish times calculated
- ✅ Slack/float values calculated
- ❓ **Visual presentation of critical path calculation may be missing**

**Action Required:**
- Create visual presentation of critical path calculation:
  - Screenshot or formatted table showing critical path calculation steps
  - Show how critical path was identified
  - Show forward pass and backward pass calculations
  - Highlight critical path activities
- Include in report
- Show in video demonstration
- Reference: `docs/pert_calculations.md`

---

## 📋 SUMMARY OF REMAINING MISSING ITEMS

### Visual Diagrams/Charts Required:
1. ❌ Sprint 1 Burndown Chart (visual image)
2. ❌ Sprint 2 Burndown Chart (visual image)
3. ❌ Sprint 3 Burndown Chart (visual image)
4. ❌ PERT Network Diagram (visual image)
5. ❌ EVM Chart (visual image)
6. ❌ Velocity Chart (visual image)
7. ❌ Visual Symbolic Tree Diagrams (minimum 5-6 high-complexity functions, ideally all 23 functions)

### Evidence/Screenshots Required:
8. ❌ Planning Poker session screenshots/photos
9. ❌ Test execution results screenshots (black-box, white-box, coverage)
10. ❌ GitHub commit history screenshots (showing links to user stories)
11. ❌ GitHub Project board screenshots (all 3 sprints with user stories, assignments, dates)

### Documentation/Presentations Required:
12. ❌ COCOMO I calculation presentation/screenshots
13. ❌ COCOMO II calculation presentation/screenshots
14. ❌ EVM calculation presentation/screenshots
15. ❌ Critical path calculation presentation/screenshots

---

**Total Missing Items:** 15 categories  
**Estimated Effort:**
- Visual diagrams: Medium-High (7 diagrams to create)
- Planning Poker evidence: Low (screenshots/photos)
- Test execution screenshots: Low (run tests and capture)
- GitHub evidence: Low-Medium (screenshots of existing GitHub content)
- Calculation presentations: Low (format existing calculations visually)

