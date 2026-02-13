from __future__ import annotations

from typing import Any

from nexi_mcp.client import NexiClient
from nexi_mcp.config import get_config
from nexi_mcp.mac import generate_timestamp, mac_profile_info


async def metodi_pagamento(
    platform: str = "custom",
    platform_vers: str = "0",
    plugin_vers: str = "0",
) -> dict[str, Any]:
    """Recupera i metodi di pagamento attivi per un merchant dal Back Office Nexi XPay.

    Args:
        platform: Nome del CMS (default: custom)
        platform_vers: Versione del CMS (default: 0)
        plugin_vers: Versione del plugin (default: 0)
    """
    config = get_config()
    timestamp = generate_timestamp()
    mac = mac_profile_info(
        api_key=config.api_key,
        timestamp=timestamp,
        secret_key=config.secret_key,
    )

    body = {
        "apiKey": config.api_key,
        "timeStamp": timestamp,
        "mac": mac,
        "platform": platform,
        "platformVers": platform_vers,
        "pluginVers": plugin_vers,
    }

    client = NexiClient()
    response = await client.post("api/profileInfo", body)

    methods = response.get("availableMethods", [])
    metodi = [
        {
            "codice": m.get("code"),
            "descrizione": m.get("description"),
            "immagine": m.get("image"),
            "tipo": m.get("type"),
            "ricorrente": "Sì" if m.get("recurring") == "Y" else "No",
        }
        for m in methods
    ]

    return {
        "success": response.get("esito") == "OK",
        "esito": response.get("esito"),
        "platform": platform,
        "metodiPagamento": metodi,
    }
