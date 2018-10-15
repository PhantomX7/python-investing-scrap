class Stock:
    def __init__(self, name, id, link):
        self.name = name
        self.id = id
        self.link = link
    def setBalanceSheet(self,balance_sheet):
        self.balance_sheet = balance_sheet
    def setIncomeStatement(self, income_statement):
        self.income_statement = income_statement