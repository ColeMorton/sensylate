# Chart Component Colocation System

This directory implements a colocated chart architecture that eliminates configuration duplication and follows GenContentOps methodology.

## Architecture Overview

### Directory Structure

```
/frontend/src/charts/
├── chart-config.schema.ts    # TypeScript schema definitions
├── chart-registry.ts         # Auto-discovery and registration
├── README.md                 # This documentation
└── [chart-type]/             # Individual chart directories
    ├── chart.config.ts       # Colocated metadata
    ├── data-adapter.ts       # Chart-specific data logic
    └── Component.tsx         # React component (optional)
```

### Benefits

1. **Zero Configuration Duplication**: Chart metadata lives exactly once, next to the implementation
2. **Perfect Colocation**: All chart-related code grouped by feature, not by file type
3. **Auto-Discovery**: Build pipeline automatically finds and processes chart configurations
4. **Type Safety**: TypeScript schema ensures consistent configuration structure
5. **Maintainability**: Adding new charts requires zero changes to build pipeline

## Adding a New Chart

### Step 1: Create Chart Directory

```bash
mkdir /frontend/src/charts/[your-chart-type]
```

### Step 2: Add Chart Configuration

Create `chart.config.ts`:

```typescript
import type { ChartConfig } from "../chart-config.schema";

export const yourChartConfig: ChartConfig = {
  metadata: {
    title: "Your Chart Title",
    category: "Your Category",
    description: "Description of what your chart shows",
    chartType: "your-chart-type",
  },
  dataRequirements: {
    dataSources: ["/data/path/to/your/data.csv"],
    cacheable: true,
    cacheDuration: 5 * 60 * 1000, // 5 minutes
  },
  displayOptions: {
    defaultTimeframe: "daily",
    supportsIndexed: false,
    supportsPositionType: false,
    supportsSamePercentageScale: true,
  },
  productionReady: true,
};

export default yourChartConfig;
```

### Step 3: Add Data Adapter (Optional)

Create `data-adapter.ts` for custom data fetching logic:

```typescript
import type { StockDataRow } from "@/types/ChartTypes";

export class YourChartDataAdapter {
  async fetchData(signal?: AbortSignal): Promise<StockDataRow[]> {
    // Custom data fetching logic
    const response = await fetch("/data/path/to/your/data.csv", { signal });
    const csvText = await response.text();
    return this.parseCSV(csvText);
  }

  private parseCSV(csvText: string): StockDataRow[] {
    // CSV parsing logic
  }
}

export const yourChartDataAdapter = new YourChartDataAdapter();
```

### Step 4: Update Dashboard Mapping

Add your chart to the dashboard mapping in `scripts/extract-chart-configs.js`:

```javascript
const DASHBOARD_CHART_MAPPINGS = {
  your_dashboard_id: ["your-chart-type"],
  bitcoin_cycle_intelligence: ["btc-price"],
  // ... other mappings
};
```

### Step 5: Build Pipeline Integration

The chart will be automatically discovered by:

1. `extract-chart-configs.js` - Extracts TypeScript config → JSON
2. `generate_dashboard_configs.py` - Consumes JSON → Dashboard config
3. Chart Registry - Provides runtime type validation

## Chart Registry

The Chart Registry (`chart-registry.ts`) provides:

- **Auto-Discovery**: Automatically registers available charts
- **Type Validation**: Runtime checking of chart type support
- **Production Flags**: Controls chart availability across environments
- **Legacy Support**: Maintains compatibility with existing charts

### Registry Methods

```typescript
// Check if chart type is supported
chartRegistry.isSupported("btc-price"); // true

// Check production readiness
chartRegistry.isProductionReady("fundamental-revenue-fcf"); // false

// Get all supported chart types
chartRegistry.getChartTypes(); // ['btc-price', 'apple-price', ...]

// Check chart categorization
chartRegistry.isFundamentalChart("fundamental-revenue-fcf"); // true
chartRegistry.isLegacyChart("apple-price"); // true
```

## Migration Status

### ✅ Migrated Charts

- `btc-price` - Bitcoin Cycle Intelligence (Reference Implementation)

### 🔄 Legacy Charts (Using PortfolioChart)

- All portfolio/trading charts still use existing `PortfolioChart` component
- Auto-registered in chart registry for validation
- Backward compatible with existing functionality

### 🚧 Future Migrations

As charts are migrated to colocation:

1. Create chart directory with config + adapter
2. Update dashboard mapping
3. Registry automatically discovers new configuration
4. Zero changes needed in build pipeline

## Pipeline Integration

### Development Workflow

1. Make changes to chart configurations
2. `yarn data:pipeline` regenerates static configurations
3. Frontend automatically picks up changes via hot reload

### Build Workflow

1. `extract-chart-configs.js` discovers all chart configurations
2. `generate_dashboard_configs.py` merges with dashboard definitions
3. Static JSON generated for frontend consumption
4. Chart Registry validates types at runtime

This architecture ensures **single source of truth** while maintaining **perfect feature colocation** and **zero maintenance overhead** for chart addition/removal.
