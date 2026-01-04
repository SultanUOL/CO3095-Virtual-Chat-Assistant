# How to Run Tests - Complete Guide
## CO3095 Virtual Chat Assistant

This guide explains how to navigate to the correct directory and run all tests for the project.

---

## ⚠️ Important: Directory Location

**All test commands must be run from the project root directory**, not from subdirectories like `docs/`.

---

## Step 1: Navigate to Project Root

### If you're currently in the `docs/` directory:

```bash
# Go up one level to project root
cd ..
```

### If you're in any other subdirectory:

```bash
# Navigate to project root using absolute path
cd /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant
```

### If you're not sure where you are:

```bash
# Check current directory
pwd

# You should see:
# /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant
```

---

## Step 2: Verify You're in the Right Place

After navigating, verify the `tests/` directory exists:

```bash
ls tests/
```

You should see:
- `jo213/`
- `ma1059/`
- `sa1068/`
- `wg73/`
- `conftest.py`
- `helpers.py`

If you see "No such file or directory", you're not in the project root. Go back to Step 1.

---

## Step 3: Activate Virtual Environment

**Important:** Ensure your virtual environment is activated:

```bash
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

---

## Step 4: Run Tests

### Run ALL Tests (319 tests)

```bash
python -m pytest tests/ -v --tb=short
```

Or for a quick summary:
```bash
python -m pytest tests/ --tb=no -q
```

---

## Test Commands by Category

### Black-Box Tests

#### Run All Black-Box Tests
```bash
python -m pytest tests/sa1068/test/blackbox/ tests/ma1059/test/blackbox/ tests/jo213/test/blackbox/ tests/wg73/test/blackbox/ -v
```

#### Specification-Based Tests
```bash
python -m pytest tests/sa1068/test/blackbox/specification_based/ tests/ma1059/test/blackbox/specification_based/ tests/jo213/test/blackbox/specification_based/ tests/wg73/test/blackbox/specification_based/ -v
```

#### Random-Based Tests
```bash
python -m pytest tests/sa1068/test/blackbox/random_based/ tests/ma1059/test/blackbox/random_based/ tests/jo213/test/blackbox/random_based/ tests/wg73/test/blackbox/random_based/ -v
```

---

### White-Box Tests

#### Statement Coverage Tests
```bash
python -m pytest tests/sa1068/test/whitebox/statement_coverage/ tests/ma1059/test/whitebox/statement_coverage/ tests/jo213/test/whitebox/statement_coverage/ tests/wg73/test/whitebox/statement_coverage/ -v
```

#### Branch Coverage Tests
```bash
python -m pytest tests/sa1068/test/whitebox/branch_coverage/ tests/ma1059/test/whitebox/branch_coverage/ tests/jo213/test/whitebox/branch_coverage/ tests/wg73/test/whitebox/branch_coverage/ -v
```

#### Path Coverage Tests
```bash
python -m pytest tests/sa1068/test/whitebox/path_coverage/ tests/ma1059/test/whitebox/path_coverage/ tests/jo213/test/whitebox/path_coverage/ tests/wg73/test/whitebox/path_coverage/ -v
```

---

### Research Component (Symbolic & Concolic)

#### Symbolic Execution Tests

**Individual Team Members:**

```bash
# John Onwuemezia (jo213)
python -m pytest tests/jo213/test/whitebox/symbolic/ -v

# Sultan Adekoya (sa1068)
python -m pytest tests/sa1068/test/whitebox/symbolic/ -v

# Wafiq Gborigi (wg73)
python -m pytest tests/wg73/test/whitebox/symbolic/ -v

# Ayomide Adebanjo (ma1059)
python -m pytest tests/ma1059/test/whitebox/symbolic/ -v
```

**All Team Members Combined:**
```bash
python -m pytest tests/jo213/test/whitebox/symbolic/ tests/sa1068/test/whitebox/symbolic/ tests/wg73/test/whitebox/symbolic/ tests/ma1059/test/whitebox/symbolic/ -v
```

#### Concolic Testing

**Individual Team Members:**

```bash
# John Onwuemezia (jo213)
python -m pytest tests/jo213/test/whitebox/concolic/ -v

# Sultan Adekoya (sa1068)
python -m pytest tests/sa1068/test/whitebox/concolic/ -v

# Wafiq Gborigi (wg73)
python -m pytest tests/wg73/test/whitebox/concolic/ -v

