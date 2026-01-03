# How to Run Tests - Quick Guide

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

## Step 3: Run Tests

Once you're in the project root (`CO3095-Virtual-Chat-Assistant/`), you can run:

### Run All Tests
```bash
python -m pytest
```

### Run Tests for Specific Student
```bash
python -m pytest tests/wg73/
python -m pytest tests/sa1068/
python -m pytest tests/jo213/
python -m pytest tests/ma1059/
```

### Run Tests by Type
```bash
# All black-box tests
python -m pytest tests/*/test/blackbox/

# All white-box tests
python -m pytest tests/*/test/whitebox/

# Specific technique
python -m pytest tests/*/test/blackbox/specification_based/
python -m pytest tests/*/test/whitebox/branch_coverage/
```

### Run Symbolic/Concolic Tests
```bash
python -m pytest tests/jo213/test/whitebox/symbolic/
python -m pytest tests/jo213/test/whitebox/concolic/
```

---

## Step 4: Run Tests with Coverage

### Generate Coverage Report (Terminal Output)
```bash
python -m pytest --cov=src --cov-report=term tests/sa1068/ tests/wg73/ tests/jo213/ tests/ma1059/
```

### Generate HTML Coverage Report
```bash
python -m pytest --cov=src --cov-report=html tests/sa1068/ tests/wg73/ tests/jo213/ tests/ma1059/
```

### View HTML Report (after generation)
```bash
# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
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
│   ├── sa1068/
│   ├── jo213/
│   └── ma1059/
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

# Run all tests
python -m pytest

# Run specific student's tests
python -m pytest tests/wg73/

# Run with coverage
python -m pytest --cov=src --cov-report=html
```

---

## Tips

1. **Always check your current directory** with `pwd` before running tests
2. **Use tab completion** - type `tests/` and press Tab to see available directories
3. **Set up a terminal alias** (optional) to quickly navigate:
   ```bash
   # Add to your ~/.zshrc or ~/.bashrc
   alias vca='cd /Users/wafiq/PycharmProjects/CO3095-Virtual-Chat-Assistant'
   
   # Then just type: vca
   ```

---

**Last Updated:** Based on project structure as of current date  
**Total Tests:** 319 tests (all passing)  
**Test Coverage:** 80% overall

