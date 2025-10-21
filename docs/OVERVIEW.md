# Mobile Testing Framework - Project Overview

## 📋 Summary

This is a complete, production-ready mobile testing framework built with:
- **uv** - Ultra-fast Python package manager
- **Python 3.10+** - Modern Python with type hints
- **Selenium** - Industry-standard web automation
- **Pytest** - Powerful testing framework
- **Page Object Model** - Clean, maintainable architecture

## ✨ Key Features

### 1. Mobile Emulation
- ✅ iOS devices (iPhone, iPad) via Chrome/Safari
- ✅ Android devices (Samsung, Pixel) via Chrome
- ✅ Custom device configurations
- ✅ Accurate viewport and user agent simulation

### 2. Testing Capabilities
- ✅ Mobile gestures (swipe, tap, long-press)
- ✅ Touch interactions
- ✅ Responsive design testing
- ✅ Network throttling (3G, 4G simulation)
- ✅ Screenshot capture on failures
- ✅ HTML test reports

### 3. Developer Experience
- ✅ Fast setup with uv (< 1 minute)
- ✅ Page Object Model pattern
- ✅ Pytest fixtures and markers
- ✅ Parallel test execution
- ✅ Headless mode support
- ✅ Comprehensive documentation

## 📁 Project Structure

```
oppnet-wap-testing/
├── config/                    # Configuration management
│   ├── config.py             # Device presets, settings
│   └── __init__.py
│
├── drivers/                   # WebDriver factory
│   ├── driver_factory.py     # Chrome & Safari driver creation
│   └── __init__.py
│
├── pages/                     # Page Object Model
│   ├── base_page.py          # Base class with common methods
│   ├── example_page.py       # Example page object
│   └── __init__.py
│
├── tests/                     # Test suite
│   ├── conftest.py           # Pytest fixtures & hooks
│   ├── utils.py              # Helper utilities
│   ├── test_cases/           # Test files
│   │   ├── test_framework.py     # Framework validation tests
│   │   └── test_mobile_example.py # Example test cases
│   └── __init__.py
│
├── reports/                   # Generated reports
│   ├── report.html           # HTML test report
│   └── screenshots/          # Failure screenshots
│
├── README.md                  # Comprehensive documentation
├── GETTING_STARTED.md        # Quick start guide
├── pyproject.toml            # Dependencies & pytest config
├── uv.lock                   # Locked dependencies
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore patterns
└── quick-start.sh           # Setup automation script
```

## 🚀 Quick Start

### Installation
```bash
cd oppnet-wap-testing
uv sync
```

### Run Tests
```bash
# Run all tests
uv run pytest

# Run smoke tests
uv run pytest -m smoke

# Run in headless mode
uv run pytest --headless

# Test specific device
uv run pytest --device="iPhone SE" --browser=chrome
```

## 📱 Supported Devices

### iOS
- iPhone 14 Pro (390×844, 3x)
- iPhone SE (375×667, 2x)
- iPad Pro (1024×1366, 2x)

### Android
- Samsung Galaxy S21 (360×800, 3x)
- Google Pixel 6 (412×915, 2.625x)

## 🎯 Test Markers

Organize and filter tests using markers:

- `@pytest.mark.smoke` - Critical path tests
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.ios` - iOS-specific tests
- `@pytest.mark.android` - Android-specific tests
- `@pytest.mark.chrome` - Chrome browser tests
- `@pytest.mark.safari` - Safari browser tests

## 📊 Test Reports

After running tests, view the HTML report:
```bash
open reports/report.html
```

Reports include:
- Test results summary
- Execution time
- Screenshots of failures
- Full stack traces
- Test metadata

## 🧪 Example Test

```python
import pytest
from pages.base_page import BasePage

@pytest.mark.smoke
@pytest.mark.chrome
def test_mobile_navigation(driver, test_config):
    """Test mobile navigation."""
    driver.get(test_config.base_url)
    page = BasePage(driver)
    
    # Mobile gestures
    page.swipe_up()
    page.tap((By.ID, "menu-button"))
    
    assert page.is_element_visible((By.CLASS_NAME, "menu"))
```

## 🔧 Configuration

### Command Line Options
```bash
--browser=chrome|safari      # Browser selection
--device="Device Name"       # Device to emulate
--platform=iOS|Android       # Platform type
--headless                   # Headless mode
--base-url=URL              # Base URL for tests
-n auto                     # Parallel execution
-m marker                   # Run specific markers
```

### Environment Variables
```bash
TEST_ENV=dev|staging|prod   # Environment
BASE_URL=https://...        # Base URL
LOG_LEVEL=INFO|DEBUG        # Logging level
```

## 🛠 Built-in Utilities

### Mobile Gestures
```python
page.swipe_up()          # Scroll down
page.swipe_down()        # Scroll up
page.swipe_left()        # Swipe left
page.swipe_right()       # Swipe right
page.tap(locator)        # Tap element
page.long_press(locator) # Long press
```

### Wait Methods
```python
page.wait_for_element_to_disappear(locator)
page.is_element_visible(locator)
page.scroll_to_element(locator)
```

### Network Simulation
```python
from tests.utils import simulate_3g_connection, simulate_4g_connection

