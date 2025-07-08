# Complete Claude Code User Guide for MCP Servers

## Critical Known Issue: protocolVersion Validation Bug

As of July 2025, Claude Code (version 0.2.69) has a **critical blocking bug** that prevents MCP servers from connecting properly. This bug causes a protocolVersion validation error even with correct configurations. Until Anthropic fixes this issue, **Claude Desktop remains the more reliable option for MCP server integration**.

## 1. Common MCP Server Issues and Errors

### Most Common Errors

#### protocolVersion Validation Error (Current Blocker)
```json
[
  {
    "code": "invalid_type",
    "expected": "string",
    "received": "undefined",
    "path": ["protocolVersion"],
    "message": "Required"
  }
]
```
**Status**: No workaround available - requires Anthropic fix

#### Server Not Recognized
```
[info] Connected to MCP server [name]!
[error] Could not attach to MCP server [name]
[error] Server disconnected
```
**Solution**: Check configuration syntax and restart Claude Code

#### Path Resolution Failures
```
'C:\Program' is not recognized as an internal or external command
Server transport closed unexpectedly
```
**Solution**: Use absolute paths and escape spaces properly

### Platform-Specific Issues
- **macOS**: Keychain access errors, NVM path resolution problems
- **Windows**: Spaces in paths cause failures, WSL integration issues
- **Linux**: Permission problems, socket communication errors

## 2. How to Add MCP Servers to Claude Code

### Method 1: CLI Commands (Recommended)
```bash
# Basic server addition
claude mcp add <name> <command> [args...]

# With environment variables
claude mcp add github-server -e GITHUB_TOKEN=your-token -- npx -y @modelcontextprotocol/server-github

# Add remote servers
claude mcp add --transport sse remote-api https://api.example.com/mcp
claude mcp add --transport http api-server https://api.example.com/mcp
```

### Method 2: Direct Configuration File Editing
Edit `~/.claude.json` (Linux/macOS) or equivalent:
```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

### Configuration Scopes
1. **Local** (default): Project-specific, user-specific
2. **Project**: Shared via `.mcp.json` in project root
3. **User**: Global across all projects

```bash
# Add to specific scope
claude mcp add server-name -s project -- command args
claude mcp add server-name -s user -- command args
```

## 3. How to Change/Modify MCP Server Configurations

### Step-by-Step Modification Process
1. Stop Claude Code completely
2. Edit configuration file:
   - User config: `~/.claude.json`
   - Project config: `.mcp.json`
3. Make changes (example):
```json
{
  "mcpServers": {
    "github-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "new-token-here"
      }
    }
  }
}
```
4. Save file
5. Restart Claude Code
6. Verify: `claude mcp list`

### Important Notes
- No hot-reload capability exists
- All changes require full Claude Code restart
- Validate JSON syntax before saving

## 4. How to Restart MCP Servers Properly

### Current Limitations
- **No individual server restart** capability
- **No hot-reload** functionality
- Changes require full Claude Code restart

### Restart Procedures

#### Complete Restart (Required for all changes)
1. Close Claude Code completely
2. Make configuration changes if needed
3. Restart Claude Code
4. Verify servers: `/mcp` command in Claude Code

#### Command-Line Verification
```bash
# List all servers and status
claude mcp list --verbose

# Check specific server
claude mcp get server-name

# Reset project permissions
claude mcp reset-project-choices
```

#### macOS Only
```bash
# Restart Claude application
claude mcp restart
```

## 5. How to Reload MCP Servers

### Current Status
**Reload functionality is not available**. All configuration changes require:
1. Complete Claude Code shutdown
2. Configuration file modification
3. Claude Code restart

### Workaround Process
```bash
# 1. Stop Claude Code
# 2. Modify configuration
# 3. Restart Claude Code
# 4. Verify
claude mcp list
```

## 6. Troubleshooting When MCP Servers Aren't Recognized

### Systematic Troubleshooting Steps

#### Step 1: Verify Configuration
```bash
# Check JSON syntax
cat ~/.claude.json | jq .

# List configured servers
claude mcp list
```

#### Step 2: Test Server Independently
```bash
# Use MCP Inspector
npx -y @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem /path

# Test manual execution
npx @modelcontextprotocol/server-name --help
```

#### Step 3: Check Environment
```bash
# Verify Node.js version (v18+ required)
node --version

# Check environment variables
env | grep -E "API_KEY|TOKEN"

# Verify command paths
which node
which npx
```

#### Step 4: Enable Debug Mode
```bash
# Start with debug logging
claude --mcp-debug

# Set environment variables
MCP_CLAUDE_DEBUG=true claude
```

#### Step 5: Review Logs
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log

# Linux
tail -f ~/.claude/logs/mcp-server-*.log
```

### Common Recognition Issues and Fixes

1. **Path Issues**: Use absolute paths
```json
{
  "command": "/usr/local/bin/node",
  "args": ["/absolute/path/to/server.js"]
}
```

2. **NVM Users**: Specify full paths
```json
{
  "command": "/Users/username/.nvm/versions/node/v20.0.0/bin/node",
  "args": ["/Users/username/.nvm/versions/node/v20.0.0/lib/node_modules/package/dist/index.js"]
}
```

