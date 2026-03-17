from cashflow_model.day_count import get_year_fraction
from cashflow_model.cashflow_engine import project_bond_cashflows


def discount(amount, rate, years):
    return amount / (1 + rate) ** years


def calculate_npv(cashflows, discount_rate, as_of_date, convention="ACT/365"):
    total_npv = 0.0

    for cf in cashflows:
        years = get_year_fraction(as_of_date, cf.date, convention)
        pv = discount(cf.amount, discount_rate, years)
        total_npv += pv

    return total_npv


def calculate_ytm(bond, market_price, convention="ACT/365"):
    cashflows = project_bond_cashflows(bond)

    low = 0.001
    high = 0.30
    tolerance = 0.01

    while high - low > 1e-10:
        mid = (low + high) / 2
        npv = calculate_npv(cashflows, mid, bond.issue_date, convention)

        if abs(npv - market_price) < tolerance:
            return mid

        if npv > market_price:
            low = mid
        else:
            high = mid

    return (low + high) / 2


def calculate_duration(cashflows, ytm, as_of_date, convention="ACT/365"):
    total_pv = calculate_npv(cashflows, ytm, as_of_date, convention)

    duration = 0.0

    for cf in cashflows:
        years = get_year_fraction(as_of_date, cf.date, convention)
        pv = discount(cf.amount, ytm, years)
        weight = pv / total_pv
        duration += weight * years

    return duration


def calculate_modified_duration(macaulay_duration, ytm, frequency):
    return macaulay_duration / (1 + ytm / frequency)
