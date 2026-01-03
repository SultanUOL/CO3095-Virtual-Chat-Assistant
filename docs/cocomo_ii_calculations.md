# COCOMO II Cost Estimation

## Project Information

**Project Type:** Organic (Post-Architecture Model)  
**Project Duration:** 1 month (3 weeks development)  
**Team Size:** 4 members  
**Lines of Code (LOC):** 3,206  
**KLOC (Thousands of Lines of Code):** 3.206 KLOC  
**Model Used:** Post-Architecture Model

---

## COCOMO II Model Selection

**Selected Model:** Post-Architecture Model

**Rationale:**
- Project architecture is defined
- Design and implementation phase
- Suitable for detailed estimation

---

## COCOMO II Formula

```
Effort (E) = A × (Size)^E × ∏(EMi) person-months
```

Where:
- **A = 2.94** (constant for post-architecture model)
- **Size = KLOC** (source lines of code)
- **E = B + 0.01 × Σ(SFi)** (exponent based on scale factors)
- **EMi = Effort Multipliers**

---

## Step 1: Calculate Scale Factors (SF)

Scale factors determine the exponent E in the effort equation.

| Scale Factor | Rating | Value | Rationale |
|--------------|--------|-------|-----------|
| **PREC** (Precedentedness) | Nominal | 3.72 | Similar to previous projects |
| **FLEX** (Development Flexibility) | High | 2.03 | Agile methodology, flexible requirements |
| **RESL** (Architecture/Risk Resolution) | High | 2.83 | Good architecture, low risk |
| **TEAM** (Team Cohesion) | High | 2.19 | Small, cohesive team |
| **PMAT** (Process Maturity) | Nominal | 4.68 | Standard development process |

**Total Scale Factors:**
```
Σ(SFi) = 3.72 + 2.03 + 2.83 + 2.19 + 4.68 = 15.45
```

**Exponent Calculation:**
```
E = B + 0.01 × Σ(SFi)
E = 0.91 + 0.01 × 15.45
E = 0.91 + 0.1545
E = 1.0645
```

---

## Step 2: Select Effort Multipliers (EM)

### Product Factors

| Factor | Rating | Value | Rationale |
|--------|--------|-------|-----------|
| **RELY** (Required Reliability) | Nominal | 1.00 | Standard reliability requirements |
| **DATA** (Database Size) | Nominal | 1.00 | Small database (file-based) |
| **CPLX** (Product Complexity) | Nominal | 1.00 | Moderate complexity application |
| **RUSE** (Developed for Reuse) | Low | 0.95 | Some reusable components |
| **DOCU** (Documentation Match) | Nominal | 1.00 | Standard documentation |

### Platform Factors

| Factor | Rating | Value | Rationale |
|--------|--------|-------|-----------|
| **TIME** (Execution Time Constraint) | Nominal | 1.00 | No strict time constraints |
| **STOR** (Main Storage Constraint) | Nominal | 1.00 | No storage constraints |
| **PVOL** (Platform Volatility) | Nominal | 1.00 | Stable platform (Python) |

### Personnel Factors

| Factor | Rating | Value | Rationale |
|--------|--------|-------|-----------|
| **ACAP** (Analyst Capability) | High | 0.86 | Capable analysts |
| **PCAP** (Programmer Capability) | High | 0.86 | Capable programmers |
| **PCON** (Personnel Continuity) | Nominal | 1.00 | Stable team |
| **APEX** (Applications Experience) | Nominal | 1.00 | Moderate experience |
| **PLEX** (Platform Experience) | High | 0.91 | Good Python/PyCharm experience |
| **LTEX** (Language & Tool Experience) | High | 0.91 | Good Python experience |

### Project Factors

| Factor | Rating | Value | Rationale |
|--------|--------|-------|-----------|
| **TOOL** (Use of Software Tools) | High | 0.91 | Modern tools (PyCharm, pytest) |
| **SITE** (Multisite Development) | Nominal | 1.00 | Single site (virtual collaboration) |
| **SCED** (Required Development Schedule) | Nominal | 1.00 | Standard schedule |

### Calculate Product of Effort Multipliers

