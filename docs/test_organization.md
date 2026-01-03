# Test Organization Documentation

## Team Member Information

| Team Member | Name | Student ID | GitHub Username |
|-------------|------|------------|-----------------|
| 1 | Wafiq Gborigi | wg73 | WafiqGb |
| 2 | Sultan Adekoya | sa1068 | SultanUOL |
| 3 | John Onwuemezia | Jo213 | JO213-LE |
| 4 | Ayomide Adebanjo | Ma1059 | michael-ay0 |

---

## Test Folder Structure

The tests are organized according to the assignment requirements using the naming convention:
- `studentid.test.blackbox.which_technique`
- `studentid.test.whitebox.which_technique`

### Complete Structure

```
tests/
  sa1068/                         # Sultan Adekoya
    test/
      blackbox/
        specification_based/
          test_user_story_*.py
        random_based/
          test_user_story_*.py
      whitebox/
        statement_coverage/
          test_user_story_*.py
        branch_coverage/
          test_user_story_*.py
        path_coverage/
          test_user_story_*.py
  
  wg73/                           # Wafiq Gborigi
    test/
      blackbox/
        specification_based/
          test_user_story_*.py
        random_based/
          test_user_story_*.py
      whitebox/
        statement_coverage/
          test_user_story_*.py
        branch_coverage/
          test_user_story_*.py
        path_coverage/
          test_user_story_*.py
  
  jo213/                          # John Onwuemezia
    test/
      docs/
        research_symbolic_execution_and_concolic_testing.md
      blackbox/
        specification_based/
          test_user_story_*.py
        random_based/
          test_user_story_*.py
      whitebox/
        statement_coverage/
          test_user_story_*.py
        branch_coverage/
          test_user_story_*.py
        path_coverage/
          test_user_story_*.py
        symbolic/
          test_symbolic_file_lock.py
          test_symbolic_validator.py
        concolic/
          test_concolic_validator.py
  
  ma1059/                         # Ayomide Adebanjo
    test/
      blackbox/
        specification_based/
          test_user_story_*.py
        random_based/
          test_user_story_*.py
      whitebox/
        statement_coverage/
          test_user_story_*.py
        branch_coverage/
          test_user_story_*.py
        path_coverage/
          test_user_story_*.py
```

---

## User Story to Test File Mapping

### Wafiq Gborigi (wg73) - User Stories: US5-US8, US21-US24, US37-US40

**Test Files Organized By Technique:**

#### Black-Box Tests
- **Specification-Based:**
  - `wg73/test/blackbox/specification_based/test_user_story_37.py`
  - `wg73/test/blackbox/specification_based/test_user_story_38.py`
  - `wg73/test/blackbox/specification_based/test_user_story_39.py`
  - `wg73/test/blackbox/specification_based/test_user_story_23.py`

- **Random-Based:**
  - `wg73/test/blackbox/random_based/test_user_story_5.py`
  - `wg73/test/blackbox/random_based/test_user_story_7.py`
  - `wg73/test/blackbox/random_based/test_user_story_8.py`
  - `wg73/test/blackbox/random_based/test_user_story_21.py`
  - `wg73/test/blackbox/random_based/test_user_story_22.py`
  - `wg73/test/blackbox/random_based/test_user_story_23.py`
  - `wg73/test/blackbox/random_based/test_user_story_24.py`
  - `wg73/test/blackbox/random_based/test_user_story_38.py`
  - `wg73/test/blackbox/random_based/test_user_story_40.py`

#### White-Box Tests
- **Statement Coverage:**
  - `wg73/test/whitebox/statement_coverage/test_user_story_6.py`
  - `wg73/test/whitebox/statement_coverage/test_user_story_40.py`

- **Branch Coverage:**
  - `wg73/test/whitebox/branch_coverage/test_user_story_21.py`
  - `wg73/test/whitebox/branch_coverage/test_user_story_23.py`
  - `wg73/test/whitebox/branch_coverage/test_user_story_37.py`
  - `wg73/test/whitebox/branch_coverage/test_user_story_38.py`
  - `wg73/test/whitebox/branch_coverage/test_user_story_39.py`
  - `wg73/test/whitebox/branch_coverage/test_user_story_40.py`

---

### Sultan Adekoya (sa1068) - User Stories: US1-US4, US17-US20, US33-US36

**Test Files Organized By Technique:**

#### Black-Box Tests
- **Random-Based:**
  - `sa1068/test/blackbox/random_based/test_user_story_1.py`
  - `sa1068/test/blackbox/random_based/test_user_story_2.py`
  - `sa1068/test/blackbox/random_based/test_user_story_3.py`
  - `sa1068/test/blackbox/random_based/test_user_story_17.py`
  - `sa1068/test/blackbox/random_based/test_user_story_18.py`
  - `sa1068/test/blackbox/random_based/test_user_story_19.py`
  - `sa1068/test/blackbox/random_based/test_user_story_20.py`
  - `sa1068/test/blackbox/random_based/test_user_story_34.py`
  - `sa1068/test/blackbox/random_based/test_user_story_36.py`

