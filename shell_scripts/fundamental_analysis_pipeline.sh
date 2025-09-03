#!/usr/bin/env bash
# Script: fundamental_analysis_pipeline.sh
# Purpose: Execute complete DASV fundamental analysis workflow using Claude Code commands
# Requirements: Claude Code CLI, Claude authentication, valid Claude commands
# Compatibility: macOS, Linux (bash 4.0+)

# Strict error handling
set -euo pipefail
IFS=$'\n\t'

# Global configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly DATA_OUTPUTS="${PROJECT_ROOT}/data/outputs"
readonly CLAUDE_COMMANDS_DIR="${PROJECT_ROOT}/.claude/commands/fundamental_analysis"
readonly RICH_UI_SCRIPT="${SCRIPT_DIR}/rich_pipeline_ui.py"

# Output directories
readonly DISCOVERY_DIR="${DATA_OUTPUTS}/fundamental_analysis/discovery"
readonly ANALYSIS_DIR="${DATA_OUTPUTS}/fundamental_analysis/analysis"
readonly SYNTHESIS_DIR="${DATA_OUTPUTS}/fundamental_analysis"
readonly VALIDATION_DIR="${DATA_OUTPUTS}/fundamental_analysis/validation"

# Logging configuration
readonly LOG_DIR="${PROJECT_ROOT}/logs"
readonly LOG_FILE="${LOG_DIR}/fundamental_analysis_$(date '+%Y%m%d_%H%M%S').log"
readonly MAX_LOG_FILES=10

# Default configuration
readonly DEFAULT_CONFIDENCE_THRESHOLD="9.0"
readonly DEFAULT_VALIDATION_DEPTH="institutional"
readonly DEFAULT_RETRY_ATTEMPTS=1
readonly CLAUDE_COMMAND_TIMEOUT=900

# Global variables
TICKER=""
ANALYSIS_DATE=""
CONFIDENCE_THRESHOLD="${DEFAULT_CONFIDENCE_THRESHOLD}"
VALIDATION_DEPTH="${DEFAULT_VALIDATION_DEPTH}"
RETRY_ATTEMPTS="${DEFAULT_RETRY_ATTEMPTS}"
CURRENT_ATTEMPT=0
EXECUTION_ID="$(date '+%Y%m%d_%H%M%S')_$$"

# Claude command files
readonly CLAUDE_COMMANDS=(
    "discover.md"
    "analyze.md"
    "synthesize.md"
    "validate.md"
)

# Rich UI helper functions
use_rich_ui() {
    # Check if rich UI script exists and python3 is available
    [[ -f "${RICH_UI_SCRIPT}" ]] && command -v python3 >/dev/null 2>&1
}

rich_header() {
    if use_rich_ui; then
        python3 "${RICH_UI_SCRIPT}" header --ticker "${TICKER}" --date "${ANALYSIS_DATE}" --execution-id "${EXECUTION_ID}" 2>/dev/null || true
    fi
}

rich_phase_update() {
    local phase="${1}"
    local status="${2}"
    local message="${3:-}"

    if use_rich_ui; then
        python3 "${RICH_UI_SCRIPT}" phase --phase "${phase}" --status "${status}" --message "${message}" 2>/dev/null || true
    fi
}

rich_confidence_check() {
    local score="${1}"
    local threshold="${2}"
    local passed="${3}"

    if use_rich_ui; then
        local passed_arg=""
        [[ "${passed}" == "true" ]] && passed_arg="--passed"
        python3 "${RICH_UI_SCRIPT}" confidence --confidence-score "${score}" --threshold "${threshold}" ${passed_arg} 2>/dev/null || true
    fi
}

rich_summary() {
    local summary_file="${1}"

    if use_rich_ui && [[ -f "${summary_file}" ]]; then
        python3 "${RICH_UI_SCRIPT}" summary --summary-file "${summary_file}" 2>/dev/null || true
    fi
}

