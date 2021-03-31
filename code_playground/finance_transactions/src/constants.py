class MortgageConfig:

    SCHEDULE_COLUMNS = ["date", "interest_rate", "payment_principal", "balance"]
    LOAN_DATE = "2017-04-27"
    HOME_VALUE_AMOUNT = 360050
    NUMBER_OF_YEARS = 25
    INITIAL_TERM = 5
    COMPOUND_FREQUENCY_PER_ANNUM = 2 # semi-annual compound frequency
    PERSONAL_CONTRACT_RATE = -0.85 # prime minus personal contract rate is the mortgage interest rate

    # could be scraped from Bank of Canada website
    PRIME_RATES_SCHEDULE = {"2017-04-27": 2.70, "2020-04-01": 0.75}
    PAYMENT_DUE_SCHEDULE = {"2017-04-27": "1,554.10"}
    TAX_SCHEDULE = {"2017-04-27": "269", "2020-04-01": "235"}


