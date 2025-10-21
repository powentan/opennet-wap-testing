# Getting Started Guide - Mobile Test Framework

## Quick Start (5 minutes)

### 1. Setup the Environment

Navigate to the framework directory:
```bash
cd mobile-test-framework
```

Run the quick start script:
```bash
./quick-start.sh
```

Or manually sync dependencies:
```bash
uv sync
```

### 2. Run Your First Test

Run a simple smoke test:
```bash
uv run pytest -m smoke --headless
```

### 3. View the Report

Open the generated HTML report:
```bash
open reports/report.html  # macOS
# or
xdg-open reports/report.html  # Linux
# or navigate to reports/report.html in your browser
```

## Common Usage Patterns

### Testing Different Devices

#### iPhone 14 Pro (Default)
```bash
uv run pytest --browser=chrome --device="iPhone 14 Pro" --platform=iOS
```

#### Samsung Galaxy S21
```bash
uv run pytest --browser=chrome --device="Samsung Galaxy S21" --platform=Android
```

#### iPad Pro
```bash
uv run pytest --browser=chrome --device="iPad Pro" --platform=iOS
```

#### iPhone SE
```bash
uv run pytest --browser=chrome --device="iPhone SE" --platform=iOS
```

#### Google Pixel 6
```bash
uv run pytest --browser=chrome --device="Pixel 6" --platform=Android
```

### Running Specific Test Types

#### Smoke Tests (Quick validation)
```bash
uv run pytest -m smoke
```

#### Regression Tests
```bash
uv run pytest -m regression
```

#### iOS Specific Tests
```bash
uv run pytest -m ios
```

#### Android Specific Tests
```bash
uv run pytest -m android
```

#### Chrome Tests Only
```bash
uv run pytest -m chrome
```

### Testing with Different Browsers

#### Chrome (Android emulation)
```bash
uv run pytest --browser=chrome --device="Samsung Galaxy S21"
```

#### Safari (iOS emulation) - macOS only
```bash
uv run pytest --browser=safari --device="iPhone 14 Pro"
```

Note: Safari requires enabling WebDriver on macOS:
```bash
safaridriver --enable
```

### Performance Testing

#### Run in Headless Mode (Faster)
```bash
uv run pytest --headless
```

#### Parallel Execution
```bash
# Use all CPU cores
uv run pytest -n auto

# Use specific number of workers
uv run pytest -n 4
```

#### Single Worker (Sequential)
```bash
uv run pytest -n 0
```

### Running Specific Tests

#### Single Test File
```bash
uv run pytest tests/test_cases/test_framework.py
```

#### Single Test Function
```bash
uv run pytest tests/test_cases/test_framework.py::test_framework_setup
```

#### Single Test Class
```bash
uv run pytest tests/test_cases/test_mobile_example.py::TestMobileChrome
```

#### Single Test Method in Class
```bash
uv run pytest tests/test_cases/test_mobile_example.py::TestMobileChrome::test_page_loads
```

### Testing Different Environments

#### Development Environment
```bash
export TEST_ENV=dev
uv run pytest --base-url=https://dev.example.com
```

#### Staging Environment
```bash
export TEST_ENV=staging
uv run pytest --base-url=https://staging.example.com
```

#### Production Environment
```bash
export TEST_ENV=prod
uv run pytest --base-url=https://www.example.com
```

### Advanced Options

#### Verbose Output
```bash
uv run pytest -v
```

#### Very Verbose Output (show test details)
```bash
uv run pytest -vv
```

#### Show Test Output (print statements)
```bash
uv run pytest -s
```

#### Stop on First Failure
```bash
uv run pytest -x
```

#### Stop After N Failures
```bash
uv run pytest --maxfail=3
```

#### Rerun Failed Tests
```bash
# Run all tests
uv run pytest

# Rerun only failures
uv run pytest --lf
```

#### Run New Tests Only
```bash
uv run pytest --nf
```

## Writing Your First Test

### 1. Create a Page Object

Create a new file in `pages/` directory:

```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page object."""
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def login(self, username: str, password: str):
        """Perform login."""
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        """Get error message text."""
        return self.get_text(self.ERROR_MESSAGE)
```

### 2. Create a Test File

Create a new file in `tests/test_cases/` directory:

