from datetime import date
from cashflow_model.day_count import (
    actual_360,
    actual_365,
    thirty_360,
    actual_actual,
    get_year_fraction
)

# -----------------------------
# TEST 1
# -----------------------------
start = date(2024, 1, 1)
end = date(2024, 7, 1)

print("=== Jan 1 → Jul 1 ===")
print("ACT/360:", actual_360(start, end))
print("ACT/365:", actual_365(start, end))
print("30/360 :", thirty_360(start, end))
print("ACT/ACT:", actual_actual(start, end))

print("\nUsing helper:")
print("ACT/360:", get_year_fraction(start, end, "ACT/360"))
print("30/360 :", get_year_fraction(start, end, "30/360"))

# -----------------------------
# TEST 2 (LEAP YEAR EDGE CASE)
# -----------------------------
start2 = date(2024, 2, 28)
end2 = date(2024, 3, 1)

print("\n=== Feb 28 → Mar 1 (Leap Year) ===")
print("ACT/360:", actual_360(start2, end2))
print("ACT/365:", actual_365(start2, end2))
print("30/360 :", thirty_360(start2, end2))
print("ACT/ACT:", actual_actual(start2, end2))