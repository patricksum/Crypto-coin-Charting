# Coin Charting 4 charts per row, 2hr candle-stick in last 7 days
# modify the following: 
# 1. save result (pdf) in figpath P:\VCCY (Windows file format)
# 2. Data are from Binance, get your API keys
#   open account by https://www.binance.com/en/register?ref=FGZBIG41  (U get 10% and I get 10% rebate)
#   You may also open KUCOIN account https://www.kucoin.com/ucenter/signup?rcode=7sw1bf
# 3. update the arrary ,lc, below to include your favourites

import pandas as pd
import numpy as np
import datetime as dt
import math
# import investpy as ipy
import matplotlib.pyplot as plt  # https://matplotlib.org/
# import mplfinance as mpf
# from mpl_finance import candlestick2_ohlc
from mplfinance.original_flavor import candlestick2_ohlc
# binance data
from binance.client import Client
from binance.websockets import BinanceSocketManager

# get your own API keys (from Binance)
api_key="yr key"
api_secret="yr secret"

client = Client(api_key, api_secret)

# -- list of coins 
lc = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "LTCUSDT",
      "DOTUSDT", "1INCHUSDT", "SNXUSDT", "DOGEUSDT",
      "AAVEUSDT", "COMPUSDT", "SOLUSDT", "SRMUSDT",
      "UNIUSDT", "MANAUSDT", "AUDIOUSDT", "LINKUSDT",
      "ZRXUSDT", "ETHUPUSDT", "BTCUPUSDT", "BTCDOWNUSDT"]
#      "USDT",

# location to save the result in windows file system
figpath="P:\\VCCY\\"  #"D:\\python\\data\\

# 7-day every 2 hour
def gethistdata(coin):
    # fetch klines from Binance
	# klines = client.get_historical_klines(coin, Client.KLINE_INTERVAL_2HOUR, "7 day ago UTC")
    candles = client.get_klines(symbol=coin, interval=Client.KLINE_INTERVAL_2HOUR)

    cols = ["optime", "open", "high", "low", "close", "vol", "cltime", "quoteAV", "trades", "takerbuybase", "takerbuyquote", "ingore"]
    df = pd.DataFrame(candles, columns=cols)
    df.optime = pd.to_datetime(df.optime+8*3600*1000, unit='ms')  # convert to UTC+8
    df.cltime = pd.to_datetime(df.cltime+8*3600*1000, unit='ms')  # convert to UTC+8
    df = df.set_index('optime')
    df.open = pd.to_numeric(df.open)
    df.high = pd.to_numeric(df.high)
    df.low = pd.to_numeric(df.open)
    df.close = pd.to_numeric(df.close)
    df.vol = pd.to_numeric(df.vol)
    return df.iloc[-83:].copy()


# -- set start date and end date
now = dt.datetime.now().strftime("%H:%M")
end_date = dt.date.today().strftime("%Y/%m/%d") +" "+ now
start_date = (dt.date.today() - dt.timedelta(days=7)).strftime("%Y/%m/%d") +" "+ now

fig = plt.figure(figsize = (15,12))
# plt.title("Coins list - "+start_date+" to "+end_date)
fig.suptitle("Coins 7-day charts - "+start_date+" to "+end_date)

# -- axis controller
maxcol = 4
i = 0 # row index
j = 0 # column index (0,maxcol)
lastrow= np.ceil(len(lc) / maxcol) -1 # count from 0
la=[]

for coin in lc:

    # -- download coin data to dataframe
    
    data = gethistdata(coin)

    # -- construct the chart
    la.append(plt.subplot2grid((int(lastrow+1),maxcol), (i,j)))

    avg_priceD = client.get_avg_price(symbol=coin)
    avg_price  = float(avg_priceD["price"])
    titleline = coin[0:len(coin)-4] if "USDT" in coin else coin
    signnum = 8
    la[-1].title.set_text(titleline +" "+str(round(avg_price,signnum-int(math.log10(abs(avg_price)))-1)))
    la[-1].set_xticks(range(0, len(data.index), 10))
    la[-1].set_xticklabels(data.index[::10].strftime("%Y-%m-%d %H:0"))

    candlestick2_ohlc(la[-1], opens=data["open"], highs=data["high"], lows=data["low"], closes=data["close"],
                      width=0.5, colorup="green", colordown="red", alpha=1)
    j+=1
    
    if i < lastrow:
        plt.setp(la[-1].get_xticklabels(), visible=False)
    else:
        plt.setp(la[-1].xaxis.get_majorticklabels(), rotation=90)
        
    if j > maxcol -1:
        i+=1
        j=0
fig.savefig(figpath+"coinfig-"+dt.date.today().strftime("%Y%m%d")+dt.datetime.now().strftime("%H%M")+".pdf")        
# plt.show()