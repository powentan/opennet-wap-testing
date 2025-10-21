"""
Driver factory for creating mobile web drivers.
Supports both browser emulation and real device/emulator testing.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from webdriver_manager.chrome import ChromeDriverManager
from appium import webdriver as appium_webdriver
from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options
from typing import Optional, Union
import logging
import subprocess
import time

from config.config import BrowserConfig, DEVICE_PRESETS, REAL_DEVICE_CONFIGS

logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory class for creating WebDriver instances configured for mobile testing."""
    
    @staticmethod
    def start_ios_simulator(device_name: str, udid: Optional[str] = None) -> str:
        """
        Start an iOS simulator.
        
        Args:
            device_name: Name of the simulator
            udid: Optional UDID of the simulator
            
        Returns:
            UDID of the started simulator
        """
        try:
            if not udid or udid == "auto":
                # Find UDID by device name
                result = subprocess.run(
                    ["xcrun", "simctl", "list", "devices", "available"],
                    capture_output=True, text=True
                )
                for line in result.stdout.split('\n'):
                    if device_name in line and "Shutdown" in line:
                        # Extract UDID from line like: iPhone 16 Pro (UDID) (Shutdown)
                        udid = line.split('(')[1].split(')')[0]
                        break
                
                if not udid or udid == "auto":
                    raise ValueError(f"Could not find simulator: {device_name}")
            
            # Boot the simulator
            logger.info(f"Starting iOS simulator: {device_name} ({udid})")
            subprocess.run(["xcrun", "simctl", "boot", udid], check=False)
            time.sleep(3)  # Wait for simulator to boot
            
            logger.info(f"iOS simulator started: {device_name}")
            return udid
        except Exception as e:
            logger.error(f"Failed to start iOS simulator: {e}")
            raise
    
    @staticmethod
    def start_android_emulator(avd_name: str) -> None:
        """
        Start an Android emulator.
        
        Args:
            avd_name: Name of the AVD to start
        """
        try:
            # Check if emulator is already running
            result = subprocess.run(
                ["adb", "devices"], capture_output=True, text=True
            )
            
            if avd_name not in result.stdout:
                logger.info(f"Starting Android emulator: {avd_name}")
                
                # Use full path to emulator
                import os
                emulator_path = os.path.expanduser("~/Library/Android/sdk/emulator/emulator")
                
                # Start emulator in background
                subprocess.Popen(
                    [emulator_path, "-avd", avd_name, "-no-snapshot-load"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                
                # Wait for emulator to be ready
                logger.info("Waiting for emulator to boot...")
                max_wait = 120  # 2 minutes
                start_time = time.time()
                
                while time.time() - start_time < max_wait:
                    result = subprocess.run(
                        ["adb", "shell", "getprop", "sys.boot_completed"],
                        capture_output=True, text=True
                    )
                    if "1" in result.stdout:
                        logger.info(f"Android emulator ready: {avd_name}")
                        time.sleep(5)  # Additional wait for stability
                        return
                    time.sleep(5)
                
                raise TimeoutError(f"Emulator {avd_name} failed to start within {max_wait} seconds")
            else:
                logger.info(f"Android emulator already running: {avd_name}")
        except Exception as e:
            logger.error(f"Failed to start Android emulator: {e}")
            raise
    
    @staticmethod
    def create_appium_ios_driver(config: BrowserConfig) -> appium_webdriver.Remote:
        """
        Create Appium driver for iOS simulator.
        
        Args:
            config: BrowserConfig instance with browser settings
            
        Returns:
            Appium WebDriver instance for iOS
        """
        device_config = REAL_DEVICE_CONFIGS.get(config.device_name)
        
        if not device_config:
            raise ValueError(f"No real device configuration found for: {config.device_name}")
        
        # Start simulator if not running
        udid = device_config.get("udid")
        if udid:
            udid = DriverFactory.start_ios_simulator(config.device_name, udid)
        
        # Configure Appium options for iOS
        options = XCUITestOptions()
        options.platform_name = device_config["platformName"]
        options.platform_version = device_config["platformVersion"]
        options.device_name = device_config["deviceName"]
        options.automation_name = device_config["automationName"]
        options.browser_name = device_config["browserName"]
        
        if udid:
            options.udid = udid
        
        # Additional capabilities
        options.set_capability("newCommandTimeout", 300)
        options.set_capability("connectHardwareKeyboard", True)
        
        logger.info(f"Creating Appium iOS driver for {config.device_name}")
        driver = appium_webdriver.Remote(
            config.appium_server_url,
            options=options
        )
        
        # Set timeouts
        driver.implicitly_wait(config.implicit_wait)
        
        logger.info(f"Appium iOS driver created for {config.device_name}")
        return driver
    
    @staticmethod
    def create_appium_android_driver(config: BrowserConfig) -> appium_webdriver.Remote:
        """
        Create Appium driver for Android emulator.
        
        Args:
            config: BrowserConfig instance with browser settings
            
        Returns:
            Appium WebDriver instance for Android
        """
        device_config = REAL_DEVICE_CONFIGS.get(config.device_name)
        
        if not device_config:
            raise ValueError(f"No real device configuration found for: {config.device_name}")
        
        # Start emulator if not running
        avd_name = device_config.get("avd")
        if avd_name:
            DriverFactory.start_android_emulator(avd_name)
        
        # Configure Appium options for Android
        options = UiAutomator2Options()
        options.platform_name = device_config["platformName"]
        options.platform_version = device_config.get("platformVersion", "")
        options.device_name = device_config["deviceName"]
        options.automation_name = device_config["automationName"]
        options.browser_name = device_config["browserName"]
        
        if avd_name:
            options.avd = avd_name
        
        # Additional capabilities
        options.set_capability("newCommandTimeout", 300)
        options.set_capability("avdLaunchTimeout", 120000)
        options.set_capability("avdReadyTimeout", 120000)
        options.set_capability("chromedriverAutodownload", True)
        
        # Auto-install Appium helper apps
        options.set_capability("skipServerInstallation", False)
        options.set_capability("skipDeviceInitialization", False)
        options.set_capability("skipUnlock", False)
        
        # Ensure Settings and UiAutomator2 apps are installed
        options.set_capability("ensureWebviewsHavePages", True)
        options.set_capability("nativeWebScreenshot", True)
        
        logger.info(f"Creating Appium Android driver for {config.device_name}")
        driver = appium_webdriver.Remote(
            config.appium_server_url,
            options=options
        )
        
        # Set timeouts
        driver.implicitly_wait(config.implicit_wait)
        
        logger.info(f"Appium Android driver created for {config.device_name}")
        return driver
    
    @staticmethod
    def create_chrome_driver(config: BrowserConfig) -> webdriver.Chrome:
        """
        Create Chrome WebDriver configured for mobile emulation.
        
        Args:
            config: BrowserConfig instance with browser settings
            
        Returns:
            Configured Chrome WebDriver instance
        """
        chrome_options = ChromeOptions()
        
        # Get device preset if available
        device_preset = DEVICE_PRESETS.get(config.device_name)
        
        if device_preset:
            # Configure mobile emulation with custom device metrics
            mobile_emulation = {
                "deviceMetrics": {
                    "width": device_preset["viewport"]["width"],
                    "height": device_preset["viewport"]["height"],
                    "pixelRatio": device_preset["pixel_ratio"]
                },
                "userAgent": device_preset["user_agent"]
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        else:
            # Fallback to generic mobile settings
            chrome_options.add_argument(f'--window-size={config.window_size[0]},{config.window_size[1]}')
            
        # Additional Chrome options
        if config.headless:
            chrome_options.add_argument('--headless=new')
            
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Performance optimizations
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Create driver
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set timeouts
        driver.implicitly_wait(config.implicit_wait)
        driver.set_page_load_timeout(config.page_load_timeout)
        driver.set_script_timeout(config.script_timeout)
        
        logger.info(f"Chrome driver created for {config.device_name} on {config.platform}")
        return driver
    
    @staticmethod
    def create_safari_driver(config: BrowserConfig) -> webdriver.Safari:
        """
        Create Safari WebDriver configured for mobile emulation.
        
        Args:
            config: BrowserConfig instance with browser settings
            
        Returns:
            Configured Safari WebDriver instance
        """
        safari_options = SafariOptions()
        
        # Safari-specific options
        safari_options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
        
        # Create driver
        service = SafariService()
        driver = webdriver.Safari(service=service, options=safari_options)
        
        # Set window size for mobile simulation
        driver.set_window_size(config.window_size[0], config.window_size[1])
        
        # Set timeouts
        driver.implicitly_wait(config.implicit_wait)
        driver.set_page_load_timeout(config.page_load_timeout)
        driver.set_script_timeout(config.script_timeout)
        
        # Inject user agent via JavaScript for iOS simulation
        device_preset = DEVICE_PRESETS.get(config.device_name)
        if device_preset:
            user_agent = device_preset["user_agent"]
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
        
        logger.info(f"Safari driver created for {config.device_name} on {config.platform}")
        return driver
    
    @staticmethod
    def create_driver(config: BrowserConfig) -> Union[webdriver.Remote, appium_webdriver.Remote]:
        """
        Create appropriate WebDriver based on configuration.
        
        Args:
            config: BrowserConfig instance with browser settings
            
        Returns:
            Configured WebDriver instance (Selenium or Appium)
            
        Raises:
            ValueError: If browser type is not supported
        """
        # Use real device/emulator if specified
        if config.use_real_device:
            logger.info(f"Creating driver for real device/emulator: {config.device_name}")
            if config.platform.lower() == "ios":
                return DriverFactory.create_appium_ios_driver(config)
            elif config.platform.lower() == "android":
                return DriverFactory.create_appium_android_driver(config)
            else:
                raise ValueError(f"Unsupported platform for real device: {config.platform}")
        
        # Use browser emulation (original behavior)
        browser = config.browser_name.lower()
        
        if browser == "chrome":
            return DriverFactory.create_chrome_driver(config)
        elif browser == "safari":
            return DriverFactory.create_safari_driver(config)
        else:
            raise ValueError(f"Unsupported browser: {browser}. Use 'chrome' or 'safari'")
    
    @staticmethod
    def quit_driver(driver: Optional[webdriver.Remote]) -> None:
        """
        Safely quit the WebDriver.
        
        Args:
            driver: WebDriver instance to quit
        """
        if driver:
            try:
                driver.quit()
                logger.info("Driver closed successfully")
            except Exception as e:
                logger.error(f"Error closing driver: {e}")
