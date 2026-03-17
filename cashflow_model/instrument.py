from datetime import date
from dateutil.relativedelta import relativedelta


class Bond:
    def __init__(
        self,
        name: str,
        face_value: float,
        coupon_rate: float,
        payment_frequency: int,
        issue_date: date,
        maturity_date: date,
    ):
        self.name = name
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.payment_frequency = payment_frequency
        self.issue_date = issue_date
        self.maturity_date = maturity_date

    def get_coupon_amount(self) -> float:
        """
        Coupon payment per period.
        Example:
        1000 face value, 5% annual coupon, semiannual payments
        = 1000 * 0.05 / 2 = 25
        """
        return self.face_value * self.coupon_rate / self.payment_frequency

    def get_payment_dates(self) -> list:
        """
        Generate coupon payment dates from issue_date to maturity_date.

        For example:
        payment_frequency = 2  -> every 6 months
        payment_frequency = 4  -> every 3 months
        payment_frequency = 12 -> every 1 month
        """
        payment_dates = []

        months_per_step = 12 // self.payment_frequency
        current_date = self.issue_date + relativedelta(months=months_per_step)

        while current_date <= self.maturity_date:
            payment_dates.append(current_date)
            current_date += relativedelta(months=months_per_step)

        return payment_dates

    def __str__(self) -> str:
        years_to_maturity = (self.maturity_date - self.issue_date).days / 365.25

        return (
            f"Bond(name='{self.name}', "
            f"face_value={self.face_value:.2f}, "
            f"coupon_rate={self.coupon_rate:.2%}, "
            f"payment_frequency={self.payment_frequency}, "
            f"years_to_maturity={years_to_maturity:.2f})"
        )


class Loan:
    def __init__(
        self,
        name: str,
        original_balance: float,
        coupon_rate: float,
        payment_frequency: int,
        issue_date: date,
        maturity_date: date,
        monthly_payment: float,
    ):
        self.name = name
        self.original_balance = original_balance
        self.coupon_rate = coupon_rate
        self.payment_frequency = payment_frequency
        self.issue_date = issue_date
        self.maturity_date = maturity_date
        self.monthly_payment = monthly_payment

    def __str__(self) -> str:
        years_to_maturity = (self.maturity_date - self.issue_date).days / 365.25

        return (
            f"Loan(name='{self.name}', "
            f"original_balance={self.original_balance:.2f}, "
            f"coupon_rate={self.coupon_rate:.2%}, "
            f"payment_frequency={self.payment_frequency}, "
            f"monthly_payment={self.monthly_payment:.2f}, "
            f"years_to_maturity={years_to_maturity:.2f})"
        )
