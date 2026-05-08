<div align="center">

# Date Calculator Ai MCP

**Date Calculator AI MCP Server — Date math tools.**

[![PyPI](https://img.shields.io/pypi/v/meok-date-calculator-ai-mcp)](https://pypi.org/project/meok-date-calculator-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Date Calculator AI MCP Server — Date math tools.

## Tools

| Tool | Description |
|------|-------------|
| `days_between` | Calculate days between two dates (YYYY-MM-DD). Also returns weeks, months estima |
| `add_business_days` | Add business days to a date, optionally excluding holidays (comma-separated YYYY |
| `next_weekday` | Find the next occurrence of a weekday. target_day: Monday-Sunday. occurrence: nt |
| `format_date` | Parse and reformat dates. Common formats: %Y-%m-%d, %d/%m/%Y, %m/%d/%Y, %B %d %Y |

## Installation

```bash
pip install meok-date-calculator-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "date-calculator-ai": {
      "command": "python",
      "args": ["-m", "meok_date_calculator_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
