# loaner
Loaner is a utility Python package containing tools for evaluating loan offers.

## Usage
---
```Python
from loaner import Loan

principal = 10000
interest = 0.06
payment = 193.33
start = (1, 1, 2020)
inflation = 0.015
loan = Loan(principal, interest, payment, start, inflation)

loan.tot_int # returns total interest paid
loan.tot_pay # returns total amount paid
loan.table # returns payment schedule as pandas.DataFrame

loan.pv_int # returns present value of interest paid
loan.pv_pay # returns present value of amount paid
loan.pv_table # returns payment schedule with PV calculations, as pandas.DataFrame
```

## License
[MIT](LICENSE)