rich_error() {
    local message="${1}"
    local code="${2:-1}"
    local details="${3:-}"

    if use_rich_ui; then
        python3 "${RICH_UI_SCRIPT}" error --error-message "${message}" --error-code "${code}" --error-details "${details}" 2>/dev/null || true
    fi
}

rich_confirm() {
    local ticker="${1}"
    local date="${2}"

    if use_rich_ui; then
        python3 "${RICH_UI_SCRIPT}" confirm --ticker "${ticker}" --date "${date}" 2>/dev/null
        return $?
    else
        # Fallback to simple confirmation
        echo "Execute pipeline for ${ticker} on ${date}? [y/N]: "
        read -r response
        [[ "${response}" =~ ^[Yy] ]]
    fi
}

# Error handling and cleanup
cleanup() {
    local exit_code=$?
    log "INFO" "Cleaning up execution (exit code: ${exit_code})"

    # Remove any temporary files
    find "${DATA_OUTPUTS}" -name "*.tmp" -mtime +1 -delete 2>/dev/null || true

    # Cleanup incomplete files on failure
    if [[ ${exit_code} -ne 0 && -n "${TICKER}" && -n "${ANALYSIS_DATE}" ]]; then
        log "WARN" "Removing incomplete files due to failure"
        rm -f "${DISCOVERY_DIR}/${TICKER}_${ANALYSIS_DATE}_discovery.json.tmp" 2>/dev/null || true
        rm -f "${ANALYSIS_DIR}/${TICKER}_${ANALYSIS_DATE}_analysis.json.tmp" 2>/dev/null || true
        rm -f "${SYNTHESIS_DIR}/${TICKER}_${ANALYSIS_DATE}.md.tmp" 2>/dev/null || true
    fi

    log "INFO" "Cleanup completed"
    exit "${exit_code}"
}

error_exit() {
    local msg="${1:-Unknown error}"
    local code="${2:-1}"
    local details="${3:-}"
    log "ERROR" "${msg}"

    # Display rich error if available, otherwise fallback to plain text
    rich_error "${msg}" "${code}" "${details}"
    echo "ERROR: ${msg}" >&2
    exit "${code}"
}

trap cleanup EXIT
trap 'error_exit "Script failed at line ${LINENO}" 130' INT
trap 'error_exit "Script terminated" 143' TERM
trap 'error_exit "Script failed at line ${LINENO}"' ERR

# Logging framework
log() {
    local level="${1}"
    local msg="${2}"
    local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    local log_entry="[${timestamp}] [${level}] [${EXECUTION_ID}] ${msg}"

    # Create log directory if it doesn't exist
    mkdir -p "${LOG_DIR}"

    # Write to log file
    echo "${log_entry}" >> "${LOG_FILE}"

    # Also output to console for INFO and WARN levels
    case "${level}" in
        "INFO"|"WARN")
            echo "${log_entry}"
            ;;
        "ERROR")
            echo "${log_entry}" >&2
            ;;
    esac
}

# Rotate log files to prevent disk space issues
rotate_logs() {
    if [[ -d "${LOG_DIR}" ]]; then
        local log_count
        log_count=$(find "${LOG_DIR}" -name "fundamental_analysis_*.log" | wc -l)

        if [[ ${log_count} -gt ${MAX_LOG_FILES} ]]; then
            log "INFO" "Rotating old log files (found ${log_count}, keeping ${MAX_LOG_FILES})"
            # Calculate how many files to remove (compatible with macOS)
            local files_to_remove=$((log_count - MAX_LOG_FILES))
            find "${LOG_DIR}" -name "fundamental_analysis_*.log" -type f -print0 | \
                xargs -0 ls -t | tail -n ${files_to_remove} | \
                xargs rm -f
        fi
    fi
}

