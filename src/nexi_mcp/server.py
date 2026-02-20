from __future__ import annotations

import json
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP

from nexi_mcp.config import get_config
from nexi_mcp.date_parser import parse_periodo
from nexi_mcp.tools.dettaglio_ordine import dettaglio_ordine as _dettaglio_ordine
from nexi_mcp.tools.elenco_ordini import elenco_ordini as _elenco_ordini
from nexi_mcp.tools.metodi_pagamento import metodi_pagamento as _metodi_pagamento
from nexi_mcp.tools.warning import warning as _warning

config = get_config()
mcp = FastMCP(f"nexi-mcp-server ({config.alias})")


def _format(result: dict[str, Any]) -> str:
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
async def list_orders(
    periodo: Annotated[
        str,
        'Search period. Exact format: "dd/mm/yyyy - dd/mm/yyyy" (e.g. "01/01/2026 - 31/01/2026"). '
        'Also accepts natural expressions: "today", "yesterday", "last week", "last month", '
        '"last N days", "last N months" (max 90 days).',
    ],
    canale: Annotated[str, "Payment channel"] = "All",
    codiceTransazione: Annotated[str, "Filter by specific transaction code"] = "",
    stato: Annotated[list[str] | None, "Array of statuses to filter"] = None,
) -> str:
    """Retrieve the list of orders from Nexi XPay Back Office. Supports filters by period, channel, status, and transaction code."""
    result = await _elenco_ordini(
        periodo=parse_periodo(periodo),
        canale=canale,
        codice_transazione=codiceTransazione,
        stato=stato,
    )
    return _format(result)


@mcp.tool()
async def order_details(
    codiceTransazione: Annotated[str, "Merchant transaction identifier"],
) -> str:
    """Retrieve full details of a specific order from Nexi XPay Back Office by transaction code."""
    result = await _dettaglio_ordine(codice_transazione=codiceTransazione)
    return _format(result)


@mcp.tool()
async def warnings(
    codiceTransazione: Annotated[str | None, "Transaction identifier"] = None,
    dataTransazioneDal: Annotated[str | None, 'Start date in "dd/mm/yyyy hh:mm:ss" format'] = None,
    dataTransazioneAl: Annotated[str | None, 'End date in "dd/mm/yyyy hh:mm:ss" format'] = None,
) -> str:
    """Retrieve warnings/anomalies from Nexi XPay Back Office. Can filter by transaction code or date range."""
    result = await _warning(
        codice_transazione=codiceTransazione,
        data_transazione_dal=dataTransazioneDal,
        data_transazione_al=dataTransazioneAl,
    )
    return _format(result)


@mcp.tool()
async def payment_methods(
    platform: Annotated[str, "CMS name (default: custom)"] = "custom",
    platformVers: Annotated[str, "CMS version (default: 0)"] = "0",
    pluginVers: Annotated[str, "Plugin version (default: 0)"] = "0",
) -> str:
    """Retrieve active payment methods for a merchant from Nexi XPay Back Office."""
    result = await _metodi_pagamento(
        platform=platform,
        platform_vers=platformVers,
        plugin_vers=pluginVers,
    )
    return _format(result)


def main() -> None:
    mcp.run(transport="stdio")
