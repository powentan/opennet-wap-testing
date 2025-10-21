# Mobile Test Framework Documentation

Complete documentation for testing mobile web applications with browser emulation and real Android/iOS emulators.

---

## 📚 Table of Contents

### 🚀 Getting Started
- **[Quick Start Guide](#quick-start-guide)** - Get up and running in 5 minutes
- **[Installation](#installation)** - Detailed setup instructions
- **[Your First Test](#your-first-test)** - Run your first test

### 📖 Core Documentation
- **[Framework Overview](OVERVIEW.md)** - Architecture, features, and capabilities
- **[Getting Started Guide](GETTING_STARTED.md)** - Step-by-step setup and usage
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions
- **[Changelog](CHANGELOG.md)** - Version history and updates

### 📱 Real Emulator Testing (New!)
- **[Real Emulator Guide](REAL_EMULATOR_GUIDE.md)** - Complete guide for real device testing
- **[Emulator Quick Start](EMULATOR_QUICKSTART.md)** - Quick reference for emulator commands
- **[Setup Complete](SETUP_COMPLETE.md)** - Post-setup verification and next steps
- **[Next Steps](NEXT_STEPS.txt)** - Quick reference card

### 📋 Reference
- **[Framework Summary](FRAMEWORK_SUMMARY.txt)** - Quick reference

---

## 🚀 Quick Start Guide

### Option 1: Browser Emulation (Fast - Recommended for Development)

```bash
# Navigate to framework
cd oppnet-wap-testing

# Install dependencies (first time only)
uv sync

# Run tests
uv run pytest -m smoke

# View results
open reports/report.html
```

**Use for:** Development, quick testing, CI/CD

---

### Option 2: Real Emulator/Simulator (Accurate - For Final Validation)

**Prerequisites:** Appium must be installed and drivers configured

```bash
# 1. Install Appium drivers (one-time)
appium driver install xcuitest      # iOS
appium driver install uiautomator2  # Android

# 2. Start Appium server
./run-emulator-tests.sh start

# 3. Run tests on iOS Simulator
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"

# 4. Run tests on Android Emulator
./run-emulator-tests.sh test-android Medium_Phone_API_35
```

**Use for:** Final validation, accurate testing, native features

---

## 📖 Installation

### Prerequisites
- Python 3.10 or higher
- uv package manager (included)
- Chrome browser (for Android emulation)
- Safari browser (for iOS emulation, macOS only)
- **Optional:** Appium (for real emulator testing)

### Install Framework

```bash
# Navigate to framework directory
cd oppnet-wap-testing

# Install all dependencies
uv sync

# Verify installation
uv run pytest --version
```

### Optional: Install Appium for Real Emulators

```bash
# Install Appium globally
npm install -g appium

# Install drivers
appium driver install xcuitest
appium driver install uiautomator2

# Verify
appium driver list
```

---

## 🧪 Your First Test

### Test with Browser Emulation

```bash
# Run all tests
uv run pytest

# Run smoke tests only
uv run pytest -m smoke

# Run on specific device (emulated)
uv run pytest --device="iPhone SE" --browser=safari

# Run in headless mode
uv run pytest --headless
```

### Test with Real Emulator

```bash
# Start Appium (in separate terminal)
appium

# Run on iOS Simulator
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=iOS \
    --device="iPhone SE (3rd generation)" \
    -v

# Run on Android Emulator
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=Android \
    --device="Medium_Phone_API_35" \
    -v
```

---

## 📱 Two Testing Modes

### Mode 1: Browser Emulation (Default)

**How it works:**
```
Test → Selenium → Chrome/Safari → Mobile Device Emulation
```

**Characteristics:**
- ⚡ **Fast**: Tests run in seconds
- 🚀 **Easy**: No emulator setup needed
- 🔧 **Simple**: Works on any platform
- ⚠️ **Limitation**: Simulated mobile environment

**When to use:**
- Daily development
- Quick smoke tests
- CI/CD pipelines
- Cross-platform testing

**Command:**
```bash
uv run pytest
```

---

### Mode 2: Real Emulator/Simulator (New!)

**How it works:**
```
Test → Appium → Real Emulator/Simulator → Native Browser
```

**Characteristics:**
- 🎯 **Accurate**: Real device behavior
- 📱 **Native**: Actual iOS/Android environment
- 🔍 **Comprehensive**: Full feature testing
- 🐢 **Slower**: Takes 30-60 seconds to start

**When to use:**
- Final validation
- Release testing
- Native feature testing
- Accurate performance testing

**Command:**
```bash
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
```

---

## 📋 Available Devices

### Browser Emulation Mode

Pre-configured devices:
- **iPhone 14 Pro** (default)
- **iPhone SE**
- **iPad Pro**
- **Samsung Galaxy S21**
- **Pixel 6**

```bash
uv run pytest --device="iPhone SE"
uv run pytest --device="Samsung Galaxy S21"
uv run pytest --device="iPad Pro"
```

### Real Emulator Mode

**Your iOS Simulators (12):**
- iPhone 16 Pro, iPhone 16 Pro Max, iPhone 16, iPhone 16 Plus
- iPhone SE (3rd generation)
- iPad Pro 11-inch (M4), iPad Pro 13-inch (M4)
- iPad Air 11-inch (M2), iPad Air 13-inch (M2)
- iPad mini (A17 Pro)
- iPad (10th generation)

**Your Android Emulators (3):**
- Medium_Phone_API_35
- Small_Phone_API_35
- my_emulator

```bash
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
./run-emulator-tests.sh test-android Medium_Phone_API_35
```

---

## 📝 Common Commands

### Browser Emulation Mode

```bash
# Basic test run
uv run pytest

# Smoke tests
uv run pytest -m smoke

# Specific platform
uv run pytest -m ios
uv run pytest -m android

# Headless mode
uv run pytest --headless

# Specific test file
uv run pytest tests/test_cases/test_mobile_example.py

# Parallel execution
uv run pytest -n auto

# Custom device
uv run pytest --device="iPhone SE" --browser=safari
```

### Real Emulator Mode

```bash
# Using helper script (easiest)
./run-emulator-tests.sh start                          # Start Appium
./run-emulator-tests.sh test-ios "iPhone SE..."        # Test iOS
./run-emulator-tests.sh test-android "Medium_Phone..." # Test Android
./run-emulator-tests.sh devices                        # List devices
./run-emulator-tests.sh stop                           # Stop Appium

# Using pytest directly (more control)
uv run pytest --use-real-device --platform=iOS --device="iPhone SE (3rd generation)"
uv run pytest --use-real-device --platform=Android --device="Medium_Phone_API_35"
uv run pytest -m "emulator and ios" --use-real-device
uv run pytest -m "emulator and android" --use-real-device
```

---

## 🎯 Command-Line Options

### Browser Emulation Options

| Option | Description | Example |
|--------|-------------|---------|
| `--browser` | Browser to use (chrome/safari) | `--browser=safari` |
| `--device` | Device to emulate | `--device="iPhone SE"` |
| `--platform` | Platform (iOS/Android) | `--platform=iOS` |
| `--headless` | Run without visible browser | `--headless` |
| `--base-url` | Base URL for tests | `--base-url=https://example.com` |

### Real Emulator Options

| Option | Description | Example |
|--------|-------------|---------|
| `--use-real-device` | Enable real emulator mode | `--use-real-device` |
| `--platform` | iOS or Android | `--platform=iOS` |
| `--device` | Device/emulator name | `--device="iPhone SE (3rd generation)"` |
| `--appium-server` | Appium server URL | `--appium-server=http://localhost:4723` |

### Test Selection Options

| Option | Description | Example |
|--------|-------------|---------|
| `-m` | Run tests with specific marker | `-m smoke` |
| `-k` | Run tests matching pattern | `-k "test_login"` |
| `-v` | Verbose output | `-v` |
| `-n` | Parallel execution (num workers) | `-n auto` |
| `--collect-only` | Show tests without running | `--collect-only` |

---

## 🏷️ Test Markers

Organize and filter tests using markers:

```python
@pytest.mark.smoke                 # Smoke tests
@pytest.mark.regression           # Regression tests
@pytest.mark.ios                  # iOS-specific tests
@pytest.mark.android              # Android-specific tests
@pytest.mark.chrome               # Chrome browser tests
@pytest.mark.safari               # Safari browser tests
@pytest.mark.emulator             # Real emulator tests
@pytest.mark.browser_emulation    # Browser emulation tests
```

**Usage:**
```bash
uv run pytest -m smoke                    # Run only smoke tests
uv run pytest -m "ios and smoke"         # iOS smoke tests
uv run pytest -m "not slow"              # Skip slow tests
uv run pytest -m "emulator and android"  # Android emulator tests
```

---

## 📊 Test Reports

### HTML Reports

Automatically generated after each test run:

```bash
# Run tests
uv run pytest

# Open report
open reports/report.html
```

Reports include:
- Test results summary
- Test duration
- Screenshots on failures
- System information

### Screenshots

Automatically captured on test failures:
- Location: `reports/screenshots/`
- Naming: `{test_name}_{timestamp}.png`
- Attached to HTML report

---

## 🐛 Troubleshooting

### Common Issues

**Browser Emulation:**
- Chrome/Safari not found → Install browser
- Tests timing out → Increase timeout settings
- Element not found → Check selectors, add explicit waits

**Real Emulator:**
- Appium not starting → Check port 4723, kill existing process
- Simulator won't boot → Use `xcrun simctl boot "device"`
- Emulator not found → Verify device name matches exactly
- Connection refused → Ensure Appium server is running

**See [Troubleshooting Guide](TROUBLESHOOTING.md) for detailed solutions.**

---

## 📚 Documentation Guide

### Start Here

1. **New to the framework?**
   - Read this file (README.md)
   - Follow [Getting Started Guide](GETTING_STARTED.md)
   - Run your first test (see above)

2. **Want to use real emulators?**
   - Read [Next Steps](NEXT_STEPS.txt) for quick overview
   - Read [Emulator Quick Start](EMULATOR_QUICKSTART.md) for commands
   - Read [Real Emulator Guide](REAL_EMULATOR_GUIDE.md) for comprehensive guide

3. **Need help?**
   - Check [Troubleshooting](TROUBLESHOOTING.md)
   - Review [Framework Overview](OVERVIEW.md)

### Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| **README.md** (this file) | Main documentation index | Start here |
| **[OVERVIEW.md](OVERVIEW.md)** | Framework architecture | Understanding internals |
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Step-by-step setup | Initial setup |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Common issues | When stuck |
| **[REAL_EMULATOR_GUIDE.md](REAL_EMULATOR_GUIDE.md)** | Complete emulator guide | Using real devices |
| **[EMULATOR_QUICKSTART.md](EMULATOR_QUICKSTART.md)** | Quick emulator reference | Command lookup |
| **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** | Post-setup guide | After setup |
| **[NEXT_STEPS.txt](NEXT_STEPS.txt)** | Quick reference card | Quick lookup |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history | What's new |
| **[FRAMEWORK_SUMMARY.txt](FRAMEWORK_SUMMARY.txt)** | Quick summary | Quick overview |

---

## 🎓 Learning Path

### Beginner (Browser Emulation)

1. Install framework: `uv sync`
2. Read this README
3. Run first test: `uv run pytest -m smoke`
4. Review test examples in `tests/test_cases/test_mobile_example.py`
5. Write your first test
6. Read [Getting Started Guide](GETTING_STARTED.md)

### Intermediate (Custom Tests)

1. Understand Page Object Model (see `pages/` directory)
2. Create custom page objects
3. Write test suites for your app
4. Use markers to organize tests
5. Configure parallel execution
6. Set up CI/CD integration

### Advanced (Real Emulators)

1. Install Appium: `npm install -g appium`
2. Install drivers: `appium driver install xcuitest uiautomator2`
3. Read [Real Emulator Guide](REAL_EMULATOR_GUIDE.md)
4. Start Appium: `./run-emulator-tests.sh start`
5. Run emulator tests: `./run-emulator-tests.sh test-ios "..."`
6. Optimize test execution
7. Set up emulator farm

---

## 🤝 Best Practices

### Test Development
1. **Start with browser emulation** - Fast iteration during development
2. **Use page objects** - Keep tests maintainable
3. **Add explicit waits** - Avoid flaky tests
4. **Use markers** - Organize test suites
5. **Validate with real emulators** - Before releases

### Test Execution
1. **Smoke tests daily** - Quick validation
2. **Full suite before commits** - Catch regressions
3. **Emulator tests before releases** - Final validation
4. **Parallel execution** - Speed up test runs
5. **Monitor reports** - Track test health

### Emulator Testing
1. **Keep emulators running** - Faster test execution
2. **Use snapshots** - Quick reset to clean state
3. **Start Appium once** - Reuse across test runs
4. **Test on multiple devices** - Ensure compatibility
5. **Clean up after tests** - Reset app state

---

## 🚀 Next Steps

### Immediate Actions

```bash
# 1. Verify setup
cd oppnet-wap-testing
uv run pytest --version

# 2. Run first test (browser emulation)
uv run pytest -m smoke

# 3. View report
open reports/report.html
```

### For Real Emulator Testing

```bash
# 1. Install Appium drivers
appium driver install xcuitest
appium driver install uiautomator2

# 2. Start Appium
./run-emulator-tests.sh start

# 3. Run emulator test
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
```

### Continue Learning

1. Read [Getting Started Guide](GETTING_STARTED.md)
2. Explore test examples in `tests/test_cases/`
3. Review [Framework Overview](OVERVIEW.md)
4. For real emulators: Read [Real Emulator Guide](REAL_EMULATOR_GUIDE.md)

---

## 📖 Additional Resources

### Within Framework
- Test examples: `tests/test_cases/`
- Page objects: `pages/`
- Helper scripts: `*.sh` files
- Configuration: `config/config.py`

### External Links
- [Pytest Documentation](https://docs.pytest.org/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Appium Documentation](https://appium.io/docs/)
- [Page Object Model Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)

---

## ✨ Features Summary

### Browser Emulation Mode
✅ Fast test execution (seconds)  
✅ Pre-configured devices (5 devices)  
✅ Chrome & Safari support  
✅ Headless mode  
✅ Parallel execution  
✅ HTML reports with screenshots  
✅ Page Object Model  
✅ Mobile gestures (swipe, tap)  

### Real Emulator Mode (New!)
✅ Accurate device testing  
✅ 12 iOS simulators ready  
✅ 3 Android emulators ready  
✅ Automatic emulator management  
✅ Native browser testing  
✅ Real touch interactions  
✅ Helper scripts included  
✅ Comprehensive documentation  

---

## 🎉 You're Ready!

You now have access to comprehensive documentation for both browser emulation and real emulator testing.

**Quick links:**
- 🚀 [Getting Started](GETTING_STARTED.md)
- 📱 [Real Emulator Guide](REAL_EMULATOR_GUIDE.md)
- 🐛 [Troubleshooting](TROUBLESHOOTING.md)
- 📋 [Quick Reference](NEXT_STEPS.txt)

**Start testing:**
```bash
cd oppnet-wap-testing
uv run pytest -m smoke
```

---

**Happy Testing! 📱🚀**
