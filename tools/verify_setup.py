#!/usr/bin/env python3
"""
Verification script for real emulator/simulator testing setup.
"""
import sys
import subprocess
import importlib.util

def check(name, test_func, fix_hint=""):
    """Check a condition and print result."""
    try:
        result = test_func()
        if result:
            print(f"✅ {name}")
            return True
        else:
            print(f"❌ {name}")
            if fix_hint:
                print(f"   Fix: {fix_hint}")
            return False
    except Exception as e:
        print(f"❌ {name}: {str(e)}")
        if fix_hint:
            print(f"   Fix: {fix_hint}")
        return False

def check_module(module_name):
    """Check if a Python module is installed."""
    return importlib.util.find_spec(module_name) is not None

def check_command(cmd):
    """Check if a command is available."""
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def main():
    print("\n🔍 Verifying Real Emulator/Simulator Testing Setup\n")
    
    checks = []
    
    # Python modules
    print("Python Dependencies:")
    checks.append(check("Pytest installed", 
                       lambda: check_module("pytest")))
    checks.append(check("Selenium installed", 
                       lambda: check_module("selenium")))
    checks.append(check("Appium Python Client installed", 
                       lambda: check_module("appium"),
                       "Run: uv sync"))
    
    # System tools
    print("\nSystem Tools:")
    checks.append(check("Appium server installed", 
                       lambda: check_command(["appium", "--version"]),
                       "Install: npm install -g appium"))
    checks.append(check("xcrun (iOS tools) available", 
                       lambda: check_command(["xcrun", "--version"])))
    checks.append(check("adb (Android tools) available", 
                       lambda: check_command(["adb", "--version"])))
    
    # Appium drivers
    print("\nAppium Drivers (optional but recommended):")
    try:
        result = subprocess.run(
            ["appium", "driver", "list"],
            capture_output=True, text=True, timeout=5
        )
        has_xcuitest = "xcuitest" in result.stdout.lower()
        has_uiautomator2 = "uiautomator2" in result.stdout.lower()
        
        checks.append(check("XCUITest driver (iOS)", 
                           lambda: has_xcuitest,
                           "Install: appium driver install xcuitest"))
        checks.append(check("UiAutomator2 driver (Android)", 
                           lambda: has_uiautomator2,
                           "Install: appium driver install uiautomator2"))
    except:
        print("⚠️  Could not check Appium drivers (Appium may not be running)")
    
    # Configuration files
    print("\nConfiguration Files:")
    import os
    checks.append(check("test_real_emulators.py exists", 
                       lambda: os.path.exists("tests/test_cases/test_real_emulators.py")))
    checks.append(check("run-emulator-tests.sh exists", 
                       lambda: os.path.exists("run-emulator-tests.sh")))
    checks.append(check("docs/ directory exists", 
                       lambda: os.path.exists("docs")))
    checks.append(check("Documentation complete", 
                       lambda: os.path.exists("docs/REAL_EMULATOR_GUIDE.md")))
    
    # Devices
    print("\nAvailable Devices:")
    try:
        result = subprocess.run(
            ["xcrun", "simctl", "list", "devices", "available"],
            capture_output=True, text=True, timeout=5
        )
        ios_count = result.stdout.count("iPhone") + result.stdout.count("iPad")
        print(f"   Found {ios_count} iOS simulators")
    except:
        print("   ⚠️  Could not list iOS simulators")
    
    try:
        result = subprocess.run(
            ["~/Library/Android/sdk/emulator/emulator", "-list-avds"],
            capture_output=True, text=True, timeout=5, shell=True
        )
        android_count = len([line for line in result.stdout.split('\n') if line.strip()])
        print(f"   Found {android_count} Android emulators")
    except:
        print("   ⚠️  Could not list Android emulators")
    
    # Summary
    print("\n" + "="*50)
    passed = sum(checks)
    total = len(checks)
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ Setup is complete! You're ready to test on real emulators!")
        print("\nNext steps:")
        print("  1. Start Appium: ./run-emulator-tests.sh start")
        print("  2. Run iOS test: ./run-emulator-tests.sh test-ios \"iPhone SE (3rd generation)\"")
        print("  3. Run Android test: ./run-emulator-tests.sh test-android Medium_Phone_API_35")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please review the messages above.")
        print("\nRead docs/SETUP_COMPLETE.md for detailed setup instructions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
