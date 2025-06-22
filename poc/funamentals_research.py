import requests
import yfinance as yf

def get_history(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1mo")
        if df.empty:
            print("No historical data found.")
            return {}
        jsonData = {}
        for index, date in enumerate(df.index):
            jsonData[str(date).split(' ')[0]] = {}
            for col in df.columns:
                jsonData[str(date).split(' ')[0]][col] = df.loc[date][col]
        print(jsonData)
        return jsonData
    except Exception as e:
        print(f"Error fetching history for {ticker}: {e}")
        return e

def get_cashflow(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.cashflow
        if df.empty:
            print("No cashflow data found.")
            return {}
        jsonData = {}
        for index, date in enumerate(df.index):
            jsonData[str(date)] = {}
            for col in df.columns:
                jsonData[str(date)][str(col).split(' ')[0]] = df.loc[date][col]
        return jsonData
    except Exception as e:
        print(f"Error fetching cashflow for {ticker}: {e}")
        return {}

def get_incomestatement(ticker):
    try:
        stock = yf.Ticker(ticker)
        df = stock.incomestmt
        if df.empty:
            print("No income statement data found.")
            return {}
        jsonData = {}
        for index, date in enumerate(df.index):
            jsonData[str(date)] = {}
            for col in df.columns:
                jsonData[str(date)][str(col).split(' ')[0]] = df.loc[date][col]
        return jsonData
    except Exception as e:
        print(f"Error fetching income statement for {ticker}: {e}")
        return {}

def aggregate_financial_data(symbol):
    return {
        "income_statement": get_incomestatement(symbol),
        "history": get_history(symbol),
        "cash_flow": get_cashflow(symbol),
    }