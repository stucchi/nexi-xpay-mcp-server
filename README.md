# nexi-xpay-mcp-server

[![MCP](https://badge.mcpx.dev/default)](https://modelcontextprotocol.io)
[![PyPI](https://img.shields.io/pypi/v/nexi-xpay-mcp-server)](https://pypi.org/project/nexi-xpay-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MCP server for the **Nexi XPay Back Office APIs**. Enables AI assistants (Claude, Cursor, etc.) to query orders, transaction details, warnings/anomalies, and payment methods from your Nexi XPay merchant account.

## Tools

| Tool | Description |
|------|-------------|
| `list_orders` | List orders with filters (date range, channel, status, transaction code) |
| `order_details` | Full details of a specific transaction |
| `warnings` | Retrieve warnings/anomalies (default: last 7 days) |
| `payment_methods` | List active payment methods for the merchant |

## Prerequisites

- Python >= 3.10
- A Nexi XPay merchant account with Back Office API access
- API credentials: **Alias**, **API Key** and **Secret Key** (from Nexi Back Office)

## Installation

```bash
uvx nexi-xpay-mcp-server
```

## Usage in .mcp.json

Add to your MCP configuration file (`.mcp.json` for Claude Code, `claude_desktop_config.json` for Claude Desktop):

```json
{
  "mcpServers": {
    "nexi": {
      "command": "uvx",
      "args": ["nexi-xpay-mcp-server"],
      "env": {
        "NEXI_ALIAS": "your_alias",
        "NEXI_SECRET_KEY": "your_secret_key"
      }
    }
  }
}
```

### Multiple merchants

Use different keys to run one instance per merchant:

```json
{
  "mcpServers": {
    "nexi-acme": {
      "command": "uvx",
      "args": ["nexi-xpay-mcp-server"],
      "env": {
        "NEXI_ALIAS": "acme_merchant",
        "NEXI_SECRET_KEY": "acme_secret_key"
      }
    },
    "nexi-globex": {
      "command": "uvx",
      "args": ["nexi-xpay-mcp-server"],
      "env": {
        "NEXI_ALIAS": "globex_merchant",
        "NEXI_SECRET_KEY": "globex_secret_key"
      }
    }
  }
}
```

## Environment variables

| Variable | Required | Default | Description |
|----------|:--------:|---------|-------------|
| `NEXI_ALIAS` | Yes | — | Merchant alias (also used as API key) |
| `NEXI_SECRET_KEY` | Yes | — | Secret key for MAC calculation |
| `NEXI_TEST` | No | `false` | Set to `true` to use the test environment |

## Development

```bash
git clone https://github.com/stucchi/nexi-xpay-mcp-server.git
cd nexi-xpay-mcp-server
uv sync
```

Local run:

```bash
NEXI_ALIAS=your_alias NEXI_SECRET_KEY=your_secret uv run nexi-xpay-mcp-server
```

## License

MIT

<!-- mcp-name: io.github.stucchi/nexi-xpay -->
