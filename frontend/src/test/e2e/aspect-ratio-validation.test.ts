import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { e2eHelper, setupE2ETest, cleanupE2ETest, type TestContext, E2ETestHelper } from '../e2e/setup';

describe('Aspect Ratio Validation E2E Tests', () => {
  let context: TestContext;

  beforeEach(async () => {
    context = await setupE2ETest();
  });

  afterEach(async () => {
    await cleanupE2ETest();
  });

  describe('Aspect Ratio Dimension Validation', () => {
    const aspectRatios = [
      { id: '16:9', name: 'Widescreen', width: 1920, height: 1080 },
      { id: '4:3', name: 'Traditional', width: 1440, height: 1080 },
      { id: '3:4', name: 'Portrait', width: 1080, height: 1440 }
    ];

    aspectRatios.forEach(({ id, name, width, height }) => {
      it(`validates ${id} aspect ratio dimensions and layout`, async () => {
        const { page, baseURL } = context;

        await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=${id}`, {
          waitUntil: 'networkidle0',
          timeout: 15000
        });

        await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

        // Verify aspect ratio is selected in UI
        const selectedRatio = await page.$eval('#aspect-ratio-select', el => (el as HTMLSelectElement).value);
        expect(selectedRatio).toBe(id);

        // Check CSS custom properties are set correctly
        const dashboard = await page.$('.photo-booth-dashboard');
        const computedWidth = await dashboard?.evaluate(el => {
          return getComputedStyle(el).getPropertyValue('--photo-booth-width');
        });
        const computedHeight = await dashboard?.evaluate(el => {
          return getComputedStyle(el).getPropertyValue('--photo-booth-height');
        });

        expect(computedWidth).toBe(`${width}px`);
        expect(computedHeight).toBe(`${height}px`);

        // Take screenshot for visual verification
        await e2eHelper.takeScreenshot(page, `aspect-ratio-${id.replace(':', 'x')}-${name.toLowerCase()}`);

        // Verify dashboard content fits within expected bounds
        const dashboardBox = await dashboard?.boundingBox();
        expect(dashboardBox).toBeTruthy();
        
        // Allow for some flexibility in dimensions due to browser rendering
        const tolerance = 50;
        expect(dashboardBox!.width).toBeGreaterThan(width - tolerance);
        expect(dashboardBox!.height).toBeGreaterThan(height - tolerance);
      });
    });

    it('compares all aspect ratios visually for layout consistency', async () => {
      const { page, baseURL } = context;

      const screenshots: string[] = [];

      for (const ratio of aspectRatios) {
        await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=${ratio.id}&mode=light`, {
          waitUntil: 'networkidle0',
          timeout: 15000
        });

        await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });
        
        // Wait for charts to stabilize
        await E2ETestHelper.sleep(3000);

        const screenshotName = `comparison-${ratio.id.replace(':', 'x')}-light`;
        await e2eHelper.takeScreenshot(page, screenshotName);
        screenshots.push(screenshotName);

        // Verify consistent header/footer presence across all ratios
        const header = await page.$('.dashboard-header h1');
        const footer = await page.$('.dashboard-footer h1');
        
        expect(header).toBeTruthy();
        expect(footer).toBeTruthy();
        
        const headerText = await header?.evaluate(el => el.textContent);
        const footerText = await footer?.evaluate(el => el.textContent);
        
        expect(headerText).toBe('Twitter Live Signals');
        expect(footerText).toBe('colemorton.com');

        // Verify charts are present in all ratios
        const charts = await page.$$('.photo-booth-chart');
        expect(charts.length).toBe(2); // Portfolio history portrait has 2 charts
      }
    });
  });

  describe('Aspect Ratio Theme Combinations', () => {
    const aspectRatios = ['16:9', '4:3', '3:4'];
    const modes = ['light', 'dark'];

    aspectRatios.forEach(aspectRatio => {
      modes.forEach(mode => {
        it(`validates ${aspectRatio} aspect ratio in ${mode} mode`, async () => {
          const { page, baseURL } = context;

          await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=${aspectRatio}&mode=${mode}`, {
            waitUntil: 'networkidle0',
            timeout: 15000
          });

          await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

          // Verify theme is applied correctly
          const dashboard = await page.$('.photo-booth-dashboard');
          const hasDarkClass = await dashboard?.evaluate(el => el.classList.contains('dark'));
          
          if (mode === 'dark') {
            expect(hasDarkClass).toBe(true);
          } else {
            expect(hasDarkClass).toBe(false);
          }

          // Verify aspect ratio selection
          const selectedRatio = await page.$eval('#aspect-ratio-select', el => (el as HTMLSelectElement).value);
          expect(selectedRatio).toBe(aspectRatio);

          // Verify mode button state
          const activeButton = await page.$('.bg-blue-500');
          const buttonText = await activeButton?.evaluate(el => el.textContent?.trim());
          expect(buttonText?.toLowerCase()).toBe(mode);

          // Take screenshot for theme + aspect ratio combination
          await e2eHelper.takeScreenshot(page, `${aspectRatio.replace(':', 'x')}-${mode}-combination`);

          // Verify chart visibility in both themes
          const charts = await page.$$('.photo-booth-chart');
          for (const chart of charts) {
            const isVisible = await chart.isIntersectingViewport();
            expect(isVisible).toBe(true);
          }
        });
      });
    });
  });

  describe('Aspect Ratio Switching Behavior', () => {
    it('smoothly transitions between aspect ratios', async () => {
      const { page, baseURL } = context;

      await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait`, {
        waitUntil: 'networkidle0',
        timeout: 15000
      });

      await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

      const ratios = ['16:9', '4:3', '3:4', '16:9']; // Include return to original

      for (let i = 0; i < ratios.length; i++) {
        const ratio = ratios[i];
        
        // Take screenshot before change (except first iteration)
        if (i > 0) {
          await e2eHelper.takeScreenshot(page, `before-switch-to-${ratio.replace(':', 'x')}`);
        }

        // Change aspect ratio
        await page.selectOption('#aspect-ratio-select', ratio);

        // Verify loading state appears
        const loadingIndicator = await page.waitForSelector('text=Loading...', { timeout: 2000 }).catch(() => null);
        if (loadingIndicator) {
          await e2eHelper.takeScreenshot(page, `loading-state-${ratio.replace(':', 'x')}`);
        }

        // Wait for ready state
        await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

        // Take screenshot after change
        await e2eHelper.takeScreenshot(page, `after-switch-to-${ratio.replace(':', 'x')}`);

        // Verify aspect ratio change was applied
        const selectedRatio = await page.$eval('#aspect-ratio-select', el => (el as HTMLSelectElement).value);
        expect(selectedRatio).toBe(ratio);

        // Verify content is still visible
        const header = await page.$('.dashboard-header h1');
        const footer = await page.$('.dashboard-footer h1');
        expect(header).toBeTruthy();
        expect(footer).toBeTruthy();

        // Wait briefly between transitions
        await E2ETestHelper.sleep(1000);
      }
    });

    it('maintains URL synchronization during aspect ratio changes', async () => {
      const { page, baseURL } = context;

      await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait`, {
        waitUntil: 'networkidle0',
        timeout: 15000
      });

      await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

      const ratios = ['4:3', '3:4', '16:9'];

      for (const ratio of ratios) {
        await page.selectOption('#aspect-ratio-select', ratio);
        await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

        // Check URL was updated
        const currentURL = page.url();
        expect(currentURL).toContain(`aspect_ratio=${ratio}`);

        // Refresh page and verify state is maintained
        await page.reload({ waitUntil: 'networkidle0' });
        await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

        const selectedRatio = await page.$eval('#aspect-ratio-select', el => (el as HTMLSelectElement).value);
        expect(selectedRatio).toBe(ratio);
      }
    });
  });

  describe('Export Mode Dimension Validation', () => {
    it('validates export mode CSS behavior for different aspect ratios', async () => {
      const { page, baseURL } = context;

      const aspectRatios = ['16:9', '4:3', '3:4'];

      for (const ratio of aspectRatios) {
        await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=${ratio}`, {
          waitUntil: 'networkidle0',
          timeout: 15000
        });

        await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

        // Simulate export mode by hiding controls
        await page.evaluate(() => {
          const controls = document.querySelectorAll('.photo-booth-controls');
          controls.forEach(control => {
            (control as HTMLElement).style.display = 'none';
            (control as HTMLElement).style.visibility = 'hidden';
          });
        });

        // Wait for CSS changes to apply
        await E2ETestHelper.sleep(1000);

        // Take screenshot in export mode
        await e2eHelper.takeScreenshot(page, `export-mode-${ratio.replace(':', 'x')}`);

        // Verify dashboard fills viewport in export mode
        const dashboard = await page.$('.photo-booth-dashboard');
        const viewport = page.viewport();
        const dashboardBox = await dashboard?.boundingBox();

        expect(dashboardBox).toBeTruthy();
        expect(viewport).toBeTruthy();

        // In export mode, dashboard should fill available space
        expect(dashboardBox!.width).toBeGreaterThan(viewport!.width * 0.9);
        expect(dashboardBox!.height).toBeGreaterThan(viewport!.height * 0.8);

        // Verify content is not clipped
        const header = await page.$('.dashboard-header');
        const footer = await page.$('.dashboard-footer');
        const headerBox = await header?.boundingBox();
        const footerBox = await footer?.boundingBox();

        expect(headerBox).toBeTruthy();
        expect(footerBox).toBeTruthy();
        expect(headerBox!.x).toBeGreaterThanOrEqual(0);
        expect(footerBox!.x).toBeGreaterThanOrEqual(0);
      }
    });

    it('compares display mode vs export mode layout differences', async () => {
      const { page, baseURL } = context;

      await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=3:4`, {
        waitUntil: 'networkidle0',
        timeout: 15000
      });

      await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

      // Take screenshot in display mode
      await e2eHelper.takeScreenshot(page, 'display-mode-3x4-with-controls');

      // Get dashboard dimensions in display mode
      const dashboard = await page.$('.photo-booth-dashboard');
      const displayModeBox = await dashboard?.boundingBox();

      // Switch to export mode simulation
      await page.evaluate(() => {
        const controls = document.querySelectorAll('.photo-booth-controls');
        controls.forEach(control => {
          (control as HTMLElement).style.display = 'none';
          (control as HTMLElement).style.visibility = 'hidden';
        });
      });

      await E2ETestHelper.sleep(1000);

      // Take screenshot in export mode
      await e2eHelper.takeScreenshot(page, 'export-mode-3x4-no-controls');

      // Get dashboard dimensions in export mode
      const exportModeBox = await dashboard?.boundingBox();

      // Verify layout differences
      expect(exportModeBox).toBeTruthy();
      expect(displayModeBox).toBeTruthy();

      // Export mode should utilize more vertical space
      expect(exportModeBox!.height).toBeGreaterThan(displayModeBox!.height);
    });
  });

  describe('Chart Adaptation to Aspect Ratios', () => {
    it('validates charts adapt properly to portrait vs landscape ratios', async () => {
      const { page, baseURL } = context;

      const ratios = [
        { id: '16:9', orientation: 'landscape', width: 1920, height: 1080 },
        { id: '3:4', orientation: 'portrait', width: 1080, height: 1440 }
      ];

      for (const ratio of ratios) {
        await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=${ratio.id}`, {
          waitUntil: 'networkidle0',
          timeout: 15000
        });

        await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

        // Wait for charts to fully render
        await E2ETestHelper.sleep(5000);

        await e2eHelper.takeScreenshot(page, `charts-${ratio.orientation}-${ratio.id.replace(':', 'x')}`);

        // Verify charts are visible and have reasonable dimensions
        const charts = await page.$$('.photo-booth-chart');
        
        expect(charts.length).toBe(2);

        for (const chart of charts) {
          const chartBox = await chart.boundingBox();
          expect(chartBox).toBeTruthy();
          expect(chartBox!.width).toBeGreaterThan(200);
          expect(chartBox!.height).toBeGreaterThan(100);

          // Charts should fit within the dashboard bounds
          const dashboardBox = await page.$eval('.photo-booth-dashboard', el => el.getBoundingClientRect());
          expect(chartBox!.x).toBeGreaterThanOrEqual(dashboardBox.x - 10); // Small tolerance
          expect(chartBox!.y).toBeGreaterThanOrEqual(dashboardBox.y - 10);
          expect(chartBox!.x + chartBox!.width).toBeLessThanOrEqual(dashboardBox.x + dashboardBox.width + 10);
        }
      }
    });

    it('validates chart responsiveness during rapid aspect ratio changes', async () => {
      const { page, baseURL } = context;

      await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait`, {
        waitUntil: 'networkidle0',
        timeout: 15000
      });

      await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

      const ratios = ['16:9', '3:4', '4:3', '3:4', '16:9'];

      for (let i = 0; i < ratios.length; i++) {
        const ratio = ratios[i];
        
        await page.selectOption('#aspect-ratio-select', ratio);
        
        // Don't wait for full ready state, just brief stabilization
        await E2ETestHelper.sleep(2000);
        
        // Verify charts are still present and visible
        const charts = await page.$$('.photo-booth-chart');
        expect(charts.length).toBe(2);

        for (const chart of charts) {
          const isVisible = await chart.isIntersectingViewport();
          expect(isVisible).toBe(true);
        }

        await e2eHelper.takeScreenshot(page, `rapid-change-${i}-${ratio.replace(':', 'x')}`);
      }

      // Wait for final ready state
      await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });
      await e2eHelper.takeScreenshot(page, 'rapid-changes-final-state');
    });
  });

  describe('Aspect Ratio Edge Cases', () => {
    it('handles invalid aspect ratio parameters gracefully', async () => {
      const { page, baseURL } = context;

      const invalidRatios = ['invalid:ratio', '0:0', 'abc:def', '1:2:3'];

      for (const invalidRatio of invalidRatios) {
        await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=${invalidRatio}`, {
          waitUntil: 'networkidle0',
          timeout: 15000
        });

        await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

        // Should fall back to default 16:9
        const selectedRatio = await page.$eval('#aspect-ratio-select', el => (el as HTMLSelectElement).value);
        expect(selectedRatio).toBe('16:9');

        await e2eHelper.takeScreenshot(page, `invalid-ratio-fallback-${invalidRatio.replace(/[^a-zA-Z0-9]/g, '_')}`);
      }
    });

    it('validates consistent behavior across browser refreshes', async () => {
      const { page, baseURL } = context;

      const testRatio = '3:4';

      await page.goto(`${baseURL}/photo-booth?dashboard=portfolio_history_portrait&aspect_ratio=${testRatio}`, {
        waitUntil: 'networkidle0',
        timeout: 15000
      });

      await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

      // Get initial state
      const initialRatio = await page.$eval('#aspect-ratio-select', el => (el as HTMLSelectElement).value);
      const initialHeader = await page.$eval('.dashboard-header h1', el => el.textContent);
      
      await e2eHelper.takeScreenshot(page, 'before-refresh-3x4');

      // Refresh the page
      await page.reload({ waitUntil: 'networkidle0' });
      await page.waitForSelector('.photo-booth-ready', { timeout: 20000 });

      // Verify state is maintained
      const afterRefreshRatio = await page.$eval('#aspect-ratio-select', el => (el as HTMLSelectElement).value);
      const afterRefreshHeader = await page.$eval('.dashboard-header h1', el => el.textContent);

      expect(afterRefreshRatio).toBe(initialRatio);
      expect(afterRefreshHeader).toBe(initialHeader);

      await e2eHelper.takeScreenshot(page, 'after-refresh-3x4');
    });
  });
});