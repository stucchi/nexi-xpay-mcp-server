"""Parse natural-language or shorthand date expressions into the
``gg/mm/aaaa - gg/mm/aaaa`` format required by the Nexi XPay API.

If the input is already in the correct format it is returned as-is.
"""

from __future__ import annotations

import re
from datetime import date, timedelta

_DATE_RE = re.compile(r"^\d{2}/\d{2}/\d{4}\s*-\s*\d{2}/\d{2}/\d{4}$")

_fmt = "%d/%m/%Y"


def _range(start: date, end: date) -> str:
    return f"{start.strftime(_fmt)} - {end.strftime(_fmt)}"


def parse_periodo(raw: str) -> str:
    """Convert *raw* into ``gg/mm/aaaa - gg/mm/aaaa``.

    Supported inputs (case-insensitive):
    - Already formatted: ``"01/01/2026 - 31/01/2026"``
    - ``"oggi"`` / ``"today"``
    - ``"ieri"`` / ``"yesterday"``
    - ``"ultima settimana"`` / ``"last week"``
    - ``"ultimo mese"`` / ``"last month"``
    - ``"ultimi N giorni"`` / ``"last N days"``
    - ``"ultimi N mesi"`` / ``"last N months"``
    """
    text = raw.strip()

    if _DATE_RE.match(text):
        return text

    today = date.today()
    lower = text.lower()

    if lower in ("oggi", "today"):
        return _range(today, today)

    if lower in ("ieri", "yesterday"):
        ieri = today - timedelta(days=1)
        return _range(ieri, ieri)

    if lower in ("ultima settimana", "last week"):
        return _range(today - timedelta(days=7), today)

    if lower in ("ultimo mese", "last month"):
        return _range(today - timedelta(days=30), today)

    if lower in ("ultimi 3 mesi", "last 3 months", "ultimo trimestre"):
        return _range(today - timedelta(days=90), today)

    # "ultimi N giorni" / "last N days"
    m = re.match(r"(?:ultimi|last)\s+(\d+)\s+(?:giorni|days)", lower)
    if m:
        days = int(m.group(1))
        return _range(today - timedelta(days=days), today)

    # "ultimi N mesi" / "last N months"
    m = re.match(r"(?:ultimi|last)\s+(\d+)\s+(?:mesi|months)", lower)
    if m:
        months = int(m.group(1))
        days = min(months * 30, 90)  # Nexi max 90 giorni
        return _range(today - timedelta(days=days), today)

    # Fallback: return as-is and let Nexi decide
    return text
