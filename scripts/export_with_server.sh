#!/bin/bash

# Photo Booth Export Helper Script
# Automatically starts dev server and runs export

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values (will be updated from dashboard configuration)
DASHBOARD_ID="portfolio_history_portrait"
MODE="light"
ASPECT_RATIO="3:4"
FORMAT="png"
DPI="300"
SCALE_FACTOR="3"
TICKER=""

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to read dashboard configuration and set defaults
get_dashboard_defaults() {
    local dashboard_id="$1"
    local config_file="$(dirname "$0")/../frontend/public/data/dashboards.json"

    if [ ! -f "$config_file" ]; then
        print_warning "Dashboard configuration not found: $config_file"
        print_warning "Using hardcoded defaults"
        return 1
    fi

    # Try to extract export_defaults for the specified dashboard
    if command -v jq >/dev/null 2>&1; then
        # Use jq if available (preferred)
        local dashboard_config=$(jq -r --arg id "$dashboard_id" '.dashboards[] | select(.id == $id) | .export_defaults' "$config_file" 2>/dev/null)

        if [ "$dashboard_config" != "null" ] && [ -n "$dashboard_config" ]; then
            # Extract specific values from export_defaults
            local aspect_ratio=$(echo "$dashboard_config" | jq -r '.aspect_ratio // empty' 2>/dev/null)
            local format=$(echo "$dashboard_config" | jq -r '.format // empty' 2>/dev/null)
            local dpi=$(echo "$dashboard_config" | jq -r '.dpi // empty' 2>/dev/null)

            # Update defaults if values exist in configuration
            [ -n "$aspect_ratio" ] && ASPECT_RATIO="$aspect_ratio"
            [ -n "$format" ] && FORMAT="$format"
            [ -n "$dpi" ] && DPI="$dpi"

            print_status "Using dashboard configuration defaults for: $dashboard_id"
            return 0
        fi
    else
        # Fallback: basic grep parsing (less reliable but works without jq)
        print_warning "jq not available, using basic configuration parsing"

        # Find the dashboard section and extract export_defaults
        local in_dashboard=false
        local in_export_defaults=false

        while IFS= read -r line; do
            # Check if we found the target dashboard
            if [[ "$line" == *"\"id\": \"$dashboard_id\""* ]]; then
                in_dashboard=true
                continue
            fi

            # If we're in the dashboard and find export_defaults
            if [ "$in_dashboard" = true ] && [[ "$line" == *"\"export_defaults\":"* ]]; then
                in_export_defaults=true
                continue
            fi

            # Extract values from export_defaults
            if [ "$in_export_defaults" = true ]; then
                if [[ "$line" == *"\"aspect_ratio\":"* ]]; then
                    local aspect_ratio=$(echo "$line" | sed 's/.*"aspect_ratio": *"\([^"]*\)".*/\1/')
                    [ -n "$aspect_ratio" ] && ASPECT_RATIO="$aspect_ratio"
                elif [[ "$line" == *"\"format\":"* ]]; then
                    local format=$(echo "$line" | sed 's/.*"format": *"\([^"]*\)".*/\1/')
                    [ -n "$format" ] && FORMAT="$format"
                elif [[ "$line" == *"\"dpi\":"* ]]; then
                    local dpi=$(echo "$line" | sed 's/.*"dpi": *\([0-9]*\).*/\1/')
                    [ -n "$dpi" ] && DPI="$dpi"
                elif [[ "$line" == *"}"* ]]; then
                    # End of export_defaults or dashboard
                    break
                fi
            fi

            # If we hit the next dashboard, stop
            if [ "$in_dashboard" = true ] && [[ "$line" == *"\"id\":"* ]] && [[ "$line" != *"\"$dashboard_id\""* ]]; then
                break
            fi

        done < "$config_file"

        print_status "Using basic configuration parsing for: $dashboard_id"
        return 0
    fi

    print_warning "No export_defaults found for dashboard: $dashboard_id"
    return 1
}

