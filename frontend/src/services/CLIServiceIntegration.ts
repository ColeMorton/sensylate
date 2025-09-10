/**
 * CLI Service Integration Layer
 *
 * Provides interface between frontend data dependency manager and
 * backend CLI services for automatic data refreshes.
 */

import type { ChartType } from "@/types/ChartTypes";
import type { DataRefreshResult } from "@/types/DataDependencyTypes";

/**
 * CLI Service configuration
 */
export interface CLIServiceConfig {
  name: string;
  description: string;
  scriptPath: string;
  capabilities: string[];
  rateLimits: {
    requestsPerMinute: number;
    requestsPerHour: number;
  };
  authentication?: {
    required: boolean;
    method: "api-key" | "oauth" | "basic";
  };
}

/**
 * CLI command execution request
 */
export interface CLICommandRequest {
  service: string;
  command: string;
  args: string[];
  timeout?: number;
  environment?: Record<string, string>;
  workingDirectory?: string;
}

/**
 * CLI command execution result
 */
export interface CLICommandResult {
  success: boolean;
  stdout: string;
  stderr: string;
  exitCode: number;
  duration: number;
  error?: string;
}

/**
 * Data refresh request for CLI services
 */
export interface CLIDataRefreshRequest {
  chartType: ChartType;
  service: string;
  dataType: string;
  parameters?: Record<string, any>;
  outputPath?: string;
}

/**
 * Rate limiter for CLI service calls
 */
class RateLimiter {
  private requests: Map<string, number[]> = new Map();

  private cleanupOldRequests(serviceId: string, windowMs: number): void {
    const now = Date.now();
    const requests = this.requests.get(serviceId) || [];
    const filtered = requests.filter((timestamp) => now - timestamp < windowMs);
    this.requests.set(serviceId, filtered);
  }

  public canMakeRequest(serviceId: string, config: CLIServiceConfig): boolean {
    // Check per-minute limit
    this.cleanupOldRequests(serviceId, 60 * 1000); // 1 minute
    const minuteRequests = this.requests.get(serviceId) || [];
    if (minuteRequests.length >= config.rateLimits.requestsPerMinute) {
      return false;
    }

    // Check per-hour limit
    this.cleanupOldRequests(serviceId, 60 * 60 * 1000); // 1 hour
    const hourRequests = this.requests.get(serviceId) || [];
    if (hourRequests.length >= config.rateLimits.requestsPerHour) {
      return false;
    }

    return true;
  }

  public recordRequest(serviceId: string): void {
    const requests = this.requests.get(serviceId) || [];
    requests.push(Date.now());
    this.requests.set(serviceId, requests);
  }

  public getNextAvailableTime(
    serviceId: string,
    config: CLIServiceConfig,
  ): number {
    this.cleanupOldRequests(serviceId, 60 * 1000);
    const requests = this.requests.get(serviceId) || [];

    if (requests.length < config.rateLimits.requestsPerMinute) {
      return 0; // Can make request immediately
    }

    // Calculate when the oldest request in the window expires
    const oldestRequest = Math.min(...requests);
    return oldestRequest + 60 * 1000 - Date.now();
  }
}

/**
 * CLI Service Integration Manager
 */
export class CLIServiceIntegration {
  private services: Map<string, CLIServiceConfig> = new Map();
  private rateLimiter = new RateLimiter();
  private requestQueue: Array<{
    request: CLIDataRefreshRequest;
    resolve: (result: DataRefreshResult) => void;
    reject: (error: Error) => void;
  }> = [];
  private processing = false;

  constructor() {
    this.loadServiceConfigurations();
    this.startQueueProcessor();
  }

  /**
   * Load CLI service configurations
   */
  private loadServiceConfigurations(): void {
    // Load from configuration (in real implementation, this would load from config file)
    const services: CLIServiceConfig[] = [
      {
        name: "Yahoo Finance CLI",
        description: "Real-time and historical market data",
        scriptPath: "scripts/yahoo_finance_cli.py",
        capabilities: ["stock-prices", "market-data", "benchmarks"],
        rateLimits: {
          requestsPerMinute: 60,
          requestsPerHour: 2000,
        },
        authentication: {
          required: false,
          method: "api-key",
        },
      },
      {
        name: "Financial Modeling Prep CLI",
        description: "Advanced financial data and fundamentals",
        scriptPath: "scripts/fmp_cli.py",
        capabilities: ["fundamentals", "financial-statements", "market-data"],
        rateLimits: {
          requestsPerMinute: 300,
          requestsPerHour: 10000,
        },
        authentication: {
          required: true,
          method: "api-key",
        },
      },
      {
        name: "Alpha Vantage CLI",
        description: "Financial market data and technical indicators",
        scriptPath: "scripts/alpha_vantage_cli.py",
        capabilities: ["stock-prices", "technical-indicators", "market-data"],
        rateLimits: {
          requestsPerMinute: 5,
          requestsPerHour: 500,
        },
        authentication: {
          required: true,
          method: "api-key",
        },
      },
      {
        name: "CoinGecko CLI",
        description: "Cryptocurrency market data",
        scriptPath: "scripts/coingecko_cli.py",
        capabilities: ["crypto-prices", "market-data"],
        rateLimits: {
          requestsPerMinute: 10,
          requestsPerHour: 1000,
        },
      },
    ];

    services.forEach((service) => {
      this.services.set(
        service.name.toLowerCase().replace(/\s+/g, "-"),
        service,
      );
    });
  }

