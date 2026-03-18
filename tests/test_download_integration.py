"""Integration tests for JSON I/O adapter."""
from cashflow_model.io_adapter import (
    load_json_file,
    build_bond_and_project_cashflows,
)


def test_build_bond_and_project_cashflows():
    """Test building bond from JSON and projecting cashflows."""
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
    
    assert isinstance(result, dict)
    assert "cashflows" in result
    assert len(result["cashflows"]) > 0
    
    # Check basic fields are in the result
    assert result["instrument_type"] == "bond"
    assert result["coupon_rate"] == 0.05


def test_cashflows_have_required_fields():
    """Test that projected cashflows have required fields."""
    instrument_data = {
        "instrument_id": "TEST_BOND",
        "instrument_type": "bond",
        "principal": 1000,
        "currency": "USD",
        "issue_date": "2024-01-01",
        "maturity_date": "2026-01-01",
        "coupon_rate": 0.04,
        "payment_frequency": "annual",
        "day_count_convention": "ACT/365"
    }
    
    result = build_bond_and_project_cashflows(instrument_data)
    
    for cf in result["cashflows"]:
        assert "date" in cf
        assert "type" in cf
        assert "amount" in cf


def test_cashflow_total_matches_principal():
    """Test that principal appears in final cashflow."""
    instrument_data = {
        "instrument_id": "TEST_BOND",
        "instrument_type": "bond",
        "principal": 1000,
        "currency": "USD",
        "issue_date": "2024-01-01",
        "maturity_date": "2025-01-01",
        "coupon_rate": 0.05,
        "payment_frequency": "annual",
        "day_count_convention": "ACT/365"
    }
    
    result = build_bond_and_project_cashflows(instrument_data)
    
    # Check that final cashflow includes principal
    final_cf = result["cashflows"][-1]
    assert final_cf["type"] == "principal" or "principal" in str(final_cf).lower()


def test_semi_annual_frequency():
    """Test semi-annual payment frequency."""
    instrument_data = {
        "instrument_id": "SA_BOND",
        "instrument_type": "bond",
        "principal": 1000,
        "currency": "USD",
        "issue_date": "2024-01-01",
        "maturity_date": "2026-01-01",
        "coupon_rate": 0.04,
        "payment_frequency": "semi-annual",
        "day_count_convention": "ACT/365"
    }
    
    result = build_bond_and_project_cashflows(instrument_data)
    
    # 2 years * 2 payments/year + principal = 5 cashflows
    assert len(result["cashflows"]) == 5


def test_quarterly_frequency():
    """Test quarterly payment frequency."""
    instrument_data = {
        "instrument_id": "Q_BOND",
        "instrument_type": "bond",
        "principal": 1000,
        "currency": "USD",
        "issue_date": "2024-01-01",
        "maturity_date": "2025-01-01",
        "coupon_rate": 0.04,
        "payment_frequency": "quarterly",
        "day_count_convention": "ACT/365"
    }
    
    result = build_bond_and_project_cashflows(instrument_data)
    
    # 1 year * 4 payments/year + principal = 5 cashflows
    assert len(result["cashflows"]) == 5