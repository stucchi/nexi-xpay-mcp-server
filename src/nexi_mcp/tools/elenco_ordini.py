from __future__ import annotations

from typing import Any

from nexi_mcp.client import NexiClient
from nexi_mcp.config import get_config
from nexi_mcp.mac import generate_timestamp, mac_report_ordini


async def elenco_ordini(
    periodo: str,
    canale: str = "All",
    codice_transazione: str = "",
    stato: list[str] | None = None,
) -> dict[str, Any]:
    """Recupera l'elenco degli ordini dal Back Office Nexi XPay.

    Args:
        periodo: Intervallo date nel formato "gg/mm/aaaa - gg/mm/aaaa" (max 90 giorni)
        canale: Canale di pagamento (All, MyBank, CartaCredito, PayPal, sofort)
        codice_transazione: Filtro per transazione specifica
        stato: Array di stati da filtrare
    """
    config = get_config()
    timestamp = generate_timestamp()
    mac = mac_report_ordini(
        api_key=config.api_key,
        codice_transazione=codice_transazione,
        periodo=periodo,
        canale=canale,
        timestamp=timestamp,
        secret_key=config.secret_key,
    )

    body: dict[str, Any] = {
        "apiKey": config.api_key,
        "codiceTransazione": codice_transazione,
        "periodo": periodo,
        "canale": canale,
        "timeStamp": timestamp,
        "mac": mac,
    }
    if stato:
        body["stato"] = stato

    client = NexiClient()
    response = await client.post("api/bo/reportOrdini", body)

    return {
        "success": response.get("esito") == "OK",
        "esito": response.get("esito"),
        "descrizioneEsito": response.get("descrizioneEsito"),
        "elapsedTime": response.get("elapsedTime"),
        "orderId": response.get("orderId"),
        "ordini": response.get("report", []),
    }
