#!/bin/bash
#
# Quick start script for testing on real emulators/simulators
# Usage: ./run-emulator-tests.sh [ios|android] [device-name]
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Appium is installed
check_appium() {
    if ! command -v appium &> /dev/null; then
        print_error "Appium is not installed!"
        print_info "Install with: npm install -g appium"
        exit 1
    fi
    print_success "Appium is installed"
}

# Check if Appium is running
check_appium_running() {
    if curl -s http://localhost:4723/status > /dev/null 2>&1; then
        print_success "Appium server is running"
        return 0
    else
        print_warning "Appium server is not running"
        return 1
    fi
}

# Start Appium server
start_appium() {
    print_info "Starting Appium server..."
    # Start with ChromeDriver auto-download enabled for Android support
    appium --allow-insecure chromedriver_autodownload > appium.log 2>&1 &
    APPIUM_PID=$!
    
    # Wait for Appium to start
    sleep 5
    
    if check_appium_running; then
        print_success "Appium server started (PID: $APPIUM_PID)"
        echo $APPIUM_PID > .appium.pid
    else
        print_error "Failed to start Appium server"
        print_info "Check appium.log for details"
        exit 1
    fi
}

# Stop Appium server
stop_appium() {
    if [ -f .appium.pid ]; then
        PID=$(cat .appium.pid)
        if ps -p $PID > /dev/null 2>&1; then
            print_info "Stopping Appium server (PID: $PID)..."
            kill $PID
            rm .appium.pid
            print_success "Appium server stopped"
        fi
    fi
}

# Print available devices
show_devices() {
    echo ""
    print_info "Available iOS Simulators:"
    echo "  - iPhone 16 Pro"
    echo "  - iPhone SE (3rd generation)"
    echo "  - iPad Pro 11-inch (M4)"
    echo ""
    print_info "Available Android Emulators:"
    echo "  - Medium_Phone_API_35"
    echo "  - Small_Phone_API_35"
    echo "  - my_emulator"
    echo ""
}

# Show usage
show_usage() {
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  start               Start Appium server"
    echo "  stop                Stop Appium server"
    echo "  test-ios [device]   Run tests on iOS simulator"
    echo "  test-android [device] Run tests on Android emulator"
    echo "  devices             Show available devices"
    echo "  help                Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 test-ios \"iPhone SE (3rd generation)\""
    echo "  $0 test-android Medium_Phone_API_35"
    echo ""
}

# Main script
main() {
    case "${1:-help}" in
        start)
            check_appium
            if check_appium_running; then
                print_warning "Appium is already running"
            else
                start_appium
            fi
            ;;
        
        stop)
            stop_appium
            ;;
        
        test-ios)
            check_appium
            if ! check_appium_running; then
                start_appium
            fi
            
            DEVICE="${2:-iPhone SE (3rd generation)}"
            print_info "Running tests on iOS simulator: $DEVICE"
            
            uv run pytest tests/test_cases/test_real_emulators.py \
                --use-real-device \
                --platform=iOS \
                --device="$DEVICE" \
                -v \
                -m "emulator and ios"
            
            print_success "iOS tests completed!"
            ;;
        
        test-android)
            check_appium
            if ! check_appium_running; then
                start_appium
            fi
            
            DEVICE="${2:-Medium_Phone_API_35}"
            print_info "Running tests on Android emulator: $DEVICE"
            
            uv run pytest tests/twitch \
                --use-real-device \
                --platform=Android \
                --device="$DEVICE" \
                -s \
                -v
            
            print_success "Android tests completed!"
            ;;
        
        devices)
            show_devices
            ;;
        
        help|--help|-h)
            show_usage
            ;;
        
        *)
            print_error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

# Trap SIGINT and SIGTERM to cleanup
trap 'print_info "Cleaning up..."; stop_appium; exit 1' INT TERM

main "$@"
