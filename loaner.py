#pylint: disable=[invalid-name]
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

# assumptions:
# - compound interest
# - monthly payment / compunding

# inputs
princ = 10_000              # principal
inter = 0.05                # interest rate (% annual)
payme = 250                 # monthly payment
d, m, y = (1, 1, 2020)      # first repayment date (DD,MM,YYYY)

# initialize (first month)
ind = 0
date = [datetime(year=y, month=m, day=d)]       # Payment date
bal_open = [princ]                              # monthly opening balance
int_acc = [bal_open[ind]*inter/12]              # interest accrued during month
contrib = [payme]                               # contribution (payment)
bal_close = [bal_open[0] + int_acc[0] - contrib[0]]

# monthly payments
while bal_close[ind] > 0:
    ind += 1
    date.append(date[ind-1] + relativedelta(months=+1))
    bal_open.append(bal_close[ind-1])
    int_acc.append(bal_open[ind]*inter/12)
    contrib.append(payme)
    if bal_open[ind] + int_acc[ind] < contrib[ind]:
        contrib[ind] = bal_open[ind] + int_acc[ind]
    bal_close.append(bal_open[ind] + int_acc[ind] - contrib[ind])

# repayment summary table
pd.options.display.float_format = "${:,.2f}".format
sum_df = pd.DataFrame(
    {
        "Date": date,
        "Opening Balance": bal_open,
        "Accrued Interest": int_acc,
        "Contribution": contrib,
        "Closing Balance": bal_close
    }
)
tot_int = sum_df['Accrued Interest'].sum()
tot_pay = sum_df["Contribution"].sum()

# output results
out = (f"Loan Summary\n"
       "------------\n"
       f"Principal:         ${princ:.2f}\n"
       f"Interest rate:     {inter:.2f}%\n"
       f"Monthly Payment:   ${payme:.2f}\n"
       f"Repayment Period:  {len(sum_df)} weeks\n"
       f"Total interest:    ${tot_int:.2f}\n"
       f"Total paid:        ${tot_pay:.2f}\n\n\n"
       f"Repayment summary table:\n"
       "------------------------\n"
       f"{sum_df}")
print(out)
