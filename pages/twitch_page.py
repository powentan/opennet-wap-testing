from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time


class TwitchPage(BasePage):
    
    # Locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    BROWSE_BUTTON = (By.XPATH, "//div[text()='Browse']")  # Browse navigation button
    VIDEO_CARDS = (By.CSS_SELECTOR, "[data-a-target='search-result-video']")  # Video search results
    
    def __init__(self, driver, timeout=10):
        """Initialize example page."""
        super().__init__(driver, timeout)
    
    def search_and_submit(self, query: str):
        """
        Type search query and submit by pressing Enter.
        
        This method finds the search input, types the query, and presses Enter
        to submit the search instead of clicking a search button.
        
        Args:
            query: Search query string (e.g., "StarCraft II")
            
        Example:
            page = TwitchPage(driver)
            page.search_and_submit("StarCraft II")
        """
        from selenium.webdriver.common.keys import Keys
        
        # Find search input
        search_input = self.find_element(self.SEARCH_INPUT)
        
        # Clear any existing text
        search_input.clear()
        
        # Type the query
        search_input.send_keys(query)
        
        # Press Enter to search
        search_input.send_keys(Keys.RETURN)
        
        print(f"Searched for: {query}")

    def click_browse(self):
        """
        Click the Browse button in navigation.
        
        Uses text-based XPath selector for reliability across different
        styled components. Includes retry logic and overlay handling.
        
        Example:
            page = TwitchPage(driver)
            page.click_browse()
        """
        # Try to click with retries and overlay handling
        self.click_with_retry(self.BROWSE_BUTTON)
    
    
    def dismiss_popup_adb(self, wait_time: int = 3, device_id: str = None):
        """
        Dismiss Twitch popup using ADB (Android Debug Bridge).
        
        This method uses ADB commands to find and tap the popup button directly,
        which can be faster and more reliable than WebDriver in some cases.
        
        Args:
            wait_time: Time to wait for popup to appear (default: 3 seconds)
            device_id: ADB device ID (optional, uses first device if not specified)
            
        Example:
            page = TwitchPage(driver)
            page.dismiss_popup_adb()  # Auto-detect device
            # or
            page.dismiss_popup_adb(device_id="emulator-5554")  # Specific device
        """
        import subprocess
        import re
        
        # Wait for popup to appear
        time.sleep(wait_time)
        
        try:
            # Build ADB command prefix
            adb_prefix = ["adb"]
            if device_id:
                adb_prefix.extend(["-s", device_id])
            
            # Dump UI hierarchy
            print("🔍 Searching for popup using ADB...")
            dump_cmd = adb_prefix + ["shell", "uiautomator", "dump", "/sdcard/window_dump.xml"]
            subprocess.run(dump_cmd, capture_output=True, text=True, timeout=10)
            
            # Pull the dump file
            pull_cmd = adb_prefix + ["shell", "cat", "/sdcard/window_dump.xml"]
            result = subprocess.run(pull_cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                print("❌ Failed to dump UI hierarchy")
                return
            
            xml_content = result.stdout
            
            # Search for "Keep using web" button in the XML
            # Pattern: text="Keep using web" bounds="[x1,y1][x2,y2]"
            pattern = r'text="[^"]*[Kk]eep[^"]*web[^"]*"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"'
            match = re.search(pattern, xml_content)
            
            if match:
                x1, y1, x2, y2 = map(int, match.groups())
                
                # Calculate center point
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                
                print(f"✓ Found popup button at coordinates: ({center_x}, {center_y})")
                
                # Tap using ADB
                tap_cmd = adb_prefix + ["shell", "input", "tap", str(center_x), str(center_y)]
                tap_result = subprocess.run(tap_cmd, capture_output=True, text=True, timeout=5)
                
                if tap_result.returncode == 0:
                    print("✓ Dismissed popup using ADB tap")
                else:
                    print("❌ ADB tap command failed")
            else:
                print("ℹ️  Popup not found in UI hierarchy (already dismissed?)")
                
        except subprocess.TimeoutExpired:
            print("⚠️  ADB command timeout")
        except Exception as e:
            print(f"⚠️  ADB dismissal failed: {e}")
    
    def dismiss_popup_adb_simple(self, x: int, y: int, wait_time: int = 3, device_id: str = None):
        """
        Dismiss popup using ADB tap at specific coordinates (simple/fast).
        
        Use this if you already know the popup button coordinates on your device.
        This is the fastest method as it doesn't need to search for the element.
        
        Args:
            x: X coordinate to tap
            y: Y coordinate to tap
            wait_time: Time to wait for popup to appear (default: 3 seconds)
            device_id: ADB device ID (optional)
            
        Example:
            page = TwitchPage(driver)
            # Tap at specific coordinates (e.g., center of button)
            page.dismiss_popup_adb_simple(540, 1500)
        """
        import subprocess
        
        # Wait for popup to appear
        time.sleep(wait_time)
        
        try:
            # Build ADB command
            adb_cmd = ["adb"]
            if device_id:
                adb_cmd.extend(["-s", device_id])
            adb_cmd.extend(["shell", "input", "tap", str(x), str(y)])
            
            # Execute tap
            result = subprocess.run(adb_cmd, capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                print(f"✓ Tapped at ({x}, {y}) using ADB")
            else:
                print(f"❌ ADB tap failed: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️  ADB tap failed: {e}")
    
    def dismiss_popup_hybrid(self, wait_time: int = 3, use_adb_fallback: bool = True):
        """
        Hybrid approach: Try Appium first, fallback to ADB if it fails.
        
        This is the most reliable method as it combines both approaches:
        1. First tries standard Appium/UiAutomator
        2. Falls back to ADB if Appium fails
        
        Args:
            wait_time: Time to wait for popup to appear (default: 3 seconds)
            use_adb_fallback: Enable ADB fallback (default: True)
            
        Example:
            page = TwitchPage(driver)
            page.dismiss_popup_hybrid()  # Try Appium, fallback to ADB
        """
        # Wait for popup
        time.sleep(wait_time)
        
        # Try Appium/UiAutomator first
        try:
            keep_web = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Keep using web")')
            keep_web.click()
            print("✓ Dismissed popup using Appium")
            return
        except Exception as e:
            print(f"ℹ️  Appium method failed: {e}")
        
        # Fallback to ADB if enabled
        if use_adb_fallback:
            print("🔄 Trying ADB fallback...")
            self.dismiss_popup_adb(wait_time=0)  # Already waited
    
    def click_with_retry(self, locator: tuple, max_attempts: int = 3, 
                        scroll_to_element: bool = True):
        """
        Click element with retry logic and overlay handling.
        
        This method handles common click issues:
        1. Waits for element to be clickable
        2. Scrolls element into view
        3. Tries JavaScript click if normal click fails
        4. Retries on ElementClickInterceptedException
        
        Args:
            locator: Element locator tuple (By, selector)
            max_attempts: Maximum retry attempts (default: 3)
            scroll_to_element: Scroll to element before clicking (default: True)
            
        Example:
            page.click_with_retry(page.BROWSE_BUTTON)
        """
        from selenium.common.exceptions import (
            ElementClickInterceptedException,
            StaleElementReferenceException
        )
        
        for attempt in range(max_attempts):
            try:
                # Wait for element to be present
                element = self.find_element(locator, timeout=10)
                
                # Scroll element into view
                if scroll_to_element:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                        element
                    )
                    time.sleep(0.5)  # Wait for smooth scroll
                
                # Wait a bit for any overlays to disappear
                time.sleep(0.5)
                
                # Try normal click first
                try:
                    element.click()
                    print(f"✓ Clicked element successfully")
                    return
                except ElementClickInterceptedException:
                    print(f"⚠️  Click intercepted, trying JavaScript click (attempt {attempt + 1}/{max_attempts})")
                    
                    # Try JavaScript click
                    self.driver.execute_script("arguments[0].click();", element)
                    print(f"✓ Clicked via JavaScript")
                    return
                    
            except StaleElementReferenceException:
                if attempt < max_attempts - 1:
                    print(f"⚠️  Element stale, retrying... (attempt {attempt + 1}/{max_attempts})")
                    time.sleep(1)
                    continue
                else:
                    raise
            except ElementClickInterceptedException:
                if attempt < max_attempts - 1:
                    print(f"⚠️  Click still intercepted, retrying... (attempt {attempt + 1}/{max_attempts})")
                    time.sleep(1)
                    continue
                else:
                    raise
        
        raise Exception(f"Failed to click element after {max_attempts} attempts")
    
