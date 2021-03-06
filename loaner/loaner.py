from dataclasses import dataclass
from datetime import date
from typing import Optional, Tuple

import pandas as pd
from dateutil.relativedelta import relativedelta

# assumptions:
# - compound interest
# - monthly payment / compunding


def _rnd(value: float) -> float:
    """Round value to 2 decimal places."""
    return round(value, 2)


@dataclass
class Loan:
    """Creates a Loan object. Used for assessment of loan repayment options."""
    princ: float
    inter: float
    payme: float
    start: Optional[Tuple[int, int, int]] = None
    infl: float = 0.015

    def __post_init__(self) -> None:
        self._validate_princ(self.princ)
        self._validate_inter(self.inter)
        self._validate_payme(self.payme)
        if self.start is None:
            self.start_date: date = date.today()
        elif self._validate_start(self.start):
            self.start_date = date(
                year=self.start[2], month=self.start[0], day=self.start[1])

        pd.options.display.float_format = "${:,.2f}".format
        pd.options.display.width = 0
        self.table = self._calculate_payment_schedule()
        self.tot_int = round(self.table['Accrued Interest'].sum(), 2)
        self.tot_pay = round(self.table["Contribution"].sum(), 2)
        self.period = len(self.table)
        self.end_date = self.table.iloc[-1].loc["Payment Date"]

        self.pv_table = self._calculate_pv_table()
        self.pv_int = _rnd(self.pv_table["pv Interest"].sum())
        self.pv_pay = _rnd(self.pv_table["pv Contrib"].sum())

    @staticmethod
    def _validate_princ(princ) -> None:
        """Validate principal input."""
        if princ <= 0:
            raise ValueError("Principal must be greater than zero.")

    @staticmethod
    def _validate_inter(inter) -> None:
        """Validate interest rate input."""
        if not 0 < inter < 1:
            raise ValueError("Interest must be between 0 and 1.")

    @staticmethod
    def _validate_payme(payme) -> None:
        """Validate payment input."""
        if payme <= 0:
            raise ValueError("Payment must be greater than 0.")

    @staticmethod
    def _validate_start(start) -> bool:
        """Validate start date input."""
        if not len(start) == 3:
            raise ValueError("Date must be specified as (mm,dd,yyyy).")
        try:
            date(year=start[2], month=start[0], day=start[1])
        except ValueError as invalid_date:
            raise ValueError("Date must be specified as (mm,dd,yyyy).") from invalid_date
        return True

    def _calculate_payment_schedule(self) -> pd.DataFrame:
        """Calculate a payment summary table for the loan.

        Returns
        -------
        pd.DataFrame
            Payment summary table stored in a DataFrame
        """

        # initialize (first month)
        ind = 0
        pay_date = [self.start_date]
        bal_open = [self.princ]
        int_acc = [_rnd(bal_open[ind]*self.inter/12)]
        contrib = [self.payme]
        bal_close = [bal_open[0] + int_acc[0] - contrib[0]]

        # monthly payments
        while bal_close[ind] > 0:
            ind += 1
            pay_date.append(pay_date[ind-1] + relativedelta(months=+1))
            bal_open.append(bal_close[ind-1])
            int_acc.append(_rnd(bal_open[ind]*self.inter/12))
            contrib.append(self.payme)
            if bal_open[ind] + int_acc[ind] < contrib[ind]:
                contrib[ind] = bal_open[ind] + int_acc[ind]
            bal_close.append(bal_open[ind] + int_acc[ind] - contrib[ind])

        sum_df = pd.DataFrame(
            {
                "Payment Date": pay_date,
                "Opening Balance": bal_open,
                "Accrued Interest": int_acc,
                "Contribution": contrib,
                "Closing Balance": bal_close
            }
        )
        return sum_df

    def _calculate_pv_table(self):
        table = self.table.copy()
        table["Inflation Factor"] = 1/(1+self.infl)**((table.index+1)/12)
        table["pv Interest"] = table["Inflation Factor"]*table["Accrued Interest"]
        table["pv Contrib"] = table["Inflation Factor"]*table["Contribution"]
        table["Inflation Factor"] = table["Inflation Factor"].map("{:.2%}".format)
        return table

    def __str__(self):
        """convert to string representation"""
        msg = ("Loan Summary\n"
               "------------\n"
               f"Principal:         ${self.princ:.2f}\n"
               f"Interest rate:     {self.inter*100:.2f}%\n"
               f"Monthly payment:   ${self.payme:.2f}\n"
               f"Start date:        {self.start_date.strftime('%m-%d-%Y')}\n"
               f"Repayment period:  {self.period} months\n"
               f"Total interest:    ${self.tot_int:.2f}\n"
               f"Total paid:        ${self.tot_pay:.2f}\n\n\n"
        )
        return msg
