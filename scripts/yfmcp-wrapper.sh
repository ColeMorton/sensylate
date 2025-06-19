#!/bin/bash
# Wrapper script for Yahoo Finance MCP server
exec uvx --from git+https://github.com/narumiruna/yfinance-mcp.git yfmcp "$@"