```python
# tests/test_cases/test_login.py
import pytest
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.chrome
class TestLogin:
    """Login test cases."""
    
    def test_valid_login(self, driver, test_config):
        """Test login with valid credentials."""
        driver.get(f"{test_config.base_url}/login")
        login_page = LoginPage(driver)
        
        login_page.login("testuser", "password123")
        
        # Verify redirect to dashboard
        assert "/dashboard" in driver.current_url
    
    def test_invalid_login(self, driver, test_config):
        """Test login with invalid credentials."""
        driver.get(f"{test_config.base_url}/login")
        login_page = LoginPage(driver)
        
        login_page.login("invalid", "wrong")
        
        # Verify error message
        error = login_page.get_error_message()
        assert "Invalid credentials" in error
```

### 3. Run Your Test

```bash
uv run pytest tests/test_cases/test_login.py -v
```

## Mobile-Specific Features

### Touch Gestures

```python
from pages.base_page import BasePage

def test_swipe_gestures(driver):
    page = BasePage(driver)
    
    # Swipe up (scroll down)
    page.swipe_up()
    
    # Swipe down (scroll up)
    page.swipe_down()
    
    # Swipe left
    page.swipe_left()
    
    # Swipe right
    page.swipe_right()
```

### Tap and Long Press

```python
def test_touch_interactions(driver):
    page = BasePage(driver)
    
    # Tap element
    page.tap((By.ID, "menu-button"))
    
    # Long press for 2 seconds
    page.long_press((By.ID, "item"), duration=2000)
```

### Check Viewport Size

```python
def test_mobile_viewport(driver):
    viewport = driver.execute_script("""
        return {
            width: window.innerWidth,
            height: window.innerHeight
        }
    """)
    
    assert viewport['width'] <= 500, "Should be mobile viewport"
```

## Debugging Tests

### Take Screenshots

```python
def test_with_screenshot(driver):
    from tests.utils import take_screenshot
    
    driver.get("https://example.com")
    take_screenshot(driver, "my_test")
    # Screenshot saved to reports/screenshots/
```

### Highlight Elements (Visual Debugging)

```python
def test_with_highlight(driver):
    from tests.utils import highlight_element
    
    element = driver.find_element(By.ID, "button")
    highlight_element(driver, element, duration=2)
```

### Run in Non-Headless Mode

```bash
# Remove --headless flag or don't use it
uv run pytest tests/test_cases/test_login.py
```

### Add Print Statements

```python
def test_debug(driver):
    print("Starting test...")
    driver.get("https://example.com")
    print(f"Current URL: {driver.current_url}")
    print(f"Title: {driver.title}")
```

Run with output shown:
```bash
uv run pytest -s
```

## Network Simulation

### Simulate 3G Connection

```python
def test_slow_network(driver):
    from tests.utils import simulate_3g_connection
    
    simulate_3g_connection(driver)
    driver.get("https://example.com")
    # Page loads with 3G speed
```

### Simulate 4G Connection

```python
def test_4g_network(driver):
    from tests.utils import simulate_4g_connection
    
    simulate_4g_connection(driver)
    driver.get("https://example.com")
```

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/mobile-tests.yml`:

```yaml
name: Mobile Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh
    
    - name: Install dependencies
      run: uv sync
    
    - name: Run tests
      run: uv run pytest -m smoke --headless
    
    - name: Upload test reports
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-reports
        path: reports/
```

## Tips and Best Practices

1. **Always Use Headless for CI/CD**: Add `--headless` flag
2. **Use Markers**: Organize tests with markers for easy filtering
3. **Parallel Execution**: Use `-n auto` for faster test runs
4. **Screenshot on Failure**: Already configured automatically
5. **Clean Test Data**: Use fixtures to set up and tear down
6. **Independent Tests**: Each test should be able to run independently
7. **Explicit Waits**: Use built-in wait methods, avoid `time.sleep()`
8. **Page Objects**: Keep test logic separate from page interactions

## Troubleshooting

### ChromeDriver Issues

If ChromeDriver is not found:
```bash
# Clear cache and let it re-download
rm -rf ~/.wdm
uv run pytest
```

### Safari Issues (macOS)

Enable Safari WebDriver:
```bash
safaridriver --enable
```

### Tests Hanging

Increase timeouts in `config/config.py`:
```python
implicit_wait: int = 20
page_load_timeout: int = 60
```

### Permission Denied on macOS

Allow ChromeDriver to run:
```bash
xattr -d com.apple.quarantine /path/to/chromedriver
```

## Getting Help

1. Check the README.md for comprehensive documentation
2. Review example tests in `tests/test_cases/`
3. Look at page object examples in `pages/`
4. Check configuration options in `config/config.py`

## Next Steps

1. Write tests for your specific application
2. Create page objects for your pages
3. Set up CI/CD integration
4. Add custom fixtures as needed
5. Extend the framework with additional utilities

Happy Testing! 🚀
