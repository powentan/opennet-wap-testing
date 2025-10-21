"""Base Page Object Model class."""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from typing import Tuple, Optional
import logging
import time

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize base page.
        
        Args:
            driver: WebDriver instance
            timeout: Default timeout for waits
        """
        self.driver = driver
        self.timeout = timeout
    
    def find_element(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        Find element with explicit wait.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout
            
        Returns:
            WebElement if found
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found within {wait_time}s: {locator}")
            raise
    
    def find_elements(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        Find multiple elements with explicit wait.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout
            
        Returns:
            List of WebElements
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        try:
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found within {wait_time}s: {locator}")
            return []
    
    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        Click on element with wait for clickability.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
        logger.debug(f"Clicked element: {locator}")
    
    def send_keys(self, locator: Tuple[str, str], text: str, timeout: Optional[int] = None):
        """
        Send keys to element.
        
        Args:
            locator: Tuple of (By, locator_string)
            text: Text to send
            timeout: Optional custom timeout
        """
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        logger.debug(f"Sent keys to element: {locator}")
    
    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        """
        Get text from element.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout
            
        Returns:
            Text content of element
        """
        element = self.find_element(locator, timeout)
        text = element.text
        logger.debug(f"Got text from element {locator}: {text}")
        return text
    
    def is_element_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout
            
        Returns:
            True if visible, False otherwise
        """
        try:
            wait_time = timeout or self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_to_disappear(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        Wait for element to disappear.
        
        Args:
            locator: Tuple of (By, locator_string)
            timeout: Optional custom timeout
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.invisibility_of_element_located(locator))
        logger.debug(f"Element disappeared: {locator}")
    
    def scroll_to_element(self, locator: Tuple[str, str]):
        """
        Scroll to element.
        
        Args:
            locator: Tuple of (By, locator_string)
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.debug(f"Scrolled to element: {locator}")
    
    def swipe_up(self, duration: int = 300):
        """
        Perform swipe up gesture (mobile scroll).
        
        Args:
            duration: Duration of swipe in milliseconds
        """
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] * 0.7
        end_y = size['height'] * 0.3
        
        self._swipe(start_x, int(start_y), start_x, int(end_y), duration)
        logger.debug("Performed swipe up")
    
    def swipe_down(self, duration: int = 100):
        """
        Perform swipe down gesture (mobile scroll).
        
        Args:
            duration: Duration of swipe in milliseconds
        """
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] * 0.3
        end_y = size['height'] * 0.7
        
        self._swipe(start_x, int(start_y), start_x, int(end_y), duration)
        logger.debug("Performed swipe down")
    
    def swipe_left(self, duration: int = 300):
        """
        Perform swipe left gesture.
        
        Args:
            duration: Duration of swipe in milliseconds
        """
        size = self.driver.get_window_size()
        start_x = size['width'] * 0.7
        start_y = size['height'] // 2
        end_x = size['width'] * 0.3
        
        self._swipe(int(start_x), start_y, int(end_x), start_y, duration)
        logger.debug("Performed swipe left")
    
    def swipe_right(self, duration: int = 300):
        """
        Perform swipe right gesture.
        
        Args:
            duration: Duration of swipe in milliseconds
        """
        size = self.driver.get_window_size()
        start_x = size['width'] * 0.3
        start_y = size['height'] // 2
        end_x = size['width'] * 0.7
        
        self._swipe(int(start_x), start_y, int(end_x), start_y, duration)
        logger.debug("Performed swipe right")
    
    def _swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int):
        """
        Perform swipe gesture using Actions API.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            duration: Duration in milliseconds
        """
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(duration / 1000)
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
    
    def tap(self, locator: Tuple[str, str]):
        """
        Perform tap gesture on element.
        
        Args:
            locator: Tuple of (By, locator_string)
        """
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.click(element).perform()
        logger.debug(f"Tapped element: {locator}")
    
    def long_press(self, locator: Tuple[str, str], duration: int = 1000):
        """
        Perform long press gesture on element.
        
        Args:
            locator: Tuple of (By, locator_string)
            duration: Duration in milliseconds
        """
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.click_and_hold(element).pause(duration / 1000).release().perform()
        logger.debug(f"Long pressed element: {locator} for {duration}ms")
    
    def take_screenshot(self, filename: str):
        """
        Take screenshot.
        
        Args:
            filename: Path to save screenshot
        """
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
    
    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url
    
    def get_title(self) -> str:
        """Get page title."""
        return self.driver.title
    
    def navigate_to(self, url: str):
        """
        Navigate to URL.
        
        Args:
            url: URL to navigate to
        """
        self.driver.get(url)
        logger.info(f"Navigated to: {url}")
    
    def refresh(self):
        """Refresh current page."""
        self.driver.refresh()
        logger.debug("Page refreshed")
    
    def go_back(self):
        """Navigate back."""
        self.driver.back()
        logger.debug("Navigated back")
    
    def go_forward(self):
        """Navigate forward."""
        self.driver.forward()
        logger.debug("Navigated forward")
    
    def take_screenshot(self, filename: str = None, directory: str = "screenshots") -> str:
        """
        Take a screenshot and save to file.
        
        Args:
            filename: Filename for screenshot (default: auto-generated with timestamp)
            directory: Directory to save screenshot (default: "screenshots")
            
        Returns:
            Full path to saved screenshot
            
        Example:
            page.take_screenshot("my_screenshot.png")
            page.take_screenshot()  # Auto-generated name
        """
        import os
        from datetime import datetime
        
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        # Ensure .png extension
        if not filename.endswith('.png'):
            filename += '.png'
        
        # Full path
        filepath = os.path.join(directory, filename)
        
        # Take screenshot
        self.driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")
        print(f"📸 Screenshot saved: {filepath}")
        
        return filepath
    
    def wait_for_page_load(self, timeout: int = 30):
        """
        Wait for page to fully load.
        
        Args:
            timeout: Maximum wait time in seconds
        """
        from selenium.webdriver.support.ui import WebDriverWait
        
        wait = WebDriverWait(self.driver, timeout)
        
        # Wait for document ready state
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        logger.debug("Page loaded")
        print("✓ Page loaded")
    
    def execute_script(self, script: str, *args):
        """
        Execute JavaScript.
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to script
            
        Returns:
            Result of script execution
        """
        return self.driver.execute_script(script, *args)
    
    def wait(self, seconds: float):
        """
        Wait for specified seconds.
        
        Args:
            seconds: Number of seconds to wait
        """
        time.sleep(seconds)
        logger.debug(f"Waited {seconds} seconds")
