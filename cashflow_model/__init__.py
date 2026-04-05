"""
Cashflow Model — Fixed Income Analytics Engine

A modular library for bond and loan cashflow projection,
present value calculations, and interest rate scenario analysis.
"""

from cashflow_model.instrument import Bond, Loan
from cashflow_model.cashflow_engine import (
    Cashflow,
    project_bond_cashflows,
    project_amortizing_loan,
    total_cashflows,
    total_interest,
)
from cashflow_model.day_count import get_year_fraction
from cashflow_model.accrual import (
    simple_interest,
    compound_interest,
    accrued_interest,
    clean_price,
)
from cashflow_model.present_value import (
    discount,
    calculate_npv,
    calculate_ytm,
    calculate_duration,
    calculate_modified_duration,
)
from cashflow_model.scenario import (
    Scenario,
    STANDARD_SCENARIOS,
    run_scenario,
    run_all_scenarios,
    estimate_pnl_from_duration,
)

__all__ = [
    # Instruments
    "Bond",
    "Loan",
    # Cashflows
    "Cashflow",
    "project_bond_cashflows",
    "project_amortizing_loan",
    "total_cashflows",
    "total_interest",
    # Day count
    "get_year_fraction",
    # Accrual
    "simple_interest",
    "compound_interest",
    "accrued_interest",
    "clean_price",
    # Present value
    "discount",
    "calculate_npv",
    "calculate_ytm",
    "calculate_duration",
    "calculate_modified_duration",
    # Scenario
    "Scenario",
    "STANDARD_SCENARIOS",
    "run_scenario",
    "run_all_scenarios",
    "estimate_pnl_from_duration",
]
