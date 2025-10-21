# Real Emulator/Simulator Testing - Quick Reference

## 🎯 What Changed

The framework now supports **TWO testing modes**:

| Mode | Description | Use Case | Speed |
|------|-------------|----------|-------|
| **Browser Emulation** | Chrome/Safari with mobile device emulation | Quick development, CI/CD | ⚡ Fast |
| **Real Emulator/Simulator** | Actual Android/iOS emulators via Appium | Accurate testing, final validation | 🐢 Slower |

## 🚀 Quick Start

### 1. Start Appium Server (Required for Real Emulators)

```bash
cd mobile-test-framework

# Option 1: Use helper script
./run-emulator-tests.sh start

# Option 2: Start manually
appium
```

### 2. Run Tests on iOS Simulator

```bash
# Quick way
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"

# Or with pytest
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=iOS \
    --device="iPhone SE (3rd generation)" \
    -v
```

### 3. Run Tests on Android Emulator

```bash
# Quick way
./run-emulator-tests.sh test-android Medium_Phone_API_35

# Or with pytest
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=Android \
    --device="Medium_Phone_API_35" \
    -v
```

## 📱 Available Devices

### Your iOS Simulators (12 devices available):
- ✅ iPhone 16 Pro
- ✅ iPhone 16 Pro Max  
- ✅ iPhone 16
- ✅ iPhone 16 Plus
- ✅ iPhone SE (3rd generation)
- ✅ iPad Pro 11-inch (M4)
- ✅ iPad Pro 13-inch (M4)
- ✅ iPad Air 11-inch (M2)
- ✅ iPad Air 13-inch (M2)
- ✅ iPad mini (A17 Pro)
- ✅ iPad (10th generation)

### Your Android Emulators (3 AVDs available):
- ✅ Medium_Phone_API_35
- ✅ Small_Phone_API_35
- ✅ my_emulator

## 📝 Command Examples

### Browser Emulation Mode (Default - No Appium needed)
```bash
# Fast, for development
uv run pytest
uv run pytest -m smoke
uv run pytest tests/test_cases/test_mobile_example.py
```

### Real Emulator Mode (Appium required)
```bash
# iOS
uv run pytest -m "emulator and ios" --use-real-device --platform=iOS
uv run pytest --use-real-device --platform=iOS --device="iPhone 16 Pro"

# Android
uv run pytest -m "emulator and android" --use-real-device --platform=Android  
uv run pytest --use-real-device --platform=Android --device="my_emulator"

# Specific test
uv run pytest tests/test_cases/test_real_emulators.py::TestIOSSimulator::test_safari_on_ios_simulator \
    --use-real-device --platform=iOS --device="iPhone SE (3rd generation)"
```

### Using Helper Script
```bash
# Start Appium
./run-emulator-tests.sh start

# Run iOS tests
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
./run-emulator-tests.sh test-ios "iPhone 16 Pro"
./run-emulator-tests.sh test-ios "iPad Pro 11-inch (M4)"

# Run Android tests
./run-emulator-tests.sh test-android Medium_Phone_API_35
./run-emulator-tests.sh test-android Small_Phone_API_35
./run-emulator-tests.sh test-android my_emulator

# Show available devices
./run-emulator-tests.sh devices

# Stop Appium
./run-emulator-tests.sh stop
```

## 🔧 New Files Added

1. **`tests/test_cases/test_real_emulators.py`** - Example tests for real emulators
2. **`REAL_EMULATOR_GUIDE.md`** - Comprehensive guide (9,900+ words)
3. **`run-emulator-tests.sh`** - Helper script for easy execution

## 🎨 Updated Files

1. **`pyproject.toml`** - Added `appium-python-client` dependency
2. **`config/config.py`** - Added real device configurations
3. **`drivers/driver_factory.py`** - Added Appium driver support
4. **`tests/conftest.py`** - Added `--use-real-device` option
5. **`README.md`** - Added real emulator testing section

