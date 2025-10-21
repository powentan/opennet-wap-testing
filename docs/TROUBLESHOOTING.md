# Troubleshooting Guide

## Common Issues and Solutions

### ❌ Error: `pytest: error: unrecognized arguments: --browser=chrome`

**Problem**: You're seeing this error when trying to run tests:
```
pytest: error: unrecognized arguments: --browser=chrome
```

**Root Cause**: This happens when pytest is run from the wrong directory or without using `uv run`.

**Solution**:

1. Make sure you're in the `oppnet-wap-testing` directory:
   ```bash
   cd /path/to/oppnet-wap-testing
   ```

2. Use `uv run` to execute pytest (not just `pytest`):
   ```bash
   # ✅ Correct
   uv run pytest --browser=chrome
   
   # ❌ Wrong (if run from parent directory or without uv)
   pytest --browser=chrome
   ```

**Why this happens**:
- The `--browser` option is defined in `tests/conftest.py`
- Pytest needs to find this file to recognize the option
- Using `uv run` ensures the correct Python environment and working directory

### ✅ Quick Fix Commands

From the project root (WAP directory):
```bash
cd oppnet-wap-testing && uv run pytest --browser=chrome
```

Or navigate first:
```bash
cd oppnet-wap-testing
uv run pytest --browser=chrome
```

### 📋 Common Command Patterns

```bash
# Basic test run
uv run pytest

# With specific browser
uv run pytest --browser=chrome
uv run pytest --browser=safari

# With device emulation
uv run pytest --browser=chrome --device="iPhone SE"

# Headless mode
uv run pytest --headless

# Run specific tests
uv run pytest tests/test_cases/test_mobile_example.py
uv run pytest -m smoke
```

### 🔍 Verify Setup

Test that everything is configured correctly:
```bash
# Check that pytest recognizes custom options
uv run pytest --help | grep -A2 "browser"

# Collect tests without running
uv run pytest --collect-only

# Run one simple test
uv run pytest tests/test_cases/test_framework.py::test_framework_setup -v
```

### 🐛 Still Having Issues?

1. **Check you're in the right directory**:
   ```bash
   pwd  # Should show: .../oppnet-wap-testing
   ls   # Should show: tests/, config/, drivers/, etc.
   ```

2. **Verify virtual environment**:
   ```bash
   uv sync  # Re-sync dependencies
   ```

3. **Check Python version**:
   ```bash
   python --version  # Should be 3.10 or higher
   ```

4. **Verify pytest installation**:
   ```bash
   uv run pytest --version
   ```

### 📖 Related Documentation

- See `README.md` for full usage instructions
- See `GETTING_STARTED.md` for step-by-step setup
- See parent directory's `README.md` for quick start commands

---

**Remember**: Always run pytest from the `oppnet-wap-testing` directory using `uv run pytest`! 🚀
