import json
from datetime import date

from cashflow_model.instrument import Bond
from cashflow_model.cashflow_engine import project_bond_cashflows


FREQUENCY_MAP = {
    "annual": 1,
    "semi-annual": 2,
    "quarterly": 4,
    "monthly": 12,
}

DAY_COUNT_MAP = {
    "Actual/360": "ACT/360",
    "Actual/365": "ACT/365",
    "30/360": "30/360",
    "Actual/Actual": "ACT/ACT",
}


def parse_date(date_str):
    return date.fromisoformat(date_str)


def load_json_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def build_bond_from_schema(data):
    if data["instrument_type"] != "bond":
        raise ValueError("This adapter currently supports bond input only.")

    payment_frequency = FREQUENCY_MAP[data["payment_frequency"]]

    return Bond(
        name=data["instrument_id"],
        face_value=float(data["principal"]),
        coupon_rate=float(data.get("coupon_rate", 0.0)),
        payment_frequency=payment_frequency,
        issue_date=parse_date(data["issue_date"]),
        maturity_date=parse_date(data["maturity_date"]),
    )


def export_cashflows_to_example_format(cashflows):
    exported = []

    for cf in cashflows:
        exported.append(
            {
                "date": str(cf.date),
                "type": cf.cashflow_type.lower(),
                "amount": round(cf.amount, 2),
            }
        )

    return exported


def build_bond_and_project_cashflows(schema_data):
    bond = build_bond_from_schema(schema_data)
    cashflows = project_bond_cashflows(bond)

    return {
        "instrument_type": "bond",
        "principal": bond.face_value,
        "coupon_rate": bond.coupon_rate,
        "payment_frequency": reverse_frequency_map(bond.payment_frequency),
        "cashflows": export_cashflows_to_example_format(cashflows),
    }


def reverse_frequency_map(freq_int):
    reverse_map = {v: k for k, v in FREQUENCY_MAP.items()}
    return reverse_map[freq_int]


def save_json_file(data, filepath):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)