/**
 * Debug Server Errors Script
 *
 * This script starts a new dev server and captures detailed error output
 * to understand what's causing the blog post failures.
 */

import { spawn } from 'child_process';
import { writeFileSync } from 'fs';
import path from 'path';

const DEBUG_OUTPUT_DIR = path.join(process.cwd(), 'debug-output');
const DEV_SERVER_URL = 'http://localhost:4322'; // Different port to avoid conflicts

class ServerErrorDebugger {
  constructor() {
    this.serverProcess = null;
    this.errorLogs = [];
    this.outputLogs = [];
  }

  async startDevServer() {
    console.log('🚀 Starting dev server with error capture...');

    return new Promise((resolve, reject) => {
      // Kill any existing servers on our test port
      spawn('pkill', ['-f', 'astro dev.*4322'], { stdio: 'inherit' });

      setTimeout(() => {
        this.serverProcess = spawn('yarn', ['dev', '--port', '4322'], {
          cwd: process.cwd(),
          env: {
            ...process.env,
            NODE_ENV: 'development',
            PUBLIC_FEATURE_CHARTS_PAGE: 'false'
          }
        });

        this.serverProcess.stdout.on('data', (data) => {
          const output = data.toString();
          this.outputLogs.push({ type: 'stdout', message: output, timestamp: Date.now() });
          console.log('📝 [SERVER]', output.trim());

          if (output.includes('ready in')) {
            console.log('✅ Dev server ready!');
            resolve();
          }
        });

        this.serverProcess.stderr.on('data', (data) => {
          const error = data.toString();
          this.errorLogs.push({ type: 'stderr', message: error, timestamp: Date.now() });
          console.log('❌ [ERROR]', error.trim());
        });

        this.serverProcess.on('error', (error) => {
          console.error('💥 Process error:', error);
          reject(error);
        });

        // Timeout after 30 seconds
        setTimeout(() => {
          if (this.serverProcess) {
            console.log('⏰ Server start timeout');
            resolve(); // Continue anyway
          }
        }, 30000);
      }, 2000);
    });
  }

  async testBlogRoutes() {
    console.log('🧪 Testing blog routes...');

    const testRoutes = [
      '/blog',
      '/blog/post-1',
      '/blog/adbe-fundamental-analysis-20250723'
    ];

    for (const route of testRoutes) {
      console.log(`📍 Testing: ${route}`);

      try {
        const response = await fetch(`${DEV_SERVER_URL}${route}`);
        const content = await response.text();

        console.log(`   Status: ${response.status}`);

        if (!response.ok) {
          console.log(`   Error content preview: ${content.substring(0, 200)}...`);

          this.errorLogs.push({
            type: 'http_error',
            route,
            status: response.status,
            content: content.substring(0, 1000),
            timestamp: Date.now()
          });
        } else {
          console.log(`   ✅ Success`);
        }

      } catch (error) {
        console.log(`   💥 Request failed: ${error.message}`);
        this.errorLogs.push({
          type: 'request_error',
          route,
          error: error.message,
          timestamp: Date.now()
        });
      }

      // Wait for any server-side errors to be logged
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }

  generateReport() {
    const report = {
      timestamp: new Date().toISOString(),
      summary: {
        totalErrors: this.errorLogs.length,
        totalOutputs: this.outputLogs.length
      },
      errorLogs: this.errorLogs,
      outputLogs: this.outputLogs
    };

    const reportPath = path.join(DEBUG_OUTPUT_DIR, 'server-error-debug.json');
    writeFileSync(reportPath, JSON.stringify(report, null, 2));

    console.log(`📄 Debug report saved to: ${reportPath}`);

    // Show recent errors
    console.log('\n🔍 Recent Errors:');
    this.errorLogs.slice(-5).forEach((log, index) => {
      console.log(`${index + 1}. [${log.type}] ${log.message || log.error || JSON.stringify(log)}`);
    });

    return reportPath;
  }

  async cleanup() {
    if (this.serverProcess) {
      console.log('🧹 Cleaning up dev server...');
      this.serverProcess.kill('SIGTERM');

      // Force kill if it doesn't stop
      setTimeout(() => {
        if (this.serverProcess && !this.serverProcess.killed) {
          this.serverProcess.kill('SIGKILL');
        }
      }, 5000);
    }
  }

  async run() {
    try {
      await this.startDevServer();
      await this.testBlogRoutes();
      this.generateReport();
    } catch (error) {
      console.error('💥 Debug run failed:', error);
    } finally {
      await this.cleanup();
    }
  }
}

// Main execution
async function main() {
  console.log('🔍 Server Error Debugger');
  console.log('='.repeat(50));

  const errorDebugger = new ServerErrorDebugger();
  await errorDebugger.run();

  console.log('\n🎉 Error debugging complete!');
}

main().catch(console.error);