3. **Windows Spaces**: Escape properly
```json
{
  "command": "C:\\Program Files\\nodejs\\node.exe",
  "args": ["C:\\Users\\username\\server.js"]
}
```

## 7. Best Practices for MCP Server Management

### Configuration Management
1. **Use version control** for `.mcp.json` (project scope)
2. **Never commit API keys** - use environment variables
3. **Validate JSON syntax** before saving
4. **Document server purposes** in comments

### Security Best Practices
```json
{
  "mcpServers": {
    "secure-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "server-package"],
      "env": {
        "API_KEY": "${API_KEY}",  // Reference env var
        "ENDPOINT": "https://api.example.com"
      }
    }
  }
}
```

### Performance Optimization
1. **Host servers in US data centers** for lower latency
2. **Implement caching** in custom servers
3. **Use appropriate transport**:
   - STDIO: Local processes
   - SSE: Remote HTTP-compatible
   - WebSocket: Real-time bidirectional

### Multi-Server Strategy
```bash
# User-scoped (global)
claude mcp add utilities -s user -- npx utility-server

# Project-scoped (team sharing)
claude mcp add project-db -s project -- node ./local-db.js

# Local-scoped (personal)
claude mcp add dev-tools -- npx dev-server
```

## 8. Configuration File Formats and Locations

### File Locations by Platform

#### Linux/WSL/macOS
- User config: `~/.claude.json`
- Project config: `.mcp.json` (project root)
- Settings: `~/.claude/settings.json`
- Logs: `~/.claude/logs/`

#### Windows (via WSL)
- Same as Linux within WSL environment

### Configuration Format Examples

#### Basic Structure
```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "command-to-run",
      "args": ["arg1", "arg2"],
      "env": {
        "KEY": "value"
      }
    }
  }
}
```

#### Complete Example
```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/john/Documents"]
    },
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    },
    "postgres": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-postgres", "--db-url", "postgresql://user:pass@localhost:5432/mydb"]
    }
  }
}
```

## 9. Debug/Logging Procedures

### Enable Debug Logging

#### Method 1: Command-Line Flags
```bash
# Enable MCP debug mode
claude --mcp-debug

# Verbose logging
claude --verbose
```

#### Method 2: Environment Variables
```bash
# Set debug environment
MCP_CLAUDE_DEBUG=true claude
MCP_LOG_LEVEL=debug claude
```

#### Method 3: Configuration
```json
{
  "mcpServers": {
    "debug-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "MCP_CLAUDE_DEBUG": "true",
        "LOG_LEVEL": "debug"
      }
    }
  }
}
```

### Log File Locations
- **macOS**: `~/Library/Logs/Claude/mcp*.log`
- **Linux**: `~/.claude/logs/mcp-server-*.log`
- **Server logs**: Named `mcp-server-[SERVERNAME].log`

### Using MCP Inspector
```bash
# Test any server
npx -y @modelcontextprotocol/inspector

# Test specific server
npx -y @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem /path

# Test local development server
npx -y @modelcontextprotocol/inspector node ./my-server.js
```

### Debug Commands in Claude Code
```bash
# Check server status
/mcp

# View available tools
/tools

# Check configuration
/config
```

## 10. Known Limitations and Bugs

### Critical Bugs (July 2025)
1. **protocolVersion Validation Bug**: Prevents all MCP server connections
   - Status: Awaiting Anthropic fix
   - Workaround: Use Claude Desktop

2. **OAuth Authentication Failures**: Remote servers with OAuth don't work
   - Affects: GitHub MCP server, other OAuth-based services
   - Workaround: None available

3. **No Hot-Reload**: Configuration changes require full restart
   - Status: Feature not implemented
   - Workaround: Manual restart required

### Feature Limitations vs Claude Desktop
- Limited remote server support
- Incomplete OAuth implementation
- Fewer transport types supported
- Less robust error handling
- No individual server restart capability

### Version Requirements
- **Node.js**: v18 minimum, v20+ recommended
- **Avoid**: Node.js v23.10.0 (macOS compatibility issues)
- **NVM Users**: May experience path resolution problems

### Expected Timeline
- **Short-term (1-2 months)**: Critical bug fixes
- **Medium-term (3-6 months)**: Feature parity with Claude Desktop
- **Long-term (6+ months)**: Stable production-ready support

## Quick Reference Commands

```bash
# Add servers
claude mcp add name command args
claude mcp add name -e KEY=value -- command args
claude mcp add --transport sse name https://api.com/mcp

# Manage servers
claude mcp list
claude mcp get server-name
claude mcp remove server-name
claude mcp reset-project-choices

# Debug
claude --mcp-debug
MCP_CLAUDE_DEBUG=true claude
npx -y @modelcontextprotocol/inspector

# In Claude Code
/mcp         # Check status
/tools       # List tools
/config      # View config
```

## Recommendations

Given the current state of MCP support in Claude Code:

1. **Use Claude Desktop** for production MCP workflows
2. **Stick to Node.js v20 LTS** for compatibility
3. **Use absolute paths** in all configurations
4. **Test servers independently** before adding
5. **Monitor GitHub issues** for bug fix updates
6. **Join the Discord community** for support

The MCP implementation in Claude Code is evolving rapidly. While it shows promise, the current research preview has significant limitations that impact reliability. Users should expect issues and be prepared to troubleshoot or fall back to Claude Desktop for critical workflows.
