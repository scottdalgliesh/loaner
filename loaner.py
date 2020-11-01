from datetime import date
from typing import Optional, Tuple

import pandas as pd
from dateutil.relativedelta import relativedelta

# assumptions:
# - compound interest
# - monthly payment / compunding


class Loan:
    """Creates a Loan object. Used for assessment of loan repayment options.
    """

    def __init__(self, princ: float, inter: float,
                 payme: float, start: Optional[Tuple[int]] = None) -> None:
        if princ <= 0:
            raise ValueError("Principal must be greater than zero.")
        self.princ = princ

        if not 0 < inter < 1:
            raise ValueError("Interest must be between 0 and 1.")
        self.inter = inter

        if payme <= 0:
            raise ValueError("Payment must be greater than 0.")
        self.payme = payme

        if start is None:
            self.start = date.today()
        elif self._check_start_date(start):
            self.start = date(year=start[2], month=start[1], day=start[0])
        else:
            raise ValueError("Date must be specified as (mm,dd,yyyy).")

        pd.options.display.float_format = "${:,.2f}".format
        pd.options.display.width = 0
        self.table = self._calculate_payment_schedule()
        self.tot_int = round(self.table['Accrued Interest'].sum(), 2)
        self.tot_pay = round(self.table["Contribution"].sum(), 2)

    def _calculate_payment_schedule(self) -> pd.DataFrame:
        """Calculate a payment summary table for the loan.

        Returns
        -------
        pd.DataFrame
            Payment summary table stored in a DataFrame
        """

        # initialize (first month)
        ind = 0
        pay_date = [self.start]
        bal_open = [self.princ]
        int_acc = [bal_open[ind]*self.inter/12]
        contrib = [self.payme]
        bal_close = [bal_open[0] + int_acc[0] - contrib[0]]

        # monthly payments
        while bal_close[ind] > 0:
            ind += 1
            pay_date.append(pay_date[ind-1] + relativedelta(months=+1))
            bal_open.append(bal_close[ind-1])
            int_acc.append(bal_open[ind]*self.inter/12)
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

    @staticmethod
    def _check_start_date(start) -> bool:
        """Validate start date input.

        Parameters
        ----------
        start : Tuple
            Start date entered as (mm,dd,yyyy)

        Returns
        -------
        bool
        """

        if not len(start) == 3:
            return False
        try:
            date(year=start[2], month=start[1], day=start[0])
        except ValueError:
            return False
        return True

    def __repr__(self):
        """convert to formal string, for repr()."""
        date_str = self.start.strftime("%m,%d,%Y")
        msg = (f"Loan(princ={self.princ}, inter={self.inter}"
               f", payme={self.payme}, start=({date_str}))")
        return msg

    def __str__(self):
        """convert to string representation"""
        msg = ("Loan Summary\n"
               "------------\n"
               f"Principal:         ${self.princ:.2f}\n"
               f"Interest rate:     {self.inter:.2f}%\n"
               f"Monthly Payment:   ${self.payme:.2f}\n"
               f"Start Date:        {self.start.strftime('%m,%d,%Y')}\n"
               f"Repayment Period:  {len(self.table)} weeks\n"
               f"Total interest:    ${self.tot_int:.2f}\n"
               f"Total paid:        ${self.tot_pay:.2f}\n\n\n"
               f"Repayment summary table:\n"
               "------------------------\n"
               f"{self.table}")
        return msg