#### White-Box Tests
- **Statement Coverage:**
  - `sa1068/test/whitebox/statement_coverage/test_user_story_20.py`
  - `sa1068/test/whitebox/statement_coverage/test_user_story_34.py`
  - `sa1068/test/whitebox/statement_coverage/test_user_story_35.py`
  - `sa1068/test/whitebox/statement_coverage/test_user_story_36.py`

- **Branch Coverage:**
  - `sa1068/test/whitebox/branch_coverage/test_user_story_35.py`

- **Path Coverage:**
  - `sa1068/test/whitebox/path_coverage/test_user_story_4.py`
  - `sa1068/test/whitebox/path_coverage/test_user_story_33.py`
  - `sa1068/test/whitebox/path_coverage/test_user_story_34.py`

---

### John Onwuemezia (Jo213) - User Stories: US9-US12, US25-US28, US41-US44

**Test Files Organized By Technique:**

#### Black-Box Tests
- **Specification-Based:**
  - `jo213/test/blackbox/specification_based/test_user_story_25.py`
  - `jo213/test/blackbox/specification_based/test_user_story_26.py`
  - `jo213/test/blackbox/specification_based/test_user_story_27.py`
  - `jo213/test/blackbox/specification_based/test_user_story_28.py`
  - `jo213/test/blackbox/specification_based/test_user_story_41.py`
  - `jo213/test/blackbox/specification_based/test_user_story_42.py`
  - `jo213/test/blackbox/specification_based/test_user_story_44.py`

- **Random-Based:**
  - `jo213/test/blackbox/random_based/test_user_story_9.py`
  - `jo213/test/blackbox/random_based/test_user_story_10.py`
  - `jo213/test/blackbox/random_based/test_user_story_11.py`
  - `jo213/test/blackbox/random_based/test_user_story_12.py`

#### White-Box Tests
- **Statement Coverage:**
  - `jo213/test/whitebox/statement_coverage/test_user_story_41.py`
  - `jo213/test/whitebox/statement_coverage/test_user_story_43.py`
  - `jo213/test/whitebox/statement_coverage/test_user_story_44.py`

- **Symbolic Execution:**
  - `jo213/test/whitebox/symbolic/test_symbolic_file_lock.py`
  - `jo213/test/whitebox/symbolic/test_symbolic_validator.py`
  - `jo213/test/whitebox/symbolic/test_symbolic_intent_classifier.py`
  - `jo213/test/whitebox/symbolic/test_symbolic_engine_process_turn.py`
  - `jo213/test/whitebox/symbolic/test_symbolic_chat_engine.py`
  - `jo213/test/whitebox/symbolic/test_symbolic_response_generator.py`
  - `jo213/test/whitebox/symbolic/test_symbolic_history_store.py`
  - `jo213/test/whitebox/symbolic/test_symbolic_session.py`
  - `jo213/test/whitebox/symbolic/test_symbolic_commands.py`

- **Concolic Testing:**
  - `jo213/test/whitebox/concolic/test_concolic_validator.py`
  - `jo213/test/whitebox/concolic/test_concolic_intent_classifier.py`
  - `jo213/test/whitebox/concolic/test_concolic_engine_process_turn.py`
  - `jo213/test/whitebox/concolic/test_concolic_chat_engine.py`
  - `jo213/test/whitebox/concolic/test_concolic_response_generator.py`
  - `jo213/test/whitebox/concolic/test_concolic_history_store.py`
  - `jo213/test/whitebox/concolic/test_concolic_session.py`
  - `jo213/test/whitebox/concolic/test_concolic_commands.py`

---

### Ayomide Adebanjo (Ma1059) - User Stories: US13-US16, US29-US32, US45-US48

**Test Files Organized By Technique:**

#### Black-Box Tests
- **Specification-Based:**
  - `ma1059/test/blackbox/specification_based/test_user_story_13.py`
  - `ma1059/test/blackbox/specification_based/test_user_story_29.py`
  - `ma1059/test/blackbox/specification_based/test_user_story_30.py`
  - `ma1059/test/blackbox/specification_based/test_user_story_32.py`
  - `ma1059/test/blackbox/specification_based/test_user_story_48.py`

- **Random-Based:**
  - `ma1059/test/blackbox/random_based/test_user_story_13.py`
  - `ma1059/test/blackbox/random_based/test_user_story_14.py`
  - `ma1059/test/blackbox/random_based/test_user_story_15.py`
  - `ma1059/test/blackbox/random_based/test_user_story_16.py`
  - `ma1059/test/blackbox/random_based/test_user_story_32.py`
  - `ma1059/test/blackbox/random_based/test_user_story_45.py`
  - `ma1059/test/blackbox/random_based/test_user_story_46.py`

