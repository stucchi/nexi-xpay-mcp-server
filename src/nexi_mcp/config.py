from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class NexiConfig:
    alias: str
    secret_key: str
    test: bool
    base_url: str

    @property
    def api_key(self) -> str:
        return self.alias

    @staticmethod
    def from_env() -> NexiConfig:
        alias = os.environ.get("NEXI_ALIAS", "")
        secret_key = os.environ.get("NEXI_SECRET_KEY", "")
        test = os.environ.get("NEXI_TEST", "false").lower() in ("true", "1", "yes")

        missing: list[str] = []
        if not alias:
            missing.append("NEXI_ALIAS")
        if not secret_key:
            missing.append("NEXI_SECRET_KEY")

        if missing:
            raise RuntimeError(
                f"Variabili d'ambiente obbligatorie mancanti: {', '.join(missing)}.\n"
                "Configura le seguenti variabili d'ambiente:\n"
                "  NEXI_ALIAS      - Alias del merchant (usato anche come API key)\n"
                "  NEXI_SECRET_KEY - Chiave segreta per calcolo MAC\n"
                "  NEXI_TEST       - Usa ambiente di test (default: false)"
            )

        if not test:
            base_url = "https://ecommerce.nexi.it/ecomm/"
        else:
            base_url = "https://int-ecommerce.nexi.it/ecomm/"

        return NexiConfig(
            alias=alias,
            secret_key=secret_key,
            test=test,
            base_url=base_url,
        )


_config: NexiConfig | None = None


def get_config() -> NexiConfig:
    global _config
    if _config is None:
        _config = NexiConfig.from_env()
    return _config
