from dataclasses import dataclass

from cashflow_model.cashflow_engine import project_bond_cashflows
from cashflow_model.present_value import calculate_npv


@dataclass
class Scenario:
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
	cashflows = project_bond_cashflows(bond)
	shocked_rate = base_rate + scenario.rate_shift
	return calculate_npv(cashflows, shocked_rate, as_of_date, convention)


def run_all_scenarios(bond, base_rate, scenarios, as_of_date, convention="ACT/365"):
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
	print(f"Base NPV: {base_npv:.2f}\n")
	print(f"{'Scenario':<15} {'NPV':>12} {'$ Change':>12} {'% Change':>12}")
	print("-" * 55)

	for name, new_npv, dollar_change, pct_change in scenario_results:
		print(f"{name:<15} {new_npv:>12.2f} {dollar_change:>12.2f} {pct_change:>11.2f}%")


def estimate_pnl_from_duration(modified_duration, rate_change, portfolio_value):
	return -modified_duration * rate_change * portfolio_value
