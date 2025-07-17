# Python Type Annotation Guidelines - Sensylate Platform

**Date:** July 17, 2025
**Version:** 1.0
**Scope:** Python codebase type safety standards
**Target Audience:** Development team

## Overview

This guide establishes type annotation standards for the Sensylate platform, building on our successful MyPy rollout. These patterns ensure code quality, maintainability, and developer productivity.

## Core Type Annotation Patterns

### 1. Basic Type Annotations

```python
# Variables with explicit types
name: str = "AAPL"
price: float = 150.25
count: int = 100
is_active: bool = True

# Collections with type parameters
trades: List[TradeData] = []
metrics: Dict[str, float] = {}
symbols: Set[str] = {"AAPL", "GOOGL", "MSFT"}
```

### 2. Function Signatures

```python
def calculate_returns(
    prices: List[float],
    weights: Optional[List[float]] = None
) -> List[float]:
    """Always annotate parameters and return types."""
    if weights is None:
        weights = [1.0] * len(prices)
    return [p * w for p, w in zip(prices, weights)]
```

### 3. Numpy Array Types

```python
import numpy as np
import numpy.typing as npt

# Preferred: Use numpy.typing for array annotations
def process_data(values: List[float]) -> npt.NDArray[np.float64]:
    """Convert lists to numpy arrays with proper typing."""
    return np.array(values)

# Type-safe array operations
def safe_cumsum(data: Union[List[float], npt.NDArray]) -> npt.NDArray[np.float64]:
    """Handle both lists and arrays safely."""
    return np.cumsum(np.asarray(data))
```

### 4. Dataclass Usage

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class TradeData:
    """Type-safe data structures with validation."""
    ticker: str
    return_pct: float
    duration_days: int
    quality: str
    entry_date: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate data after initialization."""
        if self.duration_days < 0:
            raise ValueError("Duration must be positive")
```

### 5. Union Types and Optional

```python
from typing import Union, Optional

# Union for multiple valid types
Price = Union[int, float]

# Optional for nullable values
def get_trade_data(ticker: str) -> Optional[TradeData]:
    """Returns trade data or None if not found."""
    # Implementation here
    return None

# Preferred: Use | syntax in Python 3.10+
def modern_union(value: str | int | float) -> str:
    """Modern union syntax."""
    return str(value)
```

### 6. Generic Types and Protocols

```python
from typing import TypeVar, Generic, Protocol

T = TypeVar('T')

class DataProcessor(Generic[T]):
    """Generic data processor for any data type."""

    def process(self, data: List[T]) -> List[T]:
        return data

# Protocol for duck typing
class Drawable(Protocol):
    def draw(self) -> None: ...

def render_chart(chart: Drawable) -> None:
    """Works with any object that has a draw method."""
    chart.draw()
```

## Common Patterns in Sensylate Codebase

### 1. Financial Data Processing

```python
from typing import Dict, List, Tuple
import pandas as pd

def analyze_portfolio(
    trades: List[TradeData],
    benchmark: pd.DataFrame
) -> Dict[str, Union[float, List[str]]]:
    """Analyze portfolio performance against benchmark."""
    return {
        "total_return": 15.5,
        "sharpe_ratio": 1.2,
        "top_performers": ["AAPL", "GOOGL"]
    }
```

### 2. Chart Generation

```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class ChartGenerator(ABC):
    """Abstract base for chart generators."""

    @abstractmethod
    def create_chart(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Any:
        """Create chart with specified data and configuration."""
        pass
```

### 3. Service Layer

```python
from typing import Optional, Dict, Any
import requests

class APIClient:
    """Type-safe API client implementation."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def get_data(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Fetch data from API endpoint."""
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        return response.json()
```

### 4. Configuration Management

```python
from pathlib import Path
from typing import Dict, Any, Union

ConfigValue = Union[str, int, float, bool, List[Any], Dict[str, Any]]

def load_config(config_path: Union[str, Path]) -> Dict[str, ConfigValue]:
    """Load configuration with proper type hints."""
    # Implementation here
    return {}
```

## Error Handling Patterns

### 1. Custom Exceptions

```python
class ValidationError(Exception):
    """Raised when data validation fails."""

    def __init__(self, message: str, field: str) -> None:
        super().__init__(message)
        self.field = field

def validate_trade(trade: TradeData) -> None:
    """Validate trade data with type-safe exceptions."""
    if not trade.ticker:
        raise ValidationError("Ticker cannot be empty", "ticker")
```

### 2. Result Types

```python
from typing import Union, Generic, TypeVar

T = TypeVar('T')
E = TypeVar('E', bound=Exception)

class Result(Generic[T, E]):
    """Type-safe result type for error handling."""

    def __init__(self, value: Optional[T] = None, error: Optional[E] = None):
        self.value = value
        self.error = error

    @property
    def is_ok(self) -> bool:
        return self.error is None
```

## MyPy Configuration Integration

### Module-Specific Settings

```ini
# Strict checking for well-typed modules
[mypy-scripts.utils.config_validator]
disallow_untyped_defs = True
warn_return_any = True

