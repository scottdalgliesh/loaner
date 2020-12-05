#pylint:disable=[missing-function-docstring, protected-access]
from typing import Any, Callable

import pytest

from loaner.loaner import Loan  # pylint:disable=[import-error]



class TestValidation:
    """Input validation unit tests."""

    @staticmethod
    def check_validation(func: Callable, inp: Any, exception_raised: bool) -> None:
        """Base function for testing input validation methods

        Parameters
        ----------
        func : None
            input validation function to test
        inp : Any
            Input to validate using func
        exception_raised : bool
            True if exception is expected to be raised
        """
        if not exception_raised:
            assert func(inp) is None
        else:
            with pytest.raises(ValueError):
                func(inp)

    princ_input = [
        pytest.param(-1, True, id="negative"),
        pytest.param(0, True, id="zero"),
        pytest.param(1, False, id="positive")
    ]

    @pytest.mark.parametrize("inp, exception_raised", princ_input)
    def test_validate_princ(self, inp, exception_raised):
        self.check_validation(Loan._validate_princ, inp, exception_raised)

    inter_input = [
        pytest.param(-0.01, True, id="negative"),
        pytest.param(0, True, id="zero"),
        pytest.param(0.01, False, id="positive < 1"),
        pytest.param(1.01, True, id="positive > 1"),
    ]

    @pytest.mark.parametrize("inp, exception_raised", inter_input)
    def test_validate_inter(self, inp, exception_raised):
        self.check_validation(Loan._validate_inter, inp, exception_raised)

    payme_input = [
        pytest.param(-0.01, True, id="negative"),
        pytest.param(0, True, id="zero"),
        pytest.param(0.01, False, id="positive"),
    ]

    @pytest.mark.parametrize("inp, exception_raised", payme_input)
    def test_validate_payme(self, inp, exception_raised):
        self.check_validation(Loan._validate_inter, inp, exception_raised)

    start_input = [
        pytest.param((1, 1), True, id="incomplete tuple"),
        pytest.param((1, 1, 1, 1), True, id="oversized tuple"),
        pytest.param((13, 1, 1), True, id="invalid month"),
        pytest.param((1, 0, 1), True, id="invalid day"),
        pytest.param((1, 1, -1), True, id="invalid year"),
        pytest.param((12, 1, 1), False, id="valid tuple")
    ]

    @pytest.mark.parametrize("inp, exception_raised", start_input)
    def test_validate_start(self, inp, exception_raised):
        func = Loan._validate_start
        if not exception_raised:
            assert func(inp) is True
        else:
            with pytest.raises(ValueError):
                func(inp)


class TestCalculation:
    """Interest calculation unit tests."""

    # test case taken from: https://www.calculator.net/loan-calculator.html
    test_calc_inp = [
        pytest.param(10_000, 0.06, 193.33, 1599.68, 60, id="basic_1"),
        pytest.param(25_000, 0.06, 1108.02, 1592.37, 24, id="basic_2"),
        pytest.param(10_000, 0.06, 10_050, 50, 1, id="single_period")
    ]

    @pytest.mark.parametrize("princ, inter, payme, tot_int, period", test_calc_inp)
    def test_calculate_payment_schedule(self, princ, inter, payme, tot_int, period):
        test_loan = Loan(
            princ=princ,
            inter=inter,
            payme=payme,
            start=(1, 1, 2020)
        )
        assert test_loan.tot_int == tot_int
        assert len(test_loan.table) == period

    def test_calculate_pv_table(self):
        test_loan = Loan(
            princ=10_000,
            inter=0.06,
            payme=193.33,
            start=(1, 1, 2020),
            infl=0.015
        )
        assert test_loan.pv_table.loc[11,"Inflation Factor"] == f"{(1+test_loan.infl)**(-1):.2%}"
        assert test_loan.pv_table.loc[23,"Inflation Factor"] == f"{(1+test_loan.infl)**(-2):.2%}"
        assert test_loan.pv_table.loc[59,"Inflation Factor"] == f"{(1+test_loan.infl)**(-5):.2%}"


class TestMisc:
    """Misc tests for Loan object"""

    @pytest.fixture
    def sample_loan(self):
        return Loan(10_000, 0.06, 1000, (1, 1, 2020))

    def test_str(self, sample_loan):
        sample_repr = "Loan(princ=10000, inter=0.06, payme=1000, start=(1, 1, 2020), infl=0.015)"
        assert sample_loan.__repr__() == sample_repr

    def test_repr(self, sample_loan):
        sample_str = (
            "Loan Summary\n"
            "------------\n"
            "Principal:         $10000.00\n"
            "Interest rate:     6.00%\n"
            "Monthly Payment:   $1000.00\n"
            "Start Date:        01-01-2020\n"
            "Repayment Period:  11 weeks\n"
            "Total interest:    $284.80\n"
            "Total paid:        $10284.80\n\n\n"
        )
        assert sample_loan.__str__() == sample_str
