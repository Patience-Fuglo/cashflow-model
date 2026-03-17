from datetime import date

from cashflow_model.instrument import Bond
from cashflow_model.cashflow_engine import (
    project_bond_cashflows,
    project_amortizing_loan,
    print_cashflow_schedule,
    total_cashflows,
    total_interest,
)

# --------------------------------------------------
# TEST 1: BOND CASHFLOWS
# --------------------------------------------------
bond = Bond(
    name="3Y Bond",
    face_value=1000.0,
    coupon_rate=0.06,
    payment_frequency=1,
    issue_date=date(2024, 1, 1),
    maturity_date=date(2027, 1, 1),
)

bond_cashflows = project_bond_cashflows(bond)

print("=== BOND CASHFLOW SCHEDULE ===")
print_cashflow_schedule(bond_cashflows)

print("\nBond total cashflows:", total_cashflows(bond_cashflows))
print("Bond total interest:", total_interest(bond_cashflows))

# --------------------------------------------------
# TEST 2: LOAN CASHFLOWS
# --------------------------------------------------
loan_cashflows = project_amortizing_loan(
    balance=10000.0,
    annual_rate=0.05,
    monthly_payment=188.71,
    num_months=60,
)

print("\n=== LOAN CASHFLOW SCHEDULE ===")
print_cashflow_schedule(loan_cashflows[:10])  # first 5 months only (10 rows)

print("\nLoan total cashflows:", total_cashflows(loan_cashflows))
print("Loan total interest:", total_interest(loan_cashflows))

first_interest = loan_cashflows[0].amount
last_principal = loan_cashflows[-1].amount

print("\nFirst month's interest:", first_interest)
print("Last principal payment:", last_principal)