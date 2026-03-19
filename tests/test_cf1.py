"""Scenario analysis utility functions and tests for interest rate shocks."""
from dataclasses import dataclass
from datetime import date

from tests.test_utils import approx, run_module_tests

from cashflow_model.cashflow_engine import project_bond_cashflows
from cashflow_model.instrument import Bond
from cashflow_model.present_value import calculate_npv


@dataclass
class Scenario:
    """Represents an interest rate scenario."""
    name: str
    rate_shift: float
    description: str = ""


STANDARD_SCENARIOS = [
    Scenario("Rates +0.5%", 0.005, "Rates rise by 50 bps"),
    Scenario("Rates +1%", 0.01, "Rates rise by 100 bps"),
    Scenario("Rates +2%", 0.02, "Rates rise by 200 bps"),
    Scenario("Rates -0.5%", -0.005, "Rates fall by 50 bps"),
    Scenario("Rates -1%", -0.01, "Rates fall by 100 bps"),
    Scenario("Rates -2%", -0.02, "Rates fall by 200 bps"),
]


def run_scenario(bond, base_rate, scenario, as_of_date, convention="ACT/365"):
    """Run a single scenario and return NPV."""
    cashflows = project_bond_cashflows(bond)
    shocked_rate = base_rate + scenario.rate_shift
    return calculate_npv(cashflows, shocked_rate, as_of_date, convention)


def run_all_scenarios(bond, base_rate, scenarios, as_of_date, convention="ACT/365"):
    """Run all scenarios and return base NPV and scenario results."""
    cashflows = project_bond_cashflows(bond)
    base_npv = calculate_npv(cashflows, base_rate, as_of_date, convention)

    results = []

    for scenario in scenarios:
        shocked_rate = base_rate + scenario.rate_shift
        new_npv = calculate_npv(cashflows, shocked_rate, as_of_date, convention)
        dollar_change = new_npv - base_npv
        pct_change = (dollar_change / base_npv) * 100

        results.append((scenario.name, new_npv, dollar_change, pct_change))

    return base_npv, results


def print_scenario_report(base_npv, scenario_results):
    """Print formatted scenario analysis report."""
    print(f"Base NPV: {base_npv:.2f}\n")
    print(f"{'Scenario':<15} {'NPV':>12} {'$ Change':>12} {'% Change':>12}")
    print("-" * 55)

    for name, new_npv, dollar_change, pct_change in scenario_results:
        print(f"{name:<15} {new_npv:>12.2f} {dollar_change:>12.2f} {pct_change:>11.2f}%")


def estimate_pnl_from_duration(modified_duration, rate_change, portfolio_value):
    """Estimate P&L from duration approximation."""
    return -modified_duration * rate_change * portfolio_value


# ============================================================================
# TESTS
# ============================================================================

def test_scenario_definition():
    """Test Scenario dataclass creation."""
    scenario = Scenario("Test", 0.01, "Test description")
    assert scenario.name == "Test"
    assert scenario.rate_shift == 0.01
    assert scenario.description == "Test description"


def test_standard_scenarios_loaded():
    """Test that standard scenarios are properly defined."""
    assert len(STANDARD_SCENARIOS) == 6
    assert STANDARD_SCENARIOS[0].name == "Rates +0.5%"
    assert STANDARD_SCENARIOS[0].rate_shift == 0.005


def test_run_scenario():
    """Test running a single scenario."""
    bond = Bond(
        name="Test Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    
    scenario = Scenario("Test +1%", 0.01)
    npv = run_scenario(bond, 0.04, scenario, date(2024, 1, 1))
    
    assert isinstance(npv, float)
    assert npv > 0


def test_run_all_scenarios():
    """Test running all scenarios."""
    bond = Bond(
        name="Test Bond",
        face_value=1000.0,
        coupon_rate=0.05,
        payment_frequency=1,
        issue_date=date(2024, 1, 1),
        maturity_date=date(2027, 1, 1),
    )
    
    base_npv, results = run_all_scenarios(
        bond, 0.04, STANDARD_SCENARIOS, date(2024, 1, 1)
    )
    
    assert len(results) == len(STANDARD_SCENARIOS)
    assert base_npv > 0
    
    for name, npv, dollar_change, pct_change in results:
        assert isinstance(npv, float)
        assert isinstance(dollar_change, float)
        assert isinstance(pct_change, float)


def test_estimate_pnl_from_duration():
    """Test PnL estimation using duration."""
    modified_duration = 2.5
    rate_change = 0.01  # +100 bps
    portfolio_value = 1000000.0
    
    pnl = estimate_pnl_from_duration(modified_duration, rate_change, portfolio_value)
    
    # Loss should be negative when rates go up
    assert pnl < 0
    assert pnl == approx(-25000.0)


if __name__ == "__main__":
    raise SystemExit(run_module_tests(globals()))