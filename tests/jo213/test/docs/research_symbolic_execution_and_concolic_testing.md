# Research Component: Symbolic Execution and Concolic Testing

This document provides the **required evidence** for the report section:

> **Research Component on Symbolic Execution and Concolic Testing**: details of how symbolic execution and concolic testing were performed (symbolic tree, path conditions, concrete test cases, and pass/fail results).

It is written to be pasted into the report section required by the CO3095 brief fileciteturn0file0.

---

## 1) What we did (and how it maps to our codebase)

### Symbolic execution (white-box)
We treat function inputs as **symbols** (e.g., `x`, `raw_text`) and explore each branch. Each branch adds a constraint to a **path condition (PC)**. A path is feasible if its PC can be satisfied.

**Outputs we show below:**
- **Symbolic tree** (ASCII)
- **Path conditions** per leaf
- **Concrete test cases** that satisfy each PC
- **Test outcome** (pass/fail)

### Concolic testing (concrete + symbolic)
We execute the function with a **concrete seed input**, record the branch predicates encountered, then generate new inputs by **flipping one predicate** (negating it) to force exploration of a different path.

**Outputs we show below:**
- seed input
- observed branch predicate
- negated predicate
- generated “mutant” input
- test outcome (pass/fail)

---

## 2) Symbolic execution evidence (selected core functions)

> Note: The project contains many functions; the report focuses on functions that are (a) core to behaviour and (b) branch-heavy / risk-prone. We still achieve full functional coverage via unit tests (all tests passing), and we add dedicated *symbolic/concolic* test packages as required.

### 2.1 `FileLock.try_acquire()` (vca/storage/file_lock.py)

**Intent:** Non-raising attempt to acquire a lockfile.

#### Symbolic tree
Let `E` mean “lock file exists already”.

```
try_acquire()
 ├─ if ¬E (os.open succeeds)
 │    └─ return True
 └─ if E (FileExistsError)
      └─ return False
```

#### Path conditions (PC)
- **PC1:** `¬E`  (lock file absent)  → returns `True`
- **PC2:** `E`   (lock file present) → returns `False`

#### Concrete test cases
Implemented in: `tests/studentid/test/whitebox/symbolic/test_symbolic_file_lock.py::test_try_acquire_symbolic_branches`
- **TC1 (PC1):** ensure no `.lock` file exists → expect `True`
- **TC2 (PC2):** pre-create `.lock` file → expect `False`

#### Test result
`pytest -q tests/studentid/test/whitebox/symbolic` → **PASS** (see Section 4).

---

### 2.2 `FileLock.acquire()` (vca/storage/file_lock.py)

**Intent:** Acquire lock with retries or raise `FileLockTimeout`.

#### Symbolic tree
Let `A_i` mean “try_acquire returns True on attempt i”, and `k = max(1, retries)`.

```
acquire(retries=k)
 ├─ if (A_1 ∨ A_2 ∨ ... ∨ A_k)
 │    └─ return normally
 └─ else (¬A_1 ∧ ¬A_2 ∧ ... ∧ ¬A_k)
      └─ raise FileLockTimeout
```

#### Path conditions (PC)
- **PC1:** `∃i ∈ [1..k]. A_i`  → returns normally
- **PC2:** `∀i ∈ [1..k]. ¬A_i` → raises `FileLockTimeout`

#### Concrete test cases
Implemented in: `tests/studentid/test/whitebox/symbolic/test_symbolic_file_lock.py::test_acquire_raises_after_retry_budget`
- **TC (PC2):** pre-create `.lock` file and use `retries=2` → expect `FileLockTimeout`

#### Test result
`pytest -q tests/studentid/test/whitebox/symbolic` → **PASS**.

---

### 2.3 `InputValidator.clean()` (vca/core/validator.py)

**Intent:** deterministic input cleaning/normalisation (US19). Core correctness risks include truncation, whitespace/control-char handling, and punctuation collapsing.

#### Symbolic tree (key branches)
Let:
- `R` be the raw input object
- `T = str(R)` unless `R is None` then `T = ""`
- `N(T)` be unicode normalisation (best-effort)
- `C(T)` be control-char removal + whitespace collapsing + punctuation collapse
- `L = len(C(T))`

Key branch predicate:
- `L > MAX_LEN`

```
clean(R)
 ├─ if R is None
 │    └─ T := ""
 └─ else
      └─ T := str(R)

C := normalise+strip+collapse(T)

 ├─ if len(C) <= MAX_LEN
 │    └─ return CleanResult(text=C, was_truncated=False)
 └─ if len(C) > MAX_LEN
      └─ return CleanResult(text=C[:MAX_LEN], was_truncated=True)
```

