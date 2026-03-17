from cashflow_model.io_adapter import (
    load_json_file,
    build_bond_and_project_cashflows,
)

# -----------------------------------
# Example schema-style input
# -----------------------------------
instrument_data = {
    "instrument_id": "US_Treasury_5Y",
    "instrument_type": "bond",
    "principal": 1000,
    "currency": "USD",
    "issue_date": "2024-01-01",
    "maturity_date": "2029-01-01",
    "coupon_rate": 0.05,
    "payment_frequency": "semi-annual",
    "day_count_convention": "30/360"
}

result = build_bond_and_project_cashflows(instrument_data)

print("=== INTEGRATED OUTPUT ===")
print(result)

print("\n=== CASHFLOWS ONLY ===")
for cf in result["cashflows"]:
    print(cf)