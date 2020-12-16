import pandas as pd

from unittest import TestCase, mock
from points.src.order import OrderDataObject
from points.src.constants import OrderConfig
from points.tests.constants import TestOrderConfig


class TestOrderDataObject(TestCase):
    """
    Background Thinking:
    1. wanted to use the same test case data from the assignment to test all the functions where possible
    2. some functions are easy to test the further down in the class OrderDataObject
    ie. initial test for get_data_to_dataframe is hard to test without rerunning the same method used to create function
    """

    def setUp(self):
        self.sut = OrderDataObject()
        self.data_constants = OrderConfig

        self.raw_data = TestOrderConfig.ORDERS
        self.raw_data_df = pd.DataFrame().from_dict(self.raw_data)
        self.final_data_df = pd.DataFrame().from_dict(TestOrderConfig.ORDERS_GROUPED)

    def tearDown(self):
        pass

    def test_get_data_to_dataframe(self):
        """
        Test that dataframe exists and is not empty
        Don't want to use the same method I used in my function to do the test
        """
        result = self.sut.get_data_to_dataframe(self.raw_data)

        # test that dataframe is exists
        self.assertIsNotNone(result)

        # test that dataframe is not empty
        self.assertFalse(result.empty)

    def test_groupby_sum_dataframe(self):
        """
        Test that dataframe sums the proper columns
        """

        # filter final data and update column names
        payload_df = self.final_data_df
        payload_df = payload_df[
            (payload_df["Offer name"] == "60% Bonus promo")
            & (payload_df["Status"] == "complete")
        ]

        # grab raw data and filter for records that should be summed
        raw_data_df = self.raw_data_df
        raw_data_df = raw_data_df[
            (raw_data_df["offerName"] == "60% Bonus promo")
            & (raw_data_df["status"] == "complete")
        ]

        result = self.sut.groupby_sum_dataframe(
            raw_data_df, self.data_constants.GROUPBY_LIST
        )

        # test that final result equals to final data set payload for a specific record
        self.assertEqual(
            payload_df["Total base points"].sum(), result["basePoints"].sum()
        )
        self.assertEqual(
            payload_df["Total bonus points"].sum(), result["bonusPoints"].sum()
        )

    def test_groupby_unique_dataframe(self):
        """
        Test that dataframe sums the proper columns that should give a unique
        """
        # filter final data and update column names
        payload_df = self.final_data_df
        payload_df = payload_df[
            (payload_df["Offer name"] == "60% Bonus promo")
            & (payload_df["Status"] == "complete")
        ]

        # grab raw data and filter for records that should be summed
        raw_data_df = self.raw_data_df
        raw_data_df = raw_data_df[
            (raw_data_df["offerName"] == "60% Bonus promo")
            & (raw_data_df["status"] == "complete")
        ]

        result = self.sut.groupby_unique_dataframe(
            raw_data_df,
            self.data_constants.GROUPBY_LIST,
            self.data_constants.GROUPBY_UNIQUE_VALUES,
        )

        # test that final result equals to final data set payload for a specific record
        self.assertEqual(payload_df["Unique members"].sum(), result["memberId"].sum())

    def test_merge_dataframes(self):
        """
        Test that new dataframe has all columns. If merged correctly, then all fields appear without suffix changes
        """
        df1 = self.raw_data_df
        df2 = pd.DataFrame().from_dict(
            [{"offerName": "50% Bonus promo", "status": "pending", "new_field": "4"}]
        )

        result = self.sut.merge_dataframes(df1, df2, self.data_constants.GROUPBY_LIST)

        # test that all columns from both dataframes is in the final result
        for item in df1.columns:
            self.assertIn(item, result.columns)

        for item in df2.columns:
            self.assertIn(item, result.columns)

    def test_rename_dataframe_columns(self):
        """
        Test that columns have been renamed and these columns match the final output
        """
        # grab the list columns from final data set
        payload_df = self.final_data_df
        payload_columns = payload_df.columns

        # setup raw dataframe
        result = self.sut.rename_dataframe_columns(
            self.raw_data_df, self.data_constants.GROUPBY_COLUMNS
        )

        # test that column names in final file exist in the result
        for item in payload_columns:
            self.assertIn(item, result.columns)

    def test_handle(self):
        """
        Test that final result is returned
        """
        # load final data set
        payload_df = self.final_data_df
        result = self.sut.handle()

        # test that final result equals to final data set payload
        self.assertEqual(payload_df.to_dict(), result.to_dict())


if __name__ == "__main__":
    unittest.handle()
