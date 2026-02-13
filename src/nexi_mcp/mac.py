from __future__ import annotations

import hashlib
import time


def calculate_mac(params: str, secret_key: str) -> str:
    raw = params + secret_key
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def generate_timestamp() -> int:
    return int(time.time() * 1000)


def mac_report_ordini(
    api_key: str,
    codice_transazione: str,
    periodo: str,
    canale: str,
    timestamp: int,
    secret_key: str,
) -> str:
    params = (
        f"apiKey={api_key}"
        f"codiceTransazione={codice_transazione}"
        f"periodo={periodo}"
        f"canale={canale}"
        f"timeStamp={timestamp}"
    )
    return calculate_mac(params, secret_key)


def mac_situazione_ordine(
    api_key: str,
    codice_transazione: str,
    timestamp: int,
    secret_key: str,
) -> str:
    params = (
        f"apiKey={api_key}"
        f"codiceTransazione={codice_transazione}"
        f"timeStamp={timestamp}"
    )
    return calculate_mac(params, secret_key)


def mac_warning(
    api_key: str,
    timestamp: int,
    secret_key: str,
) -> str:
    params = f"apiKey={api_key}timeStamp={timestamp}"
    return calculate_mac(params, secret_key)


def mac_profile_info(
    api_key: str,
    timestamp: int,
    secret_key: str,
) -> str:
    params = f"apiKey={api_key}timeStamp={timestamp}"
    return calculate_mac(params, secret_key)
