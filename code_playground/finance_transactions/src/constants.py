class MortgageConfig:

    SCHEDULE_COLUMNS = ["date", "interest_rate", "payment_principal", "balance"]
    LOAN_DATE = "2017-04-27"
    LOAN_AMOUNT = 360050
    NUMBER_OF_YEARS = 25
    PERSONAL_CONTRACT_RATE = -0.85

    # could be scraped from Bank of Canada website
    PRIME_RATES_SCHEDULE = {"2017-04-27": 1.80, "2020-04-01": 0.75}
    TAX_SCHEDULE = {"2017-04-27": "269", "2020-04-01": "235"}
