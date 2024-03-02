import requests
import traceback

from src.api import database
from src.model.FundamentalData import CompanyOverview, IncomeStatement, BalanceSheet, CashFlow, Earnings

# https://www.alphavantage.co/support/#api-key
apikey = "RSNV5C041ETQCGWI"


def company_overview(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={apikey}'
        url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo"

        # 使用 format() 方法替换字符串
        url = url.format(symbol=symbol, apikey=apikey)
        print(url)

        r = requests.get(url)
        data = r.json()

        #　属性名の変換
        entity = CompanyOverview.from_json(data)

        # データ登録
        # database.save(entity)

        # データ登録
        entity = entity.to_json()
        database.insert(CompanyOverview, **entity)
    except:
        print("company_overview except:")
        traceback.print_exc()
    else:
        return data
    finally:
        pass

def income_statement(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={apikey}'

        url = "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo"

        # 使用 format() 方法替换字符串
        url = url.format(symbol=symbol, apikey=apikey)
        print(url)

        r = requests.get(url)
        data = r.json()

        # 遍历 list 并添加新属性
        entities = []
        for report in data['annualReports']:
            report["ReportType"] = "annualReports"
            report["Symbol"] = data["symbol"]
            entities.append(IncomeStatement.from_json(report))

        for report in data['quarterlyReports']:
            report["ReportType"] = "quarterlyReports"
            report["Symbol"] = data["symbol"]
            entities.append(IncomeStatement.from_json(report))

        # データ登録
        database.save_many(*entities)
    except:
        print("income_statement except:")
        traceback.print_exc()
    else:
        return data
    finally:
        pass



def balance_sheet(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={apikey}'
        url = "https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo"

        # 使用 format() 方法替换字符串
        url = url.format(symbol=symbol, apikey=apikey)
        print(url)

        r = requests.get(url)
        data = r.json()

        # 遍历 list 并添加新属性
        entities = []
        for report in data['annualReports']:
            report["ReportType"] = "annualReports"
            report["Symbol"] = data["symbol"]
            entities.append(BalanceSheet.from_json(report))

        for report in data['quarterlyReports']:
            report["ReportType"] = "quarterlyReports"
            report["Symbol"] = data["symbol"]
            entities.append(BalanceSheet.from_json(report))

        # データ登録
        database.save_many(*entities)
    except:
        print("balance_sheet insert except:")
        traceback.print_exc()
    else:
        return data
    finally:
        pass


def cash_flow(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={apikey}'
        url = "https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=demo"

        # 使用 format() 方法替换字符串
        url = url.format(symbol=symbol, apikey=apikey)
        print(url)

        r = requests.get(url)
        data = r.json()

        # 遍历 list 并添加新属性
        entities = []
        for report in data['annualReports']:
            report["ReportType"] = "annualReports"
            report["Symbol"] = data["symbol"]
            entities.append(CashFlow.from_json(report))

        for report in data['quarterlyReports']:
            report["ReportType"] = "quarterlyReports"
            report["Symbol"] = data["symbol"]
            entities.append(CashFlow.from_json(report))

        # データ登録
        database.save_many(*entities)
    except:
        print("balance_sheet insert except:")
        traceback.print_exc()
    else:
        return data
    finally:
        pass


def earnings(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={apikey}'
        url = "https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo"

        # 使用 format() 方法替换字符串
        url = url.format(symbol=symbol, apikey=apikey)
        print(url)

        r = requests.get(url)
        data = r.json()

        # 遍历 list 并添加新属性
        entities = []
        for report in data['annualEarnings']:
            report["ReportType"] = "annualReports"
            report["Symbol"] = data["symbol"]
            entities.append(Earnings.from_json(report))

        for report in data['quarterlyEarnings']:
            report["ReportType"] = "quarterlyReports"
            report["Symbol"] = data["symbol"]
            entities.append(Earnings.from_json(report))

        # データ登録
        database.save_many(*entities)
    except:
        print("balance_sheet insert except:")
        traceback.print_exc()
    else:
        return data
    finally:
        pass


def listing_status(symbol):
    try:
        # Querying all active stocks and ETFs as of the latest trading day:
        # https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo

        #  Querying all delisted stocks and ETFs as of 2014-07-10:
        # https://www.alphavantage.co/query?function=LISTING_STATUS&date=2014-07-10&state=delisted&apikey=demo

        url = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo'
        url = "https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo"

    except:
        print("balance_sheet insert except:")
        traceback.print_exc()
    else:
        pass
    finally:
        pass