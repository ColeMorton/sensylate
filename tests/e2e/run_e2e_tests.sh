#!/usr/bin/env bash

# DASV E2E Test Execution Harness
# Main test runner for comprehensive end-to-end testing of the fundamental analysis pipeline
#
# Test Scenarios:
#   1. Full E2E success flow
#   2. Validation fail then retry success
#   3. Phase confidence failure with retry logic
#   4. Confidence parsing failure with retry
#
# Usage: ./run_e2e_tests.sh [options]
#   -s, --scenario SCENARIO   Run specific scenario (1-4, or 'all')
#   -d, --debug              Enable debug output
#   -p, --preserve-on-fail   Preserve test environment on failure
#   -h, --help              Show help message

set -euo pipefail

# Script directory and imports
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Import test libraries
source "$SCRIPT_DIR/lib/test_utils.sh"
source "$SCRIPT_DIR/lib/test_assertions.sh"

# Configuration
readonly DEFAULT_TICKER="AAPL"
readonly TEST_DATE=$(date +%Y%m%d)
readonly TOTAL_SCENARIOS=4

# Color output for main script
readonly MAIN_RED='\033[0;31m'
readonly MAIN_GREEN='\033[0;32m'
readonly MAIN_YELLOW='\033[1;33m'
readonly MAIN_BLUE='\033[0;34m'
readonly MAIN_NC='\033[0m'

# Command line options
DEBUG_MODE=false
PRESERVE_ON_FAIL=false
RUN_SCENARIO="all"

# Test execution tracking
declare -a SCENARIO_RESULTS=()
TOTAL_SCENARIOS_RUN=0
PASSED_SCENARIOS=0
FAILED_SCENARIOS=0

# =============================================================================
# Command Line Processing
# =============================================================================

show_help() {
    cat << EOF
DASV E2E Test Suite

USAGE:
    $0 [OPTIONS]

OPTIONS:
    -s, --scenario SCENARIO    Run specific scenario (1-4, or 'all')
                              1: Full E2E success flow
                              2: Validation fail then retry success
                              3: Phase confidence failure with retry
                              4: Confidence parsing failure with retry

    -d, --debug               Enable debug output and preserve logs
    -p, --preserve-on-fail    Preserve test environments on failure
    -h, --help               Show this help message

EXAMPLES:
    $0                        # Run all test scenarios
    $0 -s 1                   # Run only scenario 1
    $0 -s all -d              # Run all scenarios with debug output
    $0 -s 2 -p                # Run scenario 2, preserve environment on failure

EOF
}

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -s|--scenario)
                RUN_SCENARIO="$2"
                shift 2
                ;;
            -d|--debug)
                DEBUG_MODE=true
                export TEST_DEBUG=true
                shift
                ;;
            -p|--preserve-on-fail)
                PRESERVE_ON_FAIL=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1" >&2
                show_help >&2
                exit 1
                ;;
        esac
    done

    # Validate scenario selection
    if [[ "$RUN_SCENARIO" != "all" ]] && ! [[ "$RUN_SCENARIO" =~ ^[1-4]$ ]]; then
        echo "Error: Invalid scenario '$RUN_SCENARIO'. Must be 1-4 or 'all'." >&2
        exit 1
    fi
}

# =============================================================================
# Test Scenario Implementations
# =============================================================================

