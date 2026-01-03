# PERT Network Analysis & Critical Path Calculation

## Project Information

**Project:** Virtual Chat Assistant  
**Total Activities:** 48 user stories (US1-US48)  
**Project Duration:** 3 weeks (3 sprints)

---

## PERT Methodology

PERT (Program Evaluation and Review Technique) is used to:
1. Identify dependencies between activities
2. Calculate earliest and latest start/finish times
3. Determine the critical path (longest path through the network)
4. Calculate slack/float for non-critical activities

---

## Activity Dependencies Analysis

For this project, user stories are organized into 3 sprints with logical dependencies:

### Sprint 1 Dependencies (Foundation)
- **US1-US4:** Core infrastructure (no dependencies)
- **US5-US8:** Build on core infrastructure (depend on US1-US4)
- **US9-US12:** Enhance core features (depend on US1-US8)
- **US13-US16:** Additional features (depend on US1-US12)

### Sprint 2 Dependencies (Enhancement)
- **US17-US20:** Build on Sprint 1 foundation (depend on Sprint 1 completion)
- **US21-US24:** Enhanced features (depend on US17-US20)
- **US25-US28:** Further enhancements (depend on US21-US24)
- **US29-US32:** Additional enhancements (depend on US25-US28)

### Sprint 3 Dependencies (Advanced)
- **US33-US36:** Advanced features (depend on Sprint 2 completion)
- **US37-US40:** Integration features (depend on US33-US36)
- **US41-US44:** Final features (depend on US37-US40)
- **US45-US48:** Integration and testing (depend on US41-US44)

---

## Simplified PERT Network

For calculation purposes, we'll group activities by sprint milestones:

### Activities Summary

| Activity ID | Description | Duration (Days) | Predecessors |
|-------------|-------------|-----------------|--------------|
| A1 | Sprint 1 Foundation (US1-US4) | 2 | - |
| A2 | Sprint 1 Core Features (US5-US8) | 2 | A1 |
| A3 | Sprint 1 Enhancements (US9-US12) | 2 | A2 |
| A4 | Sprint 1 Completion (US13-US16) | 1 | A3 |
| A5 | Sprint 2 Foundation (US17-US20) | 2 | A4 |
| A6 | Sprint 2 Features (US21-US24) | 2 | A5 |
| A7 | Sprint 2 Enhancements (US25-US28) | 2 | A6 |
| A8 | Sprint 2 Completion (US29-US32) | 1 | A7 |
| A9 | Sprint 3 Foundation (US33-US36) | 2 | A8 |
| A10 | Sprint 3 Features (US37-US40) | 2 | A9 |
| A11 | Sprint 3 Enhancements (US41-US44) | 2 | A10 |
| A12 | Sprint 3 Completion (US45-US48) | 1 | A11 |

**Total Duration:** 21 days (3 weeks)

---

## PERT Time Estimates

For each activity, we use three time estimates:
- **Optimistic (O):** Best case scenario
- **Most Likely (M):** Normal scenario
- **Pessimistic (P):** Worst case scenario

### Time Estimates Table

| Activity | Optimistic (O) | Most Likely (M) | Pessimistic (P) | Expected Time (TE) |
|----------|----------------|-----------------|-----------------|-------------------|
| A1 | 1.5 | 2 | 2.5 | 2.00 |
| A2 | 1.5 | 2 | 2.5 | 2.00 |
| A3 | 1.5 | 2 | 2.5 | 2.00 |
| A4 | 0.75 | 1 | 1.25 | 1.00 |
| A5 | 1.5 | 2 | 2.5 | 2.00 |
| A6 | 1.5 | 2 | 2.5 | 2.00 |
| A7 | 1.5 | 2 | 2.5 | 2.00 |
| A8 | 0.75 | 1 | 1.25 | 1.00 |
| A9 | 1.5 | 2 | 2.5 | 2.00 |
| A10 | 1.5 | 2 | 2.5 | 2.00 |
| A11 | 1.5 | 2 | 2.5 | 2.00 |
| A12 | 0.75 | 1 | 1.25 | 1.00 |

