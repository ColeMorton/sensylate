# Photo-Booth Test Module

This is an isolated test module containing all tests related to the photo-booth/dashboard/image export feature. The module is designed to be self-contained with shared utilities, mocks, and test runners.

## 📁 Directory Structure

```
src/test/photo-booth/
├── __mocks__/                    # Shared mock configurations
│   ├── setup.ts                  # Main mock setup and configuration
│   ├── photo-booth-config.mock.ts # Photo-booth config mocks
│   ├── dashboard-loader.mock.ts  # Dashboard service mocks
│   └── test-data.mock.ts         # Centralized test data
├── unit/                         # Component unit tests
│   ├── PhotoBoothDisplay.test.tsx
│   └── DashboardRenderer.test.tsx
├── integration/                  # Integration workflow tests
│   └── workflow.test.tsx
├── e2e/                          # End-to-end browser tests
│   ├── photo-booth-e2e.test.ts
│   ├── aspect-ratio.test.ts
│   ├── visual-regression.test.ts
│   └── error-handling.test.ts
├── fixtures/                     # Test fixture data
├── utils/                        # Test utilities and helpers
│   ├── test-helpers.ts           # Unit/integration test helpers
│   └── e2e-setup.ts             # E2E test setup utilities
├── photo-booth-test-suite.ts     # Main test runner script
└── README.md                     # This file
```

## 🚀 Quick Start

### Run All Tests
```bash
npm run test:photo-booth
```

### Run Specific Test Types
```bash
npm run test:photo-booth:unit         # Unit tests only
npm run test:photo-booth:integration  # Integration tests only
npm run test:photo-booth:e2e          # E2E tests only
```

### Development & Debugging
```bash
npm run test:photo-booth:watch        # Watch mode
npm run test:photo-booth:coverage     # With coverage report
npm run test:photo-booth -- --verbose # Verbose output
```

## 🧪 Test Types

### Unit Tests (`unit/`)
Component-level tests focusing on individual functionality:
- **PhotoBoothDisplay.test.tsx**: Main component behavior, props, state management
- **DashboardRenderer.test.tsx**: Dashboard rendering logic and layout

**Key Features:**
- Isolated component testing
- Mocked external dependencies
- Fast execution (< 2 seconds)
- High test coverage of core logic

### Integration Tests (`integration/`)
Workflow tests covering component interactions:
- **workflow.test.tsx**: Complete user workflows, parameter synchronization, export processes

**Key Features:**
- Multi-component interaction testing
- Real user event simulation
- State management validation
- API integration testing

### E2E Tests (`e2e/`)
Browser-based tests covering complete user journeys:
- **photo-booth-e2e.test.ts**: Full page functionality, navigation, user interactions  
- **aspect-ratio.test.ts**: Aspect ratio handling and dimension validation
- **visual-regression.test.ts**: Visual consistency and screenshot validation
- **error-handling.test.ts**: Error scenarios and edge cases

**Key Features:**
- Real browser testing with Puppeteer
- Screenshot comparison
- Network error simulation
- Cross-viewport testing
- Performance validation

## 🛠 Utilities & Helpers

### Test Helpers (`utils/test-helpers.ts`)
Common utilities for unit and integration tests:
```typescript
import { mockURLSearchParams, waitForPhotoBoothReady } from '../utils/test-helpers';

// Mock URL parameters
mockURLSearchParams({ dashboard: 'portfolio_history_portrait', mode: 'dark' });

// Wait for component to be ready
await waitForPhotoBoothReady();

// Simulate parameter changes
await changePhotoBoothParams(user, { aspectRatio: '3:4', mode: 'dark' });
```

### E2E Setup (`utils/e2e-setup.ts`)  
Browser test utilities and page management:
```typescript
import { setupPhotoBoothE2E, photoBoothE2EHelper } from '../utils/e2e-setup';

// Setup E2E test environment
const { page, browser } = await setupPhotoBoothE2E();

// Navigate to photo-booth with parameters
await photoBoothE2EHelper.navigateToPhotoBooth(page, { dashboard: 'test', mode: 'light' });

// Wait for ready state
await photoBoothE2EHelper.waitForPhotoBoothReady(page);
```

## 🎭 Mocks & Test Data

### Mock Setup (`__mocks__/setup.ts`)
Centralized mock configuration that handles:
- Photo-booth config import mocking
- Dashboard loader service mocking  
- Chart component mocking
- Default mock behaviors

**Usage:**
```typescript
import { setupPhotoBoothMocks } from '../__mocks__/setup';

beforeEach(() => {
  setupPhotoBoothMocks();
});
```

