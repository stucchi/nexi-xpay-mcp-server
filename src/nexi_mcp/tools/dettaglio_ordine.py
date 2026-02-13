from __future__ import annotations

from typing import Any

from nexi_mcp.client import NexiClient
from nexi_mcp.config import get_config
from nexi_mcp.mac import generate_timestamp, mac_situazione_ordine


async def dettaglio_ordine(codice_transazione: str) -> dict[str, Any]:
    """Recupera i dettagli di un ordine specifico dal Back Office Nexi XPay.

    Args:
        codice_transazione: Identificativo della transazione merchant
    """
    config = get_config()
    timestamp = generate_timestamp()
    mac = mac_situazione_ordine(
        api_key=config.api_key,
        codice_transazione=codice_transazione,
        timestamp=timestamp,
        secret_key=config.secret_key,
    )

    body = {
        "apiKey": config.api_key,
        "codiceTransazione": codice_transazione,
        "timeStamp": timestamp,
        "mac": mac,
    }

    client = NexiClient()
    response = await client.post("api/bo/situazioneOrdine", body)

    success = response.get("esito") == "OK"
    result: dict[str, Any] = {"success": success}
    result.update(response)
    return result
