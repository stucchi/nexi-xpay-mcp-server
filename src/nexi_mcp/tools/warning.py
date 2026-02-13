from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from nexi_mcp.client import NexiClient
from nexi_mcp.config import get_config
from nexi_mcp.mac import generate_timestamp, mac_warning


def _format_date(d: datetime) -> str:
    return d.strftime("%d/%m/%Y %H:%M:%S")


async def warning(
    codice_transazione: str | None = None,
    data_transazione_dal: str | None = None,
    data_transazione_al: str | None = None,
) -> dict[str, Any]:
    """Recupera i warning/anomalie dal Back Office Nexi XPay.

    Args:
        codice_transazione: Identificativo della transazione
        data_transazione_dal: Data di inizio nel formato "gg/mm/aaaa hh:mm:ss"
        data_transazione_al: Data di fine nel formato "gg/mm/aaaa hh:mm:ss"
    """
    config = get_config()
    timestamp = generate_timestamp()
    mac = mac_warning(
        api_key=config.api_key,
        timestamp=timestamp,
        secret_key=config.secret_key,
    )

    now = datetime.now()
    dal = data_transazione_dal or _format_date(now - timedelta(days=7))
    al = data_transazione_al or _format_date(now)

    body: dict[str, Any] = {
        "apiKey": config.api_key,
        "timeStamp": timestamp,
        "mac": mac,
        "dataTransazioneDal": dal,
        "dataTransazioneAl": al,
    }
    if codice_transazione:
        body["codiceTransazione"] = codice_transazione

    client = NexiClient()
    response = await client.post("api/bo/warning", body)

    esito = response.get("esito", "")
    errore = response.get("errore", {})
    no_data = isinstance(errore, dict) and errore.get("codice") == 2

    success = esito == "OK" or no_data

    result: dict[str, Any] = {
        "success": success,
        "esito": esito,
    }
    if no_data:
        result["messaggio"] = "Nessun warning trovato"
    result["warning"] = response.get("warning", [])
    return result
