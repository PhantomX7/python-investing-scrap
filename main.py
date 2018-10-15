from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
from Stock import Stock
import json

base_url = "https://www.investing.com"
index_url = "https://www.investing.com/equities/indonesia"



def getHtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url=url, headers=headers)
    return urlopen(req).read()


def main():
    stockList = []

    index_soup = BeautifulSoup(getHtml(index_url), 'html.parser')
    for row in index_soup.find_all("tr", id=re.compile('^pair_')):
        # print(row)
        stockList.append(Stock(row.find('a').string, row.get('id')[5::], row.find('a').get('href')))

    # for stock in stockList:
    #     print(f'{stock.name} - {stock.id}')
    fetchBalanceSheetAnnual(stockList)
    fetchIncomeStatementAnnual(stockList)

    data = {}
    # for stock in stockList:
    stock = stockList[0]
    data[stock.name] = {
        'balance_sheet': stock.balance_sheet,
        'income_statement':stock.income_statement
    }
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)


def fetchBalanceSheetAnnual(stockList):
    for stock in stockList:
        # stock = stockList[0]
        balance_sheet_soup = BeautifulSoup(getHtml('https://www.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID={stock.id}&report_type=BAL&period_type=Annual'),
            'html.parser')

        # check if api exist, some api doesnt exist that cause error to be thrown
        if (balance_sheet_soup.find('tr', id="header_row") == None): continue

        # get years
        years = []
        for idx, year in enumerate(balance_sheet_soup.find('tr', id="header_row").find_all('span')):
            # skip the header
            if(idx == 0): continue
            # put in year and skip if empty
            if (year.string):
                years.append(year.string)
            else:
                years.append('-')
        print(stock.name + '-' + stock.id+' balance sheet')

        balance_sheet = {}
        datas = ["Total Current Assets", "Total Assets", "Total Current Liabilities", "Total Liabilities",
                 "Total Equity",
                 "Total Liabilities & Shareholders' Equity", "Total Common Shares Outstanding",
                 "Total Preferred Shares Outstanding"]
        for row in balance_sheet_soup.find('tbody').find_all('tr'):
            if (row.find('table')): continue
            column = row.find_all('td')

            if (column[0].find('span').contents[0] in datas):
                balance_sheet[column[0].find('span').contents[0]] = {
                    years[0]: column[1].string,
                    years[1]: column[2].string,
                    years[2]: column[3].string,
                    years[3]: column[4].string,
                }

        stock.setBalanceSheet(balance_sheet)

        print(balance_sheet)

def fetchIncomeStatementAnnual(stockList):
    for stock in stockList:
        stock = stockList[0]
        income_statement_soup = BeautifulSoup(getHtml('https://www.investing.com/instruments/Financials/changereporttypeajax?action=change_report_type&pair_ID={stock.id}&report_type=INC&period_type=Annual'),'html.parser')

        # check if api exist, some api doesnt exist that cause error to be thrown
        if (income_statement_soup.find('tr', id="header_row") == None): continue

        # get years
        years = []
        for idx, year in enumerate(income_statement_soup.find('tr', id="header_row").find_all('span')):
            # skip the header
            if(idx == 0): continue
            # put in year and skip if empty
            if (year.string):
                years.append(year.string)
            else:
                years.append('-')
        # print(stock.name + '-' + stock.id+' balance sheet')
        # print(years)

        income_statement={}
        datas=["Net Income"]
        for row in income_statement_soup.find('tbody').find_all('tr'):
            if (row.find('table')): continue
            column = row.find_all('td')

            if (column[0].find('span').contents[0] in datas):
                income_statement[column[0].find('span').contents[0]] = {
                    years[0]: column[1].string,
                    years[1]: column[2].string,
                    years[2]: column[3].string,
                    years[3]: column[4].string,
                }

        stock.setIncomeStatement(income_statement)
        print(income_statement)



if __name__ == "__main__":
    main()
