# Quick Element Inspection Guide

## 🚀 Quick Start - 3 Methods

### Method 1: Chrome Remote Debugging (Android) - RECOMMENDED

```bash
# Step 1: Run your test
pytest tests/twitch/test_twitch.py -v -s

# Step 2: While test is running, open Chrome browser
# Step 3: Navigate to: chrome://inspect/#devices
# Step 4: Click "inspect" next to your page
# Step 5: Use DevTools as normal!
```

### Method 2: Safari Web Inspector (iOS)

```bash
# Step 1: Run your test on iOS simulator
pytest tests/twitch/test_twitch.py --platform iOS -v -s

# Step 2: Open Safari
# Step 3: Develop menu → [Your Simulator] → [Page]
# Step 4: Use Web Inspector!
```

### Method 3: Keep Browser Open

```bash
# Run debug test that pauses
DEBUG=true pytest tests/twitch/test_twitch_debug.py::TestTwitchDebug::test_keep_browser_open -v -s
```

---

## 📱 Available Debug Tests

### 1. Full Page Inspection
```bash
DEBUG=true pytest tests/twitch/test_twitch_debug.py::TestTwitchDebug::test_inspect_twitch_page -v -s
```
**Features:**
- Lists all buttons, links, inputs
- Shows element properties
- Saves page source
- Pauses for manual inspection

### 2. Popup Inspection
```bash
DEBUG=true pytest tests/twitch/test_twitch_debug.py::TestTwitchDebug::test_inspect_popup -v -s
```
**Features:**
- Waits for popup
- Tries multiple selector strategies
- Saves before/after page source
- Shows what worked

### 3. Interactive Selector Discovery
```bash
pytest tests/twitch/test_twitch_debug.py::test_interactive_popup_discovery -v -s
```
**Features:**
- Tests 7+ different selector strategies
- Shows which ones work
- Great for finding hard-to-locate elements

### 4. Element Hierarchy
```bash
pytest tests/twitch/test_twitch_debug.py::TestTwitchDebug::test_element_hierarchy -v -s
```
**Features:**
- Prints DOM tree structure
- Shows element relationships
- Helps understand page structure

---

## 🛠️ Using Helper Functions in Your Tests

### Import the utilities
```python
from tests.utils import (
    inspect_page_elements,
    save_page_source,
    debug_pause,
    find_by_text_android,
    find_by_text_ios
)
```

### Example Usage

```python
def test_with_inspection(driver, test_config):
    driver.get(test_config.base_url)
    
    # Inspect all elements on page
    inspect_page_elements(driver)
    
    # Save page source
    save_page_source(driver, "my_page.xml")
    
    # Find element by text (Android)
    element = find_by_text_android(driver, "Keep using web")
    if element:
        element.click()
    
    # Pause if in debug mode
    debug_pause(driver, "After action - inspect changes")
```

---

## 🔧 Debug Mode

Set `DEBUG=true` to enable automatic pauses:

```bash
# Linux/Mac
DEBUG=true pytest tests/twitch/test_twitch.py -v -s

# Windows PowerShell
$env:DEBUG="true"; pytest tests/twitch/test_twitch.py -v -s

# Windows CMD
set DEBUG=true && pytest tests/twitch/test_twitch.py -v -s
```

---

## 📝 Common Selector Strategies

### XPath (Works everywhere)
```python
driver.find_element(By.XPATH, "//button[contains(text(), 'Keep using web')]")
driver.find_element(By.XPATH, "//*[@id='my-button']")
```

### CSS Selector (Web contexts)
```python
driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
driver.find_element(By.CSS_SELECTOR, ".keep-web-button")
```

### Android UiAutomator (Android native/hybrid)
```python
from appium.webdriver.common.appiumby import AppiumBy

driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 
    'new UiSelector().textContains("Keep using web")')
driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.example:id/button")')
```

### iOS Predicate (iOS native/hybrid)
```python
from appium.webdriver.common.appiumby import AppiumBy

driver.find_element(AppiumBy.IOS_PREDICATE, 
    'label CONTAINS "Keep using web"')
driver.find_element(AppiumBy.IOS_PREDICATE,
    'name == "MyButton"')
```

---

## 💡 Pro Tips

### 1. Save Page Source for Offline Analysis
```python
from tests.utils import save_page_source
save_page_source(driver, "my_page.xml")
# Opens in reports/ directory with timestamp
```

### 2. Highlight Elements While Testing
```python
from tests.utils import highlight_element
element = driver.find_element(By.ID, "my-button")
highlight_element(driver, element, duration=3)  # Red border for 3 seconds
```

### 3. Take Screenshots
```python
from tests.utils import take_screenshot
take_screenshot(driver, "my_screenshot")
# Saved to reports/screenshots/ with timestamp
```

### 4. Check If Element Is Visible
```python
from tests.utils import is_element_in_viewport
element = driver.find_element(By.ID, "my-button")
if is_element_in_viewport(driver, element):
    element.click()
```

---

## 🐛 Troubleshooting

### Can't see device in chrome://inspect
```bash
# Check ADB connection
adb devices

# Restart ADB
adb kill-server
adb start-server
```

### Safari Inspector not showing
```bash
# Enable Web Inspector in Simulator
xcrun simctl spawn booted defaults write com.apple.Safari WebKitDeveloperExtrasEnabled -bool true
```

### Element not found
1. Use `save_page_source()` to examine HTML
2. Use `inspect_page_elements()` to list all elements
3. Try `test_interactive_popup_discovery` to test multiple selectors
4. Use `debug_pause()` to manually inspect with DevTools

---

## 📚 More Information

See [ELEMENT_INSPECTION_GUIDE.md](./ELEMENT_INSPECTION_GUIDE.md) for detailed documentation.
