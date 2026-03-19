"""Unit tests for cashflow projection engine."""
from datetime import date
from io import StringIO
from contextlib import redirect_stdout

from tests.test_utils import approx, run_module_tests

from cashflow_model.instrument import Bond
from cashflow_model.cashflow_engine import (
    project_bond_cashflows,
    project_amortizing_loan,
    print_cashflow_schedule,
    total_cashflows,
    total_interest,
)


def test_project_bond_cashflows():
    """Test bond cashflow projection."""
    bond = Bond(
        name="3Y Bond",
        face_value=1000.0,
        coupon_rate=0.06,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    
    # 3 years, annual payment = 3 coupons + 1 principal = 4 cashflows
    assert len(cashflows) == 4
    
    # Check first 3 are coupons
    for i in range(3):
        assert cashflows[i].amount == approx(60.0)  # 0.06 * 1000
        assert cashflows[i].cashflow_type == "COUPON"
    
    # Last one is principal
    assert cashflows[3].amount == approx(1000.0)
    assert cashflows[3].cashflow_type == "PRINCIPAL"


def test_project_bond_cashflows_semi_annual():
    """Test bond cashflow projection with semi-annual payments."""
    bond = Bond(
        name="2Y Bond",
        face_value=1000.0,
        coupon_rate=0.04,
        payment_frequency=2,  # semi-annual
        issue_date=date(2024, 1, 1),
        maturity_date=date(2026, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    
    # 2 years, semi-annual = 4 coupons + 1 principal = 5 cashflows
    assert len(cashflows) == 5
    
    # Semi-annual coupon = 0.04 * 1000 / 2 = 20
    for i in range(4):
        assert cashflows[i].amount == approx(20.0)
        assert cashflows[i].cashflow_type == "COUPON"
    
    # Final payment = principal only
    assert cashflows[4].amount == approx(1000.0)
    assert cashflows[4].cashflow_type == "PRINCIPAL"


def test_project_amortizing_loan():
    """Test amortizing loan cashflow projection."""
    loan_cashflows = project_amortizing_loan(
        balance=10000.0,
        annual_rate=0.05,
        monthly_payment=188.71,
        num_months=60,
    )
    
    # Each month generates 2 cashflows (interest and principal)
    assert len(loan_cashflows) == 120


def test_total_cashflows():
    """Test total cashflows calculation."""
    bond = Bond(
        name="1Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2025, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    total = total_cashflows(cashflows)
    
    # 1 coupon (50) + principal (1000) = 1050
    assert total == approx(1050.0)


def test_total_interest():
    """Test total interest calculation."""
    bond = Bond(
        name="1Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2025, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    interest = total_interest(cashflows)
    
    # Total interest paid = 50
    assert interest == approx(50.0)


def test_loan_total_cashflows():
    """Test total cashflows for amortizing loan."""
    loan_cashflows = project_amortizing_loan(
        balance=10000.0,
        annual_rate=0.05,
        monthly_payment=188.71,
        num_months=60,
    )
    
    total = total_cashflows(loan_cashflows)
    
    # This includes both interest and principal components
    assert total > 10000.0


def test_loan_total_interest():
    """Test total interest for amortizing loan."""
    loan_cashflows = project_amortizing_loan(
        balance=10000.0,
        annual_rate=0.05,
        monthly_payment=188.71,
        num_months=60,
    )
    
    interest = total_interest(loan_cashflows)
    
    # Total interest should be positive
    assert interest > 0


def test_bond_cashflow_dates():
    """Test that cashflow dates are correct."""
    bond = Bond(
        name="2Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2026, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    
    # Check dates
    assert cashflows[0].date == date(2025, 1, 1)
    assert cashflows[1].date == date(2026, 1, 1)


def test_print_cashflow_schedule():
    """Test printing cashflow schedule."""
    bond = Bond(
        name="1Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2025, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    
    # Should not raise an error
    output = StringIO()
    with redirect_stdout(output):
        print_cashflow_schedule(cashflows)

    captured = output.getvalue()
    assert "coupon" in captured.lower() or "principal" in captured.lower()


if __name__ == "__main__":
    raise SystemExit(run_module_tests(globals()))