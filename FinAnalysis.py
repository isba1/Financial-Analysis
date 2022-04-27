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

        capital_expenditures_historic = []
        for year in cash_flow_data["annualReports"]:
            capital_expenditures_historic.append((float(year["capitalExpenditures"])))
        capital_expenditures_historic.reverse()
        self.capital_expenditures_historic_array = np.array(capital_expenditures_historic)

        price_as_list = list(price_data["Time Series (Daily)"])
        current_day = price_as_list[0]
        self.final_closing_price = float(price_data["Time Series (Daily)"][current_day]["4. close"])

        self.EBITDA_data = int(income_statement_data["annualReports"][0]["ebitda"])

        self.current_debt = int(balance_sheet_data["annualReports"][0]["currentDebt"])

        self.investments = int(balance_sheet_data["annualReports"][0]["investments"])

        self.cash_cash_equivalents = int(
            balance_sheet_data["annualReports"][0]["cashAndCashEquivalentsAtCarryingValue"])

        debt_historic = []
        for year in balance_sheet_data["annualReports"]:
            debt_historic.append(float('{:0.2e}'.format(float(year["shortLongTermDebtTotal"]))))
        debt_historic.reverse()
        self.debt_historic_array = np.array(debt_historic)

        operating_cash_flow_historic = []
        for year in cash_flow_data["annualReports"]:
            operating_cash_flow_historic.append(float(year["operatingCashflow"]))
        operating_cash_flow_historic.reverse()
        self.operating_cash_flow_historic_array = np.array(operating_cash_flow_historic)

        invest_cash_flow_historic = []
        for year in cash_flow_data["annualReports"]:
            invest_cash_flow_historic.append(float(year["cashflowFromInvestment"]))
        invest_cash_flow_historic.reverse()
        self.invest_cash_flow_historic_array = np.array(invest_cash_flow_historic)

        finance_cash_flow_historic = []
        for year in cash_flow_data["annualReports"]:
            finance_cash_flow_historic.append(float(year["cashflowFromFinancing"]))
        finance_cash_flow_historic.reverse()
        self.finance_cash_flow_historic_array = np.array(finance_cash_flow_historic)

        total_assets_historic = []
        for year in balance_sheet_data["annualReports"]:
            total_assets_historic.append(float(year["totalAssets"]))
        total_assets_historic.reverse()
        self.total_assets_historic_array = np.array(total_assets_historic)

        total_liabilities_historic = []
        for year in balance_sheet_data["annualReports"]:
            total_liabilities_historic.append(float(year["totalLiabilities"]))
        total_liabilities_historic.reverse()
        self.total_liabilities_historic_array = np.array(total_liabilities_historic)

        total_shareholder_equity_historic = []
        for year in balance_sheet_data["annualReports"]:
            total_shareholder_equity_historic.append(float(year["totalShareholderEquity"]))
        total_shareholder_equity_historic.reverse()
        self.total_shareholder_equity_historic_array = np.array(total_shareholder_equity_historic)

        self.ROE_historic_array = []
        self.historic_free_cash_flow = []

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

        # calculates EPS for each year
        for item in self.gross_profit_historic_array:
            rnd = round(item / self.shares_outstanding, 2)
            eps_historic.append(rnd)
        self.eps_historic_array = np.array(eps_historic)

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

    def free_cash_flow_historic(self):
        # gives us an array of the past years free cash flow
        for i in range(0, len(self.operating_cash_flow_historic_array)):
            self.historic_free_cash_flow.append(float('{:0.2e}'.format(self.operating_cash_flow_historic_array[i] - self.capital_expenditures_historic_array[i])))

        x = np.arange(len(self.historic_free_cash_flow))
        fig, ax = plt.subplots()
        bars = ax.bar(x, self.historic_free_cash_flow)
        ax.bar_label(bars, fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(self.years_array)
        plt.xlabel("Date")
        plt.ylabel("Free Cash Flow ($)")
        plt.title("Historic Free Cash Flow")
        plt.show()


    def BVPS(self):
        return self.total_shareholder_equity / self.shares_outstanding

    def PE_ratio(self):
        return self.final_closing_price / (self.gross_profit / self.shares_outstanding)

    def EBITDA(self):
        return self.EBITDA_data

    def enterprice_value(self):
        return (self.final_closing_price * self.shares_outstanding) + self.current_debt - self.investments - self.cash_cash_equivalents

    def return_on_equity(self):
        return self.net_income / self.total_shareholder_equity

    def return_on_equity_historic(self):
        # creates an array of historic ROE
        for i in range(0, len(self.net_income_historic_array)):
            self.ROE_historic_array.append(self.net_income_historic_array[i] / self.total_shareholder_equity_historic_array[i])

        x = np.arange(len(self.ROE_historic_array))
        fig, ax = plt.subplots()
        bars = ax.bar(x, self.ROE_historic_array)
        ax.bar_label(bars, fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(self.years_array, fontsize=8)
        plt.ylabel("ROE")
        plt.xlabel("Date")
        fig.suptitle("Historic Return on Equity (ROE)")
        plt.show()




    def historic_debt(self):
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
        x = np.arange(len(self.operating_cash_flow_historic_array))
        x_large = x * 10
        fig, ax = plt.subplots()
        w = 6
        ax.bar(x_large - ((w / 3) + 1), self.operating_cash_flow_historic_array, label="Operating Cash Flow", width=3)
        ax.bar(x_large, self.finance_cash_flow_historic_array, label="Financing Cash Flow", width=3)
        ax.bar(x_large + ((w / 3) + 1), self.invest_cash_flow_historic_array, label="Investing Cash Flow", width=3)
        ax.set_xticks([])
        ax.set_xticklabels([])
        plt.table(cellText=[self.operating_cash_flow_historic_array, self.invest_cash_flow_historic_array,
                            self.finance_cash_flow_historic_array],
                  colLabels=self.years_array,
                  rowLabels=("Operating Cash Flow", "Investing Cash Flow", "Financing Cash Flow"),
                  rowColours=("lightsteelblue", "yellowgreen", "bisque"))
        plt.legend(loc="lower left", bbox_to_anchor=(0.92, 0.92))
        plt.ylabel("Cash FLows ($)")
        fig.suptitle("Historic Cash Flows")
        plt.show()

    def asset_historic_vs_liabilities_historic(self):
        x = np.arange(len(self.years_array))
        x_large = x * 10
        fig, ax = plt.subplots()
        w = 4
        rect1 = ax.bar(x_large - w / 2, self.total_assets_historic_array, width=4)
        rect2 = ax.bar(x_large + w / 2, self.total_liabilities_historic_array, width=4)
        ax.set_xticks([])
        ax.set_xticklabels([])
        plt.ylabel("Assets/Liabilities ($)")
        ax.legend([rect1, rect2], ["Assets", "Liabilities"], loc="lower left", bbox_to_anchor=(0.92, 0.92))
        fig.suptitle("Historic Assets vs Historic Liabilities")
        fig.tight_layout()
        plt.table(cellText=[self.total_assets_historic_array, self.total_liabilities_historic_array],
                  colLabels=self.years_array,
                  rowLabels=("Assets", "Liabilites"),
                  rowColours=("lightsteelblue", "bisque"))
        plt.show()

    def rh_vs_gp_vs_ni(self):
        fig, ax = plt.subplots()
        ax.bar(self.years_array, self.net_income_historic_array, label="Net Income")
        ax.bar(self.years_array, self.gross_profit_historic_array, label="Gross Profit",
               bottom=self.net_income_historic_array)
        ax.bar(self.years_array, self.total_revenue_historic_array, label="Revenue",
               bottom=self.gross_profit_historic_array)
        ax.legend(loc="lower left", bbox_to_anchor=(0.92, 0.92))
        ax.set_xticks("")
        ax.set_xticklabels([])
        plt.ylabel("Revenue/Gross Profit/Net Income ($)")
        fig.suptitle("Historic Revenue vs Gross Profit vs Net Income")
        plt.table(cellText=[self.total_revenue_historic_array, self.gross_profit_historic_array,
                            self.net_income_historic_array],
                  rowLabels=("Revenue", "Gross Profit", "Net Income"), loc="bottom",
                  colLabels=self.years_array, rowColours=("yellowgreen", "bisque", "lightsteelblue")
                  )
        plt.show()


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
# FA.revenue_historic()
# FA.historic_net_income()
# FA.historic_gross_profit()
# FA.EPS_historic()
# FA.historic_debt()
# FA.historic_cash_flow()
# FA.asset_historic_vs_liabilities_historic()
# FA.rh_vs_gp_vs_ni()
# FA.rh_vs_gp_vs_ni()
#FA.return_on_equity_historic()
# FA.free_cash_flow_historic()