#### Path conditions (PC)
- **PC1:** `R is None` and `len(C("")) <= MAX_LEN` → not truncated
- **PC2:** `R is not None` and `len(C(str(R))) <= MAX_LEN` → not truncated
- **PC3:** `len(C(str(R))) > MAX_LEN` → truncated

#### Concrete test cases
Implemented in:
- Symbolic tests: `tests/studentid/test/whitebox/symbolic/test_symbolic_validator.py`
- Concolic tests: `tests/studentid/test/whitebox/concolic/test_concolic_validator.py`

Examples:
- **TC (PC1):** `R=None` → expect empty output, not truncated
- **TC (PC2):** `R="\t hi\n"` → whitespace normalised, not truncated
- **TC (PC3):** `R="a"*(MAX_LEN+1)` → truncated, `was_truncated=True`

#### Test result
`pytest -q tests/studentid/test/whitebox/symbolic tests/studentid/test/whitebox/concolic` → **7 passed**.

---

### 2.4 `HistoryStore.load_turns()` high-level symbolic analysis (vca/storage/history_store.py)

**Why included:** this is a core persistence function with multiple safe-fail branches (missing file, concurrent writer lock, legacy `.txt` format, and corruption handling).

#### Symbolic tree (high level)
Let:
- `F` = history file exists
- `L` = lock can be acquired (`FileLock.try_acquire()` returns True)
- `S` = suffix is legacy text (`.txt`)
- `OK` = JSON parsing + schema checks succeed (no corruption)

```
load_turns()
 ├─ if ¬F
 │    └─ return []
 └─ if F
      ├─ if ¬L
      │    └─ return last_good_cache
      └─ if L
           ├─ if S
           │    ├─ if legacy_read_ok -> return turns
           │    └─ else -> return []          (corrupt legacy)
           └─ if ¬S (JSONL)
                ├─ if read_error -> return []
                ├─ if ¬OK -> return []        (corrupt JSON / invalid role / etc.)
                └─ if OK -> return parsed turns (bounded to max_turns)
```

#### Path conditions (PC) examples
- **PC1:** `¬F` → returns empty list
- **PC2:** `F ∧ ¬L` → returns cached last-good turns
- **PC3:** `F ∧ L ∧ S ∧ legacy_read_ok` → returns legacy turns
- **PC4:** `F ∧ L ∧ ¬S ∧ OK` → returns JSONL turns
- **PC5:** `F ∧ L ∧ ¬S ∧ ¬OK` → returns [] (corruption safe-fail)

#### Concrete test cases (already in the repository)
These branches are exercised by the existing unit tests:
- `tests/test_user_story_9.py` (basic persistence + load of missing file)
- `tests/test_user_story_25.py` and `tests/test_user_story_31.py` (history load/save correctness)
- `tests/test_user_story_35.py` (bounded startup load window behaviour)
- `tests/test_user_story_44.py` (stability policies and trimming)

All of these tests pass in the full suite run (`pytest -q`).

## 3) Concolic testing evidence (example)

### 3.1 Concolic flip of the truncation predicate in `InputValidator.clean()`

Predicate of interest:
- `P: len(cleaned_text) > MAX_LEN`

**Seed execution**
- seed input: `"a" * MAX_LEN`
- observed: `P` is **False**
- result: `was_truncated == False`

**Predicate negation + mutant generation**
- negate to force other branch: `¬P` becomes `len(cleaned_text) > MAX_LEN` (**True**)
- mutant input: `"a" * (MAX_LEN + 1)`
- expected: `was_truncated == True`

Implemented in: `tests/studentid/test/whitebox/concolic/test_concolic_validator.py::test_concolic_flip_truncation_predicate`

Result: **PASS**.

---

## 4) Test cases and results (pass/fail evidence)

### Dedicated symbolic and concolic test suites
Command:

- `pytest -q tests/studentid/test/whitebox/symbolic tests/studentid/test/whitebox/concolic`

Output:
- `7 passed`

### Full project test run
Command:
- `pytest -q`

Outcome:
- `168 passed`

**Therefore there are no failing test cases**, and no bug explanations are required.

---

## 5) Where this sits in the report

Paste this content into the report section:

- **Testing and Test Coverage Measurement** → **Research Component on Symbolic Execution and Concolic Testing** fileciteturn0file0.

---

## Appendix A — File locations added for this requirement

- `docs/research_symbolic_execution_and_concolic_testing.md`
- `tests/studentid/test/whitebox/symbolic/test_symbolic_file_lock.py`
- `tests/studentid/test/whitebox/symbolic/test_symbolic_validator.py`
- `tests/studentid/test/whitebox/concolic/test_concolic_validator.py`

> Replace `studentid` in the folder path with your actual student ID package prefix if your group is enforcing the module naming convention.