# Test Case 1: Full E2E Success Flow
run_scenario_1_success() {
    local scenario="scenario_1_success"
    local test_name="E2E_FULL_SUCCESS"

    echo -e "${MAIN_BLUE}=== Test Scenario 1: Full E2E Success Flow ===${MAIN_NC}"

    # Setup test environment
    local test_dir
    test_dir=$(setup_test_environment "success" "$DEFAULT_TICKER" "$TEST_DATE")

    # Set log file path based on test directory
    local TEST_LOG_FILE="$test_dir/logs/test_execution.log"

    # Reset test counters
    reset_test_counters

    # Execute the shell script
    local execution_success=false
    if execute_shell_script_with_timeout "$DEFAULT_TICKER" "$test_dir" "$TEST_TIMEOUT" "$TEST_LOG_FILE"; then
        execution_success=true
        log_test_event "INFO" "SCENARIO_1" "Shell script execution completed successfully"
    else
        log_test_event "ERROR" "SCENARIO_1" "Shell script execution failed"
    fi

    # Validate results
    local validation_success=false
    if $execution_success; then
        if assert_full_e2e_success "$test_name" "$test_dir" "$DEFAULT_TICKER" "$TEST_DATE"; then
            validation_success=true
            log_test_event "INFO" "SCENARIO_1" "E2E validation completed successfully"
        else
            log_test_event "ERROR" "SCENARIO_1" "E2E validation failed"
        fi
    fi

    # Additional specific validations for success scenario
    if $validation_success; then
        # Verify all DASV phases have high confidence scores
        local phases=("discovery" "analysis" "synthesis" "validation")
        for phase in "${phases[@]}"; do
            local output_path
            output_path=$(get_expected_output_path "$phase" "$test_dir" "$DEFAULT_TICKER" "$TEST_DATE")
            assert_dasv_phase_success "${test_name}_${phase}_high_confidence" "$phase" "$output_path" "9.0"
        done

        # Verify no retries were needed
        assert_file_not_exists "${test_name}_no_retries" "$test_dir/logs/retry_log.txt" "No retry log should exist for successful flow"
    fi

    # Record scenario result
    local overall_success
    if $execution_success && $validation_success && [[ $FAILED_ASSERTIONS -eq 0 ]]; then
        SCENARIO_RESULTS+=("SCENARIO_1: PASSED")
        overall_success=true
        echo -e "${MAIN_GREEN}✓ Scenario 1 PASSED${MAIN_NC}"
    else
        SCENARIO_RESULTS+=("SCENARIO_1: FAILED")
        overall_success=false
        echo -e "${MAIN_RED}✗ Scenario 1 FAILED${MAIN_NC}"
    fi

    # Print test summary
    print_test_summary "Scenario 1: Full E2E Success"

    # Cleanup
    cleanup_test_environment "$test_dir" "$PRESERVE_ON_FAIL"

    return $([ "$overall_success" = true ] && echo 0 || echo 1)
}

# Test Case 2: Validation Fail Then Retry Success
run_scenario_2_validation_retry() {
    local scenario="scenario_2_validation_retry"
    local test_name="VALIDATION_FAIL_RETRY_SUCCESS"

    echo -e "${MAIN_BLUE}=== Test Scenario 2: Validation Fail Then Retry Success ===${MAIN_NC}"

    # Setup test environment with validation failure on first attempt
    local test_dir
    test_dir=$(setup_test_environment "validation_fail_then_success" "$DEFAULT_TICKER" "$TEST_DATE")

    # Set log file path based on test directory
    local TEST_LOG_FILE="$test_dir/logs/test_execution.log"

    # Reset test counters
    reset_test_counters

    # Configure mock to fail validation initially, then succeed
    export TEST_VALIDATION_FAIL_FIRST=true

    # Execute the shell script
    local execution_success=false
    if execute_shell_script_with_timeout "$DEFAULT_TICKER" "$test_dir" "$TEST_TIMEOUT" "$TEST_LOG_FILE"; then
        execution_success=true
        log_test_event "INFO" "SCENARIO_2" "Shell script execution completed"
    else
        log_test_event "ERROR" "SCENARIO_2" "Shell script execution failed"
    fi

    # Validate retry mechanism was triggered
    local retry_success=false
    if $execution_success; then
        if assert_retry_mechanism "$test_name" "validation" "true" "$TEST_LOG_FILE"; then
            retry_success=true
            log_test_event "INFO" "SCENARIO_2" "Retry mechanism validation successful"
        else
            log_test_event "ERROR" "SCENARIO_2" "Retry mechanism validation failed"
        fi
    fi

    # Validate final success after retry
    local final_success=false
    if $retry_success; then
        if assert_full_e2e_success "$test_name" "$test_dir" "$DEFAULT_TICKER" "$TEST_DATE"; then
            final_success=true
            log_test_event "INFO" "SCENARIO_2" "Final E2E validation successful"
        else
            log_test_event "ERROR" "SCENARIO_2" "Final E2E validation failed"
        fi
    fi

    # Additional validations for retry scenario
    if $final_success; then
        # Check that validation phase ultimately succeeded
        local validation_path
        validation_path=$(get_expected_output_path "validation" "$test_dir" "$DEFAULT_TICKER" "$TEST_DATE")
        assert_dasv_phase_success "${test_name}_final_validation" "validation" "$validation_path" "9.0"

        # Check retry was logged properly
        assert_contains "${test_name}_retry_logged" "$(cat "$TEST_LOG_FILE")" "Retrying phase validation" "Retry attempt should be logged"
    fi

    # Record scenario result
    local overall_success
    if $execution_success && $retry_success && $final_success && [[ $FAILED_ASSERTIONS -eq 0 ]]; then
        SCENARIO_RESULTS+=("SCENARIO_2: PASSED")
        overall_success=true
        echo -e "${MAIN_GREEN}✓ Scenario 2 PASSED${MAIN_NC}"
    else
        SCENARIO_RESULTS+=("SCENARIO_2: FAILED")
        overall_success=false
        echo -e "${MAIN_RED}✗ Scenario 2 FAILED${MAIN_NC}"
    fi

    # Print test summary
    print_test_summary "Scenario 2: Validation Fail Then Retry Success"

    # Cleanup
    unset TEST_VALIDATION_FAIL_FIRST
    cleanup_test_environment "$test_dir" "$PRESERVE_ON_FAIL"

    return $([ "$overall_success" = true ] && echo 0 || echo 1)
}