```
∏(EMi) = RELY × DATA × CPLX × RUSE × DOCU × TIME × STOR × PVOL ×
         ACAP × PCAP × PCON × APEX × PLEX × LTEX × TOOL × SITE × SCED

∏(EMi) = 1.00 × 1.00 × 1.00 × 0.95 × 1.00 × 1.00 × 1.00 × 1.00 ×
         0.86 × 0.86 × 1.00 × 1.00 × 0.91 × 0.91 × 0.91 × 1.00 × 1.00

∏(EMi) = 0.95 × 0.86 × 0.86 × 0.91 × 0.91 × 0.91
∏(EMi) = 0.95 × 0.7396 × 0.753571
∏(EMi) = 0.530
```

---

## Step 3: Calculate Effort

**Given:**
- A = 2.94
- Size = 3.206 KLOC
- E = 1.0645
- ∏(EMi) = 0.530

**Calculation:**
```
E = 2.94 × (3.206)^1.0645 × 0.530
E = 2.94 × 3.449 × 0.530
E = 5.38 person-months
```

**Result: Effort = 5.38 person-months**

---

## Step 4: Calculate Schedule

### Schedule Formula
```
Schedule (T) = 3.67 × (Effort)^(0.28 + 0.2 × (E - B)) months
```

Where:
- B = 0.91 (base exponent)
- E = 1.0645 (calculated exponent)

**Calculation:**
```
T = 3.67 × (5.38)^(0.28 + 0.2 × (1.0645 - 0.91))
T = 3.67 × (5.38)^(0.28 + 0.2 × 0.1545)
T = 3.67 × (5.38)^(0.28 + 0.0309)
T = 3.67 × (5.38)^0.3109
T = 3.67 × 1.657
T = 6.08 months
```

**Result: Schedule = 6.08 months**

---

## Step 5: Calculate Staffing

```
Staffing = Effort / Schedule
Staffing = 5.38 / 6.08
Staffing = 0.88 people (≈ 1 person)
```

**Result: Staffing = 0.88 people (≈ 1 person)**

---

## Results Summary

| Metric | Value | Unit |
|--------|-------|------|
| **Lines of Code** | 3,206 | LOC |
| **KLOC** | 3.206 | KLOC |
| **Scale Factor Sum** | 15.45 | - |
| **Exponent (E)** | 1.0645 | - |
| **Effort Multiplier Product** | 0.530 | - |
| **Effort** | 5.38 | person-months |
| **Schedule** | 6.08 | months |
| **Staffing** | 0.88 | people (≈ 1) |

---

## Comparison: COCOMO I vs COCOMO II

| Metric | COCOMO I | COCOMO II | Actual |
|--------|----------|-----------|--------|
| Effort | 8.10 PM | 5.38 PM | ~3.0 PM* |
| Schedule | 5.50 months | 6.08 months | 0.75 months |
| Staffing | 1.47 people | 0.88 people | 4 people |

*Actual effort: 4 people × 0.75 months = 3.0 person-months

### Analysis

**COCOMO II vs COCOMO I:**
- COCOMO II estimates **lower effort** (5.38 vs 8.10 PM) due to:
  - More refined model
  - Better tool usage (TOOL = 0.91)
  - High personnel capability ratings
  - High team cohesion

**Both Models vs Actual:**
- Both models estimate longer schedules than actual
- Actual project completed much faster due to:
  - Parallel development (4 people)
  - Agile methodology
  - Modern development tools
  - Clear, well-understood requirements
  - Good team coordination

**Key Differences:**
1. **Model Sophistication:** COCOMO II accounts for more factors (17 EM vs basic model)
2. **Modern Practices:** Actual project benefits from modern tools and methodologies
3. **Team Size:** Models suggest 1 person, but 4-person team enables parallel work

---

## Conclusions

1. **COCOMO II provides more refined estimates** than COCOMO I
2. **Both models are conservative** for small, agile projects
3. **Actual project efficiency** exceeded model predictions
4. **Models serve as baseline** for project planning and comparison
5. **Agile methodology and modern tools** significantly improve productivity beyond model assumptions

---

## Notes

- COCOMO II is more sophisticated and accounts for modern development practices
- Effort multipliers reflect our project's strengths (good tools, capable team)
- Scale factors indicate a relatively low-complexity, flexible project
- Actual results demonstrate the value of agile methodologies and parallel development
- Models provide theoretical baselines useful for project planning and comparison

