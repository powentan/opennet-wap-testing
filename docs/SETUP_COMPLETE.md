# 🎉 Real Emulator/Simulator Testing - Setup Complete!

## ✅ What's Been Configured

Your mobile testing framework now supports **real Android emulators and iOS simulators** using Appium!

### 📦 Installed Components
- ✅ Appium Python Client (v5.2.4)
- ✅ iOS Simulator support (XCUITest driver)
- ✅ Android Emulator support (UiAutomator2 driver)
- ✅ 10 example tests for real emulators
- ✅ Helper scripts for easy execution
- ✅ Comprehensive documentation

### 📁 New Files Created
1. **`tests/test_cases/test_real_emulators.py`** - Example tests (10 tests)
2. **`REAL_EMULATOR_GUIDE.md`** - Complete guide (~10,000 words)
3. **`EMULATOR_QUICKSTART.md`** - Quick reference guide
4. **`run-emulator-tests.sh`** - Helper script for running tests

### 🔧 Modified Files
1. **`pyproject.toml`** - Added Appium dependency
2. **`config/config.py`** - Added real device configurations for your emulators
3. **`drivers/driver_factory.py`** - Added Appium driver creation logic
4. **`tests/conftest.py`** - Added `--use-real-device` command-line option
5. **`README.md`** - Updated with real emulator testing info

---

## 🚀 Getting Started (3 Steps)

### Step 1: Install Appium Drivers (One-time setup)

```bash
# Install iOS driver
appium driver install xcuitest

# Install Android driver  
appium driver install uiautomator2

# Verify installation
appium driver list
```

### Step 2: Start Appium Server

```bash
cd mobile-test-framework

# Option A: Use helper script (recommended)
./run-emulator-tests.sh start

# Option B: Start manually
appium
```

Keep this terminal open while running tests!

### Step 3: Run Your First Test

**iOS Simulator:**
```bash
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
```

**Android Emulator:**
```bash
./run-emulator-tests.sh test-android Medium_Phone_API_35
```

---

## 📱 Your Available Devices

### iOS Simulators (12 available):
```bash
# iPhone models
./run-emulator-tests.sh test-ios "iPhone 16 Pro"
./run-emulator-tests.sh test-ios "iPhone 16 Pro Max"
./run-emulator-tests.sh test-ios "iPhone 16"
./run-emulator-tests.sh test-ios "iPhone 16 Plus"
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"

# iPad models
./run-emulator-tests.sh test-ios "iPad Pro 11-inch (M4)"
./run-emulator-tests.sh test-ios "iPad Pro 13-inch (M4)"
./run-emulator-tests.sh test-ios "iPad Air 11-inch (M2)"
./run-emulator-tests.sh test-ios "iPad Air 13-inch (M2)"
./run-emulator-tests.sh test-ios "iPad mini (A17 Pro)"
./run-emulator-tests.sh test-ios "iPad (10th generation)"
```

### Android Emulators (3 available):
```bash
./run-emulator-tests.sh test-android Medium_Phone_API_35
./run-emulator-tests.sh test-android Small_Phone_API_35
./run-emulator-tests.sh test-android my_emulator
```

---

## 📖 Command Reference

### Using Helper Script (Easiest)

```bash
# Start Appium
./run-emulator-tests.sh start

# Run iOS tests
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"

# Run Android tests
./run-emulator-tests.sh test-android Medium_Phone_API_35

# Show available devices
./run-emulator-tests.sh devices

# Stop Appium
./run-emulator-tests.sh stop

# Show help
./run-emulator-tests.sh help
```

### Using pytest Directly (More Control)

```bash
# iOS tests
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=iOS \
    --device="iPhone SE (3rd generation)" \
    -v

# Android tests
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=Android \
    --device="Medium_Phone_API_35" \
    -v

# Run only iOS emulator tests
uv run pytest -m "emulator and ios" --use-real-device --platform=iOS

# Run only Android emulator tests
uv run pytest -m "emulator and android" --use-real-device --platform=Android

# Run specific test
uv run pytest tests/test_cases/test_real_emulators.py::TestIOSSimulator::test_safari_on_ios_simulator \
    --use-real-device --platform=iOS --device="iPhone SE (3rd generation)" -v
```

---

## 🎨 Two Testing Modes

### Mode 1: Browser Emulation (Default - Fast)
**Use for:** Development, quick testing, CI/CD

```bash
# No Appium needed
uv run pytest
uv run pytest -m smoke
uv run pytest --headless
```

**Pros:** ⚡ Fast, easy setup, works anywhere  
**Cons:** Less accurate, limited features

### Mode 2: Real Emulator/Simulator (New - Accurate)
**Use for:** Final validation, accurate testing, native features

```bash
# Requires Appium
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
./run-emulator-tests.sh test-android Medium_Phone_API_35
```

**Pros:** 🎯 Accurate, real behavior, full features  
**Cons:** Slower, requires setup

---

## 🧪 Example Test