# Test Case 3: Phase Confidence Failure With Retry Logic
run_scenario_3_confidence_fail() {
    local scenario="scenario_3_confidence_fail"
    local test_name="CONFIDENCE_FAIL_RETRY"

    echo -e "${MAIN_BLUE}=== Test Scenario 3: Phase Confidence Failure With Retry ===${MAIN_NC}"

    # Setup test environment with low confidence failure
    local test_dir
    test_dir=$(setup_test_environment "confidence_fail_retry" "$DEFAULT_TICKER" "$TEST_DATE")

    # Set log file path based on test directory
    local TEST_LOG_FILE="$test_dir/logs/test_execution.log"

    # Reset test counters
    reset_test_counters

    # Configure mock to return low confidence on first attempt for analysis phase
    export TEST_CONFIDENCE_FAIL_PHASE="analysis"
    export TEST_CONFIDENCE_FAIL_FIRST=true

    # Execute the shell script
    local execution_success=false
    if execute_shell_script_with_timeout "$DEFAULT_TICKER" "$test_dir" "$TEST_TIMEOUT" "$TEST_LOG_FILE"; then
        execution_success=true
        log_test_event "INFO" "SCENARIO_3" "Shell script execution completed"
    else
        log_test_event "ERROR" "SCENARIO_3" "Shell script execution failed"
    fi

    # Validate confidence failure detection and retry
    local confidence_retry_success=false
    if $execution_success; then
        if assert_retry_mechanism "$test_name" "analysis" "true" "$TEST_LOG_FILE"; then
            confidence_retry_success=true
            log_test_event "INFO" "SCENARIO_3" "Confidence failure retry validation successful"
        else
            log_test_event "ERROR" "SCENARIO_3" "Confidence failure retry validation failed"
        fi
    fi

    # Validate final success after confidence retry
    local final_success=false
    if $confidence_retry_success; then
        if assert_full_e2e_success "$test_name" "$test_dir" "$DEFAULT_TICKER" "$TEST_DATE"; then
            final_success=true
            log_test_event "INFO" "SCENARIO_3" "Final E2E validation after confidence retry successful"
        else
            log_test_event "ERROR" "SCENARIO_3" "Final E2E validation after confidence retry failed"
        fi
    fi

    # Additional validations for confidence failure scenario
    if $final_success; then
        # Verify that analysis phase ultimately has high confidence
        local analysis_path
        analysis_path=$(get_expected_output_path "analysis" "$test_dir" "$DEFAULT_TICKER" "$TEST_DATE")
        assert_dasv_phase_success "${test_name}_final_analysis" "analysis" "$analysis_path" "9.0"

        # Check confidence failure was logged
        assert_contains "${test_name}_confidence_fail_logged" "$(cat "$TEST_LOG_FILE")" "confidence score" "Confidence failure should be logged"
    fi

    # Record scenario result
    local overall_success
    if $execution_success && $confidence_retry_success && $final_success && [[ $FAILED_ASSERTIONS -eq 0 ]]; then
        SCENARIO_RESULTS+=("SCENARIO_3: PASSED")
        overall_success=true
        echo -e "${MAIN_GREEN}✓ Scenario 3 PASSED${MAIN_NC}"
    else
        SCENARIO_RESULTS+=("SCENARIO_3: FAILED")
        overall_success=false
        echo -e "${MAIN_RED}✗ Scenario 3 FAILED${MAIN_NC}"
    fi

    # Print test summary
    print_test_summary "Scenario 3: Phase Confidence Failure With Retry"

    # Cleanup
    unset TEST_CONFIDENCE_FAIL_PHASE TEST_CONFIDENCE_FAIL_FIRST
    cleanup_test_environment "$test_dir" "$PRESERVE_ON_FAIL"

    return $([ "$overall_success" = true ] && echo 0 || echo 1)
}

