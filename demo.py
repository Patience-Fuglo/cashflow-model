#!/usr/bin/env python3
"""
Demo script showing the Cashflow Model engine in action.

Run with: python demo.py
"""

from datetime import date

from cashflow_model import (
    Bond,
    project_bond_cashflows,
    calculate_npv,
    calculate_ytm,
    calculate_duration,
    calculate_modified_duration,
    STANDARD_SCENARIOS,
    run_all_scenarios,
    estimate_pnl_from_duration,
    project_amortizing_loan,
    total_interest,
)


def print_header(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print('=' * 60)


def demo_bond_pricing():
    """Demonstrate bond cashflow projection and pricing."""
    print_header("Bond Pricing & Cashflow Projection")

    # Create a 5-year bond with 5% annual coupon
    bond = Bond(
        name="5Y Treasury",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,  # Annual
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
    )

    print(f"\nBond: {bond.name}")
    print(f"Face Value: ${bond.face_value:,.2f}")
    print(f"Coupon Rate: {bond.coupon_rate:.2%}")
    print(f"Maturity: {bond.maturity_date}")

    # Project cashflows
    cashflows = project_bond_cashflows(bond)

    print("\nCashflow Schedule:")
    print(f"{'Date':<15} {'Type':<12} {'Amount':>12}")
    print("-" * 40)

    for cf in cashflows:
        print(f"{str(cf.date):<15} {cf.cashflow_type:<12} ${cf.amount:>10,.2f}")

    # Calculate present value at different discount rates
    as_of_date = date(2024, 1, 1)

    print("\nPresent Value at Different Discount Rates:")
    print(f"{'Rate':<10} {'NPV':>15} {'vs Par':>12}")
    print("-" * 40)

    for rate in [0.03, 0.04, 0.05, 0.06, 0.07]:
        npv = calculate_npv(cashflows, rate, as_of_date, "ACT/365")
        vs_par = "Premium" if npv > 1000 else "Discount" if npv < 1000 else "Par"
        print(f"{rate:.2%}      ${npv:>12,.2f}    {vs_par}")


def demo_ytm_and_duration():
    """Demonstrate YTM calculation and duration."""
    print_header("Yield-to-Maturity & Duration")

    bond = Bond(
        name="3Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2027, 1, 1),
    )

    as_of_date = date(2024, 1, 1)
    cashflows = project_bond_cashflows(bond)

    # Calculate NPV at 4% discount rate
    discount_rate = 0.04
    npv = calculate_npv(cashflows, discount_rate, as_of_date, "ACT/365")

    print(f"\nBond: {bond.name}")
    print(f"Discount Rate: {discount_rate:.2%}")
    print(f"NPV (Dirty Price): ${npv:,.2f}")

    # Calculate YTM given market price
    ytm = calculate_ytm(bond, npv, "ACT/365")
    print(f"YTM (should match discount rate): {ytm:.4%}")

    # Calculate duration
    duration = calculate_duration(cashflows, discount_rate, as_of_date, "ACT/365")
    mod_duration = calculate_modified_duration(duration, discount_rate, bond.payment_frequency)

    print(f"\nMacaulay Duration: {duration:.4f} years")
    print(f"Modified Duration: {mod_duration:.4f}")


def demo_scenario_analysis():
    """Demonstrate interest rate scenario analysis."""
    print_header("Interest Rate Scenario Analysis")

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

    # Run all standard scenarios
    base_npv, results = run_all_scenarios(
        bond=bond,
        base_rate=base_rate,
        scenarios=STANDARD_SCENARIOS,
        as_of_date=as_of_date,
        convention="ACT/365",
    )

    print(f"\nBase Rate: {base_rate:.2%}")
    print(f"Base NPV: ${base_npv:,.2f}")

    print(f"\n{'Scenario':<15} {'NPV':>12} {'$ Change':>12} {'% Change':>10}")
    print("-" * 52)

    for name, npv, dollar_change, pct_change in results:
        print(f"{name:<15} ${npv:>10,.2f} {dollar_change:>+12,.2f} {pct_change:>+9.2f}%")

    # Duration-based P&L estimate
    cashflows = project_bond_cashflows(bond)
    duration = calculate_duration(cashflows, base_rate, as_of_date, "ACT/365")
    mod_duration = calculate_modified_duration(duration, base_rate, bond.payment_frequency)

    rate_shock = 0.01  # +100 bps
    estimated_pnl = estimate_pnl_from_duration(mod_duration, rate_shock, base_npv)

    # Find actual P&L from scenario results
    actual_pnl = next(dc for name, _, dc, _ in results if name == "Rates +1%")

    print(f"\nDuration-Based P&L Estimate (for +1% shock):")
    print(f"  Modified Duration: {mod_duration:.4f}")
    print(f"  Estimated P&L: ${estimated_pnl:,.2f}")
    print(f"  Actual P&L:    ${actual_pnl:,.2f}")


def demo_loan_amortization():
    """Demonstrate loan amortization cashflows."""
    print_header("Loan Amortization")

    balance = 10000.0
    annual_rate = 0.05
    monthly_payment = 200.0
    num_months = 60

    cashflows = project_amortizing_loan(balance, annual_rate, monthly_payment, num_months)

    print(f"\nLoan Amount: ${balance:,.2f}")
    print(f"Annual Rate: {annual_rate:.2%}")
    print(f"Monthly Payment: ${monthly_payment:,.2f}")
    print(f"Term: {num_months} months")

    # Show first 3 and last 3 months
    print(f"\n{'Month':<10} {'Interest':>12} {'Principal':>12}")
    print("-" * 36)

    interest_cfs = [cf for cf in cashflows if cf.cashflow_type == "INTEREST"]
    principal_cfs = [cf for cf in cashflows if cf.cashflow_type == "PRINCIPAL"]

    for i in range(min(3, len(interest_cfs))):
        print(f"{interest_cfs[i].date:<10} ${interest_cfs[i].amount:>10,.2f} ${principal_cfs[i].amount:>10,.2f}")

    if len(interest_cfs) > 6:
        print("...")

    for i in range(max(0, len(interest_cfs) - 3), len(interest_cfs)):
        if i >= 3:
            print(f"{interest_cfs[i].date:<10} ${interest_cfs[i].amount:>10,.2f} ${principal_cfs[i].amount:>10,.2f}")

    total_int = total_interest(cashflows)
    print(f"\nTotal Interest Paid: ${total_int:,.2f}")


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print(" CASHFLOW MODEL — FIXED INCOME ANALYTICS ENGINE")
    print("=" * 60)

    demo_bond_pricing()
    demo_ytm_and_duration()
    demo_scenario_analysis()
    demo_loan_amortization()

    print("\n" + "=" * 60)
    print(" Demo complete.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