# Function to check if server is running
check_server() {
    if curl -s http://localhost:4321/photo-booth > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to start dev server
start_server() {
    print_status "Starting development server..."
    cd "$(dirname "$0")/../frontend"

    # Start server in background
    yarn dev > /tmp/astro_server.log 2>&1 &
    SERVER_PID=$!

    # Wait for server to be ready
    print_status "Waiting for server to be ready..."
    for i in {1..30}; do
        if check_server; then
            print_success "Development server is running at http://localhost:4321"
            return 0
        fi
        echo -n "."
        sleep 1
    done

    print_error "Server failed to start within 30 seconds"
    print_error "Check the log at /tmp/astro_server.log"
    cat /tmp/astro_server.log
    return 1
}

# Function to stop server
stop_server() {
    if [ ! -z "$SERVER_PID" ]; then
        print_status "Stopping development server (PID: $SERVER_PID)..."
        kill $SERVER_PID 2>/dev/null || true
        wait $SERVER_PID 2>/dev/null || true
        print_success "Development server stopped"
    fi
}

# Function to run export
run_export() {
    print_status "Running photo booth export..."
    print_status "Dashboard: $DASHBOARD_ID"
    print_status "Mode: $MODE"
    print_status "Aspect Ratio: $ASPECT_RATIO"
    print_status "Format: $FORMAT"
    print_status "DPI: $DPI"
    print_status "Scale Factor: ${SCALE_FACTOR}x"
    if [ -n "$TICKER" ]; then
        print_status "Ticker: $TICKER"
    fi

    cd "$(dirname "$0")"

    # Build command with optional ticker parameter
    cmd="python3 photo_booth_generator.py \
        --dashboard \"$DASHBOARD_ID\" \
        --mode \"$MODE\" \
        --aspect-ratio \"$ASPECT_RATIO\" \
        --format \"$FORMAT\" \
        --dpi \"$DPI\" \
        --scale-factor \"$SCALE_FACTOR\""

    if [ -n "$TICKER" ]; then
        cmd="$cmd --ticker \"$TICKER\""
    fi

    eval $cmd
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --dashboard ID        Dashboard ID (default: portfolio_history_portrait)"
    echo "  --mode MODE          Theme mode: light, dark, both (default: light)"
    echo "  --aspect-ratio RATIO  Aspect ratio: 16:9, 4:3, 3:4 (default: 3:4)"
    echo "  --format FORMAT      Export format: png, svg, both (default: png)"
    echo "  --dpi DPI            DPI setting: 150, 300, 600 (default: 300)"
    echo "  --scale-factor SCALE  Scale factor: 2, 3, 4 (default: 3)"
    echo "  --ticker TICKER      Ticker symbol for fundamental analysis (e.g., GOOGL, NVDA)"
    echo "  --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --dashboard portfolio_history_portrait --mode dark"
    echo "  $0 --dashboard fundamental_analysis --ticker NVDA --mode light"
    echo "  $0 --aspect-ratio 16:9 --format both --dpi 600"
}

# First pass: extract dashboard ID to load configuration defaults
temp_dashboard_id="$DASHBOARD_ID"
temp_args=("$@")
i=0
while [ $i -lt ${#temp_args[@]} ]; do
    if [ "${temp_args[$i]}" = "--dashboard" ] && [ $((i+1)) -lt ${#temp_args[@]} ]; then
        temp_dashboard_id="${temp_args[$((i+1))]}"
        break
    fi
    i=$((i+1))
done

# Load dashboard-specific configuration defaults
get_dashboard_defaults "$temp_dashboard_id"
DASHBOARD_ID="$temp_dashboard_id"

# Parse command line arguments (second pass for all parameters)
while [[ $# -gt 0 ]]; do
    case $1 in
        --dashboard)
            DASHBOARD_ID="$2"
            shift 2
            ;;
        --mode)
            MODE="$2"
            shift 2
            ;;
        --aspect-ratio)
            ASPECT_RATIO="$2"
            shift 2
            ;;
        --format)
            FORMAT="$2"
            shift 2
            ;;
        --dpi)
            DPI="$2"
            shift 2
            ;;
        --scale-factor)
            SCALE_FACTOR="$2"
            shift 2
            ;;
        --ticker)
            TICKER="$2"
            shift 2
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Trap to ensure server cleanup on exit
trap stop_server EXIT

# Main execution
print_status "Photo Booth Export Helper"
print_status "=========================="

# Check if server is already running
if check_server; then
    print_success "Development server is already running"
    SERVER_WAS_RUNNING=true
else
    print_status "Development server is not running"
    if ! start_server; then
        exit 1
    fi
    SERVER_WAS_RUNNING=false
fi

# Run the export
if run_export; then
    print_success "Export completed successfully!"
    print_success "Files saved to: data/outputs/photo-booth/"
else
    print_error "Export failed"
    exit 1
fi

# Only stop server if we started it
if [ "$SERVER_WAS_RUNNING" = false ]; then
    stop_server
else
    print_status "Leaving development server running (it was already running)"
fi

print_success "Done!"
