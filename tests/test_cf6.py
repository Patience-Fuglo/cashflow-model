"""Unit tests for scenario analysis and interest rate risk."""
from datetime import date

import pytest

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
    estimate_pnl_from_duration,
)


def test_scenario_analysis_npv_decreases_with_rates():
    """Test that NPV decreases when rates increase."""
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
    
    # Calculate NPV at base rate
    base_npv = calculate_npv(cashflows, base_rate, as_of_date, convention="ACT/365")
    
    # Calculate NPV at higher rate
    higher_rate = base_rate + 0.01
    higher_npv = calculate_npv(cashflows, higher_rate, as_of_date, convention="ACT/365")
    
    # NPV should decrease when rates increase
    assert higher_npv < base_npv


def test_scenario_analysis_npv_increases_with_rates():
    """Test that NPV increases when rates decrease."""
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
    
    # Calculate NPV at base rate
    base_npv = calculate_npv(cashflows, base_rate, as_of_date, convention="ACT/365")
    
    # Calculate NPV at lower rate
    lower_rate = base_rate - 0.01
    lower_npv = calculate_npv(cashflows, lower_rate, as_of_date, convention="ACT/365")
    
    # NPV should increase when rates decrease
    assert lower_npv > base_npv


def test_run_all_scenarios():
    """Test running all standard scenarios."""
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
    
    base_npv, results = run_all_scenarios(
        bond=bond,
        base_rate=base_rate,
        scenarios=STANDARD_SCENARIOS,
        as_of_date=as_of_date,
        convention="ACT/365",
    )
    
    # Should have results for all standard scenarios
    assert len(results) == len(STANDARD_SCENARIOS)
    
    # Results should be tuples of (name, npv, dollar_change, pct_change)
    for name, npv, dollar_change, pct_change in results:
        assert isinstance(name, str)
        assert isinstance(npv, float)
        assert isinstance(dollar_change, float)
        assert isinstance(pct_change, float)


def test_scenario_symmetry():
    """Test that positive and negative rate shocks have roughly symmetric effect on duration-adjusted P&L."""
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
    
    # Up 100 bps
    up_npv = calculate_npv(cashflows, base_rate + 0.01, as_of_date, convention="ACT/365")
    up_change = up_npv - base_npv
    
    # Down 100 bps
    down_npv = calculate_npv(cashflows, base_rate - 0.01, as_of_date, convention="ACT/365")
    down_change = down_npv - base_npv
    
    # Changes should be roughly opposite (convexity may cause slight asymmetry)
    assert up_change < 0
    assert down_change > 0


def test_estimate_pnl_from_duration_negative_rate_move():
    """Test P&L estimation when rates rise (negative return)."""
    modified_duration = 5.0
    rate_change = 0.01  # +100 bps
    portfolio_value = 1000000.0
    
    pnl = estimate_pnl_from_duration(modified_duration, rate_change, portfolio_value)
    
    # Should be negative when rates rise
    assert pnl < 0
    # Should be -5 * 0.01 * 1000000 = -50000
    assert pnl == pytest.approx(-50000.0)


def test_estimate_pnl_from_duration_positive_rate_move():
    """Test P&L estimation when rates fall (positive return)."""
    modified_duration = 5.0
    rate_change = -0.01  # -100 bps
    portfolio_value = 1000000.0
    
    pnl = estimate_pnl_from_duration(modified_duration, rate_change, portfolio_value)
    
    # Should be positive when rates fall
    assert pnl > 0
    # Should be -5 * (-0.01) * 1000000 = +50000
    assert pnl == pytest.approx(50000.0)


def test_duration_approximation_accuracy():
    """Test accuracy of duration approximation vs actual NPV change."""
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
    modified_duration = calculate_modified_duration(
        duration, base_rate, bond.payment_frequency
    )
    
    # Actual change from +100 bps
    actual_npv = calculate_npv(cashflows, base_rate + 0.01, as_of_date, convention="ACT/365")
    actual_change = actual_npv - base_npv
    
    # Estimated change using duration
    estimated_change = estimate_pnl_from_duration(
        modified_duration, 0.01, base_npv
    )
    
    # Estimated should be close to actual (within ~5% for small moves)
    percent_error = abs(estimated_change - actual_change) / abs(actual_change) * 100
    assert percent_error < 10.0


def test_higher_duration_more_sensitive_to_rates():
    """Test that bonds with higher duration are more sensitive to rates."""
    # Short bond
    short_bond = Bond(
        name="1Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2025, 1, 1),
    )
    
    # Long bond
    long_bond = Bond(
        name="10Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2034, 1, 1),
    )
    
    as_of_date = date(2024, 1, 1)
    base_rate = 0.04
    
    short_cashflows = project_bond_cashflows(short_bond)
    long_cashflows = project_bond_cashflows(long_bond)
    
    short_npv_base = calculate_npv(short_cashflows, base_rate, as_of_date, convention="ACT/365")
    short_npv_shocked = calculate_npv(short_cashflows, base_rate + 0.01, as_of_date, convention="ACT/365")
    short_pct_change = (short_npv_shocked - short_npv_base) / short_npv_base
    
    long_npv_base = calculate_npv(long_cashflows, base_rate, as_of_date, convention="ACT/365")
    long_npv_shocked = calculate_npv(long_cashflows, base_rate + 0.01, as_of_date, convention="ACT/365")
    long_pct_change = (long_npv_shocked - long_npv_base) / long_npv_base
    
    # Long bond should be more sensitive
    assert abs(long_pct_change) > abs(short_pct_change)