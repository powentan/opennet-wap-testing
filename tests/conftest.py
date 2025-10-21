"""Pytest configuration and fixtures."""
import pytest
import logging
import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import BrowserConfig, TestConfig
from drivers.driver_factory import DriverFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use: chrome or safari"
    )
    parser.addoption(
        "--device",
        action="store",
        default="iPhone 14 Pro",
        help="Device to emulate"
    )
    parser.addoption(
        "--platform",
        action="store",
        default="iOS",
        help="Platform: iOS or Android"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.example.com",
        help="Base URL for tests"
    )
    parser.addoption(
        "--use-real-device",
        action="store_true",
        default=False,
        help="Use real emulator/simulator instead of browser emulation"
    )
    parser.addoption(
        "--appium-server",
        action="store",
        default="http://localhost:4723",
        help="Appium server URL"
    )


@pytest.fixture(scope="session")
def test_config(request):
    """Test configuration fixture."""
    config = TestConfig()
    config.base_url = request.config.getoption("--base-url")
    
    # Create screenshot directory
    os.makedirs(config.screenshot_dir, exist_ok=True)
    
    return config


@pytest.fixture(scope="session")
def browser_config(request):
    """Browser configuration fixture."""
    config = BrowserConfig()
    config.browser_name = request.config.getoption("--browser")
    config.device_name = request.config.getoption("--device")
    config.platform = request.config.getoption("--platform")
    config.headless = request.config.getoption("--headless")
    config.use_real_device = request.config.getoption("--use-real-device")
    config.appium_server_url = request.config.getoption("--appium-server")
    
    mode = "real emulator/simulator" if config.use_real_device else "browser emulation"
    logger.info(f"Browser config: {config.browser_name}, Device: {config.device_name}, Platform: {config.platform}, Mode: {mode}")
    return config


@pytest.fixture(scope="function")
def driver(browser_config) -> WebDriver:
    """
    WebDriver fixture that creates and quits driver for each test.
    
    Args:
        browser_config: Browser configuration
        
    Yields:
        WebDriver instance
    """
    driver = None
    try:
        driver = DriverFactory.create_driver(browser_config)
        yield driver
    finally:
        if driver:
            DriverFactory.quit_driver(driver)


@pytest.fixture(scope="class")
def class_driver(browser_config) -> WebDriver:
    """
    WebDriver fixture that creates and quits driver for test class.
    Useful for test classes that share driver state.
    
    Args:
        browser_config: Browser configuration
        
    Yields:
        WebDriver instance
    """
    driver = None
    try:
        driver = DriverFactory.create_driver(browser_config)
        yield driver
    finally:
        if driver:
            DriverFactory.quit_driver(driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only capture on test failure
    if report.when == "call" and report.failed:
        driver = None
        
        # Try to get driver from different fixture scopes
        if "driver" in item.funcargs:
            driver = item.funcargs["driver"]
        elif "class_driver" in item.funcargs:
            driver = item.funcargs["class_driver"]
        
        if driver:
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join("reports/screenshots", screenshot_name)
            
            try:
                driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
                
                # Attach to pytest-html report
                if hasattr(report, 'extra'):
                    report.extra.append(pytest.html.extras.image(screenshot_path))
            except Exception as e:
                logger.error(f"Failed to take screenshot: {e}")


# Markers for filtering tests
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "ios: iOS specific tests")
    config.addinivalue_line("markers", "android: Android specific tests")
    config.addinivalue_line("markers", "chrome: Chrome browser tests")
    config.addinivalue_line("markers", "safari: Safari browser tests")
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")
