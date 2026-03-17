from cashflow_model.day_count import get_year_fraction


def simple_interest(principal, annual_rate, year_fraction):
    return principal * annual_rate * year_fraction


def compound_interest(principal, annual_rate, year_fraction, frequency):
    return principal * (1 + annual_rate / frequency) ** (frequency * year_fraction) - principal


def find_last_coupon_date(bond, settlement_date):
    last_date = bond.issue_date

    for payment_date in bond.get_payment_dates():
        if payment_date <= settlement_date:
            last_date = payment_date
        else:
            break

    return last_date


def find_next_coupon_date(bond, settlement_date):
    for payment_date in bond.get_payment_dates():
        if payment_date > settlement_date:
            return payment_date

    return None


def accrued_interest(bond, settlement_date, convention="30/360"):
    last_coupon = find_last_coupon_date(bond, settlement_date)
    year_fraction = get_year_fraction(last_coupon, settlement_date, convention)

    annual_coupon = bond.face_value * bond.coupon_rate
    return annual_coupon * year_fraction


def clean_price(dirty_price, accrued):
    return dirty_price - accrued