**Expected Time Formula:**
```
TE = (O + 4M + P) / 6
```

---

## Forward Pass Calculation (Earliest Times)

Calculate Earliest Start (ES) and Earliest Finish (EF):

| Activity | ES | Duration | EF | Predecessor EF |
|----------|----|----------|----|----------------|
| A1 | 0 | 2 | 2 | - |
| A2 | 2 | 2 | 4 | A1 (EF=2) |
| A3 | 4 | 2 | 6 | A2 (EF=4) |
| A4 | 6 | 1 | 7 | A3 (EF=6) |
| A5 | 7 | 2 | 9 | A4 (EF=7) |
| A6 | 9 | 2 | 11 | A5 (EF=9) |
| A7 | 11 | 2 | 13 | A6 (EF=11) |
| A8 | 13 | 1 | 14 | A7 (EF=13) |
| A9 | 14 | 2 | 16 | A8 (EF=14) |
| A10 | 16 | 2 | 18 | A9 (EF=16) |
| A11 | 18 | 2 | 20 | A10 (EF=18) |
| A12 | 20 | 1 | 21 | A11 (EF=20) |

**Project Completion:** Day 21 (3 weeks)

---

## Backward Pass Calculation (Latest Times)

Calculate Latest Start (LS) and Latest Finish (LF):

| Activity | LF | Duration | LS | Successor LS |
|----------|----|----------|----|--------------|
| A12 | 21 | 1 | 20 | - (End) |
| A11 | 20 | 2 | 18 | A12 (LS=20) |
| A10 | 18 | 2 | 16 | A11 (LS=18) |
| A9 | 16 | 2 | 14 | A10 (LS=16) |
| A8 | 14 | 1 | 13 | A9 (LS=14) |
| A7 | 13 | 2 | 11 | A8 (LS=13) |
| A6 | 11 | 2 | 9 | A7 (LS=11) |
| A5 | 9 | 2 | 7 | A6 (LS=9) |
| A4 | 7 | 1 | 6 | A5 (LS=7) |
| A3 | 6 | 2 | 4 | A4 (LS=6) |
| A2 | 4 | 2 | 2 | A3 (LS=4) |
| A1 | 2 | 2 | 0 | A2 (LS=2) |

---

## Slack/Float Calculation

**Total Float = LS - ES = LF - EF**

| Activity | ES | EF | LS | LF | Total Float | Status |
|----------|----|----|----|----|-------------|--------|
| A1 | 0 | 2 | 0 | 2 | 0 | **Critical** |
| A2 | 2 | 4 | 2 | 4 | 0 | **Critical** |
| A3 | 4 | 6 | 4 | 6 | 0 | **Critical** |
| A4 | 6 | 7 | 6 | 7 | 0 | **Critical** |
| A5 | 7 | 9 | 7 | 9 | 0 | **Critical** |
| A6 | 9 | 11 | 9 | 11 | 0 | **Critical** |
| A7 | 11 | 13 | 11 | 13 | 0 | **Critical** |
| A8 | 13 | 14 | 13 | 14 | 0 | **Critical** |
| A9 | 14 | 16 | 14 | 16 | 0 | **Critical** |
| A10 | 16 | 18 | 16 | 18 | 0 | **Critical** |
| A11 | 18 | 20 | 18 | 20 | 0 | **Critical** |
| A12 | 20 | 21 | 20 | 21 | 0 | **Critical** |

---

## Critical Path

**Critical Path:** All activities have zero float, meaning the entire path is critical.

**Critical Path:**
```
A1 → A2 → A3 → A4 → A5 → A6 → A7 → A8 → A9 → A10 → A11 → A12
```

**Critical Path Duration:**
```
2 + 2 + 2 + 1 + 2 + 2 + 2 + 1 + 2 + 2 + 2 + 1 = 21 days
```

**Critical Path = 21 days (3 weeks)**

---

## PERT Network Diagram (ASCII)

