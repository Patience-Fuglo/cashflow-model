from datetime import date

from cashflow_model.instrument import Bond
from cashflow_model.cashflow_engine import project_bond_cashflows
from cashflow_model.present_value import (
    discount,
    calculate_npv,
    calculate_ytm,
    calculate_duration,
    calculate_modified_duration,
)

bond = Bond(
    name="3Y Bond",
    face_value=1000.0,
    coupon_rate=0.05,
    payment_frequency=1,
    issue_date=date(2024, 1, 1),
    maturity_date=date(2027, 1, 1),
)

cashflows = project_bond_cashflows(bond)

print("=== TEST DISCOUNT ===")
print("PV of 1000 in 1 year at 4%:", discount(1000, 0.04, 1))

print("\n=== TEST NPV ===")
npv = calculate_npv(
    cashflows=cashflows,
    discount_rate=0.04,
    as_of_date=date(2024, 1, 1),
    convention="ACT/365"
)
print("NPV at 4%:", npv)

print("\n=== TEST YTM ===")
ytm = calculate_ytm(
    bond=bond,
    market_price=npv,
    convention="ACT/365"
)
print("YTM:", ytm)

print("\n=== TEST DURATION ===")
duration = calculate_duration(
    cashflows=cashflows,
    ytm=ytm,
    as_of_date=date(2024, 1, 1),
    convention="ACT/365"
)
print("Macaulay Duration:", duration)

modified_duration = calculate_modified_duration(
    macaulay_duration=duration,
    ytm=ytm,
    frequency=bond.payment_frequency
)
print("Modified Duration:", modified_duration)