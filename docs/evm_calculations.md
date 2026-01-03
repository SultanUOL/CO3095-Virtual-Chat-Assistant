# Earned Value Management (EVM) Calculations

## Project Information

**Project:** Virtual Chat Assistant  
**Total Story Points:** 140 SP  
**Number of Sprints:** 3  
**Project Duration:** 3 weeks (0.75 months)  
**Team Size:** 4 members

---

## EVM Basic Concepts

EVM uses Story Points as a proxy for value/cost since this is an academic project without actual monetary costs.

**Budget at Completion (BAC):** Total planned story points = 140 SP  
**Measurement Method:** Story Points completed

---

## EVM Metrics at Project Completion

### Budget at Completion (BAC)
```
BAC = Total Planned Story Points
BAC = 140 SP
```

### Actual Completion
- **Sprint 1 Completed:** 39 SP
- **Sprint 2 Completed:** 43 SP
- **Sprint 3 Completed:** 58 SP
- **Total Completed:** 140 SP

---

## Earned Value Calculations

### After Sprint 1

**Planned Value (PV):**
```
PV = Planned story points for Sprint 1
PV = 39 SP
```

**Earned Value (EV):**
```
EV = Actual story points completed in Sprint 1
EV = 39 SP
```

**Actual Cost (AC):**
```
AC = Story points "spent" (using SP as proxy for effort)
AC = 39 SP
```

**Performance Indices:**
```
CPI (Cost Performance Index) = EV / AC
CPI = 39 / 39 = 1.00

SPI (Schedule Performance Index) = EV / PV
SPI = 39 / 39 = 1.00
```

**Status:** ✅ On budget and on schedule

---

### After Sprint 2

**Planned Value (PV):**
```
PV = Planned story points for Sprint 1 + Sprint 2
PV = 39 + 43 = 82 SP
```

**Earned Value (EV):**
```
EV = Actual story points completed (Sprint 1 + Sprint 2)
EV = 39 + 43 = 82 SP
```

**Actual Cost (AC):**
```
AC = Story points "spent"
AC = 82 SP
```

**Performance Indices:**
```
CPI = EV / AC = 82 / 82 = 1.00
SPI = EV / PV = 82 / 82 = 1.00
```

**Status:** ✅ On budget and on schedule

---

### After Sprint 3 (Project Completion)

**Planned Value (PV):**
```
PV = Total planned story points
PV = 140 SP
```

**Earned Value (EV):**
```
EV = Total actual story points completed
EV = 140 SP
```

**Actual Cost (AC):**
```
AC = Total story points "spent"
AC = 140 SP
```

**Performance Indices:**
```
CPI = EV / AC = 140 / 140 = 1.00
SPI = EV / PV = 140 / 140 = 1.00
```

**Status:** ✅ Project completed on budget and on schedule

---

## Forecast Calculations

### Estimate at Completion (EAC)

**Formula 1: EAC = BAC / CPI**
```
EAC = 140 / 1.00 = 140 SP
```

**Formula 2: EAC = AC + (BAC - EV)**
```
EAC = 140 + (140 - 140) = 140 SP
```

**EAC = 140 SP** (matches BAC - project on track)

### Variance at Completion (VAC)

```
VAC = BAC - EAC
VAC = 140 - 140 = 0 SP
```

**VAC = 0 SP** (no variance - perfect performance)

### Estimate to Complete (ETC)

```
ETC = EAC - AC
ETC = 140 - 140 = 0 SP
```

**ETC = 0 SP** (project complete)

---

## EVM Summary Table

| Metric | After Sprint 1 | After Sprint 2 | After Sprint 3 (Final) |
|--------|---------------|----------------|------------------------|
| **BAC** | 140 SP | 140 SP | 140 SP |
| **PV** | 39 SP | 82 SP | 140 SP |
| **EV** | 39 SP | 82 SP | 140 SP |
| **AC** | 39 SP | 82 SP | 140 SP |
| **CPI** | 1.00 | 1.00 | 1.00 |
| **SPI** | 1.00 | 1.00 | 1.00 |
| **EAC** | 140 SP | 140 SP | 140 SP |
| **VAC** | 0 SP | 0 SP | 0 SP |
| **ETC** | 101 SP | 58 SP | 0 SP |

---

## Performance Analysis

### Cost Performance Index (CPI)

**CPI = 1.00** throughout the project

**Interpretation:**
- CPI = 1.00: Exactly on budget
- No cost overruns or savings
- Efficient use of resources
- Perfect cost performance

### Schedule Performance Index (SPI)

**SPI = 1.00** throughout the project

**Interpretation:**
- SPI = 1.00: Exactly on schedule
- No schedule delays or acceleration
- Planned work completed as scheduled
- Perfect schedule performance

---

## Key Performance Indicators

### Overall Performance
- ✅ **Cost Performance:** Excellent (CPI = 1.00)
- ✅ **Schedule Performance:** Excellent (SPI = 1.00)
- ✅ **Project Status:** Completed successfully
- ✅ **Variance:** Zero variance from plan

### Project Health
- **Green Status:** All metrics indicate healthy project
- **On Track:** Project completed exactly as planned
- **Efficient:** No waste, no delays
- **Successful:** All objectives met

---

## EVM Chart Data

### For Creating EVM Charts (Excel/Google Sheets)

**Data for Cumulative EVM Chart:**
```
Sprint,PV,EV,AC
Sprint 1,39,39,39
Sprint 2,82,82,82
Sprint 3,140,140,140
```

**Chart Type:** Line chart showing PV, EV, AC over time

**Formatting:**
- PV (Planned Value): Blue line
- EV (Earned Value): Green line
- AC (Actual Cost): Red line
- Y-axis: 0 to 140 SP
- X-axis: Sprint 1, Sprint 2, Sprint 3

---

## Interpretation & Conclusions

### Project Success Factors

1. **Accurate Planning:** Story points accurately estimated
2. **Effective Execution:** All planned work completed
3. **Team Performance:** Excellent coordination and delivery
4. **Agile Methodology:** Effective sprint planning and execution

### EVM Insights

1. **Perfect Performance:** CPI and SPI both at 1.00 indicate:
   - Accurate initial estimates
   - Effective project management
   - Good team coordination
   - Successful agile implementation

2. **Zero Variance:** VAC = 0 indicates:
   - No scope creep
   - No budget overruns
   - No schedule delays
   - Perfect execution

3. **Predictability:** Consistent performance across all sprints shows:
   - Reliable estimation process
   - Predictable team velocity
   - Effective planning poker process
   - Good project control

---

## Notes

- EVM calculations use Story Points as a proxy for value/cost
- This is appropriate for academic projects without monetary budgets
- Perfect CPI and SPI (1.00) indicate ideal project execution
- All metrics demonstrate successful project completion
- EVM analysis validates the effectiveness of agile methodology and team coordination

---

## Recommendations

1. **Maintain Practices:** Continue using accurate estimation and planning
2. **Document Learnings:** Capture successful practices for future projects
3. **Team Recognition:** Acknowledge excellent team performance
4. **Process Improvement:** While performance was perfect, always look for improvement opportunities

