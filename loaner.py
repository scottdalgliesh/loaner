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
    bal_close.append(bal_open[ind] + int_acc[ind] - contrib[ind])

sum_df = pd.DataFrame(
    {
        "Date": date,
        "Opening Balance": bal_open,
        "Accrued Interest": int_acc,
        "Contribution": contrib,
        "Closing Balance": bal_close
    }
)

print(sum_df)