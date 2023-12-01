from typing import List, Dict, Any

SUBSCRIBERS = ["1"]

INVOICES = [
    {
        "due": "2023-11-10",
        "amt": 550000,
        "min_amt": 550000,
        "inv_id": ["1"],
        "sub_id": "1",
        "curr": "PYG",
        "addl": ["Factura Nro: 001-001-0000001 - Cliente: Juan Pérez"],
        "next_dues":
            [
                {
                    "amt": 550000,
                    "date": "2023-12-10"
                },
                {
                    "amt": 550000,
                    "date": "2024-01-10"
                },
            ],
        "cm_amt": 50000,
        "cm_curr": "PYG",
        "dsc": "Cuota de Noviembre"
    }
]


def get_subscriber_invoices(
    sub_ids: List[str],
    inv_ids: List[str] | None = None
) -> List[Dict[Any, Any]]:
    sub_invoices = []
    for invoice in INVOICES:
        if invoice["sub_id"] in sub_ids:
            sub_invoices.append(invoice)

    invoices = []

    for invoice in sub_invoices:
        if inv_ids is None or (
            len(invoice["inv_id"]) > 0 and invoice["inv_id"] in inv_ids
        ):
            invoices.append(invoice)

    return invoices


def subscriber_exists(sub_ids: List[str]) -> bool:
    for invoice in INVOICES:
        if invoice["sub_id"] in sub_ids:
            return True

    return False
