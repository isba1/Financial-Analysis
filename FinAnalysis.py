import numpy as np
import matplotlib.pyplot as plt
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

        total_revenue_historic = []
        for year in income_statement_data["annualReports"]:
            total_revenue_historic.append(int(year["totalRevenue"]))
        total_revenue_historic.reverse()
        self.total_revenue_historic_array = np.array(total_revenue_historic)

        self.net_income = int(cash_flow_data["annualReports"][0]["netIncome"])

        net_income_historic = []
        for year in cash_flow_data["annualReports"]:
            net_income_historic.append(int(year["netIncome"]))
        net_income_historic.reverse()
        self.net_income_historic_array = np.array(net_income_historic)

        self.gross_profit = int(income_statement_data["annualReports"][0]["grossProfit"])

        gross_profit_historic = []
        for year in income_statement_data["annualReports"]:
            gross_profit_historic.append(int(year["grossProfit"]))
        gross_profit_historic.reverse()
        self.gross_profit_historic_array = np.array(gross_profit_historic)

        self.eps_historic_array = []

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

        debt_historic = []
        for year in balance_sheet_data["annualReports"]:
            debt_historic.append(int(year["shortLongTermDebtTotal"]))
        debt_historic.reverse()
        self.debt_historic_array = np.array(debt_historic)

        operating_cash_flow_historic = []
        for year in cash_flow_data["annualReports"]:
            operating_cash_flow_historic.append(int(year["operatingCashflow"]))
        operating_cash_flow_historic.reverse()
        self.operating_cash_flow_historic_array = np.array(operating_cash_flow_historic)

        total_assets_historic = []
        for year in balance_sheet_data["annualReports"]:
            total_assets_historic.append(int(year["totalAssets"]))
        total_assets_historic.reverse()
        self.total_assets_historic_array = np.array(total_assets_historic)


        total_liabilities_historic = []
        for year in balance_sheet_data["annualReports"]:
            total_liabilities_historic.append(int(year["totalLiabilities"]))
        total_liabilities_historic.reverse()
        self.total_liabilities_historic_array = np.array(total_liabilities_historic)


        years = []
        for year in balance_sheet_data["annualReports"]:
            years.append(year["fiscalDateEnding"])
        years.reverse()
        self.years_array = np.array(years)


    def current_ratio(self):
        return self.total_assets / self.total_liabilities

    def working_capital(self):
        return self.total_assets - self.total_liabilities

    def debt_equity_ratio(self):
        return self.total_liabilities / self.total_shareholder_equity

    def revenue_historic(self):
        x = np.arange(len(self.total_revenue_historic_array))
        #y = np.linspace(0, np.amax(self.total_revenue_historic_array) + 100000000, 8)
        fig, ax = plt.subplots()
        bars = ax.bar(x, self.total_revenue_historic_array)
        ax.set_title = "Historic Revenue"
        ax.set_xticks(x)
        ax.set_xticklabels(self.years_array)
        #ax.set_yticks(y)
        #ax.set_yticklabels(y)
        ax.bar_label(bars)
        plt.ylabel("Total Revenue ($)")
        plt.xlabel("Date")
        plt.show()

    def historic_net_income(self):
        # return graph rather just the list
        return self.net_income_historic_array

    def historic_gross_profit(self):
        # return graph rather than just the list
        return self.gross_profit_historic_array

    def EPS(self):
        return self.gross_profit / self.shares_outstanding

    def EPS_historic(self):
        eps_historic = []
        for item in self.gross_profit_historic_array:
            eps_historic.append(item / self.shares_outstanding)
        self.eps_historic_array = np.array(eps_historic)
        # return graph instead of the array
        return self.eps_historic_array

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
        # return graph rather than just the list
        return self.debt_historic_array

    def historic_cash_flow(self):
        # return graph rather than just the list
        return self.operating_cash_flow_historic_array

    #def asset_historic_vs_liabilities_historic(self):
        # return the graph of this









FA = Financial_Analysis("IBM")
""""
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
print(f"Historic Cash Flow: {FA.historic_cash_flow()}")
print(f"Historic Debt: {FA.historic_debt()}")
"""
FA.revenue_historic()