## 💡 How It Works

### Browser Emulation Mode (Original)
```
Test → Selenium → Chrome/Safari → Mobile Device Emulation
```
- **Pros**: Fast, no emulator needed, works anywhere
- **Cons**: Less accurate, limited native features

### Real Emulator Mode (New)
```
Test → Appium → Emulator/Simulator → Real Browser (Safari/Chrome)
```
- **Pros**: Accurate, real device behavior, full features
- **Cons**: Slower, requires Appium, more setup

## 🔑 Key Command-Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--use-real-device` | Enable real emulator mode | `--use-real-device` |
| `--platform` | iOS or Android | `--platform=iOS` |
| `--device` | Device/emulator name | `--device="iPhone SE (3rd generation)"` |
| `--appium-server` | Appium server URL | `--appium-server=http://localhost:4723` |
| `-m emulator` | Run only emulator tests | `-m emulator` |
| `-v` | Verbose output | `-v` |

## 📊 Test Markers

New markers for organizing tests:

```python
@pytest.mark.emulator              # For emulator/simulator tests
@pytest.mark.browser_emulation     # For browser emulation tests
@pytest.mark.ios                   # iOS-specific tests
@pytest.mark.android               # Android-specific tests
@pytest.mark.smoke                 # Smoke tests
```

## 🐛 Troubleshooting

### Appium not starting?
```bash
# Check if port is in use
lsof -i :4723

# Kill process if needed
kill -9 <PID>

# Restart Appium
appium
```

### iOS Simulator not booting?
```bash
# List simulators
xcrun simctl list devices available

# Boot manually
xcrun simctl boot "iPhone SE (3rd generation)"
```

### Android Emulator not starting?
```bash
# List AVDs
~/Library/Android/sdk/emulator/emulator -list-avds

# Start manually
~/Library/Android/sdk/emulator/emulator -avd Medium_Phone_API_35
```

### Tests failing on emulators?
```bash
# Check Appium status
curl http://localhost:4723/status

# Check Appium drivers
appium driver list

# Install drivers if missing
appium driver install xcuitest
appium driver install uiautomator2
```

## 📖 Documentation

- **`REAL_EMULATOR_GUIDE.md`** - Complete guide with examples, troubleshooting, best practices
- **`README.md`** - Updated with real emulator testing section
- **`TROUBLESHOOTING.md`** - Common issues and solutions

## ✅ Verification

Test your setup:

```bash
# 1. Check Appium is installed
appium --version

# 2. Start Appium
./run-emulator-tests.sh start

# 3. Run a simple iOS test
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"

# 4. Run a simple Android test
./run-emulator-tests.sh test-android Medium_Phone_API_35

# 5. Stop Appium
./run-emulator-tests.sh stop
```

## 🎯 Best Practices

1. **Development**: Use browser emulation (fast)
   ```bash
   uv run pytest -m smoke
   ```

2. **Pre-commit**: Use browser emulation (CI/CD friendly)
   ```bash
   uv run pytest --headless
   ```

3. **Final Validation**: Use real emulators (accurate)
   ```bash
   ./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
   ./run-emulator-tests.sh test-android Medium_Phone_API_35
   ```

4. **Debugging**: Use real emulators with visible UI
   ```bash
   # Start emulator first (visible)
   xcrun simctl boot "iPhone SE (3rd generation)"
   # Then run tests
   uv run pytest --use-real-device --platform=iOS -v
   ```

## 🚀 Next Steps

1. ✅ Install Appium drivers:
   ```bash
   appium driver install xcuitest
   appium driver install uiautomator2
   ```

2. ✅ Start Appium:
   ```bash
   ./run-emulator-tests.sh start
   ```

3. ✅ Run your first test:
   ```bash
   ./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
   ```

4. ✅ Read the comprehensive guide:
   ```bash
   cat REAL_EMULATOR_GUIDE.md
   ```

---

**Ready to test on real emulators! 📱🚀**
