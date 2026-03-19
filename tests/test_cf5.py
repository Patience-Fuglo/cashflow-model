"""Unit tests for present value calculations."""
from datetime import date

from tests.test_utils import approx, run_module_tests

from cashflow_model.instrument import Bond
from cashflow_model.cashflow_engine import project_bond_cashflows
from cashflow_model.present_value import (
    discount,
    calculate_npv,
    calculate_ytm,
    calculate_duration,
    calculate_modified_duration,
)


def test_discount():
    """Test discount factor calculation."""
    future_value = 1000.0
    rate = 0.04
    time = 1.0
    
    pv = discount(future_value, rate, time)
    
    # PV = FV / (1 + r)^t = 1000 / 1.04 = 961.538...
    assert pv == approx(1000.0 / 1.04)


def test_discount_multiple_years():
    """Test discount over multiple years."""
    future_value = 1000.0
    rate = 0.05
    time = 2.0
    
    pv = discount(future_value, rate, time)
    
    # PV = 1000 / 1.05^2
    assert pv == approx(1000.0 / (1.05 ** 2))


def test_discount_zero_time():
    """Test discount with zero time."""
    future_value = 1000.0
    rate = 0.05
    time = 0.0
    
    pv = discount(future_value, rate, time)
    
    # PV = FV / (1 + r)^0 = FV / 1 = FV
    assert pv == approx(future_value)


def test_calculate_npv():
    """Test NPV calculation for a bond."""
    bond = Bond(
        name="3Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    
    npv = calculate_npv(
        cashflows=cashflows,
        discount_rate=0.04,
        as_of_date=date(2024, 1, 1),
        convention="ACT/365"
    )
    
    # Should be positive since discount rate < coupon rate
    assert npv > 0
    assert isinstance(npv, float)


def test_calculate_npv_par_value():
    """Test NPV equals par when discount rate equals coupon rate."""
    bond = Bond(
        name="3Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    
    npv = calculate_npv(
        cashflows=cashflows,
        discount_rate=0.05,  # Same as coupon rate
        as_of_date=date(2024, 1, 1),
        convention="ACT/365"
    )
    
    # Should be approximately par value
    assert npv == approx(1000.0, rel=0.01)


def test_calculate_ytm():
    """Test YTM calculation."""
    bond = Bond(
        name="3Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    
    market_price = 950.0
    ytm = calculate_ytm(
        bond=bond,
        market_price=market_price,
        convention="ACT/365"
    )
    
    # YTM should be > coupon rate when bond trades below par
    assert ytm > bond.coupon_rate
    assert isinstance(ytm, float)


def test_calculate_duration():
    """Test Macaulay duration calculation."""
    bond = Bond(
        name="3Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    
    duration = calculate_duration(
        cashflows=cashflows,
        ytm=0.05,
        as_of_date=date(2024, 1, 1),
        convention="ACT/365"
    )
    
    # Duration should be between 0 and maturity
    assert 0 < duration < 3.0
    assert isinstance(duration, float)


def test_calculate_modified_duration():
    """Test modified duration calculation."""
    macaulay_duration = 2.5
    ytm = 0.05
    frequency = 1  # annual
    
    modified_duration = calculate_modified_duration(
        macaulay_duration=macaulay_duration,
        ytm=ytm,
        frequency=frequency
    )
    
    # Modified = Macaulay / (1 + ytm/frequency)
    expected = macaulay_duration / (1 + ytm / frequency)
    assert modified_duration == approx(expected)


def test_modified_duration_semi_annual():
    """Test modified duration with semi-annual payments."""
    macaulay_duration = 2.5
    ytm = 0.05
    frequency = 2  # semi-annual
    
    modified_duration = calculate_modified_duration(
        macaulay_duration=macaulay_duration,
        ytm=ytm,
        frequency=frequency
    )
    
    # Modified = 2.5 / (1 + 0.05/2) = 2.5 / 1.025
    expected = macaulay_duration / (1 + ytm / frequency)
    assert modified_duration == approx(expected)


def test_duration_higher_yield_lower_duration():
    """Test that higher yield results in lower modified duration."""
    bond = Bond(
        name="3Y Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    
    cashflows = project_bond_cashflows(bond)
    
    duration_low_yield = calculate_duration(
        cashflows=cashflows,
        ytm=0.03,
        as_of_date=date(2024, 1, 1),
        convention="ACT/365"
    )
    
    duration_high_yield = calculate_duration(
        cashflows=cashflows,
        ytm=0.07,
        as_of_date=date(2024, 1, 1),
        convention="ACT/365"
    )
    
    # Higher yield should result in lower duration
    assert duration_low_yield > duration_high_yield


if __name__ == "__main__":
    raise SystemExit(run_module_tests(globals()))