# DASV E2E Testing Framework

## Overview

This E2E testing framework provides comprehensive testing for the DASV (Discovery → Analysis → Synthesis → Validation) fundamental analysis pipeline using mock Claude CLI responses and realistic test scenarios.

## Architecture

```
tests/e2e/
├── README.md                 # This documentation
├── run_e2e_tests.sh         # Main test execution harness
├── fixtures/                # Test data fixtures for all DASV phases
├── lib/                     # Test library functions
│   ├── test_assertions.sh   # Comprehensive assertion framework
│   └── test_utils.sh        # Environment setup and utilities
└── mocks/                   # Mock Claude CLI implementation
    ├── claude -> mock_claude.sh  # Symlink for PATH override
    └── mock_claude.sh       # Mock Claude CLI script
```

## Test Scenarios

The framework implements 4 comprehensive test scenarios:

### 1. Full E2E Success Flow
- **Purpose**: Validate complete DASV pipeline execution with high confidence scores
- **Expected**: All phases complete successfully with confidence ≥ 9.0/10.0
- **Validation**: File existence, confidence parsing, phase-specific content validation

### 2. Validation Fail Then Retry Success
- **Purpose**: Test retry mechanism when validation phase fails initially
- **Flow**: Validation fails (confidence < 9.0) → Retry → Validation succeeds
- **Validation**: Retry logging, eventual success after failure

### 3. Phase Confidence Failure With Retry
- **Purpose**: Test retry mechanism when any phase returns low confidence
- **Flow**: Phase returns confidence < 9.0 → Pipeline restarts from failed phase → Success
- **Validation**: Confidence threshold detection, phase restart logic

### 4. Confidence Parsing Failure With Retry
- **Purpose**: Test handling of malformed confidence scores in outputs
- **Flow**: Phase returns malformed confidence → Parse error detected → Retry → Success
- **Validation**: Parse error detection, error handling, retry mechanism

## Key Components

### Mock Claude CLI (`mocks/mock_claude.sh`)
- **Environment Control**: Uses `TEST_*` environment variables for scenario control
- **Fixture Loading**: Dynamically loads test fixtures based on scenario and phase
- **Realistic Output**: Generates outputs in correct project directory structure
- **Debug Support**: Comprehensive debug logging with `DEBUG_MOCK=true`

### Assertion Framework (`lib/test_assertions.sh`)
- **DASV-Specific Validations**: Phase-specific content and structure validation
- **Confidence Score Parsing**: Handles multiple confidence score formats (JSON/markdown)
- **Threshold Validation**: Configurable confidence thresholds (default: 9.0/10.0)
- **Comprehensive Reporting**: Detailed pass/fail reporting with error messages

### Test Utilities (`lib/test_utils.sh`)
- **Environment Management**: Isolated test environments with proper cleanup
- **Process Control**: Shell script execution with timeout handling
- **Path Management**: Correct output path generation matching shell script structure
- **Logging**: Comprehensive test execution logging and debugging

## Usage

### Basic Execution

```bash
# Run all test scenarios
./tests/e2e/run_e2e_tests.sh

# Run specific scenario
./tests/e2e/run_e2e_tests.sh -s 1

# Run with debug output
./tests/e2e/run_e2e_tests.sh -s 1 -d

# Preserve test environment on failure
./tests/e2e/run_e2e_tests.sh -p
```

### Environment Variables

Key environment variables for test control:

```bash
# Scenario control
TEST_SCENARIO="success|confidence_fail_retry|parse_fail_retry"

# Phase-specific failure control
TEST_VALIDATION_FAIL_FIRST=true      # Fail validation on first attempt
TEST_CONFIDENCE_FAIL_PHASE="analysis" # Phase to fail with low confidence
TEST_CONFIDENCE_FAIL_FIRST=true      # Fail confidence on first attempt
TEST_PARSE_FAIL_PHASE="discovery"    # Phase to fail with malformed confidence
TEST_PARSE_FAIL_FIRST=true          # Fail parsing on first attempt

# Debug control
TEST_DEBUG=true                      # Enable test framework debug output
DEBUG_MOCK=true                     # Enable mock Claude CLI debug output
```

