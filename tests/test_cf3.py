from datetime import date
from cashflow_model.instrument import Bond
from cashflow_model.accrual import (
    simple_interest,
    compound_interest,
    find_last_coupon_date,
    find_next_coupon_date,
    accrued_interest,
    clean_price,
)

# -----------------------------------
# Create test bond
# -----------------------------------
bond = Bond(
    name="US Treasury 5Y",
    face_value=1000.0,
    coupon_rate=0.05,
    payment_frequency=2,
    issue_date=date(2024, 1, 1),
    maturity_date=date(2029, 1, 1),
)

# -----------------------------------
# Test simple interest
# -----------------------------------
si = simple_interest(1000, 0.05, 0.25)
print("Simple interest:", si)

# -----------------------------------
# Test compound interest
# -----------------------------------
ci = compound_interest(1000, 0.05, 1, 2)
print("Compound interest:", ci)

# -----------------------------------
# Test coupon dates around settlement
# -----------------------------------
settlement = date(2024, 4, 1)

last_coupon = find_last_coupon_date(bond, settlement)
next_coupon = find_next_coupon_date(bond, settlement)

print("Last coupon date:", last_coupon)
print("Next coupon date:", next_coupon)

# -----------------------------------
# Test accrued interest
# -----------------------------------
accrued = accrued_interest(bond, settlement, convention="30/360")
print("Accrued interest:", accrued)

# -----------------------------------
# Test clean price
# -----------------------------------
dirty = 1012.50
clean = clean_price(dirty, accrued)

print("Dirty price:", dirty)
print("Clean price:", clean)