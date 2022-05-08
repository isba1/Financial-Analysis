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

        self.total_assets = float(balance_sheet_data["annualReports"][0]["totalAssets"])
        self.total_liabilities = float(balance_sheet_data["annualReports"][0]["totalLiabilities"])
        self.total_shareholder_equity = float(balance_sheet_data["annualReports"][0]["totalShareholderEquity"])
        self.total_revenue_current = float(income_statement_data["annualReports"][0]["totalRevenue"])

        total_revenue_historic = []
        for year in income_statement_data["annualReports"]:
            total_revenue_historic.append(float('{:0.2e}'.format(float(year["totalRevenue"]))))
        total_revenue_historic.reverse()
        self.total_revenue_historic_array = np.array(total_revenue_historic)

        self.net_income = float(cash_flow_data["annualReports"][0]["netIncome"])

        net_income_historic = []
        for year in cash_flow_data["annualReports"]:
            net_income_historic.append(float('{:0.2e}'.format(float(year["netIncome"]))))
        net_income_historic.reverse()
        self.net_income_historic_array = np.array(net_income_historic)

        self.gross_profit = float(income_statement_data["annualReports"][0]["grossProfit"])

        gross_profit_historic = []
        for year in income_statement_data["annualReports"]:
            gross_profit_historic.append(float('{:0.2e}'.format(float(year["grossProfit"]))))
        gross_profit_historic.reverse()
        self.gross_profit_historic_array = np.array(gross_profit_historic)

        self.eps_historic_array = []

        self.shares_outstanding = float(balance_sheet_data["annualReports"][0]["commonStockSharesOutstanding"])

        self.operating_cash_flow = float(cash_flow_data["annualReports"][0]["operatingCashflow"])
        self.capital_expenditures = float(cash_flow_data["annualReports"][0]["capitalExpenditures"])

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

        self.EBITDA_data = float(income_statement_data["annualReports"][0]["ebitda"])

        self.current_debt = float(balance_sheet_data["annualReports"][0]["currentDebt"])

        self.investments = float(balance_sheet_data["annualReports"][0]["investments"])

        self.cash_cash_equivalents = float(
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
            self.dividend_payout = float(cash_flow_data["annualReports"][0]["dividendPayout"])

        self.cost_of_goods = float(income_statement_data["annualReports"][0]["costofGoodsAndServicesSold"])

        self.current_assets = float(balance_sheet_data["annualReports"][0]["totalCurrentAssets"])
        self.current_liabilities = float(balance_sheet_data["annualReports"][0]["totalCurrentLiabilities"])
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
        self.cash_flow_to_debt_rank = 0
        self.historic_revenue_rank_past = 0
        self.historic_revenue_rank_current = 0
        self.historic_net_income_rank_past = 0
        self.historic_net_income_rank_current = 0
        self.net_income_margin_rank = 0
        self.historic_gross_profit_rank_past = 0
        self.historic_gross_profit_rank_current = 0
        self.gross_profit_margin_rank = 0
        self.working_capital_rank = 0
        self.leverage_rank = 0
        self.total_asset_turnover_rank = 0

    def current_ratio(self):
        return self.current_assets / self.current_liabilities

    def working_capital(self):
        return self.current_assets - self.current_liabilities

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

    def cash_flow_to_debt(self):
        return self.operating_cash_flow / self.current_debt

    def leverage(self):
        return self.total_assets / self.total_shareholder_equity

    def total_asset_turnover(self):
        return self.total_revenue_current / (self.total_assets / 2)

    def net_income_margin(self):
        return (self.net_income / self.total_revenue_current) * 100

    def gross_profit_margin(self):
        return ((self.total_revenue_current - self.cost_of_goods) / self.total_revenue_current) * 100

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
        # ranks the current ratio
        if 2 <= self.current_ratio():
            self.current_ratio_rank = 5
        elif 1.5 <= self.current_ratio() < 2:
            self.current_ratio_rank = 4
        elif 1.2 <= self.current_ratio() < 1.5:
            self.current_ratio_rank = 3
        elif 1 <= self.current_ratio() < 1.2:
            self.current_ratio_rank = 2
        elif self.current_ratio() < 1:
            self.current_ratio_rank = 1

        return self.current_ratio_rank

    def debt_to_equity_rank(self):
        # ranks the debt to equity ratio
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
        # ranks price to book ratio
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
        # ranks price to sales ratio
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
        # ranks dividend payout ratio
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
        # ranks dividend yield ratio
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

    def rank_cash_flow_to_debt(self):
        # ranks cash flow to debt ratio
        if 66 <= self.cash_flow_to_debt():
            self.cash_flow_to_debt_rank = 5
        elif 50 <= self.cash_flow_to_debt() < 66:
            self.cash_flow_to_debt_rank = 4
        elif 40 <= self.cash_flow_to_debt() < 50:
            self.cash_flow_to_debt_rank = 3
        elif 30 <= self.cash_flow_to_debt() < 40:
            self.cash_flow_to_debt_rank = 2
        elif self.cash_flow_to_debt() < 30:
            self.cash_flow_to_debt_rank = 1

        return self.cash_flow_to_debt_rank

    def past_historic_revenue_rank(self):
        # determines average rate of change over last five years
        yearly_rates_of_change_sum = 0
        for i in range(0, len(self.total_revenue_historic_array) - 1):
            yearly_rates_of_change_sum += ((self.total_revenue_historic_array[i + 1] - self.total_revenue_historic_array[i]) /
                                           self.historic_free_cash_flow[i]) * 100
        avg_roc = yearly_rates_of_change_sum / 4

        # ranks the average percentage growth over the last 5 years
        if 10 <= avg_roc:
            self.historic_revenue_rank_past = 5
        elif 8 <= avg_roc < 10:
            self.historic_revenue_rank_past = 4
        elif 6 <= avg_roc < 8:
            self.historic_revenue_rank_past = 3
        elif 4 <= avg_roc < 6:
            self.historic_revenue_rank_past = 2
        elif avg_roc < 4:
            self.historic_revenue_rank_past = 1

        return self.historic_revenue_rank_past

    def current_historic_revenue_rank(self):
        # determines four year avg
        four_year_sum = 0
        for i in self.historic_free_cash_flow[0:3]:
            four_year_sum += i
        four_year_avg = four_year_sum / 4

        # determinges current rate of change
        current_roc = ((self.historic_free_cash_flow[4] - four_year_avg) / four_year_avg) * 100

        # ranks the current growth
        if 10 <= current_roc:
            self.historic_revenue_rank_current = 5
        elif 8 <= current_roc < 10:
            self.historic_revenue_rank_current = 4
        elif 6 <= current_roc < 8:
            self.historic_revenue_rank_current = 3
        elif 4 <= current_roc < 6:
            self.historic_revenue_rank_current = 2
        elif current_roc < 4:
            self.historic_revenue_rank_current = 1

        return self.historic_revenue_rank_current


    def past_historic_net_income_rank(self):
        # determines average rate of change over last five years
        yearly_rates_of_change_sum = 0
        for i in range(0, len(self.total_revenue_historic_array) - 1):
            yearly_rates_of_change_sum += ((self.total_revenue_historic_array[i + 1] -
                                            self.total_revenue_historic_array[i]) /
                                           self.historic_free_cash_flow[i]) * 100
        avg_roc = yearly_rates_of_change_sum / 4

        # ranks the average change over last 5 years
        if 20 <= avg_roc:
            self.historic_net_income_rank_past = 5
        elif 15 <= avg_roc < 20:
            self.historic_net_income_rank_past = 4
        elif 10 <= avg_roc < 15:
            self.historic_net_income_rank_past = 3
        elif 5 <= avg_roc < 15:
            self.historic_net_income_rank_past = 2
        elif avg_roc < 5:
            self.historic_net_income_rank_past = 1

        return self.historic_net_income_rank_past


    def current_historic_net_income_rank(self):
        # determines four year avg
        four_year_sum = 0
        for i in self.historic_free_cash_flow[0:3]:
            four_year_sum += i
        four_year_avg = four_year_sum / 4

        # determinges current rate of change
        current_roc = ((self.historic_free_cash_flow[4] - four_year_avg) / four_year_avg) * 100

        # ranks the current rate of change
        if 20 <= current_roc:
            self.historic_net_income_rank_current = 5
        elif 15 <= current_roc < 20:
            self.historic_net_income_rank_current = 4
        elif 10 <= current_roc < 15:
            self.historic_net_income_rank_current = 3
        elif 5 <= current_roc < 15:
            self.historic_net_income_rank_current = 2
        elif current_roc < 5:
            self.historic_net_income_rank_current = 1

        return self.historic_net_income_rank_current

    def rank_net_income_margin(self):
        # ranks net income margin
        if 20 <= self.net_income_margin():
            self.net_income_margin_rank = 5
        elif 15 <= self.net_income_margin() < 20:
            self.net_income_margin_rank = 4
        elif 10 <= self.net_income_margin() < 15:
            self.net_income_margin_rank = 3
        elif 5 <= self.net_income_margin() < 10:
            self.net_income_margin_rank = 2
        elif self.net_income_margin() < 5:
            self.net_income_margin_rank = 1

        return self.net_income_margin_rank

    def past_historic_gross_profit_rank(self):
        # determines average rate of change over last five years
        yearly_rates_of_change_sum = 0
        for i in range(0, len(self.total_revenue_historic_array) - 1):
            yearly_rates_of_change_sum += ((self.total_revenue_historic_array[i + 1] -
                                            self.total_revenue_historic_array[i]) /
                                           self.historic_free_cash_flow[i]) * 100
        avg_roc = yearly_rates_of_change_sum / 4

        # ranks rate of change over last five years
        if 45 <= avg_roc:
            self.historic_gross_profit_rank_past = 5
        elif 30 <= avg_roc < 45:
            self.historic_gross_profit_rank_past = 4
        elif 15 <= avg_roc < 30:
            self.historic_gross_profit_rank_past = 3
        elif 5 <= avg_roc < 15:
            self.historic_gross_profit_rank_past = 2
        elif avg_roc < 5:
            self.historic_gross_profit_rank_past = 1

        return self.historic_gross_profit_rank_past

    def current_historic_gross_profit_rank(self):
        # determines four year avg
        four_year_sum = 0
        for i in self.historic_free_cash_flow[0:3]:
            four_year_sum += i
        four_year_avg = four_year_sum / 4

        # determinges current rate of change
        current_roc = ((self.historic_free_cash_flow[4] - four_year_avg) / four_year_avg) * 100

        # ranks the current rate of change
        if 45 <= current_roc:
            self.historic_gross_profit_rank_current = 5
        elif 30 <= current_roc < 45:
            self.historic_gross_profit_rank_current = 4
        elif 15 <= current_roc < 30:
            self.historic_gross_profit_rank_current = 3
        elif 5 <= current_roc < 15:
            self.historic_gross_profit_rank_current = 2
        elif current_roc < 5:
            self.historic_gross_profit_rank_current = 1

        return self.historic_gross_profit_rank_current


    def rank_gross_profit_margin(self):
        # ranks the gross profit margin
        if 70 <= self.gross_profit_margin():
            self.gross_profit_margin_rank = 5
        elif 50 <= self.gross_profit_margin() < 70:
            self.gross_profit_margin_rank = 4
        elif 30 <= self.gross_profit_margin() < 50:
            self.gross_profit_margin_rank = 3
        elif 10 <= self.gross_profit_margin() < 30:
            self.gross_profit_margin_rank = 2
        elif self.gross_profit_margin() < 10:
            self.gross_profit_margin_rank = 1

        return self.gross_profit_margin_rank

    def rank_leverage(self):
        # ranks leverage
        if 2 <= self.leverage():
            self.leverage_rank = 1
        elif 1.5 <= self.leverage() < 2:
            self.leverage_rank = 2
        elif 1 <= self.leverage() < 1.5:
            self.leverage_rank = 3
        elif 0.5 <= self.leverage() < 1:
            self.leverage_rank = 4
        elif self.leverage() < 0.5:
            self.leverage_rank = 5

        return self.leverage_rank

    def rank_total_asset_turnover(self):
        # ranks the total asset turnover ratio
        if 2.5 <= self.total_asset_turnover():
            self.total_asset_turnover_rank = 5
        elif 0.5 <= self.total_asset_turnover() < 2.5:
            self.total_asset_turnover_rank = 4
        elif 0.25 <= self.total_asset_turnover() < 0.5:
            self.total_asset_turnover_rank = 3
        elif 0.15 <= self.total_asset_turnover() < 0.25:
            self.total_asset_turnover_rank = 2
        elif self.total_asset_turnover() < 0.15:
            self.total_asset_turnover_rank = 1

        return self.total_asset_turnover_rank



    def total_rank(self):
        total_rank_sum = self.ratio_dividend_payout_rank() + self.price_to_sales_rank() + self.price_to_book_rank() + self.debt_to_equity_rank() + self.rank_current_ratio() + self.free_cash_rank_current() + self.free_cash_rank_past() + self.ROE_rank_past() + self.ROE_rank_current() + self.EPS_rank_current() + self.EPS_rank_past() + self.pe_ratio_rank() + self.rank_dividend_yield_ratio() + self.rank_cash_flow_to_debt() + self.past_historic_revenue_rank() + self.current_historic_revenue_rank() + self.past_historic_net_income_rank() + self.current_historic_net_income_rank() + self.rank_net_income_margin() + self.past_historic_gross_profit_rank() + self.current_historic_gross_profit_rank() + self.rank_gross_profit_margin() + self.rank_leverage() + self.rank_total_asset_turnover()
        self.avg_rank = total_rank_sum / 24
        return round(self.avg_rank, 5)

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
        BVPS_XLE_dict["XOM"] = round((float(
            self.XOM_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.XOM_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLE_dict["CVX"] = round((float(
            self.CVX_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.CVX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLE_dict["EOG"] = round((float(
            self.EOG_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.EOG_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        # for some reason COP shares outstanding in most recent years were negative, and I'm assuming it's a glitch in
        # the API, so I just used the most recent year with a positive shares outstanding value
        BVPS_XLE_dict["COP"] = round((float(
            self.COP_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.COP_balance_sheet["annualReports"][2]["commonStockSharesOutstanding"])), 3)
        BVPS_XLE_dict["SLB"] = round((float(
            self.SLB_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.SLB_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLE_dict

    # EPS for XLE tickers
    def EPS_XLE(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLE_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLE_dict["XOM"] = round((float(self.XOM_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.XOM_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLE_dict["CVX"] = round((float(self.CVX_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.CVX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLE_dict["EOG"] = round((float(self.EOG_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.EOG_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        # for some reason COP shares outstanding in most recent years were negative, and I'm assuming it's a glitch in
        # the API, so I just used the most recent year with a positive shares outstanding value
        EPS_XLE_dict["COP"] = round((float(self.COP_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.COP_balance_sheet["annualReports"][2]["commonStockSharesOutstanding"])), 3)
        EPS_XLE_dict["SLB"] = round((float(self.SLB_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.SLB_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLE_dict

    # debt to equity for XLE tickers
    def debt_equity_XLE(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLE_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLE_dict["XOM"] = round(((float(self.XOM_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.XOM_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLE_dict["CVX"] = round(((float(self.CVX_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.CVX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLE_dict["EOG"] = round(((float(self.EOG_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.EOG_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLE_dict["COP"] = round(((float(self.COP_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.COP_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLE_dict["SLB"] = round(((float(self.SLB_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.SLB_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLE_dict

    # ROE for XLE tickers
    def ROE_XLE(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLE_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLE_dict["XOM"] = round((float(self.XOM_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.XOM_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLE_dict["CVX"] = round((float(self.CVX_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.CVX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLE_dict["EOG"] = round((float(self.EOG_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.EOG_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLE_dict["COP"] = round((float(self.COP_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.COP_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLE_dict["SLB"] = round((float(self.SLB_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.SLB_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLE_dict

    # free cash flow for XLE tickers
    def free_cash_XLE(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLE_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLE_dict["XOM"] = (float(self.XOM_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.XOM_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLE_dict["CVX"] = (float(self.CVX_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.CVX_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLE_dict["EOG"] = (float(self.EOG_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.EOG_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLE_dict["COP"] = (float(self.COP_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.COP_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLE_dict["SLB"] = (float(self.SLB_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.SLB_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLE_dict


""""
XLE = Sector_Analysis_XLE()
print(XLE.BVPS_XLE())
print(XLE.EPS_XLE())
print(XLE.debt_equity_XLE())
print(XLE.ROE_XLE())
print(XLE.free_cash_XLE())
"""


class Sector_Analysis_XLB:
    def __init__(self):
        self.tickerListXLB = ["LIN", "FCX", "NEM", "SHW", "APD"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/LINJson/LINbalance.json",
                'r') as f:
            self.LIN_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/FCXJson/FCXbalance.json",
                'r') as f:
            self.FCX_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NEMJson/NEMbalance.json",
                'r') as f:
            self.NEM_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/SHWJson/SHWbalance.json",
                'r') as f:
            self.SHW_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/APDJson/APDbalance.json",
                'r') as f:
            self.APD_balance_sheet = json.load(f)

        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/LINJson/LINcash.json",
                'r') as f:
            self.LIN_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/FCXJson/FCXcash.json",
                'r') as f:
            self.FCX_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NEMJson/NEMcash.json",
                'r') as f:
            self.NEM_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/SHWJson/SHWcash.json",
                'r') as f:
            self.SHW_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/APDJson/APDcash.json",
                'r') as f:
            self.APD_cash_sheet = json.load(f)

        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/LINJson/LINincome.json",
                'r') as f:
            self.LIN_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/FCXJson/FCXincome.json",
                'r') as f:
            self.FCX_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NEMJson/NEMincome.json",
                'r') as f:
            self.NEM_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/SHWJson/SHWincome.json",
                'r') as f:
            self.SHW_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/APDJson/APDincome.json",
                'r') as f:
            self.APD_income_sheet = json.load(f)

    # function for XLB ticker's BVPS
    def BVPS_XLB(self):
        # dictionary that returns BVPS for each ticker
        BVPS_XLB_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLB_dict["LIN"] = round((float(
            self.LIN_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.LIN_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLB_dict["FCX"] = round((float(
            self.FCX_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.FCX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLB_dict["NEM"] = round((float(
            self.NEM_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.NEM_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLB_dict["SHW"] = round((float(
            self.SHW_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.SHW_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLB_dict["APD"] = round((float(
            self.APD_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.APD_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLB_dict

    # EPS for XLB tickers
    def EPS_XLB(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLB_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLB_dict["LIN"] = round((float(self.LIN_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.LIN_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLB_dict["FCX"] = round((float(self.FCX_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.FCX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLB_dict["NEM"] = round((float(self.NEM_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.NEM_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLB_dict["SHW"] = round((float(self.SHW_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.SHW_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLB_dict["APD"] = round((float(self.APD_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.APD_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLB_dict

    # debt to equity for XLB tickers
    def debt_equity_XLB(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLB_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLB_dict["LIN"] = round(((float(self.LIN_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.LIN_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLB_dict["FCX"] = round(((float(self.FCX_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.FCX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLB_dict["NEM"] = round(((float(self.NEM_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.NEM_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLB_dict["SHW"] = round(((float(self.SHW_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.SHW_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLB_dict["APD"] = round(((float(self.APD_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.APD_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLB_dict

    # ROE for XLB tickers
    def ROE_XLB(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLB_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLB_dict["LIN"] = round((float(self.LIN_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.LIN_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLB_dict["FCX"] = round((float(self.FCX_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.FCX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLB_dict["NEM"] = round((float(self.NEM_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.NEM_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLB_dict["SHW"] = round((float(self.SHW_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.SHW_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLB_dict["APD"] = round((float(self.APD_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.APD_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLB_dict

    # free cash flow for XLB tickers
    def free_cash_XLB(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLB_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLB_dict["LIN"] = (float(self.LIN_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.LIN_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLB_dict["FCX"] = (float(self.FCX_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.FCX_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLB_dict["NEM"] = (float(self.NEM_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.NEM_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLB_dict["SHW"] = (float(self.SHW_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.SHW_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLB_dict["APD"] = (float(self.APD_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.APD_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLB_dict

"""
XLB = Sector_Analysis_XLB()
print(XLB.BVPS_XLB())
print(XLB.EPS_XLB())
print(XLB.ROE_XLB())
print(XLB.debt_equity_XLB())
print(XLB.free_cash_XLB())
"""


class Sector_Analysis_XLI:
    def __init__(self):
        self.tickerListXLI = ["HON", "UPS", "UNP", "BA", "RTX"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/HONJson/HONbalance.json",
                'r') as f:
            self.HON_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/UPSJson/UPSbalance.json",
                'r') as f:
            self.UPS_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/UNPJson/UNPbalance.json",
                'r') as f:
            self.UNP_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/BAJson/BAbalance.json",
                'r') as f:
            self.BA_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/RTXJson/RTXbalance.json",
                'r') as f:
            self.RTX_balance_sheet = json.load(f)

        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/HONJson/HONcash.json",
                'r') as f:
            self.HON_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/UPSJson/UPScash.json",
                'r') as f:
            self.UPS_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/UNPJson/UNPcash.json",
                'r') as f:
            self.UNP_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/BAJson/BAcash.json",
                'r') as f:
            self.BA_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/RTXJson/RTXcash.json",
                'r') as f:
            self.RTX_cash_sheet = json.load(f)

        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/HONJson/HONincome.json",
                'r') as f:
            self.HON_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/UPSJson/UPSincome.json",
                'r') as f:
            self.UPS_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/UNPJson/UNPincome.json",
                'r') as f:
            self.UNP_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/BAJson/BAincome.json",
                'r') as f:
            self.BA_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/RTXJson/RTXincome.json",
                'r') as f:
            self.RTX_income_sheet = json.load(f)

    # function for XLI ticker's BVPS
    def BVPS_XLI(self):
        # dictionary that returns BVPS for each ticker
        BVPS_XLI_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLI_dict["HON"] = round((float(
            self.HON_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.HON_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLI_dict["UPS"] = round((float(
            self.UPS_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.UPS_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLI_dict["UNP"] = round((float(
            self.UNP_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.UNP_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLI_dict["BA"] = round((float(
            self.BA_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.BA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLI_dict["RTX"] = round((float(
            self.RTX_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.RTX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLI_dict

    # EPS for XLI tickers
    def EPS_XLI(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLI_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLI_dict["HON"] = round((float(self.HON_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.HON_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLI_dict["UPS"] = round((float(self.UPS_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.UPS_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLI_dict["UNP"] = round((float(self.UNP_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.UNP_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLI_dict["BA"] = round((float(self.BA_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.BA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLI_dict["RTX"] = round((float(self.RTX_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.RTX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLI_dict

    # debt to equity for XLB tickers
    def debt_equity_XLI(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLI_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLI_dict["HON"] = round(((float(self.HON_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.HON_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLI_dict["UPS"] = round(((float(self.UPS_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.UPS_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLI_dict["UNP"] = round(((float(self.UNP_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.UNP_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLI_dict["BA"] = round(((float(self.BA_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.BA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLI_dict["RTX"] = round(((float(self.RTX_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.RTX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLI_dict

    # ROE for XLB tickers
    def ROE_XLI(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLI_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLI_dict["HON"] = round((float(self.HON_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.HON_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLI_dict["UPS"] = round((float(self.UPS_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.UPS_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLI_dict["UNP"] = round((float(self.UNP_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.UNP_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLI_dict["BA"] = round((float(self.BA_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.BA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLI_dict["RTX"] = round((float(self.RTX_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.RTX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLI_dict

    # free cash flow for XLB tickers
    def free_cash_XLI(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLI_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLI_dict["HON"] = (float(self.HON_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.HON_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLI_dict["UPS"] = (float(self.UPS_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.UPS_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLI_dict["UNP"] = (float(self.UNP_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.UNP_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLI_dict["BA"] = (float(self.BA_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.BA_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLI_dict["RTX"] = (float(self.RTX_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.RTX_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLI_dict

"""
XLI = Sector_Analysis_XLI()
print(XLI.EPS_XLI())
print(XLI.ROE_XLI())
print(XLI.BVPS_XLI())
print(XLI.debt_equity_XLI())
print(XLI.free_cash_XLI())
"""

class Sector_Analysis_XLY:
    def __init__(self):
        self.tickerListXLY = ["AMZN", "TSLA", "HD", "NKE", "MCD"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/AMZNJson/AMZNbalance.json",
                'r') as f:
            self.AMZN_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/TSLAJson/TSLAbalance.json",
                'r') as f:
            self.TSLA_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/HDJson/HDbalance.json",
                'r') as f:
            self.HD_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NKEJson/NKEbalance.json",
                'r') as f:
            self.NKE_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MCDJson/MCDbalance.json",
                'r') as f:
            self.MCD_balance_sheet = json.load(f)

        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/AMZNJson/AMZNcash.json",
                'r') as f:
            self.AMZN_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/TSLAJson/TSLAcash.json",
                'r') as f:
            self.TSLA_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/HDJson/HDcash.json",
                'r') as f:
            self.HD_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NKEJson/NKEcash.json",
                'r') as f:
            self.NKE_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MCDJson/MCDcash.json",
                'r') as f:
            self.MCD_cash_sheet = json.load(f)

        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/AMZNJson/AMZNincome.json",
                'r') as f:
            self.AMZN_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/TSLAJson/TSLAincome.json",
                'r') as f:
            self.TSLA_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/HDJson/HDincome.json",
                'r') as f:
            self.HD_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NKEJson/NKEincome.json",
                'r') as f:
            self.NKE_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MCDJson/MCDincome.json",
                'r') as f:
            self.MCD_income_sheet = json.load(f)

    # function for XLY ticker's BVPS
    def BVPS_XLY(self):
        # dictionary that returns BVPS for each ticker
        BVPS_XLY_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLY_dict["AMZN"] = round((float(
            self.AMZN_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.AMZN_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLY_dict["TSLA"] = round((float(
            self.TSLA_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.TSLA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLY_dict["HD"] = round((float(
            self.HD_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.HD_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLY_dict["NKE"] = round((float(
            self.NKE_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.NKE_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLY_dict["MCD"] = round((float(
            self.MCD_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.MCD_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLY_dict

    # EPS for XLY tickers
    def EPS_XLY(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLY_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLY_dict["AMZN"] = round((float(self.AMZN_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.AMZN_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLY_dict["TSLA"] = round((float(self.TSLA_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.TSLA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLY_dict["HD"] = round((float(self.HD_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.HD_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLY_dict["NKE"] = round((float(self.NKE_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.NKE_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLY_dict["MCD"] = round((float(self.MCD_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.MCD_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLY_dict

    # debt to equity for XLY tickers
    def debt_equity_XLY(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLY_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLY_dict["AMZN"] = round(((float(self.AMZN_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.AMZN_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLY_dict["TSLA"] = round(((float(self.TSLA_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.TSLA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLY_dict["HD"] = round(((float(self.HD_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.HD_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLY_dict["NKE"] = round(((float(self.NKE_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.NKE_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLY_dict["MCD"] = round(((float(self.MCD_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.MCD_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLY_dict

    # ROE for XLY tickers
    def ROE_XLY(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLY_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLY_dict["AMZN"] = round((float(self.AMZN_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.AMZN_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLY_dict["TSLA"] = round((float(self.TSLA_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.TSLA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLY_dict["HD"] = round((float(self.HD_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.HD_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLY_dict["NKE"] = round((float(self.NKE_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.NKE_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLY_dict["MCD"] = round((float(self.MCD_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.MCD_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLY_dict

    # free cash flow for XLY tickers
    def free_cash_XLY(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLY_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLY_dict["AMZN"] = (float(self.AMZN_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.AMZN_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLY_dict["TSLA"] = (float(self.TSLA_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.TSLA_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLY_dict["HD"] = (float(self.HD_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.HD_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLY_dict["NKE"] = (float(self.NKE_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.NKE_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLY_dict["MCD"] = (float(self.MCD_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.MCD_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLY_dict

class Sector_Analysis_XLP:
    def __init__(self):
        self.tickerListXLP = ["PG", "KO", "PEP", "WMT", "COST"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PGJson/PGbalance.json",
                'r') as f:
            self.PG_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/KOJson/KObalance.json",
                'r') as f:
            self.KO_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PEPJson/PEPbalance.json",
                'r') as f:
            self.PEP_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/WMTJson/WMTbalance.json",
                'r') as f:
            self.WMT_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/COSTJson/COSTbalance.json",
                'r') as f:
            self.COST_balance_sheet = json.load(f)

        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PGJson/PGcash.json",
                'r') as f:
            self.PG_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/KOJson/KOcash.json",
                'r') as f:
            self.KO_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PEPJson/PEPcash.json",
                'r') as f:
            self.PEP_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/WMTJson/WMTcash.json",
                'r') as f:
            self.WMT_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/COSTJson/COSTcash.json",
                'r') as f:
            self.COST_cash_sheet = json.load(f)

        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PGJson/PGincome.json",
                'r') as f:
            self.PG_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/KOJson/KOincome.json",
                'r') as f:
            self.KO_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PEPJson/PEPincome.json",
                'r') as f:
            self.PEP_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/WMTJson/WMTincome.json",
                'r') as f:
            self.WMT_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/COSTJson/COSTincome.json",
                'r') as f:
            self.COST_income_sheet = json.load(f)

    # function for XLP ticker's BVPS
    def BVPS_XLP(self):
        # dictionary that returns BVPS for each ticker
        BVPS_XLP_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLP_dict["PG"] = round((float(
            self.PG_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.PG_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLP_dict["KO"] = round((float(
            self.KO_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.KO_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLP_dict["PEP"] = round((float(
            self.PEP_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.PEP_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLP_dict["WMT"] = round((float(
            self.WMT_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.WMT_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLP_dict["COST"] = round((float(
            self.COST_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.COST_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLP_dict

    # EPS for XLP tickers
    def EPS_XLP(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLP_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLP_dict["PG"] = round((float(self.PG_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.PG_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLP_dict["KO"] = round((float(self.KO_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.KO_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLP_dict["PEP"] = round((float(self.PEP_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.PEP_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLP_dict["WMT"] = round((float(self.WMT_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.WMT_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLP_dict["COST"] = round((float(self.COST_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.COST_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLP_dict

    # debt to equity for XLP tickers
    def debt_equity_XLP(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLP_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLP_dict["PG"] = round(((float(self.PG_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.PG_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLP_dict["KO"] = round(((float(self.KO_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.KO_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLP_dict["PEP"] = round(((float(self.PEP_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.PEP_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLP_dict["WMT"] = round(((float(self.WMT_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.WMT_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLP_dict["COST"] = round(((float(self.COST_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.COST_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLP_dict

    # ROE for XLP tickers
    def ROE_XLP(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLP_dict = {}


        # adds tickers' corresponding ROE to the dictionary
        ROE_XLP_dict["PG"] = round((float(self.PG_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.PG_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLP_dict["KO"] = round((float(self.KO_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.KO_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLP_dict["PEP"] = round((float(self.PEP_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.PEP_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLP_dict["WMT"] = round((float(self.WMT_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.WMT_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLP_dict["COST"] = round((float(self.COST_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.COST_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLP_dict

    # free cash flow for XLP tickers
    def free_cash_XLP(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLP_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLP_dict["PG"] = (float(self.PG_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.PG_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLP_dict["KO"] = (float(self.KO_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.KO_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLP_dict["PEP"] = (float(self.PEP_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.PEP_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLP_dict["WMT"] = (float(self.WMT_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.WMT_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLP_dict["COST"] = (float(self.COST_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.COST_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLP_dict

"""
XLP = Sector_Analysis_XLP()
print(XLP.EPS_XLP())
print(XLP.ROE_XLP())
print(XLP.BVPS_XLP())
print(XLP.debt_equity_XLP())
print(XLP.debt_equity_XLP())
"""


class Sector_Analysis_XLV:
    def __init__(self):
        self.tickerListXLV = ["UNH", "JNJ", "PFE", "ABBV", "TMO"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/UNHJson/UNHbalance.json",
                'r') as f:
            self.UNH_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/JNJJson/JNJbalance.json",
                'r') as f:
            self.JNJ_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PFEJson/PFEbalance.json",
                'r') as f:
            self.PFE_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/ABBVJson/ABBVbalance.json",
                'r') as f:
            self.ABBV_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/TMOJson/TMObalance.json",
                'r') as f:
            self.TMO_balance_sheet = json.load(f)

        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/UNHJson/UNHcash.json",
                'r') as f:
            self.UNH_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/JNJJson/JNJcash.json",
                'r') as f:
            self.JNJ_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PFEJson/PFEcash.json",
                'r') as f:
            self.PFE_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/ABBVJson/ABBVcash.json",
                'r') as f:
            self.ABBV_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/TMOJson/TMOcash.json",
                'r') as f:
            self.TMO_cash_sheet = json.load(f)

        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/UNHJson/UNHincome.json",
                'r') as f:
            self.UNH_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/JNJJson/JNJincome.json",
                'r') as f:
            self.JNJ_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PFEJson/PFEincome.json",
                'r') as f:
            self.PFE_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/ABBVJson/ABBVincome.json",
                'r') as f:
            self.ABBV_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/TMOJson/TMOincome.json",
                'r') as f:
            self.TMO_income_sheet = json.load(f)

    # function for XLV ticker's BVPS
    def BVPS_XLV(self):
        # dictionary that returns BVPS for each ticker
        BVPS_XLV_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLV_dict["UNH"] = round((float(
            self.UNH_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.UNH_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLV_dict["JNJ"] = round((float(
            self.JNJ_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.JNJ_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLV_dict["PFE"] = round((float(
            self.PFE_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.PFE_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLV_dict["ABBV"] = round((float(
            self.ABBV_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.ABBV_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLV_dict["TMO"] = round((float(
            self.TMO_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.TMO_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLV_dict

    # EPS for XLV tickers
    def EPS_XLV(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLV_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLV_dict["UNH"] = round((float(self.UNH_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.UNH_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLV_dict["JNJ"] = round((float(self.JNJ_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.JNJ_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLV_dict["PFE"] = round((float(self.PFE_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.PFE_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLV_dict["ABBV"] = round((float(self.ABBV_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.ABBV_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLV_dict["TMO"] = round((float(self.TMO_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.TMO_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLV_dict

    # debt to equity for XLV tickers
    def debt_equity_XLV(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLV_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLV_dict["UNH"] = round(((float(self.UNH_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.UNH_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLV_dict["JNJ"] = round(((float(self.JNJ_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.JNJ_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLV_dict["PFE"] = round(((float(self.PFE_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.PFE_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLV_dict["ABBV"] = round(((float(self.ABBV_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.ABBV_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLV_dict["TMO"] = round(((float(self.TMO_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.TMO_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLV_dict

    # ROE for XLV tickers
    def ROE_XLV(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLV_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLV_dict["UNH"] = round((float(self.UNH_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.UNH_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLV_dict["JNJ"] = round((float(self.JNJ_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.JNJ_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLV_dict["PFE"] = round((float(self.PFE_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.PFE_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLV_dict["ABBV"] = round((float(self.ABBV_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.ABBV_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLV_dict["TMO"] = round((float(self.TMO_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.TMO_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLV_dict

    # free cash flow for XLV tickers
    def free_cash_XLV(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLV_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLV_dict["UNH"] = (float(self.UNH_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.UNH_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLV_dict["JNJ"] = (float(self.JNJ_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.JNJ_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLV_dict["PFE"] = (float(self.PFE_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.PFE_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLV_dict["ABBV"] = (float(self.ABBV_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.ABBV_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLV_dict["TMO"] = (float(self.TMO_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.TMO_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLV_dict

"""
XLV = Sector_Analysis_XLV()
print(XLV.EPS_XLV())
print(XLV.ROE_XLV())
print(XLV.BVPS_XLV())
print(XLV.debt_equity_XLV())
print(XLV.free_cash_XLV())
"""

class Sector_Analysis_XLF:
    def __init__(self):
        self.tickerListXLF = ["JPM", "BAC", "WFC", "C", "MS"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/JPMJson/JPMbalance.json",
                'r') as f:
            self.JPM_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/BACJson/BACbalance.json",
                'r') as f:
            self.BAC_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/WFCJson/WFCbalance.json",
                'r') as f:
            self.WFC_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CJson/Cbalance.json",
                'r') as f:
            self.C_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MSJson/MSbalance.json",
                'r') as f:
            self.MS_balance_sheet = json.load(f)

        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/JPMJson/JPMcash.json",
                'r') as f:
            self.JPM_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/BACJson/BACcash.json",
                'r') as f:
            self.BAC_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/WFCJson/WFCcash.json",
                'r') as f:
            self.WFC_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CJson/Ccash.json",
                'r') as f:
            self.C_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MSJson/MScash.json",
                'r') as f:
            self.MS_cash_sheet = json.load(f)

        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/JPMJson/JPMincome.json",
                'r') as f:
            self.JPM_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/BACJson/BACincome.json",
                'r') as f:
            self.BAC_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/WFCJson/WFCincome.json",
                'r') as f:
            self.WFC_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CJson/Cincome.json",
                'r') as f:
            self.C_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MSJson/MSincome.json",
                'r') as f:
            self.MS_income_sheet = json.load(f)

    # function for XLF ticker's BVPS
    def BVPS_XLF(self):
        # dictionary that returns BVPS for each ticker
        BVPS_XLF_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLF_dict["JPM"] = round((float(
            self.JPM_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.JPM_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLF_dict["BAC"] = round((float(
            self.BAC_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.BAC_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLF_dict["WFC"] = round((float(
            self.WFC_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.WFC_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLF_dict["C"] = round((float(
            self.C_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.C_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLF_dict["MS"] = round((float(
            self.MS_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.MS_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLF_dict

    # EPS for XLF tickers
    def EPS_XLF(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLF_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLF_dict["JPM"] = round((float(self.JPM_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.JPM_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLF_dict["BAC"] = round((float(self.BAC_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.BAC_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLF_dict["WFC"] = round((float(self.WFC_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.WFC_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLF_dict["C"] = round((float(self.C_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.C_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLF_dict["MS"] = round((float(self.MS_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.MS_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLF_dict

    # debt to equity for XLF tickers
    def debt_equity_XLF(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLF_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLF_dict["JPM"] = round(((float(self.JPM_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.JPM_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLF_dict["BAC"] = round(((float(self.BAC_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.BAC_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLF_dict["WFC"] = round(((float(self.WFC_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.WFC_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLF_dict["C"] = round(((float(self.C_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.C_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLF_dict["MS"] = round(((float(self.MS_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.MS_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLF_dict

    # ROE for XLF tickers
    def ROE_XLF(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLF_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLF_dict["JPM"] = round((float(self.JPM_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.JPM_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLF_dict["BAC"] = round((float(self.BAC_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.BAC_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLF_dict["WFC"] = round((float(self.WFC_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.WFC_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLF_dict["C"] = round((float(self.C_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.C_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLF_dict["MS"] = round((float(self.MS_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.MS_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLF_dict

    # free cash flow for XLF tickers
    def free_cash_XLF(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLF_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary

        # JPM, BAC, WFC has no capital expenditures so I filled in the value with 0
        FREE_CASH_XLF_dict["JPM"] = float(self.JPM_cash_sheet["annualReports"][0]["operatingCashflow"]) - 0
        FREE_CASH_XLF_dict["BAC"] = float(self.BAC_cash_sheet["annualReports"][0]["operatingCashflow"]) - 0
        FREE_CASH_XLF_dict["WFC"] = float(self.WFC_cash_sheet["annualReports"][0]["operatingCashflow"]) - 0
        FREE_CASH_XLF_dict["C"] = (float(self.C_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.C_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLF_dict["MS"] = (float(self.MS_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.MS_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLF_dict

"""
XLF = Sector_Analysis_XLF()
print(XLF.EPS_XLF())
print(XLF.ROE_XLF())
print(XLF.BVPS_XLF())
print(XLF.debt_equity_XLF())
print(XLF.free_cash_XLF())
"""

class Sector_Analysis_XLU:
    def __init__(self):
        self.tickerListXLU = ["NEE", "DUK", "SO", "D", "EXC"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NEEJson/NEEbalance.json",
                'r') as f:
            self.NEE_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/DUKJson/DUKbalance.json",
                'r') as f:
            self.DUK_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/SOJson/SObalance.json",
                'r') as f:
            self.SO_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/DJson/Dbalance.json",
                'r') as f:
            self.D_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/EXCJson/EXCbalance.json",
                'r') as f:
            self.EXC_balance_sheet = json.load(f)

        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NEEJson/NEEcash.json",
                'r') as f:
            self.NEE_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/DUKJson/DUKcash.json",
                'r') as f:
            self.DUK_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/SOJson/SOcash.json",
                'r') as f:
            self.SO_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/DJson/Dcash.json",
                'r') as f:
            self.D_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/EXCJson/EXCcash.json",
                'r') as f:
            self.EXC_cash_sheet = json.load(f)

        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NEEJson/NEEincome.json",
                'r') as f:
            self.NEE_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/DUKJson/DUKincome.json",
                'r') as f:
            self.DUK_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/SOJson/SOincome.json",
                'r') as f:
            self.SO_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/DJson/Dincome.json",
                'r') as f:
            self.D_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/EXCJson/EXCincome.json",
                'r') as f:
            self.EXC_income_sheet = json.load(f)

    # function for XLU ticker's BVPS
    def BVPS_XLU(self):
        # dictionary that returns BVPS for each ticker
        BVPS_XLU_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLU_dict["NEE"] = round((float(
            self.NEE_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.NEE_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLU_dict["DUK"] = round((float(
            self.DUK_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.DUK_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLU_dict["SO"] = round((float(
            self.SO_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.SO_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLU_dict["D"] = round((float(
            self.D_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.D_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLU_dict["EXC"] = round((float(
            self.EXC_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.EXC_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLU_dict

    # EPS for XLU tickers
    def EPS_XLU(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLU_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLU_dict["NEE"] = round((float(self.NEE_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.NEE_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLU_dict["DUK"] = round((float(self.DUK_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.DUK_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLU_dict["SO"] = round((float(self.SO_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.SO_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLU_dict["D"] = round((float(self.D_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.D_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLU_dict["EXC"] = round((float(self.EXC_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.EXC_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLU_dict

    # debt to equity for XLU tickers
    def debt_equity_XLU(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLU_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLU_dict["NEE"] = round(((float(self.NEE_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.NEE_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLU_dict["DUK"] = round(((float(self.DUK_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.DUK_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLU_dict["SO"] = round(((float(self.SO_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.SO_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLU_dict["D"] = round(((float(self.D_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.D_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLU_dict["EXC"] = round(((float(self.EXC_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.EXC_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLU_dict

    # ROE for XLU tickers
    def ROE_XLU(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLU_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLU_dict["NEE"] = round((float(self.NEE_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.NEE_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLU_dict["DUK"] = round((float(self.DUK_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.DUK_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLU_dict["SO"] = round((float(self.SO_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.SO_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLU_dict["D"] = round((float(self.D_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.D_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLU_dict["EXC"] = round((float(self.EXC_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.EXC_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLU_dict

    # free cash flow for XLU tickers
    def free_cash_XLU(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLU_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLU_dict["NEE"] = float(self.NEE_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.NEE_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLU_dict["DUK"] = float(self.DUK_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.DUK_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLU_dict["SO"] = float(self.SO_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.SO_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLU_dict["D"] = (float(self.D_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.D_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLU_dict["EXC"] = (float(self.EXC_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.EXC_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLU_dict

"""
XLU = Sector_Analysis_XLU()
print(XLU.EPS_XLU())
print(XLU.ROE_XLU())
print(XLU.BVPS_XLU())
print(XLU.free_cash_XLU())
print(XLU.debt_equity_XLU())
"""

class Sector_Analysis_XLK:
    def __init__(self):
        self.tickerListXLK = ["AAPL", "MSFT", "NVDA", "V", "MA"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/AAPLJson/AAPLbalancesheet.json",
                'r') as f:
            self.AAPL_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MSFTJson/MSFTbalance.json",
                'r') as f:
            self.MSFT_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NVDAJson/NVDAbalance.json",
                'r') as f:
            self.NVDA_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/VJson/Vbalance.json",
                'r') as f:
            self.V_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MAJson/MAbalance.json",
                'r') as f:
            self.MA_balance_sheet = json.load(f)

        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/AAPLJson/AAPLcash.json",
                'r') as f:
            self.AAPL_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MSFTJson/MSFTcash.json",
                'r') as f:
            self.MSFT_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NVDAJson/NVDAcash.json",
                'r') as f:
            self.NVDA_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/VJson/Vcash.json",
                'r') as f:
            self.V_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MAJson/MAcash.json",
                'r') as f:
            self.MA_cash_sheet = json.load(f)

        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/AAPLJson/AAPLincome.json",
                'r') as f:
            self.AAPL_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MSFTJson/MSFTincome.json",
                'r') as f:
            self.MSFT_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NVDAJson/NVDAincome.json",
                'r') as f:
            self.NVDA_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/VJson/Vincome.json",
                'r') as f:
            self.V_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/MAJson/MAincome.json",
                'r') as f:
            self.MA_income_sheet = json.load(f)

    # function for XLK ticker's BVPS
    def BVPS_XLK(self):
        # dictionary that returns BVPS for each ticker
        BVPS_XLK_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLK_dict["AAPL"] = round((float(
            self.AAPL_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.AAPL_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLK_dict["MSFT"] = round((float(
            self.MSFT_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.MSFT_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLK_dict["NVDA"] = round((float(
            self.NVDA_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.NVDA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLK_dict["V"] = round((float(
            self.V_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.V_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLK_dict["MA"] = round((float(
            self.MA_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.MA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLK_dict

    # EPS for XLK tickers
    def EPS_XLK(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLK_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLK_dict["AAPL"] = round((float(self.AAPL_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.AAPL_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLK_dict["MSFT"] = round((float(self.MSFT_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.MSFT_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLK_dict["NVDA"] = round((float(self.NVDA_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.NVDA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLK_dict["V"] = round((float(self.V_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.V_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLK_dict["MA"] = round((float(self.MA_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.MA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLK_dict

    # debt to equity for XLK tickers
    def debt_equity_XLK(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLK_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLK_dict["AAPL"] = round(((float(self.AAPL_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.AAPL_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLK_dict["MSFT"] = round(((float(self.MSFT_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.MSFT_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLK_dict["NVDA"] = round(((float(self.NVDA_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.NVDA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLK_dict["V"] = round(((float(self.V_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.V_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLK_dict["MA"] = round(((float(self.MA_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.MA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLK_dict

    # ROE for XLK tickers
    def ROE_XLK(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLK_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLK_dict["AAPL"] = round((float(self.AAPL_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.AAPL_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLK_dict["MSFT"] = round((float(self.MSFT_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.MSFT_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLK_dict["NVDA"] = round((float(self.NVDA_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.NVDA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLK_dict["V"] = round((float(self.V_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.V_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLK_dict["MA"] = round((float(self.MA_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.MA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLK_dict

    # free cash flow for XLK tickers
    def free_cash_XLK(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLK_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLK_dict["AAPL"] = float(self.AAPL_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.AAPL_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLK_dict["MSFT"] = float(self.MSFT_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.MSFT_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLK_dict["NVDA"] = float(self.NVDA_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.NVDA_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLK_dict["V"] = (float(self.V_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.V_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLK_dict["MA"] = (float(self.MA_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.MA_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLK_dict
"""
XLK = Sector_Analysis_XLK()
print(XLK.ROE_XLK())
print(XLK.EPS_XLK())
print(XLK.BVPS_XLK())
print(XLK.debt_equity_XLK())
print(XLK.free_cash_XLK())
"""

class Sector_Analysis_XLC:
    def __init__(self):
        self.tickerListXLC = ["FB", "GOOGL", "NFLX", "DIS", "CMCSA"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/FBJson/FBbalance.json",
                'r') as f:
            self.FB_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/GOOGLJson/GOOGLbalance.json",
                'r') as f:
            self.GOOGL_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NFLXJson/NFLXbalance.json",
                'r') as f:
            self.NFLX_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/DISJson/DISbalance.json",
                'r') as f:
            self.DIS_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CMCSAJson/CMCSAbalance.json",
                'r') as f:
            self.CMCSA_balance_sheet = json.load(f)

        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/FBJson/FBcash.json",
                'r') as f:
            self.FB_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/GOOGLJson/GOOGLcash.json",
                'r') as f:
            self.GOOGL_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NFLXJson/NFLXcash.json",
                'r') as f:
            self.NFLX_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/DISJson/DIScash.json",
                'r') as f:
            self.DIS_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CMCSAJson/CMCSAcash.json",
                'r') as f:
            self.CMCSA_cash_sheet = json.load(f)

        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/FBJson/FBincome.json",
                'r') as f:
            self.FB_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/GOOGLJson/GOOGLincome.json",
                'r') as f:
            self.GOOGL_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/NFLXJson/NFLXincome.json",
                'r') as f:
            self.NFLX_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/DISJson/DISincome.json",
                'r') as f:
            self.DIS_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CMCSAJson/CMCSAincome.json",
                'r') as f:
            self.CMCSA_income_sheet = json.load(f)

    # function for XLC ticker's BVPS
    def BVPS_XLC(self):
        # dictionary that returns BVPS for each ticker
        BVPS_XLC_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLC_dict["FB"] = round((float(
            self.FB_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.FB_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLC_dict["GOOGL"] = round((float(
            self.GOOGL_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.GOOGL_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLC_dict["NFLX"] = round((float(
            self.NFLX_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.NFLX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLC_dict["DIS"] = round((float(
            self.DIS_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.DIS_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLC_dict["CMCSA"] = round((float(
            self.CMCSA_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.CMCSA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLC_dict

    # EPS for XLC tickers
    def EPS_XLC(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLC_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLC_dict["FB"] = round((float(self.FB_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.FB_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLC_dict["GOOGL"] = round((float(self.GOOGL_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.GOOGL_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLC_dict["NFLX"] = round((float(self.NFLX_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.NFLX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLC_dict["DIS"] = round((float(self.DIS_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.DIS_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLC_dict["CMCSA"] = round((float(self.CMCSA_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.CMCSA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLC_dict

    # debt to equity for XLC tickers
    def debt_equity_XLC(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLC_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLC_dict["FB"] = round(((float(self.FB_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.FB_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLC_dict["GOOGL"] = round(((float(self.GOOGL_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.GOOGL_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLC_dict["NFLX"] = round(((float(self.NFLX_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.NFLX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLC_dict["DIS"] = round(((float(self.DIS_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.DIS_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLC_dict["CMCSA"] = round(((float(self.CMCSA_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.CMCSA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLC_dict

    # ROE for XLC tickers
    def ROE_XLC(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLC_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLC_dict["FB"] = round((float(self.FB_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.FB_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLC_dict["GOOGL"] = round((float(self.GOOGL_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.GOOGL_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLC_dict["NFLX"] = round((float(self.NFLX_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.NFLX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLC_dict["DIS"] = round((float(self.DIS_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.DIS_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLC_dict["CMCSA"] = round((float(self.CMCSA_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.CMCSA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLC_dict

    # free cash flow for XLC tickers
    def free_cash_XLC(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLC_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLC_dict["FB"] = float(self.FB_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.FB_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLC_dict["GOOGL"] = float(self.GOOGL_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.GOOGL_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLC_dict["NFLX"] = float(self.NFLX_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.NFLX_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLC_dict["DIS"] = (float(self.DIS_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.DIS_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLC_dict["CMCSA"] = (float(self.CMCSA_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.CMCSA_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLC_dict
"""
XLC = Sector_Analysis_XLC()
print(XLC.ROE_XLC())
print(XLC.free_cash_XLC())
print(XLC.EPS_XLC())
print(XLC.BVPS_XLC())
print(XLC.debt_equity_XLC())
"""

class Sector_Analysis_XLRE:
    def __init__(self):
        self.tickerListXlRE = ["AMT", "PLD", "CCI", "EQIX", "PSA"]

        # will need to read each ticker's json file as a python dictionary

        # this block is for the ticker's balance sheets
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/AMTJson/AMTbalance.json",
                'r') as f:
            self.AMT_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PLDJson/PLDbalance.json",
                'r') as f:
            self.PLD_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CCIJson/CCIbalance.json",
                'r') as f:
            self.CCI_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/EQIXJson/EQIXbalance.json",
                'r') as f:
            self.EQIX_balance_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PSAJson/PSAbalance.json",
                'r') as f:
            self.PSA_balance_sheet = json.load(f)

        # this block is for the ticker's cash statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/AMTJson/AMTcash.json",
                'r') as f:
            self.AMT_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PLDJson/PLDcash.json",
                'r') as f:
            self.PLD_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CCIJson/CCIcash.json",
                'r') as f:
            self.CCI_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/EQIXJson/EQIXcash.json",
                'r') as f:
            self.EQIX_cash_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PSAJson/PSAcash.json",
                'r') as f:
            self.PSA_cash_sheet = json.load(f)

        # this block is for the ticker's income statements
        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/AMTJson/AMTincome.json",
                'r') as f:
            self.AMT_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PLDJson/PLDincome.json",
                'r') as f:
            self.PLD_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/CCIJson/CCIincome.json",
                'r') as f:
            self.CCI_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/EQIXJson/EQIXincome.json",
                'r') as f:
            self.EQIX_income_sheet = json.load(f)

        with open(
                "/Users/ishaandas/Documents/FinancialAnalysis/Financial-Analysis/SectorFinAnalysisJson/PSAJson/PSAincome.json",
                'r') as f:
            self.PSA_income_sheet = json.load(f)

    # function for XLRE ticker's BVPS
    def BVPS_XLRE(self):
        # dictionary that returns BVPS for each ticker
        BVPS_XLRE_dict = {}

        # adds each ticker's BVPS to the dictionary
        BVPS_XLRE_dict["AMT"] = round((float(
            self.AMT_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.AMT_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLRE_dict["PLD"] = round((float(
            self.PLD_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.PLD_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLRE_dict["CCI"] = round((float(
            self.CCI_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.CCI_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLRE_dict["EQIX"] = round((float(
            self.EQIX_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.EQIX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        BVPS_XLRE_dict["PSA"] = round((float(
            self.PSA_balance_sheet["annualReports"][0]["totalShareholderEquity"]) / float(
            self.PSA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        return BVPS_XLRE_dict

    # EPS for XLRE tickers
    def EPS_XLRE(self):
        # dictionary that returns the EPS for each ticker
        EPS_XLRE_dict = {}

        # adds each ticker's EPS to the dictionary
        EPS_XLRE_dict["AMT"] = round((float(self.AMT_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.AMT_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLRE_dict["PLD"] = round((float(self.PLD_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.PLD_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLRE_dict["CCI"] = round((float(self.CCI_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.CCI_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLRE_dict["EQIX"] = round((float(self.EQIX_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.EQIX_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)
        EPS_XLRE_dict["PSA"] = round((float(self.PSA_income_sheet["annualReports"][0]["grossProfit"]) / float(
            self.PSA_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])), 3)

        # returns the final dictionary
        return EPS_XLRE_dict

    # debt to equity for XLRE tickers
    def debt_equity_XLRE(self):
        # dictionary that contains tickers' debt to equity ratios
        DE_XLRE_dict = {}

        # adds tickers' corresponding EPS to the dictionary
        DE_XLRE_dict["AMT"] = round(((float(self.AMT_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.AMT_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLRE_dict["PLD"] = round(((float(self.PLD_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.PLD_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLRE_dict["CCI"] = round(((float(self.CCI_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.CCI_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLRE_dict["EQIX"] = round(((float(self.EQIX_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.EQIX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        DE_XLRE_dict["PSA"] = round(((float(self.PSA_balance_sheet["annualReports"][0]["totalLiabilities"])) / float(
            self.PSA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return DE_XLRE_dict

    # ROE for XLRE tickers
    def ROE_XLRE(self):
        # dictionary that will contain the ticker and their ROE
        ROE_XLRE_dict = {}

        # adds tickers' corresponding ROE to the dictionary
        ROE_XLRE_dict["AMT"] = round((float(self.AMT_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.AMT_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLRE_dict["PLD"] = round((float(self.PLD_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.PLD_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLRE_dict["CCI"] = round((float(self.CCI_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.CCI_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLRE_dict["EQIX"] = round((float(self.EQIX_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.EQIX_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)
        ROE_XLRE_dict["PSA"] = round((float(self.PSA_cash_sheet["annualReports"][0]["netIncome"]) / float(
            self.PSA_balance_sheet["annualReports"][0]["totalShareholderEquity"])), 3)

        # returns the final dictionary
        return ROE_XLRE_dict

    # free cash flow for XLRE tickers
    def free_cash_XLRE(self):
        # dictionary that contains the ticker and their free cash flow
        FREE_CASH_XLRE_dict = {}

        # adds the ticker and corresponding free cash flow to the dictionary
        FREE_CASH_XLRE_dict["AMT"] = float(self.AMT_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.AMT_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLRE_dict["PLD"] = float(self.PLD_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.PLD_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLRE_dict["CCI"] = float(self.CCI_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.CCI_cash_sheet["annualReports"][0]["capitalExpenditures"])
        FREE_CASH_XLRE_dict["EQIX"] = (float(self.EQIX_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.EQIX_cash_sheet["annualReports"][0]["capitalExpenditures"]))
        FREE_CASH_XLRE_dict["PSA"] = (float(self.PSA_cash_sheet["annualReports"][0]["operatingCashflow"]) - float(
            self.PSA_cash_sheet["annualReports"][0]["capitalExpenditures"]))

        # returns the final dictionary
        return FREE_CASH_XLRE_dict

"""
XLRE = Sector_Analysis_XLRE()
print(XLRE.EPS_XLRE())
print(XLRE.BVPS_XLRE())
print(XLRE.ROE_XLRE())
print(XLRE.debt_equity_XLRE())
print(XLRE.free_cash_XLRE())
"""

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

FA = Financial_Analysis("AAPL")
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
FA.rank_cash_flow_to_debt()
FA.past_historic_revenue_rank()
FA.current_historic_revenue_rank()
FA.past_historic_net_income_rank()
FA.current_historic_net_income_rank()
FA.rank_net_income_margin()
FA.past_historic_gross_profit_rank()
FA.current_historic_gross_profit_rank()
FA.rank_gross_profit_margin()
FA.rank_leverage()
FA.rank_total_asset_turnover()
print(FA.total_rank())
print(FA.five_ytd_change())
print(FA.compare_rank_return())


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
