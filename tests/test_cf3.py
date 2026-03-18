"""Unit tests for accrual interest and pricing functions."""
from datetime import date

import pytest

from cashflow_model.instrument import Bond
from cashflow_model.accrual import (
    simple_interest,
    compound_interest,
    find_last_coupon_date,
    find_next_coupon_date,
    accrued_interest,
    clean_price,
)


def test_simple_interest():
    """Test simple interest calculation."""
    principal = 1000.0
    rate = 0.05
    time = 0.25  # 1 quarter
    
    interest = simple_interest(principal, rate, time)
    
    # I = P * r * t = 1000 * 0.05 * 0.25 = 12.5
    assert interest == pytest.approx(12.5)


def test_simple_interest_one_year():
    """Test simple interest for one year."""
    principal = 1000.0
    rate = 0.05
    time = 1.0
    
    interest = simple_interest(principal, rate, time)
    
    assert interest == pytest.approx(50.0)


def test_compound_interest():
    """Test compound interest calculation."""
    principal = 1000.0
    rate = 0.05
    years = 1
    frequency = 2  # semi-annual
    
    interest = compound_interest(principal, rate, years, frequency)
    
    # Interest = P * ((1 + r/m)^(m*t) - 1) = 1000 * (1.025^2 - 1) = 50.625
    assert interest == pytest.approx(50.625)


def test_compound_interest_multiple_years():
    """Test compound interest over multiple years."""
    principal = 1000.0
    rate = 0.05
    years = 2
    frequency = 2  # semi-annual
    
    interest = compound_interest(principal, rate, years, frequency)
    
    # Interest = P * ((1 + r/m)^(m*t) - 1) = 1000 * (1.025^4 - 1)
    expected = principal * ((1.025 ** 4) - 1)
    assert interest == pytest.approx(expected)


def test_find_last_coupon_date():
    """Test finding the last coupon date before settlement."""
    bond = Bond(
        name="Test Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=2,  # semi-annual
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
    )
    
    settlement = date(2024, 4, 1)
    last_coupon = find_last_coupon_date(bond, settlement)
    
    # Last coupon before Apr 1 should be Jan 1 (semi-annual from Jan 1)
    assert last_coupon == date(2024, 1, 1)


def test_find_next_coupon_date():
    """Test finding the next coupon date after settlement."""
    bond = Bond(
        name="Test Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=2,  # semi-annual
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
    )
    
    settlement = date(2024, 4, 1)
    next_coupon = find_next_coupon_date(bond, settlement)
    
    # Next coupon after Apr 1 should be Jul 1 (semi-annual from Jan 1)
    assert next_coupon == date(2024, 7, 1)


def test_accrued_interest():
    """Test accrued interest calculation."""
    bond = Bond(
        name="Test Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=2,  # semi-annual
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
    )
    
    settlement = date(2024, 4, 1)
    accrued = accrued_interest(bond, settlement, convention="30/360")
    
    # Should be positive
    assert accrued > 0
    assert isinstance(accrued, float)


def test_clean_price():
    """Test clean price calculation from dirty price."""
    dirty_price = 1012.50
    accrued = 12.50
    
    clean = clean_price(dirty_price, accrued)
    
    # Clean = Dirty - Accrued
    assert clean == pytest.approx(1000.0)


def test_clean_price_example():
    """Test clean price with realistic values."""
    dirty_price = 1050.0
    accrued = 25.0
    
    clean = clean_price(dirty_price, accrued)
    
    assert clean == pytest.approx(1025.0)


def test_bond_creation():
    """Test bond object creation for accrual tests."""
    bond = Bond(
        name="US Treasury 5Y",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=2,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
    )
    
    assert bond.name == "US Treasury 5Y"
    assert bond.face_value == 1000.0
    assert bond.coupon_rate == 0.05
    assert bond.payment_frequency == 2