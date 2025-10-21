# Real Emulator/Simulator Testing Guide

This guide explains how to run tests on real Android emulators and iOS simulators using Appium.

## 🎯 Overview

The framework now supports two testing modes:

1. **Browser Emulation Mode** (default): Tests run in Chrome/Safari with mobile device emulation
2. **Real Emulator/Simulator Mode**: Tests run on actual Android emulators or iOS simulators using Appium

## 📋 Prerequisites

### For iOS Simulators (macOS only):
- ✅ Xcode installed (already have it)
- ✅ iOS Simulators installed (already have them)
- ✅ Appium installed (already have it at `/opt/homebrew/bin/appium`)

### For Android Emulators:
- ✅ Android SDK installed (already have it)
- ✅ Android emulators created (already have 3 emulators)
- ✅ Appium installed (already have it)

### Additional Requirements:
```bash
# Appium Doctor - verify your setup
npm install -g appium-doctor

# Run diagnostics
appium-doctor --android
appium-doctor --ios

# Install Appium drivers (if not already installed)
appium driver install xcuitest      # For iOS
appium driver install uiautomator2  # For Android
```

## 🚀 Quick Start

### 1. Start Appium Server

In a separate terminal window:
```bash
appium
```

Or start in background:
```bash
appium > appium.log 2>&1 &
```

### 2. Run Tests on iOS Simulator

```bash
# Navigate to framework directory
cd mobile-test-framework

# Run on iPhone SE (3rd generation)
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=iOS \
    --device="iPhone SE (3rd generation)" \
    -v

# Run on iPhone 16 Pro
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=iOS \
    --device="iPhone 16 Pro" \
    -v

# Run on iPad
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=iOS \
    --device="iPad Pro 11-inch (M4)" \
    -v
```

### 3. Run Tests on Android Emulator

```bash
# Run on Medium Phone API 35
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=Android \
    --device="Medium_Phone_API_35" \
    -v

# Run on Small Phone API 35
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=Android \
    --device="Small_Phone_API_35" \
    -v

# Run on custom emulator
uv run pytest tests/test_cases/test_real_emulators.py \
    --use-real-device \
    --platform=Android \
    --device="my_emulator" \
    -v
```

## 📱 Available Devices

### iOS Simulators (Auto-detected):
- iPhone 16 Pro
- iPhone 16 Pro Max
- iPhone 16
- iPhone 16 Plus
- iPhone SE (3rd generation)
- iPad Pro 11-inch (M4)
- iPad Pro 13-inch (M4)
- iPad Air 11-inch (M2)
- iPad Air 13-inch (M2)
- iPad mini (A17 Pro)
- iPad (10th generation)

### Android Emulators (Your AVDs):
- Medium_Phone_API_35
- Small_Phone_API_35
- my_emulator

## 🎨 Testing Modes Comparison

| Feature | Browser Emulation | Real Emulator/Simulator |
|---------|------------------|------------------------|
| Setup Time | Fast (seconds) | Slower (30-60 seconds) |
| Accuracy | Good | Excellent |
| Native Features | Limited | Full |
| Performance Testing | Limited | Realistic |
| Touch Gestures | Simulated | Real |
| Network Conditions | Emulated | Real |
| Battery/Sensors | No | Yes (with additional setup) |

## 📝 Command Reference

### Basic Commands

```bash
# Browser emulation (default, fast)
uv run pytest

# Real iOS simulator
uv run pytest --use-real-device --platform=iOS --device="iPhone SE (3rd generation)"

# Real Android emulator
uv run pytest --use-real-device --platform=Android --device="Medium_Phone_API_35"

# Run only emulator tests
uv run pytest -m emulator --use-real-device --platform=iOS

# Run iOS-specific emulator tests
uv run pytest -m "emulator and ios" --use-real-device --platform=iOS

# Run Android-specific emulator tests
uv run pytest -m "emulator and android" --use-real-device --platform=Android
```

### Advanced Commands

```bash
# Custom Appium server URL
uv run pytest --use-real-device --appium-server="http://192.168.1.100:4723"

# Run specific test file
uv run pytest tests/test_cases/test_real_emulators.py --use-real-device

# Run specific test class
uv run pytest tests/test_cases/test_real_emulators.py::TestIOSSimulator --use-real-device

# Run specific test method
uv run pytest tests/test_cases/test_real_emulators.py::TestIOSSimulator::test_safari_on_ios_simulator \
    --use-real-device --platform=iOS --device="iPhone SE (3rd generation)" -v

# Parallel execution (careful with emulators!)
uv run pytest --use-real-device -n 2
```

## 🔧 Configuration

### Available Command-Line Options

```bash
--use-real-device          # Enable real emulator/simulator mode
--platform=iOS|Android     # Platform to test on
--device="Device Name"     # Device/emulator name
--appium-server=URL        # Appium server URL (default: http://localhost:4723)
--browser=chrome|safari    # Browser (not used in real device mode)
--base-url=URL            # Base URL for tests
```

