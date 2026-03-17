from dataclasses import dataclass


@dataclass
class Cashflow:
    date: object
    amount: float
    cashflow_type: str


def project_bond_cashflows(bond, convention="30/360"):
    cashflows = []

    for payment_date in bond.get_payment_dates():
        cashflows.append(
            Cashflow(
                date=payment_date,
                amount=bond.get_coupon_amount(),
                cashflow_type="COUPON",
            )
        )

        if payment_date == bond.maturity_date:
            cashflows.append(
                Cashflow(
                    date=payment_date,
                    amount=bond.face_value,
                    cashflow_type="PRINCIPAL",
                )
            )

    return cashflows


def project_amortizing_loan(balance, annual_rate, monthly_payment, num_months):
    cashflows = []
    remaining_balance = balance

    for month in range(1, num_months + 1):
        interest = remaining_balance * annual_rate / 12
        principal_portion = monthly_payment - interest

        if principal_portion > remaining_balance:
            principal_portion = remaining_balance
            monthly_total = interest + principal_portion
        else:
            monthly_total = monthly_payment

        cashflows.append(
            Cashflow(
                date=f"Month {month}",
                amount=interest,
                cashflow_type="INTEREST",
            )
        )

        cashflows.append(
            Cashflow(
                date=f"Month {month}",
                amount=principal_portion,
                cashflow_type="PRINCIPAL",
            )
        )

        remaining_balance -= principal_portion

        if remaining_balance <= 1e-8:
            remaining_balance = 0
            break

    return cashflows


def print_cashflow_schedule(cashflows):
    print(f"{'Date':<15} {'Type':<12} {'Amount':>12} {'Running Total':>15}")
    print("-" * 58)

    running_total = 0.0

    for cf in cashflows:
        running_total += cf.amount
        print(f"{str(cf.date):<15} {cf.cashflow_type:<12} {cf.amount:>12.2f} {running_total:>15.2f}")


def total_cashflows(cashflows):
    return sum(cf.amount for cf in cashflows)


def total_interest(cashflows):
    return sum(cf.amount for cf in cashflows if cf.cashflow_type in ["COUPON", "INTEREST"])
