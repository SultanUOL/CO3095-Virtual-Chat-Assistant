# Missing Deliverables Analysis - CO3095 Group Assignment

**Analysis Date:** Based on current project state  
**Excluded from Analysis:** Video, Written Report, Cover Sheet, GitHub Board Setup

---

## 🔍 REMAINING MISSING DELIVERABLES

### ❌ CRITICAL MISSING ITEMS

#### 1. Visual Diagrams and Charts

**Status:** ⚠️ **DATA EXISTS, BUT VISUAL CHARTS/DIAGRAMS ARE MISSING**

All data and calculations are complete. Visual charts/images need to be created for the video demonstration and report.

##### 1.1 Burndown Charts (3 charts required)
- ❌ **Visual charts/images are NOT created**
- **Action:** Create 3 line graphs (Sprint 1, 2, 3) showing Planned vs Actual Remaining
- **Data Source:** `docs/burndown_charts/sprint1_burndown_data.md`, `sprint2_burndown_data.md`, `sprint3_burndown_data.md`
- **Tool:** Excel, Google Sheets, or diagramming tool
- **Export:** PNG/JPEG images

##### 1.2 PERT Network Diagram
- ❌ **Visual PERT network diagram/image is NOT created**
- **Action:** Create network diagram showing activities, dependencies, critical path (highlighted), durations, ES/EF/LS/LF times, and slack values
- **Data Source:** `docs/pert_calculations.md`
- **Tool:** Draw.io, Lucidchart, MS Visio, PowerPoint, or Google Slides
- **Export:** PNG/JPEG image

##### 1.3 EVM Charts (Earned Value Management)
- ❌ **Visual EVM charts/images are NOT created**
- **Action:** Create line graph showing PV, EV, and AC lines over time
- **Data Source:** `docs/evm_calculations.md`
- **Tool:** Excel or Google Sheets
- **Export:** PNG/JPEG image

##### 1.4 Velocity Chart
- ❌ **Visual velocity chart/image is NOT created**
- **Action:** Create bar/column chart showing Planned vs Completed velocity for all 3 sprints
- **Data Source:** `docs/velocity_tracking.md`
- **Tool:** Excel or Google Sheets
- **Export:** PNG/JPEG image

---

#### 2. Planning Poker Evidence

- ❌ **Visual evidence/screenshots are NOT included**
- **Action:** Take screenshots/photos of Planning Poker session:
  - Screenshot of Planning Poker tool (point.poker) showing voting session
  - Screenshot showing story point assignments
  - Evidence of team discussion/voting process
- **Data Source:** `docs/planning_poker_story_points.md` (has data, needs visual evidence)
- **Include:** In report and video demonstration

---

#### 3. Research Component - Visual Symbolic Tree Diagrams

- ❌ **Visual symbolic tree diagrams (PNG/JPEG images) are NOT created**
- **Current State:** ASCII trees exist, but visual diagrams needed for professional presentation
- **Action:** Create visual symbolic tree diagrams for tested functions
- **Priority Functions (Focus on these first):**
  - `IntentClassifier.classify_result()` (CC=32) - **HIGHEST PRIORITY**
  - `HistoryStore.load_turns()` (CC=21) - **HIGH PRIORITY**
  - `ChatEngine.process_turn()` (CC=12)
  - `ResponseGenerator.extract_topic_from_last_user_message()` (CC=11)
  - `ChatEngine._parse_clarification_choice()` (CC=11)
- **Minimum:** Create visual diagrams for at least 5-6 highest complexity functions (CC ≥ 20)
- **Tool:** Draw.io, Lucidchart, or similar
- **Must Show:** Symbolic paths, branch points, constraints, path coverage, decision nodes
- **Export:** PNG/JPEG images
- **Reference:** `tests/jo213/test/docs/research_symbolic_execution_and_concolic_testing.md`

---

### ⚠️ ITEMS REQUIRING ACTION (Need to Capture/Create)

#### 4. Test Execution Results/Screenshots

- ❓ **Test execution screenshots/results documentation may be missing**
- **Action:** Run tests and capture screenshots of:
  - Overall test execution (all 319 tests) showing "X passed"
  - Black-box test execution (specification-based and random-based)
  - White-box test execution (statement, branch, path coverage)
  - Symbolic/concolic test execution (156 tests)
  - Coverage reports (HTML screenshots showing 80% coverage)
- **Include:** In report and video demonstration

---

#### 5. GitHub Evidence

##### 5.1 Commit History Screenshots
- ❓ **GitHub commit history screenshots may be missing**
- **Action:** 
  - Verify commit messages reference user stories (e.g., `[US1]`, `US1:`, etc.)
  - Take screenshots showing commits linked to user stories, commit messages, branch structure, timeline
- **Include:** In report and video demonstration

##### 5.2 Project Board Screenshots
- ❓ **GitHub Project board screenshots may be missing**
- **Action:** 
  - Verify GitHub Project board exists and is accessible
  - Take screenshots for each sprint (Sprint 1: US1-US16, Sprint 2: US17-US32, Sprint 3: US33-US48)
  - Each screenshot should show: user story numbers, assigned team member, start/end dates, status
- **Include:** In report and video demonstration
- **Note:** If GitHub Project board is not set up, create it before submission

---

#### 6. Calculation Presentation Evidence

##### 6.1 COCOMO I & II Calculation Presentations
- ❓ **Visual presentation of calculations may be missing**
- **Action:** Create screenshots or formatted tables showing:
  - COCOMO I calculation steps with formulas and intermediate values
  - COCOMO II calculation steps with formulas and intermediate values
- **Data Source:** `docs/cocomo_i_calculations.md`, `docs/cocomo_ii_calculations.md`
- **Include:** In report and video demonstration

##### 6.2 EVM Calculation Presentation
- ❓ **Visual presentation of EVM calculations may be missing**
- **Action:** Create screenshot or formatted table showing EVM calculation steps
- **Data Source:** `docs/evm_calculations.md`
- **Include:** In report and video demonstration

##### 6.3 Critical Path Calculation Presentation
- ❓ **Visual presentation of critical path calculation may be missing**
- **Action:** Create screenshot or formatted table showing:
  - Critical path calculation steps
  - How critical path was identified
  - Forward pass and backward pass calculations
  - Critical path activities highlighted
- **Data Source:** `docs/pert_calculations.md`
- **Include:** In report and video demonstration

---