# Test Case 4: Confidence Parsing Failure With Retry
run_scenario_4_parse_fail() {
    local scenario="scenario_4_parse_fail"
    local test_name="CONFIDENCE_PARSE_FAIL_RETRY"

    echo -e "${MAIN_BLUE}=== Test Scenario 4: Confidence Parsing Failure With Retry ===${MAIN_NC}"

    # Setup test environment with parsing failure
    local test_dir
    test_dir=$(setup_test_environment "parse_fail_retry" "$DEFAULT_TICKER" "$TEST_DATE")

    # Set log file path based on test directory
    local TEST_LOG_FILE="$test_dir/logs/test_execution.log"

    # Reset test counters
    reset_test_counters

    # Configure mock to return malformed confidence on first attempt
    export TEST_PARSE_FAIL_PHASE="discovery"
    export TEST_PARSE_FAIL_FIRST=true

    # Execute the shell script
    local execution_success=false
    if execute_shell_script_with_timeout "$DEFAULT_TICKER" "$test_dir" "$TEST_TIMEOUT" "$TEST_LOG_FILE"; then
        execution_success=true
        log_test_event "INFO" "SCENARIO_4" "Shell script execution completed"
    else
        log_test_event "ERROR" "SCENARIO_4" "Shell script execution failed"
    fi

    # Validate parsing failure detection and retry
    local parse_retry_success=false
    if $execution_success; then
        if assert_retry_mechanism "$test_name" "discovery" "true" "$TEST_LOG_FILE"; then
            parse_retry_success=true
            log_test_event "INFO" "SCENARIO_4" "Parse failure retry validation successful"
        else
            log_test_event "ERROR" "SCENARIO_4" "Parse failure retry validation failed"
        fi
    fi

    # Validate final success after parsing retry
    local final_success=false
    if $parse_retry_success; then
        if assert_full_e2e_success "$test_name" "$test_dir" "$DEFAULT_TICKER" "$TEST_DATE"; then
            final_success=true
            log_test_event "INFO" "SCENARIO_4" "Final E2E validation after parse retry successful"
        else
            log_test_event "ERROR" "SCENARIO_4" "Final E2E validation after parse retry failed"
        fi
    fi

    # Additional validations for parsing failure scenario
    if $final_success; then
        # Verify discovery phase ultimately has valid confidence
        local discovery_path
        discovery_path=$(get_expected_output_path "discovery" "$test_dir" "$DEFAULT_TICKER" "$TEST_DATE")
        assert_dasv_phase_success "${test_name}_final_discovery" "discovery" "$discovery_path" "9.0"

        # Check parsing failure was logged
        assert_contains "${test_name}_parse_fail_logged" "$(cat "$TEST_LOG_FILE")" "Failed to parse confidence" "Parse failure should be logged"
    fi

    # Record scenario result
    local overall_success
    if $execution_success && $parse_retry_success && $final_success && [[ $FAILED_ASSERTIONS -eq 0 ]]; then
        SCENARIO_RESULTS+=("SCENARIO_4: PASSED")
        overall_success=true
        echo -e "${MAIN_GREEN}✓ Scenario 4 PASSED${MAIN_NC}"
    else
        SCENARIO_RESULTS+=("SCENARIO_4: FAILED")
        overall_success=false
        echo -e "${MAIN_RED}✗ Scenario 4 FAILED${MAIN_NC}"
    fi

    # Print test summary
    print_test_summary "Scenario 4: Confidence Parsing Failure With Retry"

    # Cleanup
    unset TEST_PARSE_FAIL_PHASE TEST_PARSE_FAIL_FIRST
    cleanup_test_environment "$test_dir" "$PRESERVE_ON_FAIL"

    return $([ "$overall_success" = true ] && echo 0 || echo 1)
}

# =============================================================================
# Main Test Execution
# =============================================================================

# Execute individual scenario
run_single_scenario() {
    local scenario_number="$1"

    TOTAL_SCENARIOS_RUN=$((TOTAL_SCENARIOS_RUN + 1))

    case "$scenario_number" in
        1)
            if run_scenario_1_success; then
                PASSED_SCENARIOS=$((PASSED_SCENARIOS + 1))
                return 0
            else
                FAILED_SCENARIOS=$((FAILED_SCENARIOS + 1))
                return 1
            fi
            ;;
        2)
            if run_scenario_2_validation_retry; then
                PASSED_SCENARIOS=$((PASSED_SCENARIOS + 1))
                return 0
            else
                FAILED_SCENARIOS=$((FAILED_SCENARIOS + 1))
                return 1
            fi
            ;;
        3)
            if run_scenario_3_confidence_fail; then
                PASSED_SCENARIOS=$((PASSED_SCENARIOS + 1))
                return 0
            else
                FAILED_SCENARIOS=$((FAILED_SCENARIOS + 1))
                return 1
            fi
            ;;
        4)
            if run_scenario_4_parse_fail; then
                PASSED_SCENARIOS=$((PASSED_SCENARIOS + 1))
                return 0
            else
                FAILED_SCENARIOS=$((FAILED_SCENARIOS + 1))
                return 1
            fi
            ;;
        *)
            echo -e "${MAIN_RED}Invalid scenario number: $scenario_number${MAIN_NC}" >&2
            return 1
            ;;
    esac
}