#### White-Box Tests
- **Statement Coverage:**
  - `ma1059/test/whitebox/statement_coverage/test_user_story_29.py`
  - `ma1059/test/whitebox/statement_coverage/test_user_story_31.py`
  - `ma1059/test/whitebox/statement_coverage/test_user_story_47.py`

---

## Testing Techniques Classification

### Black-Box Testing Techniques

#### Specification-Based Testing
- Tests that validate functionality against specifications
- Tests using external datasets (JSON files)
- Tests with expected outcomes defined in data files
- Examples:
  - `test_user_story_37.py` - Uses `us37_phrases.json` dataset
  - `test_user_story_38.py` - Uses `us38_synonyms.json` dataset
  - `test_user_story_39.py` - Uses `us39_false_positives.json` dataset
  - `test_user_story_25.py` - Tests JSONL format specifications

#### Random-Based Testing
- Tests with varied inputs
- Boundary value testing
- Equivalence partitioning
- Tests exploring different input scenarios
- Examples:
  - `test_user_story_1.py` - Tests empty, unicode, long text inputs
  - `test_user_story_5.py` - Tests various classifier inputs
  - `test_user_story_21.py` - Tests multiple intent classifications

### White-Box Testing Techniques

#### Statement Coverage
- Tests that execute all statements in the code
- Basic functional tests ensuring code paths are executed
- Examples:
  - `test_user_story_6.py` - Tests validator functions
  - `test_user_story_40.py` - Tests handler routing

#### Branch Coverage
- Tests that check specific branches and decision points
- Tests using internal methods (`classify_result`, `route`)
- Tests checking conditional logic
- Examples:
  - `test_user_story_21.py` - Tests routing handlers for each intent
  - `test_user_story_37.py` - Tests rule selection and priority
  - `test_user_story_39.py` - Tests partial match prevention

#### Path Coverage
- Tests covering multiple execution paths
- Tests using mocking and stage interception
- Complex integration tests
- Examples:
  - `test_user_story_33.py` - Tests process_turn orchestration stages
  - `test_user_story_4.py` - Tests validation paths

#### Symbolic Execution
- Located in: `jo213/test/whitebox/symbolic/`
- Tests analyzing symbolic execution paths
- Files (9 total):
  - `test_symbolic_file_lock.py`
  - `test_symbolic_validator.py`
  - `test_symbolic_intent_classifier.py`
  - `test_symbolic_engine_process_turn.py`
  - `test_symbolic_chat_engine.py`
  - `test_symbolic_response_generator.py`
  - `test_symbolic_history_store.py`
  - `test_symbolic_session.py`
  - `test_symbolic_commands.py`

#### Concolic Testing
- Located in: `jo213/test/whitebox/concolic/`
- Tests combining concrete and symbolic execution
- Files (8 total):
  - `test_concolic_validator.py`
  - `test_concolic_intent_classifier.py`
  - `test_concolic_engine_process_turn.py`
  - `test_concolic_chat_engine.py`
  - `test_concolic_response_generator.py`
  - `test_concolic_history_store.py`
  - `test_concolic_session.py`
  - `test_concolic_commands.py`

---

## Research Component Test Organization

### Symbolic Execution and Concolic Testing

**Location:** `tests/jo213/test/`

**Structure:**
- **Documentation:** `docs/research_symbolic_execution_and_concolic_testing.md`
- **Symbolic Tests:** `whitebox/symbolic/` (9 test files)
  - `test_symbolic_file_lock.py`
  - `test_symbolic_validator.py`
  - `test_symbolic_intent_classifier.py`
  - `test_symbolic_engine_process_turn.py`
  - `test_symbolic_chat_engine.py`
  - `test_symbolic_response_generator.py`
  - `test_symbolic_history_store.py`
  - `test_symbolic_session.py`
  - `test_symbolic_commands.py`
- **Concolic Tests:** `whitebox/concolic/` (8 test files)
  - `test_concolic_validator.py`
  - `test_concolic_intent_classifier.py`
  - `test_concolic_engine_process_turn.py`
  - `test_concolic_chat_engine.py`
  - `test_concolic_response_generator.py`
  - `test_concolic_history_store.py`
  - `test_concolic_session.py`
  - `test_concolic_commands.py`

**Note:** These tests demonstrate symbolic execution and concolic testing methodologies applied to 23 functions across the codebase. Total of 110+ new symbolic/concolic tests covering functions with varying complexity levels.

---

## Test Coverage Summary

### Current Test Coverage Status

- **Total Test Files:** 48 user story test files (organized) + symbolic/concolic tests
- **Total Tests:** 319 tests (all passing)
  - 163 original user story tests
  - 110 new symbolic/concolic tests (added for 18 additional functions)
  - 46 existing symbolic/concolic tests (original 5 functions)