# Ayomide Adebanjo (ma1059)
python -m pytest tests/ma1059/test/whitebox/concolic/ -v
```

**All Team Members Combined:**
```bash
python -m pytest tests/jo213/test/whitebox/concolic/ tests/sa1068/test/whitebox/concolic/ tests/wg73/test/whitebox/concolic/ tests/ma1059/test/whitebox/concolic/ -v
```

#### Symbolic + Concolic Combined

**Individual Team Members:**

```bash
# John Onwuemezia (jo213)
python -m pytest tests/jo213/test/whitebox/symbolic/ tests/jo213/test/whitebox/concolic/ -v

# Sultan Adekoya (sa1068)
python -m pytest tests/sa1068/test/whitebox/symbolic/ tests/sa1068/test/whitebox/concolic/ -v

# Wafiq Gborigi (wg73)
python -m pytest tests/wg73/test/whitebox/symbolic/ tests/wg73/test/whitebox/concolic/ -v

# Ayomide Adebanjo (ma1059)
python -m pytest tests/ma1059/test/whitebox/symbolic/ tests/ma1059/test/whitebox/concolic/ -v
```

**All Team Members Combined:**
```bash
python -m pytest tests/jo213/test/whitebox/symbolic/ tests/jo213/test/whitebox/concolic/ tests/sa1068/test/whitebox/symbolic/ tests/sa1068/test/whitebox/concolic/ tests/wg73/test/whitebox/symbolic/ tests/wg73/test/whitebox/concolic/ tests/ma1059/test/whitebox/symbolic/ tests/ma1059/test/whitebox/concolic/ -v
```

---

## Run Tests by Team Member

### Wafiq (wg73)
```bash
python -m pytest tests/wg73/ -v
```

### Sultan (sa1068)
```bash
python -m pytest tests/sa1068/ -v
```

### John (jo213)
```bash
python -m pytest tests/jo213/ -v
```

### Ayomide (ma1059)
```bash
python -m pytest tests/ma1059/ -v
```

---

## Step 5: Run Tests with Coverage

### Generate Coverage Report (Terminal Output)
```bash
python -m pytest --cov=src --cov-report=term --cov-report=term-missing tests/
```

### Generate HTML Coverage Report
```bash
python -m pytest --cov=src --cov-report=html tests/
```

### View HTML Report (after generation)

**macOS:**
```bash
open htmlcov/index.html
```

**Linux:**
```bash
xdg-open htmlcov/index.html
```

**Windows:**
```bash
start htmlcov/index.html
```

---

## Common Errors and Solutions

### Error: "file or directory not found: tests/..."

**Problem:** You're running the command from the wrong directory (e.g., from `docs/`).

**Solution:**
```bash
# Navigate to project root first
cd /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant

# Then run your test command
python -m pytest tests/wg73/
```

### Error: "cd: no such file or directory: tests"

**Problem:** You're trying to `cd` into `tests/` from `docs/`. The `tests/` directory is a sibling of `docs/`, not a child.

**Solution:**
```bash
# From docs/, go up to project root first
cd ..

# Now you can access tests/
python -m pytest tests/wg73/
```

### Error: "collected 0 items" or "no tests ran"

**Problem:** Pytest can't find the test files because you're in the wrong directory.

**Solution:**
1. Check your current directory: `pwd`
2. If you're not in `/Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant`, navigate there
3. Verify `tests/` directory exists: `ls tests/`
4. Run your test command again

---

## Directory Structure Reference

```
CO3095-Virtual-Chat-Assistant/    ← You MUST be HERE to run tests
├── docs/                         ← If you're here, run: cd ..
├── tests/                        ← Tests are located here
│   ├── wg73/
│   │   └── test/
│   │       ├── blackbox/
│   │       └── whitebox/
│   ├── sa1068/
│   │   └── test/
│   │       ├── blackbox/
│   │       └── whitebox/
│   ├── jo213/
│   │   └── test/
│   │       ├── blackbox/
│   │       └── whitebox/
│   │           ├── symbolic/
│   │           └── concolic/
│   └── ma1059/
│       └── test/
│           ├── blackbox/
│           └── whitebox/
├── src/                          ← Source code
├── README.md
└── requirements.txt
```

---

## Quick Reference Commands

```bash
# Navigate to project root (from anywhere)
cd /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant

# Or from docs/ directory
cd ..

# Verify location
pwd
ls tests/

# Activate virtual environment
source .venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run specific student's tests
python -m pytest tests/wg73/ -v

# Run with coverage
python -m pytest --cov=src --cov-report=html tests/
open htmlcov/index.html
```

---
