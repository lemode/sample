"""
Background:
* Calculate the mortgage amoritization on the fly
* Select the current period from that schedule
* Create one journal entry to load into Wave Accounting for the current period
* Create multiple journal entries to load into in a specified period

"""

import numpy as np
import pandas as pd
import datetime

from dateutil.relativedelta import relativedelta
from code_playground.finance_transactions.src.constants import (
    MortgageConfig as constants,
)


class MortgageService:
    def __init__(self):
        self.df_mortgage_schedule = pd.DataFrame(columns=constants.SCHEDULE_COLUMNS)
        self.months_per_year = 12

    def convert_string_to_date(self, date_string):
        return datetime.datetime.strptime(date_string, "%Y-%m-%d")

    def get_list_of_dates_rates_changed(self, rate_schedule):

        list_date_keys = rate_schedule.keys()
        list_schedule_dates = []

        for date_keys in list_date_keys:
            schedule_date = self.convert_string_to_date(date_keys)
            list_schedule_dates.append(schedule_date)

        return list_schedule_dates

    def get_start_date(self):
        """
        Finds the start date of the prime rates schedule
        equivalent to when the morgage loan was created
        """
        return self.convert_string_to_date(constants.LOAN_DATE)

    def get_end_date(self, start_date, number_of_years):
        return start_date + relativedelta(years=number_of_years)

    def get_date_range(self, start_date, end_date, rate_schedule):

        # https://stackoverflow.com/questions/22696662/python-list-of-first-day-of-month-for-given-period
        date_range = pd.date_range(
            start_date, end_date, freq="1M"
        ) - pd.offsets.MonthBegin(1)
        return date_range

    def generate_schedule_of_values(
        self, period_date, rate_schedule
    ):
        """
        Calculate the prime rate, payment due or tax schedule for a specific period based on date and rate schedule

        Args:
            period_date : str - the start date of the period you want the rate of
            rate_schedule : dict - the dates where the schedule for all the different prime rates
        """

        period_date = (
            self.convert_string_to_date(period_date).date().strftime("%Y-%m-%d")
        )
        list_rate_schedule = self.get_list_of_dates_rates_changed(rate_schedule)

        min_date = min(list_rate_schedule).date().strftime("%Y-%m-%d")
        max_date = (
            list_rate_schedule[len(list_rate_schedule) - 1].date().strftime("%Y-%m-%d")
        )

        if period_date <= min_date:
            prime_rate = rate_schedule[min_date]
            return prime_rate

        elif period_date >= max_date:
            prime_rate = rate_schedule[max_date]
            return prime_rate
        else:
            for rate_date in list_rate_schedule:
                begin = rate_date.date().strftime("%Y-%m-%d")
                if begin < max_date:
                    end_position = list_rate_schedule.index(rate_date) + 1
                    end = list_rate_schedule[end_position].strftime("%Y-%m-%d")
                    if begin <= period_date < end:
                        prime_rate = rate_schedule[begin]
                        return prime_rate
 
    def get_lifetime_interest_owing(self):
        initial_prime_rate = constants.PRIME_RATES_SCHEDULE[constants.LOAN_DATE]
        contract_rate = constants.PERSONAL_CONTRACT_RATE

        initial_interest_rate = initial_prime_rate + contract_rate
        number_of_periods = (constants.INITIAL_TERM*constants.COMPOUND_FREQUENCY_PER_ANNUM) # remove the initial period

        lifetime_interest_owing = ((1+initial_interest_rate)**number_of_periods-1)
        print(initial_interest_rate)
        print(number_of_periods)
        print(lifetime_interest_owing)
        return lifetime_interest_owing

    def get_mortgage_amount(self):
        total_interest = self.get_lifetime_interest_owing()
        home_value = constants.HOME_VALUE_AMOUNT
        print(total_interest)
        print(home_value)
        return 373360

    def get_monthly_payment(self):
        mortgage_amount = self.get_mortgage_amount()
        compound_period = constants.COMPOUND_FREQUENCY_PER_ANNUM
        number_of_periods = 12 * constants.NUMBER_OF_YEARS
        annual_interest = self.get_annual_interest

        interest_rate = ((1+annual_interest/compound_period)**(compound_period/compound_period))-1



    def generate_rates_schedule(
        self, date_range, rate_schedule=constants.PRIME_RATES_SCHEDULE
    ):
        """
        Calculate mortgage prime  and personal rate schedule based on amounts and schedules

        Args:
            date_range : list - each monthly period within the morgage contract
            rate_schedule : dict - the dates where the schedule for all the different prime rates
        """

        prime_rates_schedule = constants.PRIME_RATES_SCHEDULE
        payment_due_schedule = constants.PAYMENT_DUE_SCHEDULE

        index = 0
        dict_prime_rates = {}
        dict_payment_due = {}

        while index < len(date_range):
            period_date = date_range[index].strftime("%Y-%m-%d")

            period_rate = self.generate_schedule_of_values(period_date,prime_rates_schedule)
            dict_prime_rates.update({period_date: period_rate})

            payment_due = self.generate_schedule_of_values(period_date,payment_due_schedule)
            dict_payment_due.update({period_date: payment_due})

            index += 1

        df_prime_rates = pd.DataFrame.from_dict(dict_prime_rates, orient="index").reset_index()
        df_prime_rates.columns = ["payment_date", "prime_rate"]
        df_prime_rates["payment_date"].astype("datetime64")
        df_prime_rates["contract_rate"] = constants.PERSONAL_CONTRACT_RATE
        df_prime_rates["interest_rate"] = df_prime_rates["prime_rate"] + df_prime_rates["contract_rate"]

        df_payment_due = pd.DataFrame.from_dict(dict_payment_due, orient="index").reset_index()
        df_payment_due.columns = ["payment_date", "payment_due"]        

        df = df_prime_rates
        df = df.merge(df_payment_due, on="payment_date")

        df['mortgage_balance'] = np.nan
        df['mortgage_balance'].iloc[0] = self.get_mortgage_amount()

        compound_period = constants.COMPOUND_FREQUENCY_PER_ANNUM

        df["interest_due"] = (((1+(df["interest_rate"]/100)/compound_period)**(compound_period/12))-1)*df["mortgage_balance"]

        return df

    def handle(self):
        """
        Get mortgage amoritization schedule
        """
        start_date = self.get_start_date()
        end_date = self.get_end_date(start_date, constants.NUMBER_OF_YEARS)
        dates = self.get_date_range(
            start_date, end_date, constants.PRIME_RATES_SCHEDULE
        )
        rates = self.generate_rates_schedule(dates)
        return rates

    # def get_morgage_schedule(self,loan_amount,number_of_periods,rate_schedule,tax_schedule):
    #     """
    #     Calculate mortgage based on amounts and schedules

    #     Args:
    #         loan_amount : int - total amount of the morgage loan
    #         number_of_periods : int - number of periods the schedule would be applied over
    #         rate_schedule : dict - the dates where the schedule for all the different prime rates
    #         tax_schedule : dict - the dates and amounts for all tax schedules
    #     """

    # df = pd.DataFrame.from_dict(rate_schedule, orient='index').reset_index()
    # df.columns = ['date','interest_rate']
    # df['date'].astype('datetime64')

    # df = pd.DataFrame(columns = ['date','interest_rate'])
