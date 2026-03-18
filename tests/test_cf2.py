"""Unit tests for day count conventions."""
from datetime import date

import pytest

from cashflow_model.day_count import (
    actual_360,
    actual_365,
    thirty_360,
    actual_actual,
    get_year_fraction,
)


def test_actual_360_jan_to_jul():
    """Test ACT/360 for Jan 1 to Jul 1."""
    start = date(2024, 1, 1)
    end = date(2024, 7, 1)
    
    year_fraction = actual_360(start, end)
    
    # Actual count: 182 days / 360 = 0.5055...
    assert year_fraction == pytest.approx(182 / 360, rel=1e-4)


def test_actual_365_jan_to_jul():
    """Test ACT/365 for Jan 1 to Jul 1."""
    start = date(2024, 1, 1)
    end = date(2024, 7, 1)
    
    year_fraction = actual_365(start, end)
    
    # Actual count: 182 days / 365 = 0.4986...
    assert year_fraction == pytest.approx(182 / 365, rel=1e-4)


def test_thirty_360_jan_to_jul():
    """Test 30/360 for Jan 1 to Jul 1."""
    start = date(2024, 1, 1)
    end = date(2024, 7, 1)
    
    year_fraction = thirty_360(start, end)
    
    # (6 * 30) / 360 = 180 / 360 = 0.5
    assert year_fraction == pytest.approx(0.5, rel=1e-4)


def test_actual_actual_jan_to_jul():
    """Test ACT/ACT for Jan 1 to Jul 1."""
    start = date(2024, 1, 1)
    end = date(2024, 7, 1)
    
    year_fraction = actual_actual(start, end)
    
    # Actual count: 182 days / 366 (leap year 2024) = 0.4972...
    assert year_fraction == pytest.approx(182 / 366, rel=1e-4)


def test_leap_year_edge_case_actual_360():
    """Test ACT/360 for Feb 28 to Mar 1 in leap year."""
    start = date(2024, 2, 28)
    end = date(2024, 3, 1)
    
    year_fraction = actual_360(start, end)
    
    # 2 days / 360 = 0.00555...
    assert year_fraction == pytest.approx(2 / 360, rel=1e-4)


def test_leap_year_edge_case_actual_365():
    """Test ACT/365 for Feb 28 to Mar 1 in leap year."""
    start = date(2024, 2, 28)
    end = date(2024, 3, 1)
    
    year_fraction = actual_365(start, end)
    
    # 2 days / 365 = 0.00547...
    assert year_fraction == pytest.approx(2 / 365, rel=1e-4)


def test_leap_year_edge_case_thirty_360():
    """Test 30/360 for Feb 28 to Mar 1 in leap year."""
    start = date(2024, 2, 28)
    end = date(2024, 3, 1)
    
    year_fraction = thirty_360(start, end)
    
    # 3 days / 360 = 0.00833... (30/360 uses actual day count here)
    assert year_fraction == pytest.approx(3 / 360, rel=1e-4)


def test_leap_year_edge_case_actual_actual():
    """Test ACT/ACT for Feb 28 to Mar 1 in leap year."""
    start = date(2024, 2, 28)
    end = date(2024, 3, 1)
    
    year_fraction = actual_actual(start, end)
    
    # 2 days / 366 (leap year) = 0.00546...
    assert year_fraction == pytest.approx(2 / 366, rel=1e-4)


def test_get_year_fraction_with_convention():
    """Test get_year_fraction helper function."""
    start = date(2024, 1, 1)
    end = date(2024, 7, 1)
    
    result_360 = get_year_fraction(start, end, "ACT/360")
    result_365 = get_year_fraction(start, end, "ACT/365")
    result_30_360 = get_year_fraction(start, end, "30/360")
    
    assert result_360 == pytest.approx(182 / 360, rel=1e-4)
    assert result_365 == pytest.approx(182 / 365, rel=1e-4)
    assert result_30_360 == pytest.approx(0.5, rel=1e-4)


def test_same_start_and_end_date():
    """Test day count when start and end dates are the same."""
    start = date(2024, 1, 1)
    end = date(2024, 1, 1)
    
    assert actual_360(start, end) == 0.0
    assert actual_365(start, end) == 0.0
    assert thirty_360(start, end) == 0.0
    assert actual_actual(start, end) == 0.0


def test_one_year_apart():
    """Test day count for exactly one year apart."""
    start = date(2024, 1, 1)
    end = date(2025, 1, 1)
    
    result_360 = actual_360(start, end)
    result_365 = actual_365(start, end)
    
    # 366 days (leap year) / 360 and / 365
    assert result_360 == pytest.approx(366 / 360, rel=1e-4)
    assert result_365 == pytest.approx(366 / 365, rel=1e-4)