# Prerequisites validation for Claude Code
validate_prerequisites() {
    log "INFO" "Validating Claude Code prerequisites and environment"

    # Check Claude CLI is available
    if ! command -v claude >/dev/null 2>&1; then
        error_exit "Claude Code CLI is required but not found in PATH. Please install Claude Code." 2
    fi

    log "INFO" "Claude Code CLI found"

    # Test Claude authentication
    if ! timeout 10 claude --help >/dev/null 2>&1; then
        error_exit "Claude Code CLI is not responding. Please check your authentication and network connection." 2
    fi

    log "INFO" "Claude Code CLI is responding"

    # Check project structure
    local required_dirs=(
        "${DATA_OUTPUTS}"
        "${CLAUDE_COMMANDS_DIR}"
    )

    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "${dir}" ]]; then
            error_exit "Required directory not found: ${dir}" 3
        fi
    done

    # Verify Claude command files exist
    for command_file in "${CLAUDE_COMMANDS[@]}"; do
        local command_path="${CLAUDE_COMMANDS_DIR}/${command_file}"
        if [[ ! -f "${command_path}" ]]; then
            error_exit "Required Claude command file not found: ${command_path}" 3
        fi
    done

    # Create output directories
    local output_dirs=(
        "${DISCOVERY_DIR}"
        "${ANALYSIS_DIR}"
        "${VALIDATION_DIR}"
    )

    for dir in "${output_dirs[@]}"; do
        mkdir -p "${dir}" || error_exit "Cannot create directory: ${dir}" 5
    done

    log "INFO" "Prerequisites validation completed successfully"
    return 0
}

# Input validation and processing
validate_input() {
    local input="${1}"
    local pattern="${2}"
    local error_msg="${3}"

    if [[ ! "${input}" =~ ${pattern} ]]; then
        error_exit "${error_msg}" 2
    fi
}

process_input_parameters() {
    log "INFO" "Processing input parameters"

    # Validate ticker
    if [[ -z "${TICKER}" ]]; then
        error_exit "Ticker symbol is required" 2
    fi

    # Sanitize and validate ticker format
    TICKER=$(echo "${TICKER}" | tr '[:lower:]' '[:upper:]' | sed 's/[^A-Z0-9._-]//g')
    validate_input "${TICKER}" "^[A-Z0-9._-]{1,10}$" "Invalid ticker format: ${TICKER}"

    # Set default date if not provided
    if [[ -z "${ANALYSIS_DATE}" ]]; then
        ANALYSIS_DATE=$(date '+%Y%m%d')
        log "INFO" "Using current date: ${ANALYSIS_DATE}"
    fi

    # Validate date format
    validate_input "${ANALYSIS_DATE}" "^[0-9]{8}$" "Invalid date format: ${ANALYSIS_DATE} (expected: YYYYMMDD)"

    # Validate confidence threshold
    if ! python3 -c "
threshold = float('${CONFIDENCE_THRESHOLD}')
if not (9.0 <= threshold <= 10.0):
    exit(1)
" 2>/dev/null; then
        error_exit "Invalid confidence threshold: ${CONFIDENCE_THRESHOLD} (must be 9.0-10.0)" 2
    fi

    # Validate retry attempts
    if [[ ! "${RETRY_ATTEMPTS}" =~ ^[1-5]$ ]]; then
        error_exit "Invalid retry attempts: ${RETRY_ATTEMPTS} (must be 1-5)" 2
    fi

    log "INFO" "Input parameters validated: TICKER=${TICKER}, DATE=${ANALYSIS_DATE}, CONFIDENCE=${CONFIDENCE_THRESHOLD}"
}