- **Coverage:** Comprehensive coverage across all modules

### Coverage by Module

- **Core Engine:** Comprehensive coverage
- **Intent Classification:** Comprehensive coverage (black-box and white-box)
- **Response Generation:** Comprehensive coverage
- **Storage:** Comprehensive coverage (including symbolic/concolic)
- **Validation:** Comprehensive coverage (including symbolic/concolic)
- **CLI:** Comprehensive coverage

---

## Naming Convention Compliance

### Assignment Requirement

Tests should follow the naming convention:
- `studentid.test.blackbox.which_technique`
- `studentid.test.whitebox.which_technique`

### Current Status

- ✅ **Folder Structure:** Fully compliant
- ✅ **Test Files:** Organized by student ID, test type, and technique
- ✅ **Naming Convention:** Follows `studentid/test/blackbox|whitebox/technique/` pattern
- ✅ **Research Component:** Properly organized in Jo213 folder

### Organization Details

1. **Student ID Folders:** Created for all team members (sa1068, wg73, jo213, ma1059)
2. **Test Type Separation:** Clear separation between blackbox and whitebox tests
3. **Technique Classification:** Tests organized by specific technique:
   - Black-box: `specification_based`, `random_based`
   - White-box: `statement_coverage`, `branch_coverage`, `path_coverage`, `symbolic`, `concolic`
4. **Mixed Test Files:** Files containing both black-box and white-box tests are split appropriately

---

## Running Tests

**⚠️ Important:** All commands below assume you're in the **project root directory**. If you're in the `docs/` directory, navigate to the project root first:
```bash
cd /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant
```

Alternatively, you can run commands from any directory by using the project root path:
```bash
# From docs/ directory or any other location:
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/wg73/
```

### Run All Tests
```bash
# From project root:
python -m pytest

# Or from any directory:
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/
```

### Run Tests for Specific Student
```bash
# From project root:
python -m pytest tests/wg73/
python -m pytest tests/sa1068/
python -m pytest tests/jo213/
python -m pytest tests/ma1059/

# Or from any directory (using absolute paths):
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/wg73/
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/sa1068/
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/jo213/
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/ma1059/
```

### Run Tests by Type
```bash
# From project root:
# All black-box tests
python -m pytest tests/*/test/blackbox/

# All white-box tests
python -m pytest tests/*/test/whitebox/

# Specific technique
python -m pytest tests/*/test/blackbox/specification_based/
python -m pytest tests/*/test/whitebox/branch_coverage/

# Or from any directory (using absolute paths):
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/*/test/blackbox/
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/*/test/whitebox/
```

### Run Symbolic/Concolic Tests
```bash
# From project root:
python -m pytest tests/jo213/test/whitebox/symbolic/
python -m pytest tests/jo213/test/whitebox/concolic/

# Or from any directory:
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/jo213/test/whitebox/symbolic/
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/jo213/test/whitebox/concolic/
```

### Run Original Test Files (Root Level)
```bash
# From project root:
python -m pytest tests/test_user_story_*.py

# Or from any directory:
python -m pytest /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant/tests/test_user_story_*.py
```

---

## Summary

### Current Organization Status

- ✅ All 48 user story test files organized
- ✅ Tests separated by black-box and white-box
- ✅ Tests classified by technique (specification-based, random-based, statement coverage, branch coverage, path coverage)
- ✅ Symbolic/concolic tests properly organized (Jo213 folder)
- ✅ Research documentation present
- ✅ Folder structure follows assignment naming convention
- ✅ All tests passing (319 tests: 163 original + 110 new symbolic/concolic + 46 existing symbolic/concolic)

### Key Features

1. **Complete Organization:** All tests organized by student ID, test type, and technique
2. **Mixed Files Split:** Files with both black-box and white-box tests are properly split
3. **Technique Classification:** Tests accurately classified based on code analysis
4. **Research Component:** Symbolic execution and concolic testing properly documented and organized
5. **Backward Compatibility:** Original test files remain in `tests/` root for compatibility

### Compliance Status

- **Test Files:** ✅ Fully compliant
- **Naming Convention:** ✅ Fully compliant (`studentid.test.blackbox.technique` / `studentid.test.whitebox.technique`)
- **Coverage:** ✅ Comprehensive
- **Research Component:** ✅ Well organized and documented
- **Organization:** ✅ Complete and properly structured

---

## Notes

- Tests are organized according to assignment requirements
- Original test files in `tests/` root are maintained for backward compatibility
- Mixed test files (containing both black-box and white-box tests) have been split appropriately
- Test classification is based on code analysis and function naming patterns
- All tests continue to pass after organization
- Research component (symbolic/concolic) is properly organized in Jo213 folder
