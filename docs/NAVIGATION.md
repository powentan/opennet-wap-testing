# Documentation Navigation Guide

Quick navigation for all framework documentation.

---

## 🚀 Get Started (5 minutes)

**New to the framework?** Start here:

1. **[Main Documentation Index](README.md)** - Overview and quick start
2. **[Getting Started Guide](GETTING_STARTED.md)** - Step-by-step setup
3. Run first test: `cd .. && uv run pytest -m smoke`

---

## 📱 Testing Modes

### Browser Emulation (Fast)
**Best for:** Development, quick testing, CI/CD

**Read:**
- [Main README](README.md#browser-emulation-mode) - Quick overview
- [Getting Started Guide](GETTING_STARTED.md) - Complete setup

**Run:**
```bash
uv run pytest -m smoke
```

---

### Real Emulator/Simulator (Accurate)
**Best for:** Final validation, release testing

**Read:**
1. **[Next Steps](NEXT_STEPS.txt)** ⭐ Quick overview (read first!)
2. **[Emulator Quick Start](EMULATOR_QUICKSTART.md)** - Command reference
3. **[Real Emulator Guide](REAL_EMULATOR_GUIDE.md)** - Complete guide
4. **[Setup Complete](SETUP_COMPLETE.md)** - Post-setup verification

**Run:**
```bash
./run-emulator-tests.sh start
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
```

---

## 📚 All Documentation

### Essential Reading
| File | Size | Purpose | Read When |
|------|------|---------|-----------|
| **[README.md](README.md)** | 15 KB | Complete documentation index | Start here |
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | 9.6 KB | Step-by-step setup guide | Initial setup |
| **[NEXT_STEPS.txt](NEXT_STEPS.txt)** | 7.9 KB | Quick reference card | Quick lookup ⭐ |

### Real Emulator Docs
| File | Size | Purpose | Read When |
|------|------|---------|-----------|
| **[REAL_EMULATOR_GUIDE.md](REAL_EMULATOR_GUIDE.md)** | 9.7 KB | Complete emulator guide | Using real devices |
| **[EMULATOR_QUICKSTART.md](EMULATOR_QUICKSTART.md)** | 7.2 KB | Quick command reference | Command lookup |
| **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** | 9.7 KB | Post-setup verification | After Appium setup |

### Reference
| File | Size | Purpose | Read When |
|------|------|---------|-----------|
| **[OVERVIEW.md](OVERVIEW.md)** | 9.5 KB | Framework architecture | Understanding internals |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | 2.6 KB | Common issues | When stuck |
| **[FRAMEWORK_SUMMARY.txt](FRAMEWORK_SUMMARY.txt)** | 5.1 KB | Quick overview | Quick reference |
| **[CHANGELOG.md](CHANGELOG.md)** | 1.4 KB | Version history | What's new |

---

## 🎯 By Task

### "I want to set up the framework"
1. Read: [README.md](README.md) → [GETTING_STARTED.md](GETTING_STARTED.md)
2. Run: `cd .. && uv sync && uv run pytest -m smoke`

### "I want to use real emulators"
1. Read: [NEXT_STEPS.txt](NEXT_STEPS.txt) → [EMULATOR_QUICKSTART.md](EMULATOR_QUICKSTART.md)
2. Install: `appium driver install xcuitest uiautomator2`
3. Run: `cd .. && ./run-emulator-tests.sh start`

### "I'm stuck with an error"
1. Read: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Check: [REAL_EMULATOR_GUIDE.md](REAL_EMULATOR_GUIDE.md#troubleshooting)
3. Verify: Run `cd .. && ./verify_setup.py`

### "I want to understand the framework"
1. Read: [OVERVIEW.md](OVERVIEW.md)
2. Review: Code in `../pages/` and `../tests/`
3. Check: [FRAMEWORK_SUMMARY.txt](FRAMEWORK_SUMMARY.txt)

### "I need a quick command reference"
1. Read: [NEXT_STEPS.txt](NEXT_STEPS.txt) - Best quick reference!
2. Read: [EMULATOR_QUICKSTART.md](EMULATOR_QUICKSTART.md)
3. Run: `cd .. && ./run-emulator-tests.sh help`

---

## 📖 Reading Path

### Beginner (1 hour)
```
README.md
  ↓
GETTING_STARTED.md
  ↓
Run first test
  ↓
Review examples in ../tests/test_cases/
```

### Intermediate (2 hours)
```
Beginner path
  ↓
OVERVIEW.md
  ↓
Write custom tests
  ↓
TROUBLESHOOTING.md (as needed)
```

### Advanced (3 hours)
```
Intermediate path
  ↓
NEXT_STEPS.txt
  ↓
EMULATOR_QUICKSTART.md
  ↓
REAL_EMULATOR_GUIDE.md
  ↓
SETUP_COMPLETE.md
  ↓
Set up and run real emulators
```

---

## 🔍 Find Information Fast

### Commands
- **Browser tests**: [README.md](README.md#common-commands)
- **Emulator tests**: [EMULATOR_QUICKSTART.md](EMULATOR_QUICKSTART.md#command-reference)
- **All commands**: [NEXT_STEPS.txt](NEXT_STEPS.txt#command-cheat-sheet)

### Configuration
- **Devices**: [README.md](README.md#available-devices)
- **Real devices**: [EMULATOR_QUICKSTART.md](EMULATOR_QUICKSTART.md#available-devices)
- **Options**: [README.md](README.md#command-line-options)

### Examples
- **Test examples**: See `../tests/test_cases/`
- **Page objects**: See `../pages/`
- **Configuration**: See `../config/config.py`

### Troubleshooting
- **Quick fixes**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Emulator issues**: [REAL_EMULATOR_GUIDE.md](REAL_EMULATOR_GUIDE.md#troubleshooting)
- **Verification**: Run `cd .. && ./verify_setup.py`

---

## 📱 Device Lists

### Browser Emulation Devices
See: [README.md](README.md#available-devices)
- iPhone 14 Pro, iPhone SE, iPad Pro
- Samsung Galaxy S21, Pixel 6

### Real Emulators Available
See: [EMULATOR_QUICKSTART.md](EMULATOR_QUICKSTART.md#available-devices)

**iOS Simulators (12):**
- iPhone 16 Pro, iPhone 16 Pro Max, iPhone 16, iPhone 16 Plus
- iPhone SE (3rd generation)
- iPad Pro, iPad Air, iPad mini, iPad (10th gen)

**Android Emulators (3):**
- Medium_Phone_API_35
- Small_Phone_API_35
- my_emulator

---

## ⚡ Quick Links

| What You Need | Go To |
|--------------|-------|
| Get started now | [README.md](README.md) |
| Setup instructions | [GETTING_STARTED.md](GETTING_STARTED.md) |
| Command reference | [NEXT_STEPS.txt](NEXT_STEPS.txt) ⭐ |
| Real emulators | [EMULATOR_QUICKSTART.md](EMULATOR_QUICKSTART.md) |
| Stuck? | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| Deep dive | [REAL_EMULATOR_GUIDE.md](REAL_EMULATOR_GUIDE.md) |
| What's new? | [CHANGELOG.md](CHANGELOG.md) |

---

## 💡 Pro Tips

1. **Start simple**: Use browser emulation first, add real emulators later
2. **Bookmark [NEXT_STEPS.txt](NEXT_STEPS.txt)**: Best quick reference for commands
3. **Use helper scripts**: `./run-emulator-tests.sh` makes life easier
4. **Read in order**: README → Getting Started → Next Steps → Emulator Guide
5. **Keep docs open**: Reference while coding

---

## 🎯 Documentation Stats

- **Total files**: 10
- **Total size**: ~78 KB
- **Total words**: ~30,000
- **Reading time**: ~2 hours for everything
- **Quick start time**: ~5 minutes

---

## 📞 Need Help?

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [README.md](README.md)
3. Run verification: `cd .. && ./verify_setup.py`
4. Check helper: `cd .. && ./run-emulator-tests.sh help`

---

**Happy Testing! 📱🚀**

[Back to Main Documentation](README.md)
