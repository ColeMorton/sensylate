# E2E Testing Suite for Photo Booth Dashboard Features

## Overview

This comprehensive testing suite provides complete coverage for the photo booth dashboard functionality, focusing on the `portfolio_history_portrait` dashboard with extensive aspect ratio and dimension testing.

## Test Structure

### 1. Mock Data and Fixtures (`/src/test/mocks/` & `/src/test/fixtures/`)

- **`photo-booth.mock.ts`**: Mock configurations, URL params, and test scenarios
- **`dashboard.mock.ts`**: Dashboard service mocks and API response fixtures
- **`fixtures/`**: Static test data including chart data, dashboard configs, and API responses

### 2. Unit Tests (`/src/test/components/`)

#### PhotoBoothDisplay Component (`PhotoBoothDisplay.test.tsx`)

- ✅ Component initialization and loading states
- ✅ URL parameter parsing (dashboard, mode, aspect_ratio, format, dpi, scale)
- ✅ State management and URL synchronization
- ✅ CSS custom properties for aspect ratio dimensions
- ✅ Export functionality and API integration
- ✅ Error handling and fallbacks

#### DashboardRenderer Component (`DashboardRenderer.test.tsx`)

- ✅ Portfolio history portrait specific rendering
- ✅ Header/footer conditional display
- ✅ Chart rendering with `titleOnly` flag
- ✅ Theme switching behavior
- ✅ Layout class application
- ✅ Aspect ratio handling

### 3. Integration Tests (`/src/test/integration/`)

#### Photo Booth Workflow (`photo-booth-workflow.test.tsx`)

- ✅ Complete dashboard loading flow
- ✅ Parameter synchronization workflows
- ✅ Aspect ratio changes with dimension updates
- ✅ Theme switching workflows
- ✅ Export workflow end-to-end
- ✅ Portfolio history portrait specific features
- ✅ Error recovery workflows

### 4. E2E Tests (`/src/test/e2e/`)

#### Core Dashboard Functionality (`photo-booth-e2e.test.ts`)

- ✅ Page loading and navigation
- ✅ Dashboard interaction (theme switching, parameter changes)
- ✅ Content verification and structure validation
- ✅ Responsive behavior across viewports
- ✅ Performance and loading benchmarks
- ✅ Error handling and recovery

#### Aspect Ratio Validation (`aspect-ratio-validation.test.ts`)

- ✅ Dimension validation for all aspect ratios (16:9, 4:3, 3:4)
- ✅ Visual consistency across ratios and themes
- ✅ Smooth transitions between aspect ratios
- ✅ Export mode vs display mode behavior
- ✅ Chart adaptation to different orientations
- ✅ Edge cases and parameter validation

#### Visual Regression Testing (`visual-regression.test.ts`)

- ✅ Screenshot baseline creation and management
- ✅ Cross-theme visual consistency
- ✅ Responsive visual testing across viewports
- ✅ Export mode visual validation
- ✅ Chart visual consistency
- ✅ Cross-browser compatibility testing

#### Error Handling (`error-handling.test.ts`)

- ✅ Network error scenarios (API failures, timeouts)
- ✅ Export error handling (API failures, timeouts, race conditions)
- ✅ Invalid parameter handling and XSS prevention
- ✅ Browser compatibility edge cases
- ✅ Performance under stress conditions
- ✅ Security validation

### 5. Visual Testing Infrastructure (`/src/test/e2e/screenshot-baseline-manager.ts`)

- ✅ Baseline screenshot management
- ✅ Visual comparison utilities
- ✅ Metadata tracking for test configurations
- ✅ Image hash generation for change detection
- ✅ Cleanup and validation utilities

## Key Test Scenarios Covered

### Priority 1 (Core Functionality)

1. **Dashboard Loading**: Component initialization with URL parameters ✅
2. **Aspect Ratio Switching**: 3:4 portrait mode with correct dimensions ✅
3. **Theme Toggle**: Light/dark mode with proper chart theming ✅
4. **Export Simulation**: Mock API export workflow ✅

