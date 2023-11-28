from datetime import datetime
from typing import Dict, Any, List

from processors.dates import convert_dates_to_iso
from processors.none_values import remove_none


def postprocess_record_with_related_fields(
    parents: List[str], children: List[str], record: Dict[str, Any]
) -> Dict[str, Any]:
    record = postprocess_record(record)
    new_record = {}
    for key, value in record.items():
        key_parts = key.split(".")

        if len(key_parts) == 2:
            parent_key = key_parts[0]
            child_key = key_parts[1]

            if parent_key in parents:
                new_record[child_key] = value
            elif parent_key in children:
                if parent_key not in new_record:
                    new_record[parent_key] = {}

                new_record[parent_key][child_key] = value

    return new_record


def postprocess_record(record: Dict[str, Any]) -> Dict[str, Any]:
    record = convert_dates_to_iso(record)

    return record


def preprocess_record(
    record: Dict[str, Any],
    datetime_fields: List[str] | None = None
) -> Dict[str, Any]:
    record = remove_none(record)
    if "created_at" in record:
        record["created_at"] = datetime.fromisoformat(record["created_at"])
    record["updated_at"] = datetime.utcnow()

    if datetime_fields is not None:
        for key, val in record.items():
            if key in datetime_fields:
                record[key] = datetime.fromisoformat(val.replace('Z', '+00:00'))

    return record