  /**
   * Start the request queue processor
   */
  private startQueueProcessor(): void {
    setInterval(() => {
      if (!this.processing && this.requestQueue.length > 0) {
        this.processQueue();
      }
    }, 1000); // Check queue every second
  }

  /**
   * Process queued requests
   */
  private async processQueue(): Promise<void> {
    if (this.processing || this.requestQueue.length === 0) {
      return;
    }

    this.processing = true;

    const { request, resolve, reject } = this.requestQueue.shift()!;
    try {
      const result = await this.executeDataRefresh(request);
      resolve(result);
    } catch (error) {
      reject(error instanceof Error ? error : new Error("Unknown error"));
    } finally {
      this.processing = false;
    }
  }

  /**
   * Get available CLI services
   */
  public getAvailableServices(): CLIServiceConfig[] {
    return Array.from(this.services.values());
  }

  /**
   * Get specific CLI service configuration
   */
  public getService(serviceId: string): CLIServiceConfig | undefined {
    return this.services.get(serviceId);
  }

  /**
   * Check if service can handle a specific capability
   */
  public canServiceHandle(serviceId: string, capability: string): boolean {
    const service = this.services.get(serviceId);
    return service?.capabilities.includes(capability) ?? false;
  }

  /**
   * Request data refresh through CLI service
   */
  public async requestDataRefresh(
    request: CLIDataRefreshRequest,
  ): Promise<DataRefreshResult> {
    const service = this.services.get(request.service);
    if (!service) {
      return {
        success: false,
        status: {
          status: "error",
          ageHours: 0,
          retryCount: 0,
          refreshing: false,
          error: `Service '${request.service}' not found`,
        },
        duration: 0,
        error: {
          message: `CLI service '${request.service}' is not available`,
          code: "SERVICE_NOT_FOUND",
          retryable: false,
        },
        source: {
          type: "cli-api",
          location: request.service,
          refreshMethod: "api-poll",
          frequency: "on-demand",
          cliService: request.service,
        },
      };
    }

    // Check rate limits
    if (!this.rateLimiter.canMakeRequest(request.service, service)) {
      const nextAvailable = this.rateLimiter.getNextAvailableTime(
        request.service,
        service,
      );

      return {
        success: false,
        status: {
          status: "error",
          ageHours: 0,
          retryCount: 0,
          refreshing: false,
          error: "Rate limit exceeded",
        },
        duration: 0,
        error: {
          message: `Rate limit exceeded. Try again in ${Math.ceil(nextAvailable / 1000)} seconds`,
          code: "RATE_LIMIT_EXCEEDED",
          retryable: true,
        },
        source: {
          type: "cli-api",
          location: service.scriptPath,
          refreshMethod: "api-poll",
          frequency: "on-demand",
          cliService: request.service,
        },
      };
    }

    // Queue the request if we can't process immediately
    return new Promise((resolve, reject) => {
      this.requestQueue.push({ request, resolve, reject });
    });
  }

  /**
   * Execute data refresh through CLI service
   */
  private async executeDataRefresh(
    request: CLIDataRefreshRequest,
  ): Promise<DataRefreshResult> {
    const service = this.services.get(request.service)!;
    const startTime = Date.now();

    try {
      // Record the request for rate limiting
      this.rateLimiter.recordRequest(request.service);

      // Build CLI command
      const command = this.buildCLICommand(service, request);

      // Execute CLI command
      const result = await this.executeCLICommand(command);

      const duration = Date.now() - startTime;

      if (result.success) {
        return {
          success: true,
          status: {
            status: "available",
            lastUpdated: Date.now(),
            ageHours: 0,
            retryCount: 0,
            refreshing: false,
            lastUpdateSource: "api",
          },
          recordsUpdated: this.estimateRecordsFromOutput(result.stdout),
          duration,
          source: {
            type: "cli-api",
            location: service.scriptPath,
            refreshMethod: "api-poll",
            frequency: "on-demand",
            cliService: request.service,
          },
        };
      } else {
        return {
          success: false,
          status: {
            status: "error",
            lastUpdated: Date.now(),
            ageHours: 0,
            retryCount: 1,
            refreshing: false,
            error: result.error || result.stderr,
          },
          duration,
          error: {
            message: result.error || result.stderr || "CLI command failed",
            code: `CLI_ERROR_${result.exitCode}`,
            retryable: result.exitCode !== 127, // 127 = command not found
          },
          source: {
            type: "cli-api",
            location: service.scriptPath,
            refreshMethod: "api-poll",
            frequency: "on-demand",
            cliService: request.service,
          },
        };
      }
    } catch (error) {
      const duration = Date.now() - startTime;

      return {
        success: false,
        status: {
          status: "error",
          lastUpdated: Date.now(),
          ageHours: 0,
          retryCount: 1,
          refreshing: false,
          error: error instanceof Error ? error.message : "Unknown error",
        },
        duration,
        error: {
          message:
            error instanceof Error ? error.message : "CLI execution failed",
          code: "CLI_EXECUTION_ERROR",
          retryable: true,
        },
        source: {
          type: "cli-api",
          location: service.scriptPath,
          refreshMethod: "api-poll",
          frequency: "on-demand",
          cliService: request.service,
        },
      };
    }
  }

