import json
import requests

class Financial_Analysis:
    def __init__(self, symbol):
        self.symbol = symbol
        url_price = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&apikey=KJHOTYX4RQYVFABB"
        url_income_statement = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.symbol}&apikey=KJHOTYX4RQYVFABB"
        url_balance_sheet = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={self.symbol}&apikey=KJHOTYX4RQYVFABB"
        url_cash_flow = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={self.symbol}&apikey=KJHOTYX4RQYVFABB"

        income_statement = requests.get(url_income_statement)
        balance_sheet = requests.get(url_balance_sheet)
        cash_flow = requests.get(url_cash_flow)
        price = requests.get(url_price)

        self.income_statement_data = income_statement.json()
        self.balance_sheet_data = balance_sheet.json()
        self.cash_flow_data = cash_flow.json()
        self.price_data = price.json()

    def current_ratio(self):



FA = Financial_Analysis("AAPl")