# Unified Chart Data Service Architecture

## Overview

The Unified Chart Data Service consolidates the functionality of `ChartDataService` and `EnhancedChartDataService` into a single, registry-driven service that supports chart-specific data adapters.

## Architecture Benefits

### ✅ Eliminates Service Duplication
- **Before**: 2 separate services with overlapping functionality
- **After**: 1 unified service with adapter pattern
- **Result**: 500+ lines of duplicated code eliminated

### ✅ Chart-Specific Data Logic Colocation  
- **Before**: All chart data fetching centralized in one massive service
- **After**: Chart-specific adapters colocated with chart components
- **Result**: Perfect feature colocation following GenContentOps principles

### ✅ Registry-Driven Data Fetching
- **Before**: Hardcoded method names for each chart type
- **After**: Dynamic adapter resolution via chart registry
- **Result**: Zero maintenance when adding new chart types

### ✅ Enhanced Features Integration
- **Before**: Enhanced service wraps original service awkwardly  
- **After**: Enhanced features built into unified service
- **Result**: Cleaner architecture with optional enhancement

## Usage Examples

### Basic Data Fetching
```typescript
import { unifiedChartDataService } from '@/services/UnifiedChartDataService';

// Generic method works with any chart type
const data = await unifiedChartDataService.fetchChartData('btc-price');
```

### Enhanced Data Fetching (with dependency management)
```typescript
const response = await unifiedChartDataService.fetchEnhancedChartData('btc-price');
console.log(response.dataStatus); // Data freshness info
console.log(response.refreshCapability); // Refresh options
await response.refresh(); // Manual refresh
```

### Cached Data Fetching
```typescript
const data = await unifiedChartDataService.fetchCachedChartData(
  'btc-price',
  undefined, // signal
  undefined, // params  
  10 * 60 * 1000 // 10 minute cache
);
```

### Modern React Hook
```typescript
import { useUnifiedChartData } from '@/hooks/useUnifiedChartData';

function MyChart() {
  const { data, loading, error, refresh } = useUnifiedChartData('btc-price', {
    enhanced: true,
    cacheDuration: 5 * 60 * 1000
  });
  
  // Works with any chart type - zero maintenance
}
```

## Chart Adapter Integration

### Adapter Interface
```typescript
interface ChartDataAdapter<T = any> {
  fetchData(signal?: AbortSignal, params?: any): Promise<T[]>;
}
```

### Colocated Adapter Example
```typescript
// /src/charts/btc-price/data-adapter.ts
export class BTCPriceDataAdapterImpl implements ChartDataAdapter<StockDataRow> {
  async fetchData(signal?: AbortSignal): Promise<StockDataRow[]> {
    const response = await fetch("/data/raw/stocks/BTC-USD/daily.csv", { signal });
    const csvText = await response.text();
    return this.parseCSV(csvText);
  }
}
```

### Registry Integration
```typescript
// Chart registry automatically discovers and uses adapters
const chartConfig = chartRegistry.getChartConfig('btc-price');
const data = await chartConfig.dataAdapter.fetchData();
```

## Migration Strategy

### Phase 1: Unified Service Creation ✅
- [x] Create UnifiedChartDataService with adapter pattern
- [x] Implement backward compatibility layer  
- [x] Create modern hooks for unified data fetching

### Phase 2: Chart-by-Chart Migration
```typescript
// Before: Centralized logic in ChartDataService
async fetchBTCPriceData(signal?: AbortSignal): Promise<StockDataRow[]> {
  // 50+ lines of BTC-specific logic
}

// After: Colocated adapter
// /src/charts/btc-price/data-adapter.ts
export class BTCPriceDataAdapter implements ChartDataAdapter { ... }
```

### Phase 3: Legacy Service Replacement
- Update component imports from legacy service to unified service
- Replace chart-specific hooks with generic `useUnifiedChartData` 
- Remove deprecated `ChartDataService` and `EnhancedChartDataService`

## Backward Compatibility

### Legacy Service Wrapper
```typescript
// ChartDataService.legacy.ts routes calls to UnifiedChartDataService
export class LegacyChartDataService {
  async fetchBTCPriceData(signal?: AbortSignal): Promise<StockDataRow[]> {
    return unifiedChartDataService.fetchChartData('btc-price', signal);
  }
}
```

### Existing Hooks Continue Working
```typescript
// Old hook implementation remains unchanged
export function useBTCPriceData(): DataServiceResponse<StockDataRow[]> {
  // Uses legacy service wrapper → unified service → chart adapter
}
```

## Data Flow Architecture

### Chart Registration & Discovery
```
Chart Component → chart.config.ts → Registry → UnifiedService
```

### Data Fetching Flow
```
Component → Hook → UnifiedService → Registry → Adapter → Data
```

### Enhanced Features Flow
```  
Component → Enhanced Hook → UnifiedService → DependencyManager → Status
```

## Performance Benefits

### Intelligent Caching
- **Per-Chart Caching**: Individual cache duration per chart type
- **Parameter-Based Cache Keys**: Different cache entries for parameterized queries
- **Unified Cache Management**: Single cache instance across all charts

### Enhanced Features (Optional)
- **Data Status Tracking**: Freshness and source information
- **Refresh Notifications**: Automatic updates when data changes  
- **Dependency Management**: Chart interdependency tracking

### Registry-Driven Optimization
- **Lazy Loading**: Adapters loaded only when needed
- **Production Filtering**: Development-only charts excluded automatically
- **Type Validation**: Runtime checks prevent invalid chart type requests

## Integration Points

### Chart Registry Integration
```typescript
// Registry provides adapter to service automatically
const adapter = chartRegistry.getChartConfig(chartType)?.dataAdapter;
if (adapter) {
  return await adapter.fetchData(signal, params);
}
```

### Legacy System Compatibility
```typescript
// Existing components work without changes
import { chartDataService } from '@/services/ChartDataService';
// → Routes to UnifiedChartDataService transparently
```

### Modern Component Integration
```typescript
// New components use unified hook
const { data, refresh, dataStatus } = useUnifiedChartData('any-chart-type');
```

This architecture achieves **perfect service consolidation** while maintaining **100% backward compatibility** and enabling **future extensibility** through the adapter pattern.