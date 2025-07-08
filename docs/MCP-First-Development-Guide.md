# MCP-First Development Guide for Sensylate

**Date**: 2025-07-04
**Status**: 🚨 **CRITICAL - MANDATORY IMPLEMENTATION**
**Applies To**: All Python scripts, commands, and analysis workflows

## Executive Summary

This guide establishes **MCP-First Development** as the mandatory standard for all Sensylate development. After discovering systematic bypassing of MCP infrastructure, this guide provides comprehensive patterns, examples, and enforcement mechanisms to prevent further anti-patterns.

## 🚨 Critical Issue Background

### The Problem
Multiple implementations have been bypassing the Yahoo Finance MCP server:
- `fundamental_analyst_discover` - Direct service imports ❌
- `test_rklb_data.py` - Direct service imports ❌
- Pattern spreading across codebase ❌

### The Impact
- **Zero ROI** on MCP server development
- **No standardization** across data access
- **Missing monitoring** and caching benefits
- **Technical debt** from inconsistent patterns
- **Architectural inconsistency** throughout platform

## MCP-First Development Principles

### Core Principle: Protocol Over Implementation
```python
# ❌ WRONG - Direct Implementation Access
from yahoo_finance_service import YahooFinanceService
service = YahooFinanceService()
data = service.get_stock_info("AAPL")

# ✅ CORRECT - MCP Protocol Access
from lib.mcp_client_wrapper import call_yahoo_finance_tool
data = call_yahoo_finance_tool("get_stock_fundamentals", {"symbol": "AAPL"})
```

### Benefits of MCP-First Approach

| Aspect | Direct Implementation | MCP-First |
|--------|----------------------|-----------|
| **Coupling** | Tight coupling | Loose coupling via protocol |
| **Standardization** | Each script different | Consistent interface |
| **Caching** | Per-instance | Centralized server-wide |
| **Rate Limiting** | Per-instance | Server-wide control |
| **Error Handling** | Inconsistent | Standardized responses |
| **Monitoring** | No visibility | Full observability |
| **Testing** | Must mock services | Mock MCP responses |
| **Maintenance** | Multiple implementations | Single server to maintain |

## Development Patterns

### Pattern 1: Simple Tool Calls
```python
# Use for single MCP tool calls
from lib.mcp_client_wrapper import call_yahoo_finance_tool, MCPError

try:
    result = call_yahoo_finance_tool(
        "get_stock_fundamentals",
        {"symbol": "AAPL"}
    )
    print(f"Success: {result}")
except MCPError as e:
    print(f"MCP Error: {e}")
```

### Pattern 2: Multiple Tool Calls (Context Manager)
```python
# Use for multiple calls to same server
from lib.mcp_client_wrapper import MCPClientWrapper

try:
    with MCPClientWrapper("yahoo-finance") as client:
        fundamentals = client.call_tool("get_stock_fundamentals", {"symbol": "AAPL"})
        market_data = client.call_tool("get_market_data", {"symbol": "AAPL", "period": "1y"})
        financials = client.call_tool("get_financial_statements", {"symbol": "AAPL"})

        return {
            "fundamentals": fundamentals,
            "market_data": market_data,
            "financials": financials
        }
except MCPError as e:
    print(f"MCP Error: {e}")
```

### Pattern 3: Class-Based Integration
```python
# Use for analysis classes and complex workflows
from lib.mcp_client_wrapper import MCPClientWrapper

class FinancialAnalyzer:
    def __init__(self, mcp_server="yahoo-finance"):
        self.mcp_server = mcp_server

    def analyze_company(self, symbol):
        with MCPClientWrapper(self.mcp_server) as client:
            # Collect all data via MCP
            data = self._collect_comprehensive_data(client, symbol)
            # Perform analysis
            return self._perform_analysis(data)

    def _collect_comprehensive_data(self, client, symbol):
        return {
            "fundamentals": client.call_tool("get_stock_fundamentals", {"symbol": symbol}),
            "market_data": client.call_tool("get_market_data", {"symbol": symbol, "period": "5y"}),
            "financials": client.call_tool("get_financial_statements", {"symbol": symbol})
        }
```

## Available MCP Servers

### Yahoo Finance Server
```python
# Configuration in mcp-servers.json
{
    "yahoo-finance": {
        "command": "python",
        "args": ["mcp_servers/yahoo_finance_server.py"],
        "description": "Yahoo Finance data standardization"
    }
}

# Available Tools:
# - get_stock_fundamentals
# - get_market_data
# - get_financial_statements
```