# Execute Claude command with error handling
execute_claude_command() {
    local command_file="${1}"
    local phase_name="${2}"
    local expected_output="${3}"

    log "INFO" "Executing Claude command: ${command_file}"

    local command_path="${CLAUDE_COMMANDS_DIR}/${command_file}"
    local temp_output="${expected_output}.tmp"

    # Execute Claude command with timeout and input ticker
    if timeout "${CLAUDE_COMMAND_TIMEOUT}" bash -c "echo '${TICKER}' | claude -p '${command_path}'" 2>&1 | tee -a "${LOG_FILE}"; then
        log "INFO" "Claude command executed successfully: ${command_file}"

        # Wait a moment for file system to sync
        sleep 2

        # Check if expected output file was created
        if [[ -f "${expected_output}" && -s "${expected_output}" ]]; then
            log "INFO" "${phase_name} output file created successfully: ${expected_output}"
            return 0
        elif [[ -f "${temp_output}" && -s "${temp_output}" ]]; then
            # Handle case where output has .tmp extension
            mv "${temp_output}" "${expected_output}"
            log "INFO" "${phase_name} output file moved from temp: ${expected_output}"
            return 0
        else
            # Search for any files that might have been created with similar names
            local base_name
            base_name=$(basename "${expected_output}")
            local found_files
            found_files=$(find "$(dirname "${expected_output}")" -name "*${TICKER}*${ANALYSIS_DATE}*" -type f 2>/dev/null || true)

            if [[ -n "${found_files}" ]]; then
                log "INFO" "Found related files: ${found_files}"
                # Try to find the most recent matching file
                local latest_file
                latest_file=$(echo "${found_files}" | head -n 1)
                if [[ -f "${latest_file}" && -s "${latest_file}" ]]; then
                    log "INFO" "Using found file: ${latest_file}"
                    echo "${latest_file}"
                    return 0
                fi
            fi

            error_exit "${phase_name} failed to generate expected output file: ${expected_output}" 7
        fi
    else
        local exit_code=$?
        error_exit "Claude command execution failed: ${command_file} (exit code: ${exit_code})" 7
    fi
}

# DASV Phase execution functions using Claude commands
execute_discovery_phase() {
    log "INFO" "Starting Discovery phase (Phase 1/4) using Claude command"
    rich_phase_update 1 "running" "Executing Claude discovery command"

    local discovery_output="${DISCOVERY_DIR}/${TICKER}_${ANALYSIS_DATE}_discovery.json"

    # Execute Claude discovery command
    local actual_output
    actual_output=$(execute_claude_command "discover.md" "Discovery" "${discovery_output}")

    # Validate JSON output
    if [[ -f "${actual_output}" ]]; then
        if python3 -m json.tool "${actual_output}" >/dev/null 2>&1; then
            if [[ "${actual_output}" != "${discovery_output}" ]]; then
                mv "${actual_output}" "${discovery_output}"
            fi
            log "INFO" "Discovery phase completed successfully: ${discovery_output}"
            rich_phase_update 1 "completed" "Discovery data collected and validated"
            return 0
        else
            rich_phase_update 1 "failed" "Invalid JSON output generated"
            error_exit "Discovery output is not valid JSON: ${actual_output}" 7
        fi
    else
        rich_phase_update 1 "failed" "No output file generated"
        error_exit "Discovery phase failed - no output file found" 7
    fi
}

execute_analysis_phase() {
    log "INFO" "Starting Analysis phase (Phase 2/4) using Claude command"
    rich_phase_update 2 "running" "Processing discovery data for analysis"

    local discovery_input="${DISCOVERY_DIR}/${TICKER}_${ANALYSIS_DATE}_discovery.json"
    local analysis_output="${ANALYSIS_DIR}/${TICKER}_${ANALYSIS_DATE}_analysis.json"

    # Verify discovery input exists
    if [[ ! -f "${discovery_input}" ]]; then
        rich_phase_update 2 "failed" "Discovery input file not found"
        error_exit "Discovery input not found: ${discovery_input}" 8
    fi

    # Execute Claude analysis command
    local actual_output
    actual_output=$(execute_claude_command "analyze.md" "Analysis" "${analysis_output}")

    # Validate JSON output
    if [[ -f "${actual_output}" ]]; then
        if python3 -m json.tool "${actual_output}" >/dev/null 2>&1; then
            if [[ "${actual_output}" != "${analysis_output}" ]]; then
                mv "${actual_output}" "${analysis_output}"
            fi
            log "INFO" "Analysis phase completed successfully: ${analysis_output}"
            rich_phase_update 2 "completed" "Financial analysis completed and validated"
            return 0
        else
            rich_phase_update 2 "failed" "Invalid JSON analysis output"
            error_exit "Analysis output is not valid JSON: ${actual_output}" 8
        fi
    else
        rich_phase_update 2 "failed" "No analysis output file generated"
        error_exit "Analysis phase failed - no output file found" 8
    fi
}