```
                    START
                      |
        [A1: 2 days]
         US1-US4
           |
        [A2: 2 days]
         US5-US8
           |
        [A3: 2 days]
         US9-US12
           |
        [A4: 1 day]
        US13-US16
           |
        [A5: 2 days]
        US17-US20
           |
        [A6: 2 days]
        US21-US24
           |
        [A7: 2 days]
        US25-US28
           |
        [A8: 1 day]
        US29-US32
           |
        [A9: 2 days]
        US33-US36
           |
        [A10: 2 days]
        US37-US40
           |
        [A11: 2 days]
        US41-US44
           |
        [A12: 1 day]
        US45-US48
           |
                    END
```

**Note:** This is a serial network with no parallel paths, making all activities critical.

---

## Critical Path Analysis

### Why All Activities Are Critical

In this project structure:
- Each sprint builds on the previous one
- Activities are sequential with clear dependencies
- No parallel paths exist
- Any delay in any activity delays the entire project

### Critical Path Characteristics

1. **Zero Slack:** All activities have zero total float
2. **Longest Path:** Critical path is the longest path (21 days)
3. **Project Duration:** Determined by critical path = 21 days
4. **No Buffer:** No flexibility in scheduling

---

## PERT Variance and Standard Deviation

### Variance Calculation

**Variance Formula:**
```
σ² = ((P - O) / 6)²
```

| Activity | σ² | σ (Standard Deviation) |
|----------|-----|------------------------|
| A1 | 0.0278 | 0.167 |
| A2 | 0.0278 | 0.167 |
| A3 | 0.0278 | 0.167 |
| A4 | 0.0069 | 0.083 |
| A5 | 0.0278 | 0.167 |
| A6 | 0.0278 | 0.167 |
| A7 | 0.0278 | 0.167 |
| A8 | 0.0069 | 0.083 |
| A9 | 0.0278 | 0.167 |
| A10 | 0.0278 | 0.167 |
| A11 | 0.0278 | 0.167 |
| A12 | 0.0069 | 0.083 |

**Total Variance (Critical Path):**
```
σ²_total = 0.0278 × 9 + 0.0069 × 3 = 0.2502 + 0.0207 = 0.2709
```

**Standard Deviation:**
```
σ_total = √0.2709 = 0.521 days
```

---

## Probability Analysis

### Probability of Completing in 21 Days

Using Z-score:
```
Z = (Target - Expected) / σ
Z = (21 - 21) / 0.521 = 0
```

**Probability:** 50% (median of normal distribution)

### Probability of Completing in 20 Days

```
Z = (20 - 21) / 0.521 = -1.92
Probability ≈ 2.7% (low probability)
```

### Probability of Completing in 22 Days

```
Z = (22 - 21) / 0.521 = 1.92
Probability ≈ 97.3% (high probability)
```

---

## Conclusions

1. **Critical Path:** Entire project path is critical (no slack)
2. **Duration:** 21 days (3 weeks) matches planned duration
3. **Dependencies:** Sequential dependencies ensure quality but reduce flexibility
4. **Risk:** Any delay affects project completion date
5. **Probability:** 50% chance of completing exactly on time (21 days)

---

## Recommendations

1. **Buffer Management:** Consider adding small buffers between sprints
2. **Parallel Work:** Where possible, identify opportunities for parallel development
3. **Risk Mitigation:** Monitor critical path activities closely
4. **Contingency:** Plan for potential delays in critical activities

---

## Notes

- PERT analysis assumes sequential dependencies between sprints
- Actual project structure may have some parallel work within sprints
- Critical path represents the minimum project duration
- All activities are on the critical path due to sequential structure
- Variance calculations provide probability estimates for completion dates

---

## Instructions for Visual Diagram

To create a visual PERT diagram:

1. **Use Draw.io or similar tool**
2. **Create nodes** for each activity (A1-A12)
3. **Draw arrows** showing dependencies (A1→A2→A3→...→A12)
4. **Label nodes** with activity ID, duration, and user stories
5. **Highlight critical path** in red or bold
6. **Include time estimates** (ES, EF, LS, LF) on nodes

**Example Node Format:**
```
[A1]
US1-US4
Duration: 2 days
ES: 0, EF: 2
LS: 0, LF: 2
Float: 0 (Critical)
```

