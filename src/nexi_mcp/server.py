from __future__ import annotations

import json
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP

from nexi_mcp.config import get_config
from nexi_mcp.tools.dettaglio_ordine import dettaglio_ordine as _dettaglio_ordine
from nexi_mcp.tools.elenco_ordini import elenco_ordini as _elenco_ordini
from nexi_mcp.tools.metodi_pagamento import metodi_pagamento as _metodi_pagamento
from nexi_mcp.tools.warning import warning as _warning

config = get_config()
mcp = FastMCP(f"nexi-mcp-server ({config.alias})")


def _format(result: dict[str, Any]) -> str:
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
async def elenco_ordini(
    periodo: Annotated[str, 'Intervallo date nel formato "gg/mm/aaaa - gg/mm/aaaa" (max 90 giorni)'],
    canale: Annotated[str, "Canale di pagamento"] = "All",
    codiceTransazione: Annotated[str, "Filtro per transazione specifica"] = "",
    stato: Annotated[list[str] | None, "Array di stati da filtrare"] = None,
) -> str:
    """Recupera l'elenco degli ordini dal Back Office Nexi XPay. Supporta filtri per periodo, canale, stato e codice transazione."""
    result = await _elenco_ordini(
        periodo=periodo,
        canale=canale,
        codice_transazione=codiceTransazione,
        stato=stato,
    )
    return _format(result)


@mcp.tool()
async def dettaglio_ordine(
    codiceTransazione: Annotated[str, "Identificativo della transazione merchant"],
) -> str:
    """Recupera i dettagli di un ordine specifico dal Back Office Nexi XPay utilizzando il codice transazione."""
    result = await _dettaglio_ordine(codice_transazione=codiceTransazione)
    return _format(result)


@mcp.tool()
async def warning(
    codiceTransazione: Annotated[str | None, "Identificativo della transazione"] = None,
    dataTransazioneDal: Annotated[str | None, 'Data di inizio nel formato "gg/mm/aaaa hh:mm:ss"'] = None,
    dataTransazioneAl: Annotated[str | None, 'Data di fine nel formato "gg/mm/aaaa hh:mm:ss"'] = None,
) -> str:
    """Recupera i warning/anomalie dal Back Office Nexi XPay. È possibile filtrare per codice transazione o intervallo di date."""
    result = await _warning(
        codice_transazione=codiceTransazione,
        data_transazione_dal=dataTransazioneDal,
        data_transazione_al=dataTransazioneAl,
    )
    return _format(result)


@mcp.tool()
async def metodi_pagamento(
    platform: Annotated[str, "Nome del CMS (default: custom)"] = "custom",
    platformVers: Annotated[str, "Versione del CMS (default: 0)"] = "0",
    pluginVers: Annotated[str, "Versione del plugin (default: 0)"] = "0",
) -> str:
    """Recupera i metodi di pagamento attivi per un merchant dal Back Office Nexi XPay."""
    result = await _metodi_pagamento(
        platform=platform,
        platform_vers=platformVers,
        plugin_vers=pluginVers,
    )
    return _format(result)


def main() -> None:
    mcp.run(transport="stdio")