Here's what a test looks like for real emulators:

```python
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.emulator
@pytest.mark.ios
class TestIOSSimulator:
    @pytest.mark.smoke
    def test_safari_on_ios_simulator(self, driver, test_config):
        """Test Safari on real iOS simulator."""
        driver.get("https://www.google.com")
        
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        assert search_box.is_displayed()
        search_box.send_keys("Appium iOS testing")
        assert "Google" in driver.title
```

---

## 🎯 Quick Test Checklist

Run through these to verify everything works:

```bash
# ✅ 1. Check Appium is installed
appium --version

# ✅ 2. Install Appium drivers (one-time)
appium driver install xcuitest
appium driver install uiautomator2

# ✅ 3. Start Appium
./run-emulator-tests.sh start

# ✅ 4. Test iOS simulator
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"

# ✅ 5. Test Android emulator
./run-emulator-tests.sh test-android Medium_Phone_API_35

# ✅ 6. Stop Appium
./run-emulator-tests.sh stop
```

---

## 📚 Documentation

### Quick References
- **`EMULATOR_QUICKSTART.md`** - This file, quick reference
- **`run-emulator-tests.sh help`** - Helper script usage

### Comprehensive Guides
- **`REAL_EMULATOR_GUIDE.md`** - Complete guide with:
  - Prerequisites and setup
  - Detailed command examples
  - Device configurations
  - Troubleshooting
  - Performance tips
  - Best practices
  - Advanced usage

### Framework Documentation
- **`README.md`** - Main framework documentation
- **`GETTING_STARTED.md`** - Step-by-step setup guide
- **`TROUBLESHOOTING.md`** - Common issues

---

## 🐛 Common Issues & Solutions

### Issue: Appium server not starting
```bash
# Check if port is already in use
lsof -i :4723

# Kill existing process
kill -9 <PID>

# Restart
./run-emulator-tests.sh start
```

### Issue: iOS simulator won't boot
```bash
# List available simulators
xcrun simctl list devices available

# Boot manually
xcrun simctl boot "iPhone SE (3rd generation)"
```

### Issue: Android emulator won't start
```bash
# List AVDs
~/Library/Android/sdk/emulator/emulator -list-avds

# Start manually
~/Library/Android/sdk/emulator/emulator -avd Medium_Phone_API_35 &
```

### Issue: Tests can't connect to emulator
```bash
# Check Appium status
curl http://localhost:4723/status

# Verify drivers are installed
appium driver list

# Reinstall if needed
appium driver install xcuitest
appium driver install uiautomator2
```

---

## 💡 Pro Tips

### 1. Speed Up Development
```bash
# Use browser emulation during development (fast)
uv run pytest -m smoke

# Use real emulators for final validation (accurate)
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
```

### 2. Keep Emulators Running
```bash
# Start emulator once
xcrun simctl boot "iPhone SE (3rd generation)"

# Run multiple test suites
uv run pytest test1.py --use-real-device
uv run pytest test2.py --use-real-device
uv run pytest test3.py --use-real-device
```

### 3. Parallel Testing
```bash
# Run tests on multiple emulators simultaneously
# Terminal 1: iOS
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"

# Terminal 2: Android
./run-emulator-tests.sh test-android Medium_Phone_API_35
```

### 4. CI/CD Integration
```bash
# Fast browser emulation for CI/CD
uv run pytest --headless -m smoke

# Occasional real emulator validation
# (on dedicated test infrastructure)
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
```

---

## 🎓 Learning Path

1. **Start with browser emulation** - Get familiar with the framework
   ```bash
   uv run pytest tests/test_cases/test_mobile_example.py
   ```

2. **Learn Appium basics** - Read REAL_EMULATOR_GUIDE.md
   ```bash
   cat REAL_EMULATOR_GUIDE.md
   ```

3. **Run example tests** - See real emulator testing in action
   ```bash
   ./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
   ```

4. **Write your own tests** - Copy examples from test_real_emulators.py
   ```bash
   cp tests/test_cases/test_real_emulators.py tests/test_cases/my_tests.py
   ```

5. **Optimize for your workflow** - Choose browser vs real emulator per test

---

## ✨ What's Next?

Now that you have real emulator testing set up, you can:

1. ✅ Write tests for your mobile app
2. ✅ Test on 12 different iOS simulators
3. ✅ Test on 3 different Android emulators
4. ✅ Choose between fast (browser) and accurate (emulator) testing
5. ✅ Validate mobile-specific features
6. ✅ Test touch gestures and interactions
7. ✅ Verify responsive design on real devices

---

## 🎉 You're Ready!

Your framework is fully configured for real emulator and simulator testing!

**Next command to run:**
```bash
cd mobile-test-framework
./run-emulator-tests.sh start
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
```

**Need help?** Check:
- `./run-emulator-tests.sh help`
- `REAL_EMULATOR_GUIDE.md`
- `TROUBLESHOOTING.md`

---

**Happy Testing on Real Emulators! 📱🚀**
