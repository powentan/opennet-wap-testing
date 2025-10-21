# Mobile Test Framework

A comprehensive testing framework for mobile web applications using Python, Selenium, and uv. This framework supports testing mobile apps in Chrome (Android emulation) and Safari (iOS emulation) browsers, plus real Android/iOS emulators via Appium.

> 📚 **[Complete Documentation](docs/)** | 🚀 **[Getting Started](docs/GETTING_STARTED.md)** | 📱 **[Real Emulator Guide](docs/REAL_EMULATOR_GUIDE.md)** | 🐛 **[Troubleshooting](docs/TROUBLESHOOTING.md)**

## Features

- 🚀 **Fast Setup**: Uses `uv` for ultra-fast dependency management
- 📱 **Mobile Emulation**: Support for both iOS (Safari) and Android (Chrome) devices
- 🎯 **Two Testing Modes**: Browser emulation (fast) and real emulator/simulator (accurate)
- 🧪 **Pytest Integration**: Powerful test framework with fixtures and markers
- 📸 **Screenshot Capture**: Automatic screenshots on test failures
- 📊 **HTML Reports**: Detailed test execution reports
- ⚡ **Parallel Execution**: Run tests in parallel using pytest-xdist
- 🎯 **Page Object Model**: Clean and maintainable test structure
- 🔄 **Mobile Gestures**: Built-in support for swipe, tap, and long-press actions
- 🤖 **Appium Integration**: Test on real Android emulators and iOS simulators

## Demo

![Test Execution Demo](assets/running_result.gif)

## Table of Contents

