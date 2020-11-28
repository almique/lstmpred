import pymongo
import datetime
from datetime import timedelta
from typing import List, Optional
import controllers.enumeration

class buysell():
    Datetobuy: datetime
    Datetosell: datetime
    datebuy_Predictions: float
    datesell_Pridictions: float
    filename: str
    Profit: float

class dataobject():
    Date: datetime
    Predictions: float
    filename: str

def month_check(month):
    if month > 0 and month <= 12: ## If month is between 1 and 12, return True.
        return True
    else:
        return False

def day_check(month, day):
    days_in_month = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    if 0 < day <= days_in_month[month]:
        return True
    else:
        return False


def get_closing_price(querydate, stockname) -> dataobject:
  myclient = pymongo.MongoClient("mongodb://lstmpredt:lstm09%40@lstmpreds-shard-00-00.8clst.mongodb.net:27017,lstmpreds-shard-00-01.8clst.mongodb.net:27017,lstmpreds-shard-00-02.8clst.mongodb.net:27017/lstmcloseprice?ssl=true&replicaSet=atlas-13r59k-shard-0&authSource=admin&retryWrites=true&w=majority")
  mydb = myclient["lstmcloseprice"]
  mycol = mydb["lstmpreds"]
  myquery = {"Date": {"$eq": querydate} , "Filename": stockname +'.csv'}  # for example - 2015-07-20   857.771545  ASIANPAINT.csv
  mydoc = mycol.find(myquery)
  if not mydoc:
    return 0
  else:
    for x in mydoc:
      ob = dataobject()
      ob.Date = x['Date']
      ob.Predictions = x['Predictions']
      ob.filename = stockname
      return ob

def get_closing_price_forweek(querydate, querydateend, stockname) -> List[dataobject]:
  myclient = pymongo.MongoClient("mongodb://lstmpredt:lstm09%40@lstmpreds-shard-00-00.8clst.mongodb.net:27017,lstmpreds-shard-00-01.8clst.mongodb.net:27017,lstmpreds-shard-00-02.8clst.mongodb.net:27017/lstmcloseprice?ssl=true&replicaSet=atlas-13r59k-shard-0&authSource=admin&retryWrites=true&w=majority")
  mydb = myclient["lstmcloseprice"]
  mycol = mydb["lstmpreds"]
  myquery = {"Date": {'$lte': querydateend, '$gte': querydate} , "Filename": stockname +'.csv'}  # for example - 2015-07-20   857.771545  ASIANPAINT.csv
  mydoc = mycol.find(myquery)
  if not mydoc:
    return 0
  else:
    arr = []
    for x in mydoc:
        ob = dataobject()
        ob.Date = x['Date']
        ob.Predictions = x['Predictions']
        ob.filename = stockname
        arr.append(ob)
    return arr
    
def buy_and_sell_helper(prices):
  maxprofit, last = 0, 0
  minprice = float('inf')
  for i in range(len(prices)):
      if prices[i] < minprice:
          minprice = prices[i]
      elif prices[i] - minprice > maxprofit:
          maxprofit = prices[i] - minprice
          last = prices[i]
  return [minprice, last, maxprofit]

def best_time_to_buy_and_sell(querydate, querydateend, stockname) -> buysell:
    nums = []
    dicta = {}
    myclient = pymongo.MongoClient("mongodb://lstmpredt:lstm09%40@lstmpreds-shard-00-00.8clst.mongodb.net:27017,lstmpreds-shard-00-01.8clst.mongodb.net:27017,lstmpreds-shard-00-02.8clst.mongodb.net:27017/lstmcloseprice?ssl=true&replicaSet=atlas-13r59k-shard-0&authSource=admin&retryWrites=true&w=majority")
    mydb = myclient["lstmcloseprice"]
    mycol = mydb["lstmpreds"]
    myquery = {"Date": {'$lte': querydateend, '$gte': querydate} , "Filename": stockname +'.csv'}  # for example - 2015-07-20   857.771545  ASIANPAINT.csv
    mydoc = mycol.find(myquery)
    if not mydoc:
        return 0
    else:
        for x in mydoc:
            dicta[x['Predictions']] = x['Date']
            nums.append(x['Predictions'])
        #print(nums)
        info_l = buy_and_sell_helper(nums)
        #print(info_l)
        if info_l[1] == 0 or info_l[2] == 0:
            return 0
        else:
            ob = buysell()
            ob.Datetobuy = dicta[info_l[0]]
            ob.Datetosell = dicta[info_l[1]]
            ob.datebuy_Predictions =info_l[0]
            ob.datesell_Pridictions = info_l[1]
            ob.Profit = info_l[2]
            return ob
      