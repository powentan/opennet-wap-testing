"""
Configuration settings for mobile testing framework.
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class BrowserConfig:
    """Browser configuration for mobile testing."""
    browser_name: str = "chrome"  # chrome or safari
    device_name: str = "iPhone 14 Pro"
    platform: str = "iOS"  # iOS or Android
    headless: bool = False
    window_size: tuple = (375, 812)  # iPhone 14 Pro dimensions
    implicit_wait: int = 10
    page_load_timeout: int = 30
    script_timeout: int = 30
    use_real_device: bool = False  # Use real emulator/simulator instead of browser emulation
    automation_name: str = "XCUITest"  # XCUITest for iOS, UiAutomator2 for Android
    appium_server_url: str = "http://localhost:4723"  # Appium server URL


@dataclass
class TestConfig:
    """General test configuration."""
    base_url: str = os.getenv("BASE_URL", "https://m.twitch.tv/")
    screenshot_on_failure: bool = True
    screenshot_dir: str = "reports/screenshots"
    video_recording: bool = False
    max_retries: int = 3
    retry_delay: int = 2


# Device presets for common mobile devices
DEVICE_PRESETS = {
    "iPhone 14 Pro": {
        "platform": "iOS",
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "viewport": {"width": 390, "height": 844},
        "pixel_ratio": 3
    },
    "iPhone SE": {
        "platform": "iOS",
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "viewport": {"width": 375, "height": 667},
        "pixel_ratio": 2
    },
    "iPad Pro": {
        "platform": "iOS",
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "viewport": {"width": 1024, "height": 1366},
        "pixel_ratio": 2
    },
    "Samsung Galaxy S21": {
        "platform": "Android",
        "user_agent": "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        "viewport": {"width": 360, "height": 800},
        "pixel_ratio": 3
    },
    "Pixel 6": {
        "platform": "Android",
        "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",
        "viewport": {"width": 412, "height": 915},
        "pixel_ratio": 2.625
    },
}


# Real device/emulator configurations for Appium
REAL_DEVICE_CONFIGS = {
    # iOS Simulators
    "iPhone 16 Pro": {
        "platform": "iOS",
        "platformName": "iOS",
        "platformVersion": "18.3",
        "deviceName": "iPhone 16 Pro",
        "automationName": "XCUITest",
        "browserName": "Safari",
        "udid": "auto"  # Will be auto-detected
    },
    "iPhone SE (3rd generation)": {
        "platform": "iOS",
        "platformName": "iOS",
        "platformVersion": "18.3",
        "deviceName": "iPhone SE (3rd generation)",
        "automationName": "XCUITest",
        "browserName": "Safari",
        "udid": "C45F00B8-51FD-422E-AC4C-0FFA8A75EB70"
    },
    "iPad Pro 11-inch (M4)": {
        "platform": "iOS",
        "platformName": "iOS",
        "platformVersion": "18.3",
        "deviceName": "iPad Pro 11-inch (M4)",
        "automationName": "XCUITest",
        "browserName": "Safari",
        "udid": "E742102B-8EEE-46FE-B237-B7CE61854003"
    },
    # Android Emulators
    "Medium_Phone_API_35": {
        "platform": "Android",
        "platformName": "Android",
        "platformVersion": "15.0",  # API 35
        "deviceName": "Medium_Phone_API_35",
        "automationName": "UiAutomator2",
        "browserName": "Chrome",
        "avd": "Medium_Phone_API_35"
    },
    "Small_Phone_API_35": {
        "platform": "Android",
        "platformName": "Android",
        "platformVersion": "15.0",  # API 35
        "deviceName": "Small_Phone_API_35",
        "automationName": "UiAutomator2",
        "browserName": "Chrome",
        "avd": "Small_Phone_API_35"
    },
    "my_emulator": {
        "platform": "Android",
        "platformName": "Android",
        "platformVersion": "15.0",  # API 35
        "deviceName": "my_emulator",
        "automationName": "UiAutomator2",
        "browserName": "Chrome",
        "avd": "my_emulator"
    },
}


# Environment-specific configurations
ENVIRONMENTS = {
    "dev": {
        "base_url": "https://dev.example.com",
        "api_url": "https://api-dev.example.com"
    },
    "staging": {
        "base_url": "https://staging.example.com",
        "api_url": "https://api-staging.example.com"
    },
    "prod": {
        "base_url": "https://www.example.com",
        "api_url": "https://api.example.com"
    }
}


def get_environment() -> str:
    """Get current test environment from env variable."""
    return os.getenv("TEST_ENV", "dev")


def get_config_for_environment(env: Optional[str] = None) -> dict:
    """Get configuration for specified environment."""
    env = env or get_environment()
    return ENVIRONMENTS.get(env, ENVIRONMENTS["dev"])