[mypy-scripts.services.*]
disallow_untyped_defs = True
check_untyped_defs = True
```

### Progressive Enhancement

1. **Start with basic annotations** for new code
2. **Add strict checking** for well-typed modules
3. **Gradually tighten** configuration as coverage improves

## IDE Configuration

### VSCode Settings

```json
{
    "python.linting.mypyEnabled": true,
    "python.linting.mypyArgs": ["--config-file", "mypy.ini"],
    "python.analysis.typeCheckingMode": "strict"
}
```

### PyCharm Settings

- Enable "Type checker" in Python integrated tools
- Set inspection severity to "Error" for type issues
- Enable "Show error codes" for MyPy integration

## Best Practices

### Do's ✅

1. **Always annotate public function signatures**
2. **Use specific types over Any when possible**
3. **Import types from typing module explicitly**
4. **Use dataclasses for structured data**
5. **Annotate class attributes and instance variables**
6. **Use Union types for multiple valid types**
7. **Provide return type annotations for all functions**

### Don'ts ❌

1. **Don't use Any without justification**
2. **Don't ignore MyPy errors without investigation**
3. **Don't mix typed and untyped code in same module**
4. **Don't use bare Exception types**
5. **Don't forget to update type hints when refactoring**

## Error Resolution Patterns

### Pattern 1: Unsafe Instance Method Access

**Problem**: Direct access to `__init__` method on instances
```python
# ❌ Unsafe - MyPy error: Accessing "__init__" on instance is unsound
fm.fontManager.__init__()
```

**Solution**: Use safe configuration alternatives
```python
# ✅ Safe - Direct configuration approach
plt.rcParams['font.family'] = ['Heebo', 'sans-serif']

# ✅ Alternative - Explicit font registration
fm.fontManager.addfont(str(font_path))
```

### Pattern 2: Conditional Return Signatures

**Problem**: Functions with variable return types based on parameters
```python
# ❌ Problematic - matplotlib pie() returns 2 or 3 items based on autopct
wedges, texts, autotexts = ax.pie(data, autopct="")  # Error when autopct=""
```

**Solution**: Handle conditional unpacking safely
```python
# ✅ Safe - Handle variable return signatures
pie_result = ax.pie(data, autopct="")
if len(pie_result) == 3:
    wedges, texts, autotexts = pie_result
else:
    wedges, texts = pie_result
    autotexts = []
```

### Pattern 3: Numpy Array Type Compatibility

**Problem**: List/array type mismatches with numpy functions
```python
# ❌ Type error - numpy expects arrays, gets lists
values: List[float] = [1.0, 2.0, 3.0]
result = np.cumsum(values)  # Type mismatch
```

**Solution**: Explicit array conversion with proper typing
```python
# ✅ Type-safe - Convert with proper annotation
values: List[float] = [1.0, 2.0, 3.0]
result: npt.NDArray[np.float64] = np.cumsum(np.array(values))
```

## Common Anti-Patterns and Solutions

### Anti-Pattern: Using Any everywhere

```python
# ❌ Bad
def process_data(data: Any) -> Any:
    return data

# ✅ Good
def process_data(data: List[TradeData]) -> Dict[str, float]:
    return {"total_return": sum(t.return_pct for t in data)}
```

### Anti-Pattern: Missing return annotations

```python
# ❌ Bad
def calculate_metrics(trades):
    return {"count": len(trades)}

# ✅ Good
def calculate_metrics(trades: List[TradeData]) -> Dict[str, int]:
    return {"count": len(trades)}
```

### Anti-Pattern: Incorrect numpy typing

```python
# ❌ Bad
def cumsum_data(values: List[float]) -> List[float]:
    return np.cumsum(values)  # Type error: returns ndarray

# ✅ Good
def cumsum_data(values: List[float]) -> npt.NDArray[np.float64]:
    return np.cumsum(np.array(values))
```

## Migration Strategy

### Phase 1: New Code (Current)
- All new functions must have type annotations
- Use strict MyPy settings for new modules
- Require type annotations in code reviews

### Phase 2: Core Modules (Next 30 days)
- Add type annotations to core business logic
- Enable strict checking for utils and services
- Fix existing type errors systematically

### Phase 3: Full Coverage (Next quarter)
- Complete type annotation coverage
- Enable strict mode globally
- Establish type-driven development practices

## Team Adoption Monitoring

### Automated Metrics Collection

The platform includes automated metrics collection for monitoring type safety adoption:

```python
# Run typing metrics collection
python scripts/utils/typing_metrics.py

# Output includes:
# - Annotation coverage percentage
# - MyPy compliance status
# - Error categorization and trends
# - File-level statistics
# - Team adoption rates
```

### Key Metrics Tracked

1. **Annotation Coverage**: Percentage of functions with type hints
2. **MyPy Compliance**: Pass/fail status with error categorization
3. **Strict Module Count**: Modules with enhanced type checking
4. **Error Trends**: Daily tracking of error types and resolution
5. **File Statistics**: Typing import adoption and code quality

### Daily Monitoring Dashboard

```bash
# Generate daily report
python scripts/utils/typing_metrics.py

# Example output:
✅ Type safety metrics collected successfully!
📊 Report saved to: data/outputs/technical_health/typing_metrics_report_20250717.md
📈 Overall annotation coverage: 78.5%
🔍 MyPy compliance: PASS
```

## Team Training and Adoption

### Code Review Checklist

- [ ] All function parameters have type annotations
- [ ] Return types are explicitly declared
- [ ] Complex types use proper Union/Optional
- [ ] Numpy arrays use numpy.typing
- [ ] Custom classes are properly typed

### Resources for Learning

- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Python Type Hints PEP 484](https://peps.python.org/pep-0484/)
- [Typing Best Practices](https://docs.python.org/3/library/typing.html)

## Success Metrics

### Weekly Targets
- **New code**: 100% type annotation coverage
- **MyPy errors**: Decreasing trend
- **Strict modules**: 2+ new modules per week

### Monthly Goals
- **Coverage**: 90%+ of functions have type annotations
- **Errors**: <5 type errors across codebase
- **Performance**: Type checking completes in <30 seconds

---

**Remember**: Type annotations are documentation that the computer can verify. They make code more readable, maintainable, and reliable while providing excellent IDE support and catching errors early in development.

For questions or suggestions about these guidelines, please reach out to the development team or create an issue in the project repository.