- [Setup and Installation](#setup-and-installation)
- [How to Run Tests](#how-to-run-tests)
- [How to Read Reports and Screenshots](#how-to-read-reports-and-screenshots)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Setup and Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **uv package manager** - Install with:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Chrome browser** - For Android emulation testing
- **Safari browser** - For iOS emulation testing (macOS only)
- **Node.js and npm** - For running Appium (real device testing)
- **Appium** - For real emulator/simulator testing:
  ```bash
  npm install -g appium
  ```

### Installation Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd /path/to/mobile-test-framework
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```
   
   This command will:
   - Create a virtual environment automatically
   - Install all required Python dependencies (pytest, selenium, appium-python-client, etc.)
   - Lock the dependencies in `uv.lock` file

3. **Verify installation:**
   ```bash
   uv run pytest --version
   ```
   
   You should see the pytest version number displayed.

4. **(Optional) Enable Safari WebDriver (macOS only):**
   ```bash
   safaridriver --enable
   ```

### Additional Setup for Real Device Testing

If you plan to use real Android emulators or iOS simulators:

1. **Install Appium:**
   ```bash
   npm install -g appium
   ```

2. **For Android testing:**
   - Install Android Studio
   - Set up Android SDK
   - Create Android Virtual Devices (AVDs)

3. **For iOS testing (macOS only):**
   - Install Xcode
   - Install Xcode Command Line Tools
   - iOS Simulators come bundled with Xcode

## How to Run Tests

The framework supports two testing modes:
1. **Browser Emulation Mode**: Fast testing using Chrome/Safari with mobile device emulation
2. **Real Emulator/Simulator Mode**: Accurate testing on actual Android emulators or iOS simulators using Appium

### Quick Start - Browser Emulation Mode

Run all tests with default settings:
```bash
uv run pytest
```

This will run tests using Chrome browser with iPhone 14 Pro emulation.

### Using the Helper Script (Real Emulator/Simulator Testing)

The `run-emulator-tests.sh` script simplifies testing on real devices by managing the Appium server and test execution.

#### Available Commands

```bash
# Show all available commands
./run-emulator-tests.sh help

# Show available devices
./run-emulator-tests.sh devices

# Start Appium server
./run-emulator-tests.sh start

# Stop Appium server
./run-emulator-tests.sh stop
```

#### Running Tests on Android Emulator

**Prerequisites:**
- Android Studio installed with Android SDK
- Android Virtual Device (AVD) created (e.g., Medium_Phone_API_35)
- AVD must be started before running tests

**Example: Run tests on Android emulator**

1. Start your Android emulator from Android Studio or command line:
   ```bash
   emulator -avd Medium_Phone_API_35
   ```

2. Run tests using the helper script:
   ```bash
   ./run-emulator-tests.sh test-android Medium_Phone_API_35
   ```
   
   This command will:
   - Check if Appium is installed
   - Start Appium server automatically if not running
   - Execute tests on the specified Android emulator
   - Display test results

**Example: Run tests on a different Android emulator**
```bash
./run-emulator-tests.sh test-android Small_Phone_API_35
```

**Example: Run tests with custom emulator name**
```bash
./run-emulator-tests.sh test-android my_emulator
```

#### Running Tests on iOS Simulator (macOS only)

**Example: Run tests on iOS simulator**
```bash
./run-emulator-tests.sh test-ios "iPhone SE (3rd generation)"
```

**Example: Run tests on different iOS simulators**
```bash
# iPhone 16 Pro
./run-emulator-tests.sh test-ios "iPhone 16 Pro"

# iPad Pro
./run-emulator-tests.sh test-ios "iPad Pro 11-inch (M4)"
```

### Manual Test Execution (Advanced)

#### Direct pytest commands for real devices:

**Android:**
```bash
uv run pytest tests/twitch \
    --use-real-device \
    --platform=Android \
    --device="Medium_Phone_API_35" \
    -s \
    -v
```

**iOS:**
```bash
uv run pytest tests/twitch \
    --use-real-device \
    --platform=iOS \
    --device="iPhone SE (3rd generation)" \
    -s \
    -v
```

#### Browser Emulation with Custom Device:

```bash
# Test on iPhone SE with Safari
uv run pytest --browser=safari --device="iPhone SE" --platform=iOS

# Test on Samsung Galaxy S21 with Chrome
uv run pytest --browser=chrome --device="Samsung Galaxy S21" --platform=Android
```

#### Additional pytest Options:

```bash
# Run in headless mode (browser emulation only)
uv run pytest --headless

# Run specific test file
uv run pytest tests/twitch/test_search.py

# Run with specific markers
uv run pytest -m smoke          # Run only smoke tests
uv run pytest -m android        # Run only Android tests
uv run pytest -m emulator       # Run only emulator tests

# Run specific test function
uv run pytest tests/twitch/test_search.py::test_search_functionality

# Run with verbose output
uv run pytest -v

# Run without parallel execution
uv run pytest -n 0
```

## How to Read Reports and Screenshots

After running tests, the framework automatically generates detailed test reports and captures screenshots of failures.

### Test Reports Location

All test outputs are saved in the `reports/` directory:

```
reports/
├── report.html          # Main HTML test report
└── screenshots/         # Screenshots (if any failures occurred)
```

### Viewing the HTML Report

The HTML report provides a comprehensive overview of test execution:

**Open the report:**
```bash
# macOS
open reports/report.html

# Linux
xdg-open reports/report.html

# Windows
start reports/report.html
```

**Report Contents:**
- **Summary Section**: Total tests, passed, failed, skipped, and execution time
- **Test Results**: Detailed list of all test cases with their status
- **Test Details**: Click on any test to see:
  - Test function name and location
  - Execution time
  - Test output and logs
  - Error messages and tracebacks (for failed tests)
  - Screenshots (for failed tests with screenshots enabled)
- **Environment Info**: Python version, packages, and platform details

### Understanding Test Results

The report uses color coding for easy identification:
- 🟢 **Green (Passed)**: Test executed successfully
- 🔴 **Red (Failed)**: Test failed with error details
- 🟡 **Yellow (Skipped)**: Test was skipped
- 🟠 **Orange (Error)**: Test encountered an error during setup/teardown

### Screenshots

Screenshots are automatically captured when tests fail (configured in `tests/conftest.py`):

**Screenshot naming convention:**
```
test_<test_name>_<timestamp>.png
```

**Example:**
```
test_search_functionality_20241021_143022.png
```

**Viewing screenshots:**
1. Navigate to the `reports/screenshots/` directory
2. Open screenshots with any image viewer
3. Screenshots are also embedded in the HTML report for failed tests

**Screenshot information includes:**
- Full page capture at the moment of failure
- Timestamp of when the failure occurred
- Associated test case name

### Interpreting Test Failures

When a test fails, the report provides:

1. **Error Type**: The exception that caused the failure (e.g., AssertionError, TimeoutException)
2. **Error Message**: Description of what went wrong
3. **Stack Trace**: Full traceback showing where the error occurred
4. **Screenshot**: Visual state of the application when the test failed
5. **Test Logs**: Any print statements or logging output from the test

**Example failure analysis:**
```
AssertionError: Expected element to be visible, but it was not found
File: tests/twitch/test_search.py, line 45
Screenshot: test_search_functionality_20241021_143022.png
```

### Best Practices for Report Review

1. **Check Summary First**: Review overall pass/fail rate
2. **Prioritize Failures**: Focus on failed tests in the detailed section
3. **Review Screenshots**: Screenshots often reveal UI issues immediately
4. **Check Error Messages**: Read the error message and stack trace carefully
5. **Verify Environment**: Ensure tests ran in the expected environment (device, platform)
6. **Compare Runs**: Keep previous reports to track regression patterns

### Continuous Integration

The HTML report is CI/CD friendly and can be archived as a build artifact:
- Self-contained HTML (all styles and scripts embedded)
- No external dependencies required to view
- Can be uploaded to artifact storage or shared via email

## Project Structure

```
mobile-test-framework/
├── config/
│   ├── __init__.py
│   └── config.py              # Configuration settings
├── drivers/
│   ├── __init__.py
│   └── driver_factory.py      # WebDriver factory for Chrome/Safari
├── pages/
│   ├── __init__.py
│   ├── base_page.py           # Base Page Object class
│   └── example_page.py        # Example page object
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures and hooks
│   └── twitch/
│       ├── __init__.py
│       └── test_search.py     # Example test cases
├── reports/                   # Test reports and screenshots
│   ├── report.html           # HTML test report
│   └── screenshots/          # Failure screenshots
├── docs/                      # Complete documentation
├── run-emulator-tests.sh     # Helper script for emulator testing
├── pyproject.toml            # Project dependencies and pytest config
├── uv.lock                   # Locked dependencies
└── README.md                 # This file
```

## Configuration

### Environment Variables

Set environment variables for different configurations:

```bash
export TEST_ENV=staging
export BASE_URL=https://staging.example.com
uv run pytest
```

### Device Configuration

Edit `config/config.py` to add custom device presets or modify settings:

```python
DEVICE_PRESETS = {
    "Custom Device": {
        "platform": "iOS",
        "user_agent": "your-user-agent-string",
        "viewport": {"width": 375, "height": 812},
        "pixel_ratio": 2
    },
}
```

## Best Practices

1. **Use Page Objects**: Keep test logic separate from page interactions
2. **Use Explicit Waits**: Avoid `time.sleep()`, use built-in wait methods
3. **Mark Tests Appropriately**: Use markers for easy filtering (smoke, regression, etc.)
4. **Take Screenshots**: Automatically captured on failures via conftest
5. **Clean Test Data**: Clean up test data in teardown fixtures
6. **Independent Tests**: Each test should be able to run independently

## Troubleshooting

### Common Issues

**Safari WebDriver Issues (macOS)**

If Safari tests fail, enable Safari WebDriver:
```bash
safaridriver --enable
```

**Chrome Driver Issues**

The framework uses `webdriver-manager` to automatically download ChromeDriver. If issues occur:
```bash
# Clear webdriver-manager cache
rm -rf ~/.wdm
```

**Appium Connection Issues**

If tests fail to connect to Appium:
```bash
# Check if Appium is running
curl http://localhost:4723/status

# Restart Appium
./run-emulator-tests.sh stop
./run-emulator-tests.sh start
```

**Android Emulator Not Found**

Ensure the emulator is running before starting tests:
```bash
# List available emulators
emulator -list-avds

# Start specific emulator
emulator -avd Medium_Phone_API_35
```

**iOS Simulator Not Found**

List available iOS simulators:
```bash
xcrun simctl list devices
```

**Permission Issues (macOS)**

If you encounter permission errors:
```bash
# Allow ChromeDriver to run
xattr -d com.apple.quarantine /path/to/chromedriver
```

For more detailed troubleshooting, see the [Complete Troubleshooting Guide](docs/TROUBLESHOOTING.md).

## Additional Resources

Complete documentation is available in the [`docs/`](docs/) directory:

### 📚 Quick Links
- **[Documentation Index](docs/README.md)** - Complete documentation hub
- **[Getting Started Guide](docs/GETTING_STARTED.md)** - Detailed setup instructions
- **[Real Emulator Guide](docs/REAL_EMULATOR_GUIDE.md)** - Complete guide for Android/iOS emulators
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### 📱 Available Test Markers

The framework supports the following pytest markers:
- `@pytest.mark.smoke` - Quick smoke tests
- `@pytest.mark.regression` - Full regression tests
- `@pytest.mark.android` - Android-specific tests
- `@pytest.mark.ios` - iOS-specific tests
- `@pytest.mark.chrome` - Chrome browser tests
- `@pytest.mark.safari` - Safari browser tests
- `@pytest.mark.emulator` - Real emulator/simulator tests
- `@pytest.mark.browser_emulation` - Browser emulation tests

## Support

For issues or questions:
1. Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. Review the [Complete Documentation](docs/)
3. Check the test logs in `reports/report.html`
4. Review Appium logs in `appium.log` (for emulator testing)

## License

This project is provided as-is for testing purposes.

---

**Happy Testing! 📱🚀**