## Test Fixtures

### Fixture Categories

1. **Success Fixtures** (`*_success.*`)
   - High confidence scores (≥ 9.0/10.0)
   - Complete, valid JSON/markdown structure
   - Institutional quality content

2. **Low Confidence Fixtures** (`*_low_confidence.*`)
   - Confidence scores < 9.0/10.0
   - Valid structure but lower quality assessments
   - Used for confidence failure testing

3. **Malformed Fixtures** (`*_malformed.*`)
   - Invalid confidence score formats
   - Used for parsing error testing
   - Triggers retry mechanisms

### Fixture Structure

- **Discovery**: `discovery_*.json` - Market data, financial metrics, CLI service data
- **Analysis**: `analysis_*.json` - Financial health, competitive analysis, risk assessment
- **Synthesis**: `synthesis_*.md` - Investment thesis, business intelligence, recommendations
- **Validation**: `validation_*.json` - DASV validation results, reliability scores

## Testing Best Practices

### Adding New Test Scenarios

1. **Create Fixtures**: Add appropriate fixtures to `fixtures/` directory
2. **Environment Variables**: Define scenario-specific environment variables
3. **Mock Logic**: Update `mock_claude.sh` to handle new scenario
4. **Test Function**: Add new test function to `run_e2e_tests.sh`
5. **Assertions**: Implement scenario-specific validation logic

### Debug Testing

Enable comprehensive debugging:

```bash
export TEST_DEBUG=true
export DEBUG_MOCK=true
./tests/e2e/run_e2e_tests.sh -s 1 -d -p
```

This provides:
- Test framework debug output
- Mock Claude CLI decision logging
- Preserved test environments for inspection
- Detailed assertion failure reporting

### Test Data Management

- **Placeholders**: All fixtures use `TICKER_PLACEHOLDER` and `DATE_PLACEHOLDER`
- **Dynamic Replacement**: Mock CLI replaces placeholders with actual test values
- **Realistic Content**: Fixtures contain realistic financial analysis content
- **Confidence Variations**: Multiple confidence levels for different test scenarios

## Integration Points

### Shell Script Integration
- **Path Override**: Mock Claude CLI is inserted into PATH before shell script execution
- **Output Structure**: Mock generates outputs in correct project directory structure
- **Command Compatibility**: Full compatibility with shell script's Claude command patterns

### Assertion Integration
- **File Validation**: Checks expected output files exist and have correct structure
- **Content Validation**: Phase-specific content validation (required fields, sections)
- **Confidence Validation**: Multi-format confidence score parsing and threshold validation
- **Retry Validation**: Validates retry mechanism behavior and logging

## Troubleshooting

### Common Issues

1. **Mock Claude Not Found**: Ensure `tests/e2e/mocks/claude` symlink exists and is executable
2. **Path Issues**: Verify PATH includes mocks directory before shell script execution
3. **Permission Errors**: Ensure all scripts have execute permissions (`chmod +x`)
4. **Fixture Loading**: Check fixture files exist and have correct naming convention

### Debug Output Analysis

- **Test Framework**: Look for `[INFO]`, `[ERROR]`, `[DEBUG]` log entries
- **Mock Claude**: Enable `DEBUG_MOCK=true` for fixture loading decisions
- **Assertion Results**: Check assertion pass/fail summary for specific failure points
- **Shell Script**: Review shell script logs for Claude command execution details

## Future Enhancements

Potential improvements to the testing framework:

1. **Parallel Execution**: Run multiple scenarios concurrently
2. **Performance Testing**: Add timing and performance validation
3. **Integration Testing**: Test with actual Claude CLI in staging environment
4. **Load Testing**: Test pipeline with multiple concurrent executions
5. **Regression Testing**: Automated testing against historical outputs
