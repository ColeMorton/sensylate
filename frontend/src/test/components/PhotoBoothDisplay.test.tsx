import React from 'react';
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react';
import PhotoBoothDisplay from '@/shortcodes/PhotoBoothDisplay';
import { 
  mockPhotoBoothConfig, 
  mockURLSearchParams, 
  mockWindowHistory,
  testScenarios 
} from '../mocks/photo-booth.mock';
import { 
  mockAllDashboards, 
  mockDashboardLoader,
  mockFetchSuccess,
  mockFetchError,
  mockNetworkError,
  mockExportSuccess,
  mockExportError
} from '../mocks/dashboard.mock';

// Mock the photo booth config import
vi.mock('@/config/photo-booth.json', () => ({
  default: mockPhotoBoothConfig
}));

// Mock the dashboard loader service
vi.mock('@/services/dashboardLoader', () => ({
  DashboardLoader: mockDashboardLoader
}));

// Mock ChartDisplay component to avoid complex chart rendering in unit tests
vi.mock('@/shortcodes/ChartDisplay', () => ({
  default: ({ title, chartType, titleOnly }: any) => (
    <div data-testid={`mock-chart-${chartType}`}>
      <div data-testid="chart-title">{title}</div>
      <div data-testid="chart-title-only">{titleOnly ? 'true' : 'false'}</div>
    </div>
  )
}));

