import json
import numpy as np
import matplotlib.pyplot as plt
import requests


class Financial_Analysis:
    def __init__(self, symbol):

        self.symbol = symbol
        url_price_daily = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&apikey=KJHOTYX4RQYVFABB"
        url_income_statement = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={self.symbol}&apikey=KJHOTYX4RQYVFABB"
        url_balance_sheet = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={self.symbol}&apikey=KJHOTYX4RQYVFABB"
        url_cash_flow = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={self.symbol}&apikey=KJHOTYX4RQYVFABB"
        url_price_monthly = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={self.symbol}&apikey=KJHOTYX4RQYVFABB"

        income_statement = requests.get(url_income_statement)
        balance_sheet = requests.get(url_balance_sheet)
        cash_flow = requests.get(url_cash_flow)
        price_daily = requests.get(url_price_daily)
        price_monthly = requests.get(url_price_monthly)

        income_statement_data = income_statement.json()
        balance_sheet_data = balance_sheet.json()
        cash_flow_data = cash_flow.json()
        price_data_daily = price_daily.json()
        price_data_monthly = price_monthly.json()

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

        price_as_list = list(price_data_daily["Time Series (Daily)"])
        current_day = price_as_list[0]
        self.final_closing_price = float(price_data_daily["Time Series (Daily)"][current_day]["4. close"])




        # current monthly closing price
        price_as_list_month = list(price_data_monthly["Monthly Time Series"])
        current_month = price_as_list_month[0]
        self.monthly_closing_price = float(price_data_monthly["Monthly Time Series"][current_month]["4. close"])

        # five ytd monthly closing price
        five_ytd = price_as_list_month[60]
        self.monthly_closing_price_five_ytd = float(price_data_monthly["Monthly Time Series"][five_ytd]["4. close"])

        self.five_ytd_shares_outstanding = float(balance_sheet_data["annualReports"][4]["commonStockSharesOutstanding"])









        '''
        # API doesn't have data for prices going that far
        current_day_year = int(current_day[0:4])
        print(current_day_year)
        current_day_date = current_day[4:10]
        print(current_day_date)
        print(f"{current_day_year - 1}{current_day_date}")
        ytd_final_closing_price = []
        for i in range(0, 5):
            ytd_final_closing_price.append(float(price_data_daily["Time Series (Daily)"][f"{current_day_year - 1}{current_day_date}"]["4. close"]))
        ytd_final_closing_price.reverse()
        self.ytd_fin_close_price = ytd_final_closing_price
        '''

        self.EBITDA_data = int(income_statement_data["annualReports"][0]["ebitda"])

        self.current_debt = int(balance_sheet_data["annualReports"][0]["currentDebt"])

        self.investments = int(balance_sheet_data["annualReports"][0]["investments"])

        self.cash_cash_equivalents = int(
            balance_sheet_data["annualReports"][0]["cashAndCashEquivalentsAtCarryingValue"])

        debt_historic = []
        for year in balance_sheet_data["annualReports"]:
            if year["shortLongTermDebtTotal"] == "None":
                debt_historic.append(0)
            else:
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

        if cash_flow_data["annualReports"][0]["dividendPayout"] == "None":
            self.dividend_payout = 0
        else:
            self.dividend_payout = int(cash_flow_data["annualReports"][0]["dividendPayout"])

        '''
        Don't end up using this
        dividend_payout_historic = []
        for year in cash_flow_data["annualReports"]:
            if year["dividendPayout"] == "None":
                dividend_payout_historic.append(0)
            else:
                dividend_payout_historic.append(float(year["dividendPayout"]))
        dividend_payout_historic.reverse()
        self.dividend_payout_historic_array = dividend_payout_historic
        '''

        # self.dividend_payout_ratio_historic = []


        self.ROE_historic_array = []
        self.historic_free_cash_flow = []

        if cash_flow_data["annualReports"][0]["dividendPayoutPreferredStock"] == "None":
            self.dividend_payout_preferred = 0
        else:
            self.dividend_payout_preferred = cash_flow_data["annualReports"][0]["dividendPayoutPreferredStock"]

        dividend_payout_preferred_historic = []
        for year in cash_flow_data["annualReports"]:
            if year["dividendPayoutPreferredStock"] == "None":
                dividend_payout_preferred_historic.append(0)
            else:
                dividend_payout_preferred_historic.append(float(year["dividendPayoutPreferredStock"]))
        dividend_payout_preferred_historic.reverse()
        self.dividend_payout_preferred_historic_array = np.array(dividend_payout_preferred_historic)

        '''
        shares_outstanding_historic = []
        for year in balance_sheet_data["annualReports"]:
            shares_outstanding_historic.append(float(year["commonStockSharesOutstanding"]))
        shares_outstanding_historic.reverse()
        self.shares_outstanding_historic_array = shares_outstanding_historic
        '''

        years = []
        for year in balance_sheet_data["annualReports"]:
            years.append(year["fiscalDateEnding"])
        years.reverse()
        self.years_array = np.array(years)

        self.PE_ratio_rank = 0
        self.EPS_past_rank = 0
        self.EPS_current_rank = 0
        self.ROE_past_rank = 0
        self.ROE_current_rank = 0
        self.FCF_past_rank = 0
        self.FCF_current_rank = 0
        self.current_ratio_rank = 0
        self.dte_rank = 0
        self.ptb_rank = 0
        self.pts_rank = 0
        self.dividend_payout_ratio_rank = 0
        self.dividend_yield_rank = 0
        self.avg_rank = 0
        self.compare = []

    def current_ratio(self):
        return self.total_assets / self.total_liabilities

    def working_capital(self):
        return self.total_assets - self.total_liabilities

    def debt_equity_ratio(self):
        return self.total_liabilities / self.total_shareholder_equity

    def price_to_sales(self):
        return self.final_closing_price / self.total_revenue_current

    def dividend_payout_ratio(self):
        return self.dividend_payout / self.net_income

    def dividend_yield_ratio(self):
        return (self.dividend_payout / self.shares_outstanding) / self.final_closing_price

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
        return round(((self.net_income - self.dividend_payout_preferred) / self.shares_outstanding), 2)

    def EPS_historic(self):
        eps_historic = []

        # calculates EPS for each year
        for i in range(0, len(self.net_income_historic_array)):
            eps_historic.append((self.net_income_historic_array[i] - self.dividend_payout_preferred_historic_array[
                i]) / self.shares_outstanding)
            # eps_historic.append(rnd)
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
            self.historic_free_cash_flow.append(float('{:0.2e}'.format(
                self.operating_cash_flow_historic_array[i] - self.capital_expenditures_historic_array[i])))

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

    def price_to_book_ratio(self):
        return self.final_closing_price / self.BVPS()

    def PE_ratio(self):
        return self.final_closing_price / self.EPS()

    def EBITDA(self):
        return self.EBITDA_data

    def enterprice_value(self):
        return (self.final_closing_price * self.shares_outstanding) + self.current_debt - self.investments - self.cash_cash_equivalents

    def return_on_equity(self):
        return self.net_income / self.total_shareholder_equity

    def return_on_equity_historic(self):
        # creates an array of historic ROE
        for i in range(0, len(self.net_income_historic_array)):
            self.ROE_historic_array.append(
                self.net_income_historic_array[i] / self.total_shareholder_equity_historic_array[i])

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


    """
    I actually don't want to use historic dividend payout
    def dividend_payout_ratio_historic(self):
        # determines the values of the historic dividend payout ratio
        for i in range(0, len(self.dividend_payout_historic_array)):
            self.dividend_payout_ratio_historic.append(self.dividend_payout_historic_array[i] / self.net_income_historic_array[i])
        return self.dividend_payout_ratio_historic
    """

    def pe_ratio_rank(self):
        # determines rank of PE ratio
        if self.PE_ratio() <= 15:
            self.PE_ratio_rank = 5
        elif 15 < self.PE_ratio() <= 20:
            self.PE_ratio_rank = 4
        elif 20 < self.PE_ratio() <= 25:
            self.PE_ratio_rank = 3
        elif 25 < self.PE_ratio() <= 30:
            self.PE_ratio_rank = 2
        elif 30 < self.PE_ratio():
            self.PE_ratio_rank = 1
        return self.PE_ratio_rank

    def EPS_rank_past(self):
        # this defines average EPS rate of change over the last 5 years
        yearly_rates_of_change_sum = 0
        for i in range(0, len(self.eps_historic_array) - 1):
            yearly_rates_of_change_sum += ((self.eps_historic_array[i + 1] - self.eps_historic_array[i]) /
                                           self.eps_historic_array[i]) * 100
        avg_eps_roc_past = yearly_rates_of_change_sum / 4

        # determines the rank of the EPS growth over past 5 years
        if avg_eps_roc_past <= 3:
            self.EPS_past_rank = 1
        elif 3 < avg_eps_roc_past <= 7:
            self.EPS_past_rank = 2
        elif 7 < avg_eps_roc_past <= 11:
            self.EPS_past_rank = 3
        elif 11 < avg_eps_roc_past <= 14:
            self.EPS_past_rank = 4
        elif avg_eps_roc_past >= 15:
            self.EPS_past_rank = 5
        return self.EPS_past_rank

    def EPS_rank_current(self):
        # determines most recent growth in EPS compared to average EPS over last four years
        past_four_year_sum = 0
        for i in self.eps_historic_array[0:3]:
            past_four_year_sum += i
        past_four_year_avg = past_four_year_sum / 4
        EPS_cur_growth = ((self.eps_historic_array[4] - past_four_year_avg) / past_four_year_avg) * 100

        # determines rank of the recent growth compared to average EPS over last four years
        if EPS_cur_growth <= 3:
            self.EPS_current_rank = 1
        elif 3 < EPS_cur_growth <= 7:
            self.EPS_current_rank = 2
        elif 7 < EPS_cur_growth <= 11:
            self.EPS_current_rank = 3
        elif 11 < EPS_cur_growth <= 14:
            self.EPS_current_rank = 4
        elif EPS_cur_growth >= 15:
            self.EPS_current_rank = 5
        return self.EPS_current_rank

    def ROE_rank_past(self):
        # this defines ROE growth over past 5 years
        yearly_rates_of_change_sum = 0
        for i in range(0, len(self.ROE_historic_array) - 1):
            yearly_rates_of_change_sum += ((self.ROE_historic_array[i + 1] - self.ROE_historic_array[i]) /
                                           self.ROE_historic_array[i]) * 100
        avg_ROE_roc = yearly_rates_of_change_sum / 4

        # this determines rank ROE growth over past 5 years
        if avg_ROE_roc <= 5:
            self.ROE_past_rank = 1
        elif 5 < avg_ROE_roc <= 10:
            self.ROE_past_rank = 2
        elif 10 < avg_ROE_roc <= 14:
            self.ROE_past_rank = 3
        elif 14 < avg_ROE_roc <= 17:
            self.ROE_past_rank = 4
        elif 17 < avg_ROE_roc:
            self.ROE_past_rank = 5
        return self.ROE_past_rank

    def ROE_rank_current(self):
        # get average ROE over last 4 years
        four_year_sum = 0
        for i in self.ROE_historic_array[0:3]:
            four_year_sum += i
        four_year_avg = four_year_sum / 4

        # calculates current growth compared to last 4 year average
        ROE_cur_growth = ((self.ROE_historic_array[4] - four_year_avg) / four_year_avg) * 100

        # determines rank of ROE
        if ROE_cur_growth <= 5:
            self.ROE_current_rank = 1
        elif 5 < ROE_cur_growth <= 10:
            self.ROE_current_rank = 2
        elif 10 < ROE_cur_growth <= 14:
            self.ROE_current_rank = 3
        elif 14 < ROE_cur_growth <= 17:
            self.ROE_current_rank = 4
        elif 17 < ROE_cur_growth:
            self.ROE_current_rank = 5
        return self.ROE_current_rank

    def free_cash_rank_current(self):
        # determines four year avg of FCF
        four_year_sum = 0
        for i in self.historic_free_cash_flow[0:3]:
            four_year_sum += i
        four_year_avg = four_year_sum / 4

        # determinges current rate of change
        current_roc = ((self.historic_free_cash_flow[4] - four_year_avg) / four_year_avg) * 100

        # determines current rank of FCF
        if current_roc <= 5:
            self.FCF_current_rank = 1
        elif 5 < current_roc <= 10:
            self.FCF_current_rank = 2
        elif 10 < current_roc <= 15:
            self.FCF_current_rank = 3
        elif 15 < current_roc <= 20:
            self.FCF_current_rank = 4
        elif 20 < current_roc:
            self.FCF_current_rank = 5
        return self.FCF_current_rank

    def free_cash_rank_past(self):
        # determines average rate of change over last five years
        yearly_rates_of_change_sum = 0
        for i in range(0, len(self.historic_free_cash_flow) - 1):
            yearly_rates_of_change_sum += ((self.historic_free_cash_flow[i + 1] - self.historic_free_cash_flow[i]) /
                                           self.historic_free_cash_flow[i]) * 100
        avg_roc = yearly_rates_of_change_sum / 4

        if avg_roc <= 5:
            self.FCF_past_rank = 1
        elif 5 < avg_roc <= 10:
            self.FCF_past_rank = 2
        elif 10 < avg_roc <= 15:
            self.FCF_past_rank = 3
        elif 15 < avg_roc <= 20:
            self.FCF_past_rank = 4
        elif 20 < avg_roc:
            self.FCF_past_rank = 5
        return self.FCF_past_rank

    def rank_current_ratio(self):
        if self.current_ratio() <= 0.5:
            self.current_ratio_rank = 1
        elif 0.5 < self.current_ratio() <= 1:
            self.current_ratio_rank = 2
        elif 1 < self.current_ratio() <= 1.2:
            self.current_ratio_rank = 3
        elif 1.2 < self.current_ratio() <= 1.5:
            self.current_ratio_rank = 4
        elif 1.5 < self.current_ratio():
            self.current_ratio_rank = 5
        return self.current_ratio_rank

    def debt_to_equity_rank(self):
        if self.debt_equity_ratio() >= 2:
            self.dte_rank = 1
        elif 1.5 <= self.debt_equity_ratio() < 2:
            self.dte_rank = 2
        elif 1 <= self.debt_equity_ratio() < 1.5:
            self.dte_rank = 3
        elif 0.8 <= self.debt_equity_ratio() < 1:
            self.dte_rank = 4
        elif self.debt_equity_ratio() < 0.8:
            self.dte_rank = 5
        return self.dte_rank

    def price_to_book_rank(self):
        if self.price_to_book_ratio() <= 1:
            self.ptb_rank = 5
        elif 1 < self.price_to_book_ratio() <= 3:
            self.ptb_rank = 4
        elif 3 < self.price_to_book_ratio() <= 5:
            self.ptb_rank = 3
        elif 5 < self.price_to_book_ratio() <= 7:
            self.ptb_rank = 2
        elif 7 < self.price_to_book_ratio():
            self.ptb_rank = 1
        return self.ptb_rank

    def price_to_sales_rank(self):
        if self.price_to_sales() <= 1:
            self.pts_rank = 5
        elif 1 < self.price_to_sales() <= 2:
            self.pts_rank = 4
        elif 2 < self.price_to_sales() <= 3:
            self.pts_rank = 3
        elif 3 < self.price_to_sales() <= 4:
            self.pts_rank = 2
        elif 4 < self.price_to_sales():
            self.pts_rank = 1
        return self.pts_rank

    def ratio_dividend_payout_rank(self):
        if 30 <= self.dividend_payout_ratio() <= 50:
            self.dividend_payout_ratio_rank = 5
        elif (50 < self.dividend_payout_ratio() <= 55) or (25 <= self.dividend_payout_ratio() < 30):
            self.dividend_payout_ratio_rank = 4
        elif (55 < self.dividend_payout_ratio() <= 60) or (20 <= self.dividend_payout_ratio() < 25):
            self.dividend_payout_ratio_rank = 3
        elif (60 < self.dividend_payout_ratio() <= 65) or (15 <= self.dividend_payout_ratio() < 20):
            self.dividend_payout_ratio_rank = 2
        elif (65 < self.dividend_payout_ratio()) or (self.dividend_payout_ratio() < 15):
            self.dividend_payout_ratio_rank = 1
        return self.dividend_payout_ratio_rank

    def rank_dividend_yield_ratio(self):
        if 6 <= self.dividend_yield_ratio():
            self.dividend_yield_rank = 5
        elif 4 <= self.dividend_yield_ratio() < 6:
            self.dividend_yield_rank = 4
        elif 2 <= self.dividend_yield_ratio() < 4:
            self.dividend_yield_rank = 3
        elif 1 <= self.dividend_yield_ratio() < 2:
            self.dividend_yield_rank = 2
        elif self.dividend_yield_ratio() < 1:
            self.dividend_yield_rank = 1
        return self.dividend_yield_rank

    def total_rank(self):
        total_rank_sum = self.ratio_dividend_payout_rank() + self.price_to_sales_rank() + self.price_to_book_rank() + self.debt_to_equity_rank() + self.rank_current_ratio() + self.free_cash_rank_current() + self.free_cash_rank_past() + self.ROE_rank_past() + self.ROE_rank_current() + self.EPS_rank_current() + self.EPS_rank_past() + self.pe_ratio_rank() + self.rank_dividend_yield_ratio()
        self.avg_rank = total_rank_sum / 13
        return round(self.avg_rank, 4)

    def five_ytd_change(self):
        # returns five ytd percent change in stock price
        market_cap_past = self.monthly_closing_price_five_ytd * self.five_ytd_shares_outstanding
        market_cap_current = self.final_closing_price * self.shares_outstanding
        return round((((market_cap_current - market_cap_past) / market_cap_past) * 100), 4)

    def compare_rank_return(self):
        # compare total rank to annual return
        self.compare.append(self.symbol)
        self.compare.append(self.total_rank())
        self.compare.append(self.five_ytd_change())
        return self.compare


