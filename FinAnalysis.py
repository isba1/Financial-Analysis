
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

        income_statement_data = income_statement.json()
        balance_sheet_data = balance_sheet.json()
        cash_flow_data = cash_flow.json()
        price_data = price.json()

        self.total_assets = int(balance_sheet_data["annualReports"][0]["totalAssets"])
        self.total_liabilities = int(balance_sheet_data["annualReports"][0]["totalLiabilities"])
        self.total_shareholder_equity = int(balance_sheet_data["annualReports"][0]["totalShareholderEquity"])
        self.total_revenue_current = int(income_statement_data["annualReports"][0]["totalRevenue"])

        self.total_revenue_historic = []
        for year in income_statement_data["annualReports"]:
            self.total_revenue_historic.append(int(year["totalRevenue"]))

        self.net_income = int(cash_flow_data["annualReports"][0]["netIncome"])

        self.net_income_historic = []
        for year in cash_flow_data["annualReports"]:
            self.net_income_historic.append(int(year["netIncome"]))

        self.gross_profit = int(income_statement_data["annualReports"][0]["grossProfit"])

        self.gross_profit_historic = []
        for year in income_statement_data["annualReports"]:
            self.gross_profit_historic.append(int(year["grossProfit"]))

        self.eps_historic = []

        self.shares_outstanding = int(balance_sheet_data["annualReports"][0]["commonStockSharesOutstanding"])

        self.operating_cash_flow = int(cash_flow_data["annualReports"][0]["operatingCashflow"])
        self.capital_expenditures = int(cash_flow_data["annualReports"][0]["capitalExpenditures"])

        price_as_list = list(price_data["Time Series (Daily)"])
        current_day = price_as_list[0]
        self.final_closing_price = float(price_data["Time Series (Daily)"][current_day]["4. close"])

        self.EBITDA_data = int(income_statement_data["annualReports"][0]["ebitda"])

        self.current_debt = int(balance_sheet_data["annualReports"][0]["currentDebt"])

        self.investments = int(balance_sheet_data["annualReports"][0]["investments"])

        self.cash_cash_equivalents = int(balance_sheet_data["annualReports"][0]["cashAndCashEquivalentsAtCarryingValue"])

        self.debt_historic = []
        for year in balance_sheet_data["annualReports"]:
            self.debt_historic.append(int(year["currentDebt"]))

        self.operating_cash_flow_historic = []
        for year in cash_flow_data["annualReports"]:
            self.operating_cash_flow_historic.append(int(year["operatingCashflow"]))


    def current_ratio(self):
        return self.total_assets / self.total_liabilities

    def working_capital(self):
        return self.total_assets - self.total_liabilities

    def debt_equity_ratio(self):
        return self.total_liabilities / self.total_shareholder_equity

    def revenue_historic(self):
        return self.total_revenue_historic

    def historic_net_income(self):
        return self.net_income_historic

    def historic_gross_profit(self):
        return self.gross_profit_historic

    def EPS(self):
        return self.gross_profit / self.shares_outstanding

    def EPS_historic(self):
        for item in self.gross_profit_historic:
            self.eps_historic.append(item / self.shares_outstanding)
        return self.eps_historic

    def free_cash_flow(self):
        return self.operating_cash_flow - self.capital_expenditures

    def BVPS(self):
        return self.total_shareholder_equity / self.shares_outstanding

    def PE_ratio(self):
        return self.final_closing_price / (self.gross_profit / self.shares_outstanding)

    def EBITDA(self):
        return self.EBITDA_data

    def enterprice_value(self):
        return (self.final_closing_price * self.shares_outstanding) + self.current_debt - self.investments - self.cash_cash_equivalents

    def historic_debt(self):
        return self.debt_historic

    def historic_cash_flow(self):
        return self.operating_cash_flow_historic









FA = Financial_Analysis("IBM")
print(f"Current Ratio: {FA.current_ratio()}")
print(f"Working Capital: {FA.working_capital()}")
print(f"Debt to Equity Ratio: {FA.debt_equity_ratio()}")
print(f"Historic Revenue: {FA.revenue_historic()}")
print(f"Historic Net Income: {FA.historic_net_income()}")
print(f"Historic Gross Profit: {FA.historic_gross_profit()}")
print(f"Earnings per Share: {FA.EPS()}")
print(f"Historic Earnings Per Share: {FA.EPS_historic()}")
print(f"Free Cash Flow: {FA.free_cash_flow()}")
print(f"Book Value per Share: {FA.BVPS()}")
print(f"Price to Earnings Ratio: {FA.PE_ratio()}")
print(f"EBITDA: {FA.EBITDA()}")
print(f"Enterprise Value: {FA.enterprice_value()}")
print(f"Historic Debt: {FA.historic_debt()}")
print(f"Historic Cash Flow: {FA.operating_cash_flow_historic}")