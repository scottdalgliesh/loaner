#pylint:disable=[missing-function-docstring, protected-access]
from typing import Any, Callable

import pytest

from loaner import Loan

#TODO: add tests for loan object

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

    def test_calculate_payment_schedule(self):
        test_loan = Loan(
            princ=10_000,
            inter=0.06,
            payme=193.33,
            start=(1, 1, 2020)
        )
        delta_int = abs(test_loan.tot_int - 1599.68)
        assert delta_int == 0
        # TODO: modify Loan._calculate_payment_schedule() to correctly round
        # interest and payments to 2 decimal places
