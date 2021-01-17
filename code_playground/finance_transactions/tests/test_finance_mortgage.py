import pandas as pd

from unittest import TestCase, mock
from finance_transactions.src.finance_mortgage import MortgageService
from finance_transactions.src.constants import MortgageConfig as constants

# from points.tests.constants import TestOrderConfig


class TestMorgageService(TestCase):
    """
    Background Thinking:
    1. wanted to use the same test case data from the assignment to test all the functions where possible
    2. some functions are easy to test the further down in the class OrderDataObject
    ie. initial test for get_data_to_dataframe is hard to test without rerunning the same method used to create function
    """

    def setUp(self):
        self.sut = MortgageService
        self.constants = constants

        self.raw_data = {}
        self.raw_data_df = pd.DataFrame().from_dict(self.raw_data)
        # self.final_data_df = pd.DataFrame().from_dict(TestOrderConfig.ORDERS_GROUPED)

    def tearDown(self):
        pass

    def test_get_period_prime_rate(self):

        xrates = x.get_period_prime_rate("2017-04-01")
        rrates = x.get_period_prime_rate("2020-04-27")
        vrates = x.get_period_prime_rate("2020-05-01")


if __name__ == "__main__":
    unittest.handle()
