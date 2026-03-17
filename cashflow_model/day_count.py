from datetime import date


# -----------------------------
# ACTUAL / 360
# -----------------------------
def actual_360(start_date, end_date):
    return (end_date - start_date).days / 360


# -----------------------------
# ACTUAL / 365
# -----------------------------
def actual_365(start_date, end_date):
    return (end_date - start_date).days / 365


# -----------------------------
# 30 / 360
# -----------------------------
def thirty_360(start_date, end_date):
    y1, m1, d1 = start_date.year, start_date.month, start_date.day
    y2, m2, d2 = end_date.year, end_date.month, end_date.day

    return (360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)) / 360


# -----------------------------
# ACTUAL / ACTUAL
# -----------------------------
def actual_actual(start_date, end_date):
    # Same year
    if start_date.year == end_date.year:
        days_in_year = 366 if is_leap_year(start_date.year) else 365
        return (end_date - start_date).days / days_in_year

    total = 0.0

    # First year part
    end_of_start_year = date(start_date.year + 1, 1, 1)
    days_in_start_year = 366 if is_leap_year(start_date.year) else 365
    total += (end_of_start_year - start_date).days / days_in_start_year

    # Full years in between
    for year in range(start_date.year + 1, end_date.year):
        total += 1.0

    # Last year part
    start_of_end_year = date(end_date.year, 1, 1)
    days_in_end_year = 366 if is_leap_year(end_date.year) else 365
    total += (end_date - start_of_end_year).days / days_in_end_year

    return total


# -----------------------------
# Leap Year Check
# -----------------------------
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# -----------------------------
# HELPER FUNCTION
# -----------------------------
def get_year_fraction(start_date, end_date, convention):
    convention = convention.upper()

    if convention == "ACT/360":
        return actual_360(start_date, end_date)

    elif convention == "ACT/365":
        return actual_365(start_date, end_date)

    elif convention == "30/360":
        return thirty_360(start_date, end_date)

    elif convention == "ACT/ACT":
        return actual_actual(start_date, end_date)

    else:
        raise ValueError(f"Unsupported convention: {convention}")