from code_playground.finance_transactions.src.finance_mortgage import MortgageService

# generate morgage schedule
mortgage = MortgageService()

# result = mortgage.get_mortgage_amount()
result = mortgage.handle()
print(result)