execute_synthesis_phase() {
    log "INFO" "Starting Synthesis phase (Phase 3/4) using Claude command"
    rich_phase_update 3 "running" "Synthesizing discovery and analysis data"

    local discovery_input="${DISCOVERY_DIR}/${TICKER}_${ANALYSIS_DATE}_discovery.json"
    local analysis_input="${ANALYSIS_DIR}/${TICKER}_${ANALYSIS_DATE}_analysis.json"
    local synthesis_output="${SYNTHESIS_DIR}/${TICKER}_${ANALYSIS_DATE}.md"

    # Verify inputs exist
    if [[ ! -f "${discovery_input}" ]]; then
        rich_phase_update 3 "failed" "Discovery input file missing"
        error_exit "Discovery input not found: ${discovery_input}" 9
    fi

    if [[ ! -f "${analysis_input}" ]]; then
        rich_phase_update 3 "failed" "Analysis input file missing"
        error_exit "Analysis input not found: ${analysis_input}" 9
    fi

    # Execute Claude synthesis command
    local actual_output
    actual_output=$(execute_claude_command "synthesize.md" "Synthesis" "${synthesis_output}")

    # Validate markdown output
    if [[ -f "${actual_output}" && -s "${actual_output}" ]]; then
        if [[ "${actual_output}" != "${synthesis_output}" ]]; then
            mv "${actual_output}" "${synthesis_output}"
        fi
        log "INFO" "Synthesis phase completed successfully: ${synthesis_output}"
        rich_phase_update 3 "completed" "Investment report synthesized successfully"
        return 0
    else
        rich_phase_update 3 "failed" "No synthesis output file generated"
        error_exit "Synthesis phase failed - no output file found" 9
    fi
}

execute_validation_phase() {
    log "INFO" "Starting Validation phase (Phase 4/4) using Claude command"
    rich_phase_update 4 "running" "Validating synthesis report quality"

    local synthesis_input="${SYNTHESIS_DIR}/${TICKER}_${ANALYSIS_DATE}.md"
    local validation_output="${VALIDATION_DIR}/${TICKER}_${ANALYSIS_DATE}_validation.json"

    # Verify synthesis input exists
    if [[ ! -f "${synthesis_input}" ]]; then
        rich_phase_update 4 "failed" "Synthesis input file missing"
        error_exit "Synthesis input not found: ${synthesis_input}" 10
    fi

    # Execute Claude validation command
    local actual_output
    actual_output=$(execute_claude_command "validate.md" "Validation" "${validation_output}")

    # Validate JSON output
    if [[ -f "${actual_output}" ]]; then
        if python3 -m json.tool "${actual_output}" >/dev/null 2>&1; then
            if [[ "${actual_output}" != "${validation_output}" ]]; then
                mv "${actual_output}" "${validation_output}"
            fi
            log "INFO" "Validation phase completed successfully: ${validation_output}"
            rich_phase_update 4 "completed" "Quality validation completed"
            echo "${validation_output}"  # Return validation file path for confidence checking
            return 0
        else
            rich_phase_update 4 "failed" "Invalid validation JSON output"
            error_exit "Validation output is not valid JSON: ${actual_output}" 10
        fi
    else
        rich_phase_update 4 "failed" "No validation output file generated"
        error_exit "Validation phase failed - no output file found" 10
    fi
}

