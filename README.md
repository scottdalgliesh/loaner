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
loan = Loan(principal, interest, payment, start)

loan.tot_int # returns total interest paid
loan.tot_pay # returns total amount paid
loan.table # returns payment schedule as pandas.DataFrame
```

## License
[MIT](LICENSE)