  /**
   * Build CLI command based on service and request
   */
  private buildCLICommand(
    service: CLIServiceConfig,
    request: CLIDataRefreshRequest,
  ): CLICommandRequest {
    // This would build the appropriate command based on chart type and data requirements
    let command = "";
    let args: string[] = [];

    switch (request.chartType) {
      case "live-signals-benchmark-comparison":
        if (service.capabilities.includes("market-data")) {
          command = "get-benchmarks";
          args = ["--symbols", "SPY,QQQ,BITCOIN", "--format", "csv"];
          if (request.outputPath) {
            args.push("--output", request.outputPath);
          }
        }
        break;

      case "open-positions-pnl-timeseries":
        if (service.capabilities.includes("stock-prices")) {
          command = "get-prices";
          args = ["--realtime", "--format", "csv"];
          if (request.parameters?.symbols) {
            args.push("--symbols", request.parameters.symbols.join(","));
          }
        }
        break;

      default:
        command = "help";
        args = [];
    }

    return {
      service: request.service,
      command,
      args,
      timeout: 30000, // 30 seconds
      workingDirectory: process.cwd(),
    };
  }

  /**
   * Execute CLI command (simulation - in real implementation would call actual CLI)
   */
  private async executeCLICommand(
    request: CLICommandRequest,
  ): Promise<CLICommandResult> {
    // Simulate CLI command execution
    const startTime = Date.now();

    // Simulate network delay
    await new Promise((resolve) =>
      setTimeout(resolve, Math.random() * 2000 + 1000),
    );

    // Simulate different outcomes
    const success = Math.random() > 0.1; // 90% success rate

    if (success) {
      return {
        success: true,
        stdout: `Successfully executed ${request.command} for ${request.service}\nProcessed 150 records\nOutput saved to ${request.args.join(" ")}`,
        stderr: "",
        exitCode: 0,
        duration: Date.now() - startTime,
      };
    } else {
      return {
        success: false,
        stdout: "",
        stderr: `Error: Failed to execute ${request.command} - API rate limit exceeded`,
        exitCode: 1,
        duration: Date.now() - startTime,
        error: "CLI command failed with exit code 1",
      };
    }
  }

  /**
   * Estimate number of records from CLI output
   */
  private estimateRecordsFromOutput(stdout: string): number | undefined {
    const match = stdout.match(/Processed (\d+) records/);
    return match ? parseInt(match[1], 10) : undefined;
  }

  /**
   * Test CLI service connectivity
   */
  public async testService(serviceId: string): Promise<{
    available: boolean;
    version?: string;
    error?: string;
  }> {
    const service = this.services.get(serviceId);
    if (!service) {
      return {
        available: false,
        error: "Service not found",
      };
    }

    try {
      const result = await this.executeCLICommand({
        service: serviceId,
        command: "version",
        args: [],
        timeout: 5000,
      });

      return {
        available: result.success,
        version: result.success ? result.stdout.trim() : undefined,
        error: result.success ? undefined : result.error,
      };
    } catch (error) {
      return {
        available: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  /**
   * Get rate limit status for all services
   */
  public getRateLimitStatus(): Record<
    string,
    {
      remaining: {
        minute: number;
        hour: number;
      };
      resetTime: {
        minute: number;
        hour: number;
      };
    }
  > {
    const status: Record<string, any> = {};

    this.services.forEach((config, serviceId) => {
      const minuteRequests = this.rateLimiter.getNextAvailableTime(
        serviceId,
        config,
      );

      status[serviceId] = {
        remaining: {
          minute: Math.max(
            0,
            config.rateLimits.requestsPerMinute -
              (this.rateLimiter as any).requests.get(serviceId)?.length || 0,
          ),
          hour: Math.max(
            0,
            config.rateLimits.requestsPerHour -
              (this.rateLimiter as any).requests.get(serviceId)?.length || 0,
          ),
        },
        resetTime: {
          minute: minuteRequests,
          hour: minuteRequests, // Simplified - in reality would track separately
        },
      };
    });

    return status;
  }
}

// Export singleton instance
export const cliServiceIntegration = new CLIServiceIntegration();
export default cliServiceIntegration;