# Confidence threshold checking
check_confidence_threshold() {
    local validation_file="${1}"

    log "INFO" "Checking confidence threshold against ${CONFIDENCE_THRESHOLD}"

    if [[ ! -f "${validation_file}" ]]; then
        error_exit "Validation file not found: ${validation_file}" 11
    fi

    # Extract overall confidence score from validation JSON
    local overall_confidence
    overall_confidence=$(python3 -c "
import json
import sys

try:
    with open('${validation_file}', 'r') as f:
        data = json.load(f)

    # Try different possible paths for confidence score
    score_paths = [
        ['overall_assessment', 'overall_reliability_score'],
        ['dasv_validation_breakdown', 'overall_confidence_score'],
        ['quality_assessment', 'overall_confidence']
    ]

    score = None
    for path in score_paths:
        try:
            current = data
            for key in path:
                current = current[key]

            # Extract numeric value from score (handles formats like '9.2/10.0')
            if isinstance(current, str) and '/' in current:
                score = float(current.split('/')[0])
            elif isinstance(current, (int, float)):
                score = float(current)

            if score is not None:
                break
        except (KeyError, ValueError, TypeError):
            continue

    if score is not None:
        print(f'{score:.1f}')
    else:
        print('0.0')

except Exception as e:
    print('0.0', file=sys.stderr)
    sys.exit(1)
")

    if [[ -z "${overall_confidence}" ]]; then
        log "WARN" "Could not extract confidence score from validation file"
        return 1
    fi

    log "INFO" "Overall confidence score: ${overall_confidence}/10.0 (threshold: ${CONFIDENCE_THRESHOLD})"

    # Compare confidence score with threshold
    if python3 -c "
import sys
score = float('${overall_confidence}')
threshold = float('${CONFIDENCE_THRESHOLD}')
sys.exit(0 if score >= threshold else 1)
" 2>/dev/null; then
        log "INFO" "Confidence threshold met: ${overall_confidence} >= ${CONFIDENCE_THRESHOLD}"
        rich_confidence_check "${overall_confidence}" "${CONFIDENCE_THRESHOLD}" "true"
        return 0
    else
        log "WARN" "Confidence threshold NOT met: ${overall_confidence} < ${CONFIDENCE_THRESHOLD}"
        rich_confidence_check "${overall_confidence}" "${CONFIDENCE_THRESHOLD}" "false"
        return 1
    fi
}

# Retry mechanism for validation failures using Claude commands
retry_pipeline_on_failure() {
    local validation_file="${1}"

    if ! check_confidence_threshold "${validation_file}"; then
        if [[ ${CURRENT_ATTEMPT} -lt ${RETRY_ATTEMPTS} ]]; then
            ((CURRENT_ATTEMPT++))
            log "INFO" "Retrying pipeline execution (attempt ${CURRENT_ATTEMPT}/${RETRY_ATTEMPTS})"

            # Add small delay between retries
            sleep 5

            # Re-execute validation phase with Claude command
            log "INFO" "Re-executing validation phase using Claude command"
            validation_file=$(execute_validation_phase)

            # Recursively check again
            retry_pipeline_on_failure "${validation_file}"
        else
            log "WARN" "Maximum retry attempts reached (${RETRY_ATTEMPTS}). Pipeline completed with confidence below threshold."
            return 1
        fi
    fi

    return 0
}

# Main execution workflow using Claude commands
execute_full_pipeline() {
    log "INFO" "Starting full DASV pipeline execution for ${TICKER} using Claude commands"
    log "INFO" "Execution ID: ${EXECUTION_ID}"

    # Display rich header
    rich_header

    # Phase 1: Discovery using Claude command
    execute_discovery_phase

    # Phase 2: Analysis using Claude command
    execute_analysis_phase

    # Phase 3: Synthesis using Claude command
    execute_synthesis_phase

    # Phase 4: Validation using Claude command
    local validation_file
    validation_file=$(execute_validation_phase)

    # Check confidence threshold and retry if necessary
    if ! retry_pipeline_on_failure "${validation_file}"; then
        log "WARN" "Pipeline completed but confidence threshold not met after ${RETRY_ATTEMPTS} attempts"
    fi

    log "INFO" "Full DASV pipeline execution completed for ${TICKER}"

    # Generate execution summary
    generate_execution_summary "${validation_file}"
}

# Generate execution summary
generate_execution_summary() {
    local validation_file="${1}"

    log "INFO" "Generating execution summary"

    local summary_file="${DATA_OUTPUTS}/fundamental_analysis/${TICKER}_${ANALYSIS_DATE}_summary.json"

    # Create summary with file verification
    python3 -c "
import json
import os
from datetime import datetime

summary = {
    'execution_metadata': {
        'ticker': '${TICKER}',
        'analysis_date': '${ANALYSIS_DATE}',
        'execution_id': '${EXECUTION_ID}',
        'execution_timestamp': datetime.now().isoformat(),
        'confidence_threshold': ${CONFIDENCE_THRESHOLD},
        'validation_depth': '${VALIDATION_DEPTH}',
        'retry_attempts_used': ${CURRENT_ATTEMPT},
        'execution_method': 'claude_commands'
    },
    'claude_commands_used': [
        '.claude/commands/fundamental_analysis/discover.md',
        '.claude/commands/fundamental_analysis/analyze.md',
        '.claude/commands/fundamental_analysis/synthesize.md',
        '.claude/commands/fundamental_analysis/validate.md'
    ],
    'output_files': {
        'discovery': '${DISCOVERY_DIR}/${TICKER}_${ANALYSIS_DATE}_discovery.json',
        'analysis': '${ANALYSIS_DIR}/${TICKER}_${ANALYSIS_DATE}_analysis.json',
        'synthesis': '${SYNTHESIS_DIR}/${TICKER}_${ANALYSIS_DATE}.md',
        'validation': '${validation_file}'
    },
    'file_verification': {}
}

# Verify each output file exists and get size
for phase, filepath in summary['output_files'].items():
    if os.path.exists(filepath):
        summary['file_verification'][phase] = {
            'exists': True,
            'size_bytes': os.path.getsize(filepath),
            'last_modified': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
        }
    else:
        summary['file_verification'][phase] = {
            'exists': False,
            'size_bytes': 0,
            'last_modified': None
        }

with open('${summary_file}', 'w') as f:
    json.dump(summary, f, indent=2)
"

    log "INFO" "Execution summary generated: ${summary_file}"

    # Display rich summary to user
    rich_summary "${summary_file}"

    # Fallback plain text summary if rich UI not available
    if ! use_rich_ui; then
        echo ""
        echo "=== FUNDAMENTAL ANALYSIS PIPELINE EXECUTION SUMMARY ==="
        echo "Ticker: ${TICKER}"
        echo "Date: ${ANALYSIS_DATE}"
        echo "Execution ID: ${EXECUTION_ID}"
        echo "Execution Method: Claude Commands"
        echo "Confidence Threshold: ${CONFIDENCE_THRESHOLD}"
        echo "Retry Attempts Used: ${CURRENT_ATTEMPT}/${RETRY_ATTEMPTS}"
        echo ""
        echo "Output Files:"
        echo "- Discovery: ${DISCOVERY_DIR}/${TICKER}_${ANALYSIS_DATE}_discovery.json"
        echo "- Analysis: ${ANALYSIS_DIR}/${TICKER}_${ANALYSIS_DATE}_analysis.json"
        echo "- Synthesis: ${SYNTHESIS_DIR}/${TICKER}_${ANALYSIS_DATE}.md"
        echo "- Validation: ${validation_file}"
        echo "- Summary: ${summary_file}"
        echo ""
        echo "Log File: ${LOG_FILE}"
        echo "======================================================="
    fi
}

# Usage information
show_usage() {
    cat << EOF
Usage: ${SCRIPT_NAME} [OPTIONS] <TICKER>

Execute complete DASV fundamental analysis pipeline using Claude Code commands.

ARGUMENTS:
    TICKER                  Stock ticker symbol (required, e.g., AAPL, MSFT, TSLA)

OPTIONS:
    -d, --date DATE         Analysis date in YYYYMMDD format (default: today)
    -c, --confidence FLOAT  Confidence threshold 9.0-10.0 (default: ${DEFAULT_CONFIDENCE_THRESHOLD})
    -v, --validation DEPTH  Validation depth: standard|comprehensive|institutional (default: ${DEFAULT_VALIDATION_DEPTH})
    -r, --retry INT         Retry attempts for validation failures 1-5 (default: ${DEFAULT_RETRY_ATTEMPTS})
    -h, --help             Show this help message

EXAMPLES:
    ${SCRIPT_NAME} AAPL
    ${SCRIPT_NAME} --date 20250725 --confidence 9.5 MSFT
    ${SCRIPT_NAME} -d 20250901 -c 9.8 -v institutional TSLA
    ${SCRIPT_NAME} --retry 5 GOOGL

DASV PIPELINE PHASES (Claude Commands):
    1. Discovery  - .claude/commands/fundamental_analysis/discover.md
    2. Analysis   - .claude/commands/fundamental_analysis/analyze.md
    3. Synthesis  - .claude/commands/fundamental_analysis/synthesize.md
    4. Validation - .claude/commands/fundamental_analysis/validate.md

OUTPUT DIRECTORIES:
    Discovery: ${DATA_OUTPUTS}/fundamental_analysis/discovery/
    Analysis:  ${DATA_OUTPUTS}/fundamental_analysis/analysis/
    Synthesis: ${DATA_OUTPUTS}/fundamental_analysis/
    Validation: ${DATA_OUTPUTS}/fundamental_analysis/validation/

REQUIREMENTS:
    - Claude Code CLI installed and authenticated
    - Valid Claude command files in .claude/commands/fundamental_analysis/
    - Network connectivity for Claude API access
    - Output directory write permissions

EXECUTION METHOD:
    Each phase executes: echo TICKER | claude -p .claude/commands/fundamental_analysis/[phase].md

EXIT CODES:
    0: Success
    1: General error
    2: Invalid input parameters or Claude CLI not found
    3: Missing required files/directories
    5: Directory creation error
    7: Claude command execution failure
    8: Analysis phase failure
    9: Synthesis phase failure
    10: Validation phase failure
    11: Confidence threshold checking error

For more information about Claude Code, visit: https://claude.ai/code
EOF
}

# Main entry point
main() {
    # Initialize logging
    rotate_logs
    log "INFO" "Starting fundamental analysis pipeline using Claude commands: ${SCRIPT_NAME}"
    log "INFO" "Project root: ${PROJECT_ROOT}"

    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--date)
                ANALYSIS_DATE="$2"
                shift 2
                ;;
            -c|--confidence)
                CONFIDENCE_THRESHOLD="$2"
                shift 2
                ;;
            -v|--validation)
                VALIDATION_DEPTH="$2"
                shift 2
                ;;
            -r|--retry)
                RETRY_ATTEMPTS="$2"
                shift 2
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            -*)
                error_exit "Unknown option: $1" 2
                ;;
            *)
                if [[ -z "${TICKER}" ]]; then
                    TICKER="$1"
                else
                    error_exit "Multiple ticker symbols provided. Only one ticker is supported." 2
                fi
                shift
                ;;
        esac
    done

    # Validate required ticker parameter
    if [[ -z "${TICKER}" ]]; then
        echo "Error: Ticker symbol is required" >&2
        echo ""
        show_usage
        exit 2
    fi

    # Execute main workflow using Claude commands
    validate_prerequisites
    process_input_parameters

    # Optional interactive confirmation (only if rich UI is available and terminal is interactive)
    if use_rich_ui && [[ -t 0 ]] && [[ -t 1 ]]; then
        if ! rich_confirm "${TICKER}" "${ANALYSIS_DATE}"; then
            log "INFO" "Pipeline execution cancelled by user"
            exit 0
        fi
    fi

    execute_full_pipeline

    log "INFO" "Pipeline execution completed successfully using Claude commands"
    exit 0
}

# Execute main function with all arguments
main "$@"