simulate_3g_connection(driver)  # Slow network
simulate_4g_connection(driver)  # Fast network
```

### Screenshots
```python
from tests.utils import take_screenshot

take_screenshot(driver, "my_test")  # Manual screenshot
# Automatic screenshots on test failures
```

## 🎓 Learning Resources

### Documentation Files
1. **README.md** - Complete framework documentation
2. **GETTING_STARTED.md** - Step-by-step guide
3. **This file** - Project overview

### Example Code
1. **tests/test_cases/test_framework.py** - Framework validation
2. **tests/test_cases/test_mobile_example.py** - Example tests
3. **pages/example_page.py** - Page object example
4. **pages/base_page.py** - Base page with all methods

## 🔍 Key Components Explained

### 1. Driver Factory
Creates properly configured WebDriver instances for mobile testing:
- Chrome with mobile emulation
- Safari with iOS simulation
- Device-specific user agents
- Viewport configuration

### 2. Page Object Model
Separates test logic from page interactions:
- Reusable page components
- Maintainable locators
- Business-logic methods
- Clear abstraction

### 3. Pytest Integration
Leverages pytest's powerful features:
- Fixtures for setup/teardown
- Markers for test organization
- Parallel execution
- HTML reporting
- Screenshot capture

### 4. Configuration System
Flexible configuration management:
- Device presets
- Environment-specific settings
- Command-line overrides
- Default values

## 🚦 CI/CD Ready

The framework is ready for continuous integration:

```yaml
# GitHub Actions example
- name: Run Mobile Tests
  run: uv run pytest -m smoke --headless
```

Supports:
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Any CI/CD platform

## 📈 Performance

### Fast Execution
- Parallel test execution with pytest-xdist
- Headless mode for CI/CD
- Efficient driver management
- Smart waiting strategies

### Scalable
- Add new devices easily
- Extend page objects
- Create custom fixtures
- Add utility functions

## 🔐 Best Practices Implemented

1. ✅ Page Object Model pattern
2. ✅ Explicit waits over implicit waits
3. ✅ DRY (Don't Repeat Yourself) principle
4. ✅ Clear test naming conventions
5. ✅ Proper test isolation
6. ✅ Screenshot on failure
7. ✅ Comprehensive logging
8. ✅ Type hints for better IDE support

## 🆘 Common Issues & Solutions

### Issue: ChromeDriver not found
**Solution**: Clear cache
```bash
rm -rf ~/.wdm
```

### Issue: Safari WebDriver disabled
**Solution**: Enable it
```bash
safaridriver --enable
```

### Issue: Tests are slow
**Solution**: Use parallel execution
```bash
uv run pytest -n auto --headless
```

### Issue: Element not found
**Solution**: Check explicit waits
```python
page.wait_for_element_to_appear(locator, timeout=30)
```

## 📦 Dependencies

Core packages (auto-installed with `uv sync`):
- selenium>=4.37.0
- pytest>=8.4.2
- pytest-html>=4.1.1
- pytest-xdist>=3.8.0
- webdriver-manager>=4.0.2

## 🎯 Use Cases

This framework is perfect for:

1. **Mobile Web Application Testing**
   - Responsive design validation
   - Mobile-specific features
   - Cross-device compatibility

2. **Progressive Web Apps (PWA)**
   - Touch interactions
   - Offline capabilities
   - Mobile UI/UX

3. **E-commerce Mobile Sites**
   - Shopping flows
   - Checkout processes
   - Product browsing

4. **Content Websites**
   - Article reading experience
   - Media playback
   - Navigation patterns

## 🔄 Maintenance

### Updating Dependencies
```bash
uv sync --upgrade
```

### Adding New Dependencies
```bash
uv add package-name
```

### Updating Device Presets
Edit `config/config.py` to add new devices or modify existing ones.

## 📝 Next Steps

1. **Customize for Your App**
   - Update base URL in config
   - Create app-specific page objects
   - Write test scenarios

2. **Extend Framework**
   - Add custom fixtures
   - Create helper utilities
   - Add more device presets

3. **Set Up CI/CD**
   - Configure pipeline
   - Add test scheduling
   - Set up notifications

4. **Team Collaboration**
   - Share page objects
   - Review test coverage
   - Maintain documentation

## 🎉 You're Ready!

The framework is fully functional and ready to use. Start by:

1. Running the example tests
2. Exploring the page objects
3. Writing your first custom test
4. Integrating with your CI/CD

For detailed instructions, see **GETTING_STARTED.md**

---

**Happy Testing! 🚀📱**