### Priority 2 (Edge Cases)

1. **Error Handling**: Network failures, invalid configurations ✅
2. **Loading States**: Skeleton screens, progress indicators ✅
3. **Parameter Validation**: Invalid aspect ratios, malformed URLs ✅
4. **Responsive Breakpoints**: Mobile and desktop layout differences ✅

## Running the Tests

### Unit Tests

```bash
# Run all unit tests
yarn test

# Run specific component tests
yarn test PhotoBoothDisplay.test.tsx
yarn test DashboardRenderer.test.tsx

# Run with coverage
yarn test:coverage
```

### Integration Tests

```bash
# Run integration tests
yarn test src/test/integration

# Run with watch mode
yarn test:watch src/test/integration
```

### E2E Tests

```bash
# Run all E2E tests
yarn test:e2e

# Run with UI for debugging
yarn test:e2e:ui

# Run specific E2E test suite
yarn test:e2e src/test/e2e/photo-booth-e2e.test.ts
```

### Visual Testing

```bash
# Create/update baselines (run this first)
UPDATE_BASELINES=true yarn test:e2e src/test/e2e/visual-regression.test.ts

# Run visual regression tests
yarn test:e2e src/test/e2e/visual-regression.test.ts

# Generate screenshots during tests
E2E_SCREENSHOTS=true yarn test:e2e
```

## Test Configuration

### Environment Variables

- `E2E_BASE_URL`: Base URL for E2E tests (default: http://localhost:4321)
- `E2E_SCREENSHOTS`: Enable screenshot capture (default: false)
- `UPDATE_BASELINES`: Update visual regression baselines (default: false)

### Vitest Configuration

The test suite uses Vitest with the following key configurations:

- **Environment**: jsdom for unit tests, puppeteer for E2E
- **Timeout**: 30s for E2E tests, 5s for unit tests
- **Coverage**: v8 provider with HTML/LCOV reports
- **Setup**: Automated mock configuration and cleanup

## Coverage Goals

- **Unit Tests**: >90% code coverage for PhotoBoothDisplay and DashboardRenderer
- **Integration Tests**: Complete workflow coverage for all user scenarios
- **E2E Tests**: 100% feature coverage for photo booth functionality
- **Visual Tests**: Baseline coverage for all aspect ratios and themes

## Regression Prevention

This test suite prevents regressions in:

1. **Layout Issues**: Aspect ratio dimension mismatches
2. **Theme Problems**: Inconsistent styling across light/dark modes
3. **Export Failures**: API integration and parameter passing
4. **Parameter Handling**: URL synchronization and validation
5. **Error States**: Graceful handling of network and API failures
6. **Visual Consistency**: Screenshots prevent UI regressions

## Maintenance

### Adding New Tests

1. Follow existing naming conventions (`*.test.tsx` for components, `*.test.ts` for E2E)
2. Use appropriate test helpers and mocks from `/src/test/mocks/`
3. Update baselines when visual changes are intentional
4. Document new test scenarios in this README

### Updating Baselines

When UI changes are intentional:

1. Run with `UPDATE_BASELINES=true` to create new baselines
2. Review generated screenshots for accuracy
3. Commit new baselines with descriptive commit messages

### Performance Monitoring

Monitor test execution times and screenshot sizes:

- Unit tests should complete in <5s total
- Integration tests should complete in <30s total
- E2E tests may take up to 2 minutes per suite
- Screenshot baselines should be <2MB each

## Implementation Benefits

- ✅ **Regression Prevention**: Catches layout/dimension issues early
- ✅ **Documentation**: Tests serve as living documentation
- ✅ **Confidence**: Safe refactoring with comprehensive coverage
- ✅ **Quality Assurance**: Automated validation of visual consistency
- ✅ **TDD Approach**: Test-first development for new features
