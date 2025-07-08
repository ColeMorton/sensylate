# MCP Context Framework Specification
**Version**: 1.0
**Date**: 2025-07-06
**Status**: Production Ready

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Core Components](#core-components)
4. [Context Providers](#context-providers)
5. [Command Execution Framework](#command-execution-framework)
6. [Configuration System](#configuration-system)
7. [MCP Integration](#mcp-integration)
8. [Compliance and Enforcement](#compliance-and-enforcement)
9. [API Reference](#api-reference)
10. [Usage Patterns](#usage-patterns)
11. [Testing Framework](#testing-framework)
12. [Migration Guide](#migration-guide)
13. [Performance Considerations](#performance-considerations)
14. [Troubleshooting](#troubleshooting)

## Executive Summary

The MCP Context Framework is a comprehensive dependency injection and context management system for Sensylate that implements MCP-first development patterns with proper context decoupling. It transforms commands from tightly coupled, context-embedded implementations to pure functions that operate on injected context providers.

### Key Principles

1. **Context as First-Class Concern**: Context is treated as an architectural concern deserving explicit design attention
2. **MCP-First Development**: All external service access goes through MCP protocol
3. **Dependency Injection**: Commands receive all dependencies through constructor injection
4. **Fail-Fast Architecture**: Meaningful exceptions thrown immediately rather than fallback mechanisms
5. **Local Development Optimized**: Single environment focus with performance optimizations

### Benefits

- **Commands as Pure Functions**: Business logic separated from environmental concerns
- **Environment Flexibility**: Easy configuration changes without code modification
- **MCP Infrastructure ROI**: Full utilization of MCP server investments
- **Automated Quality Assurance**: 100% compliance enforcement through pre-commit hooks
- **Enhanced Testability**: Mock contexts instead of external services

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Sensylate Commands                      │
├─────────────────────────────────────────────────────────────┤
│                  Command Executor Layer                     │
├─────────────────────────────────────────────────────────────┤
│                   Context Provider Layer                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │     MCP     │  │    Data     │  │     Validation      │  │
│  │  Provider   │  │  Provider   │  │     Provider        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                     Context Layer                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │               LocalCommandContext                       │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐   │ │
│  │  │Execution│ │  Data   │ │   MCP   │ │ Validation  │   │ │
│  │  │Context  │ │Context  │ │Context  │ │  Context    │   │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────────┘   │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                  Configuration Layer                        │
│              (YAML Config + MCP Servers)                   │
├─────────────────────────────────────────────────────────────┤
│                    External Services                        │
│           (MCP Servers, File System, APIs)                 │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
sensylate/
├── context/                          # Context management framework
│   ├── __init__.py                   # Main context interface
│   ├── base_context.py              # Core context classes
│   ├── providers/                   # Specialized context providers
│   │   ├── __init__.py
│   │   ├── mcp_provider.py          # MCP server access
│   │   ├── data_provider.py         # File operations
│   │   └── validation_provider.py   # Quality validation
│   └── factories/                   # Context creation
│       ├── __init__.py
│       └── context_factory.py       # Configuration-based factory
├── commands/                        # Context-aware command execution
│   ├── __init__.py
│   ├── command_executor.py          # Base executor class
│   └── mcp_bridge.py               # MCP tool discovery
├── config/                         # Configuration files
│   └── local_context.yaml          # Local development config
├── scripts/                        # Enforcement and utilities
│   └── check_mcp_compliance.py     # Compliance checker
├── tests/context/                  # Framework tests
│   └── test_context_integration.py # Integration tests
└── .pre-commit-config-mcp.yaml     # Pre-commit enforcement
```

## Core Components

### LocalCommandContext

The primary dependency injection container for all command execution.

```python
@dataclasses.dataclass
class LocalCommandContext:
    execution: ExecutionContext      # Command execution environment
    data: DataContext               # File operations and data management
    mcp: MCPContext                # MCP server access configuration
    validation: ValidationContext   # Data quality and compliance rules
    metadata: Dict[str, Any]        # Additional metadata
```

**Key Methods**:
- `get_command_output_path()` - Get standardized output path for command
- `create_child_context()` - Create child context for sub-commands
- `to_dict()` - Serialize context for logging/debugging

### Context Types

#### ExecutionContext
Manages command execution environment and lifecycle.

```python
@dataclasses.dataclass
class ExecutionContext:
    timestamp: datetime             # Execution start time
    command_name: str              # Name of executing command
    working_directory: Path        # Command working directory
    timeout: int = 300            # Execution timeout in seconds
    environment: str = "local"     # Environment identifier
    user_id: Optional[str] = None  # User identifier
    session_id: Optional[str] = None # Session identifier
```

#### DataContext
Handles file operations, caching, and data organization.

```python
@dataclasses.dataclass
class DataContext:
    base_output_path: Path         # Base directory for outputs
    cache_enabled: bool = True     # Enable response caching
    backup_enabled: bool = True    # Enable automatic backups
    temp_cleanup: bool = True      # Clean temporary files
    file_permissions: int = 0o644  # Default file permissions
```

#### MCPContext
Manages MCP server access and configuration.

```python
@dataclasses.dataclass
class MCPContext:
    config_path: Path                    # Path to mcp-servers.json
    available_servers: List[str]         # List of configured servers
    health_check_enabled: bool = True    # Enable health monitoring
    health_check_interval: int = 300     # Health check frequency (seconds)
    retry_policy: RetryPolicy = EXPONENTIAL # Retry strategy
    retry_attempts: int = 3              # Maximum retry attempts
    timeout: int = 60                    # Request timeout (seconds)
    cache_responses: bool = True         # Enable response caching
```

#### ValidationContext
Defines data quality and compliance requirements.

```python
@dataclasses.dataclass
class ValidationContext:
    confidence_threshold: float = 0.8         # Minimum confidence score
    quality_gates: QualityGate = STANDARD     # Quality enforcement level
    format_validation: bool = True            # Enable format validation
    institutional_target: float = 9.5         # Institutional quality target
    strict_formatting: bool = True            # Enforce strict formatting
```

### Quality Gates

```python
class QualityGate(Enum):
    MINIMAL = "minimal"        # Basic validation only
    STANDARD = "standard"      # Standard quality requirements
    STRICT = "strict"          # High quality requirements
    INSTITUTIONAL = "institutional" # Institutional-grade quality
```

### Retry Policies

```python
class RetryPolicy(Enum):
    NONE = "none"              # No retries
    LINEAR = "linear"          # Linear backoff (1s, 2s, 3s)
    EXPONENTIAL = "exponential" # Exponential backoff (1s, 2s, 4s, 8s)
```

## Context Providers

### MCPContextProvider

Unified MCP server access with health monitoring and error handling.

```python
class MCPContextProvider:
    def __init__(self, mcp_context: MCPContext)

    # Server Management
    def get_available_servers() -> List[str]
    def is_server_configured(server_name: str) -> bool
    def get_server_health(server_name: str) -> ServerHealth

    # Tool Discovery
    def discover_all_tools() -> Dict[str, List[MCPToolInfo]]
    def find_tool(tool_name: str) -> Optional[MCPToolInfo]

    # Client Access
    def get_client(server_name: str) -> MCPClientWrapper
    def call_tool_with_retry(server_name: str, tool_name: str, arguments: Dict) -> Any

    # Health Monitoring
    def get_health_summary() -> Dict[str, Any]
```

**Key Features**:
- Automatic server health monitoring
- Intelligent caching (5-minute TTL)
- Retry logic with exponential backoff
- Tool discovery across all servers
- Connection pooling and reuse

### DataContextProvider

File operations, caching, and data organization management.

```python
class DataContextProvider:
    def __init__(self, data_context: DataContext)

    # Path Management
    def get_output_path(category: str, subcategory: str = None) -> Path
    def generate_filename(base_name: str, extension: str = "json") -> str

    # File Operations
    def save_json_output(data: Dict, output_path: Path, filename: str) -> Path
    def load_json_input(file_path: Path) -> Dict[str, Any]
    def save_markdown_output(content: str, output_path: Path, filename: str) -> Path

    # Caching
    def cache_data(key: str, data: Any, ttl_seconds: int = 3600) -> Path
    def get_cached_data(key: str) -> Optional[Any]
    def clear_cache(pattern: str = None)

    # Maintenance
    def cleanup_temp_files()
    def get_storage_summary() -> Dict[str, Any]
```

**Key Features**:
- Automatic directory structure creation
- Backup management with versioning
- TTL-based caching system
- File metadata tracking
- Storage usage monitoring

### ValidationContextProvider

Data quality assessment and compliance checking.

```python
class ValidationContextProvider:
    def __init__(self, validation_context: ValidationContext)

    # Validation Methods
    def validate_fundamental_data(data: Dict, ticker: str = None) -> ValidationResult
    def validate_ticker_symbol(ticker: str) -> ValidationResult
    def validate_json_format(data: Any, schema: Dict = None) -> ValidationResult

    # Quality Assessment
    def get_validation_summary(results: List[ValidationResult]) -> Dict[str, Any]
```

**Validation Types**:
- **Structure Validation**: Required fields and data types
- **Format Validation**: Precision, ranges, and formatting rules
- **Content Validation**: Business logic and data consistency
- **Quality Gate Enforcement**: Confidence thresholds and error limits

## Command Execution Framework

### CommandExecutor

Base class for all context-aware command implementations.

```python
class CommandExecutor(ABC):
    def __init__(self, context: LocalCommandContext)

    # Abstract Methods (implement in subclasses)
    @abstractmethod
    def execute_command(self, **kwargs) -> Dict[str, Any]

    # Framework Methods
    def execute(self, **kwargs) -> Dict[str, Any]  # Main execution with error handling
    def save_result(result: Dict, filename: str = None) -> Path
    def get_mcp_client(server_name: str) -> MCPClientWrapper
    def cache_data(key: str, data: Any) -> Path
    def get_cached_data(key: str) -> Optional[Any]
```

**Usage Pattern**:

```python
class MyCommandExecutor(CommandExecutor):
    def execute_command(self, ticker: str) -> Dict[str, Any]:
        # Input validation
        ticker_validation = self.validation_provider.validate_ticker_symbol(ticker)
        if not ticker_validation.is_valid:
            raise CommandExecutionError(f"Invalid ticker: {ticker}")

        # Use MCP for data access
        with self.get_mcp_client("yahoo-finance") as client:
            fundamentals = client.call_tool("get_stock_fundamentals", {"ticker": ticker})

        # Use context for file operations
        result = {"ticker": ticker, "data": fundamentals}
        return result
```

### MCPBridge

Tool discovery and capability mapping for commands.

```python
class MCPBridge:
    def __init__(self, mcp_provider: MCPContextProvider)

    # Capability Discovery
    def discover_all_capabilities() -> Dict[str, Any]
    def get_command_mapping(command_name: str) -> Optional[ToolMapping]
    def resolve_tools(requirements: List[MCPToolRequirement]) -> Dict[str, Any]

    # Validation and Planning
    def validate_command_requirements(command_name: str) -> Dict[str, Any]
    def get_optimal_execution_plan(command_name: str) -> Dict[str, Any]
    def get_command_coverage_report() -> Dict[str, Any]
```

**Tool Requirement Types**:

```python
class ToolRequirementType(Enum):
    REQUIRED = "required"    # Must be available for command to execute
    OPTIONAL = "optional"    # Enhances command but not required
    FALLBACK = "fallback"    # Used only when primary tools fail
```

## Configuration System

### YAML Configuration Structure

```yaml
# config/local_context.yaml
execution:
  environment: local
  working_directory: /Users/colemorton/Projects/sensylate
  timeout: 300
  session_management: true

data:
  base_output_path: ./data/outputs
  cache_enabled: true
  backup_enabled: true
  temp_cleanup: true
  file_permissions: 0o644

mcp:
  config_path: ./mcp-servers.json
  health_check_enabled: true
  health_check_interval: 300
  retry_policy: exponential
  retry_attempts: 3
  timeout: 60
  cache_responses: true

  server_priorities:
    - yahoo-finance
    - sensylate-trading
    - sec-edgar

validation:
  confidence_threshold: 0.8
  quality_gates: standard
  format_validation: true
  institutional_target: 9.5
  strict_formatting: true

# Command-specific overrides
command_overrides:
  fundamental_analyst_discover:
    validation:
      quality_gates: institutional
      institutional_target: 9.5
    data:
      backup_enabled: true
```

### ContextFactory

Configuration-based context creation with validation.

```python
class ContextFactory:
    def __init__(self, config_path: Path = None)

    # Context Creation
    def create_context(command_name: str, overrides: Dict = None) -> LocalCommandContext
    def get_command_config(command_name: str) -> Dict[str, Any]
    def list_configured_commands() -> List[str]

    # Configuration Management
    def validate_config() -> List[str]  # Returns list of validation issues
```

**Usage**:

```python
# Simple context creation
context = create_local_context("my_command")

# With custom configuration
factory = ContextFactory("config/custom_context.yaml")
context = factory.create_context("my_command", {
    "validation": {"confidence_threshold": 0.9}
})
```

## MCP Integration

### Server Configuration

The framework integrates with Sensylate's existing MCP servers through standardized configuration:

```json
{
  "mcpServers": {
    "yahoo-finance": {
      "command": "python",
      "args": ["mcp_servers/yahoo_finance_server.py"],
      "description": "Yahoo Finance data standardization"
    },
    "sensylate-trading": {
      "command": "python",
      "args": ["mcp_servers/sensylate_trading_server.py"],
      "description": "Sensylate trading analysis tools"
    },
    "sec-edgar": {
      "command": "python",
      "args": ["mcp_servers/sec_edgar_server.py"],
      "description": "SEC EDGAR filing data access"
    }
  }
}
```

### Tool Mappings

Commands declare their MCP tool requirements through mappings:

```python
fundamental_analyst_discover = ToolMapping(
    command_name="fundamental_analyst_discover",
    requirements=[
        MCPToolRequirement(
            server="yahoo-finance",
            tool="get_stock_fundamentals",
            requirement_type=ToolRequirementType.REQUIRED,
            parameters={"ticker": "string"}
        ),
        MCPToolRequirement(
            server="sec-edgar",
            tool="get_company_filings",
            requirement_type=ToolRequirementType.OPTIONAL,
            parameters={"ticker": "string", "filing_type": "string"}
        )
    ],
    server_preferences=["yahoo-finance", "sec-edgar"]
)
```

### Client Wrapper

Context manager for safe MCP client operations:

```python
# Automatic connection management
with mcp_provider.get_client("yahoo-finance") as client:
    # List available tools
    tools = client.list_tools()

    # Call tools with error handling
    result = client.call_tool("get_stock_fundamentals", {"ticker": "AAPL"})

    # Health monitoring
    health = client.get_server_health()
```

## Compliance and Enforcement

### MCP Compliance Checker

Comprehensive static analysis tool for enforcing MCP-first patterns:

```bash
# Command-line usage
python scripts/check_mcp_compliance.py                    # Check all files
python scripts/check_mcp_compliance.py file.py           # Check specific file
python scripts/check_mcp_compliance.py --report          # Generate report
python scripts/check_mcp_compliance.py --json            # JSON output
```

### Violation Types

The compliance checker detects seven types of violations:

1. **DIRECT_SERVICE_IMPORT**: Direct service imports bypassing MCP
2. **HARDCODED_PATH**: Hardcoded file paths violating context decoupling
3. **NO_CONTEXT_INJECTION**: Financial code without context injection
4. **MIXED_MCP_DIRECT**: Mixing MCP and direct service patterns
5. **MISSING_ERROR_HANDLING**: MCP calls without proper error handling
6. **CONTEXT_COUPLING**: Commands with embedded context information
7. **ANTI_PATTERN**: Other architectural anti-patterns

### Severity Levels

```python
class Severity(Enum):
    ERROR = "error"      # Blocks CI/CD pipeline
    WARNING = "warning"  # Allows pipeline but flags for review
    INFO = "info"        # Informational only
```

### Pre-commit Integration

Automatic enforcement through pre-commit hooks:

```yaml
- repo: local
  hooks:
    - id: mcp-compliance
      name: MCP Compliance Check
      entry: python scripts/check_mcp_compliance.py
      language: python
      files: '\.(py|md)$'
      pass_filenames: true
      args: ['--verbose']
```

**Installation**:

```bash
pre-commit install --config .pre-commit-config-mcp.yaml
```

## API Reference

### Context Creation

```python
# Simple factory function
def create_local_context(
    command_name: str,
    working_directory: Path = None,
    base_output_path: Path = None,
    mcp_config_path: Path = None,
    **kwargs
) -> LocalCommandContext

# Advanced factory class
class ContextFactory:
    def create_context(
        command_name: str,
        overrides: Dict[str, Any] = None,
        working_directory: Path = None
    ) -> LocalCommandContext
```

### Provider Interfaces

```python
# MCP Provider
class MCPContextProvider:
    def get_client(server_name: str) -> MCPClientWrapper
    def call_tool_with_retry(server: str, tool: str, args: Dict) -> Any
    def discover_all_tools() -> Dict[str, List[MCPToolInfo]]
    def get_health_summary() -> Dict[str, Any]

# Data Provider
class DataContextProvider:
    def get_output_path(category: str, subcategory: str = None) -> Path
    def save_json_output(data: Dict, path: Path, filename: str) -> Path
    def cache_data(key: str, data: Any, ttl: int = 3600) -> Path
    def get_cached_data(key: str) -> Optional[Any]

# Validation Provider
class ValidationContextProvider:
    def validate_fundamental_data(data: Dict, ticker: str = None) -> ValidationResult
    def validate_ticker_symbol(ticker: str) -> ValidationResult
    def validate_json_format(data: Any, schema: Dict = None) -> ValidationResult
```

### Command Execution

```python
# Base executor class
class CommandExecutor(ABC):
    @abstractmethod
    def execute_command(self, **kwargs) -> Dict[str, Any]

    def execute(self, **kwargs) -> Dict[str, Any]
    def save_result(result: Dict, filename: str = None) -> Path
    def get_mcp_client(server_name: str) -> MCPClientWrapper

# Convenience factory
def create_command_executor(command_name: str) -> CommandExecutor
```

## Usage Patterns

### Pattern 1: Simple Command Implementation

```python
from context import create_local_context
from commands import CommandExecutor

class SimpleAnalysisExecutor(CommandExecutor):
    def execute_command(self, ticker: str) -> Dict[str, Any]:
        # Validate input
        validation = self.validation_provider.validate_ticker_symbol(ticker)
        if not validation.is_valid:
            raise CommandExecutionError(f"Invalid ticker: {ticker}")

        # Get data via MCP
        with self.get_mcp_client("yahoo-finance") as client:
            data = client.call_tool("get_stock_fundamentals", {"ticker": ticker})

        return {"ticker": ticker, "analysis": data}

# Usage
context = create_local_context("simple_analysis")
executor = SimpleAnalysisExecutor(context)
result = executor.execute(ticker="AAPL")
```

### Pattern 2: Multi-Source Data Collection

```python
class ComprehensiveAnalysisExecutor(CommandExecutor):
    def execute_command(self, ticker: str, depth: str = "standard") -> Dict[str, Any]:
        analysis_data = {"ticker": ticker, "sources": []}

        # Yahoo Finance (required)
        try:
            with self.get_mcp_client("yahoo-finance") as client:
                fundamentals = client.call_tool("get_stock_fundamentals", {"ticker": ticker})
                analysis_data["yahoo_finance"] = fundamentals
                analysis_data["sources"].append("yahoo_finance")
        except Exception as e:
            raise CommandExecutionError(f"Required Yahoo Finance data failed: {e}")

        # SEC EDGAR (optional)
        try:
            with self.get_mcp_client("sec-edgar") as client:
                filings = client.call_tool("get_company_filings", {"ticker": ticker})
                analysis_data["sec_edgar"] = filings
                analysis_data["sources"].append("sec_edgar")
        except Exception as e:
            logger.warning(f"SEC EDGAR data unavailable: {e}")

        # Validate and save
        validation = self.validation_provider.validate_fundamental_data(analysis_data, ticker)
        if not validation.is_valid:
            raise CommandExecutionError("Data validation failed")

        return analysis_data
```

### Pattern 3: Cached Analysis

```python
class CachedAnalysisExecutor(CommandExecutor):
    def execute_command(self, ticker: str, force_refresh: bool = False) -> Dict[str, Any]:
        cache_key = f"analysis_{ticker}_{self.context.execution.timestamp.date()}"

        # Check cache first
        if not force_refresh:
            cached_result = self.get_cached_data(cache_key)
            if cached_result:
                logger.info(f"Using cached analysis for {ticker}")
                return cached_result

        # Perform fresh analysis
        analysis_data = self._perform_analysis(ticker)

        # Cache result
        self.cache_data(cache_key, analysis_data, ttl_seconds=3600)  # 1 hour cache

        return analysis_data

    def _perform_analysis(self, ticker: str) -> Dict[str, Any]:
        # Implementation here
        pass
```

### Pattern 4: Batch Processing

```python
class BatchAnalysisExecutor(CommandExecutor):
    def execute_command(self, tickers: List[str], parallel: bool = True) -> Dict[str, Any]:
        results = {"successful": [], "failed": []}

        for ticker in tickers:
            try:
                # Create child context for each ticker
                child_context = self.context.create_child_context(
                    f"batch_analysis_{ticker}"
                )

                # Process individual ticker
                ticker_result = self._analyze_single_ticker(ticker)
                results["successful"].append({
                    "ticker": ticker,
                    "result": ticker_result
                })

            except Exception as e:
                logger.error(f"Failed to analyze {ticker}: {e}")
                results["failed"].append({
                    "ticker": ticker,
                    "error": str(e)
                })

        return results
```

## Testing Framework

### Integration Tests

```python
import pytest
from context import create_local_context
from context.providers import MCPContextProvider, DataContextProvider

class TestContextIntegration:
    def test_context_creation(self):
        context = create_local_context("test_command")
        assert context.execution.command_name == "test_command"
        assert context.data.cache_enabled == True

    def test_mcp_provider_initialization(self):
        context = create_local_context("test_command")
        mcp_provider = MCPContextProvider(context.mcp)

        servers = mcp_provider.get_available_servers()
        assert isinstance(servers, list)

    def test_data_provider_operations(self):
        context = create_local_context("test_command")
        data_provider = DataContextProvider(context.data)

        # Test path creation
        path = data_provider.get_output_path("test_category")
        assert path.exists()

        # Test file operations
        test_data = {"test": "data"}
        saved_path = data_provider.save_json_output(
            test_data, path, "test.json"
        )
        assert saved_path.exists()

        loaded_data = data_provider.load_json_input(saved_path)
        assert loaded_data == test_data
```

### Unit Tests

```python
import pytest
from unittest.mock import Mock, patch
from context.providers.validation_provider import ValidationContextProvider
from context.base_context import ValidationContext, QualityGate

class TestValidationProvider:
    def setup_method(self):
        validation_context = ValidationContext(
            confidence_threshold=0.8,
            quality_gates=QualityGate.STANDARD
        )
        self.provider = ValidationContextProvider(validation_context)

    def test_ticker_validation_valid(self):
        result = self.provider.validate_ticker_symbol("AAPL")
        assert result.is_valid
        assert result.confidence_score == 1.0

    def test_ticker_validation_invalid(self):
        result = self.provider.validate_ticker_symbol("")
        assert not result.is_valid
        assert len(result.issues) > 0
```

### Mock Providers

```python
class MockMCPProvider:
    def __init__(self):
        self.mock_responses = {}

    def set_mock_response(self, server: str, tool: str, response: Any):
        key = f"{server}:{tool}"
        self.mock_responses[key] = response

    def get_client(self, server_name: str):
        return MockMCPClient(server_name, self.mock_responses)

class MockMCPClient:
    def __init__(self, server_name: str, responses: Dict):
        self.server_name = server_name
        self.responses = responses

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        key = f"{self.server_name}:{tool_name}"
        if key in self.responses:
            return self.responses[key]
        raise Exception(f"No mock response for {key}")
```

## Migration Guide

### Step 1: Identify Files for Migration

```bash
# Find files with direct service imports
python scripts/check_mcp_compliance.py --report
```

### Step 2: Update Imports

```python
# Before (WRONG)
from yahoo_finance_service import YahooFinanceService
from scripts.data_extraction import extract_financial_data

# After (CORRECT)
from context import create_local_context
from commands import CommandExecutor
```

### Step 3: Convert to CommandExecutor

```python
# Before (WRONG)
def analyze_stock(ticker: str):
    service = YahooFinanceService()
    data = service.get_stock_info(ticker)

    output_path = "./data/outputs/fundamental_analysis/"
    with open(f"{output_path}/{ticker}_analysis.json", "w") as f:
        json.dump(data, f)

    return data

# After (CORRECT)
class StockAnalysisExecutor(CommandExecutor):
    def execute_command(self, ticker: str) -> Dict[str, Any]:
        # Use MCP for data access
        with self.get_mcp_client("yahoo-finance") as client:
            data = client.call_tool("get_stock_fundamentals", {"ticker": ticker})

        # Use context for file operations
        self.save_result(data, f"{ticker}_analysis.json")

        return data

# Usage
context = create_local_context("stock_analysis")
executor = StockAnalysisExecutor(context)
result = executor.execute(ticker="AAPL")
```

### Step 4: Update Command Markdown Files

```markdown
<!-- Before (WRONG) -->
**Output Location**: `./data/outputs/fundamental_analysis/discovery/`
**File Naming**: `{TICKER}_{YYYYMMDD}_discovery.json`

<!-- After (CORRECT) -->
**Output Location**: `{{context.data.output_path}}/{{context.command.category}}/`
**File Naming**: `{{context.command.file_template}}`
```

### Step 5: Configuration Updates

Create command-specific configuration overrides:

```yaml
# config/local_context.yaml
command_overrides:
  your_command_name:
    validation:
      quality_gates: institutional
    data:
      category: fundamental_analysis
      subcategory: discovery
```

## Performance Considerations

### Caching Strategy

The framework implements multi-level caching:

1. **MCP Response Cache**: 5-minute TTL for tool responses
2. **Data Provider Cache**: 1-hour TTL for processed data
3. **Health Check Cache**: 5-minute TTL for server health

### Connection Pooling

- MCP clients are reused within context manager scope
- Server connections pooled per provider instance
- Automatic cleanup on context exit

### Memory Management

- Contexts are garbage collected after command completion
- Large data sets use file-based caching instead of memory
- Temporary files automatically cleaned up

### Performance Monitoring

```python
# Get performance metrics
health_summary = mcp_provider.get_health_summary()
storage_summary = data_provider.get_storage_summary()
cache_stats = data_provider.get_cache_stats()
```

## Troubleshooting

### Common Issues

#### 1. MCP Server Not Available

**Symptoms**: `MCPConnectionError: Server yahoo-finance is not configured`

**Solutions**:
- Check `mcp-servers.json` configuration
- Verify server command paths
- Run health check: `mcp_provider.get_server_health("yahoo-finance")`

#### 2. Context Configuration Errors

**Symptoms**: `ContextConfigurationError: Invalid YAML in config file`

**Solutions**:
- Validate YAML syntax
- Use `factory.validate_config()` to check configuration
- Check file permissions and paths

#### 3. Validation Failures

**Symptoms**: `ValidationError: Data validation failed`

**Solutions**:
- Check validation rules and thresholds
- Review quality gate settings
- Use `validate_fundamental_data()` for detailed error information

#### 4. Permission Errors

**Symptoms**: `PermissionError: Cannot write to output directory`

**Solutions**:
- Check directory permissions
- Verify `file_permissions` setting in context
- Ensure output directory exists and is writable

### Debug Mode

Enable debug logging for detailed troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable specific debug modes
context = create_local_context("debug_command", **{
    "development": {
        "debug_mode": True,
        "verbose_logging": True,
        "validation_debug": True
    }
})
```

### Health Checks

```python
# Comprehensive system health check
def system_health_check():
    context = create_local_context("health_check")

    # MCP health
    mcp_provider = MCPContextProvider(context.mcp)
    mcp_health = mcp_provider.get_health_summary()

    # Storage health
    data_provider = DataContextProvider(context.data)
    storage_health = data_provider.get_storage_summary()

    # Configuration health
    factory = ContextFactory()
    config_issues = factory.validate_config()

    return {
        "mcp": mcp_health,
        "storage": storage_health,
        "config_issues": config_issues,
        "overall_healthy": len(config_issues) == 0 and mcp_health["overall_health"] == "healthy"
    }
```

---

## Conclusion

The MCP Context Framework provides a comprehensive, production-ready foundation for MCP-first development in Sensylate. It successfully decouples context from commands while providing powerful abstractions for MCP integration, data management, and quality assurance.

### Key Benefits Delivered

- **Architecture Consistency**: Uniform patterns across all commands
- **MCP Infrastructure ROI**: Full utilization of MCP server investments
- **Development Velocity**: Faster command creation and modification
- **Quality Assurance**: Automated enforcement of best practices
- **Maintainability**: Centralized configuration and context management

### Production Readiness

The framework is immediately ready for production use with:
- Comprehensive error handling and logging
- Performance optimizations for local development
- Automated testing and validation
- Complete documentation and examples
- Migration tools and patterns

This specification serves as the definitive guide for understanding, using, and extending the MCP Context Framework within the Sensylate ecosystem.

**Framework Version**: 1.0
**Specification Complete**: 2025-07-06
**Status**: ✅ Production Ready