### Test Data (`__mocks__/test-data.mock.ts`)
Centralized test data including:
- URL parameter scenarios
- Viewport configurations
- Export configurations  
- Error scenarios
- XSS test payloads

**Usage:**
```typescript
import { testURLParams, testViewports } from '../__mocks__/test-data.mock';

mockURLSearchParams(testURLParams.portraitMode);
```

## 🧩 Test Patterns

### Component Testing Pattern
```typescript
import { setupPhotoBoothMocks } from '../__mocks__/setup';
import { mockURLSearchParams } from '../utils/test-helpers';

describe('Component Name', () => {
  beforeEach(() => {
    setupPhotoBoothMocks();
  });

  it('should test specific behavior', async () => {
    mockURLSearchParams({ mode: 'dark' });
    render(<Component />);
    
    await waitFor(() => {
      expect(screen.getByText('Expected Text')).toBeInTheDocument();
    });
  });
});
```

### E2E Testing Pattern
```typescript
import { setupPhotoBoothE2E, cleanupPhotoBoothE2E } from '../utils/e2e-setup';

describe('E2E Feature', () => {
  let context: E2ETestContext;

  beforeEach(async () => {
    context = await setupPhotoBoothE2E();
  });

  afterEach(async () => {
    await cleanupPhotoBoothE2E();
  });

  it('should test complete workflow', async () => {
    const { page } = context;
    
    await page.goto('/photo-booth');
    await page.waitForSelector('.photo-booth-ready');
    
    // Test interactions...
  });
});
```

## 🚨 Error Handling & Debugging

### Common Issues

1. **Mock Import Errors**
   - Ensure imports are from `../__mocks__/setup`
   - Check that `setupPhotoBoothMocks()` is called in beforeEach

2. **E2E Test Timeouts**  
   - Ensure development server is running for E2E tests
   - Increase timeout for slower CI environments
   - Check network conditions and browser resources

3. **Missing Dependencies**
   - Run `npm install` to ensure all test dependencies are installed
   - Check that @testing-library/dom is available

### Debugging Tips

- Use `--verbose` flag for detailed test output
- Add `.only` to run specific test suites
- Use browser dev tools in non-headless mode for E2E debugging
- Check screenshot outputs in `e2e/screenshots/` directory

## 📊 Coverage & Performance

### Coverage Targets
- **Unit Tests**: > 90% line coverage
- **Integration Tests**: > 80% workflow coverage  
- **E2E Tests**: 100% critical user journey coverage

### Performance Expectations
- **Unit Tests**: < 5 seconds total
- **Integration Tests**: < 15 seconds total
- **E2E Tests**: < 2 minutes total (including server startup)

## 🔧 Configuration

### Environment Variables
```bash
E2E_BASE_URL=http://localhost:4321    # E2E test server URL
E2E_SCREENSHOTS=true                  # Enable screenshot capture
E2E_NO_DEV_SERVER=true               # Skip dev server startup
CI=true                              # CI environment detection
```

### Vitest Configuration
The module uses the existing `vitest.config.ts` with:
- JSdom environment for unit/integration tests
- 30-second default timeout
- Path aliases for imports
- Coverage exclusions for test files

## 📈 Extending the Test Suite

### Adding New Tests

1. **Unit Tests**: Add to appropriate file in `unit/`
2. **Integration Tests**: Extend `workflow.test.tsx` or create new file
3. **E2E Tests**: Add to appropriate category in `e2e/`

### Adding New Utilities

1. **Test Helpers**: Add to `utils/test-helpers.ts`
2. **E2E Utilities**: Add to `utils/e2e-setup.ts`
3. **Mock Data**: Add to `__mocks__/test-data.mock.ts`

### Best Practices

- Use descriptive test names that explain the behavior being tested
- Group related tests in describe blocks
- Mock external dependencies consistently
- Test both happy path and error scenarios
- Keep tests focused and isolated
- Use data-testid attributes for reliable element selection
- Include accessibility testing where relevant

## 🤝 Contributing

When adding new photo-booth functionality:

1. Add corresponding unit tests for components
2. Add integration tests for workflows
3. Add E2E tests for user-facing features
4. Update mock data as needed
5. Run full test suite before submitting
6. Update this README if adding new patterns or utilities

## 📚 Related Documentation

- [Vitest Documentation](https://vitest.dev/)
- [Testing Library React](https://testing-library.com/docs/react-testing-library/intro/)
- [Puppeteer Documentation](https://pptr.dev/)
- [Photo-Booth Component Documentation](../../layouts/shortcodes/PhotoBoothDisplay.tsx)