from datetime import date

from cashflow_model.instrument import Bond
from cashflow_model.cashflow_engine import project_bond_cashflows
from cashflow_model.present_value import (
    calculate_npv,
    calculate_duration,
    calculate_modified_duration,
)
from cashflow_model.scenario import (
    STANDARD_SCENARIOS,
    run_all_scenarios,
    print_scenario_report,
    estimate_pnl_from_duration,
)

bond = Bond(
    name="5Y Bond",
    face_value=1000.0,
    coupon_rate=0.05,
    payment_frequency=1,
    issue_date=date(2024, 1, 1),
    maturity_date=date(2029, 1, 1),
)

as_of_date = date(2024, 1, 1)
base_rate = 0.04

cashflows = project_bond_cashflows(bond)

base_npv = calculate_npv(cashflows, base_rate, as_of_date, convention="ACT/365")
duration = calculate_duration(cashflows, base_rate, as_of_date, convention="ACT/365")
modified_duration = calculate_modified_duration(duration, base_rate, bond.payment_frequency)

print("=== BASE METRICS ===")
print("Base NPV:", base_npv)
print("Macaulay Duration:", duration)
print("Modified Duration:", modified_duration)

print("\n=== SCENARIO REPORT ===")
base_npv, scenario_results = run_all_scenarios(
    bond=bond,
    base_rate=base_rate,
    scenarios=STANDARD_SCENARIOS,
    as_of_date=as_of_date,
    convention="ACT/365",
)

print_scenario_report(base_npv, scenario_results)

print("\n=== DURATION APPROXIMATION ===")
rate_change = 0.01
estimated_pnl = estimate_pnl_from_duration(
    modified_duration=modified_duration,
    rate_change=rate_change,
    portfolio_value=base_npv,
)

print("Estimated P&L for +1% rate move:", estimated_pnl)

for name, new_npv, dollar_change, pct_change in scenario_results:
    if name == "Rates +1%":
        print("Actual P&L for +1% rate move:", dollar_change)
        break