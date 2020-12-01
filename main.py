from typing import Optional
from typing import List
from fastapi import FastAPI, Path
import pymongo
import datetime
from datetime import timedelta
from controllers.fetchquery import *
from controllers.enumeration import *


app = FastAPI(
    title="LSTM-RNN BASED PREDICTION QUERY API",
    description="An AWS and Mongodb based query System"
)

@app.post("/get_closing_price_app",
summary = "Get the Closing Price",
description = "Get Closing price of the desired date and stock",
tags=["Get the Closing Price"]
)
def get_closing_price_app(Year: int, Month: int, Day: int , stockname: StockName):
  yyyy, mm, dd = Year, Month, Day
  if month_check(int(mm)) and day_check(int(mm),int(dd)):
    querydate = datetime.datetime(int(yyyy), int(mm), int(dd), 00, 00, 00)
    return get_closing_price(querydate, stockname)
  else:
    return 0

@app.post("/get_closing_price_app_week",
summary = "Get the Closing Price for the Week",
description = "Get Closing price of the week for a stock",
tags=["Get the Closing Price For The Week"]
)
def get_closing_price_app_week(Year: int, Month: int, Day: int , stockname: StockName):
  yyyy, mm, dd = Year, Month, Day
  if month_check(int(mm)) and day_check(int(mm),int(dd)):
    querydate = datetime.datetime(int(yyyy), int(mm), int(dd), 00, 00, 00)
    querydateend = datetime.datetime(int(yyyy), int(mm), int(dd), 00, 00, 00) + timedelta(weeks = 1)
    return get_closing_price_forweek(querydate, querydateend , stockname)
  else:
    return 0

@app.post("/best_time",
summary = "Best Time To Buy And Sell Stock",
description = "Find out which is the best time to buy and sell for max profit(for any year)",
tags=["Best Time To Buy And Sell Stock/Profit"]
)
def best_time(Year: int, stockname: StockName):
  yyyy = Year
  querydate = datetime.datetime(int(yyyy), 1, 1, 00, 00, 00)
  querydateend = datetime.datetime(int(yyyy), 1, 1, 00, 00, 00) + timedelta(weeks = 52)
  return best_time_to_buy_and_sell(querydate, querydateend , stockname)

@app.post("/best_Stock",
summary = "Best Stock As Per Profit Throughout the year",
description = "Find out which is the best stock to buy and sell for max profit(for any year)",
tags=["Best Stock To Buy as per Profit In That Year"]
)
def best_Stock(Year: int, stockname: List[StockName]):
  yyyy = Year
  querydate = datetime.datetime(int(yyyy), 1, 1, 00, 00, 00)
  querydateend = datetime.datetime(int(yyyy), 1, 1, 00, 00, 00) + timedelta(weeks = 52)
  return best_Stock_to_buy_and_sell(querydate, querydateend , stockname)
