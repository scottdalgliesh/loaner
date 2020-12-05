# loaner
Loaner is a utility package containing tools for comparative evaluation of loan offers.

## Basic Usage
```Python
from loaner import Loan

# input parameters
principal = 10000
interest = 0.06
payment = 193.33
start = (1, 1, 2020)
inflation = 0.015

# create loan object 
loan = Loan(principal, interest, payment, start, inflation)

print(loan)     # general summary of loan details

loan.period     # repayment length (months)
loan.end_date   # repayment end date, as datetime
loan.tot_int    # total interest paid
loan.tot_pay    # total amount paid
loan.table      # payment schedule, as pandas.DataFrame

loan.pv_int     # present value of interest paid (inflation adjusted)
loan.pv_pay     # present value of amount paid (inflation adjusted)
loan.pv_table   # payment schedule with present value calculations (inflation adjustment) as pandas.DataFrame
```

## License
[MIT](LICENSE)