### Sensylate Trading Server
```python
# Configuration in mcp-servers.json
{
    "sensylate-trading": {
        "command": "python",
        "args": ["mcp_servers/sensylate_trading_server.py"],
        "description": "Sensylate trading analysis tools"
    }
}
```

## Error Handling Standards

### MCP-Specific Error Types
```python
from lib.mcp_client_wrapper import MCPError, MCPConnectionError, MCPToolError

try:
    result = call_yahoo_finance_tool("get_stock_fundamentals", {"symbol": "AAPL"})
except MCPConnectionError as e:
    # Handle server connection issues
    print(f"Cannot connect to MCP server: {e}")
except MCPToolError as e:
    # Handle tool execution issues
    print(f"Tool execution failed: {e}")
except MCPError as e:
    # Handle general MCP issues
    print(f"MCP error: {e}")
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error: {e}")
```

### Error Recovery Patterns
```python
def robust_data_collection(symbol, retries=3):
    """Example of robust MCP data collection with retries"""
    for attempt in range(retries):
        try:
            return call_yahoo_finance_tool("get_stock_fundamentals", {"symbol": symbol})
        except MCPConnectionError as e:
            if attempt < retries - 1:
                print(f"Connection failed, retrying... ({attempt + 1}/{retries})")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"Final attempt failed: {e}")
                raise
        except MCPToolError as e:
            # Don't retry tool errors - they're likely permanent
            print(f"Tool error (not retrying): {e}")
            raise
```

## Testing with MCP

### Unit Testing Patterns
```python
import unittest
from unittest.mock import patch, MagicMock
from lib.mcp_client_wrapper import call_yahoo_finance_tool

class TestMCPIntegration(unittest.TestCase):

    @patch('lib.mcp_client_wrapper.call_yahoo_finance_tool')
    def test_stock_fundamentals_collection(self, mock_mcp_call):
        # Mock MCP response
        mock_mcp_call.return_value = {
            "symbol": "AAPL",
            "current_price": 150.0,
            "market_cap": 2500000000000
        }

        # Test your function
        result = your_analysis_function("AAPL")

        # Verify MCP was called correctly
        mock_mcp_call.assert_called_with(
            "get_stock_fundamentals",
            {"symbol": "AAPL"}
        )

        # Verify result processing
        self.assertEqual(result["symbol"], "AAPL")
```

### Integration Testing
```python
def test_mcp_server_connectivity():
    """Test actual MCP server connectivity"""
    try:
        with MCPClientWrapper("yahoo-finance") as client:
            tools = client.list_tools()
            assert len(tools) > 0, "No tools available from MCP server"

            # Test a simple call
            result = client.call_tool("get_stock_fundamentals", {"symbol": "AAPL"})
            assert "symbol" in result, "Invalid response format"

        print("✅ MCP server connectivity test passed")
        return True
    except Exception as e:
        print(f"❌ MCP server connectivity test failed: {e}")
        return False
```

## Migration Guide

### Step 1: Identify Direct Service Usage
```bash
# Find files with direct imports (WRONG pattern)
grep -r "from yahoo_finance_service import" . --include="*.py"
grep -r "from.*service import" . --include="*.py"
grep -r "\.get_stock_info" . --include="*.py"
grep -r "\.get_historical_data" . --include="*.py"
```

### Step 2: Replace with MCP Calls
```python
# BEFORE (WRONG):
from yahoo_finance_service import YahooFinanceService
service = YahooFinanceService()
data = service.get_stock_info("AAPL")

# AFTER (CORRECT):
from lib.mcp_client_wrapper import call_yahoo_finance_tool
data = call_yahoo_finance_tool("get_stock_fundamentals", {"symbol": "AAPL"})
```

### Step 3: Update Error Handling
```python
# BEFORE (WRONG):
try:
    data = service.get_stock_info("AAPL")
except Exception as e:
    print(f"Error: {e}")

# AFTER (CORRECT):
try:
    data = call_yahoo_finance_tool("get_stock_fundamentals", {"symbol": "AAPL"})
except MCPError as e:
    print(f"MCP Error: {e}")
```

