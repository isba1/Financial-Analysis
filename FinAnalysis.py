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
            total_revenue_historic.append(float('{:0.2e}'.format(float(year["totalRevenue"]))))
        total_revenue_historic.reverse()
        self.total_revenue_historic_array = np.array(total_revenue_historic)

        self.net_income = int(cash_flow_data["annualReports"][0]["netIncome"])

        net_income_historic = []
        for year in cash_flow_data["annualReports"]:
            net_income_historic.append(float('{:0.2e}'.format(float(year["netIncome"]))))
        net_income_historic.reverse()
        self.net_income_historic_array = np.array(net_income_historic)

        self.gross_profit = int(income_statement_data["annualReports"][0]["grossProfit"])

        gross_profit_historic = []
        for year in income_statement_data["annualReports"]:
            gross_profit_historic.append(float('{:0.2e}'.format(float(year["grossProfit"]))))
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
            debt_historic.append(float('{:0.2e}'.format(float(year["shortLongTermDebtTotal"]))))
        debt_historic.reverse()
        self.debt_historic_array = np.array(debt_historic)

        operating_cash_flow_historic = []
        for year in cash_flow_data["annualReports"]:
            operating_cash_flow_historic.append(float('{:0.2e}'.format(float(year["operatingCashflow"]))))
        operating_cash_flow_historic.reverse()
        self.operating_cash_flow_historic_array = np.array(operating_cash_flow_historic)

        total_assets_historic = []
        for year in balance_sheet_data["annualReports"]:
            total_assets_historic.append(float('{:0.2e}'.format(float(year["totalAssets"]))))
        total_assets_historic.reverse()
        self.total_assets_historic_array = np.array(total_assets_historic)


        total_liabilities_historic = []
        for year in balance_sheet_data["annualReports"]:
            total_liabilities_historic.append(float('{:0.2e}'.format(float(year["totalLiabilities"]))))
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
        fig, ax = plt.subplots()
        bars = ax.bar(x, self.total_revenue_historic_array)
        ax.set_title = "Historic Revenue"
        ax.set_xticks(x)
        ax.set_xticklabels(self.years_array, fontsize=8)
        ax.bar_label(bars, fontsize=8)
        plt.ylabel("Total Revenue ($)")
        plt.xlabel("Date")
        fig.suptitle('Historic Revenue')
        plt.show()

    def historic_net_income(self):
        # return graph rather just the list
        x = np.arange(len(self.net_income_historic_array))
        fig, ax = plt.subplots()
        bars = ax.bar(x, self.net_income_historic_array)
        ax.set_xticks(x)
        ax.set_xticklabels(self.years_array, fontsize=8)
        ax.bar_label(bars, fontsize=8)
        plt.xlabel("Date")
        plt.ylabel("Net Income ($)")
        fig.suptitle("Historic Net Income")
        plt.show()

    def historic_gross_profit(self):
        # return graph rather than just the list
        x = np.arange(len(self.gross_profit_historic_array))
        fig, ax = plt.subplots()
        bars = ax.bar(x, self.gross_profit_historic_array)
        ax.bar_label(bars, fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(self.years_array, fontsize=8)
        fig.suptitle("Historic Gross Profit")
        plt.xlabel("Date")
        plt.ylabel("Gross Profit ($)")
        plt.show()

    def EPS(self):
        return round(self.gross_profit / self.shares_outstanding, 2)

    def EPS_historic(self):
        eps_historic = []
        for item in self.gross_profit_historic_array:
            rnd = round(item / self.shares_outstanding, 2)
            eps_historic.append(rnd)
        self.eps_historic_array = np.array(eps_historic)
        # return graph instead of the array
        x = np.arange(len(self.eps_historic_array))
        fig, ax = plt.subplots()
        bars = ax.bar(x, self.eps_historic_array)
        ax.set_xticks(x)
        ax.set_xticklabels(self.years_array, fontsize=8)
        ax.bar_label(bars, fontsize=8)
        plt.xlabel("Date")
        plt.ylabel("Earnings Per Share (EPS)")
        fig.suptitle("Historic Earnings Per Share (EPS)")
        plt.show()

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
        x = np.arange(len(self.debt_historic_array))
        fig, ax = plt.subplots()
        bars = ax.bar(x, self.debt_historic_array)
        ax.bar_label(bars, fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(self.years_array, fontsize=8)
        plt.ylabel("Debt ($)")
        plt.xlabel("Date")
        fig.suptitle("Historic Debt")
        plt.show()

    def historic_cash_flow(self):
        # return graph rather than just the list
        x = np.arange(len(self.operating_cash_flow_historic_array))
        fig, ax = plt.subplots()
        bars = ax.bar(x, self.operating_cash_flow_historic_array)
        ax.bar_label(bars, fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(self.years_array, fontsize=8)
        plt.xlabel("Date")
        plt.ylabel("Operating Cash FLow ($)")
        plt.title("Historic Operating Cash Flow")
        plt.show()

    def asset_historic_vs_liabilities_historic(self):
        # return the graph of this
        x = np.arange(len(self.years_array))
        x_large = x * 10
        fig, ax = plt.subplots()
        w = 4
        rect1 = ax.bar(x_large-w/2, self.total_assets_historic_array, width=4)
        rect2 = ax.bar(x_large+w/2, self.total_liabilities_historic_array, width=4)
        #ax.bar_label(rect1, fontsize=5)
        #ax.bar_label(rect2, fontsize=5)
        ax.set_xticks([])
        ax.set_xticklabels([])
        #plt.xlabel("Date")
        plt.ylabel("$")
        # fix the legend placement using loc and bbox_to_anchor
        ax.legend([rect1, rect2], ["Assets", "Liabilities"], loc="lower left", bbox_to_anchor=(0.92, 0.92))
        fig.suptitle("Historic Assets vs Historic Liabilities")
        fig.tight_layout()
        plt.table(cellText=[self.total_assets_historic_array, self.total_liabilities_historic_array],
                  colLabels=self.years_array,
                  rowLabels=("Historic Assets", "Historic Liabilites"),
                  rowColours=("lightsteelblue", "bisque"))
        plt.show()

    def rh_vs_gp_vs_ni(self):
        x = np.arange(len(self.years_array))
        fig, ax = plt.subplots()
        ax.bar(self.years_array, self.net_income_historic_array, label="Historic Net Income")
        ax.bar(self.years_array, self.gross_profit_historic_array, label="Historic Gross Profit", bottom=self.net_income_historic_array)
        ax.bar(self.years_array, self.total_revenue_historic_array, label="Historic Revenue", bottom=self.gross_profit_historic_array)
        ax.legend(loc="lower left", bbox_to_anchor=(0.92, 0.92))
        ax.set_xticks("")
        ax.set_xticklabels([])
        #plt.xlabel("Date")
        plt.ylabel("$")
        plt.title("Historic Revenue vs Gross Profit vs Net Income")
        plt.table(cellText=[self.total_revenue_historic_array, self.gross_profit_historic_array,
                            self.net_income_historic_array],
                  rowLabels=("Historic Revenue", "Historic Gross Profit", "Historic Net Income"), loc="bottom",
                  colLabels=self.years_array, rowColours=("yellowgreen", "bisque", "lightsteelblue")
                  )
        plt.show()

    #def rh_gp_ni_table(self):









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
#FA.revenue_historic()
#FA.historic_net_income()
#FA.historic_gross_profit()
#FA.EPS_historic()
#FA.historic_debt()
FA.historic_cash_flow()
#FA.asset_historic_vs_liabilities_historic()
#FA.rh_vs_gp_vs_ni()
#FA.rh_vs_gp_vs_ni()