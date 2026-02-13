from __future__ import annotations

from typing import Any

import httpx

from nexi_mcp.config import get_config


class NexiError(Exception):
    def __init__(self, message: str, status_code: int = 0, codice_esito: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.codice_esito = codice_esito


class NexiClient:
    def __init__(self) -> None:
        config = get_config()
        self._base_url = config.base_url
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def post(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(
                    self._base_url + endpoint,
                    json=data,
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as exc:
                self._raise_nexi_error(exc)
            except httpx.RequestError as exc:
                raise NexiError(f"Nessuna risposta dal server Nexi: {exc}", status_code=0) from exc
        return {}  # unreachable

    async def get(
        self, endpoint: str, params: dict[str, Any] | None = None, timeout: float = 30.0
    ) -> httpx.Response:
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                resp = await client.get(
                    self._base_url + endpoint,
                    params=params,
                    headers=self._headers,
                )
                resp.raise_for_status()
                return resp
            except httpx.HTTPStatusError as exc:
                self._raise_nexi_error(exc)
            except httpx.RequestError as exc:
                raise NexiError(f"Nessuna risposta dal server Nexi: {exc}", status_code=0) from exc
        raise NexiError("Unexpected error", status_code=0)  # unreachable

    @staticmethod
    def _raise_nexi_error(exc: httpx.HTTPStatusError) -> None:
        status = exc.response.status_code
        messages = {
            400: "Bad Request - parametri non validi",
            401: "Non autorizzato - verifica apiKey e chiaveSegreta",
            404: "Risorsa non trovata",
            503: "Servizio non disponibile",
        }
        detail = messages.get(status, f"Errore HTTP {status}")
        try:
            body = exc.response.json()
            extra = body.get("descrizioneEsito") or body.get("esito") or ""
            if extra:
                detail = f"{detail}: {extra}"
        except Exception:
            pass
        raise NexiError(detail, status_code=status) from exc
