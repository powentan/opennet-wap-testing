# Element Inspection Guide for Mobile Testing

This guide covers multiple methods to inspect elements in mobile browsers launched by Selenium/Appium.

## Table of Contents
1. [Chrome DevTools for Android](#chrome-devtools-for-android)
2. [Safari Web Inspector for iOS](#safari-web-inspector-for-ios)
3. [Appium Inspector](#appium-inspector)
4. [Browser DevTools Mobile Emulation](#browser-devtools-mobile-emulation)
5. [Programmatic Element Discovery](#programmatic-element-discovery)

---

## 1. Chrome DevTools for Android

### For Real Android Devices/Emulators

**Setup:**
1. Launch your test so the browser/app is running
2. Open Chrome on your desktop
3. Navigate to `chrome://inspect/#devices`
4. You should see your device/emulator listed

**Usage:**
- Click "inspect" next to the page you want to inspect
- Use Chrome DevTools as normal (inspect element, view DOM, console, etc.)
- Changes are reflected in real-time on the device

**In Your Test Code:**
```python
# Add a pause to keep the browser open for inspection
def test_inspect_elements(driver, test_config):
    driver.get(test_config.base_url)
    page = TwitchPage(driver)
    
    # Keep browser open for inspection
    input("Press Enter to continue after inspection...")
```

### Command to Keep Browser Open:
```bash
# Run test and add breakpoint
pytest tests/twitch/test_twitch.py::TestTwitch::test_search_functionality -v --capture=no
```

---

## 2. Safari Web Inspector for iOS

### For Real iOS Simulators/Devices

**Setup:**
1. On Mac, enable Developer menu in Safari:
   - Safari → Preferences → Advanced → "Show Develop menu in menu bar"
2. Launch your test on iOS Simulator/Device
3. In Safari's Develop menu, you'll see your simulator/device listed

**Usage:**
- Develop → [Your Device/Simulator] → [Page Title]
- Safari Web Inspector opens with full inspection capabilities
- View DOM, console, network, resources, etc.

**Enable Web Inspector in iOS Simulator:**
```bash
# For iOS Simulator
xcrun simctl spawn booted defaults write com.apple.Safari WebKitDeveloperExtrasEnabled -bool true
```

---

## 3. Appium Inspector

### Installation:
```bash
# Download from GitHub releases
# https://github.com/appium/appium-inspector/releases

# Or install via npm
npm install -g appium-inspector
```

### Usage:

**Step 1: Start Appium Server**
```bash
appium
```

**Step 2: Configure Inspector Session**

Open Appium Inspector and set up capabilities:

For Android Chrome:
```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:deviceName": "emulator-5554",
  "appium:browserName": "Chrome"
}
```

For iOS Safari:
```json
{
  "platformName": "iOS",
  "appium:automationName": "XCUITest",
  "appium:deviceName": "iPhone 14 Pro",
  "appium:platformVersion": "16.0",
  "appium:browserName": "Safari"
}
```

**Step 3: Attach to Running Session**

To inspect during a test, get the session ID and attach:

```python
# In your test
def test_with_inspection(driver):
    driver.get("https://www.twitch.tv")
    
    # Print session ID
    session_id = driver.session_id
    print(f"\nSession ID: {session_id}")
    print(f"Capabilities: {driver.capabilities}")
    
    # Keep session alive for inspection
    input("Attach Appium Inspector and press Enter...")
```

---

## 4. Browser DevTools Mobile Emulation

### For Browser Emulation Mode (Recommended for Quick Inspection)

**Chrome:**
1. Run your test
2. While browser is open, press `F12` or `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows)
3. Click the device toolbar icon or press `Cmd+Shift+M` (Mac) / `Ctrl+Shift+M` (Windows)
4. Inspect elements as normal

**Keep Browser Open During Test:**
```python
import time

def test_with_devtools(driver, test_config):
    driver.get(test_config.base_url)
    
    # Method 1: Simple sleep (not ideal)
    time.sleep(60)  # Browser stays open for 60 seconds
    
    # Method 2: Interactive pause (recommended)
    input("Press Enter after inspection...")
    
    # Method 3: Python debugger
    import pdb; pdb.set_trace()
```

---

## 5. Programmatic Element Discovery

### Using Helper Scripts

Create a helper function to discover elements:

```python
# Add to tests/utils.py or create a new helper file

from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy

def inspect_page_elements(driver):
    """Print all interactive elements on the page."""
    print("\n=== Page Inspection ===")
    
    # Get page source
    print(f"\nPage URL: {driver.current_url}")
    print(f"Page Title: {driver.title}")
    
    # Find common interactive elements
    locators = {
        "Buttons": (By.TAG_NAME, "button"),
        "Links": (By.TAG_NAME, "a"),
        "Inputs": (By.TAG_NAME, "input"),
        "Text Areas": (By.TAG_NAME, "textarea"),
    }
    
    for element_type, locator in locators.items():
        try:
            elements = driver.find_elements(*locator)
            print(f"\n{element_type} found: {len(elements)}")
            for i, elem in enumerate(elements[:5], 1):  # Show first 5
                text = elem.text or elem.get_attribute("value") or elem.get_attribute("placeholder")
                tag = elem.tag_name
                print(f"  {i}. <{tag}> text='{text[:50]}' visible={elem.is_displayed()}")
        except Exception as e:
            print(f"  Error finding {element_type}: {e}")

def find_by_text_android(driver, text):
    """Find elements by text using UiAutomator (Android)."""
    selectors = [
        f'new UiSelector().text("{text}")',
        f'new UiSelector().textContains("{text}")',
        f'new UiSelector().textMatches(".*{text}.*")',
        f'new UiSelector().descriptionContains("{text}")',
    ]
    
    for selector in selectors:
        try:
            element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)
            print(f"✓ Found with: {selector}")
            return element
        except:
            print(f"✗ Not found with: {selector}")
    
    return None

def save_page_source(driver, filename="page_source.xml"):
    """Save page source for offline inspection."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"Page source saved to: {filename}")
```

### Usage in Tests:

```python
from tests.utils import inspect_page_elements, save_page_source

def test_discover_elements(driver, test_config):
    driver.get("https://www.twitch.tv")
    
    # Wait for page load
    time.sleep(3)
    
    # Inspect elements
    inspect_page_elements(driver)
    
    # Save page source
    save_page_source(driver, "twitch_page.xml")
    
    # Try to find specific element
    from tests.utils import find_by_text_android
    element = find_by_text_android(driver, "Keep using web")
```

---

## 6. Debugging Techniques

### Add Debug Mode to Tests

Create a debug helper:

```python
# Add to conftest.py or a utils file

import os

def is_debug_mode():
    """Check if running in debug mode."""
    return os.getenv("DEBUG", "false").lower() == "true"

def debug_pause(driver, message="Paused for inspection"):
    """Pause execution if in debug mode."""
    if is_debug_mode():
        print(f"\n{'='*50}")
        print(f"🔍 {message}")
        print(f"Session ID: {driver.session_id}")
        print(f"Current URL: {driver.current_url}")
        print(f"{'='*50}\n")
        input("Press Enter to continue...")
```

### Run Tests in Debug Mode:

```bash
# Set DEBUG environment variable
DEBUG=true pytest tests/twitch/test_twitch.py -v -s

# Or inline
env DEBUG=true pytest tests/twitch/test_twitch.py::TestTwitch::test_search_functionality -v -s
```

---

## 7. Quick Reference Commands

### Keep Browser Open After Test:
```python
# Option 1: Add to your test
time.sleep(300)  # Keep open for 5 minutes

# Option 2: Use debugger
import pdb; pdb.set_trace()

# Option 3: Use pytest --pdb flag
pytest tests/twitch/test_twitch.py --pdb

# Option 4: Interactive input
input("Press Enter to close browser...")
```

### Find Elements by Different Strategies:
```python
# CSS Selector
element = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

# XPath
element = driver.find_element(By.XPATH, "//button[contains(text(), 'Keep using web')]")

# Android UiAutomator
element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
    'new UiSelector().textContains("Keep using web")')

# iOS Predicate
element = driver.find_element(AppiumBy.IOS_PREDICATE, 
    'label CONTAINS "Keep using web"')

# Accessibility ID
element = driver.find_element(By.ID, "keep-web-button")
```

---

## 8. Best Practices

1. **Use Chrome Remote Debugging** for Android - Most reliable and feature-rich
2. **Use Safari Web Inspector** for iOS - Native Apple tooling
3. **Save Page Source** when element inspection is difficult
4. **Use Appium Inspector** for native app contexts or hybrid apps
5. **Add Debug Flags** to your tests for easy inspection mode
6. **Screenshot on Failure** - Already configured in conftest.py
7. **Log Element Hierarchies** - Use helper functions to print element trees

---

## 9. Troubleshooting

### Can't See Device in chrome://inspect

```bash
# Check ADB connection
adb devices

# Restart ADB server
adb kill-server
adb start-server

# Check Chrome flags
chrome://flags/#remote-debugging
```

### Safari Inspector Not Showing

```bash
# Enable Web Inspector in Simulator
xcrun simctl spawn booted defaults write com.apple.Safari WebKitDeveloperExtrasEnabled -bool true

# Restart Safari
killall mobilesafari
```

### Appium Inspector Can't Connect

```bash
# Verify Appium is running
curl http://localhost:4723/status

# Check session is active
# Session must be running before attaching inspector
```

---

## Example: Complete Inspection Workflow

```python
# tests/twitch/test_twitch_debug.py

import pytest
import time
from pages.twitch_page import TwitchPage

@pytest.mark.debug
def test_inspect_twitch_popup(driver, test_config):
    """Test with inspection points for popup debugging."""
    
    print("\n" + "="*50)
    print("🔍 Debug Mode: Twitch Popup Inspection")
    print("="*50)
    
    # Navigate to page
    driver.get(test_config.base_url)
    
    print(f"\n✓ Navigated to: {driver.current_url}")
    print(f"✓ Session ID: {driver.session_id}")
    print("\n📱 Steps to inspect:")
    print("1. Open chrome://inspect/#devices (for Android)")
    print("2. Or use Safari Developer menu (for iOS)")
    print("3. Click 'inspect' on the page")
    
    # Wait for page load
    time.sleep(3)
    
    input("\n⏸️  Press Enter after you've opened DevTools...")
    
    # Save page source for offline inspection
    with open("debug_page_source.xml", "w") as f:
        f.write(driver.page_source)
    print("✓ Page source saved to: debug_page_source.xml")
    
    # Try to find popup
    page = TwitchPage(driver)
    
    print("\n🔍 Attempting to find popup...")
    input("⏸️  Press Enter to attempt popup dismissal...")
    
    page.dismiss_popup()
    
    print("\n✓ Test complete")
```

Run with:
```bash
pytest tests/twitch/test_twitch_debug.py::test_inspect_twitch_popup -v -s
```