describe('PhotoBoothDisplay Component', () => {
  beforeEach(() => {
    // Reset all mocks
    vi.clearAllMocks();
    
    // Mock successful dashboard loading by default
    mockDashboardLoader.getAllDashboards.mockResolvedValue(mockAllDashboards);
    
    // Mock successful fetch by default
    global.fetch = mockFetchSuccess(mockExportSuccess) as any;
  });

  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  describe('Component Initialization', () => {
    it('renders loading state initially', () => {
      render(<PhotoBoothDisplay />);
      
      expect(screen.getByText('Loading dashboards...')).toBeInTheDocument();
    });

    it('renders dashboard after successful loading', async () => {
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('Portfolio History Portrait')).toBeInTheDocument();
      });
    });

    it('displays error when dashboard loading fails', async () => {
      mockDashboardLoader.getAllDashboards.mockRejectedValue(new Error('Network error'));
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('Failed to Load Dashboards')).toBeInTheDocument();
      });
    });
  });

  describe('URL Parameter Parsing', () => {
    it('parses dashboard parameter from URL', async () => {
      mockURLSearchParams(testScenarios.portraitMode);
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const select = screen.getByDisplayValue('Portfolio History Portrait');
        expect(select).toBeInTheDocument();
      });
    });

    it('parses mode parameter and sets theme', async () => {
      mockURLSearchParams({ mode: 'dark' });
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const darkButton = screen.getByRole('button', { name: /dark/i });
        expect(darkButton).toHaveClass('bg-blue-500');
      });
    });

    it('parses aspect ratio parameter', async () => {
      mockURLSearchParams({ aspect_ratio: '3:4' });
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const aspectSelect = screen.getByDisplayValue('3:4 Portrait');
        expect(aspectSelect).toBeInTheDocument();
      });
    });

    it('parses format parameter', async () => {
      mockURLSearchParams({ format: 'svg' });
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const formatSelect = screen.getByDisplayValue('SVG');
        expect(formatSelect).toBeInTheDocument();
      });
    });

    it('parses DPI parameter', async () => {
      mockURLSearchParams({ dpi: '600' });
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const dpiSelect = screen.getByDisplayValue('600 (Ultra)');
        expect(dpiSelect).toBeInTheDocument();
      });
    });

    it('parses scale factor parameter', async () => {
      mockURLSearchParams({ scale: '4' });
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const scaleSelect = screen.getByDisplayValue('4x');
        expect(scaleSelect).toBeInTheDocument();
      });
    });
  });

  describe('State Management', () => {
    it('updates URL when dashboard changes', async () => {
      const { mockReplaceState } = mockWindowHistory();
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const select = screen.getByLabelText(/dashboard/i);
        fireEvent.change(select, { target: { value: 'portfolio_history_portrait' } });
      });
      
      expect(mockReplaceState).toHaveBeenCalledWith(
        {},
        '',
        expect.stringContaining('dashboard=portfolio_history_portrait')
      );
    });

    it('updates URL when mode changes', async () => {
      const { mockReplaceState } = mockWindowHistory();
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const darkButton = screen.getByRole('button', { name: /dark/i });
        fireEvent.click(darkButton);
      });
      
      expect(mockReplaceState).toHaveBeenCalledWith(
        {},
        '',
        expect.stringContaining('mode=dark')
      );
    });

    it('updates URL when aspect ratio changes', async () => {
      const { mockReplaceState } = mockWindowHistory();
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const aspectSelect = screen.getByLabelText(/ratio/i);
        fireEvent.change(aspectSelect, { target: { value: '3:4' } });
      });
      
      expect(mockReplaceState).toHaveBeenCalledWith(
        {},
        '',
        expect.stringContaining('aspect_ratio=3:4')
      );
    });
  });

  describe('CSS Custom Properties', () => {
    it('sets CSS custom properties based on aspect ratio', async () => {
      const mockSetProperty = vi.fn();
      const mockRef = {
        current: {
          style: {
            setProperty: mockSetProperty
          }
        }
      };
      
      // Mock useRef to return our controlled ref
      vi.spyOn(React, 'useRef').mockReturnValue(mockRef);
      
      mockURLSearchParams({ aspect_ratio: '3:4' });
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        expect(mockSetProperty).toHaveBeenCalledWith('--photo-booth-width', '1080px');
        expect(mockSetProperty).toHaveBeenCalledWith('--photo-booth-height', '1440px');
      });
    });
  });

  describe('Export Functionality', () => {
    it('shows export button when dashboard is ready', async () => {
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const exportButton = screen.getByRole('button', { name: /export dashboard/i });
        expect(exportButton).toBeInTheDocument();
        expect(exportButton).not.toBeDisabled();
      });
    });

    it('disables export button when dashboard is loading', () => {
      render(<PhotoBoothDisplay />);
      
      const exportButton = screen.getByRole('button', { name: /export dashboard/i });
      expect(exportButton).toBeDisabled();
    });

    it('calls export API with correct parameters', async () => {
      mockURLSearchParams(testScenarios.portraitMode);
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(async () => {
        const exportButton = screen.getByRole('button', { name: /export dashboard/i });
        fireEvent.click(exportButton);
        
        expect(global.fetch).toHaveBeenCalledWith('/api/export-dashboard', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            dashboard_id: 'portfolio_history_portrait',
            mode: 'light',
            aspect_ratio: '3:4',
            format: 'png',
            dpi: 300,
            scale_factor: 3
          })
        });
      });
    });

    it('shows success message after successful export', async () => {
      render(<PhotoBoothDisplay />);
      
      await waitFor(async () => {
        const exportButton = screen.getByRole('button', { name: /export dashboard/i });
        fireEvent.click(exportButton);
        
        await waitFor(() => {
          expect(screen.getByText(/successfully exported/i)).toBeInTheDocument();
        });
      });
    });

    it('shows error message after failed export', async () => {
      global.fetch = mockFetchError(500, 'Export failed') as any;
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(async () => {
        const exportButton = screen.getByRole('button', { name: /export dashboard/i });
        fireEvent.click(exportButton);
        
        await waitFor(() => {
          expect(screen.getByText(/export failed/i)).toBeInTheDocument();
        });
      });
    });

    it('handles network errors gracefully', async () => {
      global.fetch = mockNetworkError() as any;
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(async () => {
        const exportButton = screen.getByRole('button', { name: /export dashboard/i });
        fireEvent.click(exportButton);
        
        await waitFor(() => {
          expect(screen.getByText(/export failed/i)).toBeInTheDocument();
        });
      });
    });
  });

  describe('Dashboard Content Rendering', () => {
    it('renders portfolio history portrait with header and footer', async () => {
      mockURLSearchParams({ dashboard: 'portfolio_history_portrait' });
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('Twitter Live Signals')).toBeInTheDocument();
        expect(screen.getByText('colemorton.com')).toBeInTheDocument();
      });
    });

    it('passes titleOnly=true to charts in portfolio history portrait', async () => {
      mockURLSearchParams({ dashboard: 'portfolio_history_portrait' });
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const titleOnlyElements = screen.getAllByTestId('chart-title-only');
        titleOnlyElements.forEach(element => {
          expect(element).toHaveTextContent('true');
        });
      });
    });

    it('applies correct theme class to dashboard', async () => {
      mockURLSearchParams({ mode: 'dark' });
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const dashboard = screen.getByTestId('dashboard-content') || 
                         document.querySelector('.photo-booth-dashboard');
        expect(dashboard).toHaveClass('dark');
      });
    });
  });

  describe('Ready State Management', () => {
    it('marks component as ready after timeout', async () => {
      render(<PhotoBoothDisplay />);
      
      // Initially should show loading
      expect(screen.getByText('Loading...')).toBeInTheDocument();
      
      // After timeout should show ready
      await waitFor(() => {
        expect(screen.getByText('Ready for screenshot')).toBeInTheDocument();
      }, { timeout: 16000 }); // Slightly longer than render_timeout
    });

    it('resets ready state when parameters change', async () => {
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('Ready for screenshot')).toBeInTheDocument();
      });
      
      // Change a parameter
      const modeButton = screen.getByRole('button', { name: /dark/i });
      fireEvent.click(modeButton);
      
      // Should reset to loading
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });
  });

  describe('Error Handling', () => {
    it('shows retry button when dashboard loading fails', async () => {
      mockDashboardLoader.getAllDashboards.mockRejectedValue(new Error('Network error'));
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        const retryButton = screen.getByRole('button', { name: /retry/i });
        expect(retryButton).toBeInTheDocument();
      });
    });

    it('handles invalid dashboard ID gracefully', async () => {
      mockURLSearchParams({ dashboard: 'invalid_dashboard' });
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        expect(screen.getByText('Dashboard Not Found')).toBeInTheDocument();
      });
    });

    it('falls back to defaults for invalid parameters', async () => {
      mockURLSearchParams(testScenarios.invalidParams);
      
      render(<PhotoBoothDisplay />);
      
      await waitFor(() => {
        // Should fall back to default values
        expect(screen.getByDisplayValue('16:9 Wide')).toBeInTheDocument();
        expect(screen.getByDisplayValue('PNG')).toBeInTheDocument();
      });
    });
  });
});