### Step 4: Validate Changes
```python
# Test script to validate MCP usage
def validate_mcp_migration():
    """Validate that MCP integration works correctly"""
    symbols = ["AAPL", "GOOGL", "MSFT"]

    for symbol in symbols:
        try:
            result = call_yahoo_finance_tool("get_stock_fundamentals", {"symbol": symbol})
            print(f"✅ {symbol}: MCP call successful")
        except MCPError as e:
            print(f"❌ {symbol}: MCP error - {e}")
            return False

    print("✅ All MCP validations passed")
    return True
```

## Enforcement and Prevention

### Code Review Checklist
- [ ] **No direct service imports** - Must use MCP client wrapper
- [ ] **Proper error handling** - Must catch MCP-specific errors
- [ ] **Context managers** - Use for multiple calls to same server
- [ ] **Tool naming** - Use correct MCP tool names
- [ ] **Argument format** - Use proper JSON arguments for tools

### Automated Checks
```python
# Add to pre-commit hooks or CI/CD
def check_mcp_compliance(file_path):
    """Check if file follows MCP-first patterns"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Check for anti-patterns
    anti_patterns = [
        "from yahoo_finance_service import",
        "from.*_service import",
        "YahooFinanceService()",
        ".get_stock_info(",
        ".get_historical_data("
    ]

    violations = []
    for pattern in anti_patterns:
        if re.search(pattern, content):
            violations.append(f"Found anti-pattern: {pattern}")

    # Check for correct patterns
    correct_patterns = [
        "from lib.mcp_client_wrapper import",
        "call_yahoo_finance_tool(",
        "MCPClientWrapper("
    ]

    has_financial_code = any(p in content for p in ["yahoo", "finance", "stock", "market"])
    has_correct_pattern = any(p in content for p in correct_patterns)

    if has_financial_code and not has_correct_pattern:
        violations.append("Financial code without MCP integration")

    return violations
```

### Linting Rules
```python
# .pylintrc additions
[MESSAGES CONTROL]
# Add custom rules for MCP compliance
disable=
enable=mcp-compliance-check

[mcp-compliance]
# Detect direct service imports
forbidden-imports=yahoo_finance_service,financial_service
# Require MCP patterns for financial code
required-patterns=mcp_client_wrapper
```

## Best Practices Summary

### ✅ DO
- **Use MCP client wrapper** for all external service calls
- **Handle MCP-specific errors** with proper exception types
- **Use context managers** for multiple calls to same server
- **Follow standardized argument formats** for MCP tools
- **Test MCP integration** with proper mocking and integration tests
- **Document MCP usage** in code comments and docstrings

### ❌ DON'T
- **Import services directly** - Always use MCP protocol
- **Mix MCP and direct calls** - Choose one approach consistently
- **Ignore MCP errors** - Always handle MCP-specific exceptions
- **Create new service instances** - Use existing MCP servers
- **Bypass MCP for "quick fixes"** - Maintain consistency
- **Hardcode server configurations** - Use centralized config

## Tools and Resources

### Development Tools
- **MCP Client Wrapper**: `lib/mcp_client_wrapper.py`
- **Integration Examples**: `examples/mcp_integration_examples.py`
- **Command Update Template**: `templates/mcp_command_update_template.py`
- **Fixed Test Script**: `test_rklb_data_mcp.py`

### Server Configurations
- **MCP Servers Config**: `mcp-servers.json`
- **Yahoo Finance Server**: `mcp_servers/yahoo_finance_server.py`
- **Sensylate Trading Server**: `mcp_servers/sensylate_trading_server.py`

### Validation Scripts
```bash
# Check MCP server status
python examples/mcp_integration_examples.py

# Test Yahoo Finance MCP
python test_rklb_data_mcp.py

# Validate command updates
python templates/mcp_command_update_template.py
```

## Conclusion

**MCP-First Development is now mandatory** for all Sensylate development. This approach ensures:

- **Consistency** across all data access patterns
- **Maintainability** through centralized server management
- **Observability** with full monitoring and logging
- **Performance** via centralized caching and rate limiting
- **Flexibility** to swap implementations without code changes

**Failure to follow MCP-First patterns will be considered a critical architectural violation.**

## Next Steps

1. **Immediate**: Fix all scripts currently bypassing MCP
2. **Short-term**: Implement automated compliance checking
3. **Medium-term**: Extend MCP patterns to all external integrations
4. **Long-term**: Build advanced MCP orchestration capabilities

---

**Questions?** Refer to examples in `examples/mcp_integration_examples.py` or the command update template in `templates/mcp_command_update_template.py`.
