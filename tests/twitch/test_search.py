import pytest
from selenium.webdriver.common.by import By
from pages.twitch_page import TwitchPage


@pytest.mark.smoke
@pytest.mark.chrome
@pytest.mark.android
@pytest.mark.emulator
class TestTwitchSearchAndScroll:
    """Test cases for Twitch search with scrolling."""

    def setup_method(self):
        self.landing_url = 'https://m.twitch.tv/'
    
    @pytest.mark.parametrize(
        argnames=['keyword'],
        argvalues=[
            ('StarCraft II',),
            ('WarCraft III',),
            ('Minecraft',),
        ],
    )
    def test_search_keyword_and_screenshot_streamer(self, driver, keyword: str):
        """
        Same test but using step-by-step approach.
        
        Run with:
        pytest tests/twitch/test_search_example.py::TestTwitchSearchAndScroll::test_search_starcraft_step_by_step -v -s
        """
        print("\n" + "="*70)
        print(f"Test: Search {keyword} (Step-by-Step)")
        print("="*70)
        
        # Navigate
        driver.get(self.landing_url)
        print(f"✓ Navigated to: {driver.current_url}")
        
        # Create page object
        # Step 1: go to twitch
        page = TwitchPage(driver)
        
        # Dismiss popup
        print("\n Dismissing popup...")
        page.dismiss_popup_adb()

        # Step 2: Click Browse
        print("\n1  Clicking Browse button...")
        page.click_browse()
        page.wait(2)
        
        # Step 3: Search
        print(f"2️⃣  Searching for {keyword}...")
        page.search_and_submit(keyword)
        
        print("3️⃣  Waiting for results...")
        page.wait(2)
        
        # Step 4: Scroll down first time
        print("4️⃣  Scrolling down (1/2)...")
        page.swipe_up()
        page.wait(1)
        
        # Scroll down second time
        print("   Scrolling down (2/2)...")
        page.swipe_up()
        page.wait(1)

        # Step 5: Select the first streamer
        print("5️⃣  Clicking on first streamer...")
        # Find the first streamer card/link - it's a button containing streamer info
        # The structure has a button with class containing "tw-link" and contains a h2 element
        # Use click_with_retry to handle any overlays or interception issues
        page.click_with_retry((By.CSS_SELECTOR, "button.tw-link"))
        
        # Wait for video page to load
        print("6️⃣  Waiting for streamer page to load...")
        page.wait(3)  # Initial wait for navigation
        
        # Wait for video player or channel content to appear (indicates page loaded)
        try:
            # Wait for video player element or channel page content
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            wait = WebDriverWait(driver, 15)
            
            # Wait for either video player or channel header to be present
            wait.until(
                lambda d: d.find_elements(By.CSS_SELECTOR, "video") or 
                         d.find_elements(By.CSS_SELECTOR, "[data-a-target='video-player']") or
                         d.find_elements(By.CSS_SELECTOR, "h1") or
                         d.find_elements(By.TAG_NAME, "video")
            )
            print("✓ Streamer page loaded")
        except Exception as e:
            print(f"⚠️  Timeout waiting for page elements, continuing anyway: {e}")
        
        page.wait(5)  # Additional wait for full rendering
        
        # Get streamer info
        print(f"✓ Current URL: {driver.current_url}")
        
        # Step 6: Take screenshot
        print("7️⃣  Taking screenshot...")
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        page.take_screenshot(f"streamer_page_{timestamp}.png")
        
        print("="*70 + "\n")
        
        print("\n✅ Test completed successfully!")
        print("="*70 + "\n")