class Sector_Analysis_XLE:
    def __init__(self):
        self.tickerListXLE = ["XOM", "CVX", "EOG", "COP", "SLB"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/XOMJson/XOMbalance.json",
                'r') as f:
            self.XOM_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CVXJson/CVXbalance.json",
                'r') as f:
            self.CVX_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/EOGJson/EOGbalance.json",
                'r') as f:
            self.EOG_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/COPJson/COPbalance.json",
                'r') as f:
            self.COP_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/SLBJson/SLBbalance.json",
                'r') as f:
            self.SLB_balance_sheet = json.load(f)


        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/XOMJson/XOMcash.json",
                'r') as f:
            self.XOM_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CVXJson/CVXcash.json",
                'r') as f:
            self.CVX_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/EOGJson/EOGcash.json",
                'r') as f:
            self.EOG_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/COPJson/COPcash.json",
                'r') as f:
            self.COP_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/SLBJson/SLBcash.json",
                'r') as f:
            self.SLB_cash_sheet = json.load(f)


        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/XOMJson/XOMincome.json",
                'r') as f:
            self.XOM_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CVXJson/CVXincome.json",
                'r') as f:
            self.CVX_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/EOGJson/EOGincome.json",
                'r') as f:
            self.EOG_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/COPJson/COPincome.json",
                'r') as f:
            self.COP_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/SLBJson/SLBincome.json",
                'r') as f:
            self.SLB_income_sheet = json.load(f)


    # function for XLE ticker's BVPS
    def BVPS_XLE(self):

        # dictionary that returns BVPS for each ticker
        BVPS_XLE_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLE_dict["XOM"] = round((float(self.XOM_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(self.XOM_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLE_dict["CVX"] = round((float(self.CVX_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(self.CVX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLE_dict["EOG"] = round((float(self.EOG_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(self.EOG_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        # for some reason COP shares outstanding in most recent years were negative, and I'm assuming it's a glitch in
        # the API, so I just used the most recent year with a positive shares outstanding value
        BVPS_XLE_dict["COP"] = round((float(self.COP_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(self.COP_balance_sheet["annualReports"][2]["commonStockSharesOutstanding"])), 3)
        BVPS_XLE_dict["SLB"] = round((float(self.SLB_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(self.SLB_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLE_dict

    # EPS for XLE tickers
    def EPS_XLE(self):

        # dictionary that returns the EPS for each ticker
        EPS_XLE_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLE_dict["XOM"] = round((float(self.XOM_income_sheet["annualReports"][0]["grossProfit"]) / float(self.XOM_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLE_dict["CVX"] = round((float(self.CVX_income_sheet["annualReports"][0]["grossProfit"]) / float(self.CVX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLE_dict["EOG"] = round((float(self.EOG_income_sheet["annualReports"][0]["grossProfit"]) / float(self.EOG_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        # for some reason COP shares outstanding in most recent years were negative, and I'm assuming it's a glitch in
        # the API, so I just used the most recent year with a positive shares outstanding value
        EPS_XLE_dict["COP"] = round((float(self.COP_income_sheet["annualReports"][0]["grossProfit"]) / float(self.COP_balance_sheet["annualReports"][2]["commonStockSharesOutstanding"])), 3)
        EPS_XLE_dict["SLB"] = round((float(self.SLB_income_sheet["annualReports"][0]["grossProfit"]) / float(self.SLB_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLE_dict

    # debt to equity for XLE tickers
    def debt_equity_XLE(self):

        # dictionary that contains tickers' debt to equity ratios
        DE_XLE_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLE_dict["XOM"] = round(((float(self.XOM_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(self.XOM_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLE_dict["CVX"] = round(((float(self.CVX_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(self.CVX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLE_dict["EOG"] = round(((float(self.EOG_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(self.EOG_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLE_dict["COP"] = round(((float(self.COP_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(self.COP_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLE_dict["SLB"] = round(((float(self.SLB_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(self.SLB_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLE_dict


    # ROE for XLE tickers
    def ROE_XLE(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLE_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLE_dict["XOM"] = round((float(self.XOM_cash_sheet["annualReports"][0]["netIncome"]) / float(self.XOM_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLE_dict["CVX"] = round((float(self.CVX_cash_sheet["annualReports"][0]["netIncome"]) / float(self.CVX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLE_dict["EOG"] = round((float(self.EOG_cash_sheet["annualReports"][0]["netIncome"]) / float(self.EOG_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLE_dict["COP"] = round((float(self.COP_cash_sheet["annualReports"][0]["netIncome"]) / float(self.COP_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLE_dict["SLB"] = round((float(self.SLB_cash_sheet["annualReports"][0]["netIncome"]) / float(self.SLB_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLE_dict


    # free cash flow for XLE tickers
    def free_cash_XLE(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLE_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLE_dict["XOM"] = (float(self.XOM_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(self.XOM_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLE_dict["CVX"] = (float(self.CVX_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(self.CVX_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLE_dict["EOG"] = (float(self.EOG_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(self.EOG_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLE_dict["COP"] = (float(self.COP_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(self.COP_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLE_dict["SLB"] = (float(self.SLB_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(self.SLB_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLE_dict

XLE = Sector_Analysis_XLE()
print(XLE.BVPS_XLE())
print(XLE.EPS_XLE())
print(XLE.debt_equity_XLE())
print(XLE.ROE_XLE())
print(XLE.free_cash_XLE())

class Sector_Analysis_XLB:
    def __init__(self):
        self.tickerListXLB = ["LIN", "FCX", "NEM", "SHW", "APD"]



class Sector_Analysis_XLI:
    def __init__(self):
        self.tickerListXLI = ["HON", "UPS", "UNP", "BA", "RTX"]


class Sector_Analysis_XLY:
    def __init__(self):
        self.tickerListXLY = ["AMZN", "TSLA", "HD", "NKE", "MCD"]


class Sector_Analysis_XLP:
    def __init__(self):
        self.tickerListXLP = ["PG", "KO", "PEP", "WMT", "COST"]


class Sector_Analysis_XLV:
    def __init__(self):
        self.tickerListXLV = ["UNH", "JNJ", "PFE", "ABBV", "TMO"]



class Sector_Analysis_XLF:
    def __init__(self):
        self.tickerListXLF = ["JPM", "BAC", "WFC", "C", "MS"]


class Sector_Analysis_XLU:
    def __init__(self):
        self.tickerListXLU = ["NEE", "DUK", "SO", "D", "EXC"]


class Sector_Analysis_XLK:
    def __init__(self):
        self.tickerListXLK = ["AAPL", "MSFT", "NVDA", "V", "MA"]


class Sector_Analysis_XLC:
    def __init__(self):
        self.tickerListXLC = ["FB", "GOOGL", "NFLX", "DIS", "CMCSA"]


class Sector_Analysis_XLRE:
    def __init__(self):
        self.tickerListXlRE = ["AMT", "PLD", "CCI", "EQIX", "PSA"]








"""
FA = Financial_Analysis("AAPL")
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

"""
FA.current_ratio()
FA.working_capital()
FA.debt_equity_ratio()
FA.price_to_sales()
FA.dividend_payout_ratio()
FA.dividend_yield_ratio()
FA.revenue_historic()
FA.historic_net_income()
FA.historic_gross_profit()
FA.EPS()
FA.EPS_historic()
FA.free_cash_flow()
FA.free_cash_flow_historic()
FA.BVPS()
FA.price_to_book_ratio()
FA.PE_ratio()
FA.EBITDA()
FA.enterprice_value()
FA.return_on_equity()
FA.return_on_equity_historic()
FA.historic_debt()
FA.historic_cash_flow()
FA.asset_historic_vs_liabilities_historic()
FA.rh_vs_gp_vs_ni()
FA.pe_ratio_rank()
FA.EPS_rank_past()
FA.EPS_rank_current()
FA.ROE_rank_past()
FA.ROE_rank_current()
FA.free_cash_rank_past()
FA.free_cash_rank_current()
FA.rank_current_ratio()
FA.debt_to_equity_rank()
FA.price_to_book_rank()
FA.price_to_sales_rank()
FA.ratio_dividend_payout_rank()
FA.rank_dividend_yield_ratio()
FA.total_rank()
print(FA.five_ytd_change())
print(FA.compare_rank_return())
"""


'''
# Ended up requesting the API too many times so I can't us inheritance
class Rank(Financial_Analysis):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.PE_ratio_rank = 0

    def pe_rank(self):
        # self.PE_ratio_rank = 0
        if super().PE_ratio() <= 15:
            self.PE_ratio_rank = 5
        elif 15 < super().PE_ratio() <= 20:
            self.PE_ratio_rank = 4
        elif 20 < super().PE_ratio() <= 25:
            self.PE_ratio_rank = 3
        elif 25 < super().PE_ratio() <= 30:
            self.PE_ratio_rank = 2
        elif 30 < super().PE_ratio():
            self.PE_ratio_rank = 1
        return self.PE_ratio_rank


r = Rank("IBM")
print(r.pe_rank())
'''