# Print overall test suite results
print_suite_results() {
    echo
    echo -e "${MAIN_BLUE}================================================================${MAIN_NC}"
    echo -e "${MAIN_BLUE}           DASV E2E Test Suite Results${MAIN_NC}"
    echo -e "${MAIN_BLUE}================================================================${MAIN_NC}"
    echo
    echo -e "Test Date: $(date -Iseconds)"
    echo -e "Test Configuration:"
    echo -e "  Ticker: $DEFAULT_TICKER"
    echo -e "  Debug Mode: $DEBUG_MODE"
    echo -e "  Preserve on Fail: $PRESERVE_ON_FAIL"
    echo
    echo -e "Execution Summary:"
    echo -e "  Total Scenarios Run: $TOTAL_SCENARIOS_RUN"
    echo -e "  ${MAIN_GREEN}Passed: $PASSED_SCENARIOS${MAIN_NC}"
    echo -e "  ${MAIN_RED}Failed: $FAILED_SCENARIOS${MAIN_NC}"
    echo
    echo -e "Scenario Results:"
    for result in "${SCENARIO_RESULTS[@]}"; do
        if [[ "$result" == *"PASSED"* ]]; then
            echo -e "  ${MAIN_GREEN}✓ $result${MAIN_NC}"
        else
            echo -e "  ${MAIN_RED}✗ $result${MAIN_NC}"
        fi
    done
    echo

    if [[ $FAILED_SCENARIOS -eq 0 ]]; then
        echo -e "${MAIN_GREEN}🎉 ALL E2E TESTS PASSED! 🎉${MAIN_NC}"
        return 0
    else
        echo -e "${MAIN_RED}❌ SOME E2E TESTS FAILED${MAIN_NC}"
        return 1
    fi
}

# Main execution function
main() {
    # Parse command line arguments
    parse_arguments "$@"

    # Display test suite header
    echo -e "${MAIN_BLUE}================================================================${MAIN_NC}"
    echo -e "${MAIN_BLUE}           DASV E2E Test Suite${MAIN_NC}"
    echo -e "${MAIN_BLUE}================================================================${MAIN_NC}"
    echo -e "Test Date: $(date -Iseconds)"
    echo -e "Selected Scenario: $RUN_SCENARIO"
    echo -e "Debug Mode: $DEBUG_MODE"
    echo -e "Preserve on Fail: $PRESERVE_ON_FAIL"
    echo -e "${MAIN_BLUE}================================================================${MAIN_NC}"
    echo

    # Pre-flight checks
    echo -e "${MAIN_BLUE}Performing pre-flight checks...${MAIN_NC}"

    # Check shell script exists
    if [[ ! -f "$SHELL_SCRIPT_PATH" ]]; then
        echo -e "${MAIN_RED}ERROR: Shell script not found: $SHELL_SCRIPT_PATH${MAIN_NC}" >&2
        exit 1
    fi

    # Check mock Claude CLI exists
    if [[ ! -f "$MOCKS_DIR/claude" ]]; then
        echo -e "${MAIN_RED}ERROR: Mock Claude CLI not found: $MOCKS_DIR/claude${MAIN_NC}" >&2
        exit 1
    fi

    # Check test fixtures exist
    if [[ ! -d "$FIXTURES_DIR" ]] || [[ -z "$(ls -A "$FIXTURES_DIR")" ]]; then
        echo -e "${MAIN_RED}ERROR: Test fixtures not found or empty: $FIXTURES_DIR${MAIN_NC}" >&2
        exit 1
    fi

    echo -e "${MAIN_GREEN}✓ Pre-flight checks passed${MAIN_NC}"
    echo

    # Execute scenarios
    local exit_code=0

    if [[ "$RUN_SCENARIO" == "all" ]]; then
        # Run all scenarios
        for scenario in {1..4}; do
            if ! run_single_scenario "$scenario"; then
                exit_code=1
            fi
            echo  # Add spacing between scenarios
        done
    else
        # Run single scenario
        if ! run_single_scenario "$RUN_SCENARIO"; then
            exit_code=1
        fi
    fi

    # Print final results
    print_suite_results

    exit $exit_code
}

# Execute main function with all arguments
main "$@"
