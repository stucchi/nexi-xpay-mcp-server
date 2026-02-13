# nexi-xpay-mcp-server

[![MCP](https://badge.mcpx.dev/default)](https://modelcontextprotocol.io)
[![PyPI](https://img.shields.io/pypi/v/nexi-xpay-mcp-server)](https://pypi.org/project/nexi-xpay-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Server MCP per le API **Back Office di Nexi XPay**. Permette agli assistenti AI (Claude, Cursor, ecc.) di consultare ordini, dettagli transazioni, warning e metodi di pagamento del tuo account merchant Nexi XPay.

## Strumenti

| Strumento | Descrizione |
|-----------|-------------|
| `elenco_ordini` | Elenco ordini con filtri (intervallo date, canale, stato, codice transazione) |
| `dettaglio_ordine` | Dettaglio completo di una transazione specifica |
| `warning` | Recupera warning/anomalie (default: ultimi 7 giorni) |
| `metodi_pagamento` | Elenco metodi di pagamento attivi per il merchant |

## Prerequisiti

- Python >= 3.10
- Un account merchant Nexi XPay con accesso alle API Back Office
- Le credenziali API: **Alias**, **API Key** e **Secret Key** (dal Back Office Nexi)

## Installazione

### Con Claude Code / Claude Desktop

Aggiungi al tuo file di configurazione MCP (`.mcp.json` per Claude Code, `claude_desktop_config.json` per Claude Desktop):

```json
{
  "mcpServers": {
    "nexi": {
      "command": "uvx",
      "args": ["nexi-xpay-mcp-server"],
      "env": {
        "NEXI_ALIAS": "tuo_alias",
        "NEXI_SECRET_KEY": "tua_secret_key"
      }
    }
  }
}
```

### Più merchant

Usa chiavi diverse per eseguire un'istanza per merchant:

```json
{
  "mcpServers": {
    "nexi-acme": {
      "command": "uvx",
      "args": ["nexi-xpay-mcp-server"],
      "env": {
        "NEXI_ALIAS": "acme_merchant",
        "NEXI_SECRET_KEY": "acme_secret_key",
      }
    },
    "nexi-globex": {
      "command": "uvx",
      "args": ["nexi-xpay-mcp-server"],
      "env": {
        "NEXI_ALIAS": "globex_merchant",
        "NEXI_SECRET_KEY": "globex_secret_key",
      }
    }
  }
}
```

## Variabili d'ambiente

| Variabile | Obbligatoria | Default | Descrizione |
|-----------|:------------:|---------|-------------|
| `NEXI_ALIAS` | Sì | — | Alias del merchant (usato anche come API key) |
| `NEXI_SECRET_KEY` | Sì | — | Chiave segreta per il calcolo del MAC |
| `NEXI_TEST` | No | `false` | `true` per usare l'ambiente di test |

## Sviluppo

```bash
git clone https://github.com/stucchi/nexi-xpay-mcp-server.git
cd nexi-xpay-mcp-server
uv sync
```

Esecuzione locale:

```bash
NEXI_ALIAS=tuo_alias NEXI_SECRET_KEY=tua_secret uv run nexi-xpay-mcp-server
```

## Licenza

MIT
