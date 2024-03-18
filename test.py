from configparser import ConfigParser
from fugle_trade.sdk import SDK
from fugle_trade.order import OrderObject
from fugle_trade.constant import (APCode, Trade, PriceFlag, BSFlag, Action)
import yfinance as yf
import pandas as pd
# 台股
# 讀取設定檔
config = ConfigParser()
config.read('./config.ini')
# 登入
sdk = SDK(config)
sdk.login()
# 庫存明細
inventories = sdk.get_inventories()
#print(inventories)
TW_value = 0
balance = sdk.get_balance().get("available_balance")
for stock in inventories:
    stk_na = stock.get("stk_na", "unknown")
    value_now = stock.get("value_now","0")
    TW_value += int(value_now)
    #print(f"stock name : {stk_na}, value : {value_now}")
TW_asset = TW_value + balance
print(f"TW value : {TW_value}\nbalance : {balance}\nTW asset : {TW_asset}")

# 美股
portfolio_df = pd.read_csv('./portfolio.csv')
US_value = 0
"""
stock = yf.Ticker("AAPL")
info = stock.info
for key in info.keys():
    print(key)
"""
for index, row in portfolio_df.iterrows():
    stock = yf.Ticker(row['symbol'])
    stock_info = stock.info
    current_price = stock.info['currentPrice']
    shares = row['shares']
    stock_value = shares * current_price
    US_value += stock_value
currency_usd_twd = yf.Ticker("USDTWD=X").info.get("regularMarketPreviousClose")
US_value *= currency_usd_twd
print(f"US value : {US_value}")
total_asset = US_value + TW_asset
print(f"total asset : {total_asset}")