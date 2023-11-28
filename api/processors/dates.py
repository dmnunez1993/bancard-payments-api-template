from datetime import datetime

from typing import Dict, Any


def convert_dates_to_iso(value: Dict[str, Any]) -> Dict[str, Any]:
    for key, val in value.items():
        if isinstance(val, datetime):
            value[key] = val.isoformat()

    return value