### Adding New Devices

Edit `config/config.py` and add your device to `REAL_DEVICE_CONFIGS`:

```python
REAL_DEVICE_CONFIGS = {
    "Your Custom Device": {
        "platform": "Android",
        "platformName": "Android",
        "platformVersion": "14.0",
        "deviceName": "Your Custom Device",
        "automationName": "UiAutomator2",
        "browserName": "Chrome",
        "avd": "your_avd_name"
    },
}
```

## 🐛 Troubleshooting

### iOS Simulator Issues

**Problem**: Simulator won't start
```bash
# Check available simulators
xcrun simctl list devices available

# Boot simulator manually
xcrun simctl boot "iPhone SE (3rd generation)"

# Reset simulator if needed
xcrun simctl erase "iPhone SE (3rd generation)"
```

**Problem**: WebDriver not connecting
```bash
# Check Appium is running
curl http://localhost:4723/status

# Check Appium XCUITest driver
appium driver list
```

### Android Emulator Issues

**Problem**: Emulator won't start
```bash
# List available AVDs
~/Library/Android/sdk/emulator/emulator -list-avds

# Start emulator manually
~/Library/Android/sdk/emulator/emulator -avd Medium_Phone_API_35

# Check running devices
adb devices
```

**Problem**: Chrome not found on emulator
```bash
# Connect to running emulator
adb shell

# Check Chrome package
pm list packages | grep chrome

# Install Chrome if missing (download APK first)
adb install chrome.apk
```

### Appium Server Issues

**Problem**: Server not starting
```bash
# Check if port is already in use
lsof -i :4723

# Kill process using the port
kill -9 <PID>

# Restart Appium
appium
```

**Problem**: Driver installation fails
```bash
# Clean Appium drivers
appium driver uninstall xcuitest
appium driver uninstall uiautomator2

# Reinstall
appium driver install xcuitest
appium driver install uiautomator2
```

## 📊 Performance Tips

### Speed Up Test Execution

1. **Keep emulators running**: Don't shut them down between test runs
2. **Use snapshots**: Create snapshots of emulators in a clean state
3. **Parallel testing**: Run tests on multiple emulators simultaneously
4. **Selective testing**: Use markers to run only necessary tests

```bash
# Run smoke tests only
uv run pytest -m "emulator and smoke" --use-real-device

# Skip slow tests
uv run pytest -m "emulator and not slow" --use-real-device
```

### Optimize Emulator Settings

**Android:**
```bash
# Start with better performance
~/Library/Android/sdk/emulator/emulator -avd Medium_Phone_API_35 \
    -no-snapshot-load \
    -wipe-data \
    -gpu swiftshader_indirect
```

**iOS:**
```bash
# Disable animations for faster tests
xcrun simctl boot "iPhone SE (3rd generation)"
xcrun simctl spawn "iPhone SE (3rd generation)" defaults write com.apple.springboard \
    UIApplicationAutomaticStatusBarHiddenKey -bool true
```

## 🎯 Best Practices

1. **Start Appium before tests**: Always have Appium server running
2. **Use appropriate markers**: Tag tests with `@pytest.mark.emulator`
3. **Handle timeouts**: Emulators are slower, increase timeouts if needed
4. **Clean state**: Start each test with a fresh browser context
5. **Resource management**: Close emulators when not in use
6. **CI/CD**: Use headless emulators for continuous integration

## 📚 Example Test

```python
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.emulator
@pytest.mark.ios
class TestIOSSimulator:
    def test_safari_on_ios(self, driver):
        """Test on iOS simulator."""
        driver.get("https://example.com")
        
        wait = WebDriverWait(driver, 10)
        heading = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        assert "Example Domain" in heading.text
```

Run with:
```bash
uv run pytest tests/test_cases/test_real_emulators.py::TestIOSSimulator::test_safari_on_ios \
    --use-real-device --platform=iOS --device="iPhone SE (3rd generation)" -v
```

## 🔄 Switching Between Modes

```bash
# Browser emulation (fast, for quick development)
uv run pytest tests/test_cases/test_mobile_example.py

# Real emulator (accurate, for final validation)
uv run pytest tests/test_cases/test_real_emulators.py --use-real-device

# Both modes in one run (if Appium is running)
uv run pytest  # browser emulation tests
uv run pytest -m emulator --use-real-device  # emulator tests
```

## 📖 Additional Resources

- [Appium Documentation](https://appium.io/docs/en/latest/)
- [XCUITest Driver](https://appium.io/docs/en/drivers/ios-xcuitest/)
- [UiAutomator2 Driver](https://appium.io/docs/en/drivers/android-uiautomator2/)
- [iOS Simulator Guide](https://developer.apple.com/documentation/xcode/running-your-app-in-simulator-or-on-a-device)
- [Android Emulator Guide](https://developer.android.com/studio/run/emulator)

---

**Ready to test on real devices! 📱🚀**
